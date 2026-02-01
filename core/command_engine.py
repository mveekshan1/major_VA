import re
import joblib
from skills import file_control, application_control

model = joblib.load("core/intent_model.pkl")

def normalize_name(text: str) -> str:
    text = text.lower()

    replacements = {
        " dot ": ".",
        " underscore ": "_",
        " dash ": "-",
        " space ": "",
        " slash ": "/"
    }

    for k, v in replacements.items():
        text = text.replace(k, v)

    
    text = re.sub(
        r"\b(named|called|as|file|folder|directory|a|the|please|can you|could you)",
        "",
        text
    )

    text = re.sub(r"\s+", " ", text).strip()

    parts = text.split()
    if not parts:
        return ""

    return parts[-1]

def extract_app_name(text: str) -> str:
    """
    Extracts the application name from the command text.
    This is a simple implementation that looks for keywords.
    """
    text = text.lower()
    keywords = ["open", "close", "switch to", "run", "launch", "terminate", "kill", "focus on", "start", "exit", "to"]
    
    # Remove keywords to isolate the app name
    for keyword in keywords:
        text = text.replace(keyword, "")
    
    # A more advanced version could use NLP to find the object of the verb.
    # For now, we'll take the remaining text, assuming it's the app name.
    
    # Remove common filler words
    text = re.sub(r"\b(application|program|app|the|a|an|please|can you|could you)\b", "", text)
    
    return text.strip()


def process_command(text: str) -> str:
  
    scores = model.decision_function([text])
    confidence = abs(scores).max()

    if confidence < 0.3:
        return "I am not sure what you mean. Please rephrase."

    intent = model.predict([text])[0]
    
    if intent in {"CREATE_FILE", "DELETE_FILE", "CREATE_FOLDER", "DELETE_FOLDER"}:
        name = normalize_name(text)
        if not name:
            return "Please specify a file or folder name."
        
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

    elif intent in {"OPEN_APPLICATION", "CLOSE_APPLICATION", "SWITCH_APPLICATION"}:
        app_name = extract_app_name(text)
        if not app_name:
            return f"Please specify an application name."
        
        if intent == "OPEN_APPLICATION":
            return application_control.open_application(app_name)
        elif intent == "CLOSE_APPLICATION":
            return application_control.close_application(app_name)
        elif intent == "SWITCH_APPLICATION":
            return application_control.switch_application(app_name)

    elif intent == "LIST_INSTALLED_APPLICATIONS":
        return application_control.list_installed_applications()
    
    elif intent == "LIST_RUNNING_APPLICATIONS":
        return application_control.list_running_applications()

    else:
        return "Intent not recognized."
