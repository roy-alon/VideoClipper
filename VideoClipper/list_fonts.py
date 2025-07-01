#!/usr/bin/env python3
"""
List all available fonts using TextClip.list('fonts')
"""

from moviepy import TextClip

def list_available_fonts():
    """List all available fonts on the system"""
    print("🔤 Available Fonts on Your System")
    print("=" * 50)
    
    try:
        fonts = TextClip.list('fonts')
        print(f"✅ Found {len(fonts)} available fonts:")
        print()
        
        # Group fonts by category
        bold_fonts = []
        regular_fonts = []
        other_fonts = []
        
        for font in fonts:
            font_lower = font.lower()
            if 'bold' in font_lower or 'heavy' in font_lower or 'black' in font_lower:
                bold_fonts.append(font)
            elif any(name in font_lower for name in ['arial', 'calibri', 'verdana', 'times', 'helvetica', 'roboto']):
                regular_fonts.append(font)
            else:
                other_fonts.append(font)
        
        print("🎯 **Recommended Bold Fonts:**")
        for font in sorted(bold_fonts)[:10]:  # Show first 10
            print(f"   • {font}")
        if len(bold_fonts) > 10:
            print(f"   ... and {len(bold_fonts) - 10} more")
        print()
        
        print("📝 **Common Regular Fonts:**")
        for font in sorted(regular_fonts)[:10]:  # Show first 10
            print(f"   • {font}")
        if len(regular_fonts) > 10:
            print(f"   ... and {len(regular_fonts) - 10} more")
        print()
        
        print("🔍 **All Fonts (first 20):**")
        for i, font in enumerate(sorted(fonts)[:20]):
            print(f"   {i+1:2d}. {font}")
        if len(fonts) > 20:
            print(f"   ... and {len(fonts) - 20} more fonts")
        
        print(f"\n📊 **Summary:**")
        print(f"   Total fonts: {len(fonts)}")
        print(f"   Bold fonts: {len(bold_fonts)}")
        print(f"   Regular fonts: {len(regular_fonts)}")
        print(f"   Other fonts: {len(other_fonts)}")
        
        return fonts
        
    except Exception as e:
        print(f"❌ Error listing fonts: {e}")
        return []

if __name__ == "__main__":
    list_available_fonts() 