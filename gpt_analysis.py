import json
from openai import OpenAI

class GPTAnalyzer:
    def __init__(self, api_key):
        self.client = OpenAI(api_key=api_key)

    def analyze_transcript(self, transcript: str, min_duration=60, max_duration=90, max_retries=3):
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

        messages = [
            {"role": "system", "content": prompt},
            {"role": "user", "content": f"Here's the transcript to analyze:\n\n{transcript}"}
        ]

        for attempt in range(1, max_retries + 1):
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=messages
            )
            content = response.choices[0].message.content
            # Save the raw response for debugging
            with open(f"last_gpt_response_attempt_{attempt}.json", "w", encoding="utf-8") as f:
                f.write(content)
            try:
                result = json.loads(content)
            except json.JSONDecodeError:
                # Try to extract JSON from the response if it's wrapped in text
                if 'video_summary' in content:
                    start_idx = content.find('{')
                    end_idx = content.rfind('}') + 1
                    if start_idx != -1 and end_idx != 0:
                        json_str = content[start_idx:end_idx]
                        result = json.loads(json_str)
                    else:
                        result = None
                else:
                    result = None
            if not result or 'video_summary' not in result or not isinstance(result['video_summary'], list):
                feedback = "The response was not valid JSON or did not contain the expected structure. Please try again and return only the correct JSON."
            else:
                # Validate total duration
                total_duration = sum(seg['end_time'] - seg['start_time'] for seg in result['video_summary'])
                if min_duration <= total_duration <= max_duration:
                    return result
                else:
                    feedback = f"The total duration of the summary is {total_duration:.1f} seconds, which is out of the required range ({min_duration}-{max_duration} seconds). Please fix it and return a new JSON."
            # Add the previous response and feedback to the next prompt
            messages.append({"role": "assistant", "content": content})
            messages.append({"role": "user", "content": feedback})
        # If all retries fail, return the last result (even if invalid)
        return result 