from groq import Groq
import os
from dotenv import load_dotenv

# ✅ Load environment variables
load_dotenv()

# ✅ Secure API key
client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def generate_report(goal: str):

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "system",
                "content": "You are a construction project manager. Generate professional reports."
            },
            {
                "role": "user",
                "content": f"""
Generate a structured construction report.

Project: {goal}

Include:
- Project Summary
- Key Highlights (bullet points)
- Safety Measures
- Conclusion
"""
            }
        ]
    )

    return response.choices[0].message.content


def generate_metrics(goal: str):

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "system",
                "content": "Generate realistic project metrics."
            },
            {
                "role": "user",
                "content": f"""
Give estimated project metrics for: {goal}

Format EXACTLY like:
Duration: ___
Budget: ___
Team: ___
"""
            }
        ]
    )

    return response.choices[0].message.content