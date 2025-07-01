#!/usr/bin/env python3
"""
Test Dubai-Bold font
"""

from moviepy import TextClip

def test_dubai_font():
    """Test Dubai-Bold font"""
    print("🔤 Testing Dubai-Bold Font")
    print("=" * 30)
    
    try:
        # Try to create a text clip with Dubai-Bold
        test_clip = TextClip(
            text="Test Dubai Bold",
            font_size=30,
            font="DUBAI-BOLD.TTF",
            duration=2
        )
        print("✅ Dubai-Bold font works!")
        return True
    except Exception as e:
        print(f"❌ Dubai-Bold failed: {e}")
        return False

if __name__ == "__main__":
    test_dubai_font() 