import sqlite3
import sys

from PyQt5.QtWidgets import QMainWindow, QLabel, QApplication, QPushButton, QComboBox, QLineEdit

conn = sqlite3.connect("dbname.db")
curs = conn.cursor()

curs.execute('''CREATE TABLE IF NOT EXISTS table_1(id INTEGER PRIMARY KEY AUTOINCREMENT, col_1 TEXT, col_2 TEXT)''')
curs.execute('''CREATE TABLE IF NOT EXISTS table_2(id INTEGER PRIMARY KEY AUTOINCREMENT, col_1 TEXT, col_2 TEXT)''')
curs.execute('''Insert into table_1(col_1, col_2) Values("text one", "text two")''')
curs.execute('''Insert into table_2(col_1, col_2) Values("text text", "text text")''')
conn.commit()


class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setFixedSize(600, 400)
        self.qlabel = QLabel('line 1', self)
        self.styleLable = 'border: 1px solid black'
        self.qlabel.setStyleSheet(self.styleLable)
        self.qlabel.setGeometry(10, 10, 150, 100)

        self.lEditOne = QLineEdit(self)
        self.lEditOne.move(170, 10)

        self.lEditTwo = QLineEdit(self)
        self.lEditTwo.move(170, 70)

        self.qButton1 = QPushButton("One", self)
        self.qButton2 = QPushButton("Two", self)

        self.qButton1.setGeometry(290, 10, 60, 30)
        self.qButton2.setGeometry(290, 70, 60, 30)

        self.qButton1.clicked.connect(self.funcBtnOne)
        self.qButton2.clicked.connect(self.funcBtnTwo)

        self.qCombo1 = QComboBox(self)
        self.qCombo1.addItem("table_1")
        self.qCombo1.addItem("table_2")
        self.qCombo1.move(10, 120)

        self.qCombo2 = QComboBox(self)
        self.qCombo2.addItem("col_1")
        self.qCombo2.addItem("col_2")
        self.qCombo2.addItem("col_1 and col_2")
        self.qCombo2.move(10, 170)

    def funcBtnOne(self):
        self.s = self.qCombo1.currentText()
        self.table_data = curs.execute(f'''Select * from {self.s}''')
        self.data = self.table_data.fetchall()
        self.pt = ""
        for d in self.data:
            for sd in d:
                self.pt += str(sd) + " " + "\n"
        self.qlabel.setText(self.pt)

    def funcBtnTwo(self):
        self.sTable = self.qCombo1.currentText()
        self.sCol = self.qCombo2.currentText()
        self.col_1 = self.lEditOne.text()
        self.col_2 = self.lEditTwo.text()
        if self.sCol == 'col_1 and col_2':
            curs.execute(f'''Insert into {self.sTable}(col_1, col_2) values({self.col_1}, {self.col_2})''')
        else:
            curs.execute(f'''Insert into {self.sTable}({self.sCol}) values({self.col_1})''')
            curs.execute(f'''Insert into {self.sTable}({self.sCol}) values({self.col_2})''')
        conn.commit()
        print("Success")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Main()
    ex.show()
    sys.exit(app.exec_())
