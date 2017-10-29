import math
import time
import tkinter
import random
import statistics as stats


class Node():

    def __init__(self, num, x, y):
        self.num = num - 1
        self.x = x
        self.y = y


class Path():

    def __init__(self, nodes):
        self.nodes = nodes
        self.weight = pathDistance(nodes)


def cityDistance(c1, c2):
    return math.sqrt(math.pow(c1.x - c2.x, 2) + math.pow(c1.y - c2.y, 2))


def pathDistance(tpath):
    dsum = 0
    for i in range(0, len(tpath)):
        dsum += cityDistance(Nodes[tpath[i - 1]], Nodes[tpath[i]])
    return dsum


def selParents():
    rankPaths = sorted(paths, key=lambda p: 1 / p.weight)
    rsum = numChildren * (numChildren + 1) / 2
    parents = []
    for i in range(0, 2):
        r = random.randint(1, rsum)
        for j in range(0, len(rankPaths)):
            r -= (j + 1)
            if r <= 0:
                parents.append(rankPaths[j].nodes)
                break
    return parents


def seqIns(parents):
    child = []
    iInd = 0
    jInd = 0
    for i in range(0, int(numCities / 2)):
        while parents[0][iInd] in child:
            iInd += 1
        child.append(parents[0][iInd])
        while parents[1][jInd] in child:
            jInd += 1
        child.append(parents[1][jInd])
    return child


def avgCities(parents):
    childTemp = [x[:] for x in [[]] * 2 * len(parents[0])]
    cityNum = -1
    child = []
    for i in range(0, numCities):
        cityNum = parents[0][i]
        childTemp[i + parents[1].index(cityNum)].append(cityNum)
    for ind in childTemp:
        child.extend(ind)
    return child


def crossover(paths):
    newPath = []
    for i in range(0, numChildren):
        parents = selParents()
        if crossVar:
            newPath.append(Path(seqIns(parents)))
        else:
            newPath.append(Path(avgCities(parents)))
    return newPath


def randSwap(pNodes, rands):
    pNodes[rands[0]], pNodes[rands[1]] = pNodes[rands[1]], pNodes[rands[0]]


def randDisplace(pNodes, rands):
    pNodes.insert(rands[1], pNodes.pop(rands[0]))


def mutate(paths):
    rands = []
    for i in range(0, 2):
        rands.append(random.randint(1, numCities - 1))
    if mutVar:
        for p in paths:
            if random.uniform(0, 1) < mutRate:
                randSwap(p.nodes, rands)
                p.weight = pathDistance(p.nodes)
    else:
        for p in paths:
            if random.uniform(0, 1) <= mutRate:
                randDisplace(p.nodes, rands)
                p.weight = pathDistance(p.nodes)
    return paths


def printStats():
    low = min(p.weight for p in paths)
    high = max(p.weight for p in paths)
    avg = stats.mean(p.weight for p in paths)
    stdev = stats.pstdev(p.weight for p in paths)
    print('Shortest: ' + str(low))
    print('Longest: ' + str(high))
    print('Average: ' + str(avg))
    print('Standard Deviation: ' + str(stdev))
    print()


def drawScene(path):
    for n in Nodes:
        canvas.create_oval(scale * n.x - radius, scale * n.y - radius,
                           scale * n.x + radius, scale * n.y + radius)
    for i in range(0, len(path) - 1):
        canvas.create_line(scale * Nodes[path[i]].x, scale * Nodes[path[i]].y,
                           scale * Nodes[path[i + 1]].x,
                           scale * Nodes[path[i + 1]].y)
    canvas.create_line(scale * Nodes[path[0]].x, scale * Nodes[path[0]].y,
                       scale * Nodes[path[-1]].x, scale * Nodes[path[-1]].y)


scale = 5
radius = 3
top = tkinter.Tk()
canvas = tkinter.Canvas(top, height=scale * 100, width=scale * 100)
random.seed()

start = time.time()
Nodes = []
with open('../Data/Random100.tsp', 'r') as f:
    for i in range(0, 7):
        f.readline()
    for line in f:
        line = line.split()
        Nodes.append(Node(int(line[0]) - 1, float(line[1]), float(line[2])))
    f.close()

numGens = 10000
numChildren = 50
numCities = len(Nodes)
crossVar = 0
mutVar = 0
mutRate = .02
its = 1
mPath = []
for i in range(0, its):
    paths = []
    for i in range(0, numChildren):
        temp = random.sample(range(1, numCities), numCities - 1)
        temp.insert(0, 0)
        paths.append(Path(temp))
    for i in range(0, numGens):
        paths = crossover(paths)
        paths = mutate(paths)
        curLow = [min(paths, key=lambda x: x.weight).nodes]
        curLow.append(pathDistance(curLow[0]))
        if (len(mPath) < 1 or mPath[1] > curLow[1]):
            mPath = list(curLow)
        if (i % 100 == 99):
            low = min(p.weight for p in paths)
            print(low)
            canvas.delete('all')
            drawScene(min(paths, key=lambda x: x.weight).nodes)
            canvas.pack()
            top.update_idletasks()
            top.update()
    printStats()
    end = time.time()
    print('Time: ' + str(end - start))
for i in range(0, len(mPath[0])):
    mPath[0][i] += 1
print('Optimal: ' + str(mPath))
