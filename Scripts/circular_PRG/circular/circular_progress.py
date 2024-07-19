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
        self.max_value = 100
        self.font_family = "Segoe UI"
        self.font_size = 12
        self.suffix = "%"
        self.text_color = 0xFFFFFF
        self.resize(self.width, self.height)

        # Load and scale the images
        self.center_image = QImage(r"C:\Users\pande\OneDrive\Desktop\PyQt\Samadhan-App\Images\24-hours (1).png")
        self.start_image = QImage(r'C:\Users\pande\OneDrive\Desktop\PyQt\Samadhan-App\Images\profile_white.png')
        self.end_image = QImage(r"C:\Users\pande\OneDrive\Desktop\PyQt\Samadhan-App\Images\time-left (1).png")
        
        # Scale the images to fit the progress bar
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

        pen = QPen()
        pen.setColor(self.progress_color)
        pen.setWidth(self.progress_width)
        if self.progress_rounded_cap:
            pen.setCapStyle(Qt.RoundCap)

        paint.setPen(pen)
        paint.drawArc(margin, margin, width, height, -90 * 16, -value * 16)

        image_size = min(width, height) - self.progress_width * 2
        image_rect = QRect(margin + (width - image_size) // 2, margin + (height - image_size) // 2, image_size, image_size)
        paint.drawImage(image_rect, self.center_image)

        pen.setColor(QColor(self.text_color))
        paint.setPen(pen)
        text_rect = QRect(margin, margin, width, height)
        paint.drawText(text_rect, Qt.AlignCenter | Qt.AlignTop, f"{self.value} {self.suffix}")

        # Calculate positions for the start and end images based on the progress value
        # Start image should be fixed at the bottom (6 o'clock position)
        start_angle_rad = radians(90)
        start_x = int(size / 2 + (width / 2) * cos(start_angle_rad) - self.start_image.width() / 2)
        start_y = int(size / 2 + (height / 2) * sin(start_angle_rad) - self.start_image.height() / 2)
        paint.drawImage(QRect(start_x, start_y, self.start_image.width(), self.start_image.height()), self.start_image)

        # End image should move with the progress bar
        end_angle_rad = radians(90 + (self.value * 360 / self.max_value))
        end_x = int(size / 2 + (width / 2) * cos(end_angle_rad) - self.end_image.width() / 2)
        end_y = int(size / 2 + (height / 2) * sin(end_angle_rad) - self.end_image.height() / 2)
        paint.drawImage(QRect(end_x, end_y, self.end_image.width(), self.end_image.height()), self.end_image)

        paint.end()



