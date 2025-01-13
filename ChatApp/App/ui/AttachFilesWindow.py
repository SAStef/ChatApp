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

        try:
            if file_path:
                file_name = path.basename(file_path)
                file_size = path.getsize(file_path)
                # print(file_size, type(file_size), file_name)

                # "FILE" + filnavnslængde + filstørrelse (formateret til hhv. 4 og 8 tegns længde)
                header = f'FILE{len(file_name):04}{file_size:08}'.encode('UTF-8')
                
                # Sender headeren
                self.parent.TCP_klient.send(header)
                
                # Sender filnavnet
                self.parent.TCP_klient.send(file_name.encode('UTF-8'))

                # Sender filen
                more = True
                buffersize = 2048
                file = open(file_path, 'rb')
                while more:
                    buffer = file.read(buffersize)
                    if len(buffer) < buffersize:
                        more = False
                    self.parent.TCP_klient.send(buffer)
        
        except Exception as e:
            print(f"Fejl ved afsendelse af fil {e}")


        # if file_path:
        #     ### --- PLACEHOLDER FOR AT SENDE FIL OVER CHATTEN --- ###

        #     buffersize = 2048
        #     file_content = open(file_path, 'rb')

        #     more = True
        #     while more:
        #         buffer = file_content.read(buffersize)
        #         if len(buffer) < buffersize:
        #             more = False
        #         self.parent.TCP_klient.send(buffer)
            
        #     print(f"Du har valgt {file_path}")
                



