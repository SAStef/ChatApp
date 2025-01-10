from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt

class SendHypertextMessage(QFrame):
    def __init__(self, text, parent=None):
        super().__init__(parent)
        self.lines = [text[i:i + 100] for i in range(0, len(text), 100)]

        box_height = len(self.lines) * 30

        self.layout = QVBoxLayout(self)

        for line in self.lines:
                message_label = QLabel(line)
                self.layout.addWidget(message_label)

        self.setStyleSheet("""
                QFrame {
                    background-color: #e0e0e0;
                    border-radius: 4px;
                    padding: 2px;
                    margin: 0px;
                }
                QLabel {
                    color: black;
                    font-size: 12px;
                    padding: 0px;
                    margin: 0px;
                }
            """)

        self.setFixedSize(int(len(self.lines[0]) * 6.4) + 35, box_height + 25)

        self.layout.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.setLayout(self.layout)