import sys,os
from PyQt5 import QtWidgets
import login,signupp,menu,weekly,daily,home,calandar,info
from config import get_login_status

class MyMainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        self.history=list()
        
        super().__init__()
        
        #Getting windows here
        self.login_window=login.LoginWindow()
        self.signup_window=signupp.SignupWindow()
        self.menu_window=menu.MenuWindow(self.history)
        
        status,name,email=get_login_status()
        print(status,email)
        if status:
            self.get_menu(name,email)
        else:
            self.get_login_window()
            
                    
        #connections for login window
        self.login_window.go_to_signup.clicked.connect(self.get_signup_window)
        
        
        #connections for signup class
        self.signup_window.already_have_an_account.clicked.connect(self.get_login_window)
        
        #connections for the menu Window
        self.menu_window.home_2.clicked.connect(self.get_home)
        self.menu_window.home_1.clicked.connect(self.get_home)
        self.menu_window.Daily_2.clicked.connect(self.get_daily)
        self.menu_window.daily_1.clicked.connect(self.get_daily)
        self.menu_window.weekly_2.clicked.connect(self.get_weekly)
        self.menu_window.weekly_1.clicked.connect(self.get_weekly)
        self.menu_window.calendar_2.clicked.connect(self.get_calandar)
        self.menu_window.calendar_1.clicked.connect(self.get_calandar)
        self.menu_window.info_2.clicked.connect(self.get_info)
        self.menu_window.info_1.clicked.connect(self.get_info)

#methods for the connections to the page 
    def get_signup_window(self):
        self.signup_window.show()
        self.login_window.close()
        for line_edit in self.login_window.findChildren(QtWidgets.QLineEdit):
            line_edit.clear()

    def get_login_window(self):
        self.login_window.show()
        self.signup_window.close()
        for line_edit in self.signup_window.findChildren(QtWidgets.QLineEdit):
            line_edit.clear()
    
        for radio in self.signup_window.findChildren(QtWidgets.QRadioButton):
            if radio.isChecked():
                radio.setChecked(False) 
    
    def get_menu(self,name,email):
        self.menu_window.username=name
        self.menu_window.email=email
        self.menu_window.show()
        self.menu_window.username_lbl.setText(name.split()[0])
        self.login_window.close()
        
    def get_home(self):
        self.history.append(self.menu_window.stackWidget.currentIndex())
        self.menu_window.stackWidget.setCurrentWidget(self.menu_window.homeWindow)
        
    def get_daily(self):
        self.history.append(self.menu_window.stackWidget.currentIndex())
        self.menu_window.stackWidget.setCurrentWidget(self.menu_window.dailyWindow)

    def get_weekly(self):
        self.history.append(self.menu_window.stackWidget.currentIndex())
        self.menu_window.stackWidget.setCurrentWidget(self.menu_window.weeklyWindow)

    def get_calandar(self):
        self.history.append(self.menu_window.stackWidget.currentIndex())
        self.menu_window.stackWidget.setCurrentWidget(self.menu_window.calandarWindow)

    def get_info(self):
        self.history.append(self.menu_window.stackWidget.currentIndex())
        self.menu_window.stackWidget.setCurrentWidget(self.menu_window.infoWindow)
         
def main():
    app=QtWidgets.QApplication(sys.argv)
    win=MyMainWindow()
    sys.exit(app.exec_())
    
if __name__=="__main__":
    main()