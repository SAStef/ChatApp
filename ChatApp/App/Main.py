from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt, pyqtSignal, QThread, QTimer
import socket as s
from PyQt6.QtGui import QPixmap
from Messages.SendHypertextMessage import SendHypertextMessage
from threading import Thread
from os import path
import os
# from ui.AttachFilesWindow import AttachFilesWindow #ikke brugt endnu - skal uncomment'es
<<<<<<< Updated upstream
# from ui.Themes import Themes #ikke brugt endnu - skal uncomment'es
from Messages.ReceiveHypertextMessage import ReceiveHypertextMessage #bliver ikke brugt endnu

from ui.AttachFilesWindow import AttachFilesWindow # bliver heller ikke brugt endnu
from ui.ScrollAreaUI import scrollarea_styles
from ui.ActiveFriendsPanel import active_friends_panel_style
from ui.AutoScrollButton import auto_scroll_on_button_style, auto_scroll_off_button_style
=======
from ui.Themes import Themes #ikke brugt endnu - skal uncomment'es
from Messages.ReceiveHypertextMessage import ReceiveHypertextMessage #bliver ikke brugt endnu 
>>>>>>> Stashed changes

class RecieverThread(QThread):
    message_recieved = pyqtSignal(str)
    file_recieved = pyqtSignal(bytes, str)
    
    def __init__(self, client_socket):
        super().__init__()
        self.client_socket = client_socket
        self.running = True
        
    def run(self, ):
        counter = 0
        while self.running:
            try:
                serverdata = self.client_socket.recv(2048)
                if not serverdata:
                    self.client_socket.close()
                    break
                
                decoded_data = serverdata.decode('UTF-8')

                if decoded_data.startswith('FILE:'):
                    self.receive_file(decoded_data)
                else:
                    self.message_recieved.emit(decoded_data)
            except Exception as e:
                if self.running:
                    print(f'Fejl i ReceiverThread: {e}')
                    counter += 1
                if counter > 20:
                    break

    def receive_file(self, file_header):
        header_lines = file_header.split("\n")
        filename = header_lines[0].split(":")[1].strip()
        file_length = int(header_lines[1].split(":")[1].strip())

        download_dir = "./Downloads"
        if not path.exists(download_dir):
            os.makedirs(download_dir)

        file_path = path.join(download_dir, filename)
        print(f"Modtager fil: {filename} på {file_length} bytes...")

        with open(file_path, 'wb') as f:
            bytes_received = 0
            while bytes_received < file_length:
                buffer = self.client_socket.recv(2048)
                if not buffer:
                    break
                f.write(buffer)
                bytes_received += len(buffer)
        
        print(f'Fil gemt med stien: {file_path}')

class MainWindow(QMainWindow):
    def __init__(self, ):
        super().__init__()
        
        # Tilsutter til chat-serveren
<<<<<<< Updated upstream
        self.TCP_server_ip = "127.0.0.1"

=======
        self.TCP_server_ip = "10.209.224.4"
>>>>>>> Stashed changes
        self.TCP_server_port = 1337
        self.TCP_klient = s.socket(s.AF_INET, s.SOCK_STREAM)
        self.TCP_klient.connect((self.TCP_server_ip, self.TCP_server_port))

        # Starter en tråd til recievertråden
        self.reciever = RecieverThread(self.TCP_klient)
        self.reciever.message_recieved.connect(self.handle_message)  # Connect the signal to the slot
        self.reciever.file_recieved.connect(self.handle_file)
        self.reciever.start()
        
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

        panel_south = QHBoxLayout()
        panel_south.addWidget(self.attachbutton)
        panel_south.addWidget(self.chatfld)
        panel_south.addWidget(self.sendbutton)

        self.dialogue = QScrollArea()
        self.dialogue.setWidgetResizable(True)
        self.dialogue.setStyleSheet(scrollarea_styles)
    
        self.dialogue_content = QWidget()
        self.dialogue_layout = QVBoxLayout(self.dialogue_content)
        self.dialogue_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.dialogue.setWidget(self.dialogue_content)

        self.left_group_icon= QLabel()
        self.left_group_icon.setFixedWidth(100)
        self.left_group_icon.setFixedHeight(50)
        self.left_group_icon.setStyleSheet("background-color: #0D1C2F;")
        self.left_group_icon.setPixmap(QPixmap('./ChatApp/App/Pictures/coconut.jpeg'))
        self.left_group_icon.setScaledContents(True) #Hvis det er nødvendigt (Edit: Det var det)

        self.right_group_icon= QLabel()
        self.right_group_icon.setFixedWidth(100)
        self.right_group_icon.setFixedHeight(50)
        self.right_group_icon.setStyleSheet("background-color: #0D1C2F;")
        self.right_group_icon.setPixmap(QPixmap('./ChatApp/App/Pictures/ginger.jpeg'))

<<<<<<< Updated upstream
        self.act_friends_panel = QLabel("Active users: ", self) 
        self.act_friends_panel.setFixedWidth(1000)
        self.act_friends_panel.setFixedHeight(30)

        self.act_friends_panel.setStyleSheet(active_friends_panel_style)
        
        self.AutoScrollOn = QPushButton("Autoscroll On")
        self.AutoScrollOff = QPushButton("Autoscroll Off")
        
        self.AutoScrollOn.setStyleSheet(auto_scroll_on_button_style)
        self.AutoScrollOff.setStyleSheet(auto_scroll_off_button_style)

        self.isAutoScroll = True

        upper_layout= QHBoxLayout()
        upper_layout.addWidget(self.left_group_icon)
        upper_layout.addWidget(self.act_friends_panel)
=======
        self.set_theme= QPushButton('Set Theme')
        self.set_theme.setFixedWidth(600)
        self.set_theme.setFixedHeight(50)
        self.set_theme.setStyleSheet('backgro)und-color: gray;')

        

        upper_layout= QHBoxLayout()
        #upper_layout.addSpacerItem(upper_left_spacer)
        upper_layout.addWidget(self.group_icon)
        upper_layout.addWidget(self.set_theme)
>>>>>>> Stashed changes
        upper_layout.addWidget(self.right_group_icon)
        
        # all autoscroll stuff
        auto_scroller_layout = QVBoxLayout()
        
        self.isAutoScroll = True

        opacity_effect_on = QGraphicsOpacityEffect()
        opacity_effect_on.setOpacity(1.0)  
        self.AutoScrollOn.setGraphicsEffect(opacity_effect_on)

        opacity_effect_off = QGraphicsOpacityEffect()
        opacity_effect_off.setOpacity(0.3) 
        self.AutoScrollOff.setGraphicsEffect(opacity_effect_off)
        
        auto_scroller_layout.addWidget(self.AutoScrollOn)
        auto_scroller_layout.addWidget(self.AutoScrollOff)

        auto_scroller_layout.setAlignment(Qt.AlignmentFlag.AlignRight)
        upper_layout.addLayout(auto_scroller_layout)

        panel_mid = QHBoxLayout()
        panel_mid.addWidget(self.dialogue)

        # Main layout
        layout = QVBoxLayout()
        layout.addLayout(upper_layout)
        layout.addLayout(panel_mid)
        layout.addLayout(panel_south)

        central.setLayout(layout)

        # Handle button signals
        self.sendbutton.clicked.connect(self.handleButtonClick)
<<<<<<< Updated upstream
        self.attachbutton.clicked.connect(self.handleButtonClick)
=======
        self.set_theme.clicked.connect(self.handleButtonClick)
>>>>>>> Stashed changes
        
        self.AutoScrollOff.clicked.connect(self.autoScrollButton)
        self.AutoScrollOn.clicked.connect(self.autoScrollButton)
        
    def autoScrollButton(self):
        sender = self.sender()
      
        if sender == self.AutoScrollOn:
            self.isAutoScroll = True
            opacity_effect_on = QGraphicsOpacityEffect()
            opacity_effect_on.setOpacity(1.0) 
            self.AutoScrollOn.setGraphicsEffect(opacity_effect_on)
           
            opacity_effect_off = QGraphicsOpacityEffect()
            opacity_effect_off.setOpacity(0.3) 
            self.AutoScrollOff.setGraphicsEffect(opacity_effect_off)

        elif sender == self.AutoScrollOff:
            self.isAutoScroll = False
            opacity_effect_off = QGraphicsOpacityEffect()
            opacity_effect_off.setOpacity(1.0) 
            self.AutoScrollOff.setGraphicsEffect(opacity_effect_off)

            opacity_effect_on = QGraphicsOpacityEffect()
            opacity_effect_on.setOpacity(0.3) 
            self.AutoScrollOn.setGraphicsEffect(opacity_effect_on)

    def handle_message(self, message):
        try:
                if len(message) != "" and message.strip() != "":
                    messageContent = ReceiveHypertextMessage(message)
                    self.dialogue_layout.addWidget(messageContent, alignment=Qt.AlignmentFlag.AlignLeft)

        except Exception as e:
                error_message = str(e)
                print(f"Error: {error_message}")
              
        if self.isAutoScroll == True:
            QTimer.singleShot(1, lambda: self.dialogue.verticalScrollBar().setValue(self.dialogue.verticalScrollBar().maximum()))

    def handle_file(self, file_content, file_name):
        try:
            # Gemmer filen på disken
            with open(f'./downloads/{file_name}', 'wb') as f:
                f.write(file_content)
            print(f'Filen {file_name} blev gemt i ./downloads')

        except Exception as e:
            print(f'Fejl: {e}')
        
        if self.isAutoScroll == True:
            QTimer.singleShot(1, lambda: self.dialogue.verticalScrollBar().setValue(self.dialogue.verticalScrollBar().maximum()))

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Return or event.key() == Qt.Key.Key_Enter:
            message_text = self.chatfld.text()
            
            if len(message_text) != "" and message_text.strip() != "":
                self.TCP_klient.send(message_text.encode('UTF-8'))
                try:
                        
                        message = SendHypertextMessage(message_text)
                        self.dialogue_layout.addWidget(message, alignment=Qt.AlignmentFlag.AlignRight)
                        
                except Exception as e:
                    error_message = str(e)
                    print(f"Error: {error_message}")

            if self.isAutoScroll == True:
                QTimer.singleShot(1, lambda: self.dialogue.verticalScrollBar().setValue(self.dialogue.verticalScrollBar().maximum()))
            self.chatfld.setText("")

    def handleButtonClick(self):
        sender = self.sender()
        if sender == self.sendbutton:
            message_text = self.chatfld.text()

            if len(message_text) != "" and message_text.strip() != "":
                self.TCP_klient.send(message_text.encode('UTF-8'))
                try:
                    message = SendHypertextMessage(message_text)
                    self.dialogue_layout.addWidget(message, alignment=Qt.AlignmentFlag.AlignRight)

                except Exception as e:
                    error_message = str(e)
                    print(f"Error: {error_message}")

            if self.isAutoScroll == True:
                QTimer.singleShot(1, lambda: self.dialogue.verticalScrollBar().setValue(self.dialogue.verticalScrollBar().maximum()))
            self.chatfld.setText("")
        
        elif sender == self.set_theme:
            Themes(self)

        elif sender == self.attachbutton:
            AttachFilesWindow(self)

    def closeEvent(self, event):
        try:
            # self.reciever.wait()
            self.TCP_klient.close()
        except Exception as e:
            print(f'Fejl ved nedlukning af TCP-forbindelse: {e}')
        event.accept()

if __name__ == "__main__":
    app = QApplication([])  # Initialiser QApplication
    gui = MainWindow()       # Instantierer gui - som jo er instans af QMainWindow
    gui.show()              # Skal specifikt gøres synlig (kan også ske i konstruktor)
    app.exec()
    