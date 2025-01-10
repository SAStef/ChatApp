from PyQt6.QtWidgets import *
from PyQt6.QtCore import QSize, Qt, pyqtSignal, QObject, QTimer, QThread
from threading import Thread
import random
import time
import socket as s
from PyQt6.QtGui import QPixmap

# Importerer biblioteker til at lave scener
from PyQt6.QtGui import QPen, QBrush

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

class RecieveHyperTextMessage(QFrame):
    def __init__(self, text):
        super().__init__()

        self.recievedmessage = text

        print(f'Modtaget besked via TCP {text}')

class RecieverThread(QThread):
    message_recieved = pyqtSignal(str)
    
    def __init__(self, client_socket):
        super().__init__()
        self.running = True
        self.client_socket = client_socket

    def run(self, ):
        try:
            while self.running:
                self.server_data = self.client_socket.recv(2048)
                if not self.server_data:
                    break

                self.encoded_message = self.server_data.decode('UTF-8')
                self.message_recieved.emit(self.encoded_message)
                print(self.server_data)

        except Exception as e:
            print(f'Fejl i recievertråden: {e}')


class MainWindow(QMainWindow):
    def __init__(self, ):
        super().__init__()
        
        # Tilsutter til chat-serveren
        self.TCP_server_ip = "127.0.0.1"
        self.TCP_server_port = 1337
        self.TCP_klient = s.socket(s.AF_INET, s.SOCK_STREAM)
        self.TCP_klient.connect((self.TCP_server_ip, self.TCP_server_port))

        # Starter en tråd til recievertråden
        self.reciever = RecieverThread(self.TCP_klient)
        
        # Sætter den centrale widget
        central = QWidget(self)
        self.setCentralWidget(central)

        self.setWindowTitle("Chatprogram")          # Titlen på vinduet
        self.resize(1920, 1080)                     # Standard størrelsen på vinduet der åbner
        self.setMinimumSize(800, 400)               # Mininum størrelsen på vinduet

        # Definerer widgets til south layout
        self.chatfld = QLineEdit()
        self.sendbutton = QPushButton("Send besked")
        self.attachbutton = QPushButton("Vedhæft fil(er)")

        left_spacer = QSpacerItem(200, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        right_spacer = QSpacerItem(200, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        panel_south = QHBoxLayout()
        panel_south.addSpacerItem(left_spacer)
        panel_south.addWidget(self.attachbutton)
        panel_south.addWidget(self.chatfld)
        panel_south.addWidget(self.sendbutton)
        panel_south.addSpacerItem(right_spacer)

        # Definerer widgets til mid layoutet
        self.dialogue = QScrollArea()
        self.dialogue.setWidgetResizable(True)
        self.dialogue_content = QWidget()
        self.dialogue_layout = QVBoxLayout(self.dialogue_content)

        self.dialogue_layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignRight)

        self.dialogue.setWidget(self.dialogue_content)

        self.group_icon= QLabel()
        self.group_icon.setFixedWidth(100)
        self.group_icon.setFixedHeight(50)
        self.group_icon.setStyleSheet("background-color: gray;")
        self.group_icon.setPixmap(QPixmap('coconut.jpeg'))
        self.group_icon.setScaledContents(True) #Hvis det er nødvendigt (Edit: Det var det)

        self.right_group_icon= QLabel()
        self.right_group_icon.setFixedWidth(100)
        self.right_group_icon.setFixedHeight(50)
        self.right_group_icon.setStyleSheet("background-color: gray;")

        self.act_friends_panel= QLineEdit()
        self.act_friends_panel.setFixedWidth(600)
        self.act_friends_panel.setFixedHeight(50)
        self.act_friends_panel.setStyleSheet('backgro)und-color: gray;')

        upper_layout= QHBoxLayout()
        #upper_layout.addSpacerItem(upper_left_spacer)
        upper_layout.addWidget(self.group_icon)
        upper_layout.addWidget(self.act_friends_panel)
        upper_layout.addWidget(self.right_group_icon)
        #upper_layout.addSpacerItem(right_spacer)

        self.friends_panel = QTextBrowser()
        self.friends_panel.setMaximumWidth(200)
        self.friends_panel.setStyleSheet("background-color: lightgray;")

        self.files_panel = QTextBrowser()
        self.files_panel.setMaximumWidth(200)
        self.files_panel.setStyleSheet("background-color: lightgray;")

        panel_mid = QHBoxLayout()
        panel_mid.addWidget(self.friends_panel)
        panel_mid.addWidget(self.dialogue)
        panel_mid.addWidget(self.files_panel)

        # Main layout
        layout = QVBoxLayout()
        layout.addLayout(upper_layout)
        layout.addLayout(panel_mid)
        layout.addLayout(panel_south)

        central.setLayout(layout)

        # Handle button signals
        self.sendbutton.clicked.connect(self.handleButtonClick)
        
    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Return or event.key() == Qt.Key.Key_Enter:
            message_text = self.chatfld.text()
                    
            self.TCP_klient.send(message_text.encode('UTF-8'))
                    
            try:
                if len(message_text) != "" and message_text.strip() != "":
                            
                    message = SendHypertextMessage(message_text)
                    self.dialogue_layout.addWidget(message)
                            
                    spacer = QSpacerItem(5, 5, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
                    self.dialogue_layout.addItem(spacer)

            except Exception as e:
                error_message = str(e)
                print(f"Error: {error_message}")

            self.chatfld.setText("")

    def handleButtonClick(self):
        sender = self.sender()
        if sender == self.sendbutton:
            message_text = self.chatfld.text()
            
            self.TCP_klient.send(message_text.encode('UTF-8'))
            
            try:
                if len(message_text) != "" and message_text.strip() != "":
                    
                    message = SendHypertextMessage(message_text)
                    self.dialogue_layout.addWidget(message)
                    
                    spacer = QSpacerItem(5, 5, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
                    self.dialogue_layout.addItem(spacer)

            except Exception as e:
                error_message = str(e)
                print(f"Error: {error_message}")

            self.chatfld.setText("")

        elif sender == self.attachbutton:
            pass

    def closeEvent(self, event):
        try:
            self.TCP_klient.close()
        except Exception as e:
            print(f'Fejl ved nedlukning af TCP-forbindelse: {e}')
        event.accept()

class AttachFilesWindow(QMainWindow):
    def __init__(self, p):
        super().__init__()
        self.parent = p

class Themes():
    def __innit__(self,p):
        super().__init__()
        self.parent= p        
        pass

if __name__ == "__main__":
    app = QApplication([])  # Initialiser QApplication
    gui = MainWindow()       # Instantierer gui - som jo er instans af QMainWindow
    gui.show()              # Skal specifikt gøres synlig (kan også ske i konstruktor)
    app.exec()