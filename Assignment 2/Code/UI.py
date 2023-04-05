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
        self.queryText1 = SquareLineEdit()
        
        self.queryDropDown1 = QComboBox()
        self.queryDropDown1.addItem("Select * from customer")
        self.queryDropDown1.addItem("Select * from region")
        self.queryDropDown1.addItem("Select * from orders")
        self.queryDropDown1.currentIndexChanged.connect(self.updateLineEdit)
        
        generateButton1 = QPushButton()
        
        explainText1 = SquareLineEdit()
        explainText1.setDisabled(True)
        
        #graphVizImage = QPixmap('sid.jpg')
        graphVizImage1 = SquareLineEdit()
        graphVizImage1.setDisabled(True)
        
        query1VL = QVBoxLayout()
        query1VL.addWidget(self.queryText1)
        query1VL.addWidget(self.queryDropDown1)
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

    def updateLineEdit(self, index):
        self.queryText1.setText(self.queryDropDown1.currentText())
    




if __name__ == '__main__':
    conn = psycopg2.connect(
        database="TPC-H", user='postgres', password='123456', host='127.0.0.1', port= '5432'
    )
    
    conn.autocommit = True
    cursor = conn.cursor()
    cursor.execute(
                f"EXPLAIN (FORMAT JSON) {'''SELECT * from Region, customer Where region.r_regionkey = 0'''}")
    
    #cursor.execute('''SELECT * from Region''')
    result = cursor.fetchall()
    #print(result)
    for x in result[0][0][0]["Plan"]:
        if(x != "Plans"):
            print("Key: ", x, " = ", result[0][0][0]["Plan"][x])
    for y in result[0][0][0]["Plan"]["Plans"]:
        print("-------------")
        for z in y:
            print("Key: ",z, " = ", y[z])
    #print(result[0][0][0]["Plan"])
    
    app = QApplication(sys.argv)
    widget = MyWidget()
    widget.setTestingMessage("hello")
    widget.show()
    sys.exit(app.exec())
