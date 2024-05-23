# import csv
# import json
# from PyQt5.QtWidgets import QDialog, QTableWidget, QTableWidgetItem, QMessageBox
# from PyQt5.uic import loadUi
# from utils import show_error_message
#
# class SchedulePage(QDialog):
#     def __init__(self, user_id):
#         super(SchedulePage, self).__init__()
#         self.user_id = user_id
#         loadUi("schedule.ui", self)
#         self.load_schedule()
#         self.logoutButton.clicked.connect(self.logout)
#
#     def load_schedule(self):
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
#         table_widget = self.findChild(QTableWidget, "tableWidget")
#
#         for course in courses:
#             if int(course['course_id']) in registered_courses:
#                 time_slots = self.get_time_slots(course['time'])
#                 day_indices = self.get_day_indices(course['days'])
#                 if time_slots and day_indices:
#                     course_info = f"{course['course_name']}\n{course['location']}\n{course['instructor']}"
#                     for time_slot in time_slots:
#                         for day_index in day_indices:
#                             table_widget.setItem(time_slot, day_index, QTableWidgetItem(course_info))
#
#     def get_time_slots(self, time_str):
#         time_mapping = {
#             "MWF 9-11 AM": [2, 3, 4],
#             "MWF 9-10 AM": [2, 3],
#             "MWF 11-12 AM": [4, 5],
#             "TT 2-3:30 PM": [7, 8],
#         }
#         return time_mapping.get(time_str, [])
#
#     def get_day_indices(self, day_str):
#         day_mapping = {
#             "M": [1],
#             "T": [2],
#             "W": [3],
#             "R": [4],
#             "F": [5],
#             "MWF": [1, 3, 5],
#             "TT": [2, 4],
#         }
#         return day_mapping.get(day_str, [])
#
#     def logout(self):
#         login_page = Login()
#         widget.addWidget(login_page)
#         widget.setCurrentIndex(widget.currentIndex() + 1)
