import sys, os
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QFont
from PyQt5.uic import loadUi
from stack_bar import StackedBarGraph
from circular_progress_bar import CircularProgress, get_angle, calculate_time_difference


class HomeWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.setGeometry(800, 800, 500, 500)
        self.setWindowTitle("Home")

        this_file_location = os.path.dirname(__file__)
        ui_file_location = os.path.abspath(
            os.path.join(this_file_location, "..", "UI", "home.ui")
        )
        loadUi(ui_file_location, self)

        # finding child
        self.circular_bar_frame = self.findChild(QtWidgets.QFrame, "circular_bar_frame")
        self.frame_3 = self.findChild(QtWidgets.QFrame, "frame_3")
        self.stack_bar_frame = self.findChild(QtWidgets.QFrame, "stack_bar_frame")
        self.strt_lbl = self.findChild(QtWidgets.QLabel, "strt_lbl")
        self.end_lbl = self.findChild(QtWidgets.QLabel, "end_lbl")

        # setting layouts for the frames
        self.stack_bar_frame_layout = QtWidgets.QGridLayout(self.stack_bar_frame)
        self.circular_bar_frame_layout = QtWidgets.QVBoxLayout(self.circular_bar_frame)

        # Adding the StackedBarGraph widget to the stack_bar_frame
        self.stack_bar_graph = StackedBarGraph(self.stack_bar_frame)
        self.stack_bar_frame_layout.addWidget(self.stack_bar_graph)

        # collecting params for iniitialzin ciruclar progressbar
        start_hour = 6
        start_minute = 47
        start_period = "AM"

        end_hour = 4
        end_minute = 28
        end_period = "PM"
        start_angle = get_angle(start_hour, start_minute)
        end_angle = get_angle(end_hour, end_minute)

        time_difference = calculate_time_difference(
            start_hour, start_minute, start_period, end_hour, end_minute, end_period
        )
        # initialziin  circular progress bar
        self.progress_bar = CircularProgress(start_angle, end_angle, time_difference)
        self.circular_bar_frame_layout.addWidget(
            self.progress_bar, QtCore.Qt.AlignCenter, QtCore.Qt.AlignCenter
        )
        self.strt_lbl.setText(f"{start_hour}:{start_minute} {start_period}")
        self.end_lbl.setText(f"{end_hour}:{end_minute} {end_period}")


def main():
    app = QtWidgets.QApplication(sys.argv)
    win = HomeWindow()
    win.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
