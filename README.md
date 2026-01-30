An NLP-Based Intelligent Agent for System Automation

This project implements an NLP-driven intelligent voice-based agent that enables users to automate system-level tasks using natural language through voice or text commands. The system integrates speech recognition, Natural Language Processing, and machine learning–based intent classification to interpret user commands and perform actions such as file manipulation and basic system automation.

The project is designed with a modular architecture, making it easy to understand, extend, and experiment with intelligent agent behavior.

Features

Voice and text-based command input

NLP-based intent recognition (machine learning model)

File system automation (create, delete, list files/folders)

Confidence-based intent handling

Context-aware working directory selection

Modular and extensible design

Offline-capable core functionality

Project Structure
ai-voice-agent/
│
├── core/               # NLP, intent model, command engine
├── skills/             # System automation modules (file control, etc.)
├── ui/                 # Tkinter-based frontend
├── data/               # Training dataset for intent classification
├── requirements.txt    # Python dependencies
├── main.py             # Application entry point
└── README.md

Prerequisites

Python 3.9 or higher

Git (optional, for cloning)

Microphone (for voice input)

Getting the Project
Option 1: Clone Using Git
git clone https://github.com/<your-username>/<your-repo-name>.git
cd <your-repo-name>

Option 2: Download ZIP

Click Code → Download ZIP on the GitHub page

Extract the ZIP file

Open a terminal inside the extracted folder

Create and Activate Virtual Environment
Windows
python -m venv venv
venv\Scripts\activate

Linux / macOS
python3 -m venv venv
source venv/bin/activate


You should see (venv) in your terminal after activation.

Install Dependencies
pip install -r requirements.txt


Note:

tkinter is included with Python by default

If pyaudio fails to install on Windows, install a precompiled wheel or use Vosk/Whisper instead of Google Speech Recognition

Train the NLP Intent Model (First Time Only)

Before running the application, train the intent classifier:

python core/train_intent_model.py


This will generate the trained model file used by the system.

Run the Application
python main.py


The Tkinter GUI will launch, allowing you to:

Type commands directly

Use the Voice button for spoken commands

Browse and select a working directory

Example Commands
create a file named test dot txt
create folder named project
list files
delete file named test dot txt

Notes

All core processing is done locally

No cloud services are required for basic operation

The system is designed as a task-oriented intelligent agent

The architecture supports future extensions such as:

Application control

Context memory

Multi-step task execution

Future Enhancements

Application launch and control

Context-aware dialogue handling

Multi-step agent tasks

Learning from command history

Advanced voice models (Whisper/Vosk fully offline)

License

This project is intended for academic and educational purposes as part of a final-year major project.
