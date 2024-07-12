from PyQt5.QtWidgets import QMessageBox

def show_message_box(message, title, icon):
    msg_box = QMessageBox()
    msg_box.setIcon(icon)
    msg_box.setText(message)
    msg_box.setWindowTitle(title)
    msg_box.setStandardButtons(QMessageBox.Ok)
    msg_box.exec_()
