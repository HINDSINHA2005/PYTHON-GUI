import sqlite3
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox
from PyQt5.QtGui import QPalette, QColor

class AdminPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Admin Panel")
        self.setGeometry(300, 300, 400, 500)

        self.conn = sqlite3.connect('attendance_app.db')
        self.cur = self.conn.cursor()

        # Layout
        self.layout = QVBoxLayout()

        # Styling
        self.setStyleSheet("""
            QLabel {
                font-weight: bold;
                color: #333;
            }
            QLineEdit {
                padding: 10px;
                border: 1px solid #ccc;
                border-radius: 5px;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 10px;
                border-radius: 5px;
                border: none;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #397d39;
            }
        """)

        # Widgets to Add Student
        self.student_name_label = QLabel("Student Name:")
        self.student_name_input = QLineEdit()
        self.roll_number_label = QLabel("Roll Number:")
        self.roll_number_input = QLineEdit()
        self.add_student_button = QPushButton("Add Student")
        self.add_student_button.clicked.connect(self.add_student)

        # Add widgets to layout
        self.layout.addWidget(self.student_name_label)
        self.layout.addWidget(self.student_name_input)
        self.layout.addWidget(self.roll_number_label)
        self.layout.addWidget(self.roll_number_input)
        self.layout.addWidget(self.add_student_button)

        # Widgets to Add Subject
        self.subject_name_label = QLabel("Subject Name:")
        self.subject_name_input = QLineEdit()
        self.add_subject_button = QPushButton("Add Subject")
        self.add_subject_button.clicked.connect(self.add_subject)

        self.layout.addWidget(self.subject_name_label)
        self.layout.addWidget(self.subject_name_input)
        self.layout.addWidget(self.add_subject_button)

        self.setLayout(self.layout)

    def add_student(self):
        student_name = self.student_name_input.text().strip()
        roll_number = self.roll_number_input.text().strip()

        if student_name and roll_number:
            try:
                self.cur.execute("INSERT INTO students (name, roll_number) VALUES (?, ?)", (student_name, roll_number))
                self.conn.commit()
                QMessageBox.information(self, "Success", "Student added successfully!")
                self.student_name_input.clear()
                self.roll_number_input.clear()
            except sqlite3.IntegrityError:
                QMessageBox.warning(self, "Error", "Student with this roll number already exists!")
            except sqlite3.Error as e:
                QMessageBox.critical(self, "Database Error", f"Error adding student: {e}")
        else:
            QMessageBox.warning(self, "Error", "Please fill in all fields.")

    def add_subject(self):
        subject_name = self.subject_name_input.text().strip()

        if subject_name:
            try:
                self.cur.execute("INSERT INTO subjects (name) VALUES (?)", (subject_name,))
                self.conn.commit()
                QMessageBox.information(self, "Success", "Subject added successfully!")
                self.subject_name_input.clear()
            except sqlite3.Error as e:
                QMessageBox.critical(self, "Database Error", f"Error adding subject: {e}")
        else:
            QMessageBox.warning(self, "Error", "Please enter the subject name.")

    def closeEvent(self, event):
        """Close database connection when the widget is closed."""
        self.conn.close()
        event.accept()  # Ensure the window closes

if __name__ == '__main__':
    app = QApplication([])
    admin_panel = AdminPanel()
    admin_panel.show()
    app.exec_()
