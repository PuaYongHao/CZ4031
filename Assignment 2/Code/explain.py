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
relation = ["customer", "lineitem","nation","orders","part","partsupp","region","supplier"]

#TODO
#Nid do for all the above algo print out some random english text
#either split into multiple python file that have 1 function to return a string
#or just do switch statement


def statement(nodeType):
    if nodeType == "hash_join":
        return
    elif nodeType == "index_scan":
        return
    else:
        return

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
    print("order of left tree")
    print(outputLeft)
    print("")
    print("i love this assignment")
    print("")
    print("order of right tree")
    print(outputRight)

    return outputLeft, outputRight