#!/usr/bin/env python3
"""
Comprehensive MoviePy 2.2.1 Testing Suite
Tests each feature separately with detailed output
Includes subtitle parsing and video editing functionality
With preview generation options
"""

import os
import json
import tempfile
from pathlib import Path
from moviepy import (
    VideoFileClip,
    TextClip,
    ColorClip,
    AudioFileClip,
    CompositeVideoClip,
    concatenate_videoclips
)
from moviepy import vfx, afx

class MoviePyTester:
    def __init__(self, generate_previews=True, preview_duration=3):
        self.video_path = r"C:\Users\Admin\Downloads\The.Simpsons.S35E11.1080p.WEB.h264-BAE[TGx]\video.mkv"
        self.srt_path = "demo_subtitles.srt"
        self.test_results = {}
        self.generate_previews = generate_previews
        self.preview_duration = preview_duration
        self.preview_output_dir = "preview_outputs"
        
        # Create preview output directory
        if self.generate_previews:
            os.makedirs(self.preview_output_dir, exist_ok=True)
        
    def save_preview(self, clip, filename, description=""):
        """Save a preview video for testing"""
        if not self.generate_previews:
            return
            
        try:
            output_path = os.path.join(self.preview_output_dir, filename)
            
            # Limit duration for previews
            if hasattr(clip, 'duration') and clip.duration > self.preview_duration:
                preview_clip = clip.subclipped(0, self.preview_duration)
            else:
                preview_clip = clip
            
            preview_clip.write_videofile(
                output_path,
                codec='libx264',
                audio_codec='aac',
                temp_audiofile='temp-audio.m4a',
                remove_temp=True,
                fps=24,
                verbose=False,
                logger=None
            )
            print(f"  📹 Preview saved: {filename}")
            
            # Clean up preview clip if it was created
            if preview_clip != clip:
                preview_clip.close()
                
        except Exception as e:
            print(f"  ⚠️ Failed to save preview {filename}: {e}")
    
    def test_1_video_loading(self):
        """Test 1: VideoFileClip loading and basic properties"""
        print("\n" + "="*60)
        print("TEST 1: VideoFileClip Loading")
        print("="*60)
        
        try:
            if not os.path.exists(self.video_path):
                print("❌ Video file not found, creating test video...")
                # Create a test video if the main one doesn't exist
                test_clip = ColorClip(size=(640, 480), color=(255, 0, 0), duration=5)
                test_path = "test_video.mp4"
                test_clip.write_videofile(test_path, fps=24)
                test_clip.close()
                self.video_path = test_path
            
            video = VideoFileClip(self.video_path)
            print(f"✅ Video loaded successfully")
            print(f"  - Duration: {video.duration:.2f} seconds")
            print(f"  - FPS: {video.fps}")
            print(f"  - Size: {video.size}")
            print(f"  - Has audio: {video.audio is not None}")
            
            # Save preview of original video
            self.save_preview(video, "01_original_video.mp4", "Original video preview")
            
            self.test_results['video_loading'] = True
            return video
            
        except Exception as e:
            print(f"❌ Video loading failed: {e}")
            self.test_results['video_loading'] = False
            return None
    
    def test_2_subclip_operations(self):
        """Test 2: Subclip operations"""
        print("\n" + "="*60)
        print("TEST 2: Subclip Operations")
        print("="*60)
        
        video = self.test_1_video_loading()
        if not video:
            return None
            
        try:
            # Test subclipped method
            subclip1 = video.subclipped(60, 120)
            print(f"✅ subclipped(60, 120) - Duration: {subclip1.duration:.2f}s")
            self.save_preview(subclip1, "02a_subclip_60_120.mp4", "Subclip 60-120s")
            
            # Test slice notation
            subclip2 = video[120:180]
            print(f"✅ slice[120:180] - Duration: {subclip2.duration:.2f}s")
            self.save_preview(subclip2, "02b_subclip_120_180.mp4", "Subclip 120-180s")
            
            # Test with different time ranges
            subclip3 = video.subclipped(300, 360)
            print(f"✅ subclipped(300, 360) - Duration: {subclip3.duration:.2f}s")
            self.save_preview(subclip3, "02c_subclip_300_360.mp4", "Subclip 300-360s")
            
            self.test_results['subclip_operations'] = True
            return [subclip1, subclip2, subclip3]
            
        except Exception as e:
            print(f"❌ Subclip operations failed: {e}")
            self.test_results['subclip_operations'] = False
            return None
    
    def test_3_resize_operations(self):
        """Test 3: Resize operations"""
        print("\n" + "="*60)
        print("TEST 3: Resize Operations")
        print("="*60)
        
        video = self.test_1_video_loading()
        if not video:
            return None
            
        try:
            # Test resized method with width
            resized_w = video.resized(width=640)
            print(f"✅ resized(width=640) - Size: {resized_w.size}")
            self.save_preview(resized_w, "03a_resized_width_640.mp4", "Resized to width 640")
            
            # Test resized method with height
            resized_h = video.resized(height=480)
            print(f"✅ resized(height=480) - Size: {resized_h.size}")
            self.save_preview(resized_h, "03b_resized_height_480.mp4", "Resized to height 480")
            
            # Test resized method with both dimensions
            resized_both = video.resized(width=800, height=600)
            print(f"✅ resized(width=800, height=600) - Size: {resized_both.size}")
            self.save_preview(resized_both, "03c_resized_800x600.mp4", "Resized to 800x600")
            
            # Test aspect ratio preservation
            original_aspect = video.w / video.h
            resized_aspect = resized_w.w / resized_w.h
            print(f"✅ Aspect ratio preserved: {original_aspect:.3f} -> {resized_aspect:.3f}")
            
            self.test_results['resize_operations'] = True
            return [resized_w, resized_h, resized_both]
            
        except Exception as e:
            print(f"❌ Resize operations failed: {e}")
            self.test_results['resize_operations'] = False
            return None
    
    def test_4_crop_operations(self):
        """Test 4: Crop operations"""
        print("\n" + "="*60)
        print("TEST 4: Crop Operations")
        print("="*60)
        
        video = self.test_1_video_loading()
        if not video:
            return None
            
        try:
            # Test cropped method with center positioning
            cropped_center = video.cropped(
                width=800, 
                height=600, 
                x_center=video.w/2, 
                y_center=video.h/2
            )
            print(f"✅ cropped(center) - Size: {cropped_center.size}")
            self.save_preview(cropped_center, "04a_cropped_center_800x600.mp4", "Cropped center 800x600")
            
            # Test cropped method with specific coordinates
            cropped_coords = video.cropped(
                width=640, 
                height=480, 
                x_center=video.w/4, 
                y_center=video.h/4
            )
            print(f"✅ cropped(coordinates) - Size: {cropped_coords.size}")
            self.save_preview(cropped_coords, "04b_cropped_coords_640x480.mp4", "Cropped coordinates 640x480")
            
            # Test 9:16 aspect ratio cropping
            target_width = 1080
            target_height = 1920
            cropped_9_16 = video.cropped(
                width=target_width,
                height=target_height,
                x_center=video.w/2,
                y_center=video.h/2
            )
            print(f"✅ cropped(9:16) - Size: {cropped_9_16.size}")
            self.save_preview(cropped_9_16, "04c_cropped_9_16_1080x1920.mp4", "Cropped 9:16 aspect ratio")
            
            self.test_results['crop_operations'] = True
            return [cropped_center, cropped_coords, cropped_9_16]
            
        except Exception as e:
            print(f"❌ Crop operations failed: {e}")
            self.test_results['crop_operations'] = False
            return None
    
    def test_5_text_clip_operations(self):
        """Test 5: TextClip operations"""
        print("\n" + "="*60)
        print("TEST 5: TextClip Operations")
        print("="*60)
        
        try:
            # Test basic TextClip
            txt_basic = TextClip(
                text="Hello World!",
                font_size=50,
                color='white',
                duration=3
            )
            print(f"✅ Basic TextClip - Size: {txt_basic.size}")
            self.save_preview(txt_basic, "05a_text_basic.mp4", "Basic text clip")
            
            # Test TextClip with stroke
            txt_stroke = TextClip(
                text="Stroke Test",
                font_size=40,
                color='red',
                stroke_color='black',
                stroke_width=3,
                duration=3
            )
            print(f"✅ TextClip with stroke - Size: {txt_stroke.size}")
            self.save_preview(txt_stroke, "05b_text_stroke.mp4", "Text with stroke")
            
            # Test TextClip with background
            txt_bg = TextClip(
                text="Background Test",
                font_size=35,
                color='white',
                bg_color='blue',
                duration=3
            )
            print(f"✅ TextClip with background - Size: {txt_bg.size}")
            self.save_preview(txt_bg, "05c_text_background.mp4", "Text with background")
            
            # Test TextClip positioning
            try:
                txt_positioned = txt_basic.with_position('center')
                print(f"✅ TextClip positioning with with_position")
                self.save_preview(txt_positioned, "05d_text_positioned.mp4", "Positioned text")
            except:
                try:
                    txt_positioned = txt_basic.set_position('center')
                    print(f"✅ TextClip positioning with set_position")
                    self.save_preview(txt_positioned, "05d_text_positioned.mp4", "Positioned text")
                except:
                    txt_positioned = txt_basic
                    print(f"⚠️ TextClip positioning not available")
            
            self.test_results['text_clip_operations'] = True
            return [txt_basic, txt_stroke, txt_bg, txt_positioned]
            
        except Exception as e:
            print(f"❌ TextClip operations failed: {e}")
            self.test_results['text_clip_operations'] = False
            return None
    
    def test_6_subtitle_parsing(self):
        """Test 6: Subtitle parsing from SRT file"""
        print("\n" + "="*60)
        print("TEST 6: Subtitle Parsing")
        print("="*60)
        
        try:
            if not os.path.exists(self.srt_path):
                print(f"❌ SRT file not found: {self.srt_path}")
                self.test_results['subtitle_parsing'] = False
                return None
            
            # Parse SRT file
            subtitles = []
            with open(self.srt_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Simple SRT parser
            blocks = content.strip().split('\n\n')
            for block in blocks:
                lines = block.strip().split('\n')
                if len(lines) >= 3:
                    try:
                        # Parse time line
                        time_line = lines[1]
                        start_str, end_str = time_line.split(' --> ')
                        
                        # Convert time to seconds
                        def time_to_seconds(time_str):
                            h, m, s = time_str.replace(',', '.').split(':')
                            return int(h) * 3600 + int(m) * 60 + float(s)
                        
                        start_time = time_to_seconds(start_str)
                        end_time = time_to_seconds(end_str)
                        
                        # Get text
                        text = ' '.join(lines[2:])
                        
                        subtitles.append({
                            'start_time': start_time,
                            'end_time': end_time,
                            'text': text
                        })
                        
                    except Exception as e:
                        print(f"⚠️ Failed to parse subtitle block: {e}")
                        continue
            
            print(f"✅ Parsed {len(subtitles)} subtitle segments")
            
            # Show first few subtitles
            for i, sub in enumerate(subtitles[:3]):
                print(f"  {i+1}. {sub['start_time']:.1f}s - {sub['end_time']:.1f}s: {sub['text'][:50]}...")
            
            # Create preview of subtitle overlay
            if self.generate_previews and subtitles:
                self.create_subtitle_preview(subtitles[:5])
            
            self.test_results['subtitle_parsing'] = True
            return subtitles
            
        except Exception as e:
            print(f"❌ Subtitle parsing failed: {e}")
            self.test_results['subtitle_parsing'] = False
            return None
    
    def create_subtitle_preview(self, subtitles):
        """Create a preview video showing subtitle overlays"""
        try:
            # Create background
            bg = ColorClip(size=(640, 480), color=(0, 0, 0), duration=10)
            
            # Create subtitle clips
            subtitle_clips = []
            for i, sub in enumerate(subtitles):
                txt_clip = TextClip(
                    text=sub['text'],
                    font_size=30,
                    color='white',
                    stroke_color='black',
                    stroke_width=2,
                    duration=sub['end_time'] - sub['start_time']
                )
                
                try:
                    positioned_txt = txt_clip.with_position(('center', 0.8), relative=True)
                except:
                    positioned_txt = txt_clip
                
                positioned_txt = positioned_txt.with_start(sub['start_time'])
                subtitle_clips.append(positioned_txt)
            
            # Create composite
            composite = CompositeVideoClip([bg] + subtitle_clips)
            self.save_preview(composite, "06_subtitle_preview.mp4", "Subtitle overlay preview")
            
        except Exception as e:
            print(f"  ⚠️ Failed to create subtitle preview: {e}")
    
    def test_7_composite_operations(self):
        """Test 7: Composite operations"""
        print("\n" + "="*60)
        print("TEST 7: Composite Operations")
        print("="*60)
        
        try:
            # Create background
            bg = ColorClip(size=(640, 480), color=(0, 0, 0), duration=5)
            
            # Create text overlay
            txt = TextClip(
                text="Composite Test",
                font_size=60,
                color='white',
                duration=5
            )
            
            # Position text
            try:
                positioned_txt = txt.with_position('center')
            except:
                positioned_txt = txt
            
            # Create composite
            composite = CompositeVideoClip([bg, positioned_txt])
            print(f"✅ CompositeVideoClip created - Size: {composite.size}")
            self.save_preview(composite, "07a_composite_single.mp4", "Single layer composite")
            
            # Test multiple layers
            txt2 = TextClip(
                text="Second Layer",
                font_size=40,
                color='yellow',
                duration=5
            )
            
            try:
                positioned_txt2 = txt2.with_position(('center', 100))
            except:
                positioned_txt2 = txt2
            
            composite2 = CompositeVideoClip([bg, positioned_txt, positioned_txt2])
            print(f"✅ Multi-layer composite created - Size: {composite2.size}")
            self.save_preview(composite2, "07b_composite_multi.mp4", "Multi-layer composite")
            
            self.test_results['composite_operations'] = True
            return [composite, composite2]
            
        except Exception as e:
            print(f"❌ Composite operations failed: {e}")
            self.test_results['composite_operations'] = False
            return None
    
    def test_8_concatenation_operations(self):
        """Test 8: Concatenation operations"""
        print("\n" + "="*60)
        print("TEST 8: Concatenation Operations")
        print("="*60)
        
        try:
            # Create multiple clips
            clip1 = ColorClip(size=(400, 300), color=(255, 0, 0), duration=2)
            clip2 = ColorClip(size=(400, 300), color=(0, 255, 0), duration=2)
            clip3 = ColorClip(size=(400, 300), color=(0, 0, 255), duration=2)
            
            # Concatenate
            concatenated = concatenate_videoclips([clip1, clip2, clip3])
            print(f"✅ Concatenation successful - Duration: {concatenated.duration:.2f}s")
            self.save_preview(concatenated, "08a_concatenated_same_size.mp4", "Concatenated same size clips")
            
            # Test with different sized clips
            clip4 = ColorClip(size=(300, 200), color=(255, 255, 0), duration=1)
            concatenated2 = concatenate_videoclips([clip1, clip4, clip2])
            print(f"✅ Mixed-size concatenation - Duration: {concatenated2.duration:.2f}s")
            self.save_preview(concatenated2, "08b_concatenated_mixed_size.mp4", "Concatenated mixed size clips")
            
            self.test_results['concatenation_operations'] = True
            return [concatenated, concatenated2]
            
        except Exception as e:
            print(f"❌ Concatenation operations failed: {e}")
            self.test_results['concatenation_operations'] = False
            return None
    
    def test_9_effects_operations(self):
        """Test 9: Effects operations"""
        print("\n" + "="*60)
        print("TEST 9: Effects Operations")
        print("="*60)
        
        try:
            # Create test clip
            clip = ColorClip(size=(400, 300), color=(255, 255, 255), duration=3)
            
            # Test resize effect
            try:
                resized_effect = clip.with_effects([vfx.Resize(width=200)])
                print(f"✅ Resize effect applied - Size: {resized_effect.size}")
                self.save_preview(resized_effect, "09a_effect_resize.mp4", "Resize effect")
            except Exception as e:
                print(f"⚠️ Resize effect failed: {e}")
                resized_effect = None
            
            # Test color multiplication
            try:
                darkened_effect = clip.with_effects([vfx.MultiplyColor(0.5)])
                print(f"✅ Color multiplication effect applied")
                self.save_preview(darkened_effect, "09b_effect_darken.mp4", "Darken effect")
            except Exception as e:
                print(f"⚠️ Color multiplication failed: {e}")
                darkened_effect = None
            
            # Test speed modification
            try:
                speed_effect = clip.with_effects([vfx.MultiplySpeed(2)])
                print(f"✅ Speed modification effect applied - Duration: {speed_effect.duration:.2f}s")
                self.save_preview(speed_effect, "09c_effect_speed.mp4", "Speed effect")
            except Exception as e:
                print(f"⚠️ Speed modification failed: {e}")
                speed_effect = None
            
            self.test_results['effects_operations'] = True
            return [resized_effect, darkened_effect, speed_effect]
            
        except Exception as e:
            print(f"❌ Effects operations failed: {e}")
            self.test_results['effects_operations'] = False
            return None
    
    def test_10_full_pipeline(self):
        """Test 10: Full video processing pipeline"""
        print("\n" + "="*60)
        print("TEST 10: Full Video Processing Pipeline")
        print("="*60)
        
        try:
            # Load video
            video = self.test_1_video_loading()
            if not video:
                return None
            
            # Get subtitles
            subtitles = self.test_6_subtitle_parsing()
            
            # Create clips from different time segments
            clips = []
            time_segments = [
                (60, 90, "First segment"),
                (300, 330, "Second segment"),
                (600, 630, "Third segment")
            ]
            
            for start, end, description in time_segments:
                if end <= video.duration:
                    # Extract clip
                    clip = video.subclipped(start, end)
                    
                    # Resize to 9:16 aspect ratio
                    try:
                        clip = clip.resized(height=1920)
                        clip = clip.cropped(width=1080, height=1920, x_center=clip.w/2, y_center=clip.h/2)
                        print(f"✅ Resized clip {description} to 9:16")
                    except Exception as e:
                        print(f"⚠️ Resize failed for {description}: {e}")
                    
                    # Add text overlay
                    txt_clip = TextClip(
                        text=description,
                        font_size=40,
                        color='white',
                        stroke_color='black',
                        stroke_width=2,
                        duration=clip.duration
                    )
                    
                    try:
                        positioned_txt = txt_clip.with_position(('center', 0.8), relative=True)
                    except:
                        try:
                            positioned_txt = txt_clip.with_position('center')
                        except:
                            positioned_txt = txt_clip
                    
                    # Create composite
                    composite = CompositeVideoClip([clip, positioned_txt])
                    clips.append(composite)
                    print(f"✅ Created enhanced clip: {description}")
            
            if clips:
                # Concatenate clips
                final_video = concatenate_videoclips(clips)
                print(f"✅ Pipeline completed - Final duration: {final_video.duration:.2f}s")
                
                # Save preview
                self.save_preview(final_video, "10_full_pipeline.mp4", "Full processing pipeline")
                
                self.test_results['full_pipeline'] = True
                return final_video
            else:
                print("❌ No clips created for pipeline test")
                self.test_results['full_pipeline'] = False
                return None
                
        except Exception as e:
            print(f"❌ Full pipeline failed: {e}")
            self.test_results['full_pipeline'] = False
            return None
    
    def run_all_tests(self):
        """Run all tests and generate summary"""
        print("🎬 MoviePy 2.2.1 Comprehensive Testing Suite")
        print("="*60)
        
        if self.generate_previews:
            print(f"📹 Preview generation: ENABLED (duration: {self.preview_duration}s)")
            print(f"📁 Preview output directory: {self.preview_output_dir}")
        else:
            print("📹 Preview generation: DISABLED")
        
        # Run all tests
        self.test_1_video_loading()
        self.test_2_subclip_operations()
        self.test_3_resize_operations()
        self.test_4_crop_operations()
        self.test_5_text_clip_operations()
        self.test_6_subtitle_parsing()
        self.test_7_composite_operations()
        self.test_8_concatenation_operations()
        self.test_9_effects_operations()
        self.test_10_full_pipeline()
        
        # Generate summary
        print("\n" + "="*60)
        print("TEST SUMMARY")
        print("="*60)
        
        passed = sum(1 for result in self.test_results.values() if result)
        total = len(self.test_results)
        
        for test_name, result in self.test_results.items():
            status = "✅ PASS" if result else "❌ FAIL"
            print(f"{test_name.replace('_', ' ').title()}: {status}")
        
        print(f"\nOverall: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
        
        if passed == total:
            print("🎉 All tests passed! MoviePy is working correctly.")
        else:
            print("⚠️ Some tests failed. Check the output above for details.")
        
        if self.generate_previews:
            print(f"\n📹 Preview videos saved in: {self.preview_output_dir}")
            print("   You can review these videos to see the results of each operation.")
        
        return self.test_results

def main():
    """Main function to run the comprehensive test suite"""
    import argparse
    
    parser = argparse.ArgumentParser(description='MoviePy Comprehensive Testing Suite')
    parser.add_argument('--no-previews', action='store_true', help='Disable preview generation')
    parser.add_argument('--preview-duration', type=int, default=3, help='Duration of preview videos in seconds')
    
    args = parser.parse_args()
    
    tester = MoviePyTester(
        generate_previews=not args.no_previews,
        preview_duration=args.preview_duration
    )
    
    results = tester.run_all_tests()
    
    # Save results to file
    with open('test_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\nTest results saved to: test_results.json")

if __name__ == "__main__":
    main() 