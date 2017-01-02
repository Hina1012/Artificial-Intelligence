import operator;
# class queue for BFS, UCS and A* which will be FIFO
class Queue:
    def __init__(self):
        self.list = []

    def enqueue(self, node):
        self.list.append(node)

    def dequeue(self):
        return self.list.pop(0)

    def readNode(self):
        return self.list[0]

    def IsNotEmpty(self):
        if len(self.list) == 0:
            return 0
        else:
            return 1
    def nodeNotInQueue(self, node):
        if(node not in self.list):
            return 1

#class stack for DFS which is LIFO
class Stack:
    def __init__(self):
        self.list = []

    def push(self, node):
        self.list.append(node)

    def pop(self):
        return self.list.pop()

    def IsNotEmpty(self):
        if len(self.list) == 0:
            return 0
        else:
            return 1
    def readNode(self, top):
        return self.list[top]

class Search:
    path_queue = Queue()
    path_stack = Stack()
    open_queue = Queue()
    closed_queue = Queue()
    children = Queue()
    visited = list()
    path_final = list()
    prev = {}
    def __init__(self):
        if(algo == "BFS"):
            Search.path_queue.enqueue(start)

        elif(algo == "DFS"):
            Search.path_stack.push(start)

        elif(algo == "UCS"):
            Search.open_queue.enqueue((start, 0))

        elif(algo == "A*"):
            Search.open_queue.enqueue((start, 0, adj_Dict_h[start]))

        Search.prev[start] = -1
        Search.visited = [start]

    def bfs(self, vertex):
        while (search.path_queue.IsNotEmpty()):
            nodeDequeue = search.path_queue.dequeue()
            if nodeDequeue in adj_Dict.keys():
                for i in range(0, len(adj_Dict[nodeDequeue])):
                    node = adj_Dict[nodeDequeue][i]
                    if (node not in search.visited):
                        search.visited.append(node)
                        search.prev[node] = nodeDequeue
                        search.path_queue.enqueue(node)
        nodeVal = goal
        if(goal in search.prev.keys()):
            while (search.prev[nodeVal] != -1):
                search.path_final.append(nodeVal)
                nodeVal = search.prev[nodeVal]
            if (search.prev[nodeVal] == -1):
                search.path_final.append(start)
            search.path_final.reverse()
            level = 0
            w = open("output.txt", "w")
            for item in search.path_final:
                output = '{} {}'.format(item, level)
                w.write(output + "\n")
                level += 1

        else:
            print "goal not present"

    def dfs(self, vertex):
        top = 0
        while (search.path_stack.IsNotEmpty()):
            if(search.path_stack.readNode(top) == goal):
                break
            else:
                nodeDequeue = search.path_stack.pop()
                top -= 1
                if (nodeDequeue in adj_Dict.keys()):
                    for i in range(len(adj_Dict[nodeDequeue]), 0, -1):
                        node = adj_Dict[nodeDequeue][i-1]
                        if(node not in search.visited):
                            search.prev[node] = nodeDequeue
                            search.path_stack.push(node)
                            search.visited.append(node)
                            top += 1

        nodeVal = goal
        while (search.prev[nodeVal] != -1):
            search.path_final.append(nodeVal)
            nodeVal = search.prev[nodeVal]

        if (search.prev[nodeVal] == -1):
            search.path_final.append(start)
        search.path_final.reverse()
        level = 0
        w = open("output.txt", "w")
        for item in search.path_final:
            output = '{} {}'.format(item, level)
            w.write(output + "\n")
            level += 1

    def ucs(self, vertex):
        while(1):
            if(search.open_queue.IsNotEmpty()):
                cur = search.open_queue.dequeue()
                curnode = cur[0]
                curnode_cost = cur[1]
            if(curnode == goal):
                return (curnode, curnode_cost)
            if(curnode in adj_Dict_ucs.keys()):
                for i in range(0, len(adj_Dict_ucs[curnode])):
                    search.children.enqueue(adj_Dict_ucs[curnode][i])

                while(search.children.IsNotEmpty()):
                    case = "0"
                    child = search.children.dequeue()
                    for item in search.open_queue.list:
                        if item[0] == child[0]:
                            child_cost_2 = int(curnode_cost)+int(child[1])
                            case = "2"
                            break

                    for item1 in search.closed_queue.list:
                        if(item1[0] == child[0]):
                            child_cost_3 = int(curnode_cost)+int(child[1])
                            case = "3"
                            break
                    if(case != "2" and case != 3):
                        case = "1"
                    if case == "1":#(search.open_queue.nodeNotInQueue(child[0]) or search.closed_queue.nodeNotInQueue(child[0])):
                        cost = int(curnode_cost)+int(child[1])
                        childWithTotalCost = (child[0], cost)
                        search.open_queue.enqueue(childWithTotalCost)
                        search.prev[child[0]] = curnode
                    elif (case == "2"):
                        openQueueItem = [item for item in search.open_queue.list if(item[0] == child[0])]

                        if(child_cost_2 < openQueueItem[0][1]):

                            search.open_queue.list.remove((openQueueItem[0]))
                            childNew = (child[0], child_cost_2)
                            search.open_queue.enqueue(childNew)
                            search.prev[childNew[0]] = curnode
                    elif (case == "3"):
                        closeQueueItem = [item for item in search.closed_queue.list if (item[0] == child[0])]
                        if (child_cost_3 < closeQueueItem[0][1]):
                            search.closed_queue.list.remove((closeQueueItem[0]))
                            childNew = (child[0], child_cost_3)
                            search.open_queue.enqueue(childNew)
                            search.prev[childNew[0]] = curnode


            curnodewithCost = (curnode, curnode_cost)
            search.closed_queue.enqueue(curnodewithCost)
            search.open_queue.list.sort(key = operator.itemgetter(1))


    def aStar(self, vertex):
        while (1):
            if (search.open_queue.IsNotEmpty()):
                cur = search.open_queue.dequeue()

                curnode = cur[0]
                curnode_cost = cur[1]
                curnode_h = cur[2]
            if (curnode == goal):
                return (curnode, curnode_cost)
            if (curnode in adj_Dict_ucs.keys()):
                for i in range(0, len(adj_Dict_ucs[curnode])):
                    search.children.enqueue(adj_Dict_ucs[curnode][i])
                while (search.children.IsNotEmpty()):
                    case = "0"
                    child = search.children.dequeue()
                    for item in search.open_queue.list:
                        if item[0] == child[0]:
                            child_cost_2 = int(curnode_cost) + int(child[1])
                            case = "2"
                            break

                    for item1 in search.closed_queue.list:
                        if (item1[0] == child[0]):
                            child_cost_3 = int(curnode_cost) + int(child[1])
                            case = "3"
                            break

                    if(case != "2" and case != "3"):
                        case = "1"

                    if case == "1":  # (search.open_queue.nodeNotInQueue(child[0]) or search.closed_queue.nodeNotInQueue(child[0])):
                        cost = int(curnode_cost) + int(child[1])
                        child_h = adj_Dict_h[child[0]]
                        child_cost_tot = int(child_h) + int(cost)
                        childWithTotalCost = (child[0], cost, child_cost_tot)
                        search.open_queue.enqueue(childWithTotalCost)
                        search.prev[child[0]] = curnode

                    elif (case == "2"):
                        openQueueItem = [item for item in search.open_queue.list if (item[0] == child[0])]

                        child_cost_tot_2 = int(adj_Dict_h[child[0]]) + int(child_cost_2)
                        if (child_cost_tot_2 < openQueueItem[0][2]):
                            search.open_queue.list.remove((openQueueItem[0]))
                            childNew = (child[0], child_cost_2, child_cost_tot_2)

                            search.open_queue.enqueue(childNew)
                            search.prev[childNew[0]] = curnode

                    elif (case == "3"):
                        closeQueueItem = [item for item in search.closed_queue.list if (item[0] == child[0])]
                        child_cost_tot_3 = int(adj_Dict_h[child[0]]) + int(child_cost_3)
                        if (child_cost_tot_3 < closeQueueItem[0][2]):
                            search.closed_queue.list.remove((closeQueueItem[0]))

                            childNew = (child[0], child_cost_3, child_cost_tot_3)
                            search.open_queue.enqueue(childNew)
                            search.prev[childNew[0]] = curnode


            curnode_h = int(curnode_cost) + int(adj_Dict_h[curnode])
            curnodewithCost = (curnode, curnode_cost, curnode_h)
            search.closed_queue.enqueue(curnodewithCost)
            search.open_queue.list.sort(key=operator.itemgetter(2))


inputList = []
algo = ''
start = ''
goal = ''
f = open('input.txt', 'r+')
i = 0
for line in f:
    if(line != ''):
        inputList.insert(i, line.strip())
        i += 1


inputList = filter(None, inputList)
adj_Dict = {}
adj_Dict_ucs = {}
adj_Dict_h = {}
value_h = []
value_ucs = []

algo = inputList[0].strip()
start = inputList[1].strip()
goal = inputList[2].strip()

if algo == "BFS" or algo == "DFS":
    for i in range(4, 4 + int(inputList[3])):
        key = inputList[i].split()[0]
        if key in adj_Dict.keys():
            value = adj_Dict[key]
            value.append(inputList[i].split()[1])
        else:
            value = [inputList[i].split()[1]]
        adj_Dict[key] = value
    search = Search()
    if(algo == "BFS"):
        path = search.bfs(start)
    else:
        search.dfs(start)

elif algo == "UCS":
    for i in range(4, 4 + int(inputList[3])):
        key_ucs = inputList[i].split()[0]
        if key_ucs in adj_Dict_ucs.keys():
            value_ucs = adj_Dict_ucs[key_ucs]
            value_ucs.append((inputList[i].split()[1], inputList[i].split()[2]))
        else:
            value_ucs = [(inputList[i].split()[1], inputList[i].split()[2])]
        adj_Dict_ucs[key_ucs] = value_ucs

    search = Search()
    item4 = search.ucs(start)
    nodeVal = goal
    while (search.prev[nodeVal] != -1):
        search.path_final.append(nodeVal)
        nodeVal = search.prev[nodeVal]

    if (search.prev[nodeVal] == -1):
        search.path_final.append(start)
    search.path_final.reverse()

    level = 0
    w = open("output.txt", "w")
    for item in search.path_final:
        for item1 in search.closed_queue.list:

            if(item == item1[0]):
                output = '{} {}'.format(item, item1[1])
                w.write(output + "\n")
    outputGoal = '{} {}'.format(item4[0], item4[1])
    w.write(outputGoal)

elif algo == "A*":
    startIndex = 4 + int(inputList[3])
    for j in range(startIndex + 1, startIndex + 1 + int(inputList[startIndex])):
        key_h = inputList[j].split()[0]
        value_h = inputList[j].split()[1]
        adj_Dict_h[key_h] = value_h

    search = Search()
    item5 = search.aStar(start)

    nodeVal = goal
    while (search.prev[nodeVal] != -1):
        search.path_final.append(nodeVal)
        nodeVal = search.prev[nodeVal]

    if (search.prev[nodeVal] == -1):
        search.path_final.append(start)
    search.path_final.reverse()

    level = 0
    w = open("output.txt", "w")
    for item in search.path_final:
        for item1 in search.closed_queue.list:

            if (item == item1[0]):
                output = '{} {}'.format(item, item1[1])
                w.write(output + "\n")
                print output
    print "item5", item5
    outputGoal = '{} {}'.format(item5[0], item5[1])
    w.write(outputGoal)
    print outputGoal