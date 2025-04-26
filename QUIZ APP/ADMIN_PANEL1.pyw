import sys
import sqlite3
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QMessageBox, QTableWidget, QTableWidgetItem, QComboBox

class AdminPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Admin Panel")
        self.setGeometry(400, 150, 500, 500)

        # Layout
        self.layout = QVBoxLayout()

        # Section 1: Add Questions
        self.add_question_section()

        # Section 2: View Results
        self.view_results_section()

        self.setLayout(self.layout)

    def add_question_section(self):
        # Title for adding questions
        self.title = QLabel("Add New Question")
        self.layout.addWidget(self.title)

        # Input fields for adding questions
        self.question_input = QLineEdit(self)
        self.question_input.setPlaceholderText("Enter the question")
        self.layout.addWidget(self.question_input)

        self.option1_input = QLineEdit(self)
        self.option1_input.setPlaceholderText("Option 1")
        self.layout.addWidget(self.option1_input)

        self.option2_input = QLineEdit(self)
        self.option2_input.setPlaceholderText("Option 2")
        self.layout.addWidget(self.option2_input)

        self.option3_input = QLineEdit(self)
        self.option3_input.setPlaceholderText("Option 3")
        self.layout.addWidget(self.option3_input)

        # Correct option selector (dropdown)
        self.correct_option_input = QComboBox(self)
        self.correct_option_input.addItems(["Select Correct Option", "Option 1", "Option 2", "Option 3"])
        self.layout.addWidget(self.correct_option_input)

        # Add Question Button
        self.add_question_btn = QPushButton("Add Question", self)
        self.add_question_btn.clicked.connect(self.add_question_to_db)
        self.layout.addWidget(self.add_question_btn)

    def add_question_to_db(self):
        # Get the inputs
        question = self.question_input.text()
        option1 = self.option1_input.text()
        option2 = self.option2_input.text()
        option3 = self.option3_input.text()
        correct_option = self.correct_option_input.currentIndex()

        # Ensure all inputs are provided
        if question and option1 and option2 and option3 and correct_option != 0:
            # Insert into database
            conn = sqlite3.connect('quiz_app.db')
            cursor = conn.cursor()

            cursor.execute('''
                INSERT INTO questions (question, option1, option2, option3, correct_option)
                VALUES (?, ?, ?, ?, ?)
            ''', (question, option1, option2, option3, correct_option))

            conn.commit()
            conn.close()

            QMessageBox.information(self, 'Success', 'Question added successfully!')
            self.clear_inputs()

        else:
            QMessageBox.warning(self, 'Error', 'Please fill all fields and select the correct option.')

    def clear_inputs(self):
        self.question_input.clear()
        self.option1_input.clear()
        self.option2_input.clear()
        self.option3_input.clear()
        self.correct_option_input.setCurrentIndex(0)

    def view_results_section(self):
        # Title for viewing results
        self.results_title = QLabel("View Quiz Results")
        self.layout.addWidget(self.results_title)

        # View Results Button
        self.view_results_btn = QPushButton("View Results", self)
        self.view_results_btn.clicked.connect(self.display_results)
        self.layout.addWidget(self.view_results_btn)

        # Table for displaying results
        self.results_table = QTableWidget(self)
        self.results_table.setColumnCount(2)
        self.results_table.setHorizontalHeaderLabels(["Candidate", "Score"])
        self.layout.addWidget(self.results_table)

    def display_results(self):
        # Fetch data from the database
        conn = sqlite3.connect('quiz_app.db')
        cursor = conn.cursor()

        cursor.execute('''
            SELECT c.name, r.score
            FROM quiz_results r
            JOIN candidates c ON r.candidate_id = c.id
        ''')

        results = cursor.fetchall()
        conn.close()

        # Populate the results table
        self.results_table.setRowCount(len(results))
        for row_num, row_data in enumerate(results):
            self.results_table.setItem(row_num, 0, QTableWidgetItem(row_data[0]))
            self.results_table.setItem(row_num, 1, QTableWidgetItem(str(row_data[1])))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = AdminPanel()
    window.show()
    sys.exit(app.exec_())
