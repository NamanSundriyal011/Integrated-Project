from groq import Groq
import re
import os
from dotenv import load_dotenv

# ✅ Load environment variables
load_dotenv()

# ✅ Secure API key
client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def generate_plan(goal: str):

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "system",
                "content": "You are a construction planning expert. Create structured phases and steps."
            },
            {
                "role": "user",
                "content": f"""
Break this construction project into clear structured phases.

Format:
Phase 1: Name
- Step 1
- Step 2

Phase 2: Name
- Step 1
- Step 2

Project:
{goal}
"""
            }
        ]
    )

    text = response.choices[0].message.content

    # ---------- CLEAN OUTPUT ----------
    lines = []
    for line in text.split("\n"):
        line = line.strip()

        if not line:
            continue

        # remove markdown symbols
        line = re.sub(r"\*\*", "", line)
        line = re.sub(r"\*", "", line)

        lines.append(line)

    return "\n".join(lines)