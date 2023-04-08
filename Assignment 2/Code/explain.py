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
    #e.g. customer-Seq Scan
    leftMessage = []
    for i in range(0,len(leftOutput)):
        for j in range(0,len(rightOutput)):
            if leftOutput[i][0] == rightOutput[j][0]:
                #found the 2 list to compare
                tempList = []
                for eachNode in leftOutput[i]:
                    if eachNode not in rightOutput[j]:
                        tempList.append(leftOutput[i][0]+"-"+eachNode)
                        #leftMessage.append(leftOutput[i][0]+"-"+eachNode)
                        #print(leftOutput[i][0]," ",eachNode," don't have")
                if len(tempList) !=0:
                    leftMessage.append(tempList)
    #print("gap")
    #generate message of what RHS have but LHS dont have
    rightMessage = []
    for i in range(0,len(rightOutput)):
        for j in range(0,len(leftOutput)):
            if rightOutput[i][0] == leftOutput[j][0]:
                #found the 2 list to compare
                tempList = []
                for eachNode in rightOutput[i]:
                    if eachNode not in leftOutput[j]:
                        tempList.append(leftOutput[i][0]+"-"+eachNode)
                        #rightMessage.append(rightOutput[i][0]+"-"+eachNode)
                        #print(rightOutput[i][0]," ",eachNode," don't have")
                if len(tempList) !=0:
                    rightMessage.append(tempList)
    #leftMessage = [["customer-Seq Scan","customer-hash"]] #testing debug
    #rightMessage = [["customer-Index Scan","customer-hash Scan"]] #testing debug
    #print(leftMessage)
    #print(rightMessage)
    finalMessage = []
    if len(leftMessage)==0 and len(rightMessage)==0:
        finalMessage.append("Both queries scanning method of tables are the same")
    else:
        for i in range(0,len(leftMessage)):
            for j in range(0,len(rightMessage)):
                if leftMessage[i][0].split("-")[0] == rightMessage[j][0].split("-")[0]:
                    leftDiff = ""
                    rightDiff = ""
                    table = leftMessage[i][0].split("-")[0]
                    for values in leftMessage[i]:
                        leftDiff += values.split("-")[1] +", "
                    for values in rightMessage[j]:
                        rightDiff += values.split("-")[1]+", "
                    leftDiff = leftDiff[:-2]
                    rightDiff = rightDiff[:-2]
                    #print(leftDiff)
                    #print(rightDiff)
                    finalMessage.append("Old query "+leftDiff+" from "+table+" table have been changed to "+rightDiff)
        

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

#function to generate natural language on which tables are joined together first and the difference in join types
def findJoinChanges(joinOrderLeft,joinOrderRight,joinOperator):
    leftJoinMessage = []
    rightJoinMessage = []
    joinChangesMessage = []
    #e.g. e.g. list = ['customer#10', 'nation#12', 'orders#7']
    #first 2 indexes are joined first then the result is joined with the last index
    #if list is empty means no join
    #if list only has 2 table means only 1 join

    #generate join order of the old/left query
    if len(joinOrderLeft) ==0:
        leftJoinMessage.append("Old query has no join operations")
    elif len(joinOrderLeft) == 2:
        result = "Old query has only a join between ("+joinOrderLeft[0].split("#")[0]+" and "+joinOrderLeft[1].split("#")[0]+")"
        leftJoinMessage.append(result)
    else:
        firstJoin = "("+joinOrderLeft[0].split("#")[0]+" and "+joinOrderLeft[1].split("#")[0]+")"
        secondJoin = "("+joinOrderLeft[2].split("#")[0]+")"
        result = "Old query has a join of "+firstJoin+" first, then the result is joined with "+secondJoin
        leftJoinMessage.append(result)

    #generate join order of the new/right query
    if len(joinOrderRight) ==0:
        rightJoinMessage.append("New query has no join operations")
    elif len(joinOrderRight) == 2:
        result = "New query has only a join between ("+joinOrderRight[0].split("#")[0]+" and "+joinOrderRight[1].split("#")[0]+")"
        rightJoinMessage.append(result)
    else:
        firstJoin = "("+joinOrderRight[0].split("#")[0]+" and "+joinOrderRight[1].split("#")[0]+")"
        secondJoin = "("+joinOrderRight[2].split("#")[0]+")"
        result = "New query has a join of "+firstJoin+" first, then the result is joined with "+secondJoin
        rightJoinMessage.append(result)

    #generate the difference of joins
    #e.g. [['Hash Join#2', 'Hash Join#1'], ['Hash Join#6', 'Hash Join#5']] there will only be 2 lists:
    # 1st list = old query joins
    # 2nd list = new quest joins
    # the join orders are from bottom to top
    #joinOperator = [['Nested Loop Join#2', 'Nested Loop Join#1'], ['Hash Join#6', 'Hash Join#5']] #FOR DEBUG
    leftJoin = joinOperator[0]
    rightJoin = joinOperator[1]
    noChangeText = "Both the old query and new query join types have no changes"


    if len(leftJoin)==0 and len(rightJoin)==0:
        joinChangesMessage.append("Both old and new query has no join operations")
    elif len(leftJoin)==1 and len(rightJoin)==0:
        joinName = leftJoin[0].split("#")[0]
        result = "Old query's "+ joinName+" has been removed so new query has no join"
        joinChangesMessage.append(result)
    elif len(leftJoin)==0 and len(rightJoin)==1:
        joinName = rightJoin[0].split("#")[0]
        result = "Old query initially do not have a join but the new query has added a "+joinName+" join"
        joinChangesMessage.append(result)
    elif len(leftJoin)==1 and len(rightJoin)==1:
        leftJoinName = leftJoin[0].split("#")[0]
        rightJoinName = rightJoin[0].split("#")[0]
        if leftJoinName != rightJoinName:
            result = "Old query "+leftJoinName+" has been changed to "+rightJoinName
            joinChangesMessage.append(result)
        else:
            joinChangesMessage.append(noChangeText)
    elif len(leftJoin)==2 and len(rightJoin)==1:
        leftJoinName = leftJoin[0].split("#")[0] + " and "+leftJoin[1].split("#")[0]
        rightJoinName = rightJoin[0].split("#")[0]
        result = "Old query's "+leftJoinName +" has been changed to only "+rightJoinName
        joinChangesMessage.append(result)
    elif len(leftJoin)==1 and len(rightJoin)==2:
        leftJoinName = leftJoin[0].split("#")[0]
        rightJoinName = rightJoin[0].split("#")[0] + " and "+rightJoin[1].split("#")[0]
        result = "Old query's only "+leftJoinName +" has been changed to "+rightJoinName
        joinChangesMessage.append(result)
    else:
        if leftJoin[0].split("#")[0] == rightJoin[0].split("#")[0] and leftJoin[1].split("#")[0] == rightJoin[1].split("#")[0]:
            joinChangesMessage.append(noChangeText)
        else:
            #1st level different, 2nd level same
            if leftJoin[0].split("#")[0] != rightJoin[0].split("#")[0] and leftJoin[1].split("#")[0] == rightJoin[1].split("#")[0]:
                leftJoinName = leftJoin[0].split("#")[0]
                rightJoinName = rightJoin[0].split("#")[0]
                result = "Old query first level "+leftJoinName+" has been changed to "+rightJoinName+" in the new query"
                joinChangesMessage.append(result)
            #1st level same, 2nd level different
            elif leftJoin[0].split("#")[0] == rightJoin[0].split("#")[0] and leftJoin[1].split("#")[0] != rightJoin[1].split("#")[0]:
                leftJoinName = leftJoin[1].split("#")[0]
                rightJoinName = rightJoin[1].split("#")[0]
                result = "Old query second level "+leftJoinName+" has been changed to "+rightJoinName+" in the new query"
                joinChangesMessage.append(result)
            #1st level different, 2nd level different
            else:
                leftJoinName = leftJoin[0].split("#")[0] + " and "+leftJoin[1].split("#")[0]
                rightJoinName = rightJoin[0].split("#")[0] + " and "+rightJoin[1].split("#")[0]
                result = "Old query both joins ("+leftJoinName+") has been changed to ("+rightJoinName+") in the new query"
                joinChangesMessage.append(result)
        

    return leftJoinMessage, rightJoinMessage, joinChangesMessage


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
    scanChangesMessage = findDifferencesBetweenRelations(outputLeft,outputRight,relation)
    leftOrderOfJoinMessage, rightOrderOfJoinMessage, joinChangesMessage = findJoinChanges(joinOrderLeft,joinOrderRight,joinOperator)

    print("left side relation join order: ",joinOrderLeft)
    print("right side relation join order: ",joinOrderRight)
    print("join order from both sides: ",joinOperator)
    print("result from table scanning: ",scanChangesMessage)
    print("old query join order: ",leftOrderOfJoinMessage)
    print("new query join order: ",rightOrderOfJoinMessage)
    print("old and new query join differences:",joinChangesMessage)
    
    # compare the differences in joinOperator

    return outputLeft, outputRight