from PyQt5.QtWidgets import QMessageBox

def show_error_message(parent, message):
    msg = QMessageBox(parent)
    msg.setIcon(QMessageBox.Critical)
    msg.setText(message)
    msg.setWindowTitle("Error")
    msg.exec_()
