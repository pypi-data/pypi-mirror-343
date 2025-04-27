import os
import subprocess
import shutil
import sys
from .animations import animate_install, show_completion, animate_progress

def check_prerequisites(project_type):
    """Check if required tools are installed for the project type."""
    if project_type in ['python', 'flask', 'django', 'fastapi']:
        if not shutil.which("python") and not shutil.which("python3"):
            print("Error: Python is not installed. Download from: https://www.python.org/downloads/")
            return False
        if project_type == 'django' and not shutil.which("django-admin"):
            print("Installing Django...")
            animate_install("Django")
            subprocess.run([sys.executable, "-m", "pip", "install", "django"], check=True)
        elif project_type == 'flask':
            print("Installing Flask...")
            animate_install("Flask")
            subprocess.run([sys.executable, "-m", "pip", "install", "flask"], check=True)
        elif project_type == 'fastapi':
            print("Installing FastAPI and Uvicorn...")
            animate_install("FastAPI")
            subprocess.run([sys.executable, "-m", "pip", "install", "fastapi", "uvicorn"], check=True)
    elif project_type in ['react', 'next', 'vue', 'express', 'angular']:
        if not shutil.which("node") or not shutil.which("npm"):
            print("Error: Node.js and npm are required. Download from: https://nodejs.org/")
            return False
        if project_type == 'vue' and not shutil.which("vue"):
            print("Installing Vue CLI...")
            animate_install("Vue CLI")
            subprocess.run(["npm", "install", "-g", "@vue/cli"], check=True)
        elif project_type == 'angular' and not shutil.which("ng"):
            print("Installing Angular CLI...")
            animate_install("Angular CLI")
            subprocess.run(["npm", "install", "-g", "@angular/cli"], check=True)
    elif project_type == 'laravel':
        if not shutil.which("composer"):
            print("Error: Composer is required. Download from: https://getcomposer.org/download/")
            return False
    elif project_type == 'spring':
        if not shutil.which("java"):
            print("Error: Java is required for Spring Boot. Download from: https://www.oracle.com/java/technologies/javase-downloads.html")
            return False
    elif project_type == 'go':
        if not shutil.which("go"):
            print("Error: Go is required. Download from: https://golang.org/dl/")
            return False
    elif project_type == 'rust':
        if not shutil.which("cargo"):
            print("Error: Rust and Cargo are required. Download from: https://www.rust-lang.org/tools/install")
            return False
    elif project_type == 'dotnet':
        if not shutil.which("dotnet"):
            print("Error: .NET SDK is required. Download from: https://dotnet.microsoft.com/download")
            return False
    return True

def create_docker_file(project_name, project_type):
    """Create appropriate Dockerfile based on project type."""
    dockerfile_path = os.path.join(project_name, "Dockerfile")
    docker_compose_path = os.path.join(project_name, "docker-compose.yml")
    
    # Create default Docker files based on project type
    if project_type in ['python', 'flask', 'fastapi']:
        with open(dockerfile_path, 'w') as f:
            f.write(f"""FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

{f'CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]' if project_type == 'fastapi' else f'CMD ["python", "{"app.py" if project_type == "flask" else "main.py"}"]'}
""")
        
        with open(docker_compose_path, 'w') as f:
            f.write(f"""version: '3'

services:
  app:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - .:/app
""")
            
    elif project_type == 'django':
        with open(dockerfile_path, 'w') as f:
            f.write("""FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
""")
        
        with open(docker_compose_path, 'w') as f:
            f.write("""version: '3'

services:
  web:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - .:/app
    depends_on:
      - db
  
  db:
    image: postgres:13
    environment:
      - POSTGRES_DB=postgres
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=postgres
    volumes:
      - postgres_data:/var/lib/postgresql/data/

volumes:
  postgres_data:
""")
            
    elif project_type in ['react', 'vue', 'angular']:
        with open(dockerfile_path, 'w') as f:
            f.write("""FROM node:14-alpine

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

RUN npm run build

# Production stage
FROM nginx:alpine
COPY --from=0 /app/build /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
""")
        
        with open(docker_compose_path, 'w') as f:
            f.write("""version: '3'

services:
  app:
    build: .
    ports:
      - "80:80"
""")
            
    elif project_type == 'go':
        with open(dockerfile_path, 'w') as f:
            f.write("""FROM golang:1.18-alpine AS builder

WORKDIR /app
COPY go.* ./
RUN go mod download
COPY . .
RUN go build -o main .

FROM alpine:latest
COPY --from=builder /app/main /app/main
CMD ["/app/main"]
""")
            
    elif project_type == 'rust':
        with open(dockerfile_path, 'w') as f:
            f.write("""FROM rust:1.70 as builder

WORKDIR /app
COPY . .
RUN cargo build --release

FROM debian:buster-slim
COPY --from=builder /app/target/release/app /usr/local/bin/app
CMD ["app"]
""")
            
    print(f"Docker configuration created for {project_type} project")

def setup_testing(project_name, project_type):
    """Set up testing framework based on project type."""
    if project_type in ['python', 'flask', 'django', 'fastapi']:
        # Create a tests directory
        os.makedirs(os.path.join(project_name, "tests"), exist_ok=True)
        
        # Create an __init__.py file in the tests directory
        with open(os.path.join(project_name, "tests", "__init__.py"), 'w') as f:
            f.write("# Tests for the project\n")
            
        # Create a sample test file
        with open(os.path.join(project_name, "tests", "test_basic.py"), 'w') as f:
            f.write("""import pytest

def test_sample():
    assert True
""")
            
        # Create a conftest.py file
        with open(os.path.join(project_name, "tests", "conftest.py"), 'w') as f:
            f.write("""import pytest

# Define fixtures here
""")
            
        # Ensure pytest is installed
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", "pytest"], check=True)
        except Exception as e:
            print(f"Warning: Could not install pytest: {e}")
            
    elif project_type in ['react', 'next', 'vue']:
        # These frameworks already have testing set up by default
        print(f"Testing is already set up by default for {project_type}")
        
    elif project_type == 'golang':
        # Create a tests directory
        with open(os.path.join(project_name, "main_test.go"), 'w') as f:
            f.write("""package main

import "testing"

func TestSample(t *testing.T) {
    // Add tests here
}
""")
    
    print(f"Testing framework set up for {project_type}")

def setup_ci_cd(project_name, project_type):
    """Set up CI/CD configuration for the project."""
    # Create .github/workflows directory
    workflows_dir = os.path.join(project_name, ".github", "workflows")
    os.makedirs(workflows_dir, exist_ok=True)
    
    workflow_filename = os.path.join(workflows_dir, "main.yml")
    
    if project_type in ['python', 'flask', 'django', 'fastapi']:
        with open(workflow_filename, 'w') as f:
            f.write("""name: Python CI

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.9'
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
        pip install pytest
    - name: Lint with flake8
      run: |
        pip install flake8
        flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
    - name: Test with pytest
      run: |
        pytest
""")
    elif project_type in ['react', 'next', 'vue', 'angular', 'express']:
        with open(workflow_filename, 'w') as f:
            f.write("""name: Node.js CI

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Use Node.js
      uses: actions/setup-node@v2
      with:
        node-version: '14'
    - name: Install dependencies
      run: |
        npm ci
    - name: Build
      run: |
        npm run build --if-present
    - name: Test
      run: |
        npm test --if-present
""")
    elif project_type == 'go':
        with open(workflow_filename, 'w') as f:
            f.write("""name: Go CI

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Set up Go
      uses: actions/setup-go@v2
      with:
        go-version: 1.18
    - name: Build
      run: go build -v ./...
    - name: Test
      run: go test -v ./...
""")
    elif project_type == 'rust':
        with open(workflow_filename, 'w') as f:
            f.write("""name: Rust CI

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Build
      run: cargo build --verbose
    - name: Run tests
      run: cargo test --verbose
""")
    elif project_type == 'dotnet':
        with open(workflow_filename, 'w') as f:
            f.write("""name: .NET CI

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Setup .NET
      uses: actions/setup-dotnet@v1
      with:
        dotnet-version: 6.0.x
    - name: Restore dependencies
      run: dotnet restore
    - name: Build
      run: dotnet build --no-restore
    - name: Test
      run: dotnet test --no-build --verbosity normal
""")
    
    print(f"CI/CD configuration created for {project_type} project")

def scaffold_project(project_name, project_type='python', dockerize=False, git_init=False, with_tests=False, auto_ci=False):
    """Scaffold a new project with basic files for various frameworks."""
    if not check_prerequisites(project_type):
        return
    
    try:
        animate_progress(f"Creating {project_type} project structure", 1.5)
        
        os.makedirs(project_name, exist_ok=True)
        
        with open(f"{project_name}/README.md", 'w') as f:
            f.write(f"# {project_name}\nA cool project by z0roday!")
        
        with open(f"{project_name}/.gitignore", 'w') as f:
            if project_type in ['python', 'flask', 'django', 'fastapi']:
                f.write("*.pyc\n__pycache__/\nvenv/\n.env\n.vscode/\n.idea/\n*.egg-info/\ndist/\nbuild/\n")
            elif project_type in ['react', 'next', 'vue', 'express', 'angular']:
                f.write("node_modules/\n*.log\ndist/\n.env\n.vscode/\n.idea/\npackage-lock.json\n")
            elif project_type == 'laravel':
                f.write("vendor/\n*.log\n.env\n.vscode/\n.idea/\n")
            elif project_type == 'spring':
                f.write("*.class\n*.jar\ntarget/\n.idea/\n.vscode/\n.settings/\n")
            elif project_type == 'go':
                f.write("*.exe\n*.exe~\n*.dll\n*.so\n*.dylib\nvendor/\n.env\n.vscode/\n.idea/\n")
            elif project_type == 'rust':
                f.write("target/\nCargo.lock\n.env\n.vscode/\n.idea/\n")
            elif project_type == 'dotnet':
                f.write("bin/\nobj/\n.vs/\n.vscode/\n.idea/\n")

        if project_type == 'python':
            with open(f"{project_name}/main.py", 'w') as f:
                f.write('def main():\n    print("Hello from z0roday!")\n\nif __name__ == "__main__":\n    main()\n')

            with open(f"{project_name}/requirements.txt", 'w') as f:
                f.write("# Add your dependencies here\n")
                
        elif project_type == 'flask':
            with open(f"{project_name}/app.py", 'w') as f:
                f.write('from flask import Flask, render_template\n\napp = Flask(__name__)\n\n@app.route("/")\ndef hello():\n    return render_template("index.html", title="z0roday Flask App")\n\nif __name__ == "__main__":\n    app.run(debug=True)\n')
            
            os.makedirs(f"{project_name}/templates", exist_ok=True)
            with open(f"{project_name}/templates/index.html", 'w') as f:
                f.write('<!DOCTYPE html>\n<html>\n<head>\n    <title>{{ title }}</title>\n</head>\n<body>\n    <h1>Hello from z0roday!</h1>\n</body>\n</html>\n')
            
            with open(f"{project_name}/requirements.txt", 'w') as f:
                f.write("flask==2.3.3\n")
                
        elif project_type == 'django':
            subprocess.run(['django-admin', 'startproject', 'config', project_name], check=True)
            
            # Create an app within the Django project
            original_dir = os.getcwd()
            os.chdir(project_name)
            subprocess.run(['python', 'manage.py', 'startapp', 'core'], check=True)
            os.chdir(original_dir)
            
            with open(f"{project_name}/requirements.txt", 'w') as f:
                f.write("django==4.2.4\n")
                
        elif project_type == 'fastapi':
            with open(f"{project_name}/main.py", 'w') as f:
                f.write('from fastapi import FastAPI\nfrom pydantic import BaseModel\n\napp = FastAPI(title="z0roday FastAPI")\n\nclass Item(BaseModel):\n    name: str\n    description: str = None\n\n@app.get("/")\ndef read_root():\n    return {"message": "Hello from z0roday!"}\n\n@app.post("/items/")\ndef create_item(item: Item):\n    return item\n')
            
            with open(f"{project_name}/requirements.txt", 'w') as f:
                f.write("fastapi==0.103.1\nuvicorn==0.23.2\npydantic==2.3.0\n")
                
        elif project_type == 'react':
            subprocess.run(['npx', 'create-react-app', '.'], cwd=project_name, check=True)
            
        elif project_type == 'next':
            subprocess.run(['npx', 'create-next-app@latest', '.', '--ts'], cwd=project_name, check=True)
            
        elif project_type == 'vue':
            subprocess.run(['npx', '@vue/cli', 'create', '.', '--default'], cwd=project_name, check=True)
            
        elif project_type == 'express':
            os.makedirs(f"{project_name}/src", exist_ok=True)
            os.makedirs(f"{project_name}/public", exist_ok=True)
            
            with open(f"{project_name}/src/index.js", 'w') as f:
                f.write('const express = require("express");\nconst path = require("path");\n\nconst app = express();\nconst PORT = process.env.PORT || 3000;\n\napp.use(express.json());\napp.use(express.static(path.join(__dirname, "../public")));\n\napp.get("/api", (req, res) => {\n    res.json({ message: "Hello from z0roday!" });\n});\n\napp.listen(PORT, () => {\n    console.log(`Server running on port ${PORT}`);\n});\n')
            
            with open(f"{project_name}/public/index.html", 'w') as f:
                f.write('<!DOCTYPE html>\n<html>\n<head>\n    <title>z0roday Express App</title>\n</head>\n<body>\n    <h1>Hello from z0roday!</h1>\n    <div id="app"></div>\n    <script>\n        fetch("/api")\n            .then(response => response.json())\n            .then(data => {\n                document.getElementById("app").textContent = data.message;\n            });\n    </script>\n</body>\n</html>\n')
            
            with open(f"{project_name}/package.json", 'w') as f:
                f.write('{\n  "name": "' + project_name + '",\n  "version": "1.0.0",\n  "main": "src/index.js",\n  "scripts": {\n    "start": "node src/index.js",\n    "dev": "nodemon src/index.js"\n  },\n  "dependencies": {\n    "express": "^4.18.2"\n  },\n  "devDependencies": {\n    "nodemon": "^2.0.22"\n  }\n}\n')
                
        elif project_type == 'angular':
            subprocess.run(['npx', '@angular/cli', 'new', '.', '--defaults'], cwd=project_name, check=True)
            
        elif project_type == 'laravel':
            subprocess.run(['composer', 'create-project', '--prefer-dist', 'laravel/laravel', '.'], cwd=project_name, check=True)
            
        elif project_type == 'spring':
            os.makedirs(f"{project_name}/src/main/java/com/z0roday/{project_name}", exist_ok=True)
            os.makedirs(f"{project_name}/src/main/resources", exist_ok=True)
            
            with open(f"{project_name}/pom.xml", 'w') as f:
                f.write('<?xml version="1.0" encoding="UTF-8"?>\n<project xmlns="http://maven.apache.org/POM/4.0.0">\n  <modelVersion>4.0.0</modelVersion>\n  <groupId>com.z0roday</groupId>\n  <artifactId>' + project_name + '</artifactId>\n  <version>0.0.1-SNAPSHOT</version>\n  <parent>\n    <groupId>org.springframework.boot</groupId>\n    <artifactId>spring-boot-starter-parent</artifactId>\n    <version>3.1.3</version>\n  </parent>\n  <dependencies>\n    <dependency>\n      <groupId>org.springframework.boot</groupId>\n      <artifactId>spring-boot-starter-web</artifactId>\n    </dependency>\n  </dependencies>\n</project>\n')
            
            with open(f"{project_name}/src/main/java/com/z0roday/{project_name}/Application.java", 'w') as f:
                f.write(f'package com.z0roday.{project_name};\n\nimport org.springframework.boot.SpringApplication;\nimport org.springframework.boot.autoconfigure.SpringBootApplication;\nimport org.springframework.web.bind.annotation.GetMapping;\nimport org.springframework.web.bind.annotation.RestController;\n\n@SpringBootApplication\n@RestController\npublic class Application {{\n    public static void main(String[] args) {{\n        SpringApplication.run(Application.class, args);\n    }}\n    \n    @GetMapping("/")\n    public String hello() {{\n        return "Hello from z0roday!";\n    }}\n}}\n')
            
            print("Run 'mvn spring-boot:run' in the project folder after installing Maven.")
            
        elif project_type == 'go':
            with open(f"{project_name}/main.go", 'w') as f:
                f.write('package main\n\nimport (\n\t"fmt"\n\t"net/http"\n)\n\nfunc handler(w http.ResponseWriter, r *http.Request) {\n\tfmt.Fprintf(w, "Hello from z0roday!")\n}\n\nfunc main() {\n\thttp.HandleFunc("/", handler)\n\tfmt.Println("Server starting on port 8080...")\n\thttp.ListenAndServe(":8080", nil)\n}\n')
            
            with open(f"{project_name}/go.mod", 'w') as f:
                f.write(f'module github.com/z0roday/{project_name}\n\ngo 1.18\n')
                
        elif project_type == 'rust':
            # Use cargo to initialize the project
            original_dir = os.getcwd()
            os.chdir(project_name)
            subprocess.run(['cargo', 'init', '--name', project_name], check=True)
            
            # Add simple web server to Cargo.toml
            with open("Cargo.toml", 'a') as f:
                f.write('\n[dependencies]\nactix-web = "4.3.1"\nserde = { version = "1.0.188", features = ["derive"] }\n')
            
            # Update main.rs with a simple web server
            with open("src/main.rs", 'w') as f:
                f.write('use actix_web::{web, App, HttpServer, Responder};\n\nasync fn hello() -> impl Responder {\n    "Hello from z0roday!"\n}\n\n#[actix_web::main]\nasync fn main() -> std::io::Result<()> {\n    println!("Server running at http://localhost:8080");\n    HttpServer::new(|| {\n        App::new()\n            .route("/", web::get().to(hello))\n    })\n    .bind("127.0.0.1:8080")?\n    .run()\n    .await\n}\n')
                
            os.chdir(original_dir)
            
        elif project_type == 'dotnet':
            # Initialize a new .NET web app
            original_dir = os.getcwd()
            os.chdir(project_name)
            subprocess.run(['dotnet', 'new', 'webapi', '--no-https'], check=True)
            os.chdir(original_dir)

        # Docker support
        if dockerize:
            animate_progress("Configuring Docker", 1.0)
            create_docker_file(project_name, project_type)

        # Initialize Git repository
        if git_init:
            animate_progress("Initializing Git repository", 1.0)
            original_dir = os.getcwd()
            os.chdir(project_name)
            subprocess.run(['git', 'init'], check=True)
            subprocess.run(['git', 'add', '.'], check=True)
            subprocess.run(['git', 'commit', '-m', 'Initial commit by z0roday DevBuddy'], check=True)
            os.chdir(original_dir)
            print("Initialized Git repository")

        # Setup testing framework
        if with_tests:
            animate_progress("Setting up testing framework", 1.0)
            setup_testing(project_name, project_type)
            
        # Setup CI/CD configuration
        if auto_ci:
            animate_progress("Setting up CI/CD configuration", 1.0)
            setup_ci_cd(project_name, project_type)

        # Show completion message with next steps
        show_completion(project_name, project_type)

    except (OSError, subprocess.CalledProcessError) as e:
        print(f"Error: Failed to scaffold {project_type} project: {e}")
    except Exception as e:
        print(f"Unexpected error: {str(e)}")