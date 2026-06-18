import os

from dotenv import load_dotenv
from google import genai

import config

load_dotenv()


_api_key = os.getenv("GEMINI_API_KEY")
_client = genai.Client(api_key=_api_key) if _api_key else None


def _generate_content(prompt: str) -> str:
    response = _client.models.generate_content(
        model=config.GEMINI_MODEL,
        contents=prompt
    )
    return response.text or "Gemini returned an empty response."


def analyze_job(job_text: str) -> str:
    if _client is None:
        return (
            "**AI Analysis Unavailable** - Gemini API key not configured.\n\n"
            "Add `GEMINI_API_KEY` to your `.env` file to enable AI deep analysis."
        )

    prompt = f"""
You are JobShield AI, an expert fraud detection analyst specializing in fake and scam job postings.

Analyze the following job posting and provide a detailed fraud assessment report.

JOB POSTING:
\"\"\"
{job_text}
\"\"\"

Provide your analysis in the following structured Markdown format:

## Fraud Risk Summary
State the overall risk level (HIGH / MEDIUM / LOW) and a one-sentence verdict.

## Red Flags Detected
List every suspicious element found. If none, say "No significant red flags found."

## Legitimate Indicators
List credibility signals. If none, say "No strong legitimacy indicators found."

## Linguistic Analysis
Comment on the language style, urgency tactics, vague claims, unrealistic promises, grammar issues.

## Risk Breakdown
Briefly score these categories (High / Medium / Low risk):
- Compensation Claims
- Company Transparency
- Requirements Realism
- Contact & Process Legitimacy
- Urgency & Pressure Tactics

## Final Recommendation
Give clear, actionable advice for a job seeker reading this posting.

Be concise, direct, and helpful. Use bullet points where appropriate.
"""

    try:
        return _generate_content(prompt)
    except Exception as e:
        return (
            f"**AI Analysis Error**: {str(e)}\n\n"
            "The ML model prediction above is still valid."
        )


def generate_dashboard_insights(rows: list) -> str:
    if _client is None:
        return (
            "**AI Insights Unavailable** - Gemini API key not configured.\n\n"
            "Add `GEMINI_API_KEY` to your `.env` file to enable AI insights."
        )

    if not rows:
        return "No data available to generate insights."

    total = len(rows)
    fake_count = sum(1 for row in rows if "FAKE" in row[2])
    real_count = total - fake_count
    fake_pct = round(fake_count / total * 100, 1) if total > 0 else 0

    samples = []
    for row in rows[:10]:
        desc = row[1][:150].replace("\n", " ") if row[1] else ""
        result = row[2]
        samples.append(f"- [{result}] {desc}...")

    samples_text = "\n".join(samples)

    prompt = f"""
You are JobShield AI's analytics engine. Based on the following prediction history,
generate actionable insights for a dashboard.

STATS:
- Total predictions: {total}
- Fake jobs detected: {fake_count} ({fake_pct}%)
- Real jobs: {real_count}

RECENT SAMPLES:
{samples_text}

Provide a concise insight report in Markdown with:

## Trend Analysis
What patterns do you notice?

## Common Scam Patterns
What recurring fraud tactics appear in the fake postings?

## Advice for Job Seekers
3-5 practical tips based on these findings.

## Risk Alert Level
Overall threat level based on current data: CRITICAL / HIGH / MODERATE / LOW

Keep the report concise and practical. Use bullet points.
"""

    try:
        return _generate_content(prompt)
    except Exception as e:
        return f"**Insights Generation Error**: {str(e)}"
