from PyQt6.QtWidgets import *

class Themes(QMessageBox):
    def __init__(self):
        super().__init__()     

        # theme_central= QWidget(self)
        # self.setCentralWidget(theme_central)

        self.setWindowTitle('Themes')
        self.setText('Choose a Theme')

        self.selected_theme= None
        
        self.button_MC= self.addButton('Minecraft', self.ApplyRole)
        self.button_MLP= self.addButton('My Little Pony', self.ApplyRole)
        self.button_STH= self.addButton('Sonic The Hedgehog', self.ApplyRole)

        self.button_MC.clicked.connect(self.themeHandleButtonClick)
        self.button_MLP.clicked.connect(self.themeHandleButtonClick)
        self.button_STH.clicked.connect(self.themeHandleButtonClick)

        #self.buttonClicked.connect(self.on_button_clicked)

        # self.button_MC= QPushButton('Minecraft')
        # self.button_MLP= QPushButton('My Little Pony')
        # self.button_STH= QPushButton('Sonic The Hedgehog')

        # theme_layout= QVBoxLayout()
        # theme_layout.addWidget(self.button_MC)
        # theme_layout.addWidget(self.button_MLP)
        # theme_layout.addWidget(self.button_STH)

        #theme_central.setLayout(theme_layout)

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
    app = QApplication([])
    msg_box = QMessageBox()
    msg_box.exec()
    print("Selected option:", msg_box.get_result())
    exit(app.exec())
