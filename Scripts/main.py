import sys,os
from PyQt5 import QtWidgets
import login,signupp
class MyMainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.login_window=login.LoginWindow()
        self.signup_window=signupp.SignupWindow()
        
        self.login_window.show()
        
        self.login_window.go_to_signup.clicked.connect(self.get_signup_window)
        self.signup_window.already_have_an_account.clicked.connect(self.get_login_window)
        
        
    def get_signup_window(self):
        self.signup_window.show()
        self.login_window.close()
    
    def get_login_window(self):
        self.login_window.show()
        self.signup_window.close()

def main():
    app=QtWidgets.QApplication(sys.argv)
    win=MyMainWindow()
    sys.exit(app.exec_())
    
if __name__=="__main__":
    main()