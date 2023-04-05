import sys
from PyQt6.QtCore import Qt,QSize
from PyQt6.QtWidgets import QComboBox,QApplication, QWidget, QLabel, QLineEdit, QVBoxLayout, QHBoxLayout, QPushButton

import psycopg2


class SquareLineEdit(QLineEdit):
    def sizeHint(self):
        # Override sizeHint() to return a square size
        size = super().sizeHint()
        return QSize(max(size.width(), size.height()), max(size.width(), size.height()))


class MyWidget(QWidget):
    
    def __init__(self):
        super().__init__()
        
        #Query1
        queryText1 = SquareLineEdit()
        
        queryDropDown1 = QComboBox()
        queryDropDown1.addItem("Select * from customer")
        queryDropDown1.addItem("Select * from region")
        queryDropDown1.addItem("Select * from orders")
        
        generateButton1 = QPushButton()
        
        explainText1 = SquareLineEdit()
        explainText1.setDisabled(True)
        
        #graphVizImage = QPixmap('sid.jpg')
        graphVizImage1 = SquareLineEdit()
        graphVizImage1.setDisabled(True)
        
        query1VL = QVBoxLayout()
        query1VL.addWidget(queryText1)
        query1VL.addWidget(queryDropDown1)
        query1VL.addWidget(generateButton1)
        query1VL.addWidget(explainText1)
        query1VL.addWidget(graphVizImage1)

        #Query2
        queryText2 = SquareLineEdit()
        
        queryDropDown2 = QComboBox()
        queryDropDown2.addItem("Select * from customer")
        queryDropDown2.addItem("Select * from region")
        queryDropDown2.addItem("Select * from orders")
        
        generateButton2 = QPushButton()
        
        explainText2 = SquareLineEdit()
        explainText2.setDisabled(True)
    
        #graphVizImage = QPixmap('sid.jpg')
        graphVizImage2 = SquareLineEdit()
        graphVizImage2.setDisabled(True)
        
        query2VL = QVBoxLayout()
        query2VL.addWidget(queryText2)
        query2VL.addWidget(queryDropDown2)
        query2VL.addWidget(generateButton2)
        query2VL.addWidget(explainText2)
        query2VL.addWidget(graphVizImage2)
        
        # Create title
        titleLabel = QLabel("Finally started on this project")
        testingMessage =  "HAHA"
        self.testingMessageLabel = QLabel(testingMessage)
        
        mainLayout = QHBoxLayout()
        mainLayout.addLayout(query1VL)
        mainLayout.addLayout(query2VL)
        # Set the main layout for the widget
        self.setLayout(mainLayout)
        
    def setTestingMessage(self, message):
        self.testingMessageLabel.setText(message)
    

    


if __name__ == '__main__':
    conn = psycopg2.connect(
        database="TPC-H", user='postgres', password='270198', host='127.0.0.1', port= '5432'
    )
    
    conn.autocommit = True
    cursor = conn.cursor()
    
    cursor.execute('''SELECT * from Region''')
    result = cursor.fetchall()
    print(result)
    
    app = QApplication(sys.argv)
    widget = MyWidget()
    widget.setTestingMessage("hello")
    widget.show()
    sys.exit(app.exec())
