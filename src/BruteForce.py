import math
import time


def cityDistance(c1, c2):
    return math.sqrt(math.pow(c1[1] - c2[1], 2) + math.pow(c1[2] - c2[2], 2))


def pathDistance(path):
    dis = 0
    for i in range(0, len(path)):
        dis += distanceLookup[path[i]][path[i - 1]]
    return dis


def permute(num, master):
    permutation = []
    length = len(master)
    for i in range(0, length - 1):
        changeNum = math.factorial(length - i - 1)
        permutation.append(master.pop(num // changeNum))
        num %= changeNum
    permutation.append(master.pop(0))
    return permutation


def pick2(master):
    if (master[-1] < len(master) - 1):
        swap = master.index(master[-1] + 1)
        master[-1], master[swap] = master[swap], master[-1]
    elif(master[-1] - master[1] > 1):
        swap = master.index(master[1] + 1)
        master[1], master[swap] = master[swap], master[1]
        swap = master.index(master[1] + 1)
        master[-1], master[swap] = master[swap], master[-1]
    else:
        pass
    return master


start = time.time()
Nodes = []
with open('../Data/Random10.tsp', 'r') as f:
    for i in range(0, 7):
        f.readline()
    for line in f:
        line = line.split()
        Nodes.append([float(line[0]), float(line[1]), float(line[2])])
    f.close()

numCities = len(Nodes)

distanceLookup = []
for i in range(0, numCities):
    distanceLookup.append([])
    for j in range(0, numCities):
        distanceLookup[-1].append(cityDistance(Nodes[i], Nodes[j]))


masterPath = [0, 1]
for i in range(3, numCities):
    masterPath.append(i)
masterPath.append(2)
minDist = pathDistance(masterPath)
outerLoopLength = ((numCities - 1) * (numCities - 2)) // 2
innerLoopLength = math.factorial(numCities - 3)
optimalPath = list(masterPath)
for i in range(0, outerLoopLength):
    midPath = masterPath[2:-1]
    for i in range(0, innerLoopLength):
        d = pathDistance(masterPath)
        if (d < minDist):
            optimalPath = list(masterPath)
            minDist = d
        masterPath[2:-1] = permute(i, list(midPath))
    masterPath[2:-1] = reversed(masterPath[2:-1])
    pick2(masterPath)
end = time.time()
print(minDist)
for i in range(0, len(optimalPath)):
    optimalPath[i] += 1
print(optimalPath)
print(end - start)
