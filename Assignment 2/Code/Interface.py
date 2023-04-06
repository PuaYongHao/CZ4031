import sys
from PyQt6.QtCore import Qt,QSize
from PyQt6.QtWidgets import QComboBox,QApplication, QWidget, QLabel, QTextEdit, QVBoxLayout, QPushButton, QGridLayout
from PyQt6.QtGui import QPixmap
import graphviz
import psycopg2
from explain import generateDifference


class SquareLineEdit(QTextEdit):
    def sizeHint(self):
        # Override sizeHint() to return a square size
        size = super().sizeHint()
        return QSize(max(size.width(), size.height()), max(size.width(), size.height()))


class MyWidget(QWidget):
    
    def __init__(self,password):
        super().__init__()

        self.connection = obj = psycopg2.connect(
                database="TPC-H", user='postgres', password=password, host='127.0.0.1', port= '5432')
        self.connection.autocommit = True
        self.cursor = self.connection.cursor()
        #cursor = self.connection.cursor()

        self.nodeList = list()
        self.nodeCount = 1
        #self.setFixedWidth(1000)
        
        #Query1
        self.queryText1 = SquareLineEdit()
        self.queryText1.setLineWrapColumnOrWidth(800) #Here you set the width you want
        self.queryText1.setLineWrapMode(QTextEdit.LineWrapMode.FixedPixelWidth)
        #self.queryText1.setLineWrapMode(QTextEdit.LineWrapMode.WidgetWidth)
        self.queryText1.textChanged.connect(self.carryOverText)
        
        self.queryDropDown1 = QComboBox()
        self.queryDropDown1.addItem("None")
        self.queryDropDown1.addItem("Query1")
        self.queryDropDown1.addItem("Query2")
        self.queryDropDown1.addItem("Query3")
        self.queryDropDown1.currentIndexChanged.connect(self.updateLineEdit)
        
        generateButton1 = QPushButton()
        generateButton1.setText("generate")
        generateButton1.clicked.connect(self.generateOldOrder)
        
        explainText1 = SquareLineEdit()
        explainText1.setReadOnly(True)
        # explainText1.setDisabled(True)
        
        #graphVizImage = QPixmap('sid.jpg')
        self.graphVizImage1 = QLabel()
        # self.graphVizImage1 = SquareLineEdit()
        # self.graphVizImage1.setDisabled(True)
        
        # query1VL = QVBoxLayout()
        # query1VL.addWidget(self.queryText1)
        # query1VL.addWidget(self.queryDropDown1)
        # query1VL.addWidget(generateButton1)
        # query1VL.addWidget(explainText1)
        # query1VL.addWidget(graphVizImage1)

        #Query2
        self.queryText2 = SquareLineEdit()
        
        self.queryDropDown2 = QComboBox()
        self.queryDropDown2.addItem("Where customerID = XXX")
        self.queryDropDown2.addItem("Where customerName = XXX")
        self.queryDropDown2.addItem("Select * from orders")
        
        generateButton2 = QPushButton()
        generateButton2.setText("generate")
        generateButton2.clicked.connect(self.generateNewOrder)
        
        explainText2 = SquareLineEdit()
        explainText2.setReadOnly(True)
        # explainText2.setDisabled(True)
    
        #self.graphVizImage2 = QPixmap('sid.jpg')
        self.graphVizImage2 = QLabel()
        #graphVizImage2 = SquareLineEdit()
        #graphVizImage2.setDisabled(True)
        
        # query2VL = QVBoxLayout()
        # query2VL.addWidget(self.queryText2)
        # query2VL.addWidget(queryDropDown2)
        # query2VL.addWidget(generateButton2)
        # query2VL.addWidget(explainText2)
        # query2VL.addWidget(self.graphVizImage2)
        
        # Create title
        titleLabel = QLabel("Finally started on this project")
        testingMessage =  "HAHA"
        self.testingMessageLabel = QLabel(testingMessage)
        
        mainLayout = QGridLayout()

        mainLayout.addWidget(self.queryText1, 0, 0)
        mainLayout.addWidget(self.queryDropDown1, 1, 0)
        mainLayout.addWidget(generateButton1, 2, 0)
        mainLayout.addWidget(explainText1, 3, 0)
        mainLayout.addWidget(self.graphVizImage1, 4, 0)

        mainLayout.addWidget(self.queryText2, 0, 1)
        mainLayout.addWidget(self.queryDropDown2, 1, 1)
        mainLayout.addWidget(generateButton2, 2, 1)
        mainLayout.addWidget(explainText2, 3, 1)
        mainLayout.addWidget(self.graphVizImage2, 4, 1)

        mainLayout.setRowStretch(0, 0)
        mainLayout.setRowStretch(1, 0)
        mainLayout.setRowStretch(2, 0)
        mainLayout.setRowStretch(3, 0)
        mainLayout.setRowStretch(4, 1)
        mainLayout.setColumnStretch(0, 1)
        mainLayout.setColumnStretch(1, 1)
        # mainLayout = QHBoxLayout()
        # mainLayout.addLayout(query1VL)
        # mainLayout.addLayout(query2VL)
        # Set the main layout for the widget
        self.setLayout(mainLayout)
        
    def setTestingMessage(self, message):
        #self.testingMessageLabel.setText(message)
        self.queryText1.setText(message)

    def updateLineEdit(self, index):
        index = self.queryDropDown1.currentIndex()
        if index == 0:
            self.queryText1.setText("")
        elif index == 1:
            self.queryText1.setText(str(index))
            self.queryDropDown2.clear()
            #TODO Read from text/csv file
            #for each x in fileread:
            self.queryDropDown2.addItem("x1")
            self.queryDropDown2.addItem("y1")
        elif index == 2:
            self.queryText1.setText(str(index))
            self.queryDropDown2.clear()
            #TODO Read from text/csv file
            #for each x in fileread:
            self.queryDropDown2.addItem("x2")
            self.queryDropDown2.addItem("y2")
        else:
            self.queryText1.setText(str(index))
    def carryOverText(self):
        self.queryText2.setText(self.queryText1.toPlainText())

    #generate old query order
    def generateOldOrder(self):
        query = self.queryText1.toPlainText()
        result = self.queryDB(query,self.connection)
        #print(result)
        self.leftadj, self.leftlist = self.treeDisplay(result["Plan"],1)
        
        
    def queryDB(self,query,connection):
        cursor = connection.cursor()
        cursor.execute(
                f"EXPLAIN (FORMAT JSON) {'''{}'''}".format(query))
        return cursor.fetchall()[0][0][0]

    def generateNewOrder(self):
        query = self.queryText2.toPlainText()
        result = self.queryDB(query,self.connection)
        #print(result)
        self.rightadj, self.rightlist = self.treeDisplay(result["Plan"],2)
        output = generateDifference(self.leftadj,self.leftlist,self.rightadj,self.rightlist)

    
    def treeDisplay(self, plan,index):
        #TODO Display the difference in red, maybe split into another function?
        f = graphviz.Graph()

        #query = self.textEdit.toPlainText()
        #plan = self.dbObj.getQueryPlan(query)
        
        if type(plan) is not dict:
            self.el1.setText(f'ERROR: Tree visualisation failed. Please check your query.\n{plan}')
        else:
            adjList = self.getAdjList(plan, {})[0]
            #print("adj List: ",adjList)
            nodeList = self.nodeList
            #print("Node List: ",nodeList)

            self.nodeCount = 1
            self.nodeList = list()

            for node in nodeList:
                name = node.split('#')[0]
                print(node, name)
                f.node(node, name)

            for annotate in adjList:
                if len(adjList[annotate]) != 0:
                    for annotateString in adjList[annotate]:
                        f.edge(annotate, annotateString)

            f.render("QueryPlan", format="png", view=False)

            self.im = QPixmap("./QueryPlan.png")
            if(index == 1):
                self.graphVizImage1.setPixmap(self.im)
                self.graphVizImage1.setScaledContents(True)
                self.graphVizImage1.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignHCenter)

            else:
                self.graphVizImage2.setPixmap(self.im)
                self.graphVizImage2.setScaledContents(True)
            # self.graphVizImage2.setFixedHeight(self.im.size().height())
            # self.graphVizImage2.setFixedWidth(self.im.size().width())
                self.graphVizImage2.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignHCenter)
            
            
            return adjList, nodeList

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
            self.nodeList.append(
                f"{queryPlan['Relation Name']}#{self.nodeCount}")
            planNode = f"{queryPlan['Node Type']}#{self.nodeCount}"
            if planNode in result:
                result[planNode].append(f"{queryPlan['Relation Name']}#{self.nodeCount}")
            else:
                #print("HIII ", subplan)
                result[planNode] = [f"{queryPlan['Relation Name']}#{self.nodeCount}"]
            
            #print("map this ", queryPlan['Node Type'], " to ", queryPlan['Relation Name'])
            #result[queryPlan['Node Type']] = queryPlan['Relation Name']
            curIterCount = self.nodeCount
            self.nodeCount += 1
            return [result, curIterCount]

        # Node with child nodes
        else:
            # Name the parent node, increment the count
            planNodeType = f"{queryPlan['Node Type']}#{self.nodeCount}"
            print("parent: ", queryPlan['Node Type'], " and ", self.nodeCount)
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
                
                    
            #print("finall", result)
            # return curIterCount (OR, in the 1st iteration, return the final result)
            return [result, curIterCount]

    




