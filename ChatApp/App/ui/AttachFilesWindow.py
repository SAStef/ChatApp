from PyQt6.QtWidgets import *

class AttachFilesWindow(QMainWindow):
    def __init__(self, p):
        super().__init__()
        self.parent = p
        
        