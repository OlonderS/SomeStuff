# %% [markdown]
# zad1
# Ryzyko kredytowe to ryzyko straty, jaką może ponieść jedna ze stron umowy, np. bank, udzielając kredytu osobie lub firmie, która nie będzie w stanie go spłacić zgodnie z warunkami umowy kredytowej. 
# Model Altmana, jest narzędziem służącym do oceny ryzyka upadłości firm. 
# Model ten określa prawdopodobieństwo bankructwa firmy na podstawie pięciu wskaźników finansowych, takich jak między innymi wskaźnik zadłużenia i rentowności. 
# Model jest liniowy, co niekoniecznie odzwierciedla drogę do bankructwa; model operuje na danych księgowych (dane są dostępne w pewnych odstępach czasowych, np. kwartalne); model jest prosty i bazuje na niewielkiej liczbie informacji.
# 
# zad2
# Zapoznałem się
# 
# zad3

# %%
import pandas as pd 
import numpy as np
import math
dane = pd.read_csv('data1year.csv', sep=";", header=0)
dane = dane.to_numpy()


print("Model Altmana")
results = [0,0,0,0] # tru pos, fal pos, fal neg, tru neg
def altman_model(x1,x2,x3,x4,x5):
    x1 = x1.replace(",",".")
    x2 = x2.replace(",",".")
    x3 = x3.replace(",",".")
    x4 = x4.replace(",",".")
    x5 = x5.replace(",",".")
    z = 1.2*float(x1)+1.4*float(x2)+3.3*float(x3)+0.6*float(x4)+0.99*float(x5)
    return z
dl=len(dane)
wynik = [[0 for x in range(2)] for y in range(dane.shape[0])]
dobrze=0
for i in range(dane.shape[0]):
    wynik[i][0] = altman_model(dane[i][2],dane[i][5],dane[i][6],dane[i][7],dane[i][8])
    if wynik[i][0]<=1.8:
        wynik[i][1]=1
    else:
        wynik[i][1]=0
    if wynik[i][1] == 1 and dane[i][64] == 1:
        results[0]+=1
    elif wynik[i][1] == 1 and dane[i][64] == 0:
        results[1]+=1
    elif wynik[i][1] == 0 and dane[i][64] == 1:
        results[2]+=1
    else:
        results[3]+=1
print("True positive: " + str(round(results[0]/sum(results)*100, 2)) + "%")
print("False positive: " + str(round(results[1]/sum(results)*100, 2)) + "%")
print("False negative: " + str(round(results[2]/sum(results)*100, 2)) + "%")
print("True negative: " + str(round(results[3]/sum(results)*100, 2)) + "%")

# %% [markdown]
# Model altmana dla tych danych prawidłowo przewidzał upadłość firmy (lub jej brak) około 77% przypadków. Pośrednia grupa wynikowa modelu "szara strefa" została w tym przypadku zakwalifikowana do tej, która oznacza brak upadłości firmy, co na pewno ma pewien wpływ na wynik, lecz model klasyfikuje firmę do jednej z trzech grup, a dane tylko do jednej z dwóch. Orignalne testowanie tego modelu potwierdziło jego skuteczność na poziomie 95%, więc wynik 77% może być uznawany za przeciętny, ale wpływ na to mogą mieć nierównomiernie rozłożone dane, gdzie firm nieupadłych jest znacznie więcej.
# 
# zad4

# %%
print("Model Springate'a")

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

# %% [markdown]
# Model Springate'a dla tych danych zachowuje się jeszcze gorzej i poprawnie klasyfikuję firmy do bankrutów lub nie jedynie w około 65%. Jego wyniki pokrywają się z wynikami z model Altmana w 84,48%, na co głównie ma wpływ to, że model Springate'a ma o kilkanaście % gorszą skuteczność, więc i różnice w wynikach między nimi również są rzędu kilkunastu %. 
# 
# zad5/6/7

# %%
print("Dane ograniczone do 100 firm upadłych i 100 nieupadłych\n")
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

print("\nModel Springate'a")
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

# %% [markdown]
# Skuteczności modeli nieco się zmieniły - skuteczność modelu Almana nieco spadła, a modelu Springate'a wzrosła, choć w znależności od wylosowywanych danych, wartości te różnią się od siebie. Zauważalna jest tendencja zrównywania się rodzajów prawidłowych i negatywnych klasyfikacji poprawne pozytywne i negatywne klasyfikacje oraz fałszywe pozytyne i negatywne klasyfikacje są na podobnym poziomie, a wraz ze zwiększeniem próbki, wartości te zbliżają się do siebie coraz bardziej. 
# Lepszą skutecznością popsuje się model Altmana i wydaje się być on lepszy od modelu Springate'a, niezależnie od rodzaju danych, choć jego skuteczność w tym przypadku też nie jest wygórowana, a klasyfukacja firm do "szarej strefy" może tylko pogłębiać jego niejednoznaczność. Dodatkowo, skuteczność na poziomie 70-80% mogłaby by być oznana jako wystarczającą w przypadku klasyfikacji do wielu kategorii, a nie jednej z dwóch, w której losowy model powinien mieć ~50% skuteczności.
# 
# zad8

# %%
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
# X4 aktywa obrotowe / zobowiazania krotkoterm = attr4
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
    wynik4[i][0] = maczynska_model(dane[i][0],dane[i][9],dane[i][15],dane[i][3],dane[i][35])
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


# %% [markdown]
# Model poznański przyjmuje zmienne:
# X1 wynik finansowy netto / aktywa ogółem 
# X2 aktywa obrotowe ogółem / zobowiązania krótkoterm
# X3 kapitał własny + kapytały obce długoterm / aktywa ogółem
# X4 zysk brutto ze sprzedaży / przychody netto ze sprzedaży
# 
# Model Mączyńskiej przyjmuje zmienne:
# X1 zysk / aktywa ogolem
# X2 kapital wlasny / aktywa ogolem
# X3 zysk netto + amortyzacja / kapitaly obbce
# X4 aktywa obrotowe / zobowiazania krotkoterm
# X5 przychody netto ze sprzedazy + pozostale/ aktywa ogolem
# 
# Oba modele w przypadku tych danych okazały się skuteczniejsze od analizowanych wcześniej modeli Altmana i Springate'a

# %% [markdown]
# zad 9 
# 
# Zysk operacyjny / Przychody ze sprzedaży: x1
# Odpowiedni poziom rentowności powinien zapewnić firmie stabilną pozycję na rynku. 
# 
# Dług / Kapitał własny: x2
# Wysoki poziom zadłużenia oznacza, że firma musi spłacać duże sumy odsetek i może mieć trudności w pozyskiwaniu kolejnych kredytów.
# 
# Przychody ze sprzedaży / Aktywa ogółem: x3
# Mierzy, jak wiele przychodów generuje firma na każdą jednostkę swoich aktywów.
# 
# Aktywa bieżące / Zobowiązania bieżące: x4
# Niski wskaźnik płynności może wskazywać na trudności finansowe, które mogą prowadzić do upadłości.
# 
# v = 2.1*x1-3*x2+1.5*x3+2.1*x4
# 
# dla v > 1.5 - brak bankurctwa
# v<=1.5 - bankurctwo


#Model Hadasik
# X1 aktywa obrotowe ogółem / zobowiązania krótkoterm = attr4
# X2 aktywa obrotowe ogółem - zapasy - rozliczenia międzyokresowe / zobowiązania krótkoterm, = attr40
# X3 kapitały obce / aktywa ogółem = attr2
# X4 kapitał obrotowy netto / aktywa ogółem = attr3
# X5 należności krótkoterm / przychody netto ze sprzedaży = attr62
# X6 zapasy / przychody netto ze sprzedaży = attr20
print("Model Hadasik")
def hadasik_model(x1,x2,x3,x4,x5,x6):
    x1 = x1.replace(",",".")
    x2 = x2.replace(",",".")
    x3 = x3.replace(",",".")
    x4 = x4.replace(",",".")
    x5 = x5.replace(",",".")
    x6 = x6.replace(",",".")
    z = 0.365425*float(x1)-0.765526*float(x2)-2.40435*float(x3)+1.59079*float(x4)+0.00230258*float(x5)-0.0127827*float(x6)+2.36261
    return z

wynik5 = [[0 for x in range(2)] for y in range(dane.shape[0])]
dobrze5=0
results5 = [0, 0, 0, 0]
for i in range(dane.shape[0]):
    wynik5[i][0] = hadasik_model(dane[i][3],dane[i][39],dane[i][1],dane[i][2],dane[i][61],dane[i][19])
    if wynik5[i][0]<=-0.34345:
        wynik5[i][1]=1
    else:
        wynik5[i][1]=0

    if wynik5[i][1] == 1 and dane[i][64] == 1:
        results5[0]+=1
    elif wynik5[i][1] == 1 and dane[i][64] == 0:
        results5[1]+=1
    elif wynik5[i][1] == 0 and dane[i][64] == 1:
        results5[2]+=1
    else:
        results5[3]+=1

print("True positive: " + str(round(results5[0]/sum(results5)*100, 2)) + "%")
print("False positive: " + str(round(results5[1]/sum(results5)*100, 2)) + "%")
print("False negative: " + str(round(results5[2]/sum(results5)*100, 2)) + "%")
print("True negative: " + str(round(results5[3]/sum(results5)*100, 2)) + "%")

#Model Fulmera
# X1 zysk zatrzymany / aktywa ogółem attr6
# X2 przychody ogółem / aktywa ogółem  attr1
# X3 zysk brutto / kapitały własne attr18
# X4 przepływy pieniężne / zobowiązania ogółem attr34
# X5 zobowiązania ogółem / aktywa ogółem attr2
# X6 zobowiązania bieżące / aktywa ogółem attr51
# X7 log(aktywa rzeczowe) attr29
# X8 kapitał obrotowy / zobowiązania ogółem attr50
# X9 log(zysk przed podatkiem i odsetki) attr7
print("Model Fulmera")
def fulmer_model(x1,x2,x3,x4,x5,x6,x7,x8,x9):
    x1 = x1.replace(",",".")
    x2 = x2.replace(",",".")
    x3 = x3.replace(",",".")
    x4 = x4.replace(",",".")
    x5 = x5.replace(",",".")
    x6 = x6.replace(",",".")
    x7 = x7.replace(",",".")
    x8 = x8.replace(",",".")
    x9 = x9.replace(",",".")
    z = 5.528*float(x1)+0.212*float(x2)+0.07*float(x3)+1.27*float(x4)
    -0.12*float(x5)+2.335*float(x6)+0.575*float(x7)+10.83*float(x8)+(0.894*math.log(float(x9)) if float(x9)>0 else 0)-6.075
    return z

wynik6 = [[0 for x in range(2)] for y in range(dane.shape[0])]
dobrze6=0
results6 = [0, 0, 0, 0]
for i in range(dane.shape[0]):
    wynik6[i][0] = fulmer_model(dane[i][5],dane[i][0],dane[i][17],dane[i][33],dane[i][1],dane[i][50],dane[i][28],dane[i][49],dane[i][6])
    if wynik6[i][0]<=0:
        wynik6[i][1]=1
    else:
        wynik6[i][1]=0

    if wynik6[i][1] == 1 and dane[i][64] == 1:
        results6[0]+=1
    elif wynik6[i][1] == 1 and dane[i][64] == 0:
        results6[1]+=1
    elif wynik6[i][1] == 0 and dane[i][64] == 1:
        results6[2]+=1
    else:
        results6[3]+=1

print("True positive: " + str(round(results6[0]/sum(results6)*100, 2)) + "%")
print("False positive: " + str(round(results6[1]/sum(results6)*100, 2)) + "%")
print("False negative: " + str(round(results6[2]/sum(results6)*100, 2)) + "%")
print("True negative: " + str(round(results6[3]/sum(results6)*100, 2)) + "%")