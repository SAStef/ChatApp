from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt, pyqtSignal, QThread, QTimer
import socket as s
from PyQt6.QtGui import QPixmap
from Messages.SendHypertextMessage import SendHypertextMessage
from threading import Thread
from os import path
import os
# from ui.AttachFilesWindow import AttachFilesWindow #ikke brugt endnu - skal uncomment'es
# from ui.Themes import Themes #ikke brugt endnu - skal uncomment'es
from Messages.ReceiveHypertextMessage import ReceiveHypertextMessage #bliver ikke brugt endnu

from ui.AttachFilesWindow import AttachFilesWindow # bliver heller ikke brugt endnu
from ui.ScrollAreaUI import scrollarea_styles
from ui.ActiveFriendsPanel import active_friends_panel_style
from ui.AutoScrollButton import auto_scroll_on_button_style, auto_scroll_off_button_style
from ui.Themes import Themes
from ui.SetThemeButton import set_theme_button


class ReceiveFilesThread(QThread):
    def __init__(self, client_socket, file_header):
        super().__init__()
        self.client_socket = client_socket
        self.file_header = file_header

    def run(self):
        try:
            # Use makefile() to handle the socket as a file
            sock_file = self.client_socket.makefile('rb')

            # Read the header line by line
            header_lines = []
            while True:
                line = sock_file.readline()
                if line == b'\n':  # Empty line marks the end of the header
                    break
                header_lines.append(line.decode('UTF-8').strip())

            # Process header to extract filename and file length
            if len(header_lines) < 2:
                raise ValueError("Invalid header format")

            filename = header_lines[0].split(":")[1].strip()
            file_length = int(header_lines[1].split(":")[1].strip())

            print(f"Receiving file: {filename}, size: {file_length} bytes")

            # Prepare the download directory
            download_dir = "./Downloads"
            os.makedirs(download_dir, exist_ok=True)
            file_path = os.path.join(download_dir, filename)

            # Open file to write data
            with open(file_path, 'wb') as f:
                bytes_received = 0
                while bytes_received < file_length:
                    buffer = sock_file.read(min(1024, file_length - bytes_received))
                    if not buffer:
                        raise ConnectionError("Connection closed before file transfer completed.")
                    f.write(buffer)
                    bytes_received += len(buffer)
                    print(f"Received {bytes_received}/{file_length} bytes")

                print(f"File saved to: {file_path}")

        except Exception as e:
            print(f"Error in file transfer: {e}")

        finally:
            self.client_socket.settimeout(None)
            sock_file.close()

class ReceiverThread(QThread):
    message_recieved = pyqtSignal(str)
    file_recieved = pyqtSignal(str)  # Signal to emit when a file is received
    file_transfer_in_progress = pyqtSignal(bool)  # New signal to notify about file transfer status

    def __init__(self, client_socket):
        super().__init__()
        self.client_socket = client_socket
        self.running = True

    def run(self):
        counter = 0
        while self.running:
            try:
                serverdata = self.client_socket.recv(1024)
                if not serverdata:
                    self.client_socket.close()
                    break
                
                # Check if the data is a file header (starts with 'FILE:')
                if serverdata.startswith(b'FILE:'):
                    print("Starting file transfer...")

                    # Notify that file transfer is in progress
                    self.file_transfer_in_progress.emit(True)

                    # Ensure we capture the full header before creating the thread
                    while b"\n\n" not in serverdata:
                        serverdata += self.client_socket.recv(1024)

                    # Pass the file header and client socket to ReceiveFilesThread
                    file_thread = ReceiveFilesThread(client_socket=self.client_socket, file_header=serverdata)
                    file_thread.start()

                    print("File transfer in progress...")
                else:
                    # Decode the text message and emit it
                    decoded_data = serverdata.decode('UTF-8', errors='ignore')  # Ignore invalid UTF-8 bytes
                    self.message_recieved.emit(decoded_data)

            except Exception as e:
                if self.running:
                    print(f'Error in ReceiverThread: {e}')
                    counter += 1
                if counter > 20:
                    break

    def stop(self):
        self.running = False
        
class ReceiverThread(QThread):
    message_recieved = pyqtSignal(str)
    file_recieved = pyqtSignal(str)
    file_transfer_in_progress = pyqtSignal(bool)  # Signal for file transfer progress

    def __init__(self, client_socket):
        super().__init__()
        self.client_socket = client_socket
        self.running = True

    def run(self):
        counter = 0
        while self.running:
            try:
                serverdata = self.client_socket.recv(1024)
                if not serverdata:
                    self.client_socket.close()
                    break

                # Check if the data is a file header (starts with 'FILE:')
                if serverdata.startswith(b'FILE:'):
                    print("Starting file transfer...")

                    # Notify that file transfer is in progress
                    self.file_transfer_in_progress.emit(True)

                    # Ensure we capture the full header before creating the thread
                    while b"\n\n" not in serverdata:
                        serverdata += self.client_socket.recv(1024)

                    # Pass the file header and client socket to ReceiveFilesThread
                    file_thread = ReceiveFilesThread(client_socket=self.client_socket, file_header=serverdata)
                    file_thread.start()

                    print("File transfer in progress...")
                else:
                    # Decode the text message and emit it
                    decoded_data = serverdata.decode('UTF-8', errors='ignore')  # Ignore invalid UTF-8 bytes
                    self.message_recieved.emit(decoded_data)

            except Exception as e:
                if self.running:
                    print(f'Error in ReceiverThread: {e}')
                    counter += 1
                if counter > 20:
                    break

    def stop(self):
        self.running = False
                
class MainWindow(QMainWindow):
    def __init__(self, ):
        super().__init__()

        # Tilsutter til chat-serveren
        self.TCP_server_ip = "10.209.224.4"
        self.TCP_server_port = 1337
        self.TCP_klient = s.socket(s.AF_INET, s.SOCK_STREAM)
        self.TCP_klient.connect((self.TCP_server_ip, self.TCP_server_port))

        # Starter en tråd til recievertråden
        self.reciever = ReceiverThread(self.TCP_klient)
        self.reciever.message_recieved.connect(self.handle_message)
        self.reciever.file_recieved.connect(self.handle_file)
        self.reciever.file_transfer_in_progress.connect(self.handle_file_transfer_status)  # Connect signal here
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
        
        self.sendbutton.setEnabled(True)

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
        self.right_group_icon.setScaledContents(True)

        self.act_friends_panel = QLabel("Active users: ", self) 
        self.act_friends_panel.setFixedWidth(800)
        self.act_friends_panel.setFixedHeight(30)

        self.act_friends_panel.setStyleSheet(active_friends_panel_style)
        
        self.AutoScrollOn = QPushButton("Autoscroll On")
        self.AutoScrollOff = QPushButton("Autoscroll Off")
        
        self.AutoScrollOn.setStyleSheet(auto_scroll_on_button_style)
        self.AutoScrollOff.setStyleSheet(auto_scroll_off_button_style)

        self.isAutoScroll = True

        upper_layout= QHBoxLayout()
        
        self.set_theme_btn= QPushButton('Set Theme')
        self.set_theme_btn.setFixedWidth(100)
        self.set_theme_btn.setFixedHeight(50)
        self.set_theme_btn.setStyleSheet(set_theme_button)

        

        upper_layout= QHBoxLayout()
        #upper_layout.addSpacerItem(upper_left_spacer)
        upper_layout.addWidget(self.left_group_icon)
        upper_layout.addWidget(self.act_friends_panel)
        upper_layout.addWidget(self.set_theme_btn)
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
        self.attachbutton.clicked.connect(self.handleButtonClick)
        self.set_theme_btn.clicked.connect(self.handleButtonClick)
        
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

    def handle_file_transfer_status(self, is_in_progress):
        """Handle file transfer status and disable/enable the send button."""
        if is_in_progress:
            self.sendbutton.setEnabled(False)  # Disable send button while the file is transferring
        else:
            self.sendbutton.setEnabled(True)  # Enable send button once the file transfer is complete

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
            with open(f'./downloads/{file_name}', 'wb') as f:
                f.write(file_content)
            print(f'File {file_name} saved to ./downloads')

            self.reciever.file_transfer_in_progress.emit(False)

        except Exception as e:
            print(f'Error: {e}')
        
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
                QTimer.singleShot(20, lambda: self.dialogue.verticalScrollBar().setValue(self.dialogue.verticalScrollBar().maximum()))
            self.chatfld.setText("")
        
        elif sender == self.set_theme_btn:
            Themes()

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
    