import os
import json
import re

from dotenv import load_dotenv
from google import genai

from core.agent.memory import memory

# ---------------- LOAD ENV ----------------
load_dotenv()

# ---------------- GEMINI CLIENT ----------------
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise RuntimeError("GEMINI_API_KEY environment variable not set")

client = genai.Client(api_key=api_key)

# ---------------- AGENT (DECISION ONLY) ----------------
def decide_action(user_text: str) -> dict:
    last_app = memory.get_last_app()

    prompt = f"""
You are a system automation AI agent.
Understand natural language in English or Indian languages like Telugu and Hindi.

Context:
- Last application used: {last_app or "None"}

User input:
"{user_text}"

Respond ONLY with valid JSON.

Valid actions:
open_app, close_app, list_installed, list_running, switch_app, search, none

JSON format:
{{
  "action": "open_app | close_app | list_installed | list_running | switch_app | search | none",
  "app": "string or null",
  "query": "string or null",
  "confidence": 0.0
}}
"""

    response = client.models.generate_content(
        model="gemini-1.5-flash",
        contents=prompt
    )

    raw_text = response.text.strip()

    match = re.search(r"\{.*\}", raw_text, re.S)
    if not match:
        return {"action": "none", "confidence": 0.0}

    try:
        return json.loads(match.group())
    except json.JSONDecodeError:
        return {"action": "none", "confidence": 0.0}
