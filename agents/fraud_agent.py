import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

def analyze_job(job_description):

    if not job_description:
        return "Please provide a job description."

    try:

        prompt = f"""
You are an expert in detecting fake job postings.

Analyze the following job description and provide:

1. Fraud Risk Score (0-100)
2. Risk Level
3. Suspicious Indicators
4. Recommendation
5. Final Verdict

Job Description:
{job_description}
"""

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        return response.text

    except Exception as e:
        return f"Gemini Error: {str(e)}"