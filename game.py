def solver():
    """
    Input: None
    Output: None
    (MAIN PROGRAM TO SOLVE THE RIVER CROSSING COUPLE PROBLEM.
     PROVIDES HUMAN READABLE VERSION OF THE SOLUTION)
    """
    allStates = genStates() #store all possible states in 'allStates'
    graph = genGraph(allStates) #generate the graph and store it in 'graph'
    start = 'EEEEEEE' #starting pooint assigned to start
    dest = 'WWWWWWW' #ending point assigned to dest
    path = findShortestPath(graph, start, dest) #find shorest path, store the list returned into 'path'
    genTrip(path) #generate a meaningful, human readable version of the path

def genStates():
    """
    Input: None
    Output: Gives/returns all the possible states 
    """
    directions = ('E', 'W') #possible directions
    states = [] #list to store all states is initialised
    for a in directions: #for green wife
        for b in directions: #for green husband
            for c in directions: #for red wife
                for d in directions: #for red husband
                    for e in directions: #for blue wife
                        for f in directions: #for blue husband
                            for g in directions: #for boat
                                thisState = a+b+c+d+e+f+g
                                states.append(thisState)
    return tuple(states) 

def genGraph(S):
    """
    Input: a tuple containing all possible states
    Output: a graph consisting of all legal nodes, including their links to other nodes
    """
    legalStates = [] #initialising list to store all the legal states
    graph = {} #empty graph (initialisation)
    for n in S:
        if isItLegal(n) == True: #check if the state is legal
            legalStates.append(n) #if the state is legal, it is appended to the list of all legal states
    for m in legalStates:
        nextNodes = findNextStates(m, legalStates) #finding the nodes that link to 'm' node, and storing them in 'nextNodes'
        graph[m] = nextNodes #update the graph by adding the legal states and their corresponding linking states
    return graph

def isItLegal(s):
    """
    Input: a state 's'
    Output: True returned when the state is legal, false returned when its illegal 
    """
    #check if green wife is not currently with her husband and with atleast one of the other men
    if s[0] != s[1] and (s[0] == s[3] or s[0] == s[5]): 
        return False
    #check if red wife is not currently with her husband and with atleast one of the other men
    elif s[2] != s[3] and (s[2] == s[1] or s[2] == s[5]): 
        return False
    #check if blue wife is not currently with her husband and with atleast one of the other men
    elif s[4] != s[5] and (s[4] == s[1] or s[4] == s[3]):
        return False
    #check if all the people are on a different side than the boat:
    elif s[0]==s[1]==s[2]==s[3]==s[4]==s[5] and s[0]!= s[6]:
        return False
    #else, the state is legal
    else:
        return True

def findNextStates(stt, legalStates):
    """
    Inputs: stt: a legal node whose links we need to find out & legalStates: a set of all the legal states
    Output: return linking states as a set of nodes that are linked to the state 'stt'
    """
    linkingStates = set() #initialised as a set to avoid repititions (if any)
    east, west = setPos(legalStates) #classifying states through boat position into two catagories, east and west ones

    if stt[6] == 'W': #if the boat is on the west
        comparingStates = east #the states to compare and to link are the ones that are on the east side
    else: #if the boat is on the east
        comparingStates = west #the states to compare and to link are the ones that are on the west side
    for n in comparingStates:
        if isLinked(stt, n) == True: #compare each of the possible states, to check whether they can be linked to 'stt'
            linkingStates.add(n) #add 'n', that is the linked state, to the set data type : 'linkingStates'
    return linkingStates #the set of nodes that links to the node we called the function with, is returned

def setPos(allStates):
    """
    Input: allStates: all the legal states in a list
    Output: east: list of states from these legal states when boat is on the east.
            west: list of states from these legal states when boat is on the east.
    """
    east = [] #list initialised, to store states in which boat is on the eastern side
    west = [] #list initialised, to store states in which boat is on the western side
    for s in allStates:
        if s[6] == 'W': #if boat is on west side (we know that boat's index position is 6 in the string 's')
            west.append(s)
        else:  #if boat is on east side
            east.append(s)
    return east, west

def isLinked(legalStt, possibleState):
    """
    Inputs: legalStt: a legal state from the set of all legal states & possibleState: a legal state that can possibly be linked to the legal state
    Output: return True if 'possibleState' is linked to 'legalStt' 
    """
    c = 0 #initialising the counter to 0
    idxList = [] #add the index of changed position(s) to the list for later validation
    for i in range(len(legalStt)-1): #no need to compare boat as we already limited the states in 'findNextStates' to ensure validity
        if legalStt[i] != possibleState[i]: #if the states of the compared entities are different
            c = c + 1 #increment the counter for every change found
            idxList.append(i) #append the index of the changed position to the list
    if isChangeCorrect(legalStt, idxList) and (1 <= c <= 2): #if only 1 or 2 people travel at a time, the tranision is then assumed to be valid
        return True
    else:
        return False

def isChangeCorrect(stt, thisList):
    """
    Input: stt: one of the state from legal states & thisList: a list which contain the index of the changing psoition
    Output: True returned if all of the changed positions are same as the position of the boat
            False returned of all of the changed positions are not same as the position of the boat
    """
    for i in thisList:
        if stt[i] != stt[6]: #check if the transitions/changed positions are same as boat position
            return False
    return True

# You are not expected to implement this function.
# You should have the skill of finding a suitable implementation
# to help solve the program.
def findShortestPath(graph, start, end, path=[]):
    """
    A function to find a shortest path from start to end on a graph
    This function is obtained from https://www.python.org/doc/essays/graphs/
    with one change due to the deprecation of the method has_key().
    
    Input: A graph, a starting node, an end node and an empty path
    Output: Return the shortest path in the form of a list.
    """
    
    path = path + [start]
    if start == end:
        return path
#    if not graph.has_key(start):
    if not (start in graph):
        return None
    shortestPath = None
    for node in graph[start]:
        if node not in path:
            newpath = findShortestPath(graph, node, end, path)
            if newpath :
                if not shortestPath or len(newpath) < len(shortestPath):
                    shortestPath = newpath
    return shortestPath

def genTrip(path):
    """
    Input: one of the shortest possible paths to take all people from east to west without violating any conditions
    Output: returns nothing but prints human readable version of the path (in a meaningful format)
    """
    goTo = 'the west'
    goFrom = 'the east'
    
    people = ['green wife', 'green husband', 'red wife', 'red husband', 'blue wife', 'blue husband']
    #name of each person saved in the list 'people' corresponding to their indexes in the states
    #so that printing can be done using the same loop

    loopRuns = len(path)-1 #no. of times that the loop would run (from 0 to the value assigned)
    for m in range(loopRuns):
        changesList = [] #a list to save changing postion/positions
        for n in range(len(path[0])-1):
            if path[m][n] != path[m+1][n]: #compare 'm'th and 'm+1'th states
                changesList.append(n) #append the changed states to the list to print them later

        #the use of formatting to print in a more readable way
        if len(changesList) == 1: #when only one person changed their positions
            print(f'{m+1} The {people[changesList[0]]} goes from {goFrom} to {goTo}.')
        else: #when 2 people change their position
            print(f'{m+1} The {people[changesList[0]]} and {people[changesList[1]]} go from {goFrom} to {goTo}.')
            
        goTo, goFrom = goFrom, goTo #shuffle the positions since the path is reversed now

        #The output can vary each time since there are lots of possible ways to solve this problem
        #So there might be different ouputs if you run the program many times
        #But the solution is always correct, since there are alot of possibilities here

solver() #calling the main program to generate the solution 
