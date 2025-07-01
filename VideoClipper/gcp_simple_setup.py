#!/usr/bin/env python3
"""
Simple GCP Setup for VideoClipper
Uses standard Ubuntu image with minimal dependencies
"""

import os
import subprocess
import time

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

def create_vm_instance(project_id, zone="us-central1-a"):
    """Create VM with standard Ubuntu"""
    instance_name = "videoclipper"
    
    print("🚀 Creating GCP VM instance with standard Ubuntu...")
    
    create_cmd = f"""gcloud compute instances create {instance_name} \
        --zone={zone} \
        --project={project_id} \
        --machine-type=n1-standard-4 \
        --image-family=ubuntu-2004-lts \
        --image-project=ubuntu-os-cloud \
        --boot-disk-size=30GB \
        --boot-disk-type=pd-ssd \
        --scopes=default,storage-full"""
    
    return run_command(create_cmd, "Creating VM instance")

def setup_environment(project_id, zone="us-central1-a"):
    """Setup minimal environment for VideoClipper"""
    instance_name = "videoclipper"
    
    print("🔧 Setting up minimal environment...")
    
    setup_commands = [
        # Update system
        "sudo apt-get update",
        
        # Install essential packages
        "sudo apt-get install -y python3-pip python3-venv ffmpeg",
        
        # Create virtual environment
        "python3 -m venv venv",
        
        # Activate venv and install Python packages
        "source venv/bin/activate && pip install moviepy==2.2.1 openai==1.86.0 python-dotenv==1.1.0",
        
        # Create simple run script
        '''cat > run_videoclipper.sh << 'EOF'
#!/bin/bash
source venv/bin/activate
export OPENAI_API_KEY="$1"
python main.py
echo "Processing completed!"
EOF''',
        
        # Make run script executable
        "chmod +x run_videoclipper.sh",
        
        # Test installation
        "source venv/bin/activate && python -c 'import moviepy; print(f\"MoviePy {moviepy.__version__} installed successfully!\")'"
    ]
    
    for cmd in setup_commands:
        ssh_cmd = f"gcloud compute ssh {instance_name} --zone={zone} --project={project_id} --command='{cmd}'"
        if not run_command(ssh_cmd, f"Running: {cmd[:50]}..."):
            return False
    
    return True

def upload_files(project_id, zone="us-central1-a"):
    """Upload VideoClipper files"""
    instance_name = "videoclipper"
    
    print("📤 Uploading files...")
    
    files_to_upload = [
        "main.py",
        "video_editor.py", 
        "subtitles.py",
        "gpt_analysis.py"
    ]
    
    for file_path in files_to_upload:
        if os.path.exists(file_path):
            upload_cmd = f"gcloud compute scp {file_path} {instance_name}:~/ --zone={zone} --project={project_id}"
            run_command(upload_cmd, f"Uploading {file_path}")
        else:
            print(f"⚠️ File not found: {file_path}")

def create_run_script(project_id, zone="us-central1-a"):
    """Create local run script"""
    instance_name = "videoclipper"
    
    run_script = f"""#!/bin/bash
# Simple VideoClipper GCP Runner
# Usage: ./run_simple.sh "your_openai_api_key"

if [ -z "$1" ]; then
    echo "❌ Please provide your OpenAI API key"
    echo "Usage: ./run_simple.sh 'your_api_key'"
    exit 1
fi

echo "🚀 Starting video processing on GCP..."

# Run the processor
gcloud compute ssh {instance_name} --zone={zone} --project={project_id} --command="./run_videoclipper.sh '$1'"

# Download the result
echo "📥 Downloading result..."
gcloud compute scp {instance_name}:~/youtube_shorts_output.mp4 ./ --zone={zone} --project={project_id}

echo "✅ Processing completed! Check youtube_shorts_output.mp4"
"""
    
    with open('run_simple.sh', 'w') as f:
        f.write(run_script)
    
    run_command("chmod +x run_simple.sh", "Making run script executable")
    print("✅ Created run_simple.sh")

def main():
    """Main setup function"""
    print("🎬 VideoClipper Simple GCP Setup")
    print("=" * 40)
    print("Using standard Ubuntu image (minimal dependencies)")
    print()
    
    # Get project ID
    project_id = input("Enter your GCP Project ID: ").strip()
    if not project_id:
        print("❌ Project ID is required")
        return
    
    # Create VM
    if not create_vm_instance(project_id):
        print("❌ Failed to create VM")
        return
    
    # Wait a moment for instance to be ready
    print("⏳ Waiting for instance to be ready...")
    time.sleep(30)
    
    # Setup environment
    if not setup_environment(project_id):
        print("❌ Environment setup failed")
        return
    
    # Upload files
    upload_files(project_id)
    
    # Create run script
    create_run_script(project_id)
    
    print("\n🎉 Simple GCP setup completed!")
    print("\n📋 Next steps:")
    print("1. Upload your video files:")
    print("   gcloud compute scp video.mkv videoclipper:~/ --zone=us-central1-a --project=" + project_id)
    print("   gcloud compute scp subtitles.srt videoclipper:~/ --zone=us-central1-a --project=" + project_id)
    print("2. Run: ./run_simple.sh 'your_openai_api_key'")
    print("\n💰 Cost: ~$0.05-0.10 per video (cheaper than deep learning image)")

if __name__ == "__main__":
    main() 