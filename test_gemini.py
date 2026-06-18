import os

from dotenv import load_dotenv
from google import genai

import config

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
print("Key found:", bool(api_key))

if not api_key:
    raise RuntimeError("GEMINI_API_KEY is missing from your .env file.")

client = genai.Client(api_key=api_key)

response = client.models.generate_content(
    model=config.GEMINI_MODEL,
    contents="Say hello in one sentence."
)

print(response.text)
