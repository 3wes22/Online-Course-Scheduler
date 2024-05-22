import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QStackedWidget, QMessageBox
from PyQt5.uic import loadUi

class Login(QDialog):
    def __init__(self):
        super(Login, self).__init__()
        loadUi("login.ui", self)
        self.loginbutton.clicked.connect(self.loginfunction)
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.createaccbutton.clicked.connect(self.gotocreate)

    def loginfunction(self):
        email = self.email.text()
        password = self.password.text()
        # Hardcoded credentials for validation
        valid_email = "test@example.com"
        valid_password = "password"

        if email == valid_email and password == valid_password:
            self.gotodummy()
        else:
            self.show_error_message("Wrong email or password")

    def gotodummy(self):
        dummy_page = DummyPage()
        widget.addWidget(dummy_page)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def gotocreate(self):
        createacc = CreateAcc()
        widget.addWidget(createacc)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def show_error_message(self, message):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText(message)
        msg.setWindowTitle("Error")
        msg.exec_()

class CreateAcc(QDialog):
    def __init__(self):
        super(CreateAcc, self).__init__()
        loadUi("createacc.ui", self)
        self.signupbutton.clicked.connect(self.createaccfunction)
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.confirmpass.setEchoMode(QtWidgets.QLineEdit.Password)

    def createaccfunction(self):
        email = self.email.text()
        if self.password.text() == self.confirmpass.text():
            password = self.password.text()
            print(f"Successfully created account with email: {email} and password: {password}")
            login = Login()
            widget.addWidget(login)
            widget.setCurrentIndex(widget.currentIndex() + 1)
        else:
            print("Passwords do not match!")

class DummyPage(QDialog):
    def __init__(self):
        super(DummyPage, self).__init__()
        loadUi("dummy.ui", self)
        self.logoutButton.clicked.connect(self.gotologin)

    def gotologin(self):
        widget.setCurrentIndex(0)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = QStackedWidget()

    login = Login()
    widget.addWidget(login)
    widget.setFixedWidth(480)
    widget.setFixedHeight(620)
    widget.show()

    sys.exit(app.exec_())
