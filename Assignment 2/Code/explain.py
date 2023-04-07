#natural language
#switch statement or some shit

# generic
# nested_loop
# sequential_scan
# index_scan
# hash_join
# limit
# merge_join
# setop
# sort
# materialize
# aggregate
# subquery_scan
# unique
# values_scan
# group
# hash
# function_scan
# cte_scan
# append

#TODO
#Nid do for all the above algo print out some random english text
#either split into multiple python file that have 1 function to return a string
#or just do switch statement

#check if node is a join operator
def isJoin(nodeType):
    join_elements = ["Nested Loop","Hash Join", "Merge Join"]
    if nodeType.split("#")[0] in join_elements:
        return True
    else:
        return False

#for each relation/table, generate from the relation node up to the root node
def findSequence(adjMatrix,relation,parent):
    result = [relation,parent]
    for iteration in range(len(adjMatrix)):
        for node in adjMatrix:
            #print(node)
            for child in adjMatrix[node]:
                #print(child)
                if child == parent:
                    #print("found parent: ",node)
                    result.append(node)
                    parent = node
    return result

# find and output the differences of the different scanning method of tables(if any)
# e.g. result from table scanning:  ['Old query Seq Scan from customer table have been changed to Index Scan']
# e.g. result from table scanning:  ['Both queries scanning method of tables are the same']
def findDifferencesBetweenRelations(outputLeft,outputRight,relation):
    #collect all the relation names of the right output
    leftOutput = []
    for oldList in range(0,len(outputLeft)):
        stop = 0
        tempListL = []
        for node in range(0, len(outputLeft[oldList])):
            if isJoin(outputLeft[oldList][node]):
                leftOutput.append(tempListL)
                break
            tempListL.append(outputLeft[oldList][node].split("#")[0])
    
    rightOutput = []
    for newList in range(0,len(outputRight)):
        stop = 0
        tempListL = []
        for node in range(0, len(outputRight[newList])):
            if isJoin(outputRight[newList][node]):
                rightOutput.append(tempListL)
                break
            tempListL.append(outputRight[newList][node].split("#")[0])
    #print("hehe ",leftOutput)
    #print("hehe ",rightOutput)

    #generate message of what LHS have but RHS dont have
    leftMessage = []
    for i in range(0,len(leftOutput)):
        for j in range(0,len(rightOutput)):
            if leftOutput[i][0] == rightOutput[j][0]:
                #found the 2 list to compare
                for eachNode in leftOutput[i]:
                    if eachNode not in rightOutput[j]:
                        leftMessage.append(leftOutput[i][0]+"-"+eachNode)
                        #print(leftOutput[i][0]," ",eachNode," don't have")
    #print("gap")
    #generate message of what RHS have but LHS dont have
    rightMessage = []
    for i in range(0,len(rightOutput)):
        for j in range(0,len(leftOutput)):
            if rightOutput[i][0] == leftOutput[j][0]:
                #found the 2 list to compare
                for eachNode in rightOutput[i]:
                    if eachNode not in leftOutput[j]:
                        rightMessage.append(rightOutput[i][0]+"-"+eachNode)
                        #print(rightOutput[i][0]," ",eachNode," don't have")

    #print(leftMessage)
    #print(rightMessage)
    finalMessage = []
    if len(leftMessage)==0 and len(rightMessage)==0:
        finalMessage.append("Both queries scanning method of tables are the same")
    else:
        for i in range(0,len(leftMessage)):
            for j in range(0,len(rightMessage)):
                if leftMessage[i].split("-")[0] == rightMessage[j].split("-")[0]:
                    finalMessage.append("Old query "+leftMessage[i].split("-")[1]+" from "+leftMessage[i].split("-")[0]+" table have been changed to "+rightMessage[j].split("-")[1])
    

    return finalMessage

#generate the join order 
# e.g. ['customer#10', 'nation#12', 'orders#7'] means ((customer JOIN nation) JOIN orders)
def findOrderOfJoin(outputLeft,outputRight,relation):
    joinTypes = []
    joinDict = {}
    leftJoinOrder = []
    rightJoinOrder = []
    joinOrder = []
    joinOrderR = []

    #for left output
    for i in range(0,len(outputLeft)):
        for j in range(0,len(outputLeft[i])):
            if isJoin(outputLeft[i][j]) and outputLeft[i][j] not in joinTypes:
                joinTypes.append(outputLeft[i][j])
    #if only 1 type of join, it means there is only 2 relation
    if len(joinTypes) == 1:
        for i in range(0, len(outputLeft)):
            leftJoinOrder.append(outputLeft[i][0])
        joinOrder = joinTypes
    elif len(joinTypes) == 0:
        leftJoinOrder = []
    else:
        #preload all join to value 0 in a dictionary
        for joinType in joinTypes:
            joinDict[joinType] = 0
        
        #remove all filler nodes which is not a relation or join type
        #at the same time increment the join counter into the dict
        tempOutputLeft = []
        for i in range(0,len(outputLeft)):
            tempList = []
            for j in range(0,len(outputLeft[i])):
                if outputLeft[i][j].split("#")[0] in relation or outputLeft[i][j] in joinTypes:
                    tempList.append(outputLeft[i][j])
                    if outputLeft[i][j] in joinTypes:
                        joinDict[outputLeft[i][j]] += 1
            tempOutputLeft.append(tempList)
            #outputLeft[i] = tempList

        joinDict = dict(sorted(joinDict.items(), key=lambda x:x[1]))
        #print(outputLeft)
        #print("order of the dictionary from smallest to largest value",joinDict)

        joinOrder = list(joinDict.keys())
        #print(joinOrder)
        visited = []
        for i in range(0,len(joinOrder)):
            for j in range(0,len(tempOutputLeft)):
                if tempOutputLeft[j][1] == joinOrder[i] and tempOutputLeft[j][0] not in visited:
                    visited.append(tempOutputLeft[j][0])
                    leftJoinOrder.append(tempOutputLeft[j][0])

    #for right output
    joinTypesR = []
    joinDictR = {}
    for i in range(0,len(outputRight)):
        for j in range(0,len(outputRight[i])):
            if isJoin(outputRight[i][j]) and outputRight[i][j] not in joinTypesR:
                joinTypesR.append(outputRight[i][j])
    #if only 1 type of join, it means there is only 2 relation
    if len(joinTypesR) == 1:
        for i in range(0, len(outputRight)):
            rightJoinOrder.append(outputRight[i][0])
        joinOrderR = joinTypesR
    elif len(joinTypesR) == 0:
        rightJoinOrder = []
    else:
        #preload all join to value 0 in a dictionary
        for joinType in joinTypesR:
            joinDictR[joinType] = 0
        
        #remove all filler nodes which is not a relation or join type
        #at the same time increment the join counter into the dict
        tempOutputRight = []
        for i in range(0,len(outputRight)):
            tempList = []
            for j in range(0,len(outputRight[i])):
                if outputRight[i][j].split("#")[0] in relation or outputRight[i][j] in joinTypesR:
                    tempList.append(outputRight[i][j])
                    if outputRight[i][j] in joinTypesR:
                        joinDictR[outputRight[i][j]] += 1
            tempOutputRight.append(tempList)
            #outputRight[i] = tempList

        joinDictR = dict(sorted(joinDictR.items(), key=lambda x:x[1]))
        #print(outputRight)
        #print("order of the dictionary from smallest to largest value",joinDictR)
        
        joinOrderR = list(joinDictR.keys())
        #print(joinOrderR)
        visitedR = []
        for i in range(0,len(joinOrderR)):
            for j in range(0,len(tempOutputRight)):
                if tempOutputRight[j][1] == joinOrderR[i] and tempOutputRight[j][0] not in visitedR:
                    visitedR.append(tempOutputRight[j][0])
                    rightJoinOrder.append(tempOutputRight[j][0])

    # print("left join order: ",leftJoinOrder)
    # print("right join order: ",rightJoinOrder)

    finalJoinOperator =[joinOrder,joinOrderR]

    # print(finalJoinOperator)
    return leftJoinOrder,rightJoinOrder, finalJoinOperator


# "main" function of the explain class that calls the other sub function of the class
def generateDifference(leftA,leftL,rightA,rightL):
    relation = ["customer", "lineitem","nation","orders","part","partsupp","region","supplier"]
    #print(leftA)
    #print("length is ",len(leftA))
    #implement post order traversal to generate the list
    outputLeft = []
    outputRight = []
    #findSequence(leftA,"orders#7","Seq Scan#7")
    for table in relation:
        #print("now searching: ",table)
        for node in leftA:
            for child in leftA[node]:
                if child.split("#")[0] == table:
                    outputLeft.append(findSequence(leftA,child,node))

    for table in relation:
        #print("now searching: ",table)
        for node in rightA:
            for child in rightA[node]:
                if child.split("#")[0] == table:
                    outputRight.append(findSequence(rightA,child,node))
    # print("order of left tree")
    # print(outputLeft)
    # print("")
    # print("i love this assignment")
    # print("")
    # print("order of right tree")
    # print(outputRight)

    joinOrderLeft, joinOrderRight, joinOperator = findOrderOfJoin(outputLeft,outputRight,relation)
    scanMessage = findDifferencesBetweenRelations(outputLeft,outputRight,relation)

    print("left side relation join order: ",joinOrderLeft)
    print("right side relation join order: ",joinOrderRight)
    print("join order from both sides: ",joinOperator,"<-- this is not done yet pls compare and output differences")
    print("result from table scanning: ",scanMessage)
    

    return outputLeft, outputRight