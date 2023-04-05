import sys
from PyQt6.QtCore import Qt,QSize
from PyQt6.QtWidgets import QComboBox,QApplication, QWidget, QLabel, QLineEdit, QVBoxLayout, QHBoxLayout, QPushButton
from PyQt6.QtGui import QPixmap
import graphviz
import psycopg2


class SquareLineEdit(QLineEdit):
    def sizeHint(self):
        # Override sizeHint() to return a square size
        size = super().sizeHint()
        return QSize(max(size.width(), size.height()), max(size.width(), size.height()))


class MyWidget(QWidget):
    
    def __init__(self):
        super().__init__()

        self.nodeList = list()
        self.nodeCount = 1
        
        #Query1
        self.queryText1 = SquareLineEdit()
        self.queryText1.textChanged.connect(self.carryOverText)
        
        self.queryDropDown1 = QComboBox()
        self.queryDropDown1.addItem("None")
        self.queryDropDown1.addItem("Select * from customer")
        self.queryDropDown1.addItem("Select * from region")
        self.queryDropDown1.addItem("Select * from orders")
        self.queryDropDown1.currentIndexChanged.connect(self.updateLineEdit)
        
        generateButton1 = QPushButton()
        generateButton1.setText("generate")
        
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
        self.queryText2 = SquareLineEdit()
        
        queryDropDown2 = QComboBox()
        queryDropDown2.addItem("Select * from customer")
        queryDropDown2.addItem("Select * from region")
        queryDropDown2.addItem("Select * from orders")
        
        generateButton2 = QPushButton()
        generateButton2.setText("generate")
        
        explainText2 = SquareLineEdit()
        explainText2.setDisabled(True)
    
        #self.graphVizImage2 = QPixmap('sid.jpg')
        self.graphVizImage2 = QLabel()
        #graphVizImage2 = SquareLineEdit()
        #graphVizImage2.setDisabled(True)
        
        query2VL = QVBoxLayout()
        query2VL.addWidget(self.queryText2)
        query2VL.addWidget(queryDropDown2)
        query2VL.addWidget(generateButton2)
        query2VL.addWidget(explainText2)
        query2VL.addWidget(self.graphVizImage2)
        
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
        index = self.queryDropDown1.currentIndex()
        if index == 0:
            self.queryText1.setText("")
        else:
            self.queryText1.setText(str(index))
    def carryOverText(self):
        self.queryText2.setText(self.queryText1.text())
    
    def treeDisplay(self, plan):
        """
            Function to display the traversal tree
        """
        f = graphviz.Graph()

        #query = self.textEdit.toPlainText()
        #plan = self.dbObj.getQueryPlan(query)
        
        if type(plan) is not dict:
            self.el1.setText(f'ERROR: Tree visualisation failed. Please check your query.\n{plan}')
        else:
            adjList = self.getAdjList(plan, {})[0]
            nodeList = self.nodeList

            self.nodeCount = 1
            self.nodeList = list()

            for node in nodeList:
                name = node.split('#')[0]
                f.node(node, name)

            for annotate in adjList:
                if len(adjList[annotate]) != 0:
                    for annotateString in adjList[annotate]:
                        f.edge(annotate, annotateString)

            f.render("QueryPlan", format="png", view=False)

            self.im = QPixmap("./QueryPlan.png")
            self.graphVizImage2.setPixmap(self.im)
            self.graphVizImage2.setFixedHeight(self.im.size().height())
            self.graphVizImage2.setFixedWidth(self.im.size().width())

    def getAdjList(self, queryPlan, result):
        """
        This method performs a post order DFS traversal on the query plan (a nested dictionary) and returns an adjacency list of operators as a dict type
            { parent node : [child node 1, child node 2, ...] }

        We use a count to keep track of the number of nodes visited and append it to the end of each node to make it unique 
        (else, there would be multiple Seq Scan's will be taken as the same node, when actually they are distinct Seq Scan's in the QEP)
            {
                "Hash Join#1" : ["Seq Scan#2", "Aggregate#3"], 
                "Aggregate#3" : ["Sort#4", "Seq Scan#5"]
            }
        """

        # Leaf node
        if 'Plans' not in queryPlan:
            if self.nodeCount == 1:
                self.nodeList.append(
                    f"{queryPlan['Node Type']}#{self.nodeCount}")
            curIterCount = self.nodeCount
            self.nodeCount += 1
            return [result, curIterCount]

        # Node with child nodes
        else:
            # Name the parent node, increment the count
            planNodeType = f"{queryPlan['Node Type']}#{self.nodeCount}"
            if planNodeType not in self.nodeList:
                self.nodeList.append(planNodeType)

            # Keep track of count in this recursion iteration
            curIterCount = self.nodeCount
            self.nodeCount += 1

            # DFS: keep traversing until leaf node is reached
            for subplan in queryPlan['Plans']:
                nextIterCount = self.getAdjList(subplan, result)[1]

                # Name the child node, increment the count
                subplanNodeType = f"{subplan['Node Type']}#{nextIterCount}"
                if subplanNodeType not in self.nodeList:
                    self.nodeList.append(subplanNodeType)

                # Add the child node to its parent node in the adjacency list
                if planNodeType in result:
                    result[planNodeType].append(subplanNodeType)
                else:
                    result[planNodeType] = [subplanNodeType]

            # return curIterCount (OR, in the 1st iteration, return the final result)
            return [result, curIterCount]

    




if __name__ == '__main__':
    conn = psycopg2.connect(
        database="TPC-H", user='postgres', password='123456', host='127.0.0.1', port= '5432'
    )
    
    conn.autocommit = True
    cursor = conn.cursor()
    cursor.execute(
                f"EXPLAIN (FORMAT JSON) {'''SELECT * from Region, customer Where region.r_regionkey = 0'''}")
                #f"EXPLAIN (FORMAT JSON) {'''SELECT * from Region'''}")
    
    #cursor.execute('''SELECT * from Region''')
    result = cursor.fetchall()
    #print(result)
    # for x in result[0][0][0]["Plan"]:
    #     if(x != "Plans"):
    #         print("Key: ", x, " = ", result[0][0][0]["Plan"][x])
    # for y in result[0][0][0]["Plan"]["Plans"]:
    #     print("-------------")
    #     for z in y:
    #         print("Key: ",z, " = ", y[z])
    print(result[0][0][0])
    
    app = QApplication(sys.argv)
    widget = MyWidget()
    widget.setTestingMessage("hello")
    widget.show()
    widget.treeDisplay(result[0][0][0]["Plan"])
    sys.exit(app.exec())
