# An NLP-Based Intelligent Agent for System Automation

This repository contains the implementation of an NLP-driven intelligent voice-based agent that enables users to automate system-level tasks using natural language through voice or text commands.  
The system integrates Speech Recognition, Natural Language Processing (NLP), and Machine Learning–based techniques to interpret user commands and execute system actions.

The project is designed with a modular and extensible architecture, making it suitable for academic use, experimentation, and future enhancements.

---

## Features

### Core Features
- Voice and text-based command input  
- NLP-based intent recognition using a trained ML model  
- File system automation:
  - Create files and folders  
  - Delete files and folders  
  - List files and directories  
- Confidence-based intent handling  
- Context-aware working directory selection  
- Modular architecture (UI, NLP, control, skills)  
- Offline-capable core functionality (file automation and intent classification)

---

## New: Conversational AI Agent (Advanced Features)

The project has been extended with a conversational, context-aware AI agent powered by the Gemini API. This is an addition on top of the existing NLP-based intent classification system, enhancing the system's capabilities without replacing the core functionality.

New capabilities include:
- Natural language understanding (not limited to fixed commands)
- Follow-up commands using context memory
- Application control via voice/text:
  • Open applications
  • Close applications
  • List installed applications
  • List running applications
  • Switch between applications
- Browser search using voice/text
- Multilingual input support (English and Indian languages like Telugu/Hindi)
- Context-aware execution and clarification on low confidence

### Updated High-Level Flow
Voice/Text → Gemini Agent → Context Memory → Skills → System Actions

---

## High-Level System Flow

Voice / Text Input
↓
Speech-to-Text
↓
Gemini-Based Conversational Agent
↓
Context Memory + Action Decision
↓
System Skills (Applications / Browser / Files)


---

## Prerequisites

- Python 3.9 or higher  
- Git (optional, for cloning)  
- A working microphone (for voice commands)  
- Internet connection (required for Gemini-powered features)

---

## Getting the Project

### Option 1: Clone Using Git

```bash
git clone https://github.com/akhil1225/major_VA.git
cd major_VA

## Create a Virtual Environment

Create a virtual environment inside the project folder:

'''bash
python3 -m venv venv
'''

## Activate the virtual environment:

'''bash
source venv/bin/activate
'''

## Install Required Dependencies:
# Install all required packages using the requirements.txt file:

'''bash
pip install -r requirements.txt
'''
## Configure Gemini API Key
Create a .env file in the project root and add:
'''bash
GEMINI_API_KEY=your_api_key_here
'''

## Train the NLP Model (Optional)

## The NLP intent classification model must be retrained every time the dataset is changed or the model architecture is modified.

'''bash
python core/train_intent_model.py
'''
## Run the Application
'''bash
python main.py
'''
