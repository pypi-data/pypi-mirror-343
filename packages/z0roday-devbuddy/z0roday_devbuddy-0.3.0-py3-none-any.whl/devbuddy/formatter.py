import subprocess
import os
import glob
import sys

def format_code(path, tool='black', use_git=False, recursive=False):
    """Format Python files in the given path using the specified tool."""
    try:
        if use_git:
            result = subprocess.run(['git', 'status', '--porcelain'], capture_output=True, text=True, check=True)
            files = [line.split()[1] for line in result.stdout.splitlines() if line.strip() and line.split()[1].endswith('.py')]
            if not files:
                print("No modified Python files found in git.")
                return
            paths_to_format = files
        else:
            if recursive and os.path.isdir(path):
                # Find all .py files recursively in the directory
                paths_to_format = glob.glob(f"{path}/**/*.py", recursive=True)
                if not paths_to_format:
                    print(f"No Python files found in {path}.")
                    return
            elif os.path.isdir(path):
                # Find only .py files in the current directory
                paths_to_format = glob.glob(f"{path}/*.py")
                if not paths_to_format:
                    print(f"No Python files found in {path}.")
                    return
            else:
                # Single file
                paths_to_format = [path]

        # Check if the tool is installed
        try:
            subprocess.run([tool, "--version"], capture_output=True, check=True)
        except (FileNotFoundError, subprocess.CalledProcessError):
            print(f"Tool {tool} not found. Installing...")
            subprocess.run([sys.executable, "-m", "pip", "install", tool], check=True)
    
        # Apply formatting
        print(f"Formatting {len(paths_to_format)} files with {tool}...")
        
        if tool == 'black':
            subprocess.run([tool] + paths_to_format, check=True)
        elif tool == 'autopep8':
            subprocess.run([tool, '--in-place', '--aggressive', '--aggressive'] + paths_to_format, check=True)
        elif tool == 'yapf':
            subprocess.run([tool, '--in-place'] + paths_to_format, check=True)
        elif tool == 'isort':
            subprocess.run([tool] + paths_to_format, check=True)
        
        print(f"Code formatted successfully with {tool}!")

    except subprocess.CalledProcessError as e:
        print(f"Error: Something went wrong while formatting with {tool}: {e}")
    except FileNotFoundError:
        print(f"Error: {tool} is not installed. Run 'pip install {tool}' to install it.")
    except subprocess.SubprocessError as e:
        print(f"Error: Could not process commands: {e}")
        if use_git:
            print("Are you in a git repository?")
    except Exception as e:
        print(f"Unexpected error: {str(e)}")