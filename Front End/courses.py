# import csv
# import json
# from PyQt5.QtWidgets import QDialog, QVBoxLayout, QWidget, QLabel, QPushButton, QMessageBox
# from PyQt5.uic import loadUi
# from utils import show_error_message
#
# class CoursesPage(QDialog):
#     def __init__(self, user_id):
#         super(CoursesPage, self).__init__()
#         self.user_id = user_id
#         loadUi("courses.ui", self)
#         self.load_courses()
#         self.logoutButton.clicked.connect(self.logout)
#
#     def load_courses(self):
#         try:
#             with open("../enrollments.json", "r") as file:
#                 enrollments_data = json.load(file)["users"]
#         except FileNotFoundError:
#             show_error_message(self, "enrollments.json file not found")
#             return
#         except json.JSONDecodeError:
#             show_error_message(self, "Error parsing enrollments.json file")
#             return
#
#         registered_courses = set()
#         for enrollment in enrollments_data:
#             if enrollment["student_id"] == self.user_id:
#                 registered_courses.update(enrollment["course_ids"])
#
#         try:
#             with open("../courses.csv", "r") as file:
#                 reader = csv.DictReader(file)
#                 courses = list(reader)
#         except FileNotFoundError:
#             show_error_message(self, "courses.csv file not found")
#             return
#         except csv.Error:
#             show_error_message(self, "Error parsing courses.csv file")
#             return
#
#         layout = self.findChild(QVBoxLayout, "verticalLayout")
#
#         for course in courses:
#             course_widget = QWidget()
#             course_layout = QVBoxLayout(course_widget)
#             course_label = QLabel(f"Course: {course['course_name']}")
#             course_label.setStyleSheet("color: white; font-size: 18pt;")
#             course_layout.addWidget(course_label)
#
#             course_details = [
#                 f"Section: {course['section']} | Session: {course['session']} | Subtype: {course['subtype']}",
#                 f"Type: {course['type']} | Duration: {course['duration']}",
#                 f"Credits: {course['credits']} | Credit Type: {course['credit_type']}",
#                 f"Time: {course['time']} | Days: {course['days']}",
#                 f"Location: {course['location']}",
#                 f"Instructor: {course['instructor']}"
#             ]
#
#             for detail in course_details:
#                 detail_label = QLabel(detail)
#                 detail_label.setStyleSheet("color: white;")
#                 course_layout.addWidget(detail_label)
#
#             add_button = QPushButton("Add")
#             add_button.setEnabled(True)
#             add_button.setStyleSheet("background-color: green; color: white;")
#
#             if int(course['course_id']) in registered_courses:
#                 add_button.setEnabled(False)
#                 add_button.setText("Already Registered")
#                 add_button.setStyleSheet("background-color: grey; color: white;")
#
#             add_button.clicked.connect(lambda _, cname=course["course_name"]: self.add_course(cname))
#             course_layout.addWidget(add_button)
#
#             layout.addWidget(course_widget)
#             course_widget.setLayout(course_layout)
#
#     def logout(self):
#         login_page = Login()
#         widget.addWidget(login_page)
#         widget.setCurrentIndex(widget.currentIndex() + 1)
#
#     def add_course(self, course_name):
#         QMessageBox.information(self, "Add Course", f"{course_name} added to your schedule")
