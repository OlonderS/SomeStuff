#zad1
#Ryzyko kredytowe to ryzyko straty, jaką może ponieść jedna ze stron umowy, np. bank, udzielając kredytu osobie lub firmie, która nie będzie w stanie go spłacić zgodnie z warunkami umowy kredytowej. 
#Model Altmana, jest narzędziem służącym do oceny ryzyka upadłości firm. Model ten określa prawdopodobieństwo bankructwa firmy na podstawie pięciu wskaźników finansowych, takich jak między innymi wskaźnik zadłużenia i rentowności.
#model jest liniowy, co niekoniecznie odzwierciedla drogę do bankructwa;model operuje na danych księgowych (dane są dostępne w pewnych odstępach czasowych, np. kwartalne);model jest prosty i bazuje na niewielkiej liczbie informacji

#zad2 zapoznałem się

import pandas as pd 
import numpy as np

dane = pd.read_csv('data.csv', sep=",", header=0)
dane = dane.to_numpy(type)


# czesto np nie ma zmiennej sales/assets ale jest sales/current assets ale po przyjeciu jej i jej odwróceniu czesto przyjmuje skrajnie udze wartosci np kilka tysiecy co wypacza wyniki modelu a usuwanie outlierow i normalizacja nie poprawia znacząco wynikow
#z3
#X56 - Current Assets/Total Assets, X68 - Retained Earnings to Total Assets, X1 - Return On Total Assets(C), wartość rynkowa kapitału akcyjnego = 1/X91 , przychody ze sprzedaży = 1/x71
print("Model altmana")
results = [0,0,0,0] # tru pos, fal pos, fal neg, tru neg
def altman_model(x1,x2,x3,x4,x5):
    z = 1.2*float(x1)+1.4*float(x2)+3.3*float(x3)+0.6*float(x4)+0.99*float(x5)
    return z
dl=len(dane)
wynik = [[0 for x in range(2)] for y in range(dane.shape[0])]
dobrze=0
for i in range(dane.shape[0]):
    try:
        wynik[i][0] = altman_model(dane[i][56],dane[i][68],dane[i][1],1/dane[i][91],1/dane[i][71])
    except: 
        continue
    if wynik[i][0]<=1.8:
        wynik[i][1]=1
    else:
        wynik[i][1]=0
    if wynik[i][1] == 1 and dane[i][0] == 1:
        results[0]+=1
    elif wynik[i][1] == 1 and dane[i][0] == 0:
        results[1]+=1
    elif wynik[i][1] == 0 and dane[i][0] == 1:
        results[2]+=1
    else:
        results[3]+=1
print("True positive: " + str(round(results[0]/sum(results)*100, 2)) + "%")
print("False positive: " + str(round(results[1]/sum(results)*100, 2)) + "%")
print("False negative: " + str(round(results[2]/sum(results)*100, 2)) + "%")
print("True negative: " + str(round(results[3]/sum(results)*100, 2)) + "%")



#z4
print("Model Springate'a")
# model Springate'a
# kapitał pracujący / aktywa ogółem = attr3
# X2 zysk przed spłatą odsetek i podatkiem / aktywa ogółem, = attr7
# X3 wynik brutto / zobowiązania krótkoterm, = attr12
# X4 przychody ze sprzedaży / aktywa ogółem. = attr9

def springate_model(x1,x2,x3,x4):
    x1 = x1.replace(",",".")
    x2 = x2.replace(",",".")
    x3 = x3.replace(",",".")
    x4 = x4.replace(",",".")
    z = 1.03*float(x1) + 3.07*float(x2) + 0.66*float(x3) + 0.4*float(x4)
    return z
wynik2 = [[0 for x in range(2)] for y in range(dane.shape[0])]
dobrze2=0
results2 = [0, 0, 0, 0]
for i in range(dane.shape[0]):
    wynik2[i][0] = springate_model(dane[i][2], dane[i][6], dane[i][11], dane[i][8])
    if wynik2[i][0]<0.862:
        wynik2[i][1]=1
    else:
        wynik2[i][1]=0
    if wynik2[i][1] == 1 and dane[i][64] == 1:
        results2[0]+=1
    elif wynik2[i][1] == 1 and dane[i][64] == 0:
        results2[1]+=1
    elif wynik2[i][1] == 0 and dane[i][64] == 1:
        results2[2]+=1
    else:
        results2[3]+=1

print("True positive: " + str(round(results2[0]/sum(results2)*100, 2)) + "%")
print("False positive: " + str(round(results2[1]/sum(results2)*100, 2)) + "%")
print("False negative: " + str(round(results2[2]/sum(results2)*100, 2)) + "%")
print("True negative: " + str(round(results2[3]/sum(results2)*100, 2)) + "%")

# porównanie wyników z altmana do springate'a
zgodne=0
for i in range(dane.shape[0]):
    if wynik[i][1]==wynik2[i][1]:
        zgodne=zgodne+1

zgodne2=round((zgodne/dl)*100,2)
zgodne2=str(zgodne2)
print("Modele zgadzają się ze sobą w " + zgodne2 + "%")


#zad 5
print("Dane ograniczone do 100 firm upadłych i 100 nieupadłych")
print("Model Altmana")
good = np.array([x for x in dane if x[-1] == 1])
bad  = np.array([x for x in dane if x[-1] == 0])
good2 = good[np.random.choice(good.shape[0], 100, replace=False)]
bad2 = bad[np.random.choice(bad.shape[0], 100, replace=False)]
dane2 = np.concatenate((bad2, good2), axis=0)

wynik3 = [[0 for x in range(2)] for y in range(dane2.shape[0])]
dobrze3=0
results3 = [0, 0, 0, 0]
for i in range(dane2.shape[0]):
    wynik3[i][0] = altman_model(dane2[i][2],dane2[i][5],dane2[i][6],dane2[i][7],dane2[i][8])
    if wynik3[i][0]<1.8:
        wynik3[i][1]=1
    else:
        wynik3[i][1]=0
    if wynik3[i][1] == 1 and dane2[i][64] == 1:
        results3[0]+=1
    elif wynik3[i][1] == 1 and dane2[i][64] == 0:
        results3[1]+=1
    elif wynik3[i][1] == 0 and dane2[i][64] == 1:
        results3[2]+=1
    else:
        results3[3]+=1

print("True positive: " + str(round(results3[0]/sum(results3)*100, 2)) + "%")
print("False positive: " + str(round(results3[1]/sum(results3)*100, 2)) + "%")
print("False negative: " + str(round(results3[2]/sum(results3)*100, 2)) + "%")
print("True negative: " + str(round(results3[3]/sum(results3)*100, 2)) + "%")

print("Model Springate'a")
wynik4 = [[0 for x in range(2)] for y in range(dane2.shape[0])]
dobrze4=0
results4 = [0, 0, 0, 0]
for i in range(dane2.shape[0]):
    wynik4[i][0] = springate_model(dane2[i][2], dane2[i][6], dane2[i][11], dane2[i][8])
    if wynik4[i][0]<=0.862:
        wynik4[i][1]=1
    else:
        wynik4[i][1]=0
    if wynik4[i][1] == 1 and dane2[i][64] == 1:
        results4[0]+=1
    elif wynik4[i][1] == 1 and dane2[i][64] == 0:
        results4[1]+=1
    elif wynik4[i][1] == 0 and dane2[i][64] == 1:
        results4[2]+=1
    else:
        results4[3]+=1

print("True positive: " + str(round(results4[0]/sum(results4)*100, 2)) + "%")
print("False positive: " + str(round(results4[1]/sum(results4)*100, 2)) + "%")
print("False negative: " + str(round(results4[2]/sum(results4)*100, 2)) + "%")
print("True negative: " + str(round(results4[3]/sum(results4)*100, 2)) + "%")

# porównanie wyników z altmana do springate'a
zgodne3=0
for i in range(dane2.shape[0]):
    if wynik3[i][1]==wynik4[i][1]:
        zgodne3=zgodne3+1

zgodne4=round((zgodne3/len(dane2))*100,2)
zgodne4=str(zgodne4)
print("Modele zgadzają się ze sobą w " + zgodne4 + "%")

#Zad 8
#Model poznański
# X1 wynik finansowy netto / aktywa ogółem = attr1
# X2 aktywa obrotowe ogółem / zobowiązania krótkoterm, = attr4
# X3 kapitał własny + kapytały obce długoterm / aktywa ogółem, = attr10
# X4 zysk brutto ze sprzedaży / przychody netto ze sprzedaży. = attr19
print("Model poznanski")
def poznanski_model(x1,x2,x3,x4):
    x1 = x1.replace(",",".")
    x2 = x2.replace(",",".")
    x3 = x3.replace(",",".")
    x4 = x4.replace(",",".")
    z = 3.562*float(x1) + 1.58*float(x2) + 4.288*float(x3) + 6.719*float(x4) - 2.368
    return z
wynik3 = [[0 for x in range(2)] for y in range(dane.shape[0])]
dobrze3=0
results4 = [0, 0, 0, 0]
for i in range(dane.shape[0]):
    wynik3[i][0] = poznanski_model(dane[i][0], dane[i][3], dane[i][9], dane[i][18])
    if wynik3[i][0]<=0:
        wynik3[i][1]=1
    else:
        wynik3[i][1]=0
    if wynik3[i][1] == 1 and dane[i][64] == 1:
        results4[0]+=1
    elif wynik3[i][1] == 1 and dane[i][64] == 0:
        results4[1]+=1
    elif wynik3[i][1] == 0 and dane[i][64] == 1:
        results4[2]+=1
    else:
        results4[3]+=1

print("True positive: " + str(round(results4[0]/sum(results4)*100, 2)) + "%")
print("False positive: " + str(round(results4[1]/sum(results4)*100, 2)) + "%")
print("False negative: " + str(round(results4[2]/sum(results4)*100, 2)) + "%")
print("True negative: " + str(round(results4[3]/sum(results4)*100, 2)) + "%")

#Model Mączyńskiej
# X1 zysk / aktywa ogolem = attr1
# X2 kapital wlasny / aktywa ogolem, = attr10
# X3 zysk netto + amortyzacja / kapitaly obbce = attr16
# X4aktywa obrotowe / zobowiazania krotkoterm = attr4
# X5 przychody netto ze sprzedazy + pozostale/ aktywa ogolem = attr9
print("Model Maczynskiej")
def maczynska_model(x1,x2,x3,x4,x5):
    x1 = x1.replace(",",".")
    x2 = x2.replace(",",".")
    x3 = x3.replace(",",".")
    x4 = x4.replace(",",".")
    x5 = x5.replace(",",".")
    z = 9.478*float(x1)+3.613*float(x2)+3.246*float(x3)+0.455*float(x4)+0.802*float(x5)-2.478
    return z

wynik4 = [[0 for x in range(2)] for y in range(dane.shape[0])]
dobrze4=0
results4 = [0, 0, 0, 0]
for i in range(dane.shape[0]):
    wynik4[i][0] = maczynska_model(dane[i][0],dane[i][9],dane[i][15],dane[i][3],dane[i][8])
    if wynik4[i][0]<=0:
        wynik4[i][1]=1
    else:
        wynik4[i][1]=0

    if wynik4[i][1] == 1 and dane[i][64] == 1:
        results4[0]+=1
    elif wynik4[i][1] == 1 and dane[i][64] == 0:
        results4[1]+=1
    elif wynik4[i][1] == 0 and dane[i][64] == 1:
        results4[2]+=1
    else:
        results4[3]+=1

print("True positive: " + str(round(results4[0]/sum(results4)*100, 2)) + "%")
print("False positive: " + str(round(results4[1]/sum(results4)*100, 2)) + "%")
print("False negative: " + str(round(results4[2]/sum(results4)*100, 2)) + "%")
print("True negative: " + str(round(results4[3]/sum(results4)*100, 2)) + "%")





#zad 5 

