#!/usr/bin/env python3
"""
Simple test script to test video editing with test_input_video.mp4 and demo_subtitles.srt
"""

import os
from datetime import datetime
from video_editor import VideoEditor
from subtitles import SubtitleParser

def test_video_editing():
    """Test video editing with test files"""
    print("🎬 Testing Video Editor with Test Files")
    print("=" * 50)
    
    # Test files
    video_path = "test_input_video.mp4"
    subtitle_path = "demo_subtitles.srt"
    
    # Create unique output filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = f"test_output_{timestamp}.mp4"
    
    # Check if test files exist
    if not os.path.exists(video_path):
        print(f"❌ Test video not found: {video_path}")
        return
    
    if not os.path.exists(subtitle_path):
        print(f"❌ Test subtitles not found: {subtitle_path}")
        return
    
    try:
        # Initialize video editor
        editor = VideoEditor()
        
        # Load subtitles
        print("📝 Loading subtitles...")
        with open(subtitle_path, 'r', encoding='utf-8') as f:
            srt_content = f.read()
        subtitles = SubtitleParser.parse_srt(srt_content)
        print(f"✅ Loaded {len(subtitles)} subtitles")
        
        # Show first few subtitles (after cleaning)
        print("\n📄 First 3 subtitles (after cleaning):")
        for i, sub in enumerate(subtitles[:3]):
            print(f"  {i+1}. {sub.start_time:.1f}s - {sub.end_time:.1f}s: {sub.text}")
        
        # Create test timestamps (simple segments)
        test_timestamps = {
            "video_summary": [
                {
                    "start_time": 2.0,
                    "end_time": 8.0,
                    "description": "First test segment",
                    "category": "test"
                },
                {
                    "start_time": 10.0,
                    "end_time": 16.0,
                    "description": "Second test segment", 
                    "category": "test"
                }
            ]
        }
        
        print(f"\n🎯 Test timestamps created: {len(test_timestamps['video_summary'])} segments")
        print(f"📁 Output will be saved as: {output_path}")
        
        # Create enhanced video
        print("\n🎬 Creating enhanced video...")
        editor.create_edited_video(
            input_video_path=video_path,
            timestamps=test_timestamps,
            output_path=output_path,
            subtitles=subtitles
        )
        
        if os.path.exists(output_path):
            print(f"\n✅ Test completed successfully!")
            print(f"📁 Output saved to: {output_path}")
            
            # Get file size
            file_size = os.path.getsize(output_path) / (1024 * 1024)  # MB
            print(f"📊 File size: {file_size:.1f} MB")
            
            # List all test outputs
            test_outputs = [f for f in os.listdir('.') if f.startswith('test_output_') and f.endswith('.mp4')]
            test_outputs.sort(reverse=True)  # Most recent first
            print(f"\n📋 All test outputs ({len(test_outputs)} files):")
            for i, output in enumerate(test_outputs[:5]):  # Show last 5
                size = os.path.getsize(output) / (1024 * 1024)
                print(f"  {i+1}. {output} ({size:.1f} MB)")
            if len(test_outputs) > 5:
                print(f"  ... and {len(test_outputs) - 5} more")
        else:
            print("❌ Output file not created")
            
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_video_editing() 