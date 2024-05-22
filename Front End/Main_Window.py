# from PyQt5.QtCore import Qt
# from PyQt5.QtWidgets import QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget, QApplication
#
# class MainWindow(QMainWindow):
#     def __init__(self):
#         super().__init__()
#
#         self.setWindowTitle("Course Scheduler")
#         self.setGeometry(100, 100, 600, 400)  # Set the window size
#
#         # Create a central widget
#         central_widget = QWidget()
#         self.setCentralWidget(central_widget)
#
#         # Create a layout
#         layout = QVBoxLayout()
#
#         # Create a welcome label
#         welcome_label = QLabel("Welcome to the Course Scheduler", self)
#         welcome_label.setStyleSheet("font-size: 24px;")
#         welcome_label.setAlignment(Qt.AlignCenter)
#
#         # Create a button to start scheduling courses
#         start_button = QPushButton("Start Scheduling", self)
#         start_button.setStyleSheet("font-size: 18px; padding: 10px;")
#         start_button.clicked.connect(self.on_start_button_click)
#
#         # Add widgets to the layout
#         layout.addWidget(welcome_label)
#         layout.addWidget(start_button)
#
#         # Set the layout to the central widget
#         central_widget.setLayout(layout)
#
#         self.new_window = None
#
#     def on_start_button_click(self):
#         self.new_window = AnotherWindow(self)
#         self.new_window.show()
#         self.hide()  # Hide the main window
#
#
# class AnotherWindow(QWidget):
#     def __init__(self, parent=None):
#         super().__init__(parent)
#         self.setWindowTitle("Another Window")
#         self.setGeometry(200, 200, 400, 300)
#
#         # Create a button to close this window and show the main window again
#         back_button = QPushButton("Back to Main Window", self)
#         back_button.clicked.connect(self.show_main_window)
#
#         # Layout
#         layout = QVBoxLayout()
#         layout.addWidget(back_button)
#         self.setLayout(layout)
#
#     def show_main_window(self):
#         self.parent().show()  # Show the main window
#         self.close()  # Close the current window
#
# if __name__ == "__main__":
#     import sys
#     app = QApplication(sys.argv)
#     window = MainWindow()
#     window.show()
#     sys.exit(app.exec_())
