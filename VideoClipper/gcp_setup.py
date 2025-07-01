#!/usr/bin/env python3
"""
GCP Setup Script for VideoClipper
Automates the entire setup process on Google Cloud Platform
"""

import os
import subprocess
import json
import time

class GCPSetup:
    def __init__(self, project_id, zone="us-central1-a"):
        self.project_id = project_id
        self.zone = zone
        self.instance_name = "videoclipper"
        
    def run_command(self, command, description):
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
    
    def create_vm_instance(self):
        """Create a VM instance with GPU"""
        print("🚀 Creating GCP VM instance...")
        
        # Check if instance already exists
        check_cmd = f"gcloud compute instances describe {self.instance_name} --zone={self.zone} --project={self.project_id}"
        if self.run_command(check_cmd, "Checking if instance exists"):
            print("✅ Instance already exists")
            return True
        
        # Create instance with GPU
        create_cmd = f"""gcloud compute instances create {self.instance_name} \
            --zone={self.zone} \
            --project={self.project_id} \
            --machine-type=n1-standard-4 \
            --accelerator="type=nvidia-tesla-t4,count=1" \
            --image-family=deeplearning-platform-release \
            --image-project=ml-images \
            --maintenance-policy=TERMINATE \
            --boot-disk-size=50GB \
            --boot-disk-type=pd-ssd \
            --metadata="install-nvidia-driver=True" \
            --scopes=default,storage-full"""
        
        return self.run_command(create_cmd, "Creating VM instance")
    
    def wait_for_instance(self):
        """Wait for instance to be ready"""
        print("⏳ Waiting for instance to be ready...")
        max_attempts = 30
        for attempt in range(max_attempts):
            status_cmd = f"gcloud compute instances describe {self.instance_name} --zone={self.zone} --project={self.project_id} --format='value(status)'"
            result = subprocess.run(status_cmd, shell=True, capture_output=True, text=True)
            if result.stdout.strip() == "RUNNING":
                print("✅ Instance is running")
                return True
            print(f"⏳ Instance status: {result.stdout.strip()} (attempt {attempt + 1}/{max_attempts})")
            time.sleep(10)
        
        print("❌ Instance failed to start")
        return False
    
    def upload_files(self, local_files):
        """Upload files to the VM"""
        print("📤 Uploading files to VM...")
        for file_path in local_files:
            if os.path.exists(file_path):
                upload_cmd = f"gcloud compute scp {file_path} {self.instance_name}:~/ --zone={self.zone} --project={self.project_id}"
                self.run_command(upload_cmd, f"Uploading {file_path}")
            else:
                print(f"⚠️ File not found: {file_path}")
    
    def setup_environment(self):
        """Setup the environment on the VM"""
        print("🔧 Setting up environment on VM...")
        
        setup_commands = [
            # Install additional dependencies
            "pip install moviepy==2.2.1 openai==1.86.0 python-dotenv==1.1.0",
            
            # Create run script
            '''cat > run_videoclipper.sh << 'EOF'
#!/bin/bash
export OPENAI_API_KEY="$1"
python main.py
echo "Processing completed!"
EOF''',
            
            # Make run script executable
            "chmod +x run_videoclipper.sh",
            
            # Create a simple test script
            '''cat > test_setup.py << 'EOF'
#!/usr/bin/env python3
import moviepy
import openai
import os
print("✅ All dependencies installed successfully!")
print(f"MoviePy version: {moviepy.__version__}")
print(f"OpenAI version: {openai.__version__}")
EOF''',
            
            # Test the setup
            "python test_setup.py"
        ]
        
        for cmd in setup_commands:
            ssh_cmd = f"gcloud compute ssh {self.instance_name} --zone={self.zone} --project={self.project_id} --command='{cmd}'"
            if not self.run_command(ssh_cmd, f"Running: {cmd[:50]}..."):
                return False
        
        return True
    
    def create_run_script(self):
        """Create a local script to run the processor"""
        run_script = f"""#!/bin/bash
# VideoClipper GCP Runner
# Usage: ./run_on_gcp.sh "your_openai_api_key"

if [ -z "$1" ]; then
    echo "❌ Please provide your OpenAI API key"
    echo "Usage: ./run_on_gcp.sh 'your_api_key'"
    exit 1
fi

echo "🚀 Starting video processing on GCP..."

# Run the processor on GCP
gcloud compute ssh {self.instance_name} --zone={self.zone} --project={self.project_id} --command="./run_videoclipper.sh '$1'"

# Download the result
echo "📥 Downloading result..."
gcloud compute scp {self.instance_name}:~/youtube_shorts_output.mp4 ./ --zone={self.zone} --project={self.project_id}

echo "✅ Processing completed! Check youtube_shorts_output.mp4"
"""
        
        with open('run_on_gcp.sh', 'w') as f:
            f.write(run_script)
        
        # Make it executable
        self.run_command("chmod +x run_on_gcp.sh", "Making GCP run script executable")
        print("✅ Created run_on_gcp.sh")
    
    def get_instance_info(self):
        """Get instance information"""
        print("📊 Instance Information:")
        info_cmd = f"gcloud compute instances describe {self.instance_name} --zone={self.zone} --project={self.project_id} --format='value(name,zone,machineType,status,networkInterfaces[0].accessConfigs[0].natIP)'"
        result = subprocess.run(info_cmd, shell=True, capture_output=True, text=True)
        if result.stdout:
            parts = result.stdout.strip().split('\t')
            print(f"  Name: {parts[0]}")
            print(f"  Zone: {parts[1]}")
            print(f"  Machine Type: {parts[2]}")
            print(f"  Status: {parts[3]}")
            if len(parts) > 4:
                print(f"  External IP: {parts[4]}")
    
    def cleanup(self):
        """Clean up the instance (optional)"""
        print("🧹 Cleaning up instance...")
        delete_cmd = f"gcloud compute instances delete {self.instance_name} --zone={self.zone} --project={self.project_id} --quiet"
        return self.run_command(delete_cmd, "Deleting instance")

def main():
    """Main setup function"""
    print("🎬 VideoClipper GCP Setup")
    print("=" * 40)
    
    # Get project ID
    project_id = input("Enter your GCP Project ID: ").strip()
    if not project_id:
        print("❌ Project ID is required")
        return
    
    # Initialize setup
    setup = GCPSetup(project_id)
    
    # Create VM instance
    if not setup.create_vm_instance():
        print("❌ Failed to create VM instance")
        return
    
    # Wait for instance to be ready
    if not setup.wait_for_instance():
        print("❌ Instance failed to start")
        return
    
    # Get instance info
    setup.get_instance_info()
    
    # Upload files
    files_to_upload = [
        "main.py",
        "video_editor.py", 
        "subtitles.py",
        "gpt_analysis.py",
        "video.mkv",
        "subtitles.srt"
    ]
    setup.upload_files(files_to_upload)
    
    # Setup environment
    if not setup.setup_environment():
        print("❌ Environment setup failed")
        return
    
    # Create run script
    setup.create_run_script()
    
    print("\n🎉 GCP setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Run: ./run_on_gcp.sh 'your_openai_api_key'")
    print("2. Wait for processing to complete")
    print("3. Check youtube_shorts_output.mp4")
    print("\n💰 Cost estimate: ~$0.08-0.17 per video")
    print("\n🧹 To clean up: python gcp_setup.py --cleanup")

if __name__ == "__main__":
    main() 