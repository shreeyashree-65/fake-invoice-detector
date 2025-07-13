#!/usr/bin/env python3
"""
Setup script for Fake Invoice Detector
Automates the setup process for development and production
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path

def run_command(command, cwd=None):
    """Run a command and return True if successful"""
    try:
        result = subprocess.run(command, shell=True, check=True, cwd=cwd, 
                              capture_output=True, text=True)
        print(f"✅ {command}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {command}")
        print(f"Error: {e.stderr}")
        return False

def setup_backend():
    """Set up the backend environment"""
    print("🔧 Setting up backend...")
    
    backend_dir = Path("backend")
    
    # Install Python dependencies
    if not run_command("pip install -r requirements.txt", cwd=backend_dir):
        return False
    
    # Generate training data
    if not run_command("python src/data_generator.py", cwd=backend_dir):
        return False
    
    # Train models
    if not run_command("python src/model_trainer.py", cwd=backend_dir):
        return False
    
    print("✅ Backend setup complete!")
    return True

def setup_frontend():
    """Set up the frontend environment"""
    print("🔧 Setting up frontend...")
    
    frontend_dir = Path("frontend")
    
    # Install Node.js dependencies
    if not run_command("npm install", cwd=frontend_dir):
        return False
    
    print("✅ Frontend setup complete!")
    return True

def start_development():
    """Start development servers"""
    print("🚀 Starting development servers...")
    
    # Start backend
    print("Starting backend server...")
    backend_process = subprocess.Popen(
        ["python", "app.py"], 
        cwd="backend"
    )
    
    # Start frontend
    print("Starting frontend server...")
    frontend_process = subprocess.Popen(
        ["npm", "start"], 
        cwd="frontend"
    )
    
    print("✅ Development servers started!")
    print("📱 Frontend: http://localhost:3000")
    print("🔧 Backend: http://localhost:8000")
    print("📚 API Docs: http://localhost:8000/docs")
    
    try:
        # Wait for processes
        backend_process.wait()
        frontend_process.wait()
    except KeyboardInterrupt:
        print("\n🛑 Stopping servers...")
        backend_process.terminate()
        frontend_process.terminate()

def build_docker():
    """Build Docker images"""
    print("🐳 Building Docker images...")
    
    if not run_command("docker-compose build"):
        return False
    
    print("✅ Docker images built!")
    return True

def start_docker():
    """Start Docker containers"""
    print("🐳 Starting Docker containers...")
    
    if not run_command("docker-compose up -d"):
        return False
    
    print("✅ Docker containers started!")
    print("📱 Application: http://localhost")
    print("🔧 API: http://localhost:8000")
    return True

def main():
    parser = argparse.ArgumentParser(description="Setup Fake Invoice Detector")
    parser.add_argument("action", choices=[
        "setup", "dev", "docker-build", "docker-start", "all"
    ], help="Action to perform")
    
    args = parser.parse_args()
    
    if args.action == "setup" or args.action == "all":
        if not setup_backend():
            sys.exit(1)
        if not setup_frontend():
            sys.exit(1)
    
    if args.action == "dev":
        start_development()
    
    if args.action == "docker-build" or args.action == "all":
        if not build_docker():
            sys.exit(1)
    
    if args.action == "docker-start":
        if not start_docker():
            sys.exit(1)
    
    print("🎉 Setup complete!")

if __name__ == "__main__":
    main()
