import os
from groq import Groq
from dotenv import load_dotenv
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / '.env')

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def classify_ticket(title, description):
    prompt = f"""
You are an IT support expert. Based on the ticket below, do two things:
1. Classify the priority as exactly one of: P1, P2, or P3
   - P1 = Critical: system down, data loss, security breach, affects all users
   - P2 = High: major feature broken, affects many users, no workaround
   - P3 = Medium: minor issue, workaround available, affects one user

2. Suggest a short first-response solution in 2-3 sentences.

Ticket Title: {title}
Ticket Description: {description}

Reply in exactly this format:
PRIORITY: P1
SUGGESTION: Your suggestion here.
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
    )

    text = response.choices[0].message.content.strip()

    priority = "P3"
    suggestion = "Please review this ticket and respond to the user."

    for line in text.splitlines():
        if line.startswith("PRIORITY:"):
            value = line.replace("PRIORITY:", "").strip()
            if value in ["P1", "P2", "P3"]:
                priority = value
        if line.startswith("SUGGESTION:"):
            suggestion = line.replace("SUGGESTION:", "").strip()

    return priority, suggestion