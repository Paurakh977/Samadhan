import sys 
import os
from PyQt5.QtCore import * 
from PyQt5.QtGui import * 
from PyQt5.QtWidgets import *
from circular_progress import CircularProgress

class MainWindow(QMainWindow):  
    def __init__(self):
        super().__init__()
        self.resize(600, 600)

        self.container = QFrame()
        self.container.setStyleSheet("background-color: transparent")
        self.layout = QVBoxLayout()

        self.progress = CircularProgress()
        self.progress.value = 0
        self.progress.suffix = "%"
        self.progress.font_size = 30        
        self.progress.width = 500
        self.progress.height = 500
        self.progress.progress_width = 40
        self.progress.progress_color =  QColor(22, 109, 245)
        self.progress.progress_rounded_cap = True
        self.progress.setMinimumSize(self.progress.width, self.progress.height)

        self.slider = QSlider(Qt.Horizontal) 
        self.slider.setRange(0, 100)
        self.slider.valueChanged.connect(self.change_value)

        self.layout.addWidget(self.progress, Qt.AlignCenter, Qt.AlignCenter) 
        self.layout.addWidget(self.slider, Qt.AlignCenter, Qt.AlignCenter)

        self.container.setLayout(self.layout)
        self.setCentralWidget(self.container)

        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.show()

    def change_value(self, value):
        self.progress.set_value(value)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())

