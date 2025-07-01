#!/usr/bin/env python3
"""
Test file for video resizing with aspect ratio maintenance and side trimming
Focuses on creating 9:16 aspect ratio videos for YouTube Shorts
"""

import os
import numpy as np
from moviepy import VideoFileClip, TextClip, ColorClip, CompositeVideoClip, vfx

def test_video_resize_with_aspect_ratio():
    """Test different video resizing approaches for 9:16 aspect ratio"""
    print("=== Testing Video Resize with Aspect Ratio Maintenance ===")
    
    # Test video path - you can change this to your video file
    video_path = r"C:\Users\Admin\Downloads\The.Simpsons.S35E11.1080p.WEB.h264-BAE[TGx]\video.mkv"
    
    if not os.path.exists(video_path):
        print("❌ Video file not found, creating a test video instead")
        # Create a test video with different aspect ratio
        test_clip = create_test_video()
        if test_clip is None:
            return
        video = test_clip
    else:
        try:
            video = VideoFileClip(video_path)
            print(f"✓ Video loaded: {video.w}x{video.h} (aspect: {video.w/video.h:.3f})")
        except Exception as e:
            print(f"❌ Failed to load video: {e}")
            return
    
    # Target dimensions for YouTube Shorts (9:16 aspect ratio)
    target_width = 1080
    target_height = 1920
    target_aspect = target_width / target_height  # 0.5625
    
    print(f"Target: {target_width}x{target_height} (aspect: {target_aspect:.3f})")
    
    # Test different resizing methods
    methods = [
        ("Method 1: Resize to fit height, crop width", resize_method_1),
        ("Method 2: Resize to fit width, crop height", resize_method_2),
        ("Method 3: Smart crop with blur background", resize_method_3),
        ("Method 4: Center crop with padding", resize_method_4),
    ]
    
    for method_name, method_func in methods:
        print(f"\n--- {method_name} ---")
        try:
            result_clip = method_func(video, target_width, target_height)
            if result_clip:
                print(f"✓ Success: {result_clip.w}x{result_clip.h}")
                
                # Save a short test clip
                test_output = f"test_resize_{method_name.split(':')[0].lower().replace(' ', '_')}.mp4"
                result_clip.subclipped(0, min(5, result_clip.duration)).write_videofile(
                    test_output, 
                    fps=24,
                    codec='libx264',
                    audio_codec='aac'
                )
                print(f"✓ Saved test clip: {test_output}")
                result_clip.close()
            else:
                print("❌ Method failed")
        except Exception as e:
            print(f"❌ Method failed: {e}")
    
    video.close()

def resize_method_1(video, target_width, target_height):
    """Method 1: Resize to fit height, then crop width from center"""
    print("  Resizing to fit height, then cropping width...")
    
    # First resize to fit the target height
    resized = video.resized(height=target_height)
    print(f"  After height resize: {resized.w}x{resized.h}")
    
    # Then crop from center to get target width
    if resized.w > target_width:
        x_center = resized.w // 2
        y_center = resized.h // 2
        cropped = resized.cropped(
            width=target_width, 
            height=target_height, 
            x_center=x_center, 
            y_center=y_center
        )
        print(f"  After width crop: {cropped.w}x{cropped.h}")
        return cropped
    else:
        print("  Width already fits, no cropping needed")
        return resized

def resize_method_2(video, target_width, target_height):
    """Method 2: Resize to fit width, then crop height from center"""
    print("  Resizing to fit width, then cropping height...")
    
    # First resize to fit the target width
    resized = video.resized(width=target_width)
    print(f"  After width resize: {resized.w}x{resized.h}")
    
    # Then crop from center to get target height
    if resized.h > target_height:
        x_center = resized.w // 2
        y_center = resized.h // 2
        cropped = resized.cropped(
            width=target_width, 
            height=target_height, 
            x_center=x_center, 
            y_center=y_center
        )
        print(f"  After height crop: {cropped.w}x{cropped.h}")
        return cropped
    else:
        print("  Height already fits, no cropping needed")
        return resized

def resize_method_3(video, target_width, target_height):
    """Method 3: Smart crop with blur background"""
    print("  Creating smart crop with blur background...")
    
    # Calculate which dimension to fit first
    original_aspect = video.w / video.h
    target_aspect = target_width / target_height
    
    if original_aspect > target_aspect:
        # Original is wider - fit height first
        resized = video.resized(height=target_height)
        if resized.w > target_width:
            # Crop width from center
            x_center = resized.w // 2
            y_center = resized.h // 2
            cropped = resized.cropped(
                width=target_width, 
                height=target_height, 
                x_center=x_center, 
                y_center=y_center
            )
        else:
            cropped = resized
    else:
        # Original is taller - fit width first
        resized = video.resized(width=target_width)
        if resized.h > target_height:
            # Crop height from center
            x_center = resized.w // 2
            y_center = resized.h // 2
            cropped = resized.cropped(
                width=target_width, 
                height=target_height, 
                x_center=x_center, 
                y_center=y_center
            )
        else:
            cropped = resized
    
    # Create a blurred background from the original video
    try:
        # Resize original to target dimensions and blur
        bg = video.resized(width=target_width, height=target_height)
        bg = bg.with_effects([vfx.GaussianBlur(sigma=20)])
        
        # Create a black background clip
        bg_clip = ColorClip(size=(target_width, target_height), color=(0, 0, 0), duration=video.duration)
        
        # Composite the cropped video over the background
        # Center the cropped video
        if cropped.w < target_width or cropped.h < target_height:
            # Need to center the cropped video
            x_offset = (target_width - cropped.w) // 2
            y_offset = (target_height - cropped.h) // 2
            positioned_crop = cropped.with_position((x_offset, y_offset))
            final = CompositeVideoClip([bg_clip, positioned_crop])
        else:
            final = cropped
            
        print(f"  Final size: {final.w}x{final.h}")
        return final
        
    except Exception as e:
        print(f"  Blur background failed: {e}, returning simple crop")
        return cropped

def resize_method_4(video, target_width, target_height):
    """Method 4: Center crop with padding"""
    print("  Creating center crop with padding...")
    
    # Calculate the crop area to maintain aspect ratio
    original_aspect = video.w / video.h
    target_aspect = target_width / target_height
    
    if original_aspect > target_aspect:
        # Original is wider - crop width
        crop_width = int(video.h * target_aspect)
        crop_height = video.h
        x_center = video.w // 2
        y_center = video.h // 2
    else:
        # Original is taller - crop height
        crop_width = video.w
        crop_height = int(video.w / target_aspect)
        x_center = video.w // 2
        y_center = video.h // 2
    
    # Crop the video
    cropped = video.cropped(
        width=crop_width,
        height=crop_height,
        x_center=x_center,
        y_center=y_center
    )
    
    # Resize to target dimensions
    final = cropped.resized(width=target_width, height=target_height)
    
    print(f"  Final size: {final.w}x{final.h}")
    return final

def create_test_video():
    """Create a test video with different aspect ratio for testing"""
    print("Creating test video...")
    
    try:
        # Create a test video with 16:9 aspect ratio (1920x1080)
        def make_frame(t):
            # Create a simple animated frame
            frame = np.zeros((1080, 1920, 3), dtype=np.uint8)
            
            # Add some animated elements
            x = int(960 + 400 * np.sin(t * 2))
            y = int(540 + 200 * np.cos(t * 3))
            
            # Draw a moving circle
            for i in range(max(0, y-50), min(1080, y+50)):
                for j in range(max(0, x-50), min(1920, x+50)):
                    if (i-y)**2 + (j-x)**2 < 2500:
                        frame[i, j] = [255, 100, 100]  # Red circle
            
            # Add text
            text_y = 100
            for i in range(text_y, text_y + 60):
                for j in range(100, 700):
                    if i < 1080 and j < 1920:
                        frame[i, j] = [100, 255, 100]  # Green text area
            
            return frame
        
        # Create the video clip
        test_clip = VideoFileClip(make_frame, duration=10, fps=24)
        print("✓ Test video created: 1920x1080 (16:9 aspect ratio)")
        return test_clip
        
    except Exception as e:
        print(f"❌ Failed to create test video: {e}")
        return None

def test_with_sample_video():
    """Test with a sample video if available"""
    print("\n=== Testing with Sample Video ===")
    
    # Look for common video files in the current directory
    video_extensions = ['.mp4', '.avi', '.mkv', '.mov', '.wmv']
    sample_video = None
    
    for ext in video_extensions:
        for file in os.listdir('.'):
            if file.endswith(ext):
                sample_video = file
                break
        if sample_video:
            break
    
    if sample_video:
        print(f"Found sample video: {sample_video}")
        try:
            video = VideoFileClip(sample_video)
            print(f"Video loaded: {video.w}x{video.h} (aspect: {video.w/video.h:.3f})")
            
            # Test the best method
            result = resize_method_3(video, 1080, 1920)
            if result:
                output_file = f"resized_{sample_video}"
                result.subclipped(0, min(10, result.duration)).write_videofile(
                    output_file,
                    fps=24,
                    codec='libx264',
                    audio_codec='aac'
                )
                print(f"✓ Saved resized video: {output_file}")
                result.close()
            
            video.close()
            
        except Exception as e:
            print(f"❌ Failed to process sample video: {e}")
    else:
        print("No sample video found in current directory")

def main():
    """Main test function"""
    print("🎬 Video Resize Testing for YouTube Shorts (9:16 aspect ratio)")
    print("=" * 60)
    
    # Test with the main resize function
    test_video_resize_with_aspect_ratio()
    
    # Test with sample video if available
    test_with_sample_video()
    
    print("\n✅ Testing complete! Check the generated test files.")

if __name__ == "__main__":
    main() 