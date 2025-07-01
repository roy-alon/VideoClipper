import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

try:
    models = client.models.list()
    print("Available OpenAI models:")
    for m in models.data:
        print(m.id)
except Exception as e:
    print(f"Error listing models: {e}") 