#!/usr/bin/env python3
"""
Quick test for the updated video editor with improved resizing
"""

import os
from video_editor import VideoEditor
from subtitles import SubtitleParser

def test_updated_editor():
    """Test the updated video editor with improved resizing"""
    print("🎬 Testing Updated Video Editor with Improved Resizing")
    print("=" * 60)
    
    # Initialize video editor
    editor = VideoEditor()
    
    # Test video path
    video_path = "test_input_video.mp4"
    
    if not os.path.exists(video_path):
        print("❌ Test video not found, skipping test")
        return
    
    try:
        # Load subtitles if available
        subtitle_path = "demo_subtitles.srt"
        subtitles = None
        if os.path.exists(subtitle_path):
            with open(subtitle_path, 'r', encoding='utf-8') as f:
                srt_content = f.read()
            subtitles = SubtitleParser.parse_srt(srt_content)
            print(f"✓ Loaded {len(subtitles)} subtitles")
        
        # Create a test timestamp
        test_timestamps = {
            "segments": [
                {
                    "start_time": 2.0,
                    "end_time": 7.0,
                    "description": "Test segment with improved resizing",
                    "category": "test"
                }
            ]
        }
        
        print("✓ Created test timestamps")
        
        # Test the enhanced clip creation
        print("\n--- Testing Enhanced Clip Creation ---")
        
        # Load video
        from moviepy import VideoFileClip
        video = VideoFileClip(video_path)
        print(f"✓ Video loaded: {video.w}x{video.h}")
        
        # Test creating an enhanced clip
        segment = test_timestamps["segments"][0]
        enhanced_clip = editor.create_enhanced_clip(
            video=video,
            start_time=segment["start_time"],
            end_time=segment["end_time"],
            description=segment["description"],
            category=segment["category"],
            segment_index=0,
            total_segments=1,
            subtitles=subtitles
        )
        
        if enhanced_clip:
            print(f"✓ Enhanced clip created: {enhanced_clip.w}x{enhanced_clip.h}")
            
            # Save a short test clip
            output_path = "test_updated_editor_output.mp4"
            enhanced_clip.write_videofile(
                output_path,
                fps=24,
                codec='libx264',
                audio_codec='aac'
            )
            print(f"✓ Saved test clip: {output_path}")
            enhanced_clip.close()
        else:
            print("❌ Failed to create enhanced clip")
        
        video.close()
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()

def main():
    """Main test function"""
    test_updated_editor()
    print("\n✅ Test complete!")

if __name__ == "__main__":
    main() 