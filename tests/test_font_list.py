#!/usr/bin/env python3
"""
Test TextClip.list('font') to find available fonts
"""

from moviepy import TextClip

try:
    print("🔤 Testing TextClip.list('font')")
    print("=" * 40)
    
    fonts = TextClip.list('font')
    print(f"✅ Found {len(fonts)} fonts:")
    print()
    
    # Show first 30 fonts
    for i, font in enumerate(fonts[:30]):
        print(f"{i+1:2d}. {font}")
    
    if len(fonts) > 30:
        print(f"... and {len(fonts) - 30} more")
        
    print(f"\n📊 Total fonts available: {len(fonts)}")
        
except Exception as e:
    print(f"❌ Error: {e}")
    print("Trying alternative methods...")
    
    # Try other possible methods
    try:
        print("\n🔍 Trying TextClip.list('fonts')...")
        fonts = TextClip.list('fonts')
        print(f"Found {len(fonts)} fonts with 'fonts'")
    except:
        print("❌ 'fonts' method failed")
    
    try:
        print("\n🔍 Trying TextClip.list()...")
        fonts = TextClip.list()
        print(f"Found {len(fonts)} items with no parameter")
    except:
        print("❌ No parameter method failed") 