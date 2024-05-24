import sys
import csv
import json
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import (
    QDialog, QApplication, QStackedWidget, QMessageBox, QVBoxLayout, QWidget,
    QPushButton, QLabel, QTableWidget, QTableWidgetItem
)
from PyQt5.uic import loadUi
from collections import defaultdict, deque

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

        for user in users:
            if user["email"] == email and user["password"] == password:
                user_id = user.get("id")
                if user_id is not None:
                    self.goto_dashboard(user_id)
                    return
                else:
                    self.show_error_message("User ID not found")
                    return

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
        self.backButton.clicked.connect(self.goto_dashboard)

    def load_schedule(self):
        try:
            with open("enrollments.json", "r") as file:
                enrollments_data = json.load(file)["users"]
        except FileNotFoundError:
            self.show_error_message("enrollments.json file not found")
            return
        except json.JSONDecodeError:
            self.show_error_message("Error parsing enrollments.json file")
            return

        registered_courses = set()
        for enrollment in enrollments_data:
            if enrollment["student_id"] == self.user_id:
                registered_courses.update(map(int, enrollment.get("current_courses", [])))

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

        table_widget = self.findChild(QTableWidget, "tableWidget")

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
        time_mapping = {
            "MWF 9-10 AM": [0],    # Representing the first time slot, index 0
            "MWF 10-11 AM": [1],
            "MWF 11-12 AM": [2],
            "MWF 1-2 PM": [3],
            "MWF 2-3 PM": [4],
            "TT 9-10:30 AM": [5],
            "TT 10:30-12 PM": [6],
            "TT 1-2:30 PM": [7],
            "TT 2:30-4 PM": [8],
            "TT 4-5:30 PM": [9],
        }
        return time_mapping.get(time_str, [])

    def get_day_indices(self, day_str):
        day_mapping = {
            "M": [0],  # Representing Monday, index 0
            "T": [1],  # Representing Tuesday, index 1
            "W": [2],  # Representing Wednesday, index 2
            "R": [3],  # Representing Thursday, index 3
            "F": [4],  # Representing Friday, index 4
            "MWF": [0, 2, 4],  # Representing Monday, Wednesday, and Friday
            "TT": [1, 3],  # Representing Tuesday and Thursday
        }
        return day_mapping.get(day_str, [])

    def logout(self):
        login_page = Login()
        widget.addWidget(login_page)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def goto_dashboard(self):
        dashboard = Dashboard(self.user_id)
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
        self.logoutButton.clicked.connect(self.goto_login)

    def goto_schedule(self):
        schedule_page = SchedulePage(self.user_id)
        widget.addWidget(schedule_page)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def goto_courses(self):
        courses_page = CoursesPage(self.user_id)
        widget.addWidget(courses_page)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def goto_login(self):
        login_page = Login()
        widget.addWidget(login_page)
        widget.setCurrentIndex(widget.currentIndex() + 1)

class CoursesPage(QDialog):
    def __init__(self, user_id):
        super(CoursesPage, self).__init__()
        self.user_id = user_id
        loadUi("courses.ui", self)
        self.load_courses()
        self.logoutButton.clicked.connect(self.logout)
        self.backButton.clicked.connect(self.goto_dashboard)

    def load_courses(self):
        try:
            with open("enrollments.json", "r") as file:
                enrollments_data = json.load(file)["users"]
        except FileNotFoundError:
            self.show_error_message("enrollments.json file not found")
            return
        except json.JSONDecodeError:
            self.show_error_message("Error parsing enrollments.json file")
            return

        completed_courses = set()
        current_courses = set()
        for enrollment in enrollments_data:
            if enrollment["student_id"] == self.user_id:
                completed_courses.update(map(int, enrollment.get("completed_courses", [])))
                current_courses.update(map(int, enrollment.get("current_courses", [])))

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

        # Create a mapping from course code to course ID
        course_code_to_id = {course['course_code']: int(course['course_id']) for course in courses}

        # Build the prerequisite graph
        prerequisite_graph = defaultdict(list)
        in_degree = defaultdict(int)
        for course in courses:
            course_id = int(course['course_id'])
            prerequisite_code = course["prerequisite"]
            if prerequisite_code:
                prerequisite_id = course_code_to_id.get(prerequisite_code)
                if prerequisite_id:
                    prerequisite_graph[prerequisite_id].append(course_id)
                    in_degree[course_id] += 1

        layout = self.findChild(QVBoxLayout, "verticalLayout")

        for course in courses:
            course_widget = QWidget()
            course_layout = QVBoxLayout(course_widget)
            course_label = QLabel(f"Course: {course['course_name']} ({course['course_code']})")
            course_label.setStyleSheet("color: white; font-size: 18pt;")
            course_layout.addWidget(course_label)

            course_details = [
                f"Section: {course['section']} | Session: {course['session']} | Subj: {course.get('subject', 'N/A')} | Units: {course['credits']}",
                f"Instructor: {course['instructor']} | Time: {course['time']} | Days: {course['days']}",
                f"Location: {course['location']} | Prerequisite: {course['prerequisite']}"
            ]
            for detail in course_details:
                detail_label = QLabel(detail)
                detail_label.setStyleSheet("color: white;")
                course_layout.addWidget(detail_label)

            add_button = QPushButton("Add Course")
            course_id = int(course["course_id"])

            if course_id in completed_courses:
                add_button.setEnabled(False)
                add_button.setText("Completed")
                add_button.setStyleSheet("background-color: blue; color: white;")
            elif course_id in current_courses:
                add_button.setEnabled(False)
                add_button.setText("Already Registered")
                add_button.setStyleSheet("background-color: grey; color: white;")
            else:
                prerequisite_code = course["prerequisite"]
                prerequisite_id = course_code_to_id.get(prerequisite_code)
                add_button.setStyleSheet("background-color: green; color: white;")
                add_button.clicked.connect(
                    lambda _, cid=course_id, prereq=prerequisite_id, c_time=course['time'], c_days=course['days']:
                    self.add_course(cid, prereq, c_time, c_days, prerequisite_graph, completed_courses, current_courses, in_degree)
                )

            course_layout.addWidget(add_button)
            layout.addWidget(course_widget)
            course_widget.setLayout(course_layout)

    def logout(self):
        login_page = Login()
        widget.addWidget(login_page)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def add_course(self, course_id, prerequisite_id, course_time, course_days, prerequisite_graph, completed_courses, current_courses, in_degree):
        if prerequisite_id and prerequisite_id not in completed_courses:
            QMessageBox.warning(self, "Add Course", "Prerequisite course not met. You cannot add this course.")
            return

        # Perform topological sort using Kahn's Algorithm
        topo_order = []
        zero_in_degree_queue = deque([course for course in prerequisite_graph if in_degree[course] == 0])

        while zero_in_degree_queue:
            current_course = zero_in_degree_queue.popleft()
            topo_order.append(current_course)
            for neighbor in prerequisite_graph[current_course]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    zero_in_degree_queue.append(neighbor)

        # Check if adding the course respects the topological order
        if course_id not in topo_order:
            QMessageBox.warning(self, "Add Course", "Adding this course violates the prerequisite structure.")
            return

        # Check for time conflicts with current courses
        if self.has_time_conflict(current_courses, course_time, course_days):
            QMessageBox.warning(self, "Add Course", "Time conflict detected. You cannot enroll in this course.")
            return

        try:
            with open("enrollments.json", "r") as file:
                enrollments_data = json.load(file)
        except FileNotFoundError:
            self.show_error_message("enrollments.json file not found")
            return
        except json.JSONDecodeError:
            self.show_error_message("Error parsing enrollments.json file")
            return

        for user in enrollments_data["users"]:
            if user["student_id"] == self.user_id:
                if course_id not in user["current_courses"]:
                    user["current_courses"].append(course_id)
                    QMessageBox.information(self, "Add Course", f"Course {course_id} added to your schedule")
                else:
                    QMessageBox.warning(self, "Add Course", f"Course {course_id} is already in your schedule")

        with open("enrollments.json", "w") as file:
            json.dump(enrollments_data, file, indent=4)

        # Refresh the page to update the course status
        self.load_courses()

    def has_time_conflict(self, current_courses, new_course_time, new_course_days):
        try:
            with open("courses.csv", "r") as file:
                reader = csv.DictReader(file)
                courses = {int(course['course_id']): course for course in reader}
        except FileNotFoundError:
            self.show_error_message("courses.csv file not found")
            return False
        except csv.Error:
            self.show_error_message("Error parsing courses.csv file")
            return False

        new_time_slots = self.get_time_slots(new_course_time)
        new_day_indices = self.get_day_indices(new_course_days)

        for course_id in current_courses:
            course = courses.get(course_id)
            if course:
                current_time_slots = self.get_time_slots(course['time'])
                current_day_indices = self.get_day_indices(course['days'])

                # Check if any time slots overlap
                if set(new_time_slots).intersection(current_time_slots) and set(new_day_indices).intersection(current_day_indices):
                    return True

        return False

    def get_time_slots(self, time_str):
        time_mapping = {
            "MWF 9-11 AM": [0, 1, 2],
            "MWF 9-10 AM": [0, 1],
            "MWF 11-12 AM": [2, 3],
            "TT 2-3:30 PM": [4, 5],
        }
        return time_mapping.get(time_str, [])

    def get_day_indices(self, day_str):
        day_mapping = {
            "M": [0],
            "T": [1],
            "W": [2],
            "R": [3],
            "F": [4],
            "MWF": [0, 2, 4],
            "TT": [1, 3],
        }
        return day_mapping.get(day_str, [])

    def show_error_message(self, message):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText(message)
        msg.setWindowTitle("Error")
        msg.exec_()

    def goto_dashboard(self):
        dashboard = Dashboard(self.user_id)
        widget.addWidget(dashboard)
        widget.setCurrentIndex(widget.currentIndex() + 1)



class CreateAcc(QDialog):
    def __init__(self):
        super(CreateAcc, self).__init__()
        loadUi("createacc.ui", self)

        # Connect the buttons to their respective functions
        self.signupbutton.clicked.connect(self.createaccfunction)

        # Use findChild to safely get the backtologinbutton if it exists
        self.backtologinbutton = self.findChild(QPushButton, "backtologinbutton")
        if self.backtologinbutton:
            self.backtologinbutton.clicked.connect(self.backto_login)
        else:
            print("Error: backtologinbutton not found in createacc.ui")

    def createaccfunction(self):
        email = self.email.text()
        password = self.password.text()
        confirm_password = self.confirmpass.text()

        if password != confirm_password:
            self.status_label.setText("Enter the same password in confirmation field")
            return

        try:
            with open("users.json", "r") as file:
                users_data = json.load(file)
        except FileNotFoundError:
            users_data = {"users": []}

        for user in users_data["users"]:
            if user["email"] == email:
                self.status_label.setText("User is already taken")
                return

        new_id = max((user["id"] for user in users_data["users"]), default=0) + 1
        users_data["users"].append({"id": new_id, "email": email, "password": password})

        with open("users.json", "w") as file:
            json.dump(users_data, file, indent=4)

        try:
            with open("enrollments.json", "r") as file:
                enrollments_data = json.load(file)
        except FileNotFoundError:
            enrollments_data = {"users": []}

        enrollments_data["users"].append({"student_id": new_id, "completed_courses": [], "current_courses": []})

        with open("enrollments.json", "w") as file:
            json.dump(enrollments_data, file, indent=4)

        self.status_label.setText(f"Successfully created account with email: {email}")
        login = Login()
        widget.addWidget(login)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def backto_login(self):
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
