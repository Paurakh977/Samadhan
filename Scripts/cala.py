from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QCalendarWidget,
    QVBoxLayout,
    QWidget,
)
from PyQt5.QtCore import Qt, QDate
import sys


class StyledCalendar(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Styled Calendar")
        self.setGeometry(100, 100, 400, 300)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)

        calendar = QCalendarWidget(self)

        # Set the date to July 14, 2024
        calendar.setSelectedDate(QDate(2024, 7, 14))

        # Custom Stylesheet
        calendar.setStyleSheet("""
            QCalendarWidget QWidget {
                background-color: white;
                alternate-background-color: #fff;
                
            }
            QCalendarWidget QToolButton {
                height: 35px;
                width: 100px;
                color: black;
                font-size: 18px;
                icon-size: 18px, 18px;
                background-color: white;
                qproperty-icon: none;
            }
            QCalendarWidget QToolButton#qt_calendar_prevmonth, 
            QCalendarWidget QToolButton#qt_calendar_nextmonth {
                color: black;
                background-color: white;
            }
            QCalendarWidget QToolButton#qt_calendar_prevmonth {
                qproperty-icon: url(left-arrow.png);
            }
            QCalendarWidget QToolButton#qt_calendar_nextmonth {
                qproperty-icon: url(right-arrow.png);
            }
            QCalendarWidget QMenu {
                width: 100px;
                left: 10px;
                color: black;
                font-size: 18px;
                background-color: white;
            }
            QCalendarWidget QSpinBox { 
                width: 100px; 
                font-size: 18px; 
                color: black; 
                background: white;
                selection-background-color: gray;
                selection-color: white;
            }
            QCalendarWidget QSpinBox::up-button { subcontrol-origin: border; subcontrol-position: top right; }
            QCalendarWidget QSpinBox::down-button { subcontrol-origin: border; subcontrol-position: bottom right; }
            QCalendarWidget QSpinBox::up-arrow { width: 15px; height: 15px; }
            QCalendarWidget QSpinBox::down-arrow { width: 15px; height: 15px; }
            QCalendarWidget QAbstractItemView:enabled {
                font-size: 18px;  
                color: black;  
                background-color: white;  
                selection-background-color: blue;  
                selection-color: white;  
                border-radius: 10px; 
            }
            QCalendarWidget QAbstractItemView:disabled { color: gray; }
            QCalendarWidget QAbstractItemView:selection {
                color: white;
                background-color: blue;
                border-radius: 10px;
            }
            QCalendarWidget QAbstractItemView:horizontal {
                font-size: 18px;
            }
            QCalendarWidget QAbstractItemView:vertical {
                font-size: 18px;
            }
            QCalendarWidget QAbstractItemView QHeaderView::section {
                background-color: white;
                color: black;
                font-size: 18px;
            }
            QCalendarWidget QWidget#qt_calendar_calendarview {
                border: 1px solid #ccc;
                background-color: white;
            }
            QCalendarWidget QAbstractItemView:enabled:nth-child(7) { /* Saturday */
                color: blue;
            }
            QCalendarWidget QAbstractItemView:enabled:nth-child(1) { /* Sunday */
                color: red;
            }
        """)

        layout.addWidget(calendar)
        central_widget.setLayout(layout)

        self.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = StyledCalendar()
    sys.exit(app.exec_())
