import math
import time


class Node():
    def __init__(self, num, x, y):
        self.num = num
        self.x = x
        self.y = y
        self.dist = 0
        self.backPtr = -1


def cityDistance(c1, c2):
    return math.sqrt(math.pow(c1.x - c2.x, 2) + math.pow(c1.y - c2.y, 2))


def DFS(curCity, mPath, mPathLength, mins):
    if curCity > 6:
        mPathLength += cityDistance(Nodes[curCity], Nodes[10])
        mPath.append(10)
        if mins[0] < 0 or mPathLength < mins[0]:
            mins[0] = mPathLength
            mins[1] = list(mPath)
    else:
        for city in connections[curCity]:
            path = list(mPath)
            pathLength = mPathLength
            pathLength += cityDistance(Nodes[curCity], Nodes[city])
            path.append(city)
            DFS(city, list(path), pathLength, mins)


def BFS(queue, mins):
    if len(queue) > 0 and queue[0] != 10:
        city = Nodes[queue.pop(0)]
        if (city.num < 7):
            for connect in connections[city.num]:
                if connect not in queue:
                    queue.append(connect)
                newDist = city.dist + cityDistance(city, Nodes[connect])
                if newDist < Nodes[connect].dist or Nodes[connect].dist == 0:
                    Nodes[connect].dist = newDist
                    Nodes[connect].backPtr = city
        else:
            if 10 not in queue:
                queue.append(10)
            newDist = city.dist + cityDistance(city, Nodes[10])
            if newDist < Nodes[10].dist or Nodes[10].dist == 0:
                    Nodes[10].dist = newDist
                    Nodes[10].backPtr = city
        BFS(queue, mins)
    else:
        backCity = Nodes[10]
        mins[0] = backCity.dist
        while backCity.num > 0:
            mins[1].append(backCity.backPtr.num)
            backCity = backCity.backPtr
        mins[1].reverse()


start = time.time()
Nodes = []
with open('../Data/DFS_BFS_Only.tsp', 'r') as f:
    for i in range(0, 7):
        f.readline()
    for line in f:
        line = line.split()
        Nodes.append(Node(int(line[0]) - 1, float(line[1]), float(line[2])))
    f.close()

connections = [[1, 2, 3], [2], [3, 4], [4, 5, 6], [6, 7],
               [7], [8, 9], [8, 9, 10], [10], [10]]


minsDFS = [-1, []]
DFS(0, list([0]), 0, minsDFS)

minsBFS = [0, [10]]
BFS([0], minsBFS)


for i in range(0, len(minsDFS[1])):
    minsDFS[1][i] += 1
    minsBFS[1][i] += 1
end = time.time()

print(end - start)
print('DFS' + str(minsDFS))
print('BFS' + str(minsBFS))
