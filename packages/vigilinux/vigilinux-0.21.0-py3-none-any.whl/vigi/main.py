

import os
import platform
import sys
import subprocess
import time
import threading
from dotenv import load_dotenv
from .config import settings, Colors
from .openai_api import generate_shell_command, is_command_safe
from .utils import colorize
from pathlib import Path
from .env_var import set_gemini_api_key
import itertools
home_path = Path.home()
# print(home_path)


MAX_RETRIES = 500  # Limit retries to prevent infinite loops
TIMEOUT = 10000    # Maximum time (in seconds) before killing a command


class LoadingDots:
    def __init__(self, message="Processing"):
        self.message = message
        self.running = False
        self.thread = None
        # Using a cycle of Unicode characters for a smooth spinner animation.
        self.spinner = itertools.cycle(['⣾','⣽','⣻','⢿','⡿','⣟','⣯','⣷'])

    def start(self):
        self.running = True
        self.thread = threading.Thread(target=self._animate)
        self.thread.start()

    def _animate(self):
        while self.running:
            spin_char = next(self.spinner)
            sys.stdout.write(f'\r{self.message} {spin_char}')
            sys.stdout.flush()
            time.sleep(0.1)

    def stop(self):
        self.running = False
        if self.thread is not None:
            self.thread.join()
        # Clear the line after stopping the spinner
        sys.stdout.write('\r' + ' ' * (len(self.message) + 2) + '\r')
        sys.stdout.flush()

def load_env_vars():
    load_dotenv()
    return os.getenv("GEMINI_API_KEY")  # Updated to use Gemini API key

def read_config():
    return settings["command_execution_confirmation"], settings["security_check"], settings["gemini_model_config"]

def recognize_operating_system():
    return platform.system()

def read_user_command():
    return " ".join(sys.argv[1:])

def execute_command_with_interaction(shell_command, timeout=TIMEOUT):
    """
    Executes a command while handling interactive prompts, timeouts, and showing real-time output.
    - Detects if a process is waiting for user input and asks for confirmation.
    - Ensures the command doesn't hang indefinitely.
    - Returns both stdout and stderr for AI analysis if it fails.
    """
    print(colorize(f"EXECUTING: {shell_command}", Colors.OKGREEN))

    process = subprocess.Popen(
        shell_command,
        shell=True,
        # executable='/bin/bash',
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        stdin=subprocess.PIPE,
        text=True
    )

    stdout_lines = []
    stderr_lines = []

    def read_output(stream, output_list, is_stderr=False):
        """ Reads and prints process output line by line. """
        for line in iter(stream.readline, ''):
            output_list.append(line)
            print(line.strip())  # Print real-time output

            # Detect if command is prompting for user input
            if "Continue?" in line or "yes/no" in line or "y/n" in line.lower():
                user_response = input("🔹 Enter response: ") + "\n"
                process.stdin.write(user_response)
                process.stdin.flush()
    stdout_thread = threading.Thread(target=read_output, args=(process.stdout, stdout_lines))
    stderr_thread = threading.Thread(target=read_output, args=(process.stderr, stderr_lines, True))

    stdout_thread.start()
    stderr_thread.start()
    


    # Timeout handling
    start_time = time.time()
    while process.poll() is None:
        if time.time() - start_time > timeout:
            print(colorize("⏳ Timeout reached! Terminating process...", Colors.FAIL))
            process.terminate()
            return None, "Process timed out."

    stdout_thread.join()
    stderr_thread.join()
    # Ensure the process has terminated and get its return code
    process.wait()
    stdout = ''.join(stdout_lines)
    stderr = ''.join(stderr_lines)

    if process.returncode != 0:
        raise subprocess.CalledProcessError(process.returncode, shell_command, output=stdout, stderr=stderr)

    return stdout, stderr

def execute_with_retry(user_command, shell_command, security_check, gemini_api_key, gemini_model_config, command_execution_confirmation, operating_system, retry_count=0):
    """
    Executes a command and retries intelligently if it fails.
    - Provides AI with full error context to generate improved commands.
    - Detects errors related to missing dependencies, incorrect paths, and permissions.
    - Stops retrying after reaching MAX_RETRIES.
    """
    try:
        execute_command_with_interaction(shell_command)
        print(colorize("✅ Command executed successfully!", Colors.OKGREEN))
        return  # Exit function if successful

    except subprocess.CalledProcessError as e:
        error_message = e.stderr.strip() if e.stderr else str(e)
        print(colorize(f"❌ ERROR: Command execution failed.\n🔍 Exact Error: {error_message}", Colors.FAIL))
        print(colorize(f"💀 Failed Command: {shell_command}", Colors.WARNING))

        # If max retries reached, stop
        if retry_count >= MAX_RETRIES:
            print(colorize("⚠️ Max retries reached. Aborting execution.", Colors.FAIL))
            return

        print(colorize("🔄 Retrying with AI-generated improvements...", Colors.WARNING))

        # Generate a new fixed command with full error context
        retry_prompt = (
    f"User's original request: '{user_command}'.\n"
    f"Previously generated command that failed: '{shell_command}'.\n"
    f"Exact error message from execution: '{error_message}'.\n"
    "Generate a **fixed** Windows shell command (either Command Prompt or PowerShell) that correctly achieves the user's goal, avoids previous errors, and ensures correct paths, dependencies, and permissions.\n"
    "Important:\n"
    "- If the error indicates a missing command, provide the correct installation command for Windows (e.g., using 'choco', 'winget', or 'pip').\n"
    "- If the error involves permission issues, add 'runas' if necessary, or suggest running the command as Administrator.\n"
    "- If the error is due to an existing directory, add '/Y' if supported for automatic overwrite.\n"
    "- Make sure the fixed command is executable in Windows Command Prompt or PowerShell.\n"
        )


        loader = LoadingDots("🧠 Asking AI for a better solution...\n")
        loader.start()
        new_shell_command = generate_shell_command(retry_prompt, gemini_api_key, gemini_model_config)
        loader.stop()


        print(colorize(f"🆕 New AI-generated command: {new_shell_command}", Colors.OKCYAN))

        # Retry with the improved command
        execute_with_retry(user_command, new_shell_command, security_check, gemini_api_key, gemini_model_config, command_execution_confirmation, operating_system, retry_count + 1)

def main():
    # Load environment variables
    gemini_api_key = set_gemini_api_key
    # Read config settings
    command_execution_confirmation, security_check, gemini_model_config = read_config()

    # Recognize the operating system
    operating_system = recognize_operating_system()

    # Read user command
    user_command = read_user_command()

    # Convert natural language to a shell command
    #sex
    
    
    loader = LoadingDots("💡 Generating shell command")
    loader.start()
    shell_command = generate_shell_command(user_command, gemini_api_key, gemini_model_config)
    loader.stop()


 

    # Process and execute the command with retry mechanism
    execute_with_retry(user_command, shell_command, security_check, gemini_api_key, gemini_model_config, command_execution_confirmation, operating_system)

if __name__ == "__main__":
    main()