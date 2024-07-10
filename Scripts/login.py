import sys,os,logging
from PyQt5 import QtWidgets
from PyQt5.uic import loadUi
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from config import handle_google_login
from main_file import MyMainWindow

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
        self.login_btn=self.findChild(QtWidgets.QAbstractButton,"login_btn")
        self.google_login_btn=self.findChild(QtWidgets.QPushButton,"google_btn")
        self.google_login_btn.clicked.connect(self.login_with_google)
        
        
        
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
                print("unable to log in as user not resgtred")
        except Exception as e:
            logging.error(f"Error retrieving profile information: {e}")

def main():
    app=QtWidgets.QApplication(sys.argv)
    win=LoginWindow()
    win.show()
    sys.exit(app.exec_())
    
if __name__=="__main__":
    main()