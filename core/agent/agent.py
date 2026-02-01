import os
import json
import google.generativeai as genai
from core.agent.memory import Memory

class Agent:
    def __init__(self):
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            raise ValueError("GEMINI_API_KEY environment variable not set")
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        self.memory = Memory()

    def process_command(self, user_input: str) -> str:
        # Get context from memory
        last_app = self.memory.get_last_app()
        history = self.memory.get_recent_history()

        # Build prompt for LLM
        prompt = f"""
You are a conversational AI agent that controls system applications. Based on the user's input, decide which action to take.

Available actions:
- open_app: Open an application
- close_app: Close an application
- list_apps: List installed applications
- list_running: List running applications
- switch_app: Switch to a running application
- search: Search in browser
- none: No action needed

Context:
- Last app used: {last_app or 'None'}
- Recent conversation: {json.dumps(history, indent=2)}

User input: "{user_input}"

Respond ONLY with valid JSON in this format:
{{
  "action": "open_app | close_app | list_apps | list_running | switch_app | search | none",
  "app": "string or null",
  "query": "string or null",
  "confidence": 0.0
}}

Rules:
- If app is not specified, use last_app if available.
- Confidence is a float between 0.0 and 1.0 based on how sure you are.
- If confidence < 0.5, set action to "none".
"""

        try:
            response = self.model.generate_content(prompt)
            result = json.loads(response.text.strip())
            action = result.get('action')
            app = result.get('app')
            query = result.get('query')
            confidence = result.get('confidence', 0.0)

            if confidence < 0.5:
                return "I'm not confident about that action. Can you clarify?"

            # Execute action
            if action == 'open_app':
                from skills.application_control import open_app
                if not app and last_app:
                    app = last_app
                result_str = open_app(f"open {app}")
                self.memory.update_last_app(app)
            elif action == 'close_app':
                from skills.application_control import close_app
                if not app and last_app:
                    app = last_app
                result_str = close_app(f"close {app}")
            elif action == 'list_apps':
                from skills.application_control import list_installed_apps
                result_str = list_installed_apps()
            elif action == 'list_running':
                from skills.application_control import list_running_apps
                result_str = list_running_apps()
            elif action == 'switch_app':
                from skills.application_control import switch_to_app
                if not app and last_app:
                    app = last_app
                result_str = switch_to_app(f"switch to {app}")
                self.memory.update_last_app(app)
            elif action == 'search':
                from skills.browser_control import search_in_browser
                result_str = search_in_browser(query or user_input)
            else:
                result_str = "Action not recognized."

            # Update memory
            self.memory.add_to_history(user_input, result_str)
            return result_str

        except Exception as e:
            return f"Error processing command: {e}"
