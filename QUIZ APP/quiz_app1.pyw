import sys
import sqlite3
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox
from PyQt5.QtCore import QPropertyAnimation, QEasingCurve

class Login(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Quiz Login")
        self.setGeometry(300, 300, 300, 200)
        self.setStyleSheet("""
            QWidget {
                background-color: #f0f0f0;
                color: #333;
                font-size: 14px;
            }
            QLabel {
                color: #555;
            }
            QLineEdit {
                border: 1px solid #aaa;
                border-radius: 5px;
                padding: 5px;
            }
            QPushButton {
                background-color: #007bff;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
            QPushButton:pressed {
                background-color: #00408b;
            }
        """)

        # Layout
        layout = QVBoxLayout()

        # Widgets for name and code input
        self.name_label = QLabel("Enter Name:")
        self.name_input = QLineEdit()
        self.code_label = QLabel("Enter Quiz Code:")
        self.code_input = QLineEdit()

        # Submit button
        self.submit_btn = QPushButton("Submit")
        self.submit_btn.clicked.connect(self.authenticate_candidate)

        # Add widgets to layout
        layout.addWidget(self.name_label)
        layout.addWidget(self.name_input)
        layout.addWidget(self.code_label)
        layout.addWidget(self.code_input)
        layout.addWidget(self.submit_btn)

        self.setLayout(layout)

    def authenticate_candidate(self):
        name = self.name_input.text()
        code = self.code_input.text()

        # Connect to database
        conn = sqlite3.connect('quiz_app.db')
        cursor = conn.cursor()

        # Check if candidate exists in the database
        query = "SELECT id FROM candidates WHERE name = ? AND code = ?"
        cursor.execute(query, (name, code))
        result = cursor.fetchone()

        if result:
            QMessageBox.information(self, 'Success', 'Access granted!')
            self.close()

            # Pass candidate ID to QuizApp for later score logging
            self.quiz_window = QuizApp(result[0])
            self.quiz_window.show()
        else:
            QMessageBox.warning(self, 'Error', 'Invalid name or code.')

        conn.close()

class QuizApp(QWidget):
    def __init__(self, candidate_id):
        super().__init__()
        self.candidate_id = candidate_id  # Candidate ID for storing results
        self.setWindowTitle("Quiz Application")
        self.setGeometry(300, 300, 400, 300)

        # Add style sheet
        self.setStyleSheet("""
            QWidget {
                background-color: #ffffff;
                color: #333;
                font-size: 14px;
            }
            QLabel {
                color: #555;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton {
                background-color: #28a745;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #218838;
            }
            QPushButton:pressed {
                background-color: #1e7e34;
            }
            QPushButton#nextButton {
                background-color: red; /* Change to red */
                color: white;
            }
            QPushButton#nextButton:hover {
                background-color: #cc0000; /* Darker red on hover */
            }
            QPushButton#nextButton:pressed {
                background-color: #990000; /* Even darker red when pressed */
            }
        """)

        self.question_number = 0
        self.score = 0

        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout()

        # Question Label
        self.question_label = QLabel()
        self.layout.addWidget(self.question_label)

        # Options as buttons
        self.option_buttons = []
        for _ in range(3):
            btn = QPushButton()
            btn.clicked.connect(lambda checked, i=len(self.option_buttons): self.check_answer(i))
            self.layout.addWidget(btn)
            self.option_buttons.append(btn)

        # Next Button
        self.next_btn = QPushButton("Next")
        self.next_btn.setObjectName("nextButton")  # Assign an ID to the button
        self.next_btn.clicked.connect(self.next_question)
        self.layout.addWidget(self.next_btn)

        self.setLayout(self.layout)

        # Load questions from database
        self.load_questions()

    def load_questions(self):
        # Connect to database
        conn = sqlite3.connect('quiz_app.db')
        cursor = conn.cursor()

        # Fetch questions from the database
        query = "SELECT * FROM questions ORDER BY id"
        cursor.execute(query)
        self.questions = cursor.fetchall()
        self.total_questions = len(self.questions)

        conn.close()

        if self.total_questions > 0:
            self.update_question()
        else:
            QMessageBox.warning(self, 'No Questions', 'No questions found in the database.')
            self.close()

    def check_answer(self, selected_option):
        correct_option = self.questions[self.question_number][5] - 1  # Convert to 0-based index
        if selected_option == correct_option:
            self.score += 1
        # Disable all option buttons after selecting an answer
        for btn in self.option_buttons:
            btn.setDisabled(True)

    def next_question(self):
        self.question_number += 1
        if self.question_number < self.total_questions:
            self.update_question()
        else:
            self.submit_score()

    def update_question(self):
        # Update question text
        question_data = self.questions[self.question_number]
        self.question_label.setText(question_data[1])

        # Update options text
        for i in range(3):
            self.option_buttons[i].setText(question_data[i+2])
            self.option_buttons[i].setDisabled(False)

        # Add animation to next button
        self.animate_button(self.next_btn)

    def animate_button(self, button):
        animation = QPropertyAnimation(button, b"geometry")
        animation.setDuration(500)
        animation.setStartValue(button.geometry())
        animation.setEndValue(button.geometry().adjusted(0, -10, 0, -10))
        animation.setEasingCurve(QEasingCurve.InOutBounce)
        animation.start()

    def submit_score(self):
        # Connect to the database and store the result
        conn = sqlite3.connect('quiz_app.db')
        cursor = conn.cursor()

        query = "INSERT INTO quiz_results (candidate_id, score) VALUES (?, ?)"
        cursor.execute(query, (self.candidate_id, self.score))
        conn.commit()
        conn.close()

        QMessageBox.information(self, 'Quiz Completed', f'Your score: {self.score}/{self.total_questions}')
        self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    login_window = Login()
    login_window.show()
    sys.exit(app.exec_())
