import pandas as pd
import numpy as np
import random

data = pd.read_excel("Dane_S2_50_10.xlsx", index_col=0)

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

def getNeighbours(solution,n):
    #data.rename(index={3:77},inplace=True)
    
    neighbours = []
    nList = []
    for i in range(n):
        for j in range(i+1,n):
            neighbour = solution.copy()
            index1 = neighbour.iloc[i].name
            index2 = neighbour.iloc[j].name
            neighbour.rename(index={index1:index2, index2:index1},inplace=True)
            neighbour.iloc[i] = solution.iloc[j]
            neighbour.iloc[j] = solution.iloc[i]            
            neighbours.append(neighbour)
            nList.append((index2,index1))
    return neighbours, nList

def getBestNeighbour(neighbours, nList):
    bestLength = 100000000000
    bestNeighbour = neighbours[0]
    bestList = (-1,-1)
    i = 0
    for neighbour in neighbours:
        currentLength = fullTimeSum(neighbour)
        if currentLength < bestLength:
            bestLength = currentLength
            bestNeighbour = neighbour
            bestList = nList[i]
        i += 1
    return bestNeighbour, bestLength, bestList

def DFtoRemove(l, df):
    copy = l.copy()
    df.reset_index(drop=True, inplace=True)
    i=0
    for d in copy:
        d.reset_index(drop=True, inplace=True)
        print(d.equals(df))
        if d.equals(df):
            return i
        i+=1
    return len(l)

def tabu(data, n, s, iterations):
    """
    

    Parameters
    ----------
    data : pandas DataFrame
        DESCRIPTION.
    n : integer
        number of neighbours.
    s : integer
        Length of tabu list.
    iterations : integer
        number of iterations.

    Returns
    -------
    None.

    """
    solution = getRandomSolution(data)
    print(fullTimeSum(solution))
    tabuList = []
    #Wykonujemy petle okreslona liczbe razy
    for i in range(iterations):
        print(tabuList)
        #Wygenerowanie sasiadow
        neighbours, nList = getNeighbours(solution, n)
        #Wybranie najlepszego sasiada, i dla tego sasiada, dlugosc i ktore miejsca zamienione byly
        bestNeighbour, bestLength, bestList = getBestNeighbour(neighbours, nList)
        #zamienione miejsca w odwroceonej kolejnosci
        #Dopoki jest para na liscie tabu to usuwamy ja z listy sasiadow
        swappedBestList = (bestList[1],bestList[0])
        while (bestList in tabuList) | (swappedBestList in tabuList):
            r = DFtoRemove(neighbours, bestNeighbour)
            nList.pop(r)         
            neighbours.pop(r)
            bestNeighbour, bestLength, bestList = getBestNeighbour(neighbours, nList)
            swappedBestList = (bestList[1],bestList[0])
        solution = bestNeighbour
        print(solution)
        #Sprawdzamy dlugosc listy tabu, jesli za dluga usuwamy pare, ktora jest najdluzej na liscie
        if(len(tabuList) >= s):
            tabuList.pop(0)
        tabuList.append(bestList)
        
    return solution, fullTimeSum(solution)

print(tabu(data, 10, 5, 10))
