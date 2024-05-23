import sys
import csv
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
                self.goto_dashboard(user["id"])  # Pass user ID to the dashboard
                return

        # If no match found, show error message
        self.show_error_message("Wrong email or password")

    def gotocreate(self):
        createacc = CreateAcc()
        widget.addWidget(createacc)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def goto_dashboard(self, user_id):
        dashboard = Dashboard(user_id)
        widget.addWidget(dashboard)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def show_error_message(self, message):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText(message)
        msg.setWindowTitle("Error")
        msg.exec_()

class Dashboard(QDialog):
    def __init__(self, user_id):
        super(Dashboard, self).__init__()
        self.user_id = user_id
        loadUi("dashboard.ui", self)
        self.my_schedule.clicked.connect(self.goto_schedule)
        self.courses.clicked.connect(self.goto_courses)

    def goto_schedule(self):
        schedule_page = SchedulePage()
        widget.addWidget(schedule_page)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def goto_courses(self):
        courses_page = CoursesPage(self.user_id)
        widget.addWidget(courses_page)
        widget.setCurrentIndex(widget.currentIndex() + 1)

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

        # Add new user with a unique ID
        new_id = max((user["id"] for user in users_data["users"]), default=0) + 1
        users_data["users"].append({"id": new_id, "email": email, "password": password})

        # Save updated user data to users.json
        with open("users.json", "w") as file:
            json.dump(users_data, file, indent=4)

        # Add new user to enrollments.json
        try:
            with open("enrollments.json", "r") as file:
                enrollments_data = json.load(file)
        except FileNotFoundError:
            enrollments_data = {"users": []}

        enrollments_data["users"].append({"student_id": new_id, "course_ids": []})

        with open("enrollments.json", "w") as file:
            json.dump(enrollments_data, file, indent=4)

        self.status_label.setText(f"Successfully created account with email: {email}")
        login = Login()
        widget.addWidget(login)
        widget.setCurrentIndex(widget.currentIndex() + 1)

class CoursesPage(QDialog):
    def __init__(self, user_id):
        super(CoursesPage, self).__init__()
        self.user_id = user_id
        loadUi("courses.ui", self)
        self.load_courses()
        self.logoutButton.clicked.connect(self.logout)

    def load_courses(self):
        # Load enrollments from JSON file
        try:
            with open("enrollments.json", "r") as file:
                enrollments_data = json.load(file)["users"]
        except FileNotFoundError:
            self.show_error_message("enrollments.json file not found")
            return
        except json.JSONDecodeError:
            self.show_error_message("Error parsing enrollments.json file")
            return

        # Find the courses registered by the current user
        registered_courses = set()
        for enrollment in enrollments_data:
            if enrollment["student_id"] == self.user_id:
                registered_courses.update(enrollment["course_ids"])

        # Load courses from CSV file
        try:
            with open("courses.csv", "r") as file:
                reader = csv.DictReader(file)
                courses = list(reader)
        except FileNotFoundError:
            self.show_error_message("courses.csv file not found")
            return
        except csv.Error:
            self.show_error_message("Error parsing courses.csv file")
            return

        layout = self.findChild(QVBoxLayout, "verticalLayout")

        for course in courses:
            course_widget = QWidget()
            course_layout = QVBoxLayout(course_widget)
            course_label = QLabel(f"Course: {course['course_name']}")
            course_label.setStyleSheet("color: white; font-size: 18pt;")
            course_layout.addWidget(course_label)

            course_details = [
                f"Section: {course['section']} | Session: {course['session']} | Subtype: {course['subtype']}",
                f"Type: {course['type']} | Duration: {course['duration']}",
                f"Credits: {course['credits']} | Credit Type: {course['credit_type']}",
                f"Time: {course['time']}",
                f"Location: {course['location']}",
                f"Instructor: {course['instructor']}"
            ]

            for detail in course_details:
                detail_label = QLabel(detail)
                detail_label.setStyleSheet("color: white;")
                course_layout.addWidget(detail_label)

            add_button = QPushButton("Add")
            add_button.setEnabled(True)
            add_button.setStyleSheet("background-color: green; color: white;")

            if int(course['course_id']) in registered_courses:
                add_button.setEnabled(False)
                add_button.setText("Already Registered")
                add_button.setStyleSheet("background-color: grey; color: white;")

            add_button.clicked.connect(lambda _, cname=course["course_name"]: self.add_course(cname))
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
