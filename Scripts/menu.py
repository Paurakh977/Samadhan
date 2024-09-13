from PyQt5 import QtWidgets
import sys, os, weekly, daily, home, calandar, info
from PyQt5.uic import loadUi
from config import logout_user
import main_file


class MenuWindow(QtWidgets.QMainWindow):
    def __init__(self, history):
        self.username = None
        self.email = None
        self.history = history
        super().__init__()

        this_file_location = os.path.dirname(__file__)
        ui_file_location = os.path.abspath(
            os.path.join(this_file_location, "..", "UI", "menu_ui.ui")
        )
        loadUi(ui_file_location, self)
        self.setupUI()

    def setupUI(self):
        self.setWindowTitle("SAMADHAN")
        self.setGeometry(400, 100, 1400, 900)
        self.icon_name_widget.setHidden(True)

        # findingchild
        self.icon_name_widget = self.findChild(QtWidgets.QWidget, "icon_name_widget")
        self.stackWidget = self.findChild(QtWidgets.QStackedWidget, "stackedWidget")
        self.home_2 = self.findChild(QtWidgets.QPushButton, "home_2")
        self.home_1 = self.findChild(QtWidgets.QPushButton, "home_1")
        self.username_lbl = self.findChild(QtWidgets.QLabel, "username_lbl")
        self.logout_btn_2 = self.findChild(QtWidgets.QPushButton, "logout_2")
        self.logout_btn_1 = self.findChild(QtWidgets.QPushButton, "logout_1")
        self.back_1 = self.findChild(QtWidgets.QPushButton, "back_1")
        self.back_2 = self.findChild(QtWidgets.QPushButton, "back_2")

        # button connections

        self.logout_btn_2.clicked.connect(self.logout)
        self.logout_btn_1.clicked.connect(self.logout)

        self.back_1.clicked.connect(self.prev_win)
        self.back_2.clicked.connect(self.prev_win)

        # clearing stackwidget that were used during making this using qtdesginer
        while self.stackWidget.count() > 0:
            widget = self.stackWidget.widget(0)
            self.stackWidget.removeWidget(widget)

        # setting up the windows class
        self.homeWindow = home.HomeWindow()
        self.dailyWindow = daily.DailyWindow()
        self.weeklyWindow = weekly.WeeklyWindow()
        self.calandarWindow = calandar.CalanadarWindow()
        self.infoWindow = info.InfoWindow()

        self.stackWidget.addWidget(self.homeWindow)
        self.home_1.setChecked(True)
        self.home_2.setChecked(True)
        self.stackWidget.addWidget(self.dailyWindow)
        self.stackWidget.addWidget(self.weeklyWindow)
        self.stackWidget.addWidget(self.infoWindow)
        self.stackWidget.addWidget(self.calandarWindow)

    def logout(self):
        email = self.email
        logout_user(email)
        self.main_window = main_file.MyMainWindow()
        self.close()
        self.main_window.get_login_window()

    def prev_win(self):
        if self.history:
            last_page = self.history.pop()
            self.stackWidget.setCurrentIndex(last_page)


def main():
    app = QtWidgets.QApplication(sys.argv)
    win = MenuWindow()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
