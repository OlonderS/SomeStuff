import pandas as pd
import numpy as np
import random

data = pd.read_excel("Dane_S2_200_20.xlsx", index_col=0)

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

def nSolutions(data, n):
    solutions = []
    times = []
    for i in range(n):
        solution = getRandomSolution(data)
        time = fullTimeSum(solution)
        solutions.append(solution)
        times.append(time)
    return solutions, times

def tournament(solutions, times):
    random.shuffle(solutions)
    
    solutions1 = solutions[:int(len(times)/2)]
    times1 = times[:int(len(times)/2)]
    solutions2 = solutions[int(len(times)/2):]
    times2 = times[int(len(times)/2):]
    
    min1 = min(times1)
    parent1 = solutions1[times1.index(min1)]
    ind1 = times1.index(min1)
    times1.pop(ind1)
    solutions1.pop(ind1)
    min2 = min(times2)
    parent2 = solutions2[times2.index(min2)]
    ind2 = times2.index(min2)
    times2.pop(ind2)
    solutions2.pop(ind2) 
    
    solutions = solutions1+solutions2
    times = times1+times2
    return parent1, parent2, solutions, times

def ox(p1, p2, maskLen):
    #Random place to cut data
    start = random.randint(0, len(p1)-maskLen-1)
    stop = start + maskLen

    #Empty arrays for childs and childs indexes
    child1 = np.full((p1.shape[0],p1.shape[1]),-1)
    child1Index = np.full(p1.shape[0],-1)
    child2 = np.full((p1.shape[0],p1.shape[1]),-1)
    child2Index = np.full(p1.shape[0],-1)  
    
    #Numpy arrays of parents, and parents indexes
    p1np = p1.to_numpy()
    p1Index = p1.index.to_numpy()
    p2np = p2.to_numpy()
    p2Index = p2.index.to_numpy()
    #Not changing one part of parent
    for i in range(start, stop):
        child1[i] = p1np[i]
        child1Index[i] = p1Index[i]
        child2[i] = p2np[i]
        child2Index[i] = p2Index[i]

    j = stop
    i = stop
    
    while i != start:
        if i == len(p1):
            i = 0
        if j == len(p1):
            j = 0
        if p1Index[j] in child2Index:
            j = j+1
        else:
            child2Index[i] = p1Index[j]
            child2[i] = p1np[j]
            i += 1
            j += 1
        
    j = stop
    i = stop
    
    while i != start:
        if i == len(p2):
            i = 0
        if j == len(p2):
            j = 0
        if p2Index[j] in child1Index:
            j = j+1
        else:
            child1Index[i] = p2Index[j]
            child1[i] = p2np[j]
            i += 1
            j += 1
        

    child1 = pd.DataFrame(data=child1,index=child1Index, columns=data.columns)
    child2 = pd.DataFrame(data=child2,index=child2Index, columns=data.columns)
    return child1, child2
    
def crossing(data, solutions, crosses, maskLen):
    solutions, times = nSolutions(data, solutions)
    newSolutions = []
    for i in range(crosses):
        p1, p2, solutions, times = tournament(solutions, times)
        c1, c2 = ox(p1,p2, maskLen)
        newSolutions.append(c1)
        newSolutions.append(c2)
        newSolutions.append(p1)
        newSolutions.append(p2)
        
    newSolutions = newSolutions + solutions
    return newSolutions
    
def selectNBest(solutions, n):
    times = []
    for sol in solutions:
        times.append(fullTimeSum(sol))
    
    while len(solutions) > n:
        maxT = max(times)
        ind = times.index(maxT)
        times.pop(ind)
        solutions.pop(ind)
    return solutions
    
def mutate(solutions):
    i = random.randint(0, len(solutions)-1)
    solution = solutions[i]
    task1 = random.randint(0, len(solution)-1)
    task2 = random.randint(0, len(solution)-1)
    sol = solution.copy()
    index1 = sol.iloc[task1].name
    index2 = sol.iloc[task2].name
    sol.rename(index={index1:index2, index2:index1},inplace=True)
    sol.iloc[task1] = solution.iloc[task2]
    sol.iloc[task2] = solution.iloc[task1]
    solutions[i] = sol
    return solutions
    
def genetic(data, iterations, population, crosses, mutations, maskLen):
    for i in range(iterations):
        print(i)
        solutions = crossing(data, population, crosses, maskLen)
        solutions = selectNBest(solutions,population)
        for j in range(mutations):
            solutions = mutate(solutions)
        
        solution = selectNBest(solutions, 1)
    return solution[0]

sol = genetic(data, 25, 30, 15, 5, 160)
print(fullTimeSum(sol))
sol.to_excel("genetic/genetic_25_30_15_5_160_1.xlsx")

sol = genetic(data, 25, 30, 10, 5, 160)
print(fullTimeSum(sol))
sol.to_excel("genetic/genetic_25_30_10_5_160_1.xlsx")

sol = genetic(data, 25, 60, 30, 5, 160)
print(fullTimeSum(sol))
sol.to_excel("genetic/genetic_25_60_30_5_160_1.xlsx")

sol = genetic(data, 25, 60, 20, 5, 160)
print(fullTimeSum(sol))
sol.to_excel("genetic/genetic_25_60_20_5_160_1.xlsx")

sol = genetic(data, 25, 30, 15, 5, 40)
print(fullTimeSum(sol))
sol.to_excel("genetic/genetic_25_30_15_5_40_1.xlsx")

sol = genetic(data, 25, 30, 10, 5, 40)
print(fullTimeSum(sol))
sol.to_excel("genetic/genetic_25_30_10_5_40_1.xlsx")

sol = genetic(data, 25, 60, 30, 5, 40)
print(fullTimeSum(sol))
sol.to_excel("genetic/genetic_25_60_30_5_40_1.xlsx")

sol = genetic(data, 25, 60, 20, 5, 40)
print(fullTimeSum(sol))
sol.to_excel("genetic/genetic_25_60_20_5_40_1.xlsx")

sol = genetic(data, 25, 30, 15, 5, 80)
print(fullTimeSum(sol))
sol.to_excel("genetic/genetic_25_30_15_5_80_1.xlsx")

sol = genetic(data, 25, 30, 10, 5, 80)
print(fullTimeSum(sol))
sol.to_excel("genetic/genetic_25_30_10_5_80_1.xlsx")

sol = genetic(data, 25, 60, 30, 5, 80)
print(fullTimeSum(sol))
sol.to_excel("genetic/genetic_25_60_30_5_80_1.xlsx")

sol = genetic(data, 25, 60, 20, 5, 80)
print(fullTimeSum(sol))
sol.to_excel("genetic/genetic_25_60_20_5_80_1.xlsx")