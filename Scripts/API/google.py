import sys
import os
import logging
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Configure logging
logging.basicConfig(level=logging.DEBUG)


class GoogleLoginApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Google Login")
        self.setGeometry(100, 100, 300, 200)

        layout = QVBoxLayout()

        self.login_button = QPushButton("Login with Google", self)
        self.login_button.clicked.connect(self.login_with_google)
        layout.addWidget(self.login_button)

        self.result_label = QLabel("", self)
        layout.addWidget(self.result_label)

        self.setLayout(layout)

    def login_with_google(self):
        creds_file = os.path.join(os.path.dirname(__file__), "credentials.json")
        scopes = [
            "https://www.googleapis.com/auth/userinfo.profile",
            "https://www.googleapis.com/auth/userinfo.email",
            "openid",
        ]

        try:
            flow = InstalledAppFlow.from_client_secrets_file(creds_file, scopes)
            creds = flow.run_local_server(port=0)
        except Exception as e:
            logging.error(f"Error during authentication: {e}")
            self.result_label.setText("Authentication failed!")
            return

        try:
            # Use the credentials to build the People API service
            service = build("people", "v1", credentials=creds)
            profile = (
                service.people()
                .get(resourceName="people/me", personFields="names,emailAddresses")
                .execute()
            )

            # Retrieve the uaser's name and email
            name = profile.get("names", [{}])[0].get("displayName", "N/A")
            email = profile.get("emailAddresses", [{}])[0].get("value", "N/A")

            # Update the label with the user's name and email
            print(f"Name: {name}\nEmail: {email}")
        except Exception as e:
            logging.error(f"Error retrieving profile information: {e}")
            self.result_label.setText("Failed to retrieve profile information!")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = GoogleLoginApp()
    ex.show()
    sys.exit(app.exec_())
