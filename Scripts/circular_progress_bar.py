import sys
import os
from math import cos, sin, radians
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class CircularProgress(QWidget):
    def __init__(self):
        super().__init__()
        self.value = 0
        self.width = 400
        self.height = 400
        self.progress_width = 30
        self.progress_rounded_cap = True
        self.progress_color = QColor(22, 109, 245)
        self.background_color = QColor(220, 220, 220)  # Color for the uncompleted part
        self.max_value = 100
        self.font_family = "Segoe UI"
        self.font_size = 12
        self.suffix = "%"
        self.text_color = QColor(0, 0, 0)  # Black text color
        self.resize(self.width, self.height)

        this_file_location = os.path.dirname(__file__)
        center_image = os.path.abspath(os.path.join(this_file_location, '..', 'Images', 'bg.png'))
        start_image = os.path.abspath(os.path.join(this_file_location, '..', 'Images', 'profile_white.png'))
        end_image = os.path.abspath(os.path.join(this_file_location, '..', 'Images', 'time-left (1).png'))
        self.center_image = QImage(center_image)
        self.start_image = QImage(start_image)
        self.end_image = QImage(end_image)

        self.start_image = self.start_image.scaled(30, 30, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.end_image = self.end_image.scaled(30, 30, Qt.KeepAspectRatio, Qt.SmoothTransformation)

    def add_shadow(self, enable):
        if enable:
            self.shadow = QGraphicsDropShadowEffect(self)
            self.shadow.setBlurRadius(15)
            self.shadow.setXOffset(0)
            self.shadow.setYOffset(0)
            self.shadow.setColor(QColor(0, 0, 0, 120))
            self.setGraphicsEffect(self.shadow)

    def set_value(self, value):
        self.value = value
        self.repaint()

    def paintEvent(self, e):
        size = min(self.width, self.height)
        width = int(size - self.progress_width)
        height = int(size - self.progress_width)
        margin = int(self.progress_width / 2)
        value = int(self.value * 360 / self.max_value)

        paint = QPainter()
        paint.begin(self)
        paint.setRenderHint(QPainter.Antialiasing)
        font = QFont(self.font_family, self.font_size, QFont.Bold)
        paint.setFont(font)

        rect = QRect(0, 0, size, size)
        paint.setPen(Qt.NoPen)
        paint.drawRect(rect)

        # Draw the background circle (uncompleted part)
        pen = QPen()
        pen.setColor(self.background_color)
        pen.setWidth(self.progress_width)
        if self.progress_rounded_cap:
            pen.setCapStyle(Qt.RoundCap)
        paint.setPen(pen)
        paint.drawArc(margin, margin, width, height, 0, 360 * 16)

        # Draw the progress bar (completed part)
        pen.setColor(self.progress_color)
        paint.setPen(pen)
        paint.drawArc(margin, margin, width, height, -90 * 16, -value * 16)

        # Enlarge the center image to fill the inner part
        image_size = size - self.progress_width*2
        scaled_center_image = self.center_image.scaled(image_size, image_size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        image_rect = QRect(margin + self.progress_width // 2, margin + self.progress_width // 2, image_size, image_size)
        paint.drawImage(image_rect, scaled_center_image)

        pen.setColor(self.text_color)
        paint.setPen(pen)
        text_rect = QRect(margin, margin, width, height)
        paint.drawText(text_rect, Qt.AlignCenter, f"{self.value} {self.suffix}")

        start_angle_rad = radians(90)
        start_x = int(size / 2 + (width / 2) * cos(start_angle_rad) - self.start_image.width() / 2)
        start_y = int(size / 2 + (height / 2) * sin(start_angle_rad) - self.start_image.height() / 2)
        paint.drawImage(QRect(start_x, start_y, self.start_image.width(), self.start_image.height()), self.start_image)

        end_angle_rad = radians(90 + (self.value * 360 / self.max_value))
        end_x = int(size / 2 + (width / 2) * cos(end_angle_rad) - self.end_image.width() / 2)
        end_y = int(size / 2 + (height / 2) * sin(end_angle_rad) - self.end_image.height() / 2)
        paint.drawImage(QRect(end_x, end_y, self.end_image.width(), self.end_image.height()), self.end_image)

        paint.end()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(600, 600)

        self.container = QFrame()
        self.container.setStyleSheet("background-color: white")
        self.layout = QVBoxLayout()

        self.progress = CircularProgress()
        self.progress.value = 0
        self.progress.suffix = "%"
        self.progress.font_size = 30
        self.progress.width = 500
        self.progress.height = 500
        self.progress.progress_width = 40
        self.progress.progress_color = QColor(22, 109, 245)
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
