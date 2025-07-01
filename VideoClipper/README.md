# VideoClipper

VideoClipper is a Python-based tool for advanced video editing, subtitle handling, and automated video processing. It is designed for content creators, educators, and developers who need to automate video editing workflows, generate subtitles, and process videos programmatically.

## Features
- **Automated Video Editing:** Scriptable video editing using Python and MoviePy.
- **Subtitle Generation & Handling:** Easily add, edit, and synchronize subtitles.
- **Font & Style Customization:** Supports custom fonts and advanced text rendering.
- **Cloud Deployment:** Ready for deployment on cloud platforms (see `cloud_deployment.md`).
- **Server/Client Support:** Can be run as a server for remote video processing.
- **Comprehensive Testing:** Includes a suite of tests for video, font, and subtitle features.

## Project Structure
```
VideoClipper/
├── main.py                # Main entry point
├── video_editor.py        # Core video editing logic
├── subtitles.py           # Subtitle handling utilities
├── gpt_analysis.py        # GPT-based video analysis
├── server_setup.py        # Server setup for remote processing
├── requirements.txt       # Python dependencies
├── test_*.py              # Test scripts
├── media_src/             # Source media files
├── test_outputs/          # Output from tests
├── Rubik_Wet_Paint/       # Custom font files
├── ...
```
**Note:** Ignore the nested `/VideoClipper` folder inside the main project directory. It is not part of the main codebase and should not be included in the repository.

## Setup
1. Clone the repository:
   ```bash
   git clone <repo-url>
   cd VideoClipper
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. (Optional) Set up your `.env` file for environment variables (not included in repo).

## Usage
- Run the main script in GPT mode (default, requires OpenAI API key):
  ```bash
  python main.py --mode gpt
  ```
- Run the main script in local mode (uses pre-generated timestamps from JSON):
  ```bash
  python main.py --mode local --json_path generated_timestamps.json
  ```
  - You can specify a different JSON file with the `--json_path` option.

**Mode explanation:**
- Use `gpt` mode to generate timestamps using the OpenAI API (requires tokens and API key).
- Use `local` mode to use existing timestamps from a JSON file (no API required, useful if you run out of tokens or want to reuse results).

- Explore the test scripts in the `tests/` directory for examples and advanced usage.

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
See `LICENSE` file (if available). 