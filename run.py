#!/usr/bin/env python3
"""
Main entry point for the Conflict Tracker application.
This script sets up and runs both the backend and frontend servers.
"""

import os
import sys
import subprocess
from pathlib import Path
import time

def run_command(cmd, cwd=None, env=None):
    """Run a shell command and return process"""
    process = subprocess.Popen(
        cmd,
        cwd=cwd,
        env=env or os.environ.copy(),
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    return process

def setup_backend():
    """Setup Python backend"""
    print("🔧 Setting up backend...")
    backend_dir = Path(__file__).parent / "backend"
    
    # Create virtual environment if not exists
    venv_path = backend_dir / "venv"
    if not venv_path.exists():
        print("   Creating virtual environment...")
        subprocess.run([sys.executable, "-m", "venv", str(venv_path)], check=True)
    
    # Install requirements
    print("   Installing Python dependencies...")
    pip_path = venv_path / "bin" / "pip" if sys.platform != "win32" else venv_path / "Scripts" / "pip.exe"
    subprocess.run([str(pip_path), "install", "-r", "requirements.txt"], cwd=backend_dir, check=True)
    print("✅ Backend ready!")
    return backend_dir, venv_path

def setup_frontend():
    """Setup Node.js frontend"""
    print("🔧 Setting up frontend...")
    frontend_dir = Path(__file__).parent / "frontend"
    
    # Install dependencies
    if not (frontend_dir / "node_modules").exists():
        print("   Installing npm packages...")
        subprocess.run(["npm", "install"], cwd=frontend_dir, check=True)
    
    print("✅ Frontend ready!")
    return frontend_dir

def start_backend(backend_dir, venv_path):
    """Start Flask backend server"""
    print("\n🚀 Starting backend server...")
    
    if sys.platform == "win32":
        activate_cmd = str(venv_path / "Scripts" / "activate.bat")
        python_cmd = "python"
    else:
        activate_cmd = f"source {venv_path / 'bin' / 'activate'}"
        python_cmd = "python3"
    
    # Start backend
    cmd = f"cd {backend_dir} && {activate_cmd} && {python_cmd} app.py"
    process = run_command(cmd)
    print("✅ Backend running on http://localhost:5000")
    return process

def start_frontend(frontend_dir):
    """Start React frontend development server"""
    print("\n🚀 Starting frontend development server...")
    cmd = f"cd {frontend_dir} && npm start"
    process = run_command(cmd)
    print("⏳ Frontend will open at http://localhost:3000")
    return process

def main():
    """Main entry point"""
    print("=" * 50)
    print("🌍 Conflict Tracker - Global Conflict Monitoring")
    print("=" * 50)
    print()
    
    try:
        # Setup
        print("📦 Setting up application...")
        backend_dir, venv_path = setup_backend()
        frontend_dir = setup_frontend()
        
        print("\n" + "=" * 50)
        print("🎯 Starting servers...")
        print("=" * 50)
        
        # Start servers
        backend_process = start_backend(backend_dir, venv_path)
        
        # Give backend time to start
        time.sleep(2)
        
        frontend_process = start_frontend(frontend_dir)
        
        print("\n" + "=" * 50)
        print("✨ Application is running!")
        print("=" * 50)
        print("\n📍 Backend:  http://localhost:5000")
        print("🎨 Frontend: http://localhost:3000")
        print("\nClose any terminal to stop the application")
        print("=" * 50 + "\n")
        
        # Wait for processes
        try:
            backend_process.wait()
            frontend_process.wait()
        except KeyboardInterrupt:
            print("\n\n👋 Shutting down servers...")
            backend_process.terminate()
            frontend_process.terminate()
            backend_process.wait()
            frontend_process.wait()
            print("✅ Servers stopped")
    
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nManual setup:")
        print("\nTerminal 1 (Backend):")
        print("  cd backend")
        print("  python3 -m venv venv")
        print("  source venv/bin/activate  # On Windows: venv\\Scripts\\activate")
        print("  pip install -r requirements.txt")
        print("  python3 app.py")
        print("\nTerminal 2 (Frontend):")
        print("  cd frontend")
        print("  npm install")
        print("  npm start")
        sys.exit(1)

if __name__ == "__main__":
    main()
