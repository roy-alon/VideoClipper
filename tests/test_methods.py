#!/usr/bin/env python3

from moviepy import VideoFileClip
import os

# Test with a simple video file
video_path = r"C:\Users\Admin\Downloads\The.Simpsons.S35E11.1080p.WEB.h264-BAE[TGx]\video.mkv"

try:
    print("Loading video...")
    video = VideoFileClip(video_path)
    
    print("Available methods in VideoFileClip:")
    methods = [method for method in dir(video) if not method.startswith('_')]
    for method in sorted(methods):
        print(f"  - {method}")
    
    # Check if there's a method to extract parts of the video
    if hasattr(video, 'cutout'):
        print("\nFound cutout method!")
    elif hasattr(video, 'subclip'):
        print("\nFound subclip method!")
    else:
        print("\nNo subclip or cutout method found. Let's try using slice notation...")
        try:
            # Try using slice notation
            clip = video[60:120]
            print("✓ Slice notation works: video[start:end]")
        except Exception as e:
            print(f"✗ Slice notation failed: {e}")
    
    video.close()
    
except Exception as e:
    print(f"Error: {e}")

font_path = os.path.abspath("Rubik_Wet_Paint/RubikWetPaint-Regular.ttf")
# Then use font=font_path in TextClip 