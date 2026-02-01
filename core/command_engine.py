import re
import joblib

from skills import file_control, application_control

# ---------------- GEMINI AGENT (PRIMARY) ----------------
from core.agent.agent import decide_action
from core.agent.memory import memory


# ---------------- ML INTENT MODEL (FALLBACK) ----------------
model = joblib.load("core/intent_model.pkl")


def normalize_name(text: str) -> str:
    """Extracts a filename or folder name from the command."""
    text = text.lower()

    replacements = {
        " dot ": ".",
        " underscore ": "_",
        " dash ": "-",
        " space ": ""
    }
    for k, v in replacements.items():
        text = text.replace(k, v)

    text = re.sub(
        r"\b(named|called|as|file|folder|directory|a|the|please|can you|could you|"
        r"create|delete|make|remove)\b",
        "",
        text
    )

    text = re.sub(r"\s+", " ", text).strip()
    parts = text.split()
    return parts[-1] if parts else ""


def process_command(text: str) -> str:
    """
    Processes a command using:
    1) Gemini agent (primary)
    2) ML intent classifier (fallback)
    """

    # ================= GEMINI PATH =================
    try:
        decision = decide_action(text)

        if decision and decision.get("confidence", 0) >= 0.4:
            action = decision.get("action")
            app = decision.get("app") or memory.get_last_app()
            query = decision.get("query")

            if action == "open_app":
                memory.update(app=app, action=action)
                return application_control.open_app(app)

            elif action == "close_app":
                return application_control.close_app(app)

            elif action == "switch_app":
                memory.update(app=app, action=action)
                return application_control.switch_to_app(app)

            elif action == "list_installed":
                return application_control.list_installed_apps()

            elif action == "list_running":
                return application_control.list_running_apps()

            elif action == "search":
                return application_control.search_web(query)

    except Exception as e:
        print("Gemini failed, falling back to ML:", e)

    # ================= ML FALLBACK PATH =================
    scores = model.decision_function([text])
    confidence = scores.max()

    if confidence < 0.4:
        return "I'm not quite sure what you mean. Could you please rephrase that?"

    intent = model.predict([text])[0]

    # -------- FILE OPERATIONS --------
    if intent in {"CREATE_FILE", "DELETE_FILE", "CREATE_FOLDER", "DELETE_FOLDER"}:
        name = normalize_name(text)
        if not name:
            return "Please specify a name for the file or folder."

        if intent == "CREATE_FILE":
            return file_control.create_file(name)

        elif intent == "DELETE_FILE":
            return file_control.delete_file(name)

        elif intent == "CREATE_FOLDER":
            return file_control.create_folder(name)

        elif intent == "DELETE_FOLDER":
            return file_control.delete_folder(name)

    elif intent == "LIST_FILES":
        return file_control.list_items()

    # -------- APPLICATION CONTROL --------
    elif intent == "OPEN_APPLICATION":
        return application_control.open_app(text)

    elif intent == "CLOSE_APPLICATION":
        return application_control.close_app(text)

    elif intent == "SWITCH_APPLICATION":
        return application_control.switch_to_app(text)

    elif intent == "LIST_INSTALLED_APPLICATIONS":
        return application_control.list_installed_apps()

    elif intent == "LIST_RUNNING_APPLICATIONS":
        return application_control.list_running_apps()

    # -------- FINAL FALLBACK --------
    return "I'm sorry, I don't know how to do that yet."
