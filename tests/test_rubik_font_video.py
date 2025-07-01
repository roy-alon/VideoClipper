#!/usr/bin/env python3
"""
Create a 2-second video with Rubik Wet Paint font subtitle
"""

from moviepy import ColorClip, TextClip, CompositeVideoClip

# Video parameters
width, height = 800, 400
bg_color = (30, 30, 30)  # dark background
video_duration = 0.5

# Create background clip
bg_clip = ColorClip(size=(width, height), color=bg_color, duration=video_duration)

# Create text clip with Rubik Wet Paint font
try:
    txt_clip = TextClip(
        text="Rubik Wet Plunger!",
        font_size=120,
        color='deepskyblue',
        font='Rubik_Wet_Paint/RubikWetPaint-Regular.ttf',
        size=(width, None),
        method='caption',
        duration=video_duration
    ).with_position(('center', 'center'))

    # Composite video
    final = CompositeVideoClip([bg_clip, txt_clip], size=(width, height))
    final.write_videofile('rubik_wet_paint_test_video.mp4', fps=24, codec='libx264', audio=False)
    print("✅ 2-second video created: rubik_wet_paint_test_video.mp4")
except Exception as e:
    print(f"❌ Rubik Wet Paint video failed: {e}") 