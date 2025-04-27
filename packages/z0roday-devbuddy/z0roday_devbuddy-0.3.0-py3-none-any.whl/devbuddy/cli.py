import click
import os
import sys
import shutil
import subprocess
import json
import platform
import time
from .formatter import format_code
from .scaffolder import scaffold_project
from .animations import animate_install, animate_progress, show_success
from .plugins import register_plugin_commands

@click.group()
def cli():
    """z0roday's DevBuddy - Automate your coding tasks!"""
    pass

@cli.command()
def hello():
    """Say hello from z0roday!"""
    click.echo("Hello from z0roday's DevBuddy!")

@cli.command()
@click.argument('path', default='.', type=click.Path(exists=True))
@click.option('--tool', default='black', type=click.Choice(['black', 'autopep8', 'yapf', 'isort']), help='Formatting tool to use')
@click.option('--git', is_flag=True, help='Format only git-modified files')
@click.option('--recursive', is_flag=True, help='Format files in subdirectories')
def format(path, tool, git, recursive):
    """Format Python code in the given path."""
    click.echo(f"Formatting code in: {path} with {tool}")
    format_code(path, tool=tool, use_git=git, recursive=recursive)

@cli.command()
@click.argument('project') 
@click.option('--dockerize', is_flag=True, help='Create the project with Docker support')
@click.option('--git-init', is_flag=True, help='Initialize git repository')
@click.option('--with-tests', is_flag=True, help='Set up testing framework')
@click.option('--auto-ci', is_flag=True, help='Create CI/CD configuration')
def create(project, dockerize, git_init, with_tests, auto_ci):
    """Create a new project (e.g., dbuddy create flask-app [--dockerize])."""
    if '-' not in project:
        raise click.UsageError("Please use format: <type>-<n>, e.g., flask-app")
    
    project_type, project_name = project.split('-', 1)
    supported_types = ['python', 'flask', 'django', 'fastapi', 'react', 'next', 'vue', 
                       'express', 'angular', 'laravel', 'spring', 'go', 'rust', 'dotnet']
    
    if project_type not in supported_types:
        raise click.UsageError(f"Unsupported project type: {project_type}. Supported types: {', '.join(supported_types)}")
    
    click.echo(f"Creating {project_type} project: {project_name}")
    if dockerize:
        click.echo("With Docker support")
    if git_init:
        click.echo("With Git initialization")
    if with_tests:
        click.echo("With testing framework")
    if auto_ci:
        click.echo("With CI/CD configuration")
        
    scaffold_project(project_name, project_type=project_type, dockerize=dockerize, 
                    git_init=git_init, with_tests=with_tests, auto_ci=auto_ci)

@cli.command()
@click.argument('framework_group')
def install(framework_group):
    """Install frameworks for a specific language (e.g., dbuddy install js-frameworks)."""
    animate_install(framework_group)
    
    if framework_group == 'js-frameworks':
        if not shutil.which("node"):
            click.echo("Node.js is not installed. Please install it from: https://nodejs.org/")
            return
        for dep in ["@vue/cli", "create-react-app", "@angular/cli", "next"]:
            subprocess.run(["npm", "install", "-g", dep], check=True, shell=True)
            click.echo(f"Installed {dep} successfully!")
            
    elif framework_group == 'php-frameworks':
        if not shutil.which("php") or not shutil.which("composer"):
            click.echo("PHP and Composer are required. Install PHP from: https://www.php.net/downloads.php and Composer from: https://getcomposer.org/download/")
            return
        subprocess.run(["composer", "global", "require", "laravel/installer"], check=True)
        click.echo("Installed Laravel installer successfully!")
        
    elif framework_group == 'java-frameworks':
        if not shutil.which("java"):
            click.echo("Java is required. Install it from: https://www.oracle.com/java/technologies/javase-downloads.html")
            return
        click.echo("Java frameworks like Spring Boot require manual setup with Maven/Gradle.")
        
    elif framework_group == 'python-frameworks':
        if not shutil.which("python") and not shutil.which("python3"):
            click.echo("Python is required. Install it from: https://www.python.org/downloads/")
            return
        for dep in ["flask", "django", "fastapi", "uvicorn", "pytest", "sphinx"]:
            subprocess.run([sys.executable, "-m", "pip", "install", dep], check=True)
            click.echo(f"Installed {dep} successfully!")
            
    else:
        raise click.UsageError("Supported groups: js-frameworks, php-frameworks, java-frameworks, python-frameworks")

@cli.command()
@click.argument('path', default='.', type=click.Path(exists=True))
def analyze(path):
    """Analyze code quality and suggest improvements."""
    if not os.path.exists(path):
        click.echo(f"Error: Path {path} does not exist.")
        return
        
    # Check for Python files
    has_python = any(f.endswith('.py') for f in os.listdir(path) if os.path.isfile(os.path.join(path, f)))
    if has_python:
        if not shutil.which("pylint"):
            click.echo("Installing pylint for code analysis...")
            subprocess.run([sys.executable, "-m", "pip", "install", "pylint"], check=True)
            
        click.echo(f"Analyzing Python code in {path}...")
        try:
            subprocess.run(["pylint", path], check=False)
        except subprocess.CalledProcessError:
            click.echo("Analysis completed with some issues.")
    else:
        click.echo(f"No Python files found in {path}. Only Python analysis is currently supported.")

@cli.command()
@click.argument('package_name')
def docs(package_name):
    """Generate documentation for a Python package."""
    try:
        # Ensure sphinx is installed
        subprocess.run([sys.executable, "-m", "pip", "install", "sphinx", "sphinx-rtd-theme"], check=True)
        
        # Create docs directory
        os.makedirs(f"docs/{package_name}", exist_ok=True)
        
        # Initialize sphinx
        subprocess.run(["sphinx-quickstart", "--quiet", "--project", package_name, 
                        "--author", "z0roday", f"docs/{package_name}"], check=True)
        
        click.echo(f"Documentation initialized for {package_name} in docs/{package_name}")
        click.echo("To build: cd docs && make html")
    except subprocess.SubprocessError as e:
        click.echo(f"Error generating documentation: {e}")

@cli.command()
@click.argument('template', type=click.Choice(['gitignore', 'dockerfile', 'readme', 'license']))
@click.option('--lang', help='Language for gitignore template (e.g. python, node)')
def generate(template, lang):
    """Generate common project files from templates."""
    if template == 'gitignore':
        content = ""
        if lang == 'python':
            content = "*.pyc\n__pycache__/\nvenv/\n.env\n.vscode/\n.idea/\n*.egg-info/\ndist/\nbuild/\n"
        elif lang == 'node':
            content = "node_modules/\n*.log\ndist/\n.env\n.vscode/\n.idea/\n"
        elif lang == 'java':
            content = "*.class\n*.jar\ntarget/\n.idea/\n.vscode/\n"
        else:
            content = "# Basic .gitignore\n.env\n.vscode/\n.idea/\ntmp/\ntemp/\n"
        
        with open('.gitignore', 'w') as f:
            f.write(content)
        click.echo("Generated .gitignore file")
        
    elif template == 'dockerfile':
        content = """FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "main.py"]
"""
        with open('Dockerfile', 'w') as f:
            f.write(content)
        click.echo("Generated Dockerfile")
        
    elif template == 'readme':
        project_name = os.path.basename(os.getcwd())
        content = f"""# {project_name}

A cool project by z0roday!

## Installation

```
pip install -r requirements.txt
```

## Usage

```
python main.py
```

## License

MIT
"""
        with open('README.md', 'w') as f:
            f.write(content)
        click.echo("Generated README.md")
        
    elif template == 'license':
        content = """MIT License

Copyright (c) 2023 z0roday

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
        with open('LICENSE', 'w') as f:
            f.write(content)
        click.echo("Generated LICENSE file")

@cli.command()
@click.argument('path', default='.', type=click.Path(exists=True))
@click.option('--package-manager', type=click.Choice(['pip', 'npm', 'composer']), help='Package manager to use')
@click.option('--only-outdated', is_flag=True, help='List only outdated packages')
def update_deps(path, package_manager, only_outdated):
    """Check for updates in project dependencies and optionally update them."""
    if not os.path.exists(path):
        click.echo(f"Error: Path {path} does not exist.")
        return
    
    # Auto-detect package manager if not specified
    if not package_manager:
        if os.path.exists(os.path.join(path, 'requirements.txt')):
            package_manager = 'pip'
        elif os.path.exists(os.path.join(path, 'package.json')):
            package_manager = 'npm'
        elif os.path.exists(os.path.join(path, 'composer.json')):
            package_manager = 'composer'
        else:
            click.echo("Could not detect package manager. Please specify with --package-manager")
            return
    
    click.echo(f"Checking dependencies with {package_manager}...")
    
    try:
        if package_manager == 'pip':
            if only_outdated:
                subprocess.run([sys.executable, "-m", "pip", "list", "--outdated"], check=True)
            else:
                subprocess.run([sys.executable, "-m", "pip", "list"], check=True)
                
            if click.confirm("Do you want to update outdated packages?"):
                animate_progress("Updating Python packages", 1.0)
                if os.path.exists(os.path.join(path, 'requirements.txt')):
                    subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "-r", "requirements.txt"], check=True)
                else:
                    subprocess.run([sys.executable, "-m", "pip", "list", "--outdated", "--format=json"], check=True, capture_output=True, text=True)
                    
        elif package_manager == 'npm':
            if only_outdated:
                subprocess.run(["npm", "outdated"], cwd=path, check=False)
            else:
                subprocess.run(["npm", "list", "--depth=0"], cwd=path, check=False)
                
            if click.confirm("Do you want to update outdated packages?"):
                animate_progress("Updating NPM packages", 1.0)
                subprocess.run(["npm", "update"], cwd=path, check=True)
                
        elif package_manager == 'composer':
            if only_outdated:
                subprocess.run(["composer", "outdated"], cwd=path, check=False)
            else:
                subprocess.run(["composer", "show", "--installed"], cwd=path, check=True)
                
            if click.confirm("Do you want to update outdated packages?"):
                animate_progress("Updating Composer packages", 1.0)
                subprocess.run(["composer", "update"], cwd=path, check=True)
                
        show_success("Dependency check completed!")
    except subprocess.CalledProcessError as e:
        click.echo(f"Error checking dependencies: {e}")

@cli.command()
@click.argument('env_type', type=click.Choice(['python', 'node', 'laravel', 'react', 'vue', 'django']))
@click.option('--path', default='.', type=click.Path(exists=True), help='Project path')
@click.option('--install-deps', is_flag=True, help='Install dependencies automatically')
def setup_env(env_type, path, install_deps):
    """Set up a development environment for a specific project type."""
    project_dir = os.path.abspath(path)
    
    click.echo(f"Setting up {env_type} environment in {project_dir}")
    animate_progress(f"Setting up {env_type} environment", 1.0)
    
    try:
        if env_type == 'python':
            venv_dir = os.path.join(project_dir, 'venv')
            if not os.path.exists(venv_dir):
                subprocess.run([sys.executable, '-m', 'venv', venv_dir], check=True)
                click.echo("Virtual environment created at ./venv")
                
                # Create activation scripts guide
                if platform.system() == 'Windows':
                    click.echo("Activate with: .\\venv\\Scripts\\activate")
                else:
                    click.echo("Activate with: source venv/bin/activate")
            
            if install_deps and os.path.exists(os.path.join(project_dir, 'requirements.txt')):
                if platform.system() == 'Windows':
                    pip_path = os.path.join(venv_dir, 'Scripts', 'pip')
                else:
                    pip_path = os.path.join(venv_dir, 'bin', 'pip')
                    
                subprocess.run([pip_path, 'install', '-r', 'requirements.txt'], check=True)
                click.echo("Dependencies installed from requirements.txt")
                
        elif env_type in ['node', 'react', 'vue']:
            if not os.path.exists(os.path.join(project_dir, 'package.json')):
                subprocess.run(['npm', 'init', '-y'], cwd=project_dir, check=True)
                click.echo("Created package.json")
                
            if env_type == 'react':
                subprocess.run(['npx', 'create-react-app', '.'], cwd=project_dir, check=True)
                click.echo("React environment set up")
                
            elif env_type == 'vue':
                subprocess.run(['npx', '@vue/cli', 'create', '.', '--default'], cwd=project_dir, check=True)
                click.echo("Vue environment set up")
            
            if install_deps and os.path.exists(os.path.join(project_dir, 'package.json')):
                subprocess.run(['npm', 'install'], cwd=project_dir, check=True)
                click.echo("Dependencies installed from package.json")
                
        elif env_type == 'laravel':
            if not shutil.which('composer'):
                click.echo("Composer not found. Please install Composer first.")
                return
                
            if not os.path.exists(os.path.join(project_dir, 'composer.json')):
                subprocess.run(['composer', 'create-project', '--prefer-dist', 'laravel/laravel', '.'], 
                               cwd=project_dir, check=True)
                click.echo("Laravel environment set up")
            
            if install_deps:
                subprocess.run(['composer', 'install'], cwd=project_dir, check=True)
                click.echo("Dependencies installed from composer.json")
                
        elif env_type == 'django':
            venv_dir = os.path.join(project_dir, 'venv')
            if not os.path.exists(venv_dir):
                subprocess.run([sys.executable, '-m', 'venv', venv_dir], check=True)
                click.echo("Virtual environment created at ./venv")
                
            # Install Django in the venv
            if platform.system() == 'Windows':
                pip_path = os.path.join(venv_dir, 'Scripts', 'pip')
            else:
                pip_path = os.path.join(venv_dir, 'bin', 'pip')
                
            subprocess.run([pip_path, 'install', 'django'], check=True)
            click.echo("Django installed in virtual environment")
            
            # Check if it's already a Django project
            if not os.path.exists(os.path.join(project_dir, 'manage.py')):
                if platform.system() == 'Windows':
                    django_admin_path = os.path.join(venv_dir, 'Scripts', 'django-admin')
                else:
                    django_admin_path = os.path.join(venv_dir, 'bin', 'django-admin')
                
                project_name = os.path.basename(project_dir)
                subprocess.run([django_admin_path, 'startproject', project_name, '.'], 
                               cwd=project_dir, check=True)
                click.echo(f"Django project '{project_name}' created")
        
        show_success(f"{env_type.capitalize()} environment setup completed!")
    except subprocess.CalledProcessError as e:
        click.echo(f"Error setting up environment: {e}")

@cli.group()
def plugin():
    """Manage DevBuddy plugins."""
    pass

@plugin.command('list')
def plugin_list():
    """List all installed plugins."""
    plugin_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'plugins')
    os.makedirs(plugin_dir, exist_ok=True)
    
    plugins = [name for name in os.listdir(plugin_dir) 
               if os.path.isdir(os.path.join(plugin_dir, name)) and 
               not name.startswith('__')]
    
    if not plugins:
        click.echo("No plugins installed.")
        return
        
    click.echo("Installed plugins:")
    for plugin in plugins:
        click.echo(f"  - {plugin}")

@plugin.command('install')
@click.argument('plugin_name')
@click.option('--url', help='Git repository URL')
def plugin_install(plugin_name, url):
    """Install a plugin from a Git repository."""
    plugin_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'plugins')
    os.makedirs(plugin_dir, exist_ok=True)
    
    if not url:
        url = f"https://github.com/z0roday/devbuddy-plugin-{plugin_name}.git"
    
    target_dir = os.path.join(plugin_dir, plugin_name)
    
    if os.path.exists(target_dir):
        if click.confirm(f"Plugin {plugin_name} already exists. Update it?"):
            try:
                os.chdir(target_dir)
                subprocess.run(['git', 'pull'], check=True)
                click.echo(f"Plugin {plugin_name} updated successfully!")
            except (subprocess.CalledProcessError, FileNotFoundError) as e:
                click.echo(f"Error updating plugin: {e}")
        return
    
    try:
        animate_progress(f"Installing plugin {plugin_name}", 1.0)
        subprocess.run(['git', 'clone', url, target_dir], check=True)
        
        # Check if a setup.py exists and install the plugin
        if os.path.exists(os.path.join(target_dir, 'setup.py')):
            subprocess.run([sys.executable, '-m', 'pip', 'install', '-e', target_dir], check=True)
            
        show_success(f"Plugin {plugin_name} installed successfully!")
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        click.echo(f"Error installing plugin: {e}")

@plugin.command('remove')
@click.argument('plugin_name')
def plugin_remove(plugin_name):
    """Remove an installed plugin."""
    plugin_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'plugins')
    target_dir = os.path.join(plugin_dir, plugin_name)
    
    if not os.path.exists(target_dir):
        click.echo(f"Plugin {plugin_name} is not installed.")
        return
    
    try:
        # Uninstall if it was installed as a package
        if os.path.exists(os.path.join(target_dir, 'setup.py')):
            subprocess.run([sys.executable, '-m', 'pip', 'uninstall', '-y', plugin_name], check=True)
            
        # Remove the directory
        shutil.rmtree(target_dir)
        click.echo(f"Plugin {plugin_name} removed successfully!")
    except Exception as e:
        click.echo(f"Error removing plugin: {e}")

# Register plugin commands
register_plugin_commands(cli)

if __name__ == "__main__":
    cli()