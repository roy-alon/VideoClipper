# VideoClipper Cloud Deployment Guide

## 🚀 Quick Start Options

### Option 1: Google Colab (Easiest - Free/Paid)
1. Go to [Google Colab](https://colab.research.google.com/)
2. Create new notebook
3. Upload your files (video.mkv, subtitles.srt)
4. Run setup commands:
```python
!pip install moviepy==2.2.1 openai==1.86.0 python-dotenv==1.1.0
!apt-get install -y ffmpeg
# Upload your Python files and run
```

### Option 2: AWS EC2 (Most Control)
1. Launch EC2 instance (g4dn.xlarge recommended)
2. SSH into instance
3. Run: `python server_setup.py`
4. Upload files and run

### Option 3: Google Cloud Run (Serverless)
1. Use the provided Dockerfile
2. Deploy to Cloud Run
3. Process videos via API calls

---

## 📋 Detailed Setup Instructions

### AWS EC2 Setup

#### 1. Launch Instance
```bash
# Launch g4dn.xlarge (GPU instance)
# Ubuntu 20.04 LTS recommended
# 50GB storage minimum
```

#### 2. Connect and Setup
```bash
# SSH into your instance
ssh -i your-key.pem ubuntu@your-instance-ip

# Clone or upload your VideoClipper files
git clone <your-repo> # or upload via SCP

# Run setup
python3 server_setup.py
```

#### 3. Upload Files
```bash
# From your local machine
scp -i your-key.pem video.mkv ubuntu@your-instance-ip:~/
scp -i your-key.pem subtitles.srt ubuntu@your-instance-ip:~/
```

#### 4. Run Processing
```bash
# Edit the run script with your API key
nano run_videoclipper.sh

# Run the processor
./run_videoclipper.sh
```

#### 5. Download Results
```bash
# From your local machine
scp -i your-key.pem ubuntu@your-instance-ip:~/youtube_shorts_output.mp4 ./
```

---

### Google Cloud Platform

#### 1. Create VM Instance
```bash
# Create instance with GPU
gcloud compute instances create videoclipper \
  --zone=us-central1-a \
  --machine-type=n1-standard-4 \
  --accelerator="type=nvidia-tesla-t4,count=1" \
  --image-family=debian-11 \
  --image-project=debian-cloud \
  --boot-disk-size=50GB
```

#### 2. Setup Environment
```bash
# SSH into instance
gcloud compute ssh videoclipper --zone=us-central1-a

# Run setup
python3 server_setup.py
```

---

### Docker Deployment

#### 1. Build Image
```bash
docker build -t videoclipper .
```

#### 2. Run Container
```bash
# Mount your video directory
docker run -v $(pwd)/videos:/app/videos \
  -e OPENAI_API_KEY=your_key \
  videoclipper
```

---

## 💰 Cost Estimates

### AWS EC2
- **g4dn.xlarge**: ~$0.50/hour
- **p3.2xlarge**: ~$3.00/hour
- Processing time: 10-30 minutes per video
- **Total cost**: $0.08 - $1.50 per video

### Google Colab
- **Free**: Limited GPU time
- **Pro**: $10/month, unlimited GPU
- **Pro+**: $50/month, better GPUs

### Google Cloud Platform
- **n1-standard-4 + GPU**: ~$0.50-1.50/hour
- Similar costs to AWS

---

## 🔧 Performance Optimization

### 1. Use GPU Instances
- MoviePy can utilize GPU acceleration
- 2-5x faster processing

### 2. Optimize Video Settings
```python
# In video_editor.py, adjust these settings:
final_video.write_videofile(
    output_path,
    codec='libx264',
    audio_codec='aac',
    temp_audiofile='temp-audio.m4a',
    remove_temp=True,
    fps=video.fps,
    bitrate='4000k',  # Reduced from 6000k
    preset='fast'     # Changed from 'medium'
)
```

### 3. Parallel Processing
- Process multiple videos simultaneously
- Use multiple instances

---

## 📁 File Structure for Server

```
videoclipper/
├── main.py
├── video_editor.py
├── subtitles.py
├── gpt_analysis.py
├── requirements.txt
├── server_setup.py
├── run_videoclipper.sh
├── Dockerfile
├── video.mkv              # Your input video
├── subtitles.srt          # Your subtitles
└── youtube_shorts_output.mp4  # Output video
```

---

## 🚨 Security Notes

1. **Never commit API keys** to version control
2. **Use environment variables** for sensitive data
3. **Delete temporary files** after processing
4. **Use IAM roles** instead of hardcoded credentials (AWS)
5. **Enable firewall rules** to restrict access

---

## 🔄 Batch Processing

For processing multiple videos:

```bash
#!/bin/bash
# batch_process.sh

for video in videos/*.mkv; do
    echo "Processing $video..."
    # Copy video to working directory
    cp "$video" video.mkv
    
    # Run processor
    ./run_videoclipper.sh
    
    # Move output to results
    mv youtube_shorts_output.mp4 "results/$(basename "$video" .mkv)_shorts.mp4"
done
```

---

## 📞 Support

If you encounter issues:
1. Check the logs in the run script
2. Verify all dependencies are installed
3. Ensure sufficient disk space (50GB+ recommended)
4. Check GPU drivers are properly installed

---

## 💡 Tips

1. **Start with smaller videos** to test the setup
2. **Monitor costs** - stop instances when not in use
3. **Use spot instances** for cost savings (AWS)
4. **Backup your results** before terminating instances
5. **Use compression** for faster file transfers 