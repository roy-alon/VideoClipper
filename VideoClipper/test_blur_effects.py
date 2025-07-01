#!/usr/bin/env python3
"""
Test script to check what blur effects are available in MoviePy
"""

import numpy as np
from moviepy import VideoFileClip, ColorClip, CompositeVideoClip, vfx

def test_blur_effects():
    """Test different blur effects available in MoviePy"""
    print("🎬 Testing Blur Effects in MoviePy")
    print("=" * 50)
    
    # Check what's available in vfx
    print("Available vfx effects:")
    for attr in dir(vfx):
        if not attr.startswith('_'):
            print(f"  - {attr}")
    
    print("\n" + "=" * 50)
    
    # Test specific blur effects
    blur_tests = [
        'GaussianBlur',
        'blur',
        'Blur',
        'gaussian_blur',
        'gaussian',
        'blur_image'
    ]
    
    for blur_name in blur_tests:
        try:
            blur_func = getattr(vfx, blur_name)
            print(f"✓ {blur_name} is available")
            
            # Try to create a simple test
            test_clip = ColorClip(size=(100, 100), color=(255, 0, 0), duration=1)
            
            if blur_name == 'GaussianBlur':
                blurred = test_clip.with_effects([blur_func(sigma=5)])
                print(f"  ✓ GaussianBlur with sigma=5 works")
            elif blur_name == 'blur':
                blurred = test_clip.with_effects([blur_func(5)])
                print(f"  ✓ blur with radius=5 works")
            else:
                # Try different parameter names
                try:
                    blurred = test_clip.with_effects([blur_func(5)])
                    print(f"  ✓ {blur_name} with parameter=5 works")
                except:
                    try:
                        blurred = test_clip.with_effects([blur_func(sigma=5)])
                        print(f"  ✓ {blur_name} with sigma=5 works")
                    except Exception as e:
                        print(f"  ⚠ {blur_name} exists but failed: {e}")
                        
        except AttributeError:
            print(f"❌ {blur_name} is not available")
        except Exception as e:
            print(f"⚠ {blur_name} failed: {e}")
    
    print("\n" + "=" * 50)
    
    # Test with a real video if available
    video_path = "test_input_video.mp4"
    if video_path:
        try:
            print(f"Testing blur with real video: {video_path}")
            video = VideoFileClip(video_path)
            
            # Try different blur methods
            blur_methods = []
            
            # Method 1: GaussianBlur
            try:
                blurred1 = video.with_effects([vfx.GaussianBlur(sigma=10)])
                blur_methods.append(("GaussianBlur", blurred1))
                print("✓ GaussianBlur works with real video")
            except Exception as e:
                print(f"❌ GaussianBlur failed: {e}")
            
            # Method 2: blur
            try:
                blurred2 = video.with_effects([vfx.blur(10)])
                blur_methods.append(("blur", blurred2))
                print("✓ blur works with real video")
            except Exception as e:
                print(f"❌ blur failed: {e}")
            
            # Save test results
            for method_name, blurred_clip in blur_methods:
                output_path = f"test_blur_{method_name.lower()}.mp4"
                print(f"Saving {output_path}...")
                blurred_clip.subclipped(0, min(3, blurred_clip.duration)).write_videofile(
                    output_path,
                    fps=24,
                    codec='libx264',
                    audio_codec='aac'
                )
                print(f"✓ Saved {output_path}")
                blurred_clip.close()
            
            video.close()
            
        except Exception as e:
            print(f"❌ Video blur test failed: {e}")

def test_custom_blur():
    """Test creating a custom blur effect"""
    print("\n🎬 Testing Custom Blur Effect")
    print("=" * 50)
    
    try:
        # Create a simple test clip
        test_clip = ColorClip(size=(200, 200), color=(255, 0, 0), duration=2)
        
        # Try to create a custom blur effect using numpy
        def custom_blur(get_frame, t):
            frame = get_frame(t)
            # Simple box blur (very basic)
            from scipy import ndimage
            try:
                blurred = ndimage.gaussian_filter(frame, sigma=3)
                return blurred
            except ImportError:
                # Fallback without scipy
                return frame
        
        # Apply custom blur
        try:
            blurred = test_clip.with_effects([custom_blur])
            print("✓ Custom blur effect created")
            
            # Save test
            output_path = "test_custom_blur.mp4"
            blurred.write_videofile(
                output_path,
                fps=24,
                codec='libx264'
            )
            print(f"✓ Saved {output_path}")
            blurred.close()
            
        except Exception as e:
            print(f"❌ Custom blur failed: {e}")
        
        test_clip.close()
        
    except Exception as e:
        print(f"❌ Custom blur test failed: {e}")

def main():
    """Main test function"""
    test_blur_effects()
    test_custom_blur()
    print("\n✅ Blur testing complete!")

if __name__ == "__main__":
    main() 