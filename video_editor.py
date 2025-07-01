import os
import tempfile
import json
from moviepy import VideoFileClip, TextClip, ColorClip, CompositeVideoClip, concatenate_videoclips, vfx
from subtitles import Subtitle
from typing import List
import numpy as np
from PIL import Image, ImageFilter

# Use Pillow for blur

def blur_frame(frame: np.ndarray) -> np.ndarray:
    img = Image.fromarray(frame)
    return np.array(img.filter(ImageFilter.GaussianBlur(radius=20)))

class VideoEditor:
    def __init__(self):
        pass

    def create_progress_bar(self, clip, color=(255, 255, 0), height=5):
        """
        Create a custom progress bar effect - simplified version
        """
        # Check if clip has duration
        if not hasattr(clip, 'duration') or clip.duration is None:
            print("⚠️ Clip has no duration, skipping progress bar")
            return clip
        
        # Create a simple progress bar as a separate clip instead of modifying frames
        try:
            # Create a progress bar clip
            def make_progress_bar(t):
                progression = t / clip.duration
                bar_width = int(progression * clip.w)
                if bar_width <= 0:
                    bar_width = 1
                
                # Create a simple colored rectangle
                bar_clip = ColorClip(
                    size=(bar_width, height),
                    color=color,
                    duration=clip.duration
                )
                
                # Position at bottom of clip
                try:
                    positioned_bar = bar_clip.with_position(('left', 'bottom'))
                    return positioned_bar
                except:
                    return bar_clip
            
            # For now, just return the original clip without progress bar
            # The progress bar implementation is complex and error-prone
            return clip
            
        except Exception as e:
            print(f"⚠️ Progress bar failed: {e}, skipping")
            return clip

    def create_blurred_background(self, video, target_width, target_height):
        """
        Create a blurred background from the video by stretching to fill the frame, then applying a blur (using Pillow).
        """
        try:
            # Stretch video to fill the background (may crop/stretch)
            stretched_video = video.resized(width=target_width, height=target_height)
            # Apply blur effect using image_transform (Pillow)
            blurred_bg = stretched_video.image_transform(blur_frame)
            print(f"  Created full-size blurred background: {target_width}x{target_height}")
            return blurred_bg
        except Exception as e:
            print(f"  Blur background failed: {e}, using fallback")
            return ColorClip(size=(target_width, target_height), color=(0, 0, 0), duration=video.duration)

    def create_enhanced_clip(self, video, start_time, end_time, description, category, segment_index, total_segments, subtitles: List[Subtitle]=None):
        """
        Create an enhanced clip with a 9:16 blurred background and a scaled, centered foreground video (2/3 height).
        Adds word-by-word, centered subtitles at the bottom, with timing adjusted to the segment.
        """
        try:
            # Extract the clip
            clip = video.subclipped(start_time, end_time)
            target_width, target_height = 1080, 1920
            print(f"  Original size: {clip.w}x{clip.h}")
            print(f"  Target size: {target_width}x{target_height}")

            # 1. Blurred background
            print(f"  Creating blurred background...")
            bg_clip = self.create_blurred_background(clip, target_width, target_height)

            # 2. Foreground: scale to 2/3 height, center
            contained_height = int(target_height * (2/3))
            contained = clip.resized(height=contained_height)
            x_offset = (target_width - contained.w) // 2
            y_offset = (target_height - contained.h) // 2
            contained = contained.with_position((x_offset, y_offset))

            # 3. Subtitles: word-by-word, centered, timing adjusted
            word_clips = []
            if subtitles:
                clip_start = start_time
                clip_end = end_time
                for subtitle in subtitles:
                    sub_start = subtitle.start_time
                    sub_end = subtitle.end_time
                    # Only include subtitles that overlap with this segment
                    if sub_end > clip_start and sub_start < clip_end:
                        # Adjust subtitle timing relative to the clip
                        relative_start = max(0, sub_start - clip_start)
                        relative_end = min(clip.duration, sub_end - clip_start)
                        if relative_end > relative_start:
                            words = subtitle.text.split()
                            word_count = len(words)
                            if word_count == 0:
                                continue
                            word_duration = (relative_end - relative_start) / word_count
                            for i, word in enumerate(words):
                                word_start = relative_start + i * word_duration
                                word_end = word_start + word_duration
                                # Dynamically adjust font size for long words
                                max_width = int(target_width * 0.8)
                                font_size = 120
                                if len(word) > 15:
                                    font_size = 90
                                if len(word) > 25:
                                    font_size = 70
                                
                                # Always use Rubik Wet Paint font with absolute path and method='label'
                                rubik_font_path = os.path.abspath('Rubik_Wet_Paint/RubikWetPaint-Regular.ttf')
                                adjusted_font_size = font_size
                                try:
                                    txt_clip = TextClip(
                                        text=word,
                                        font_size=adjusted_font_size,
                                        color='#e0ff2e',
                                        stroke_color='#000',
                                        stroke_width=8,
                                        font=rubik_font_path,
                                        size=(max_width, 400),
                                        method='label',
                                        duration=word_duration
                                    )
                                    # Add a stronger glow effect for better visibility
                                    try:
                                        glow_clip = TextClip(
                                            text=word,
                                            font_size=adjusted_font_size + 6,  # Larger glow
                                            color='#00f',
                                            stroke_color='rgba(0,0,0,0.5)',  # More visible glow
                                            stroke_width=12,
                                            font=rubik_font_path,
                                            size=(max_width, 400),
                                            method='label',
                                            duration=word_duration
                                        )
                                        final_clip = CompositeVideoClip([glow_clip, txt_clip])
                                        txt_clip = final_clip
                                    except:
                                        pass
                                except Exception as e:
                                    print(f"❌ Failed to render word '{word}' with Rubik Wet Paint: {e}")
                                    continue
                                # Place subtitle word near the bottom (10% from bottom)
                                txt_clip = txt_clip.with_position(("center", "center"))
                                txt_clip = txt_clip.with_start(word_start)
                                word_clips.append(txt_clip)

            # 4. Composite, force output size
            all_layers = [bg_clip, contained] + word_clips
            final_clip = CompositeVideoClip(all_layers, size=(target_width, target_height))
            return final_clip
        except Exception as e:
            print(f"Error creating enhanced clip: {e}")
            try:
                simple_clip = video.subclipped(start_time, end_time)
                simple_clip = simple_clip.resized(width=1080, height=1920)
                return simple_clip
            except:
                return None

    def create_edited_video(self, input_video_path, timestamps, output_path, subtitles: List[Subtitle]=None):
        """
        Create a new video using the specified timestamps with advanced features for 9:16 aspect ratio
        """
        try:
            # Validate timestamp structure
            if not self.validate_timestamp_structure(timestamps):
                print("❌ Invalid timestamp structure, aborting video creation")
                return
            
            # Debug: Print the timestamps structure
            print("Timestamps structure:")
            print(json.dumps(timestamps, indent=2))
            
            # Save timestamps for future reference
            self.save_timestamps_to_file(timestamps)
            
            # Load the video
            video = VideoFileClip(input_video_path)
            
            # List to store video clips
            clips = []
            
            # Get moments from the validated structure
            moments = timestamps['video_summary']
            
            # Filter out moments that are beyond the video's duration
            video_duration = video.duration
            filtered_moments = []
            for moment in moments:
                if moment['start_time'] < video_duration and moment['end_time'] <= video_duration:
                    filtered_moments.append(moment)
                else:
                    print(f"⚠️ Skipping moment beyond video duration: {moment['start_time']:.1f}s - {moment['end_time']:.1f}s (video duration: {video_duration:.1f}s)")
            
            if not filtered_moments:
                print("❌ No valid moments found within video duration")
                return
            
            moments = filtered_moments
            print(f"✅ Using {len(moments)} valid moments within video duration")
            
            # Calculate total duration and adjust if needed
            total_duration = sum(moment['end_time'] - moment['start_time'] for moment in moments)
            print(f"Total duration: {total_duration:.2f} seconds")
            
            # Process each timestamp
            for i, moment in enumerate(moments):
                start_time = moment['start_time']
                end_time = moment['end_time']
                description = moment['description']
                category = moment.get('category', 'scene')
                
                print(f"Processing clip {i+1}/{len(moments)}: {start_time:.1f}s - {end_time:.1f}s")
                print(f"  Description: {description}")
                print(f"  Category: {category}")
                
                # Create enhanced clip
                enhanced_clip = self.create_enhanced_clip(
                    video, start_time, end_time, description, category, i, len(moments), subtitles
                )
                
                if enhanced_clip is not None:
                    clips.append(enhanced_clip)
                else:
                    print(f"⚠️ Failed to create clip {i+1}, skipping")
            
            if not clips:
                print("❌ No clips were created successfully")
                return
            
            print("Concatenating clips...")
            # Concatenate all clips
            final_video = concatenate_videoclips(clips)
            
            # Add a subtle fade effect between clips
            try:
                final_video = final_video.with_effects([vfx.FadeIn(0.5), vfx.FadeOut(0.5)])
            except:
                pass
            
            print("Writing final video...")
            # Write the result with high quality settings for YouTube Shorts
            final_video.write_videofile(
                output_path,
                codec='libx264',
                audio_codec='aac',
                temp_audiofile='temp-audio.m4a',
                remove_temp=True,
                fps=24,  # Lower FPS for speed
                bitrate='1000k',  # Lower bitrate for speed
                preset='ultrafast'  # Fastest encoding
            )
            
            # Close all clips
            print("Cleaning up...")
            video.close()
            for clip in clips:
                clip.close()
            final_video.close()
            
            print(f"✅ Video created successfully: {output_path}")
            print(f"📊 Final duration: {final_video.duration:.2f} seconds")
            print(f"🎬 Number of segments: {len(clips)}")
            print(f"📱 Aspect ratio: 9:16 (YouTube Shorts optimized)")
            if subtitles:
                print(f"📝 Subtitles included: {len(subtitles)} segments")
            
        except Exception as e:
            print(f"Error in creating edited video: {e}")
            # Cleanup in case of error
            if 'video' in locals():
                video.close()
            if 'clips' in locals():
                for clip in clips:
                    clip.close()
            if 'final_video' in locals():
                final_video.close()

    def validate_timestamp_structure(self, timestamps):
        """
        Validate that timestamps follow the expected structure
        """
        if not isinstance(timestamps, dict):
            print("❌ Timestamps must be a dictionary")
            return False
        
        if 'video_summary' not in timestamps:
            print("❌ Timestamps must contain 'video_summary' key")
            return False
        
        if not isinstance(timestamps['video_summary'], list):
            print("❌ 'video_summary' must be a list")
            return False
        
        for i, moment in enumerate(timestamps['video_summary']):
            required_fields = ['start_time', 'end_time', 'description', 'category']
            for field in required_fields:
                if field not in moment:
                    print(f"❌ Moment {i} missing required field: {field}")
                    return False
            
            # Validate time values
            if not isinstance(moment['start_time'], (int, float)) or not isinstance(moment['end_time'], (int, float)):
                print(f"❌ Moment {i} has invalid time values")
                return False
            
            if moment['end_time'] <= moment['start_time']:
                print(f"❌ Moment {i} has invalid time range")
                return False
        
        print("✅ Timestamp structure validation passed")
        return True

    def save_timestamps_to_file(self, timestamps, output_path="generated_timestamps.json"):
        """
        Save generated timestamps to file for future use
        """
        try:
            with open(output_path, 'w') as f:
                json.dump(timestamps, f, indent=2)
            print(f"✅ Timestamps saved to {output_path}")
        except Exception as e:
            print(f"❌ Failed to save timestamps: {e}") 