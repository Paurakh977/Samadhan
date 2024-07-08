import sys,os
from PyQt5 import QtWidgets
from PyQt5.uic import loadUi
import login

class SignupWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        
        this_file_location=os.path.dirname(__file__)
        ui_file_location=os.path.abspath(os.path.join(this_file_location,"..","UI","signup.ui"))
        
        loadUi(ui_file_location,self)
        self.setupUI()
        
    def setupUI(self):
        self.setGeometry(600,200,600,800)
        self.setWindowTitle("SAMADHAN")
        self.login_window=login.LoginWindow()
        self.already_have_an_account=self.findChild(QtWidgets.QPushButton,"signup_btn")
        self.google_login_btn=self.findChild(QtWidgets.QPushButton,"google_btn")
        self.google_login_btn.clicked.connect(self.login_window.login_with_google)
    

def main():
    app=QtWidgets.QApplication(sys.argv)
    win=SignupWindow()
    win.show()
    sys.exit(app.exec_())
    
if __name__=="__main__":
    main()