#!/usr/bin/env python3
"""
Simple font listing script
"""

from moviepy import TextClip

try:
    fonts = TextClip.list('fonts')
    print(f"Found {len(fonts)} fonts:")
    print("=" * 30)
    
    # Show first 30 fonts
    for i, font in enumerate(fonts[:30]):
        print(f"{i+1:2d}. {font}")
    
    if len(fonts) > 30:
        print(f"... and {len(fonts) - 30} more")
        
except Exception as e:
    print(f"Error: {e}") 