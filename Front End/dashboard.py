# from PyQt5.QtWidgets import QDialog
# from PyQt5.uic import loadUi
# from Schedule_page import SchedulePage
# from Courses_page import CoursesPage
#
# class Dashboard(QDialog):
#     def __init__(self, user_id):
#         super(Dashboard, self).__init__()
#         self.user_id = user_id
#         loadUi("dashboard.ui", self)
#         self.my_schedule.clicked.connect(self.goto_schedule)
#         self.courses.clicked.connect(self.goto_courses)
#
#     def goto_schedule(self):
#         schedule_page = SchedulePage(self.user_id)
#         widget.addWidget(schedule_page)
#         widget.setCurrentIndex(widget.currentIndex() + 1)
#
#     def goto_courses(self):
#         courses_page = CoursesPage(self.user_id)
#         widget.addWidget(courses_page)
#         widget.setCurrentIndex(widget.currentIndex() + 1)
