import pandas as pd

data = pd.read_excel("Dane_S2_50_10.xlsx", index_col=0)

def fullTimeSum(data):
    
    sums = data.iloc[0:0]
    for i in range(data.shape[0]):
        #Jesli pierwszy rzad to zwykla suma
        if(i==0):
            tempSum = []
            for j in range(data.shape[1]):
                #Jesli pierwsza kolumna w pierwszym rzedzie to zwykla wartosc
                if(j==0):
                    tempSum.append(data.iloc[i,j])
                #W przeciwnym przypadku sumujemy
                else:
                    tempSum.append(tempSum[-1]+data.iloc[i,j])

        else:
            tempSum = []
            for j in range(data.shape[1]):
                
                #Jesli pierwsza kolumna to suma wartosci "powyzej" i obecnej
                if(j==0):
                    temp = sums.iloc[i-1,j]+data.iloc[i,j]
                    tempSum.append(temp)
                else:
                    temp = max(tempSum[-1]+data.iloc[i,j], sums.iloc[i-1,j]+data.iloc[i,j])
                    tempSum.append(temp)
        sums.loc[len(sums)] = tempSum
    return sums
            
        
def SumAndSort(data):
    
    data["Sum"] = data.sum(axis=1)
    data.sort_values(by="Sum", inplace=True, ascending=False)
    return data.iloc[:,:-1]
        

def firstTwoTasks(sortedData):
    d = sortedData.iloc[:2]
    restData = sortedData.iloc[2:]
    d = d.reset_index(drop=True)
    time12 = fullTimeSum(d)
    dNew = d.reindex([1,0])
    time21 = fullTimeSum(dNew)
    if(time12.iloc[-1,-1] < time21.iloc[-1,-1]):
        return d, restData
    return dNew, restData
    
def addTask(data, restOfData):
    toAdd = restOfData.iloc[:1]
    rest = restOfData.iloc[1:]
    
    minTime = -1
    final = data.iloc[0:0]
    for i in range(restOfData.shape[0]+1):
        if(i==0):
            newData = pd.concat([toAdd, data])
            minTime = fullTimeSum(newData)
            minTime = minTime.iloc[-1,-1]
            final = newData
        else:
            newData = pd.concat([data.iloc[:i], toAdd, data.iloc[i:]])
            time = fullTimeSum(newData)
            time = time.iloc[-1,-1]
            if(time<minTime):
                minTime = time
                final = newData
                    
    
    
    return final, rest
        
def NEH(data):
    dataSorted = SumAndSort(data)
    dNew, restData = firstTwoTasks(dataSorted)
    while(restData.shape[0]>0):
        dNew, restData = addTask(dNew, restData)
    return dNew


d = NEH(data)
fts = fullTimeSum(d)
print(d)
print(fts.iloc[-1,-1])
d.to_excel("neh/neh200_20.xlsx")
