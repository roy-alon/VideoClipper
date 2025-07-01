#!/usr/bin/env python3
"""
Test custom blur effect using MoviePy's Resize effect
"""

import numpy as np
from moviepy import VideoFileClip, ColorClip, CompositeVideoClip, vfx

def create_blurred_background(video, target_width, target_height, blur_factor=0.3):
    """
    Create a blurred background by resizing the video to a small size and then scaling it up
    """
    try:
        # Resize video to a very small size (this creates the blur effect)
        small_width = int(target_width * blur_factor)
        small_height = int(target_height * blur_factor)
        
        # Resize to small size (this blurs the image)
        blurred = video.resized(width=small_width, height=small_height)
        
        # Resize back to target size (this creates the blurred background)
        blurred_bg = blurred.resized(width=target_width, height=target_height)
        
        print(f"  Created blurred background: {blurred_bg.w}x{blurred_bg.h}")
        return blurred_bg
        
    except Exception as e:
        print(f"  Blur background failed: {e}")
        # Fallback to solid color
        return ColorClip(size=(target_width, target_height), color=(0, 0, 0), duration=video.duration)

def test_blurred_background():
    """Test creating a blurred background effect"""
    print("🎬 Testing Blurred Background Effect")
    print("=" * 50)
    
    video_path = "test_input_video.mp4"
    
    if not video_path:
        print("❌ Test video not found")
        return
    
    try:
        video = VideoFileClip(video_path)
        print(f"✓ Video loaded: {video.w}x{video.h}")
        
        # Target dimensions
        target_width = 1080
        target_height = 1920
        
        # Create blurred background
        print("Creating blurred background...")
        blurred_bg = create_blurred_background(video, target_width, target_height, blur_factor=0.2)
        
        # Resize original video to fit inside
        original_aspect = video.w / video.h
        target_aspect = target_width / target_height
        
        if original_aspect > target_aspect:
            # Video is wider, fit width
            resized_video = video.resized(width=target_width)
        else:
            # Video is taller, fit height
            resized_video = video.resized(height=target_height)
        
        print(f"Resized video to: {resized_video.w}x{resized_video.h}")
        
        # Center the video on the blurred background
        x_offset = (target_width - resized_video.w) // 2
        y_offset = (target_height - resized_video.h) // 2
        positioned_video = resized_video.with_position((x_offset, y_offset))
        
        # Composite them together
        final_clip = CompositeVideoClip([blurred_bg, positioned_video])
        
        # Save the result
        output_path = "test_blurred_background.mp4"
        print(f"Saving {output_path}...")
        final_clip.subclipped(0, min(5, final_clip.duration)).write_videofile(
            output_path,
            fps=24,
            codec='libx264',
            audio_codec='aac'
        )
        print(f"✓ Saved {output_path}")
        
        # Clean up
        final_clip.close()
        video.close()
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()

def test_different_blur_factors():
    """Test different blur factors"""
    print("\n🎬 Testing Different Blur Factors")
    print("=" * 50)
    
    video_path = "test_input_video.mp4"
    
    if not video_path:
        print("❌ Test video not found")
        return
    
    try:
        video = VideoFileClip(video_path)
        target_width = 1080
        target_height = 1920
        
        blur_factors = [0.1, 0.2, 0.3, 0.4]
        
        for blur_factor in blur_factors:
            print(f"Testing blur factor: {blur_factor}")
            
            # Create blurred background
            blurred_bg = create_blurred_background(video, target_width, target_height, blur_factor)
            
            # Save just the background for comparison
            output_path = f"test_blur_factor_{blur_factor}.mp4"
            blurred_bg.subclipped(0, min(3, blurred_bg.duration)).write_videofile(
                output_path,
                fps=24,
                codec='libx264',
                audio_codec='aac'
            )
            print(f"✓ Saved {output_path}")
            blurred_bg.close()
        
        video.close()
        
    except Exception as e:
        print(f"❌ Test failed: {e}")

def main():
    """Main test function"""
    test_blurred_background()
    test_different_blur_factors()
    print("\n✅ Blur background testing complete!")

if __name__ == "__main__":
    main() 