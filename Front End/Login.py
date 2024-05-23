# import json
# from PyQt5.QtWidgets import QDialog, QMessageBox
# from PyQt5.uic import loadUi
# from .create_acc import CreateAcc
# from .dashboard import Dashboard
# from .utils import show_error_message
#
# class Login(QDialog):
#     def __init__(self):
#         super(Login, self).__init__()
#         loadUi("login.ui", self)
#         self.loginbutton.clicked.connect(self.loginfunction)
#         self.password.setEchoMode(QtWidgets.QLineEdit.Password)
#         self.createaccbutton.clicked.connect(self.gotocreate)
#
#     def loginfunction(self):
#         email = self.email.text()
#         password = self.password.text()
#
#         try:
#             with open("users.json", "r") as file:
#                 data = json.load(file)
#                 users = data["users"]
#         except FileNotFoundError:
#             show_error_message(self, "users.json file not found")
#             return
#         except json.JSONDecodeError:
#             show_error_message(self, "Error parsing users.json file")
#             return
#
#         for user in users:
#             if user["email"] == email and user["password"] == password:
#                 user_id = user.get("id")
#                 if user_id is not None:
#                     self.goto_dashboard(user_id)
#                     return
#                 else:
#                     show_error_message(self, "User ID not found")
#                     return
#
#         show_error_message(self, "Wrong email or password")
#
#     def gotocreate(self):
#         createacc = CreateAcc()
#         widget.addWidget(createacc)
#         widget.setCurrentIndex(widget.currentIndex() + 1)
#
#     def goto_dashboard(self, user_id):
#         dashboard = Dashboard(user_id)
#         widget.addWidget(dashboard)
#         widget.setCurrentIndex(widget.currentIndex() + 1)
