#!/usr/bin/env python3

print("Testing imports...")

try:
    print("Testing moviepy...")
    from moviepy import VideoFileClip, TextClip, CompositeVideoClip, concatenate_videoclips
    print("✓ moviepy imported successfully")
except ImportError as e:
    print(f"✗ moviepy import failed: {e}")

try:
    print("Testing openai...")
    from openai import OpenAI
    print("✓ openai imported successfully")
except ImportError as e:
    print(f"✗ openai import failed: {e}")

try:
    print("Testing python-dotenv...")
    from dotenv import load_dotenv
    print("✓ python-dotenv imported successfully")
except ImportError as e:
    print(f"✗ python-dotenv import failed: {e}")

print("Import test completed.") 