# VideoClipper

VideoClipper is a Python-based tool for advanced video editing, subtitle handling, and automated video processing. It is designed for content creators, educators, and developers who need to automate video editing workflows, generate subtitles, and process videos programmatically.

## Features
- Automated video editing using Python and MoviePy
- Subtitle generation and handling
- Font and style customization
- Cloud deployment yet to come
- Server/client support
- Comprehensive testing

## Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/roy-alon/VideoClipper.git
   cd VideoClipper
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. (Optional) Set up your `.env` file for environment variables (not included in repo).

## Usage
Run the main script in GPT mode (default, requires OpenAI API key):
```bash
python main.py --mode gpt
```
Run the main script in local mode (uses pre-generated timestamps from JSON):
```bash
python main.py --mode local --json_path generated_timestamps.json
```

For more details, see [VideoClipper/README.md](VideoClipper/README.md). 