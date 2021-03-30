import sys, os
from os import system
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QImage, QPalette, QBrush, QIcon
from PyQt5.QtWidgets import *

class main_Window(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.setGeometry(450, 150, 1080, 800)
        self.setFixedSize(1080, 800)
        self.setWindowIcon(QIcon('image/main_icon.png'))

        bg = QImage('image/main.png')

        palette = QPalette()
        palette.setBrush(10, QBrush(bg))

        self.setPalette(palette)
        self.setWindowTitle("2Game")

        btn_racing = QPushButton(self)
        btn_racing.setStyleSheet("border-image : url(image/PyCar.png)")
        btn_racing.move(280, 550)
        btn_racing.resize(223, 134)
        btn_racing.clicked.connect(self.racing_btn_clicked)

        btn_jumping = QPushButton(self)
        btn_jumping.setStyleSheet("border-image : url(image/santa_bg.png)")
        btn_jumping.move(610, 513)
        btn_jumping.resize(170, 170)
        btn_jumping.clicked.connect(self.jumping_btn_clicked)

        self.setGeometry(450, 150, 1080, 800)
        self.show()

    def racing_btn_clicked(self):
        system("racing_game.py")

    def jumping_btn_clicked(self):
        system("juming_game.py")

if __name__ == "__main__":
       app = QApplication(sys.argv)
       ex = main_Window()
       sys.exit(app.exec_())