# z0roday's DevBuddy

A powerful CLI tool to automate common developer tasks, scaffold projects, and boost productivity.

## Features

- 🚀 **Project Scaffolding**: Create new projects with various frameworks (Python, Flask, Django, FastAPI, React, Vue, Angular, and more)
- 🔍 **Code Formatting**: Format your Python code with popular tools like Black, Autopep8, YAPF, and isort
- 📊 **Code Analysis**: Analyze code quality with Pylint
- 📝 **Documentation**: Generate documentation scaffolds with Sphinx
- 🐳 **Docker Support**: Create Dockerfiles and docker-compose.yml files for your projects
- 🧪 **Testing**: Set up testing frameworks for your projects
- 🔧 **Development Tools**: Install framework dependencies and tools
- 🔄 **Auto-update**: Keep your tools and dependencies updated
- 🛠️ **Environment Setup**: Automatically set up development environments
- 🧩 **Plugin System**: Extend functionality with plugins
- 🔍 **CI/CD Integration**: Create CI/CD configuration for GitHub Actions

## Installation

```bash
pip install z0roday-devbuddy
```

Or install directly from GitHub:

```bash
pip install git+https://github.com/z0roday/devbuddy.git
```

## Usage

### Creating a new project

```bash
# Create a Flask project
dbuddy create flask-myapp

# Create a React project with Docker support
dbuddy create react-myapp --dockerize

# Create a Django project with Git initialization and testing
dbuddy create django-myapp --git-init --with-tests

# Create a FastAPI project with CI/CD configuration
dbuddy create fastapi-myapp --auto-ci
```

### Formatting code

```bash
# Format all Python files in current directory with black
dbuddy format .

# Format using a specific tool and only git-staged files
dbuddy format . --tool autopep8 --git

# Format all files recursively
dbuddy format . --recursive
```

### Installing frameworks

```bash
# Install JavaScript frameworks
dbuddy install js-frameworks

# Install Python frameworks
dbuddy install python-frameworks
```

### Analyzing code

```bash
# Analyze Python code in current directory
dbuddy analyze .
```

### Generating documentation

```bash
# Generate documentation for a package
dbuddy docs mypackage
```

### Generating template files

```bash
# Generate a .gitignore file for Python
dbuddy generate gitignore --lang python

# Generate a Dockerfile
dbuddy generate dockerfile

# Generate a README.md
dbuddy generate readme

# Generate a LICENSE file
dbuddy generate license
```

### New Features

```bash
# Check for updates in project dependencies
dbuddy update-deps

# Update only outdated packages with npm
dbuddy update-deps --package-manager npm --only-outdated

# Setup development environment with one command
dbuddy setup-env python --install-deps

# Setup a Django environment
dbuddy setup-env django

# List installed plugins
dbuddy plugin list

# Install a plugin
dbuddy plugin install example

# Remove a plugin
dbuddy plugin remove example

# Use a plugin command (if example plugin is installed)
dbuddy system-info
dbuddy count-lines file.py
```

## Supported Project Types

- Python: Basic Python project
- Flask: Flask web application
- Django: Django web application
- FastAPI: FastAPI web API
- React: React frontend application
- Next.js: Next.js React framework
- Vue: Vue.js frontend application
- Express: Express.js Node backend
- Angular: Angular frontend framework
- Laravel: PHP Laravel framework
- Spring: Java Spring Boot framework
- Go: Go web application
- Rust: Rust web application
- .NET: ASP.NET Core web API

## Plugin System

DevBuddy supports plugins to extend its functionality. You can install plugins from Git repositories:

```bash
dbuddy plugin install my-plugin
```

To create your own plugin, create a Python package with the following structure:

```
devbuddy-plugin-myplugin/
├── __init__.py
└── ... other files
```

In your `__init__.py`, define a `register_commands` function:

```python
def register_commands(cli_group):
    @cli_group.command()
    def my_command():
        """My custom command."""
        print("Hello from my plugin!")
```

## Contributing

Contributions are welcome! Feel free to open issues or submit pull requests.

## License

MIT License
