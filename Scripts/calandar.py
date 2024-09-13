import sys
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QFont


class CalanadarWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.setGeometry(800, 800, 500, 500)
        self.setWindowTitle("Home")
        self.setup_UI()

    def setup_UI(self):
        self.centralwidget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.centralwidget)
        self.central_layout = QtWidgets.QHBoxLayout(self.centralwidget)

        self.frame_1 = QtWidgets.QFrame(self.centralwidget)
        self.central_layout.addWidget(self.frame_1)

        self.frame_1_layout = QtWidgets.QVBoxLayout(self.frame_1)

        self.frame_1.setStyleSheet(
            "QFrame { background-color: #e9f0ea; border: 4px solid #000; }"
        )

        self.label1 = QtWidgets.QLabel(self.frame_1)
        self.label1.setText("THIS IS CALANDAR PAGE")

        font = QFont()
        font.setPointSize(22)  # Set the point size before setting the font
        self.label1.setFont(font)  # Apply the font with the specified point size

        self.label1.setAlignment(QtCore.Qt.AlignCenter)  # Align text to center

        self.frame_1_layout.addWidget(self.label1)


def main():
    app = QtWidgets.QApplication(sys.argv)
    win = CalanadarWindow()
    win.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
