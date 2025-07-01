#!/usr/bin/env python3
"""
Simple font testing script
"""

from moviepy import TextClip

def test_simple_fonts():
    """Test simple font names"""
    print("🔤 Testing Simple Font Names")
    print("=" * 40)
    
    # Simple font names to test
    test_fonts = [
        'Arial',
        'Arial-Bold', 
        'Calibri',
        'Calibri-Bold',
        'Verdana',
        'Verdana-Bold',
        'Times New Roman',
        'Times New Roman-Bold',
        'Helvetica',
        'Helvetica-Bold',
        'arial.ttf',
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
        print(f"\n🎯 **Working fonts:**")
        for font in working_fonts:
            print(f"   • {font}")
    
    return working_fonts

if __name__ == "__main__":
    test_simple_fonts() 