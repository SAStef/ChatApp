from PyQt6.QtWidgets import *
from os import path
import time

class AttachFilesWindow(QMainWindow):
    def __init__(self, p):
        super().__init__()
        self.parent = p
        
        options = QFileDialog.Option.ReadOnly
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Vælg en fil du vil sende",
            "",
            "Alle filer (*.*);;PDF-filer (*.pdf);; Billedfiler (*.png *jpg *.jpeg)",
            options=options

        )

        if file_path:
            file_name = path.basename(file_path)
            file_length = path.getsize(file_path)

            file_length = path.getsize(file_path)
            # print(f'File length in bytes: {file_length}')

            # Definerer en header og sender den
            file_header = f'FILE: {file_name}\nLENGTH: {file_length}\n'
            self.parent.TCP_klient.send(file_header.encode('utf-8'))
            
            try:
                with open(file_path, 'rb') as f:           # Åbner filen som binary
                    while buffer := f.read(2048):             # Definerer en buffer i et while statement, og sender den.
                        self.parent.TCP_klient.send(buffer)
                print(f'Filen "{file_name}" er blevet sendt til serveren, og skulle gerne broadcastes')
            
            except Exception as e:
                print(f'Fejl i AttachFilesWindow hos klienten: {e}')

