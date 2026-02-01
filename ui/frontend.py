import sys
import os

from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QTextEdit, QLineEdit, QLabel, QFileDialog
)
from PySide6.QtCore import Qt, QThread, Signal

from core.command_engine import process_command
from core.voice_engine import listen_once
from core.speech_engine import speak
from skills.file_control import set_base_dir


# ---------------- WORKER THREADS ---------------- #

class CommandWorker(QThread):
    finished = Signal(str)

    def __init__(self, command):
        super().__init__()
        self.command = command

    def run(self):
        try:
            result = process_command(self.command)
        except Exception as e:
            result = f"Error: {e}"
        self.finished.emit(result)


class VoiceWorker(QThread):
    finished = Signal(str)

    def run(self):
        try:
            text = listen_once()
        except Exception:
            text = ""
        self.finished.emit(text or "")


# ---------------- MAIN UI ---------------- #

class OrbitOS(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("OrbitOS – Conversational AI Agent")
        self.resize(900, 600)
        self.setup_ui()

    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(10)

        # Title
        title = QLabel("🤖 OrbitOS")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 26px; font-weight: bold;")
        main_layout.addWidget(title)

        # Status
        self.status_label = QLabel("Status: Idle")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("color: #888;")
        main_layout.addWidget(self.status_label)

        # Input Row
        input_layout = QHBoxLayout()

        self.command_input = QLineEdit()
        self.command_input.setPlaceholderText("Type a command or use voice...")
        self.command_input.returnPressed.connect(self.run_command)

        self.run_btn = QPushButton("Run")
        self.run_btn.clicked.connect(self.run_command)

        self.voice_btn = QPushButton("🎤 Voice")
        self.voice_btn.clicked.connect(self.start_voice)

        input_layout.addWidget(self.command_input, stretch=6)
        input_layout.addWidget(self.run_btn, stretch=1)
        input_layout.addWidget(self.voice_btn, stretch=1)

        main_layout.addLayout(input_layout)

        # Working Directory
        dir_layout = QHBoxLayout()

        self.dir_label = QLabel(f"Working Directory: {os.getcwd()}")
        self.dir_label.setWordWrap(True)

        browse_btn = QPushButton("Browse")
        browse_btn.clicked.connect(self.browse_folder)

        dir_layout.addWidget(self.dir_label, stretch=6)
        dir_layout.addWidget(browse_btn, stretch=1)

        main_layout.addLayout(dir_layout)

        # Console (Chat)
        self.console = QTextEdit()
        self.console.setReadOnly(True)
        self.console.setStyleSheet(
            "font-family: Consolas; font-size: 13px; background:#111; color:#ddd;"
        )

        main_layout.addWidget(self.console, stretch=1)

    # ---------------- TEXT COMMAND ---------------- #

    def run_command(self):
        cmd = self.command_input.text().strip()
        if not cmd:
            return

        self.command_input.clear()
        self.append_user(cmd)

        self.set_busy("Thinking...")
        self.disable_inputs()

        self.worker = CommandWorker(cmd)
        self.worker.finished.connect(self.on_result)
        self.worker.start()

    # ---------------- VOICE COMMAND ---------------- #

    def start_voice(self):
        self.set_busy("Listening...")
        self.disable_inputs()

        self.voice_worker = VoiceWorker()
        self.voice_worker.finished.connect(self.on_voice_result)
        self.voice_worker.start()

    def on_voice_result(self, text):
        if not text:
            self.append_agent("Sorry, I could not understand.")
            speak("Sorry, I could not understand.")
            self.set_idle()
            self.enable_inputs()
            return

        self.append_user(text)

        self.set_busy("Thinking...")
        self.worker = CommandWorker(text)
        self.worker.finished.connect(self.on_result)
        self.worker.start()

    # ---------------- RESULT HANDLER ---------------- #

    def on_result(self, result):
        self.append_agent(result)
        speak(result)
        self.set_idle()
        self.enable_inputs()

    # ---------------- UI HELPERS ---------------- #

    def append_user(self, text):
        self.console.append(
            f"<p style='color:#00aaff;'><b>You:</b> {text}</p>"
        )

    def append_agent(self, text):
        self.console.append(
            f"<p style='color:#00ff88;'><b>Agent:</b> {text}</p><br>"
        )

    def set_busy(self, state):
        self.status_label.setText(f"Status: {state}")

    def set_idle(self):
        self.status_label.setText("Status: Idle")

    def disable_inputs(self):
        self.run_btn.setEnabled(False)
        self.voice_btn.setEnabled(False)

    def enable_inputs(self):
        self.run_btn.setEnabled(True)
        self.voice_btn.setEnabled(True)

    # ---------------- DIRECTORY ---------------- #

    def browse_folder(self):
        path = QFileDialog.getExistingDirectory(self, "Select Working Directory")
        if path:
            set_base_dir(path)
            self.dir_label.setText(f"Working Directory: {path}")


def launch_ui():
    app = QApplication(sys.argv)
    window = OrbitOS()
    window.show()
    sys.exit(app.exec())
