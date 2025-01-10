from PyQt6.QtWidgets import *

class RecieveHypertextMessage(QFrame):
    def __init__(self, text):
        super().__init__()

        self.recievedmessage = text

        print(f'Modtaget besked via TCP {text}')