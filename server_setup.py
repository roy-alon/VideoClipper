#!/usr/bin/env python3
"""
Server Setup Script for VideoClipper
Run this on your cloud server to set up the environment
"""

import os
import subprocess
import sys

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return False

def create_requirements_file():
    """Create requirements.txt with all necessary dependencies"""
    requirements = """moviepy==2.2.1
openai==1.86.0
python-dotenv==1.1.0
assemblyai
Pillow
numpy
"""
    
    with open('requirements.txt', 'w') as f:
        f.write(requirements)
    print("✅ Created requirements.txt")

def setup_environment():
    """Set up the Python environment"""
    print("🚀 Setting up VideoClipper server environment...")
    
    # Update system packages
    if not run_command("sudo apt-get update", "Updating system packages"):
        return False
    
    # Install system dependencies
    system_deps = [
        "python3-pip",
        "python3-venv", 
        "ffmpeg",
        "libsm6",
        "libxext6",
        "libxrender-dev",
        "libgomp1"
    ]
    
    for dep in system_deps:
        if not run_command(f"sudo apt-get install -y {dep}", f"Installing {dep}"):
            return False
    
    # Create virtual environment
    if not run_command("python3 -m venv venv", "Creating virtual environment"):
        return False
    
    # Activate virtual environment and install Python packages
    commands = [
        "source venv/bin/activate",
        "pip install --upgrade pip",
        "pip install -r requirements.txt"
    ]
    
    for cmd in commands:
        if not run_command(f"bash -c '{cmd}'", f"Running: {cmd}"):
            return False
    
    print("✅ Environment setup completed!")
    return True

def create_run_script():
    """Create a script to run the video processing"""
    run_script = """#!/bin/bash
# VideoClipper Run Script
# Usage: ./run_videoclipper.sh

# Activate virtual environment
source venv/bin/activate

# Set your OpenAI API key (replace with your actual key)
export OPENAI_API_KEY="your_openai_api_key_here"

# Run the video processor
python main.py

echo "Video processing completed!"
"""
    
    with open('run_videoclipper.sh', 'w') as f:
        f.write(run_script)
    
    # Make it executable
    run_command("chmod +x run_videoclipper.sh", "Making run script executable")
    print("✅ Created run_videoclipper.sh")

def create_dockerfile():
    """Create a Dockerfile for containerized deployment"""
    dockerfile = """FROM python:3.9-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \\
    ffmpeg \\
    libsm6 \\
    libxext6 \\
    libxrender-dev \\
    libgomp1 \\
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Create a script to run the application
RUN echo '#!/bin/bash\\n\
export OPENAI_API_KEY="$OPENAI_API_KEY"\\n\
python main.py' > /app/run.sh && chmod +x /app/run.sh

# Default command
CMD ["/app/run.sh"]
"""
    
    with open('Dockerfile', 'w') as f:
        f.write(dockerfile)
    print("✅ Created Dockerfile")

def main():
    """Main setup function"""
    print("🎬 VideoClipper Server Setup")
    print("=" * 40)
    
    # Create requirements file
    create_requirements_file()
    
    # Setup environment
    if not setup_environment():
        print("❌ Environment setup failed!")
        return
    
    # Create run script
    create_run_script()
    
    # Create Dockerfile
    create_dockerfile()
    
    print("\n🎉 Setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Copy your video files and subtitles.srt to the server")
    print("2. Edit run_videoclipper.sh and add your OpenAI API key")
    print("3. Run: ./run_videoclipper.sh")
    print("\n🐳 Or use Docker:")
    print("docker build -t videoclipper .")
    print("docker run -e OPENAI_API_KEY=your_key videoclipper")

if __name__ == "__main__":
    main() 