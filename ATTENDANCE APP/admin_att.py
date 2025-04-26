import sqlite3
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QComboBox, QPushButton, QVBoxLayout, QMessageBox, QListWidget
from PyQt5.QtGui import QColor, QPalette
from PyQt5.QtCore import Qt

class AttendancePanel(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Record Attendance")
        self.setGeometry(300, 300, 500, 500)

        self.conn = sqlite3.connect('attendance_app.db')
        self.cur = self.conn.cursor()

        # Widgets for Subject
        self.subject_label = QLabel("Select Subject:")
        self.subject_label.setStyleSheet("font-weight: bold; color: #333;")
        self.subject_dropdown = QComboBox()
        self.load_subjects()

        # Widgets for Student
        self.student_label = QLabel("Select Student:")
        self.student_label.setStyleSheet("font-weight: bold; color: #333;")
        self.student_dropdown = QComboBox()
        self.load_students()

        # Widgets for Attendance Status
        self.status_label = QLabel("Attendance Status:")
        self.status_label.setStyleSheet("font-weight: bold; color: #333;")
        self.status_dropdown = QComboBox()
        self.status_dropdown.addItems(["Present", "Absent"])

        # Button to Submit Attendance
        self.submit_button = QPushButton("Submit Attendance")
        self.submit_button.setStyleSheet("""
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
        self.submit_button.clicked.connect(self.record_attendance)

        # Search History
        self.history_label = QLabel("Submission History:")
        self.history_label.setStyleSheet("font-weight: bold; color: #333;")
        self.history_list = QListWidget()
        self.history_list.setStyleSheet("background-color: #f5f5f5;")

        # Layout
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.subject_label)
        self.layout.addWidget(self.subject_dropdown)
        self.layout.addWidget(self.student_label)
        self.layout.addWidget(self.student_dropdown)
        self.layout.addWidget(self.status_label)
        self.layout.addWidget(self.status_dropdown)
        self.layout.addWidget(self.submit_button)
        self.layout.addWidget(self.history_label)
        self.layout.addWidget(self.history_list)
        self.setLayout(self.layout)

    def load_subjects(self):
        try:
            self.cur.execute("SELECT name FROM subjects")
            subjects = self.cur.fetchall()
            for subject in subjects:
                self.subject_dropdown.addItem(subject[0])
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Error", f"Error loading subjects: {e}")

    def load_students(self):
        try:
            self.cur.execute("SELECT name FROM students")
            students = self.cur.fetchall()
            for student in students:
                self.student_dropdown.addItem(student[0])
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Error", f"Error loading students: {e}")

    def record_attendance(self):
        student = self.student_dropdown.currentText()
        subject = self.subject_dropdown.currentText()
        status = self.status_dropdown.currentText()

        try:
            # Get student and subject IDs
            self.cur.execute("SELECT id FROM students WHERE name=?", (student,))
            student_id = self.cur.fetchone()
            if student_id is None:
                raise ValueError("Student not found.")
            student_id = student_id[0]

            self.cur.execute("SELECT id FROM subjects WHERE name=?", (subject,))
            subject_id = self.cur.fetchone()
            if subject_id is None:
                raise ValueError("Subject not found.")
            subject_id = subject_id[0]

            # Record attendance
            self.cur.execute("INSERT INTO attendance (student_id, subject_id, date, status) VALUES (?, ?, date('now'), ?)",
                             (student_id, subject_id, status))
            self.conn.commit()

            # Add to submission history
            history_entry = f"Student: {student}, Subject: {subject}, Status: {status}"
            self.history_list.addItem(history_entry)
            if self.history_list.count() > 5:
                self.history_list.takeItem(0)  # Limit history to the last 5 entries

            QMessageBox.information(self, "Success", "Attendance recorded successfully!")

        except sqlite3.Error as e:
            QMessageBox.critical(self, "Database Error", f"Error recording attendance: {e}")
        except ValueError as ve:
            QMessageBox.warning(self, "Invalid Data", str(ve))

    def closeEvent(self, event):
        """Close database connection when the widget is closed."""
        self.conn.close()
        event.accept()  # Ensure the window closes

if __name__ == '__main__':
    app = QApplication([])
    window = AttendancePanel()
    window.show()
    app.exec_()
