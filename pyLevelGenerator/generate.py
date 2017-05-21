
# generates square map of X and Y's
from math import sqrt, e, log, floor
from random import random
from time import time

project_path = "C:\\Projects\\GeneratedScripts\\maps\\"
print_grid = False

def main():


    #path = project_path + 'groundMap.json'
    generateNMaps(1000) # cant go over 500x500 in unity

def generateNMaps(n):
    i = 5
    ii = 1

    x = 1
    while x < n and ii <= 11:
        y = x
        while y <= x and ii <= 11:
            tstart = time()
            width, length = (x, y)
            print "----------\n", ii ,"\nsize:", width * length, "[w:"+str(width)+"]", "[h:"+str(length)+"]"
            generateGridToFile(width, length, project_path + 'groundMap'+str(ii)+'.json')
            t2 = time()
            print str(t2-tstart)

            if t2-tstart > 60*2:
                return
            i = int(i*1.5)
            ii += 1
            y+=i

        x += i


def generateGridToFile(width, length, path):
    grid = makeGrid(width, length)

    # choose a few random points, and calculate what height to take
    take = findOptimalHeight(grid, width, length)
    grid = weightGrid(grid, width, length, take)
    grid = addGroundAtr(grid, width, length) # how much ground is visible
    trees = heightGeneratedTrees(grid, width, length)
    saveAsJson(grid, width, length,path)


def heightGeneratedTrees(grid, width, length):
    eh = expectedHeight(grid, width, length)
    maxh = maxHeight(grid, width, length)
    # everything x% above expected height is a tree
    trees = list()
    for i in range(width):
        for j in range(length):
            if (grid[i][j]-eh)/maxh > 0.3: # check if value is above the avg, and more than 30% of height
                sizeofBush = random()*20 # up to 20 squres per bush
                trees.append(generateTree(sizeofBush, i, j, trees))

    return trees

def generateTree(sizeofBush, i, j, tress):
    dfdsfd
    # generate tree populates the area around the given point, by adding in plus shape,
    # shape is added by making array of offset coordinates from the given point
    # then also check if there are any doubles, via by making offset array that goes from 0,0,0

    # bonus: every side being optional in every iteration



def addGroundAtr(grid, width, length):
    # find min height around the slot, and add ground to it
    for i in range(width):
        for j in range(length):
            grid[i][j] = (grid[i][j], findMinHeightAround(grid, width, length, i, j))
    return grid

def findMinHeightAround(grid, width, length, x, y):
    min = grid[x][y]
    if (x > 0 and grid[x - 1][y] < min): # if items are in last row, then skip check on them
        min = grid[x - 1][y]
    if (x < width-1 and grid[x + 1][y] < min):
        min = grid[x + 1][y]
    if (y > 0 and grid[x][y - 1] < min):
        min = grid[x][y - 1]
    if (y < length-1 and grid[x][y + 1] < min):
        min = grid[x][y + 1]
    return min


def saveAsJson(grid, width, length, path):
    json = ""
    for i in range(width):
        for j in range(length):
            json += '{ "x":'+str(i)+', "y":'+str(j)+', "height":'+str(list(grid[i][j]))+'},\n'
    json = '{ "info":"height[height, visible ground]", "grid":[\n'+json+'] }'
    with open(path, "w") as the_file:
        the_file.write(json)

def findOptimalHeight(grid, width, length):
    focalPoints = list(chooseHills(grid, width, length))
    avgh = avgHeight(focalPoints, grid)

    maxh = maxHeight(grid, width, length)
    take = (maxh *0.7+ avgh*0.3)
    return take

def expectedHeight(grid, width, length):
    sum = 0
    for i in range(width):
        for j in range(length):
           sum+= grid[i][j]
    return sum/width*length

def avgHeight(points, grid):
    avgsample = 0
    for i in points:
        x = i[0]
        y = i[1]
        h = grid[x][y]
        avgsample += h
    avgsample = int(avgsample / len(points))
    return avgsample

def weightGrid(grid, width, length, take):
    # apply some weight to the grid with another value. you could make scaling with this if you add proper params p1 and p2(*2+*0)
    for i in range(width):
        for j in range(length):
            grid[i][j] = int(min(grid[i][j] * 0.6 + take*0.4, take))
    return  grid


def maxHeight(grid, width, length):
    max = -1
    for i in range(width):
        for j in range(length):
            if grid[i][j] > max:
                max = grid[i][j]

    return max

def chooseHills(grid, width, length):
    num = max (1, int(log(width*length)))
    hills = set()
    for i in range(num):
        rngCoordinates = (int(random()*(width-1)), int(random()*length-1))
        hills.add(rngCoordinates)
    return hills


def makeGrid(width, length):
    x = list()
    for i in range(width):
        y = list()
        for j in range(length):
            y.append(stackOfRandoms(1))
        x.append(y)
        if print_grid:
            print y
    return x

def stackOfRandoms(x):
    blocks = [1,
             0]
    weights = [0.60,
               0.40]
    slot = weightedRandomItem(blocks, weights)
    if slot==1:
        return stackOfRandoms(x+1)
    if slot==0:
        return x

def weightedRandomItem(items, weights):
    rng = random()
    for i in range(len(items)-1):
        if rng < weights[i]:
            return items[i]
        rng -= weights[i]
    return items[-1]
    #if rng > 0.5:
    #    return "I"
    #elif rng <= 0.5:
    #    return "_"


if __name__ == "__main__":
    main()