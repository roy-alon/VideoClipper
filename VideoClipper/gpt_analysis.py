import json
from openai import OpenAI

class GPTAnalyzer:
    def __init__(self, api_key):
        self.client = OpenAI(api_key=api_key)

    def analyze_transcript(self, transcript: str):
        prompt = '''You are a video editing assistant. Given a transcript of a video (from subtitles):
1. Identify the most interesting and important moments that tell a coherent story.
2. Create timestamps for a summary video with a total length between 60 and 90 seconds.
3. Select moments that create a logical narrative flow from one to the next.
4. Return the response as JSON with the following structure:
   {
     "video_summary": [
       {
         "start_time": (number in seconds),
         "end_time": (number in seconds),
         "description": "short, engaging description",
         "category": "setup|conflict|climax|resolution|punchline"
       }
     ]
   }
5. Use categories: setup, conflict, climax, resolution, punchline.
Format your response as valid JSON.'''
        response = self.client.chat.completions.create(
            model="gpt-4-mini-high",
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": f"Here's the transcript to analyze:\n\n{transcript}"}
            ]
        )
        content = response.choices[0].message.content
        try:
            return json.loads(content)
        except json.JSONDecodeError:
            # Try to extract JSON from the response if it's wrapped in text
            if 'video_summary' in content:
                start_idx = content.find('{')
                end_idx = content.rfind('}') + 1
                if start_idx != -1 and end_idx != 0:
                    json_str = content[start_idx:end_idx]
                    return json.loads(json_str)
            return None 