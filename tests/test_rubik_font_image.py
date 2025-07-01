#!/usr/bin/env python3
"""
Test Rubik Wet Paint font by rendering a still image using absolute path
"""

from moviepy import TextClip
import os

font_path = os.path.abspath('Rubik_Wet_Paint/RubikWetPaint-Regular.ttf')

try:
    txt_clip = TextClip(
        text="Rubik Wet Paint Test!",
        font_size=120,
        color='blue',
        font=font_path,
        size=(800, 300),
        method='caption',
        duration=2
    )
    # Save a single frame as an image
    txt_clip.save_frame('rubik_wet_paint_test_absolute.png', t=0)
    print(f"✅ Rubik Wet Paint font rendered to rubik_wet_paint_test_absolute.png using absolute path: {font_path}")
except Exception as e:
    print(f"❌ Rubik Wet Paint font failed: {e}") 