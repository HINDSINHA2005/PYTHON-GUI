import sqlite3
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox, QListWidget
from PyQt5.QtGui import QColor, QPalette
from PyQt5.QtCore import Qt

class StudentPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Panel")
        self.setGeometry(300, 300, 400, 400)

        self.conn = sqlite3.connect('attendance_app.db')
        self.cur = self.conn.cursor()

        # Layout
        self.layout = QVBoxLayout()

        # Student Roll Number
        self.roll_number_label = QLabel("Enter Roll Number:")
        self.roll_number_label.setStyleSheet("font-weight: bold; color: #333;")
        self.roll_number_input = QLineEdit()
        self.roll_number_input.setPlaceholderText("Enter roll number here")
        self.check_attendance_button = QPushButton("Check Attendance")
        self.check_attendance_button.setStyleSheet("""
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
        self.check_attendance_button.clicked.connect(self.check_attendance)

        # Search History
        self.history_label = QLabel("Search History:")
        self.history_label.setStyleSheet("font-weight: bold; color: #333;")
        self.history_list = QListWidget()
        self.history_list.setStyleSheet("background-color: #f5f5f5;")

        # Add to layout
        self.layout.addWidget(self.roll_number_label)
        self.layout.addWidget(self.roll_number_input)
        self.layout.addWidget(self.check_attendance_button)
        self.layout.addWidget(self.history_label)
        self.layout.addWidget(self.history_list)

        self.setLayout(self.layout)

    def check_attendance(self):
        roll_number = self.roll_number_input.text().strip()

        if not roll_number:
            QMessageBox.warning(self, "Input Error", "Please enter a roll number.")
            return

        try:
            # Get student ID based on roll number
            self.cur.execute("SELECT id FROM students WHERE roll_number=?", (roll_number,))
            student_id = self.cur.fetchone()

            if student_id:
                # Fetch attendance records for the student
                self.cur.execute(
                    "SELECT subjects.name, attendance.date, attendance.status "
                    "FROM attendance "
                    "JOIN subjects ON attendance.subject_id = subjects.id "
                    "WHERE attendance.student_id=?", (student_id[0],))
                attendance_records = self.cur.fetchall()

                if attendance_records:
                    attendance_message = "Attendance Records:\n"
                    for record in attendance_records:
                        subject, date, status = record
                        attendance_message += f"Subject: {subject}, Date: {date}, Status: {status}\n"
                    QMessageBox.information(self, "Attendance", attendance_message)
                else:
                    QMessageBox.information(self, "No Records", "No attendance records found for this student.")
                
                # Add to search history
                self.history_list.addItem(roll_number)
                if self.history_list.count() > 5:
                    self.history_list.takeItem(0)  # Limit history to the last 5 entries

            else:
                QMessageBox.warning(self, "Error", "Student not found!")

        except sqlite3.Error as e:
            QMessageBox.critical(self, "Database Error", f"Error fetching attendance: {e}")

        # Clear the roll number input
        self.roll_number_input.clear()

    def closeEvent(self, event):
        """Close database connection when the widget is closed."""
        self.conn.close()
        event.accept()  # Ensure the window closes

if __name__ == '__main__':
    app = QApplication([])
    window = StudentPanel()
    window.show()
    app.exec_()
