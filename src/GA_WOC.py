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
    shape = 1
    rankPaths = sorted(paths, key=lambda p: 1 / p.weight)
    rsum = sum(math.pow(x, shape) for x in range(1, len(rankPaths) + 1))
    parents = []
    for i in range(0, 2):
        r = random.uniform(0, rsum)
        for j in range(0, len(rankPaths)):
            r -= (math.pow(j + 1, shape))
            if r <= 0:
                parents.append(rankPaths[j].nodes)
                break
    return parents


def randReverse(parents):
    rands = sorted([random.randint(0, numCities - 1) for i in range(2)])
    rands = []
    for i in range(0, 2):
        rands.append(random.randint(0, numCities - 1))
    rands.sort()
    child = parents[0][rands[0]:rands[1]][::-1]
    for i in (parents[1]):
        if i not in child:
            child.append(i)
    return (child[-rands[0]:] + child[:-rands[0]])


def crossover(paths):
    newPath = sorted(paths, key=lambda p: 1 / p.weight)[1:]
    child = Path(randReverse(selParents()))
    child = mutate(child)
    newPath.append(child)
    return newPath


def randDisplace(pNodes, rands):
    pNodes.insert(rands[1], pNodes.pop(rands[0]))


def mutate(path):
    rands = []
    for i in range(0, 2):
        rands.append(random.randint(1, numCities - 1))
    if random.uniform(0, 1) < mutRate:
        randDisplace(path.nodes, rands)
        path.weight = pathDistance(path.nodes)
    return path


def wOCMax(paths):
    edgeSums = [x[:] for x in [[0] * numCities] * numCities]
    citiesRemaining = [x for x in range(0, numCities)]
    cityCount = [0, 0, 0]
# Generate edge sums matrix
    for p in paths:
        for i in range(0, len(p.nodes)):
            edgeSums[p.nodes[i]][p.nodes[i - 1]] += 1
            edgeSums[p.nodes[i - 1]][p.nodes[i]] += 1
    child = []
# Find most common edge and start
    for i in range(0, len(edgeSums)):
        for j in range(0, len(edgeSums[i])):
            if cityCount[0] < edgeSums[i][j]:
                cityCount = [edgeSums[i][j], i, j]
    child.append(cityCount[1])
    citiesRemaining.remove(cityCount[1])
    child.append(cityCount[2])
    citiesRemaining.remove(cityCount[2])
    for i in range(0, numCities):
        edgeSums[i][cityCount[1]] = -1
        edgeSums[i][cityCount[2]] = -1
# Find most common neighbor from previous neighbor for rest of child
    while len(child) < numCities:
        cityCount[0] = -1
        lastCity = cityCount[2]
        for i in range(0, numCities):
            if cityCount[0] < edgeSums[lastCity][i]:
                cityCount = [edgeSums[lastCity][i], lastCity, i]
        for j in range(0, numCities):
            edgeSums[j][cityCount[2]] = -1
        child.append(cityCount[2])
# Replace worst parent with new child
    childPath = Path(child)
    newPath = sorted(paths, key=lambda p: 1 / p.weight)[1:]
    if childPath.weight <= newPath[len(newPath) - 1].weight:
        newPath.append(childPath)
        wocSpot.append(numChildren - 1)
    else:
        for i in range(0, len(newPath)):
            if childPath.weight > newPath[i].weight:
                newPath.insert(i, childPath)
                wocSpot.append(i)
                break
    return newPath


def printStats(mutRate):
    low = min(p.weight for p in paths)
    high = max(p.weight for p in paths)
    avg = stats.mean(p.weight for p in paths)
    stdev = stats.pstdev(p.weight for p in paths)
    print('Shortest: ' + str(low))
    print('Longest: ' + str(high))
    print('Average: ' + str(avg))
    print('Standard Deviation: ' + str(stdev))


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

wocSpot = []
numGens = 100000
numChildren = 100
numCities = len(Nodes)
mutRate = .2
its = 1
mPath = []
for _ in range(0, its):
    paths = []
    for i in range(0, int(numChildren)):
        temp = random.sample(range(1, numCities), numCities - 1)
        temp.insert(0, 0)
        paths.append(Path(temp))
    for i in range(0, numGens):
        paths = crossover(paths)
        if (i % 10 == 9):
            wOCMax(paths)
        curLow = [min(paths, key=lambda x: x.weight).nodes]
        curLow.append(pathDistance(curLow[0]))
        if (len(mPath) < 1 or mPath[1] > curLow[1]):
            mPath = list(curLow)
        if (i % 1000 == 999):
            low = min(p.weight for p in paths)
            printStats(mutRate)
            print("Current low: " + str(low))
            print()
            print('Time: ' + str(time.time() - start))
            canvas.delete('all')
            drawScene(min(paths, key=lambda x: x.weight).nodes)
            canvas.pack()
            top.update_idletasks()
            top.update()
    end = time.time()
    print('Time: ' + str(end - start))
for i in range(0, len(mPath[0])):
    mPath[0][i] += 1
print('Optimal: ' + str(mPath) + ' Average WoC Position: ' +
      str(stats.mean(wocSpot)) + ' # of Gens: ' + str(numGens))
print(wocSpot)
