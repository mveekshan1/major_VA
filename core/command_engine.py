import re
import joblib
from skills import file_control, application_control

model = joblib.load("core/intent_model.pkl")

def normalize_name(text: str) -> str:
    """Extracts a filename or folder name from the command."""
    text = text.lower()
    # Replace spoken punctuation with characters
    replacements = {" dot ": ".", " underscore ": "_", " dash ": "-", " space ": ""}
    for k, v in replacements.items():
        text = text.replace(k, v)
    
    # Remove action-related keywords to isolate the name
    text = re.sub(
        r"\b(named|called|as|file|folder|directory|a|the|please|can you|could you|create|delete|make|remove)\b",
        "",
        text
    )
    # Clean up whitespace and return the last significant word, assumed to be the name
    text = re.sub(r"\s+", " ", text).strip()
    parts = text.split()
    return parts[-1] if parts else ""

def process_command(text: str) -> str:
    """
    Processes a command by predicting its intent and routing to the correct skill.
    """
    # Use the model to predict the intent with a confidence score
    scores = model.decision_function([text])
    confidence = scores.max() 

    # If confidence is too low, ask for clarification
    if confidence < 0.4: # Increased threshold for better reliability
        return "I'm not quite sure what you mean. Could you please rephrase that?"

    intent = model.predict([text])[0]
    
    # --- File Operations ---
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

    # --- Application Control ---
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

    # --- Fallback ---
    else:
        return "I'm sorry, I don't know how to do that yet."
