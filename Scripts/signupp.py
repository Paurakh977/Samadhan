import sys,os,logging
from PyQt5 import QtWidgets
from PyQt5.uic import loadUi
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from config import insert_user
import main_file
from serial_id import get_serial_number
from hash import hash_password
from config import insert_manual_users
from msg_box import show_message_box
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
        
        
        
        #finding child
        self.already_have_an_account=self.findChild(QtWidgets.QPushButton,"signup_btn")
        self.google_login_btn=self.findChild(QtWidgets.QPushButton,"google_btn")
        
        self.name_line_edit=self.findChild(QtWidgets.QLineEdit,"name_line_edit")
        self.ph_nmbr_line_edit=self.findChild(QtWidgets.QLineEdit,"ph_nmbr_line_edit")
        self.email_line_edit=self.findChild(QtWidgets.QLineEdit,"email_line_edit")
        self.pswrd_line_edit=self.findChild(QtWidgets.QLineEdit,"pswrd_line_edit")
        
        self.sign_in_btn=self.findChild(QtWidgets.QPushButton,"sign_in_btn")
        self.sign_in_btn.clicked.connect(self.signup_manual)
        
        self.google_login_btn.clicked.connect(self.signup_with_google)
     
    def signup_manual(self):
        name = self.name_line_edit.text()
        ph_nmbr = self.ph_nmbr_line_edit.text()
        email = self.email_line_edit.text()
        password = self.pswrd_line_edit.text()
        
        radio = None
        for radio_btn in self.findChildren(QtWidgets.QRadioButton):
            if radio_btn.isChecked():
                radio = radio_btn.text()  
                break
        
        if name and ph_nmbr and email and password and radio:
            hashed_password = hash_password(password)
            serial_id = get_serial_number()
            response=insert_manual_users(name, email, ph_nmbr, hashed_password, serial_id, radio)
            if not response:
                show_message_box("User with this Email already Exists\nPlease try Again with another email","User Already Exists",QtWidgets.QMessageBox.Information)
                for line_edit in self.findChildren(QtWidgets.QLineEdit):
                    line_edit.clear()
            else:
                self.main_window=main_file.MyMainWindow()
                self.close()
                self.main_window.get_login_window()

        else:
            show_message_box("Please Fill Every Feild to Proceed","Incomplete Form",QtWidgets.QMessageBox.Critical)
            
    
    
    def signup_with_google(self):
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
            serial_id=get_serial_number()
            status=insert_user(name, email,serial_id)
            if status:
                show_message_box("Signed up successfully\nYou can Login Now","Signup Successful",QtWidgets.QMessageBox.NoIcon)
            else:
                show_message_box("There is already an account associated with the chosen google account\nPlease Try Again using another Google Account","User Already Exists",QtWidgets.QMessageBox.Information)
        except Exception as e:
            logging.error(f"Error retrieving profile information: {e}")
    
    

def main():
    app=QtWidgets.QApplication(sys.argv)
    win=SignupWindow()
    win.show()
    sys.exit(app.exec_())
    
if __name__=="__main__":
    main()