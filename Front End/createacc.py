# import json
# from PyQt5.QtWidgets import QDialog
# from PyQt5.uic import loadUi
# from .login import Login
# from .utils import show_error_message
#
# class CreateAcc(QDialog):
#     def __init__(self):
#         super(CreateAcc, self).__init__()
#         loadUi("createacc.ui", self)
#         self.signupbutton.clicked.connect(self.createaccfunction)
#         self.password.setEchoMode(QtWidgets.QLineEdit.Password)
#         self.confirmpass.setEchoMode(QtWidgets.QLineEdit.Password)
#
#     def createaccfunction(self):
#         email = self.email.text()
#         password = self.password.text()
#         confirm_password = self.confirmpass.text()
#
#         if password != confirm_password:
#             self.status_label.setText("Enter the same password in confirmation field")
#             return
#
#         try:
#             with open("users.json", "r") as file:
#                 users_data = json.load(file)
#         except FileNotFoundError:
#             users_data = {"users": []}
#
#         for user in users_data["users"]:
#             if user["email"] == email:
#                 self.status_label.setText("User is already taken")
#                 return
#
#         new_id = max((user["id"] for user in users_data["users"]), default=0) + 1
#         users_data["users"].append({"id": new_id, "email": email, "password": password})
#
#         with open("users.json", "w") as file:
#             json.dump(users_data, file, indent=4)
#
#         try:
#             with open("enrollments.json", "r") as file:
#                 enrollments_data = json.load(file)
#         except FileNotFoundError:
#             enrollments_data = {"users": []}
#
#         enrollments_data["users"].append({"student_id": new_id, "course_ids": []})
#
#         with open("enrollments.json", "w") as file:
#             json.dump(enrollments_data, file, indent=4)
#
#         self.status_label.setText(f"Successfully created account with email: {email}")
#         login = Login()
#         widget.addWidget(login)
#         widget.setCurrentIndex(widget.currentIndex() + 1)
