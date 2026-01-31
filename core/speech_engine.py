import pyttsx3

_engine = pyttsx3.init()
_engine.setProperty("rate", 175)
_engine.setProperty("volume", 1.0)
voices = _engine.getProperty("voices")
if isinstance(voices, list) and len(voices) > 1:
    _engine.setProperty("voice", voices[1].id)

def speak(text: str):
    if not text:
        return
    _engine.say(text)
    _engine.runAndWait()