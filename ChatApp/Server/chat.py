from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog, QVBoxLayout, QWidget

class ChatApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ChatApp med Fil-upload")
        self.setGeometry(100, 100, 400, 200)
        
        # Opsæt layout og knap
        layout = QVBoxLayout()
        self.upload_button = QPushButton("Upload fil", self)
        self.upload_button.clicked.connect(self.open_file_dialog)
        layout.addWidget(self.upload_button)

        # Central widget
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def open_file_dialog(self):
        # Åbn fil-dialog og få den valgte fils sti
        options = QFileDialog.Option.ReadOnly
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Vælg en fil til upload",
            "",
            "Alle filer (*.*);;PDF-filer (*.pdf);;Billedfiler (*.png *.jpg *.jpeg)",
            options=options
        )
        
        if file_path:
            print(f"Valgt fil: {file_path}")
            # Her kan du tilføje koden til at sende filen over chatten.

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = ChatApp()
    window.show()
    sys.exit(app.exec())