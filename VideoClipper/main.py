import os
from datetime import datetime
from dotenv import load_dotenv
from subtitles import SubtitleParser
from gpt_analysis import GPTAnalyzer
from video_editor import VideoEditor

load_dotenv()

def main():
    # Keep base_folder for input files
    base_folder = r"C:\Users\Admin\Downloads\The.Simpsons.S35E11.1080p.WEB.h264-BAE[TGx]\\"
    
    # Use base_folder for input files, timestamped path for output
    input_video = base_folder + "video.mkv"
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_video = f"youtube_shorts_output_{timestamp}.mp4"  # Timestamped output
    srt_path = base_folder + "subtitles.srt"
    
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("❌ OPENAI_API_KEY not found in environment variables")
        return
        
    if not os.path.exists(input_video):
        print(f"Error: Video file not found at {input_video}")
        print("Please check the base_folder path and ensure video.mkv exists")
        return
    if not os.path.exists(srt_path):
        print(f"Error: SRT file not found at {srt_path}")
        print("Please check the base_folder path and ensure subtitles.srt exists")
        return
        
    print("🎬 Starting VideoClipper processing...")
    print(f"📹 Input video: {input_video}")
    print(f"📝 Subtitles: {srt_path}")
    print(f"🎯 Output: {output_video}")
    
    # Parse subtitles
    with open(srt_path, 'r', encoding='utf-8') as f:
        srt_content = f.read()
    subtitles = SubtitleParser.parse_srt(srt_content)
    print(f"✅ Parsed {len(subtitles)} subtitle segments")
    
    # Convert to transcript
    transcript = SubtitleParser.subtitles_to_transcript(subtitles)
    print(f"📄 Transcript length: {len(transcript)} characters")
    
    # Analyze with GPT
    print("🤖 Analyzing with GPT-4...")
    analyzer = GPTAnalyzer(api_key)
    timestamps = analyzer.analyze_transcript(transcript)
    
    if not timestamps:
        print("❌ Failed to generate timestamps from subtitles.")
        return
        
    if 'video_summary' not in timestamps or not isinstance(timestamps['video_summary'], list):
        print("❌ Invalid timestamp structure returned by GPT.")
        return
        
    print(f"✅ Generated {len(timestamps['video_summary'])} timestamp segments")
    
    # Create video
    print("🎬 Creating enhanced video...")
    editor = VideoEditor()
    editor.create_edited_video(input_video, timestamps, output_video, subtitles=subtitles)
    
    print(f"🎉 Video processing completed!")
    print(f"📁 Output saved to: {output_video}")
    print("🚀 Ready for download!")

if __name__ == "__main__":
    main()