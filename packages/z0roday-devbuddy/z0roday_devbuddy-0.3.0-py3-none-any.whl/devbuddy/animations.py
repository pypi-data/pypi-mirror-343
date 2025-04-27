# animations.py
import sys
import time
import itertools
import os
import platform
import random

def animate_install(tool_name):
    """Nice animation for installation process."""
    spinner = itertools.cycle(['⣾', '⣽', '⣻', '⢿', '⡿', '⣟', '⣯', '⣷'])
    
    # Fallback for terminals that don't support Unicode
    if platform.system() == 'Windows' and not os.environ.get('WT_SESSION'):  # Not in Windows Terminal
        spinner = itertools.cycle(['|', '/', '-', '\\'])
    
    print(f"Installing {tool_name}...", end='', flush=True)
    
    for _ in range(20):
        sys.stdout.write('\r' + f"Installing {tool_name}... " + next(spinner))
        sys.stdout.flush()
        time.sleep(0.1)
    
    print("\r" + f"Installing {tool_name}... Done!      ", flush=True)

def animate_progress(message, duration=2.0):
    """Show a progress bar animation with a custom message."""
    width = 30
    for i in range(width + 1):
        progress = i / width
        bar = "█" * i + "░" * (width - i)
        percentage = int(progress * 100)
        
        # Print progress bar
        sys.stdout.write(f"\r{message} [{bar}] {percentage}%")
        sys.stdout.flush()
        
        # Simulate variable speed - starts slower, speeds up in the middle, slows down at end
        if i < width // 3:
            sleep_time = (duration / width) * 1.5
        elif i > width * 2 // 3:
            sleep_time = (duration / width) * 1.5
        else:
            sleep_time = (duration / width) * 0.5
            
        time.sleep(sleep_time)
    
    sys.stdout.write(f"\r{message} [{'█' * width}] 100%\n")
    sys.stdout.flush()

def show_success(message):
    """Display a success message with a nice animation."""
    for i in range(3):
        for c in ["⣿", "⢿", "⡿", "⣟", "⣯", "⣷"]:
            sys.stdout.write(f"\r✅ {message} {c}")
            sys.stdout.flush()
            time.sleep(0.05)
    sys.stdout.write(f"\r✅ {message}    \n")
    sys.stdout.flush()

def show_error(message):
    """Display an error message with a nice animation."""
    for i in range(3):
        sys.stdout.write(f"\r❌ {message} ")
        sys.stdout.flush()
        time.sleep(0.1)
        sys.stdout.write(f"\r   {message} ")
        sys.stdout.flush()
        time.sleep(0.1)
    sys.stdout.write(f"\r❌ {message}\n")
    sys.stdout.flush()

def show_completion(project_name, project_type):
    """Show a fancy completion message for project scaffold."""
    colors = {
        'reset': '\033[0m',
        'green': '\033[92m',
        'blue': '\033[94m',
        'yellow': '\033[93m',
        'red': '\033[91m',
        'cyan': '\033[96m',
        'magenta': '\033[95m'
    }
    
    # Don't show colors if terminal doesn't support them
    if platform.system() == 'Windows' and not os.environ.get('WT_SESSION'):
        for key in colors:
            colors[key] = ''
    
    # Cool project complete message
    print("\n" + "=" * 60)
    print(f"{colors['green']}✨ Project {project_name} created successfully! ✨{colors['reset']}")
    print(f"{colors['blue']}Type: {colors['yellow']}{project_type}{colors['reset']}")
    print(f"{colors['magenta']}Created by z0roday's DevBuddy{colors['reset']}")
    print(f"{colors['cyan']}🚀 Next steps:{colors['reset']}")
    print(f"  cd {project_name}")
    
    if project_type in ['python', 'flask', 'django', 'fastapi']:
        print("  python -m venv venv")
        print("  source venv/bin/activate  # On Windows: venv\\Scripts\\activate")
        print("  pip install -r requirements.txt")
        
        if project_type == 'flask':
            print("  python app.py")
        elif project_type == 'django':
            print("  python manage.py migrate")
            print("  python manage.py runserver")
        elif project_type == 'fastapi':
            print("  uvicorn main:app --reload")
    elif project_type in ['react', 'next', 'vue', 'angular']:
        print("  npm install")
        print("  npm start")
    elif project_type == 'go':
        print("  go run main.go")
    elif project_type == 'rust':
        print("  cargo run")
    
    print("=" * 60)