#!/usr/bin/env python3
"""
Test different font names to see which ones are available
"""

from moviepy import TextClip

def test_fonts():
    """Test different font names"""
    print("🔤 Testing Available Fonts")
    print("=" * 40)
    
    # Common font names to test
    test_fonts = [
        'Arial',
        'Arial-Bold',
        'Arial-BoldMT',
        'ArialMT',
        'Calibri',
        'Calibri-Bold',
        'Verdana',
        'Verdana-Bold',
        'Times New Roman',
        'Times New Roman-Bold',
        'Helvetica',
        'Helvetica-Bold',
        'Roboto',
        'Roboto-Bold',
        'Open Sans',
        'Open Sans-Bold',
        'arial.ttf',
        'Arial.ttf',
        'calibri.ttf',
        'verdana.ttf'
    ]
    
    working_fonts = []
    
    for font in test_fonts:
        try:
            # Try to create a small text clip with this font
            test_clip = TextClip(
                text="Test",
                font_size=20,
                font=font,
                duration=0.1
            )
            working_fonts.append(font)
            print(f"✅ {font}")
        except Exception as e:
            print(f"❌ {font} - {str(e)[:50]}...")
    
    print(f"\n📊 Results:")
    print(f"   Working fonts: {len(working_fonts)}")
    print(f"   Failed fonts: {len(test_fonts) - len(working_fonts)}")
    
    if working_fonts:
        print(f"\n🎯 **Recommended fonts:**")
        for font in working_fonts:
            print(f"   • {font}")
    
    return working_fonts

if __name__ == "__main__":
    test_fonts() 