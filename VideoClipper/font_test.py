#!/usr/bin/env python3
"""
Font testing script for MoviePy
"""

import os
from moviepy import TextClip, ColorClip, CompositeVideoClip
from PIL import ImageFont
import matplotlib.font_manager as fm

def test_available_fonts():
    """Test and list available fonts"""
    print("=== Testing Available Fonts ===")
    
    # Get system fonts
    font_list = fm.findSystemFonts()
    print(f"Found {len(font_list)} system fonts")
    
    # Test some common fonts
    test_fonts = [
        'Arial',
        'Arial-Bold',
        'arial.ttf',
        'arial',
        'Helvetica',
        'Times New Roman',
        'DejaVu Sans',
        'Liberation Sans',
        'FreeSans',
        'Ubuntu',
        'Verdana',
        'Tahoma',
        'Georgia',
        'Courier New'
    ]
    
    working_fonts = []
    
    for font_name in test_fonts:
        try:
            # Test with PIL
            test_font = ImageFont.truetype(font_name, 24)
            print(f"✅ PIL: {font_name} - OK")
            working_fonts.append(font_name)
        except:
            try:
                # Try with fallback
                test_font = ImageFont.load_default()
                print(f"⚠️ PIL: {font_name} - Using default")
            except:
                print(f"❌ PIL: {font_name} - Failed")
    
    return working_fonts

def test_moviepy_fonts():
    """Test fonts with MoviePy TextClip"""
    print("\n=== Testing MoviePy TextClip Fonts ===")
    
    # Create a background
    bg = ColorClip(size=(400, 200), color=(0, 0, 0), duration=2)
    
    # Test fonts
    test_fonts = [
        'Arial',
        'Arial-Bold', 
        'arial.ttf',
        'arial',
        'Helvetica',
        'Times New Roman',
        'DejaVu Sans',
        'Liberation Sans',
        'FreeSans',
        'Ubuntu',
        'Verdana',
        'Tahoma',
        'Georgia',
        'Courier New',
        None  # Default
    ]
    
    working_moviepy_fonts = []
    
    for font_name in test_fonts:
        try:
            print(f"Testing MoviePy font: {font_name}")
            
            txt_clip = TextClip(
                text="Test Text",
                font_size=40,
                color='white',
                stroke_color='black',
                stroke_width=2,
                font=font_name,
                duration=1
            )
            
            # Try to get the clip size (this will trigger font loading)
            size = txt_clip.size
            print(f"✅ MoviePy: {font_name} - OK (size: {size})")
            working_moviepy_fonts.append(font_name)
            
            # Clean up
            txt_clip.close()
            
        except Exception as e:
            print(f"❌ MoviePy: {font_name} - Failed: {e}")
    
    return working_moviepy_fonts

def test_font_rendering():
    """Test actual font rendering"""
    print("\n=== Testing Font Rendering ===")
    
    # Test fonts that worked
    test_fonts = [
        'Arial',
        'arial.ttf',
        'arial',
        'Helvetica',
        'DejaVu Sans',
        'Liberation Sans',
        'FreeSans',
        'Ubuntu',
        'Verdana',
        'Tahoma',
        'Georgia',
        'Courier New',
        None
    ]
    
    for font_name in test_fonts:
        try:
            print(f"Rendering test with font: {font_name}")
            
            # Create background
            bg = ColorClip(size=(600, 300), color=(0, 0, 0), duration=2)
            
            # Create text clip
            txt_clip = TextClip(
                text="Hello World!",
                font_size=50,
                color='white',
                stroke_color='black',
                stroke_width=3,
                font=font_name,
                duration=2
            )
            
            # Position text
            try:
                positioned_txt = txt_clip.with_position('center')
            except:
                positioned_txt = txt_clip
            
            # Create composite
            composite = CompositeVideoClip([bg, positioned_txt])
            
            # Write test video
            output_path = f"font_test_{font_name or 'default'}.mp4"
            composite.write_videofile(
                output_path,
                codec='libx264',
                audio_codec='aac',
                temp_audiofile='temp-audio.m4a',
                remove_temp=True,
                fps=24
            )
            
            print(f"✅ Successfully created: {output_path}")
            
            # Clean up
            composite.close()
            txt_clip.close()
            bg.close()
            
            # Only test first working font
            break
            
        except Exception as e:
            print(f"❌ Failed to render with {font_name}: {e}")

def main():
    """Run all font tests"""
    print("🎨 Font Testing for MoviePy")
    print("=" * 50)
    
    # Test available fonts
    working_fonts = test_available_fonts()
    
    # Test MoviePy fonts
    working_moviepy_fonts = test_moviepy_fonts()
    
    # Test actual rendering
    test_font_rendering()
    
    print("\n" + "=" * 50)
    print("📋 Summary:")
    print(f"Working PIL fonts: {len(working_fonts)}")
    print(f"Working MoviePy fonts: {len(working_moviepy_fonts)}")
    
    if working_moviepy_fonts:
        print(f"✅ Recommended fonts: {working_moviepy_fonts[:3]}")

if __name__ == "__main__":
    main() 