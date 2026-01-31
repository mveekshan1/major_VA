import sys
import os
from core.speech_engine import speak

from PySide6.QtWidgets import ( # type: ignore
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QTextEdit, QLineEdit, QLabel,
    QFileDialog
)
from PySide6.QtCore import Qt # type: ignore

from core.command_engine import process_command
from core.voice_engine import listen_once
from skills.file_control import set_base_dir


class OrbitOS(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("OrbitOS – Intelligent System Agent")
        self.resize(900, 600)
        self.setup_ui()

    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(12)

    
        title = QLabel("OrbitOS")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 24px; font-weight: bold;")
        main_layout.addWidget(title)


        input_layout = QHBoxLayout()

        self.command_input = QLineEdit()
        self.command_input.setPlaceholderText("Enter a command or use voice…")
        self.command_input.returnPressed.connect(self.run_command)

        run_btn = QPushButton("Run")
        run_btn.clicked.connect(self.run_command)

        voice_btn = QPushButton("Voice")
        voice_btn.clicked.connect(self.start_voice)

        input_layout.addWidget(self.command_input, stretch=6)
        input_layout.addWidget(run_btn, stretch=1)
        input_layout.addWidget(voice_btn, stretch=1)

        main_layout.addLayout(input_layout)

    
        dir_layout = QHBoxLayout()

        self.dir_label = QLabel(f"Working Directory: {os.getcwd()}")
        self.dir_label.setWordWrap(True)

        browse_btn = QPushButton("Browse")
        browse_btn.clicked.connect(self.browse_folder)

        dir_layout.addWidget(self.dir_label, stretch=6)
        dir_layout.addWidget(browse_btn, stretch=1)

        main_layout.addLayout(dir_layout)

   
        self.console = QTextEdit()
        self.console.setReadOnly(True)
        self.console.setStyleSheet(
            "font-family: Consolas; font-size: 12px;"
        )

        main_layout.addWidget(self.console, stretch=1)

    def run_command(self):
        cmd = self.command_input.text().strip()
        if not cmd:
            return

        self.console.append(f">> {cmd}")
        result = process_command(cmd)
        self.console.append(result + "\n")
        speak(result)

        self.command_input.clear()

    def start_voice(self):
        self.console.append("[Voice] Listening...")
        text = listen_once()

        if not text:
            self.console.append("[Voice] Could not understand.\n")
            speak("Sorry, I could not understand that.")
            return

        self.console.append(f"[Voice] {text}")
        result = process_command(text)

        self.console.append(result + "\n")
        speak(result)  


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
