#!/usr/bin/env python3

from moviepy import VideoFileClip

# Test with a simple video file
video_path = r"C:\Users\Admin\Downloads\The.Simpsons.S35E11.1080p.WEB.h264-BAE[TGx]\video.mkv"

try:
    print("Loading video...")
    video = VideoFileClip(video_path)
    
    print("Testing subclip method...")
    # Try different ways to call subclip
    try:
        clip1 = video.subclip(60, 120)
        print("✓ subclip(start, end) works")
    except Exception as e:
        print(f"✗ subclip(start, end) failed: {e}")
    
    try:
        clip2 = video.subclip(t_start=60, t_end=120)
        print("✓ subclip(t_start, t_end) works")
    except Exception as e:
        print(f"✗ subclip(t_start, t_end) failed: {e}")
    
    try:
        clip3 = video.subclip(start_time=60, end_time=120)
        print("✓ subclip(start_time, end_time) works")
    except Exception as e:
        print(f"✗ subclip(start_time, end_time) failed: {e}")
    
    video.close()
    
except Exception as e:
    print(f"Error: {e}") 