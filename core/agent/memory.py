import json
import os

class Memory:
    def __init__(self, memory_file='core/agent/memory.json'):
        self.memory_file = memory_file
        self.context = self.load_memory()

    def load_memory(self):
        if os.path.exists(self.memory_file):
            with open(self.memory_file, 'r') as f:
                return json.load(f)
        return {"last_app": None, "conversation_history": []}

    def save_memory(self):
        os.makedirs(os.path.dirname(self.memory_file), exist_ok=True)
        with open(self.memory_file, 'w') as f:
            json.dump(self.context, f, indent=4)

    def update_last_app(self, app_name):
        self.context["last_app"] = app_name
        self.save_memory()

    def get_last_app(self):
        return self.context.get("last_app")

    def add_to_history(self, user_input, agent_response):
        self.context["conversation_history"].append({
            "user": user_input,
            "agent": agent_response
        })
        # Keep only last 10 interactions
        if len(self.context["conversation_history"]) > 10:
            self.context["conversation_history"] = self.context["conversation_history"][-10:]
        self.save_memory()

    def get_recent_history(self, n=5):
        return self.context["conversation_history"][-n:]

# Instantiate the memory object
memory = Memory()
