import os
import json
import re
import google.generativeai as genai

from core.agent.memory import memory


# ---------------- GEMINI SETUP ----------------

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise RuntimeError("GEMINI_API_KEY environment variable not set")

genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash")


# ---------------- AGENT (DECISION ONLY) ----------------

def decide_action(user_text: str) -> dict:
    """
    Uses Gemini to decide the action to take.
    Returns a structured dict, does NOT execute anything.
    """

    last_app = memory.get_last_app()

    prompt = f"""
You are a system automation AI agent.
Understand natural language in English or Indian languages like Telugu and Hindi.

Context:
- Last application used: {last_app or "None"}

User input:
"{user_text}"

Decide the action and respond ONLY with valid JSON.

Valid actions:
open_app, close_app, list_installed, list_running, switch_app, search, none

JSON format:
{{
  "action": "open_app | close_app | list_installed | list_running | switch_app | search | none",
  "app": "string or null",
  "query": "string or null",
  "confidence": 0.0
}}

Rules:
- If app is not mentioned, infer it from context if possible.
- Confidence must be between 0.0 and 1.0.
- Do NOT include any explanation text.
"""

    response = model.generate_content(prompt)
    raw_text = response.text.strip()

    # -------- SAFE JSON EXTRACTION --------
    match = re.search(r"\{.*\}", raw_text, re.S)
    if not match:
        return {"action": "none", "confidence": 0.0}

    try:
        decision = json.loads(match.group())
    except json.JSONDecodeError:
        return {"action": "none", "confidence": 0.0}

    return decision
