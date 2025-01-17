from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtGui import QPixmap
import os
from weakref import ref

class Themes(QMessageBox):
    def __init__(self, parent):
        super().__init__()

        self.setWindowTitle('Themes')
        self.setText('Choose a Theme')
        
        self.parent = ref(parent)

        self.selected_theme = None

        self.button_MC = self.addButton('Minecraft', self.ButtonRole.ActionRole)
        self.button_MLP = self.addButton('My Little Pony', self.ButtonRole.ActionRole)
        self.button_STH = self.addButton('Sonic The Hedgehog', self.ButtonRole.ActionRole)
        
        self.button_MC.clicked.connect(self.themeHandleButtonClick)
        self.button_MLP.clicked.connect(self.themeHandleButtonClick)
        self.button_STH.clicked.connect(self.themeHandleButtonClick)

        self.exec()

    def themeHandleButtonClick(self):
        sender = self.sender()

        if sender == self.button_MC:
            self.selected_theme = 'Minecraft'
        elif sender == self.button_MLP:
            self.selected_theme = 'MyLittlePony'
        elif sender == self.button_STH:
            self.selected_theme = 'Sonic'

        self.applyTheme()

    def applyTheme(self):
        parent = self.parent()
        if not parent:  
            print("Error: Parent widget no longer exists.")
            return

        theme_map = {
            'Minecraft': 'minecraft_theme.jpg',
            'MyLittlePony': 'my_little_pony.jpg',
            'Sonic': 'sonic_the_hedgehog.jpg',
        }

        file_name = theme_map.get(self.selected_theme)
        if file_name:
            path = os.path.join('ChatApp', 'App', 'Pictures', file_name)
            parent.left_group_icon.setPixmap(QPixmap(path))
            parent.left_group_icon.setScaledContents(True)  
            parent.right_group_icon.setPixmap(QPixmap(path))
            parent.right_group_icon.setScaledContents(True)  