import sys
import json
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QStackedWidget, QMessageBox, QVBoxLayout, QWidget, QPushButton, QLabel
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

        # Load user credentials from JSON file
        try:
            with open("users.json", "r") as file:
                data = json.load(file)
                users = data["users"]
        except FileNotFoundError:
            self.show_error_message("users.json file not found")
            return
        except json.JSONDecodeError:
            self.show_error_message("Error parsing users.json file")
            return

        # Check if entered credentials match any user in the file
        for user in users:
            if user["email"] == email and user["password"] == password:
                self.gotocourses()
                return

        # If no match found, show error message
        self.show_error_message("Wrong email or password")

    def gotocourses(self):
        courses_page = CoursesPage()
        widget.addWidget(courses_page)
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


import json

import json

class CreateAcc(QDialog):
    def __init__(self):
        super(CreateAcc, self).__init__()
        loadUi("createacc.ui", self)
        self.signupbutton.clicked.connect(self.createaccfunction)
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.confirmpass.setEchoMode(QtWidgets.QLineEdit.Password)

    def createaccfunction(self):
        email = self.email.text()
        password = self.password.text()
        confirm_password = self.confirmpass.text()

        # Check if confirm password matches password
        if password != confirm_password:
            self.status_label.setText("Enter the same password in confirmation field")
            return

        # Load existing user data from users.json
        try:
            with open("users.json", "r") as file:
                users_data = json.load(file)
        except FileNotFoundError:
            users_data = {"users": []}

        # Check if the user already exists
        for user in users_data["users"]:
            if user["email"] == email:
                self.status_label.setText("User is already taken")
                return

        # Add new user
        users_data["users"].append({"email": email, "password": password})

        # Save updated user data to users.json
        with open("users.json", "w") as file:
            json.dump(users_data, file, indent=4)

        self.status_label.setText(f"Successfully created account with email: {email}")
        login = Login()
        widget.addWidget(login)
        widget.setCurrentIndex(widget.currentIndex() + 1)

class CoursesPage(QDialog):
    def __init__(self):
        super(CoursesPage, self).__init__()
        loadUi("courses.ui", self)
        self.load_courses()
        self.logoutButton.clicked.connect(self.logout)

    def load_courses(self):
        # Load courses from JSON file
        try:
            with open("courses.json", "r") as file:
                data = json.load(file)
                courses = data["courses"]
        except FileNotFoundError:
            self.show_error_message("courses.json file not found")
            return
        except json.JSONDecodeError:
            self.show_error_message("Error parsing courses.json file")
            return

        layout = self.findChild(QVBoxLayout, "verticalLayout")

        for course in courses:
            course_widget = QWidget()
            course_layout = QVBoxLayout(course_widget)
            course_label = QLabel(f"Course: {course['name']}")
            course_label.setStyleSheet("color: white; font-size: 18pt;")
            course_layout.addWidget(course_label)

            if course["registered"]:
                registered_label = QLabel("REGISTERED")
                registered_label.setStyleSheet("color: green; font-size: 14pt;")
                course_layout.addWidget(registered_label)

            details = [
                f"Section: {course['section']} | Session: {course['session']} | Subtype: {course['subtype']}",
                f"Type: {course['type']} | Duration: {course['duration']}",
                f"Credits: {course['credits']} | Credit Type: {course['credit_type']}",
                f"{course['time']}",
                f"{course['location']}",
                f"Instructor: {course['instructor']}"
            ]

            for detail in details:
                detail_label = QLabel(detail)
                detail_label.setStyleSheet("color: white;")
                course_layout.addWidget(detail_label)

            add_button = QPushButton("Add" if not course["registered"] else "Already Registered")
            add_button.setEnabled(not course["registered"])
            add_button.setStyleSheet(
                "background-color: green; color: white;" if not course["registered"]
                else "background-color: grey; color: white;"
            )
            if not course["registered"]:
                add_button.clicked.connect(lambda _, cname=course["name"]: self.add_course(cname))
            course_layout.addWidget(add_button)

            layout.addWidget(course_widget)
            course_widget.setLayout(course_layout)

    def logout(self):
        login_page = Login()
        widget.addWidget(login_page)
        widget.setCurrentIndex(widget.currentIndex() + 1)
    def add_course(self, course_name):
        print(f"Adding course: {course_name}")

    def show_error_message(self, message):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText(message)
        msg.setWindowTitle("Error")
        msg.exec_()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = QStackedWidget()

    login = Login()
    widget.addWidget(login)
    widget.setFixedWidth(480)
    widget.setFixedHeight(620)
    widget.show()

    sys.exit(app.exec_())
