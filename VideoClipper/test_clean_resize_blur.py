#!/usr/bin/env python3
"""
Clean test for resizing and blur effects only - no text overlays, using MoviePy v2 API and Pillow for blur
"""

import os
import numpy as np
from moviepy import VideoFileClip, CompositeVideoClip, TextClip
from PIL import Image, ImageFilter

def blur_frame(frame: np.ndarray) -> np.ndarray:
    img = Image.fromarray(frame)
    return np.array(img.filter(ImageFilter.GaussianBlur(radius=20)))

def test_clean_resize_blur():
    print("🎬 Testing Clean Resize and Blur Effects (MoviePy v2 API)")
    print("=" * 60)
    
    video_path = "test_input_video.mp4"
    if not os.path.exists(video_path):
        print("❌ Test video not found, skipping test")
        return
    
    try:
        target_width, target_height = 1080, 1920
        clip = VideoFileClip(video_path)
        print(f"✓ Video loaded: {clip.w}x{clip.h}")
        start_time = 0.0
        end_time = min(3.0, clip.duration)
        print(f"✓ Using segment: {start_time}s to {end_time}s")
        clip = clip.subclipped(start_time, end_time)

        # 1. Create blurred background (stretch to fill, then blur)
        bg_stretched = clip.resized(width=target_width, height=target_height)
        blurred_bg = bg_stretched.image_transform(blur_frame)

        # 2. Scale up the original video to 2/3 of the background height
        contained_height = int(target_height * (2/3))
        contained = clip.resized(height=contained_height)
        x_offset = (target_width - contained.w) // 2
        y_offset = (target_height - contained.h) // 2
        contained = contained.with_position((x_offset, y_offset))

        # 3. Composite, force output size
        final = CompositeVideoClip([blurred_bg, contained], size=(target_width, target_height))

        # 4. Preview (scaled down)
        print("\nPreviewing final composite (scaled down)...")
        final.resized(0.3).preview()

        # 5. Save the clean test clip (only 3 seconds)
        output_path = "test_clean_resize_blur_output.mp4"
        final.write_videofile(
            output_path,
            fps=24,
            codec='libx264',
            audio_codec='aac'
        )
        print(f"✓ Saved clean test clip: {output_path}")
        final.close()
        clip.close()
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()

def main():
    test_clean_resize_blur()
    print("\n✅ Clean resize and blur testing complete!")

if __name__ == "__main__":
    main() 