import sys
import webbrowser
import requests
from flask import Flask, request
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel
from PyQt5.QtCore import QThread, pyqtSignal, QObject

# Flask application setup
app = Flask(__name__)
app.secret_key = '6a0cc1c6ba2bf2304d9f0bc36d825456'  # Your secret key here

# Facebook app details (replace with your actual client ID and secret)
client_id = '1642745376490841'
client_secret = '6a0cc1c6ba2bf2304d9f0bc36d825456'
redirect_uri = 'http://localhost:5000/callback'
scope = 'email'

# Custom signal class
class SignalEmitter(QObject):
    window_closed = pyqtSignal()

# PyQt5 application window
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Facebook OAuth Login')
        self.setGeometry(100, 100, 400, 200)

        layout = QVBoxLayout()

        self.label = QLabel('Click below to login with Facebook')
        layout.addWidget(self.label)

        self.login_button = QPushButton('Login with Facebook')
        self.login_button.clicked.connect(self.login_with_facebook)
        layout.addWidget(self.login_button)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def login_with_facebook(self):
        auth_url = f'https://www.facebook.com/v20.0/dialog/oauth?client_id={client_id}&redirect_uri={redirect_uri}&scope={scope}'
        webbrowser.open(auth_url)

    def closeEvent(self, event):
        self.signal_emitter.window_closed.emit()  # Emit the custom signal when window is closed
        event.accept()

# Flask routes
@app.route('/')
def index():
    return 'Hello, World!'

@app.route('/callback')
def callback():
    error = request.args.get('error')
    if error:
        return f'Error: {error}'

    code = request.args.get('code')

    # Exchange code for access token
    token_url = 'https://graph.facebook.com/v20.0/oauth/access_token'
    params = {
        'client_id': client_id,
        'client_secret': client_secret,
        'code': code,
        'redirect_uri': redirect_uri
    }

    response = requests.get(token_url, params=params)
    data = response.json()

    access_token = data['access_token']

    # Get user's name and email
    graph_url = f'https://graph.facebook.com/me?fields=name,email&access_token={access_token}'
    user_response = requests.get(graph_url)
    user_data = user_response.json()

    # Update GUI with user info
    main_window.label.setText(f"Hello, {user_data['name']}. Your email is: {user_data['email']}")

    # Shutdown Flask server
    shutdown_server()

    return 'Login successful! You can now close this window.'

def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func:
        func()

if __name__ == '__main__':
    # Start Flask in a separate thread
    server_thread = QThread()
    server_thread.run = lambda: app.run(debug=False)
    server_thread.start()

    # Start PyQt5 application
    app = QApplication(sys.argv)
    signal_emitter = SignalEmitter()  # Create an instance of the custom signal emitter
    main_window = MainWindow()
    main_window.signal_emitter = signal_emitter  # Assign the signal emitter to main_window
    signal_emitter.window_closed.connect(shutdown_server)  # Connect window_closed signal to shutdown_server
    main_window.show()
    sys.exit(app.exec_())
