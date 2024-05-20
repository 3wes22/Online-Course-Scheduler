from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Course Scheduler")
        self.setGeometry(100, 100, 600, 400)  # Set the window size

        # Create a central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Create a layout
        layout = QVBoxLayout()

        # Create a welcome label
        welcome_label = QLabel("Welcome to the Course Scheduler", self)
        welcome_label.setStyleSheet("font-size: 24px;")
        welcome_label.setAlignment(Qt.AlignCenter)

        # Create a button to start scheduling courses
        start_button = QPushButton("Start Scheduling", self)
        start_button.setStyleSheet("font-size: 18px; padding: 10px;")
        start_button.clicked.connect(self.on_start_button_click)

        # Add widgets to the layout
        layout.addWidget(welcome_label)
        layout.addWidget(start_button)

        # Set the layout to the central widget
        central_widget.setLayout(layout)

    def on_start_button_click(self):
        # Logic to start scheduling courses can be added here
        print("Start Scheduling button clicked")
