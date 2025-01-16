from PyQt6.QtWidgets import *
from PyQt6.QtGui import QPixmap


class Themes(QMessageBox):
    def __init__(self,p):
        super().__init__()     

        self.setWindowTitle('Themes')
        self.setText('Choose a Theme')
        self.parent = p

        self.selected_theme = None
        
        self.button_MC= self.addButton('Minecraft', self.ButtonRole.ActionRole)
        self.button_MLP= self.addButton('My Little Pony', self.ButtonRole.ActionRole)
        self.button_STH= self.addButton('Sonic The Hedgehog', self.ButtonRole.ActionRole)

        self.button_MC.clicked.connect(self.themeHandleButtonClick)
        self.button_MLP.clicked.connect(self.themeHandleButtonClick)
        self.button_STH.clicked.connect(self.themeHandleButtonClick)
       
        self.exec()

    def themeHandleButtonClick(self):
        sender= self.sender()

        if sender == self.button_MC:
            self.selected_theme= 'Minecraft'
        elif sender == self.button_MLP:
            self.selected_theme= 'MyLittlePony'
        elif sender == self.button_STH:
            self.selected_theme= 'Sonic'
            
        self.appliedTheme()
    
    def appliedTheme(self):
    
        if self.selected_theme == 'Minecraft':
            self.parent.right_group_icon.setPixmap(QPixmap('./ChatApp\App\Pictures\minecraft_theme.jpg'))

        elif self.selected_theme == 'MyLittlePony':
            self.parent.right_group_icon.setPixmap(QPixmap('./ChatApp\App\Pictures\my_little_pony.jpg'))

        elif self.selected_theme == 'Sonic':
            self.parent.right_group_icon.setPixmap(QPixmap('./ChatApp\App\Pictures\sonic_the_hedgehog.jpg'))
