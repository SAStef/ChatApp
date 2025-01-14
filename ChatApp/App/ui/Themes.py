from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt, pyqtSignal, QThread
import socket as s
from PyQt6.QtGui import QPixmap
from threading import Thread


class Themes(QMainWindow):
    def __init__(self):
        super().__init__()     
        
        self.selected_theme= None

        print("funktionen blev kaldt")

        theme_central= QWidget(self)
        self.setCentralWidget(theme_central)

        self.button_MC= QPushButton('Minecraft')
        self.button_MLP= QPushButton('My Little Pony')
        self.button_STH= QPushButton('Sonic The Hedgehog')

        theme_layout= QVBoxLayout()
        theme_layout.addWidget(self.button_MC)
        theme_layout.addWidget(self.button_MLP)
        theme_layout.addWidget(self.button_STH)

        theme_central.setLayout(theme_layout)

        self.button_MC.clicked.connect(self.themeHandleButtonClick)
        self.button_MLP.clicked.connect(self.themeHandleButtonClick)
        self.button_STH.clicked.connect(self.themeHandleButtonClick)

    
        # if self.selectedTheme == 'Minecraft':
        
        #     self.parent.dialogue.setStyleSheet('''
        #         QWidget {
        #         background-image: url("minecraft_theme.jpg");
        #         background-repeat: no-repeat;
        #         background-position: center;
                
        #         }''')
        #     self.parent.dialogue.setScaledContents(True)

        # elif self.selectedTheme == 'MyLittlePony':

        #     self.parent.dialogue.setStyleSheet('''
        #         QWidget {
        #         background-image: url("my_little_pony.jpg");
        #         background-repeat: no-repeat;
        #         background-position: center;
                
        #         }''')
        #     self.parent.dialogue.setScaledContents(True)
        
        # elif self.selectedTheme == 'Sonic':

        #     self.parent.dialouge.setStyleSheet('''
        #         QWidget {
        #         background-image: url("sonic_the_hedgehog.jpg");
        #         background-repeat: no-repeat;
        #         background-position: center;
                
        #         }''')
        #     self.parent.dialogue.setScaledContents(True)
        
        # else:
        #     self.parent.dialogue.SetStyleSheet('''
        #         QWidget {
        #         background-image: url("coconut.jpeg");
        #         background-repeat: no-repeat;
        #         background-position: center;
                
        #         }''')
        #     self.parent.dialogue.setScaledContents(True)
    
    def themeHandleButtonClick(self):
        sender= self.sender()

        if sender == self.button_MC:
            self.selected_theme= ('Minecraft')
        elif sender == self.button_MLP:
            self.selected_theme= ('MyLittlePony')
        elif sender == self.button_STH:
            self.selected_theme= ('Sonic')
    
    def appliedTheme(self):
        if self.selected_theme == 'Minecraft':
            self.setStyleSheet('''
                QWidget {
                    background-image: url("minecraft_theme.jpg");
                    background-repeat: no-repeat;
                    background-position: center;
                }''')
        elif self.selected_theme == 'My Little Pony':
            self.setStyleSheet('''
                QWidget {
                    background-image: url("my_little_pony.jpg");
                    background-repeat: no-repeat;
                    background-position: center;
                }''')
        elif self.selected_theme == 'Sonic The Hedgehog':
            self.setStyleSheet('''
                QWidget {
                    background-image: url("sonic_the_hedgehog.jpg");
                    background-repeat: no-repeat;
                    background-position: center;
                }''')
        
        


if __name__ == "__main__":
    app = QApplication([])  # Initialiser QApplication
    gui = Themes()       # Instantierer gui - som jo er instans af QMainWindow
    gui.show()              # Skal specifikt gøres synlig (kan også ske i konstruktor)
    app.exec()