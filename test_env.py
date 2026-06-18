import os

from dotenv import load_dotenv

load_dotenv()

print("Current folder:", os.getcwd())
print("GEMINI_API_KEY configured:", bool(os.getenv("GEMINI_API_KEY")))
