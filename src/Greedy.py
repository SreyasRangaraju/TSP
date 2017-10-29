import math
import time
import tkinter


class Node():

    def __init__(self, num, x, y):
        self.num = num
        self.x = x
        self.y = y
        self.dist = -1
        self.edge = -1
        self.dType = -1
        # 0 = edge, 1 = node


def cityDistance(c1, c2):
    return math.sqrt(math.pow(c1.x - c2.x, 2) + math.pow(c1.y - c2.y, 2))


def cityEdgeDistance(c0, c1, c2):
    dists = []
    dists.append(cityDistance(c0, c1))
    dists.append(cityDistance(c1, c2))
    dists.append(cityDistance(c2, c0))
    if(math.pow(min(dists[0], dists[2]), 2) + math.pow(dists[1], 2) <=
       math.pow(max(dists[0], dists[2]), 2)):
        if (dists[0] < dists[2]):
            return [dists[0], 0, 1]
        else:
            return [dists[2], 1, 1]
    else:
        top = ((c2.y - c1.y) * c0.x - (c2.x - c1.x) * c0.y +
               c2.x * c1.y - c2.y * c1.x)
        bot = math.sqrt(math.pow(c2.y - c1.y, 2) + math.pow(c2.x - c1.x, 2))
        return [math.fabs(top / bot), None, 0]


def findClosestNode(cnode, EdgeNode):
    n1 = [0, 200]
    d = 0
    for n in Nodes:
        if (not EdgeNode):
            d = cityDistance(n, cnode)
        else:
            d = cityEdgeDistance(n, cnode, EdgeNode)[0]
        if (d < n1[1]):
            n1 = [n, d]
    return n1[0]


def pathDistance(tpath):
    dsum = 0
    for i in range(1, len(tpath)):
        dsum += cityDistance(tpath[i - 1], tpath[i])
    return dsum


def drawScene():
    for n in Nodes:
        canvas.create_oval(scale * n.x - radius, scale * n.y - radius,
                           scale * n.x + radius, scale * n.y + radius)
    for n in path:
        canvas.create_oval(scale * n.x - radius, scale * n.y - radius,
                           scale * n.x + radius, scale * n.y + radius)
    for i in range(0, len(path) - 1):
        canvas.create_line(scale * path[i].x, scale * path[i].y,
                           scale * path[i + 1].x, scale * path[i + 1].y)
    canvas.create_line(scale * path[0].x, scale * path[0].y,
                       scale * path[-1].x, scale * path[-1].y)


scale = 5
radius = 3
top = tkinter.Tk()
canvas = tkinter.Canvas(top, height=scale * 100, width=scale * 100)

numNodes = -1
while(True):
    order = []
    canvas.delete('all')
    start = time.time()
    Nodes = []
    with open('../Data/Random40.tsp', 'r') as f:
        for i in range(0, 7):
            f.readline()
        for line in f:
            line = line.split()
            Nodes.append(Node(int(line[0]) - 1, float(line[1]),
                              float(line[2])))
        f.close()

    numCities = len(Nodes)
    path = []
    xsum = 0
    ysum = 0

    # First 3 nodes
    for n in Nodes:
        xsum += n.x
        ysum += n.y
    icnode = Node(0, xsum / len(Nodes), ysum / len(Nodes))
    path.append(Nodes.pop(Nodes.index(findClosestNode(icnode, None))))
    path.append(Nodes.pop(Nodes.index(findClosestNode(path[0], None))))
    path.append(Nodes.pop(Nodes.index(findClosestNode(path[0], path[1]))))
    for n in path:
        order.append(n.num)

    # Sort into edges/nodes
    d = []
    for n in Nodes:
        for i in range(0, 3):
            d = cityEdgeDistance(n, path[i], path[(i + 1) % 3])
            if (n.dist == -1 or n.dist > d[0]):
                n.dist = d[0]
                n.dType = d[2]
                if (d[1]):
                    n.edge = (i + d[1]) % 3
                else:
                    n.edge = i

    # Main Loop
    for i in range(0, numNodes):
        Nodes.sort(key=lambda Node: Node.dist)
        n1 = Nodes.pop(0)
        order.append(n1.num)
        if (n1.dType == 0):
            key = n1.edge
            path.insert(n1.edge + 1, n1)
        else:
            if(cityDistance(n1, path[(n1.edge - 1) % len(path)]) -
               cityDistance(path[n1.edge], path[(n1.edge - 1) % len(path)]) <
               cityDistance(n1, path[(n1.edge + 1) % len(path)]) -
               cityDistance(path[n1.edge], path[(n1.edge + 1) % len(path)])):
                if (n1.edge == 0):
                    key = len(path) - 1
                    path.insert(len(path), n1)
                else:
                    key = n1.edge - 1
                    path.insert(n1.edge, n1)
            else:
                key = n1.edge
                path.insert(n1.edge + 1, n1)
        for n in Nodes:
            if (n.edge > key):
                n.edge += 1
            for i in range(0, 2):
                d = cityEdgeDistance(
                    n, path[key + i], path[(key + 1 + i) % len(path)])
                if (n.dist > d[0]):
                    n.dist = d[0]
                    n.dType = d[2]
                    if (d[1]):
                        n.edge = (key + i + d[1]) % len(path)
                    else:
                        n.edge = (key + i) % len(path)

    drawScene()
    canvas.pack()
    end = time.time()
    print(end - start)
    pathNums = []
    for n in path:
        pathNums.append(n.num)
    for i in range(0, len(order)):
        order[i] += 1
        pathNums[i] += 1
    print('Order of inserted cities: ' + str(order))
    print('Path of cities: ' + str(pathNums))
    print('Total distance: ' + str(pathDistance(path)))
    top.update_idletasks()
    top.update()
    while(numNodes < 0 or numNodes > numCities - 3):
        numNodes = int(input('Enter the number of cities between 0 and {} \n'.
                             format(numCities - 3)))
