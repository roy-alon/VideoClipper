#!/usr/bin/env python3
"""
Comprehensive testing file for MoviePy 2.2.1 functions
Based on the official MoviePy documentation
Enhanced with advanced effects, transformations, and compositing
"""

import os
import numpy as np
import math
from moviepy import (
    VideoClip,
    VideoFileClip,
    ImageSequenceClip,
    ImageClip,
    TextClip,
    ColorClip,
    AudioFileClip,
    AudioClip,
    CompositeVideoClip,
    concatenate_videoclips,
    clips_array,
    CompositeAudioClip,
    concatenate_audioclips
)
from moviepy import vfx, afx
from moviepy.decorators import requires_duration

def test_video_file_clip():
    """Test VideoFileClip functionality"""
    print("=== Testing VideoFileClip ===")
    
    video_path = r"C:\Users\Admin\Downloads\The.Simpsons.S35E11.1080p.WEB.h264-BAE[TGx]\video.mkv"
    
    if not os.path.exists(video_path):
        print("❌ Video file not found, skipping VideoFileClip test")
        return None
    
    try:
        # Load video file
        video = VideoFileClip(video_path)
        print(f"✓ Video loaded successfully")
        print(f"  - Duration: {video.duration:.2f} seconds")
        print(f"  - FPS: {video.fps}")
        print(f"  - Size: {video.size}")
        
        # Test subclipped method (correct method name for 2.2.1)
        subclip = video.subclipped(60, 120)
        print(f"✓ Subclip created: {subclip.duration:.2f} seconds")
        
        # Test slice notation
        slice_clip = video[60:120]
        print(f"✓ Slice notation works: {slice_clip.duration:.2f} seconds")
        
        video.close()
        return video
        
    except Exception as e:
        print(f"❌ VideoFileClip test failed: {e}")
        return None

def test_text_clip():
    """Test TextClip functionality"""
    print("\n=== Testing TextClip ===")
    
    try:
        # Test basic TextClip creation
        txt_clip = TextClip(
            text="Hello World!",
            font_size=70,
            color="white",
            bg_color="black",
            duration=2
        )
        print("✓ Basic TextClip created successfully")
        
        # Test with more parameters
        txt_clip2 = TextClip(
            text="This is a test caption with multiple lines",
            font_size=50,
            color="red",
            stroke_color="black",
            stroke_width=2,
            size=(400, 200),
            method="caption",
            duration=3
        )
        print("✓ Advanced TextClip created successfully")
        
        # Test positioning - try different methods
        try:
            positioned_clip = txt_clip.with_position('center')
            print("✓ TextClip positioning works with with_position")
        except:
            try:
                positioned_clip = txt_clip.set_position('center')
                print("✓ TextClip positioning works with set_position")
            except:
                print("⚠ TextClip positioning not tested (method not found)")
        
        return txt_clip, txt_clip2
        
    except Exception as e:
        print(f"❌ TextClip test failed: {e}")
        return None, None

def test_color_clip():
    """Test ColorClip functionality"""
    print("\n=== Testing ColorClip ===")
    
    try:
        # Create a red color clip
        color_clip = ColorClip(size=(200, 100), color=(255, 0, 0), duration=2)
        print("✓ ColorClip created successfully")
        
        # Create a blue color clip
        blue_clip = ColorClip(size=(200, 100), color=(0, 0, 255), duration=2)
        print("✓ Blue ColorClip created successfully")
        
        return color_clip, blue_clip
        
    except Exception as e:
        print(f"❌ ColorClip test failed: {e}")
        return None, None

def test_audio_extraction():
    """Test audio extraction from video"""
    print("\n=== Testing Audio Extraction ===")
    
    video_path = r"C:\Users\Admin\Downloads\The.Simpsons.S35E11.1080p.WEB.h264-BAE[TGx]\video.mkv"
    
    if not os.path.exists(video_path):
        print("❌ Video file not found, skipping audio extraction test")
        return None
    
    try:
        video = VideoFileClip(video_path)
        
        if video.audio is not None:
            print("✓ Audio track found in video")
            
            # Test audio extraction
            audio_clip = video.audio
            print(f"✓ Audio extracted: {audio_clip.duration:.2f} seconds")
            
            # Test writing audio to file
            temp_audio_path = "temp_audio.mp3"
            audio_clip.write_audiofile(temp_audio_path)
            print("✓ Audio written to file successfully")
            
            # Clean up
            if os.path.exists(temp_audio_path):
                os.remove(temp_audio_path)
                print("✓ Temporary audio file cleaned up")
            
            video.close()
            return audio_clip
        else:
            print("❌ No audio track found in video")
            video.close()
            return None
            
    except Exception as e:
        print(f"❌ Audio extraction test failed: {e}")
        return None

def test_composite_video():
    """Test CompositeVideoClip functionality"""
    print("\n=== Testing CompositeVideoClip ===")
    
    try:
        # Create a color background
        bg_clip = ColorClip(size=(400, 300), color=(0, 0, 0), duration=3)
        
        # Create text overlay
        txt_clip = TextClip(
            text="Composite Test",
            font_size=60,
            color="white",
            duration=3
        )
        
        # Try different positioning methods
        try:
            positioned_txt = txt_clip.with_position('center')
        except:
            try:
                positioned_txt = txt_clip.set_position('center')
            except:
                # If positioning doesn't work, use the text clip as is
                positioned_txt = txt_clip
        
        # Combine them
        composite = CompositeVideoClip([bg_clip, positioned_txt])
        print("✓ CompositeVideoClip created successfully")
        
        return composite
        
    except Exception as e:
        print(f"❌ CompositeVideoClip test failed: {e}")
        return None

def test_concatenate_clips():
    """Test concatenate_videoclips functionality"""
    print("\n=== Testing concatenate_videoclips ===")
    
    try:
        # Create multiple color clips
        clip1 = ColorClip(size=(200, 100), color=(255, 0, 0), duration=1)
        clip2 = ColorClip(size=(200, 100), color=(0, 255, 0), duration=1)
        clip3 = ColorClip(size=(200, 100), color=(0, 0, 255), duration=1)
        
        # Concatenate them
        concatenated = concatenate_videoclips([clip1, clip2, clip3])
        print("✓ Clips concatenated successfully")
        print(f"  - Total duration: {concatenated.duration:.2f} seconds")
        
        return concatenated
        
    except Exception as e:
        print(f"❌ concatenate_videoclips test failed: {e}")
        return None

def test_clip_modifications():
    """Test clip modification methods"""
    print("\n=== Testing Clip Modifications ===")
    
    try:
        # Create a test clip
        clip = ColorClip(size=(300, 200), color=(255, 255, 0), duration=5)
        print("✓ Base clip created")
        
        # Test with_* methods
        modified_clip = clip.with_duration(3)
        print(f"✓ Duration modified: {modified_clip.duration:.2f}s")
        
        # Test resizing
        resized_clip = clip.resized(width=150)
        print(f"✓ Resized clip: {resized_clip.size}")
        
        # Test cropping
        cropped_clip = clip.crop(x1=50, y1=50, x2=250, y2=150)
        print(f"✓ Cropped clip: {cropped_clip.size}")
        
        # Test rotation
        rotated_clip = clip.rotate(45)
        print(f"✓ Rotated clip: {rotated_clip.size}")
        
        return clip, modified_clip, resized_clip, cropped_clip, rotated_clip
        
    except Exception as e:
        print(f"❌ Clip modifications test failed: {e}")
        return None, None, None, None, None

def test_effects():
    """Test MoviePy effects"""
    print("\n=== Testing MoviePy Effects ===")
    
    try:
        # Create a test clip
        clip = ColorClip(size=(300, 200), color=(255, 255, 0), duration=3)
        print("✓ Base clip created for effects testing")
        
        # Test visual effects
        try:
            # Test resize effect
            resized_effect = clip.with_effects([vfx.Resize(width=200)])
            print("✓ Resize effect applied")
            
            # Test color multiplication
            darkened_effect = clip.with_effects([vfx.MultiplyColor(0.5)])
            print("✓ Color multiplication effect applied")
            
            # Test speed modification
            speed_effect = clip.with_effects([vfx.MultiplySpeed(2)])
            print("✓ Speed modification effect applied")
            
            return clip, resized_effect, darkened_effect, speed_effect
            
        except Exception as e:
            print(f"⚠ Effects test failed: {e}")
            return clip, None, None, None
            
    except Exception as e:
        print(f"❌ Effects test failed: {e}")
        return None, None, None, None

def test_time_transform():
    """Test time transformation"""
    print("\n=== Testing Time Transform ===")
    
    try:
        # Create a test clip
        clip = ColorClip(size=(200, 100), color=(255, 0, 255), duration=4)
        print("✓ Base clip created for time transform")
        
        # Test acceleration
        accelerated = clip.time_transform(lambda t: t * 2)
        print("✓ Time acceleration applied (2x speed)")
        
        # Test sine wave time warping
        sine_warped = clip.time_transform(lambda t: 1 + math.sin(t))
        print("✓ Sine wave time warping applied")
        
        return clip, accelerated, sine_warped
        
    except Exception as e:
        print(f"❌ Time transform test failed: {e}")
        return None, None, None

def test_image_transform():
    """Test image transformation"""
    print("\n=== Testing Image Transform ===")
    
    try:
        # Create a test clip
        clip = ColorClip(size=(200, 100), color=(255, 255, 0), duration=3)
        print("✓ Base clip created for image transform")
        
        # Test color channel inversion
        def invert_green_blue(image):
            return image[:, :, [0, 2, 1]]
        
        inverted = clip.image_transform(invert_green_blue)
        print("✓ Green/Blue channel inversion applied")
        
        # Test brightness adjustment
        def brighten(image):
            return np.clip(image * 1.5, 0, 255).astype(np.uint8)
        
        brightened = clip.image_transform(brighten)
        print("✓ Brightness adjustment applied")
        
        return clip, inverted, brightened
        
    except Exception as e:
        print(f"❌ Image transform test failed: {e}")
        return None, None, None

def test_custom_effect():
    """Test custom effect creation"""
    print("\n=== Testing Custom Effect ===")
    
    try:
        # Create a test clip
        clip = ColorClip(size=(400, 200), color=(255, 255, 255), duration=5)
        print("✓ Base clip created for custom effect")
        
        # Create a custom progress bar effect
        @requires_duration
        def progress_bar(clip, color=(255, 0, 0), height=10):
            """Add a progress bar at the bottom of the clip"""
            def filter_func(get_frame, t):
                progression = t / clip.duration
                bar_width = int(progression * clip.w)
                
                frame = get_frame(t)
                frame[-height:, 0:bar_width] = color
                
                return frame
            
            return clip.transform(filter_func, apply_to="mask")
        
        # Apply the custom effect
        progress_clip = progress_bar(clip, color=(0, 255, 0), height=15)
        print("✓ Custom progress bar effect applied")
        
        return clip, progress_clip
        
    except Exception as e:
        print(f"❌ Custom effect test failed: {e}")
        return None, None

def test_clips_array():
    """Test clips_array functionality"""
    print("\n=== Testing clips_array ===")
    
    try:
        # Create multiple clips
        clip1 = ColorClip(size=(150, 100), color=(255, 0, 0), duration=2)
        clip2 = ColorClip(size=(150, 100), color=(0, 255, 0), duration=2)
        clip3 = ColorClip(size=(150, 100), color=(0, 0, 255), duration=2)
        clip4 = ColorClip(size=(150, 100), color=(255, 255, 0), duration=2)
        
        # Create 2x2 array
        array = [
            [clip1, clip2],
            [clip3, clip4]
        ]
        
        final_clip = clips_array(array)
        print("✓ 2x2 clips array created successfully")
        print(f"  - Final size: {final_clip.size}")
        
        return final_clip
        
    except Exception as e:
        print(f"❌ clips_array test failed: {e}")
        return None

def test_advanced_compositing():
    """Test advanced compositing with timing and positioning"""
    print("\n=== Testing Advanced Compositing ===")
    
    try:
        # Create background
        bg = ColorClip(size=(500, 300), color=(0, 0, 0), duration=6)
        
        # Create text clips with different timing
        title = TextClip(
            text="MoviePy Test",
            font_size=60,
            color="white",
            duration=2
        )
        
        subtitle = TextClip(
            text="Advanced Compositing",
            font_size=40,
            color="yellow",
            duration=3
        )
        
        # Position clips
        try:
            title = title.with_position(("center", 0.2), relative=True)
            subtitle = subtitle.with_position(("center", 0.6), relative=True)
        except:
            # Fallback positioning
            title = title.with_position((200, 60))
            subtitle = subtitle.with_position((200, 180))
        
        # Set timing
        title = title.with_start(0.5)
        subtitle = subtitle.with_start(2)
        
        # Create composite
        composite = CompositeVideoClip([bg, title, subtitle])
        print("✓ Advanced composite created with timing and positioning")
        
        return composite
        
    except Exception as e:
        print(f"❌ Advanced compositing test failed: {e}")
        return None

def test_audio_compositing():
    """Test audio compositing"""
    print("\n=== Testing Audio Compositing ===")
    
    try:
        # Create simple audio clips (sine waves)
        def make_sine_wave(freq, duration):
            def make_frame(t):
                return np.sin(2 * np.pi * freq * t) * 0.3
            return AudioClip(make_frame, duration=duration)
        
        # Create different frequency audio clips
        audio1 = make_sine_wave(440, 2)  # A note
        audio2 = make_sine_wave(523, 2)  # C note
        audio3 = make_sine_wave(659, 2)  # E note
        
        # Test concatenation
        concatenated = concatenate_audioclips([audio1, audio2, audio3])
        print("✓ Audio clips concatenated")
        
        # Test composition with timing
        composite = CompositeAudioClip([
            audio1.with_volume_scaled(0.5),
            audio2.with_start(1),
            audio3.with_start(2)
        ])
        print("✓ Audio clips composited with timing")
        
        return concatenated, composite
        
    except Exception as e:
        print(f"❌ Audio compositing test failed: {e}")
        return None, None

def test_video_processing_pipeline():
    """Test the complete video processing pipeline with advanced features"""
    print("\n=== Testing Complete Video Processing Pipeline ===")
    
    video_path = r"C:\Users\Admin\Downloads\The.Simpsons.S35E11.1080p.WEB.h264-BAE[TGx]\video.mkv"
    
    if not os.path.exists(video_path):
        print("❌ Video file not found, skipping pipeline test")
        return
    
    try:
        # Load video
        video = VideoFileClip(video_path)
        print("✓ Video loaded")
        
        # Create clips from different time segments with effects
        clips = []
        time_segments = [
            (60, 90, "First segment", (255, 0, 0)),
            (300, 330, "Second segment", (0, 255, 0)),
            (600, 630, "Third segment", (0, 0, 255))
        ]
        
        for start, end, description, color in time_segments:
            if end <= video.duration:
                # Extract clip using subclipped method
                clip = video.subclipped(start, end)
                
                # Apply some effects
                try:
                    clip = clip.with_effects([vfx.Resize(width=640)])
                    print(f"✓ Applied resize effect to {description}")
                except:
                    pass
                
                # Create text overlay with custom positioning
                txt_clip = TextClip(
                    text=description,
                    font_size=40,
                    color="white",
                    stroke_color="black",
                    stroke_width=2,
                    duration=clip.duration
                )
                
                # Try different positioning methods
                try:
                    positioned_txt = txt_clip.with_position(("center", 0.8), relative=True)
                except:
                    try:
                        positioned_txt = txt_clip.with_position('center')
                    except:
                        positioned_txt = txt_clip
                
                # Create progress bar effect
                @requires_duration
                def progress_bar(clip, color, height=5):
                    def filter_func(get_frame, t):
                        progression = t / clip.duration
                        bar_width = int(progression * clip.w)
                        
                        frame = get_frame(t)
                        frame[-height:, 0:bar_width] = color
                        
                        return frame
                    
                    return clip.transform(filter_func, apply_to="mask")
                
                # Apply progress bar
                clip_with_progress = progress_bar(clip, color, height=8)
                
                # Combine video and text
                final_clip = CompositeVideoClip([clip_with_progress, positioned_txt])
                clips.append(final_clip)
                print(f"✓ Created enhanced clip: {description} ({clip.duration:.2f}s)")
        
        if clips:
            # Concatenate all clips
            final_video = concatenate_videoclips(clips)
            print(f"✓ Final video created: {final_video.duration:.2f} seconds total")
            
            # Write the result
            output_path = "advanced_test_output.mp4"
            final_video.write_videofile(
                output_path,
                codec='libx264',
                audio_codec='aac',
                temp_audiofile='temp-audio.m4a',
                remove_temp=True,
                fps=video.fps
            )
            print(f"✓ Advanced video written to {output_path}")
            
            # Clean up
            video.close()
            final_video.close()
            for clip in clips:
                clip.close()
            
            print("✓ All resources cleaned up")
            
        else:
            print("❌ No clips were created")
            video.close()
            
    except Exception as e:
        print(f"❌ Advanced pipeline test failed: {e}")

def main():
    """Run all tests"""
    print("🎬 MoviePy 2.2.1 Advanced Functionality Testing")
    print("=" * 60)
    
    # Run basic tests
    video_clip = test_video_file_clip()
    txt_clip1, txt_clip2 = test_text_clip()
    color_clip1, color_clip2 = test_color_clip()
    audio_clip = test_audio_extraction()
    composite_clip = test_composite_video()
    concatenated_clip = test_concatenate_clips()
    
    # Run advanced tests
    mod_clip, mod_clip2, resized_clip, cropped_clip, rotated_clip = test_clip_modifications()
    effect_clip, resized_effect, darkened_effect, speed_effect = test_effects()
    time_clip, accelerated_clip, sine_clip = test_time_transform()
    img_clip, inverted_clip, brightened_clip = test_image_transform()
    custom_clip, progress_clip = test_custom_effect()
    array_clip = test_clips_array()
    advanced_composite = test_advanced_compositing()
    audio_concat, audio_composite = test_audio_compositing()
    
    # Test the complete pipeline
    test_video_processing_pipeline()
    
    print("\n" + "=" * 60)
    print("🎉 Advanced testing completed!")
    print("If all tests passed, your MoviePy setup supports advanced features.")
    
    # Clean up all clips
    clips_to_clean = [
        video_clip, txt_clip1, txt_clip2, color_clip1, color_clip2, 
        audio_clip, composite_clip, concatenated_clip, mod_clip, mod_clip2,
        resized_clip, cropped_clip, rotated_clip, effect_clip, resized_effect,
        darkened_effect, speed_effect, time_clip, accelerated_clip, sine_clip,
        img_clip, inverted_clip, brightened_clip, custom_clip, progress_clip,
        array_clip, advanced_composite, audio_concat, audio_composite
    ]
    
    for clip in clips_to_clean:
        if clip is not None:
            try:
                clip.close()
            except:
                pass

if __name__ == "__main__":
    main() 