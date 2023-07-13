import pandas as pd
import numpy as np

data = pd.read_excel("data2.xlsx", index_col=0)

def getRandomSolution(data):
    solution = data.iloc[np.random.permutation(len(data))]
    return solution

def fullTimeSum(data):
    sums = data.iloc[0:0]
    for i in range(data.shape[0]):
        # Jesli pierwszy rzad to zwykla suma
        if (i == 0):
            tempSum = []
            for j in range(data.shape[1]):
                # Jesli pierwsza kolumna w pierwszym rzedzie to zwykla wartosc
                if (j == 0):
                    tempSum.append(data.iloc[i, j])
                # W przeciwnym przypadku sumujemy
                else:
                    tempSum.append(tempSum[-1] + data.iloc[i, j])

        else:
            tempSum = []
            for j in range(data.shape[1]):

                # Jesli pierwsza kolumna to suma wartosci "powyzej" i obecnej
                if (j == 0):
                    temp = sums.iloc[i - 1, j] + data.iloc[i, j]
                    tempSum.append(temp)
                else:
                    temp = max(tempSum[-1] + data.iloc[i, j], sums.iloc[i - 1, j] + data.iloc[i, j])
                    tempSum.append(temp)
        sums.loc[len(sums)] = tempSum
    time = sums.iloc[-1, -1]
    return time

#funkcja ktora tworzy liste z sasiednimi rozwiazaniami
#n - decyduje o tym jak duze ma byc sasiedztwo
#tworzy liste ramek danych z mozliwymi kombinacjami ustawienia danych
#poprzez zamiany miejscami, przykladowo:
#zamiana 1 z 2, 1 z 3, 1 z 4, 2 z 3, 2 z 4, 3 z 4 - 6 kombinacji
def getNeighbours(solution,n):
    neighbours = []
    for i in range(n):
        for j in range(i+1,n):
            neighbour = solution.copy()
            neighbour.iloc[i] = solution.iloc[j]
            neighbour.iloc[j] = solution.iloc[i]
            neighbours.append(neighbour)
    return neighbours

#funkcja sluzaca do wybrania najlepszego z sasiednich rozwiazan
def getBestNeighbour(neighbours):
    bestLength = fullTimeSum(neighbours[0])
    bestNeighbour = neighbours[0]
    for neighbour in neighbours:
        currentLength = fullTimeSum(neighbour)
        if currentLength < bestLength:
            bestLength = currentLength
            bestNeighbour = neighbour
    return bestNeighbour, bestLength

def hillClimbing(data, n):
    currentSolution = getRandomSolution(data)  #pierwsze rozwiazanie wybierane jest losowo 
    #currentSolution = data
    currentLength = fullTimeSum(currentSolution)
    neighbours = getNeighbours(currentSolution, n)
    bestNeigbour, bestLegth = getBestNeighbour(neighbours)
    print(currentSolution)

    while bestLegth < currentLength:
        print(currentSolution)
        currentSolution = bestNeigbour
        currentLength = bestLegth
        neighbours = getNeighbours(currentSolution, n)
        bestNeigbour,bestLegth = getBestNeighbour(neighbours)

    return currentSolution, currentLength

def multiStart(data, n=10, starts=10):
    bestSolution, bestTime = hillClimbing(data, n)
    for i in range(starts-1):
        newSolution, newTime = hillClimbing(data, n)
        if newTime < bestTime:
            bestTime = newTime
            bestSolution = newSolution

    return bestSolution, bestTime
currentSolution, currentLength = multiStart(data)