import sys
import csv
import json
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QStackedWidget, QMessageBox, QVBoxLayout, QWidget, QPushButton, QLabel, QTableWidget, QTableWidgetItem
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
                user_id = user.get("id")  # Get the user ID from the user data
                if user_id is not None:

                    self.goto_dashboard(user_id)  # Navigate to dashboard after successful login
                    return
                else:

                    self.show_error_message("User ID not found")
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

class SchedulePage(QDialog):
    def __init__(self, user_id):
        super(SchedulePage, self).__init__()
        self.user_id = user_id
        loadUi("schedule.ui", self)
        self.load_schedule()
        self.logoutButton.clicked.connect(self.logout)

    def load_schedule(self):
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

        # Access the QTableWidget
        table_widget = self.findChild(QTableWidget, "tableWidget")

        # Add courses to the schedule
        for course in courses:
            if int(course['course_id']) in registered_courses:
                time_slots = self.get_time_slots(course['time'])
                day_indices = self.get_day_indices(course['days'])
                if time_slots and day_indices:
                    course_info = f"{course['course_name']}\n{course['location']}\n{course['instructor']}"
                    for time_slot in time_slots:
                        for day_index in day_indices:
                            table_widget.setItem(time_slot, day_index, QTableWidgetItem(course_info))


    def get_time_slots(self, time_str):
        # Map course times to table rows (time slots)
        time_mapping = {
            "MWF 9-11 AM": [2, 3, 4],  # Example for a course spanning multiple hours
            "MWF 9-10 AM": [2, 3],
            "MWF 11-12 AM": [4, 5],
            "TT 2-3:30 PM": [7, 8],
            # Add other mappings as necessary
        }
        return time_mapping.get(time_str, [])

    def get_day_indices(self, day_str):
        # Map course days to table columns
        day_mapping = {
            "M": [1],
            "T": [2],
            "W": [3],
            "R": [4],
            "F": [5],
            "MWF": [1, 3, 5],  # Monday, Wednesday, Friday
            "TT": [2, 4],      # Tuesday, Thursday
            # Add other mappings as necessary
        }
        return day_mapping.get(day_str, [])

    def logout(self):
        login_page = Login()
        widget.addWidget(login_page)
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
        schedule_page = SchedulePage(self.user_id)
        widget.addWidget(schedule_page)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def goto_courses(self):
        courses_page = CoursesPage(self.user_id)
        widget.addWidget(courses_page)
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
                f"Time: {course['time']} | Days: {course['days']}",
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
        QMessageBox.information(self, "Add Course", f"{course_name} added to your schedule")

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



app = QApplication(sys.argv)
widget = QStackedWidget()

mainWindow = Login()
widget.addWidget(mainWindow)
widget.setFixedHeight(490)
widget.setFixedWidth(750)
widget.show()

try:
    sys.exit(app.exec_())
except:
    print("Exiting")