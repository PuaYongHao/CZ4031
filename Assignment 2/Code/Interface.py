import sys
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtWidgets import QComboBox, QWidget, QLabel, QTextEdit, QPushButton, QGridLayout, QScrollArea, QApplication
from PyQt6.QtGui import QPixmap
import graphviz
from explain import generateDifference
import explain as ex


class SquareLineEdit(QTextEdit):
    def sizeHint(self):
        # Override sizeHint() to return a square size
        size = super().sizeHint()
        return QSize(max(size.width(), size.height()), max(size.width(), size.height()))


class MyWidget(QWidget):
    connection = None

    def __init__(self, password):
        super().__init__()

        MyWidget.connection.autocommit = True
        self.cursor = MyWidget.connection.cursor()

        self.nodeList = list()
        self.nodeCount = 1

        self.startCostList = list()
        self.costList = list()
        self.rowList = list()
        self.adjListWithPlansRowValue = list()

        # Query1
        self.queryText1 = SquareLineEdit()
        self.queryText1.setLineWrapColumnOrWidth(
            800)  # Here you set the width you want
        self.queryText1.setMinimumHeight(200)
        self.queryText1.setLineWrapMode(QTextEdit.LineWrapMode.FixedPixelWidth)
        self.queryText1.textChanged.connect(self.carryOverText)

        self.queryDropDown1 = QComboBox()
        self.queryDropDown1.addItem("None")
        for i in range(1, 8):
            self.queryDropDown1.addItem("Query"+str(i))
        self.queryDropDown1.currentIndexChanged.connect(self.updateLineEdit)

        self.generateButton1 = QPushButton()
        self.generateButton1.setText("generate")
        self.generateButton1.clicked.connect(self.generateOldOrder)

        self.explainText1 = SquareLineEdit()
        self.explainText1.setReadOnly(True)
        self.scrollExplainArea = QScrollArea()
        self.scrollExplainArea.setWidgetResizable(True)
        self.scrollExplainArea.setMinimumHeight(150)
        self.scrollExplainArea.setMinimumWidth(300)
        self.scrollExplainArea.setWidget(self.explainText1)

        self.graphVizImage1 = QLabel()
        self.scrollArea1 = QScrollArea()
        self.scrollArea1.setWidgetResizable(True)
        self.scrollArea1.setMinimumHeight(300)
        self.scrollArea1.setMinimumWidth(300)
        self.scrollArea1.setWidget(self.graphVizImage1)

        # Query2
        self.queryText2 = SquareLineEdit()
        self.queryText2.setLineWrapColumnOrWidth(
            800)  # Here you set the width you want
        self.queryText2.setMinimumHeight(200)
        self.queryText2.setLineWrapMode(QTextEdit.LineWrapMode.FixedPixelWidth)
        self.queryText2.setStyleSheet("color: rgb(255,0,0)")

        self.queryDropDown2 = QComboBox()
        self.queryDropDown2.currentIndexChanged.connect(self.getQuery2)

        self.generateButton2 = QPushButton()
        self.generateButton2.setText("generate")
        self.generateButton2.setEnabled(False)
        self.generateButton2.clicked.connect(self.generateNewOrder)

        self.graphVizImage2 = QLabel()
        self.scrollArea2 = QScrollArea()
        self.scrollArea2.setWidgetResizable(True)
        self.scrollArea2.setMinimumHeight(300)
        self.scrollArea2.setMinimumWidth(300)
        self.scrollArea2.setWidget(self.graphVizImage2)

        # Create title
        titleLabel = QLabel("Finally started on this project")
        testingMessage = "HAHA"
        self.testingMessageLabel = QLabel(testingMessage)

        mainLayout = QGridLayout()

        mainLayout.addWidget(self.queryText1, 0, 0)
        mainLayout.addWidget(self.queryDropDown1, 1, 0)
        mainLayout.addWidget(self.generateButton1, 2, 0)
        mainLayout.addWidget(self.scrollArea1, 3, 0)

        mainLayout.addWidget(self.queryText2, 0, 1)
        mainLayout.addWidget(self.queryDropDown2, 1, 1)
        mainLayout.addWidget(self.generateButton2, 2, 1)
        mainLayout.addWidget(self.scrollArea2, 3, 1)

        mainLayout.addWidget(self.scrollExplainArea, 4, 0, 1, 2)

        mainLayout.setRowStretch(0, 0)
        mainLayout.setRowStretch(1, 0)
        mainLayout.setRowStretch(2, 0)
        mainLayout.setRowStretch(3, 0)
        mainLayout.setRowStretch(4, 1)
        mainLayout.setColumnStretch(0, 1)
        mainLayout.setColumnStretch(1, 1)
        # Set the main layout for the widget
        self.setLayout(mainLayout)

    def updateLineEdit(self):
        index = self.queryDropDown1.currentIndex()
        self.generateButton2.setEnabled(False)
        if index == 0:
            self.queryText1.setText("")
            self.queryDropDown2.clear()
            self.queryDropDown2.setEnabled = False
        elif index == 1:
            fd = open('../Queries/1.sql', 'r')
            sqlFile = fd.read()
            fd.close()
            self.queryText1.setText(sqlFile)
            self.queryDropDown2.clear()
            self.queryDropDown2.setEnabled = True
            self.queryDropDown2.addItem("Query1 Enhanced1")
            self.queryDropDown2.addItem("Query1 Enhanced2")
        elif index == 2:
            fd = open('../Queries/2.sql', 'r')
            sqlFile = fd.read()
            fd.close()
            self.queryText1.setText(sqlFile)
            self.queryDropDown2.clear()
            self.queryDropDown2.setEnabled = True
            self.queryDropDown2.addItem("Query2 Enhanced1")
            self.queryDropDown2.addItem("Query2 Enhanced2")
        elif index == 3:
            fd = open('../Queries/3.sql', 'r')
            sqlFile = fd.read()
            fd.close()
            self.queryText1.setText(sqlFile)
            self.queryDropDown2.clear()
            self.queryDropDown2.setEnabled = True
            self.queryDropDown2.addItem("Query3 Enhanced1")
            self.queryDropDown2.addItem("Query3 Enhanced2")
        elif index == 4:
            fd = open('../Queries/4.sql', 'r')
            sqlFile = fd.read()
            fd.close()
            self.queryText1.setText(sqlFile)
            self.queryDropDown2.clear()
            self.queryDropDown2.setEnabled = True
            self.queryDropDown2.addItem("Query4 Enhanced1")
            self.queryDropDown2.addItem("Query4 Enhanced2")
        elif index == 5:
            fd = open('../Queries/5.sql', 'r')
            sqlFile = fd.read()
            fd.close()
            self.queryText1.setText(sqlFile)
            self.queryDropDown2.clear()
            self.queryDropDown2.setEnabled = True
            self.queryDropDown2.addItem("Query5 Enhanced1")
            self.queryDropDown2.addItem("Query5 Enhanced2")
        elif index == 6:
            fd = open('../Queries/6.sql', 'r')
            sqlFile = fd.read()
            fd.close()
            self.queryText1.setText(sqlFile)
            self.queryDropDown2.clear()
            self.queryDropDown2.setEnabled = True
            self.queryDropDown2.addItem("Query6 Enhanced1")
            self.queryDropDown2.addItem("Query6 Enhanced2")
        elif index == 7:
            fd = open('../Queries/7.sql', 'r')
            sqlFile = fd.read()
            fd.close()
            self.queryText1.setText(sqlFile)
            self.queryDropDown2.clear()
            self.queryDropDown2.setEnabled = True
            self.queryDropDown2.addItem("Query7 Enhanced1")
            self.queryDropDown2.addItem("Query7 Enhanced2")
        else:
            self.queryText1.setText("nothing to be found")

    def getQuery2(self):
        index = self.queryDropDown1.currentIndex()
        if (index == 0):
            return
        index2 = self.queryDropDown2.currentIndex()
        if (index2 + 1 <= 0):
            index2 = 1
        filename = ('../Queries/')
        filename = filename + str(index) + "Enhanced" + str(index2+1) + ".sql"
        fd = open(filename, 'r')
        sqlFile = fd.read()
        fd.close()
        self.queryText2.setText(sqlFile)

    # carry over text from the left text area to the right text area
    def carryOverText(self):
        text = self.queryText1.toPlainText()
        self.queryText2.setText(text)

    # take in old query and process
    def generateOldOrder(self):
        query = self.queryText1.toPlainText()
        self.result1 = self.queryDB(query)
        self.leftadj, self.leftlist, self.costListL, self.rowListL, self.startCostListL, self.adjListWithPlansRowValueL = self.treeDisplay(
            self.result1["Plan"], 1)
        self.generateButton2.setEnabled(True)

    # query postgres DB for join order
    def queryDB(self, query):
        cursor = MyWidget.connection.cursor()
        cursor.execute(
            f"EXPLAIN (FORMAT JSON) {'''{}'''}".format(query))
        return cursor.fetchall()[0][0][0]

    # take in new query and process
    def generateNewOrder(self):
        query = self.queryText2.toPlainText()
        self.result2 = self.queryDB(query)
        self.rightadj, self.rightlist, self.costListR, self.rowListR, self.startCostListR, self.adjListWithPlansRowValueR = self.treeDisplay(
            self.result2["Plan"], 2)
        outputL, outputR, resultMessage = generateDifference(self.leftadj, self.leftlist, self.rightadj,
                                                             self.rightlist, self.costListL, self.costListR,
                                                             self.rowListL, self.rowListR, self.startCostListL,
                                                             self.startCostListR, self.adjListWithPlansRowValueL, self.adjListWithPlansRowValueR)
        self.explainText1.setText(resultMessage)

    # print the image of the join order
    def treeDisplay(self, plan, index):
        f = graphviz.Graph()

        if type(plan) is not dict:
            self.el1.setText(
                f'ERROR: Tree visualisation failed. Please check your query.\n{plan}')
        else:
            adjList = self.getAdjList(plan, {})[0]
            nodeList = self.nodeList
            costList = self.costList
            rowList = self.rowList
            startCostList = self.startCostList
            adjListWithPlansRowValue = self.adjListWithPlansRowValue

            self.nodeCount = 1
            self.nodeList = list()
            self.startCostList = list()
            self.costList = list()
            self.rowList = list()
            self.adjListWithPlansRowValue = list()

            for node in nodeList:
                name = node.split('#')[0]
                f.node(node, name)

            for annotate in adjList:
                if len(adjList[annotate]) != 0:
                    for annotateString in adjList[annotate]:
                        f.edge(annotate, annotateString)

            f.render("QueryPlan", format="png", view=False)

            self.im = QPixmap("./QueryPlan.png")
            if (index == 1):
                self.graphVizImage1.setPixmap(self.im)
                self.graphVizImage1.setScaledContents(True)
                self.graphVizImage1.setAlignment(
                    Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignHCenter)

            else:
                self.graphVizImage2.setPixmap(self.im)
                self.graphVizImage2.setScaledContents(True)
                self.graphVizImage2.setAlignment(
                    Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignHCenter)

            return adjList, nodeList, costList, rowList, startCostList, adjListWithPlansRowValue

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
            self.startCostList.append(
                f"{queryPlan['Startup Cost']}#{self.nodeCount}")
            self.costList.append(
                f"{queryPlan['Total Cost']}#{self.nodeCount}")
            self.rowList.append(
                f"{queryPlan['Plan Rows']}#{self.nodeCount}")
            planNode = f"{queryPlan['Node Type']}#{self.nodeCount}"
            if planNode in result:
                result[planNode].append(
                    f"{queryPlan['Relation Name']}#{self.nodeCount}")
            else:
                result[planNode] = [
                    f"{queryPlan['Relation Name']}#{self.nodeCount}"]
            curIterCount = self.nodeCount
            self.nodeCount += 1
            return [result, curIterCount]

        # Node with child nodes
        else:
            # Name the parent node, increment the count
            planNodeType = f"{queryPlan['Node Type']}#{self.nodeCount}"
            if planNodeType not in self.nodeList:
                self.nodeList.append(planNodeType)

            # ifplanNodeType is join add it in
            if ex.isJoin(queryPlan['Node Type']):
                if ('Join Filter' in queryPlan):
                    self.adjListWithPlansRowValue.append(
                        f"{queryPlan['Node Type']}#{queryPlan['Join Filter']}#{queryPlan['Plans'][0]['Node Type']}|{queryPlan['Plans'][0]['Plan Rows']}#{queryPlan['Plans'][1]['Node Type']}|{queryPlan['Plans'][1]['Plan Rows']}")
                elif ('Hash Cond' in queryPlan):
                    self.adjListWithPlansRowValue.append(
                        f"{queryPlan['Node Type']}#{queryPlan['Hash Cond']}#{queryPlan['Plans'][0]['Node Type']}|{queryPlan['Plans'][0]['Plan Rows']}#{queryPlan['Plans'][1]['Node Type']}|{queryPlan['Plans'][1]['Plan Rows']}")
                elif ('Merge Cond' in queryPlan):
                    self.adjListWithPlansRowValue.append(
                        f"{queryPlan['Node Type']}#{queryPlan['Merge Cond']}#{queryPlan['Plans'][0]['Node Type']}|{queryPlan['Plans'][0]['Plan Rows']}#{queryPlan['Plans'][1]['Node Type']}|{queryPlan['Plans'][1]['Plan Rows']}")
                else:
                    self.adjListWithPlansRowValue.append(
                        f"{queryPlan['Node Type']}##{queryPlan['Plans'][0]['Node Type']}|{queryPlan['Plans'][0]['Plan Rows']}#{queryPlan['Plans'][1]['Node Type']}|{queryPlan['Plans'][1]['Plan Rows']}")
            self.startCostList.append(
                f"{queryPlan['Startup Cost']}#{self.nodeCount}")

            self.costList.append(f"{queryPlan['Total Cost']}#{self.nodeCount}")

            self.rowList.append(
                f"{queryPlan['Plan Rows']}#{self.nodeCount}")

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

            return [result, curIterCount]
