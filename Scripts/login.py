import sys,os,logging
from PyQt5 import QtWidgets
from PyQt5.uic import loadUi
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from config import handle_google_login,handel_manual_login
from main_file import MyMainWindow
from hash import check_password,hash_password
from serial_id import get_serial_number
from msg_box import show_message_box


class LoginWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        this_file_location=os.path.dirname(__file__)
        ui_file_location=os.path.abspath(os.path.join(this_file_location,"..","UI","Login.ui"))
        
        loadUi(ui_file_location,self)
        self.setupUI()
        
        
    def setupUI(self):
        self.setGeometry(600,200,600,800)
        self.setWindowTitle("SAMADHAN")
        
        self.go_to_signup=self.findChild(QtWidgets.QPushButton,"signup_btn")
        self.fb_btn=self.findChild(QtWidgets.QPushButton,"fb_btn")
        self.login_btn=self.findChild(QtWidgets.QAbstractButton,"login_btn")
        self.google_login_btn=self.findChild(QtWidgets.QPushButton,"google_btn")
        
        #connections
        self.google_login_btn.clicked.connect(self.login_with_google)
        self.login_btn.clicked.connect(self.login_manual_user)
        self.fb_btn.clicked.connect(lambda:show_message_box("Unable to Connect to Server!\nPlease Try Again Later","Server Error",QtWidgets.QMessageBox.Warning))
        
    def login_manual_user(self):
        email = self.email_line_edit.text()
        password = self.pswrd_line_edit.text()
        hashed_password = hash_password(password)
        
        if email and password:
            serial_id = get_serial_number()
            status, name = handel_manual_login(email, hashed_password, serial_id)
            if status:
                self.close()
                self.main_window = MyMainWindow()
                self.main_window.get_menu(name=name, email=email)
            else:
                for line_edit in self.findChildren(QtWidgets.QLineEdit):
                    line_edit.clear()
                show_message_box("Invalid Credentials.\nPlease Try Again","Invalid Credentials",QtWidgets.QMessageBox.Warning)
        else:
            show_message_box("Email and Password must be Provided","Incomplete Form",QtWidgets.QMessageBox.Critical)
            
    def login_with_google(self):
        creds_file = os.path.join(os.path.dirname(__file__),"API", 'credentials.json')
        scopes = ['https://www.googleapis.com/auth/userinfo.profile', 'https://www.googleapis.com/auth/userinfo.email', 'openid']

        try:
            flow = InstalledAppFlow.from_client_secrets_file(creds_file, scopes)
            creds = flow.run_local_server(port=0)
        except Exception as e:
            logging.error(f"Error during authentication: {e}")
            return

        try:
            service = build('people', 'v1', credentials=creds)
            profile = service.people().get(resourceName='people/me', personFields='names,emailAddresses').execute()

            name = profile.get('names', [{}])[0].get('displayName', 'N/A')
            email = profile.get('emailAddresses', [{}])[0].get('value', 'N/A')
            status=handle_google_login(email)
            if(status):
                self.close()
                self.main_window=MyMainWindow()
                self.main_window.get_menu(name=name,email=email)
            else:
                show_message_box("User not Registered\nPlease Signup First","User Not Found",QtWidgets.QMessageBox.Information)

        except Exception as e:
            logging.error(f"Error retrieving profile information: {e}")

def main():
    app=QtWidgets.QApplication(sys.argv)
    win=LoginWindow()
    win.show()
    sys.exit(app.exec_())
    
if __name__=="__main__":
    main()