import pandas as pd
import numpy as np
import random
import math

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

#Losowo wybrany sasiad z mozliwych opcji
def getNeighbour(solution,n):
    neighbours = []
    for i in range(n):
        for j in range(i+1,n):
            neighbour = solution.copy()
            index1 = neighbour.iloc[i].name
            index2 = neighbour.iloc[j].name
            neighbour.rename(index={index1:index2, index2:index1},inplace=True)
            neighbour.iloc[i] = solution.iloc[j]
            neighbour.iloc[j] = solution.iloc[i]
            neighbours.append(neighbour)
    neighbour = random.choice(neighbours)
    return neighbour

'''
parametry:
data- dane dla ktorych rozwiazujemy problem
T - poczatkowa temperatura, T>0
F - tempreatura zamrozenia,
L - ile razy ma sie wykonywac petla for
r - wspolczynnik wygaszania 
n - jak duze ma byc sasiedztwo dla rozwiazania
'''

def simulateDannealing(data,T,F,L,r,n):
    solution = getRandomSolution(data)
    print(fullTimeSum(solution))  #wynik dla pierwszego rozwiazania ktore jest losowe
    while (T>F):
        for i in range(L):
            adjacent_solution = getNeighbour(solution, n)
            delta = fullTimeSum(adjacent_solution) - fullTimeSum(solution)
            if delta < 0:
                solution = adjacent_solution
            else:
                p = math.exp(-delta/T) #obliczanie prawdopodobienstwa na przyjecie rozwiazanie mimo ze jest gorsze
                random_number = random.uniform(0,1)
                if (p > random_number):
                    solution = adjacent_solution
        T = T * r

    return solution, fullTimeSum(solution)

SD, sdtime = simulateDannealing(data, 1, 0.3, 10, 0.9, 15)

SD.to_excel("simulateDannealing/sd_T1_F03_L10_r09_n15_1.xlsx")

print(SD, sdtime)