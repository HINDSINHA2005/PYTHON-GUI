from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox, QTableWidget, QTableWidgetItem, QWidget
from PyQt5.QtGui import QPixmap, QPalette, QBrush
from PyQt5.QtCore import QPropertyAnimation, QRect

class Ui_Form(QWidget):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(700, 500)  # Increased the main window size for better layout

        # Set background image
        self.set_background_image(Form)

        # Main Layout
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")

        # Row 1: Title Input
        self.horizontalLayout1 = QtWidgets.QHBoxLayout()
        self.horizontalLayout1.setObjectName("horizontalLayout1")
        self.label_3 = QtWidgets.QLabel(Form)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout1.addWidget(self.label_3)
        self.le1 = QtWidgets.QLineEdit(Form)
        font.setPointSize(12)
        self.le1.setFont(font)
        self.le1.setObjectName("le1")
        self.horizontalLayout1.addWidget(self.le1)
        self.b1 = QtWidgets.QPushButton(Form)
        font.setPointSize(12)
        font.setBold(True)
        self.b1.setFont(font)
        self.b1.setObjectName("b1")
        self.b1.clicked.connect(self.findprice)
        self.horizontalLayout1.addWidget(self.b1)
        self.verticalLayout.addLayout(self.horizontalLayout1)

        # Row 2: TableWidget to Display Book Details
        self.tableWidget = QtWidgets.QTableWidget(Form)
        self.tableWidget.setColumnCount(3)  # Columns for Title, Author, Price
        self.tableWidget.setHorizontalHeaderLabels(["Title", "Author", "Price"])
        self.tableWidget.setFixedSize(600, 150)  # Increased table view size for better readability
        self.verticalLayout.addWidget(self.tableWidget)

        # Row 3: Quantity Input and Total Button
        self.horizontalLayout2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout2.setObjectName("horizontalLayout2")
        self.label = QtWidgets.QLabel(Form)
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.horizontalLayout2.addWidget(self.label)
        self.le3 = QtWidgets.QLineEdit(Form)
        font.setPointSize(12)
        self.le3.setFont(font)
        self.le3.setObjectName("le3")
        self.horizontalLayout2.addWidget(self.le3)
        self.b2 = QtWidgets.QPushButton(Form)
        font.setPointSize(12)
        font.setBold(True)
        self.b2.setFont(font)
        self.b2.setObjectName("b2")
        self.b2.clicked.connect(self.findtotal)
        self.horizontalLayout2.addWidget(self.b2)
        self.le4 = QtWidgets.QLineEdit(Form)
        font.setPointSize(12)
        self.le4.setFont(font)
        self.le4.setObjectName("le4")
        self.horizontalLayout2.addWidget(self.le4)
        self.verticalLayout.addLayout(self.horizontalLayout2)

        # Row 4: Reset Button and Book List Button
        self.horizontalLayout3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout3.setObjectName("horizontalLayout3")
        self.b3 = QtWidgets.QPushButton(Form)
        font.setPointSize(12)
        font.setBold(True)
        self.b3.setFont(font)
        self.b3.setObjectName("b3")
        self.b3.clicked.connect(self.reset)
        self.horizontalLayout3.addWidget(self.b3)
        self.b4 = QtWidgets.QPushButton(Form)
        font.setPointSize(12)
        font.setBold(True)
        self.b4.setFont(font)
        self.b4.setObjectName("b4")
        self.b4.clicked.connect(self.show_all_books)
        self.horizontalLayout3.addWidget(self.b4)
        self.verticalLayout.addLayout(self.horizontalLayout3)

        # Apply Styles
        self.apply_styles()

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def apply_styles(self):
        # Set custom stylesheets
        self.setStyleSheet("""
            QWidget {
                background-color: #f5f5f5;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border-radius: 5px;
                padding: 10px;
                font-size: 12pt;
                border: 1px solid #4CAF50;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QLineEdit {
                border: 1px solid #ddd;
                border-radius: 5px;
                padding: 5px;
                font-size: 12pt;
            }
            QLabel {
                font-size: 12pt;
                color: #333;
            }
            QTableWidget {
                background-color: #fff;
                border: 1px solid #ddd;
                border-radius: 5px;
            }
            QHeaderView::section {
                background-color: #f2f2f2;
                padding: 5px;
            }
        """)

    def set_background_image(self, Form):
        # Set a background image
        oImage = QtGui.QImage("C:/Users/ak870/Videos/mini project/BOOK.jpg")  # Replace with your image path
        sImage = oImage.scaled(Form.size())
        palette = QPalette()
        palette.setBrush(10, QBrush(sImage))
        Form.setPalette(palette)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "HIND'S BOOK STORE"))
        self.label_3.setText(_translate("Form", "Enter Title"))
        self.b1.setText(_translate("Form", "Find Price"))
        self.label.setText(_translate("Form", "Enter Quantity"))
        self.b2.setText(_translate("Form", "Calculate Total Amount"))
        self.b3.setText(_translate("Form", "Reset"))
        self.b4.setText(_translate("Form", "Show All Books"))

    def findprice(self):
        import sqlite3
        db = sqlite3.connect("m5assignment.db")
        cur = db.cursor()
        ttl = self.le1.text().lower()  # Convert input to lowercase

        # Clear previous table content
        self.tableWidget.setRowCount(0)

        # Make the query case-insensitive using LOWER
        sql = "SELECT title, author, price FROM books WHERE LOWER(title)=?"
        cur.execute(sql, (ttl,))
        rec = cur.fetchone()

        if rec:
            title, author, price = rec

            # Add the fetched data into the table
            self.tableWidget.setRowCount(1)
            self.tableWidget.setItem(0, 0, QTableWidgetItem(title))
            self.tableWidget.setItem(0, 1, QTableWidgetItem(author))
            self.tableWidget.setItem(0, 2, QTableWidgetItem(str(price)))

            # Storing the price for further calculations
            self.pr = price

        else:
            # If the title is not found, display a message box
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("Title Not Found")
            msg.setWindowTitle("Error")
            msg.exec_()

    def findtotal(self):
        self.qty = float(self.le3.text())
        ttl = self.pr * self.qty
        self.le4.setText(str(ttl))

    def reset(self):
        self.le1.clear()
        self.le2.clear()
        self.le3.clear()
        self.le4.clear()
        self.tableWidget.setRowCount(0)
        self.tableWidget.setColumnCount(3)

    def show_all_books(self):
        import sqlite3
        db = sqlite3.connect("m5assignment.db")
        cur = db.cursor()
        
        # Clear previous table content
        self.tableWidget.setRowCount(0)
        
        sql = "SELECT title, author, price FROM books"
        cur.execute(sql)
        rows = cur.fetchall()
        
        if rows:
            self.tableWidget.setRowCount(len(rows))
            for row_idx, row in enumerate(rows):
                title, author, price = row
                self.tableWidget.setItem(row_idx, 0, QTableWidgetItem(title))
                self.tableWidget.setItem(row_idx, 1, QTableWidgetItem(author))
                self.tableWidget.setItem(row_idx, 2, QTableWidgetItem(str(price)))
        else:
            # If no books are found, display a message box
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("No books found in the store.")
            msg.setWindowTitle("Information")
            msg.exec_()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = Ui_Form()
    Form.show()
    sys.exit(app.exec_())
