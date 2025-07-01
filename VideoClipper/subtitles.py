from dataclasses import dataclass
from typing import List
import re

@dataclass
class Subtitle:
    start_time: float
    end_time: float
    text: str

class SubtitleParser:
    @staticmethod
    def parse_srt(srt_content: str) -> List[Subtitle]:
        subtitles = []
        lines = srt_content.strip().split('\n')
        i = 0
        while i < len(lines):
            if not lines[i].strip():
                i += 1
                continue
            try:
                # Subtitle number
                i += 1
                # Time line
                time_line = lines[i]
                start_time, end_time = SubtitleParser.parse_srt_time(time_line)
                i += 1
                # Subtitle text (may span multiple lines)
                text_lines = []
                while i < len(lines) and lines[i].strip():
                    text_lines.append(lines[i].strip())
                    i += 1
                subtitle_text = ' '.join(text_lines)
                # Remove all {...} and [...] from subtitle text
                subtitle_text = re.sub(r'\{.*?\}', '', subtitle_text)
                subtitle_text = re.sub(r'\[.*?\]', '', subtitle_text)
                subtitles.append(Subtitle(start_time, end_time, subtitle_text))
            except (ValueError, IndexError):
                i += 1
        return subtitles

    @staticmethod
    def parse_srt_time(time_line: str):
        start_str, end_str = time_line.split(' --> ')
        def time_to_seconds(time_str):
            time_parts = time_str.replace(',', '.').split(':')
            hours = int(time_parts[0])
            minutes = int(time_parts[1])
            seconds = float(time_parts[2])
            return hours * 3600 + minutes * 60 + seconds
        start_time = time_to_seconds(start_str)
        end_time = time_to_seconds(end_str)
        return start_time, end_time

    @staticmethod
    def subtitles_to_transcript(subtitles: List[Subtitle]) -> str:
        return '\n'.join([s.text for s in subtitles]) 