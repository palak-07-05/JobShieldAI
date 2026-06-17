import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

print("Key Found:", API_KEY is not None)

genai.configure(api_key=API_KEY)

model = genai.GenerativeModel("gemini-2.0-flash")

response = model.generate_content("Say hello in one sentence.")

print(response.text)