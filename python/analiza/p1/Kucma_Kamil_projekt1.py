# %% [markdown]
# Dane do projektu zostały pobrane ze strony kaggle: https://www.kaggle.com/datasets/varpit94/football-teams-rankings-stats
# Przedstawiają one kilka statystyk dotyczących wszystkich 98 zespołów z top 5 lig (angielskiej, hiszpańskiej, włoskiej, niemieckiej i francuskiej) w piłce nożnej z sezonu 2020-2021. Kolejne kolumny opisują kolejno: Nazwę klubu, liczbę strzelonych bramek, liczbę strzałów na mecz, liczbę otrzymanych żółtych kartek, liczbę otrzymanych czerwonych kartek, średnie posiadanie piłki, oraz średnią dokładność podań. 
# Dane te chcę wykorzystać w metodach porządkowania liniowego, analizy skupień oraz skalowania wielowymiarowego i na ich podstawie stworzyć ranking drużyn najlepszych do oglądania oraz pogrupować podobne do siebie drużyny względem pewnych statystyk.

# %% [markdown]
# Na początek importuje wszystkie używane w projekcie biblioteki.

# %%
from cmath import inf
import pandas as pd
import math
from tabulate import tabulate
import statistics
from kneed import KneeLocator
import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler
from scipy.cluster.hierarchy import dendrogram, linkage
from sklearn.manifold import MDS
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from sklearn.metrics import euclidean_distances
from math import sqrt
from IPython.display import Image
import warnings
warnings.filterwarnings('ignore')


# %% [markdown]
# Następnie wczytuję dane oraz sprawdzam ich podstawowe statystyki. Niektóre zmienne są ze sobą dość mocno skolerowane co jest dość intuicyjne (im więcej strzałów tym większa szansa na więcej goli), jednak w żadnym przypadku korelacja nie wynosi więcej niż 0.9, więc wartości nie przekraczają przyjmowanego progu. Inaczej jest ze współczynnikiem zmienności zmiennej opisującej dokładność podań - jego wartość wynosi mniej niż 10% - z tego powodu odrzucam tę zmienną.

# %%
def coef_var(data):
    mean = []
    std = []
    names = []
    for column in data.loc[:, data.columns != 'Team']:
        mean.append(statistics.mean(data[column]))
        std.append(statistics.stdev(data[column]))
        names.append(column)
    coef = []
    for m, s in zip(mean, std):
        coef.append(s*100/m)
    df = pd.DataFrame([coef], columns=names, index=['Wsp.zmien'])

    return df

data = pd.read_csv("music_genre.csv")

data = data.drop(('instance_id', 'aristi_name', 'key', 'mode', 'obtained_date', 'valence'), axis=1)
data.to_csv('dane.csv')
# %% [markdown]
#                                                                 Metoda Hellwiga
# Metoda Hellwiga pozwala na stworzenie rankingu obiektów na podstawie ich cech. W tym przypadku chcę stworzyć ranking najlepszych do oglądania zespołów na podstawie kilku powyższych statystyk. Można przyjąć, że im zespół strzela więcej bramek i oddaje więcej strzałów - tym jest ciekawszy do oglądania, dlatego te zmienne są stymulantami. Liczba otrzymanych żółtych i czerwonych kartek źle świadczy o zespole - te zmienne będą destymulantami. Posiadanie piłki jest pozytywną rzeczą, ale nie chcemy, aby zespół posiadał ją cały czas i nic z tego nie robił, dlatego można przyjąć 58% posiadania za optymalną wartość - zmienna ta będzie optimum. 
# Na początek zmieniam charakter wszsytkich danych na stymulanty

# %%

def to_stimulant(data, optimum):

    for column in data.loc[:, data.columns != 'Team']:
        for index, row in data.iterrows():
            if column == 'Possession%' and float(data.at[index, column])<optimum:
                data.at[index, column] = round(-1/(float(data.at[index, column])-optimum-1), 3)

            elif column == 'Possession%' and float(data.at[index, column])>optimum:
                data.at[index, column] = round(1/(float(data.at[index, column])-optimum+1), 3)
            elif column == 'Possession%':
                data.at[index, column] = 1
            elif column == 'yellow_cards' or column == 'red_cards':
                data.at[index, column] = -float(data.at[index, column])
            else:
                data.at[index, column] = float(data.at[index, column])
    return data

data = to_stimulant(data, optimum)
print(data.to_string(index=False, max_rows = 10))


# %% [markdown]
# Następnie standaryzuję dane, aby przykładowo liczba żółtych kartek, choć jest zdecydowanie większa od liczby czerwonych kartek, miała podobne znaczenie. Jednocześnie sprawdzam, czy nie ma wartości odstających.

# %%
def standardization(data):
    mean = []
    std = []
    for column in data.loc[:, data.columns != 'Team']:
        mean.append(statistics.mean(data[column]))
        std.append(statistics.stdev(data[column]))

    for column, m, s in zip(data.loc[:, data.columns != 'Team'], mean, std):
        for index, row in data.iterrows():
            data.at[index, column] = (data.at[index, column]-m)/s
    return data

data = standardization(data)
print(data.to_string(index=False, max_rows = 10))

for column in data.loc[:, data.columns != 'Team']:
    for index, row in data.iterrows():
        if abs(data.at[index, column]) >3:
            print(index, column, data.at[index, column]) # brak otrzymanego wydruku - brak wartości odstających



# %% [markdown]
# Teraz ustalam wzorzec - najlepsze wartości z każdej ze statystyk.

# %%

def pattern(data):
    pattce = []
    for column in data.loc[:, data.columns != 'Team']:
        pattce.append(max(data[column]))
    return pattce

patt = pattern(data)
print(patt)



# %% [markdown]
# Następnie wyliczam odległości - jak daleko dana zmienna odbiega od najlepszej wartości. Metoda uwzględnia wagi - zdecydowanie większe znaczenie w ocenie zespołu pod względem satysfakcji z oglądania ma dla mnie liczba strzelanych bramek aniżeli odpowiednie posiadanie piłki.

# %%

def distances(data, pattern):
    scales = [0.4, 0.25, 0.1, 0.1, 0.05]
    distance = []
    for index, row in data.iterrows():
        tmp = 0
        for column, w, i in zip(data.loc[:, data.columns != 'Team'], pattern, range(len(scales))):
            tmp += scales[i]*pow(data.at[index, column]-w, 2)
            data.at[index, column] = scales[i]*pow(data.at[index, column]-w, 2)
        distance.append(round(math.sqrt(tmp), 3))
    data['Distance'] = distance
    d0 = statistics.mean(distance) + 2*statistics.stdev(distance)
    return data, d0


data, d0 = distances(data, patt)
print(data.to_string(index=False, max_rows = 10))


# %% [markdown]
# Następnie przeliczam wartość miary odległości - im większa jej wartość - tym wyższe miejsce w rankingu

# %%

def measures(data, d0):
    data = data.drop(columns =['Goals', 'Shots pg', 'yellow_cards', 'red_cards', 'Possession%'])
    for index, row in data.iterrows():
        data.at[index, 'Distance'] = 1-(data.at[index, 'Distance']/d0)
    return data

data = measures(data, d0)
print(data.to_string(index=False, max_rows = 10))


# %% [markdown]
# Ostatnim krokiem jest posorowanie wartości. Z otrzymanego rankingu wynika, że najlepszym do oglądania zespołem jest Bayern Monachium, co pokrywa się ze statystykami, w których to zespoł ten strzelał najwięcej bramek, a w końcu na statystyka ma tutaj największe znaczenie. Ogólnie rzecz biorąc, na górze rankingu znajdują się zespoły dominujące w swoich ligach, a na dole te najsłabsze w swoich ligach co pokrywa się z rzeczywistą sytuacją, w której te najlepsze zespoły mają największą oglądalność.

# %%

data = data.sort_values('Distance', ascending=False)
ranking_final = data.rename(columns={'Distance': 'Ranking'})
print(ranking_final.to_string(index=False))

# %% [markdown]
#                                                             Metoda standaryzowanych sum
# Inną metodą porządkowania liniowego jest metoda standaryzowanych sum. W tej metodzie dla każdego obiektu sumuje się zestandaryzowane wcześniej wartości, a następnie konstruuje względny wskaźnik poziomu rozwoju.

# %% [markdown]
# Pierwsza część jest bardzo podobna, wczytuję zmienne, usuwam tę z małą zmiennością, zmieniam charakter zmiennych na stymulanty oraz standaryzuję wartości.

# %%
data = pd.read_csv("Football_teams.csv")
data = data.drop(('Pass%'), axis=1)
data = to_stimulant(data, optimum)
data = standardization(data)

# %% [markdown]
# Następnie obliczam sumy standaryzowanych rang uwzględniając takie same wagi jak poprzednio oraz sortuje je malejąco. Ich wartość mieści się w zakresie 0-1, gdzie 1 oznacza najlepszy element w rankingu, dodatkowo pozwala na zauważenie odległości między kolejnymi miejscami.

# %%
def sum_of_ranks(data):
    suma = []
    standard_suma = []
    scales = [0.4, 0.25, 0.1, 0.1, 0.05]
    for index, row in data.iterrows():
        tmp = 0
        counter = 0
        for i, column in enumerate((data.loc[:, data.columns != 'Team'])):
            tmp +=scales[i]*data.at[index, column]
            counter+=1
        suma.append(round(tmp/counter, 3))
    
    data['Suma'] = suma
    minn = min(suma)
    maxx = -inf
    for index, row in data.iterrows():
        tmp = 0
        if (data.at[index, 'Suma'] - minn) > maxx:
            maxx = data.at[index, 'Suma'] - minn
    for index, row in data.iterrows():
        data.at[index, 'Suma'] = (data.at[index, 'Suma'] - minn)/maxx
    return data

data = sum_of_ranks(data)
data = data.drop(['Goals', 'Shots pg', 'yellow_cards', 'red_cards', 'Possession%'], axis=1)
data = data.rename(columns={'Suma': 'Ranking'})
data = data.sort_values('Ranking', ascending=False)
print(data.to_string(index=False))


# %% [markdown]
# Rankingi są do siebie podobne w ogóle, ale różnią się w szczegółach, jednak na podstawie obu można dojść do podobnych wniosków.

# %% [markdown]
#                                                     Grupowanie podziałowe - metoda k-średnich
# Metoda k-średnich jest metodą należacą do grupy algorytmów analizy skupień tj. analizy polegającej na szukaniu i wyodrębnianiu grup obiektów podobnych (skupień) . Reprezentuje ona grupę algorytmów niehierarchicznych - należy z góry ustalić przyjmowaną liczbę skupień.
# Na początku standaryzuję dane a następnie używam metody k-średnich z ustaloną z góry liczbą 3 skupień. 

# %%
def kmeans(data):
    
    data2 = data[1:, 1:-1]
    scaler = StandardScaler()
    data2.astype('float')
    data2 = scaler.fit_transform(data2)

    kmeans = KMeans(
        init="random", n_clusters=3, n_init=10, max_iter=300, random_state=42
    )
    kmeans.fit(data2)

    kmeans_kwargs = {
        "init": "random",
        "n_init": 10,
        "max_iter": 300,
        "random_state": 42,
    }

    sse = []
    for k in range(1, 11):
        kmeans = KMeans(n_clusters=k, **kmeans_kwargs)
        kmeans.fit(data2)
        sse.append(kmeans.inertia_)

    plt.plot(range(1, 11), sse)
    plt.xticks(range(1, 11))
    plt.xlabel("Number of Clusters")
    plt.ylabel("SSE")
    plt.show()

    kl = KneeLocator(range(1, 11), sse, curve="convex", direction="decreasing")
    print('Elbow method: ', kl.elbow)

    silhouette_coefficients = []
    for k in range(2, 11):
        kmeans = KMeans(n_clusters=k, **kmeans_kwargs)
        kmeans.fit(data2)
        score = silhouette_score(data2, kmeans.labels_)
        silhouette_coefficients.append(score)

    plt.plot(range(2, 11), silhouette_coefficients)
    plt.xticks(range(2, 11))
    plt.xlabel("Number of Clusters")
    plt.ylabel("Silhouette Coefficient")
    plt.show()
    
data = np.genfromtxt('Football_teams.csv', delimiter=',', dtype = str)
kmeans(data)

# %% [markdown]
# Na podstawie otrzymanych wykresów i użytej metody łokciowej można przyjąć, że odpowiednią liczbą skupień jest liczba 3 - wykres się wypłaszcza - współczynnik podobieństwa do innych obiektów w skupienia nie zmienia się znacząco.

# %% [markdown]
# 
#                                                         Grupowanie hierarchiczne
# W tym przypadku nie trzeba podawać z góry liczby 'pojemników', algorytm sam dochodzi do ich liczby od góry (z 1 do n) lub od dołu (z n do 1), a bazując na odległościach między nimi, można dokonać wyboru.
# 

# %% [markdown]
# Prowadząc poprzeczną linię można podzielić dane na 4 części, odległości między mniejszymi częściami są na tyle małe, że ciężko myśleć o większej liczbie 'pojemników'.

# %%


def hierarchical(data):
    data2 = data[1:, 1:-1]
    scaler = StandardScaler()
    data2.astype('float')
    data2 = scaler.fit_transform(data2)
    
    linkage_data = linkage(data2, method='ward', metric='euclidean')
    #dendrogram(linkage_data)
    
hierarchical(data)
Image(filename='Figure_4.png') 

# %% [markdown]
#                                                         Skalowanie wielowymiarowe
# Aby zwizualizować podane wyniki, należy najpierw zmniejszyć rozmiar danych których niesposób zobrazować, co łatwo można uzyskać poprzez użycie gotowych funkcji. Opis każdej drużyny, w którego skład wchodzi 5 zmiennych należy przekształcić na taki, który będzie łatwo zwizualizować - w tym przypadku na wymiar 2d. Jakośc skalowania opisuje współcznnik stress, który po standaryzacji wynosi 0,015 co świadczy o tym, że dopasowanie jest dobre - mała część informacji jest zniekształcona.

# %%
def scaling(data):
    data2 = data[1:, 1:-1]
    scaler = StandardScaler()
    data2.astype('float64')
    data2 = scaler.fit_transform(data2)

    model2d=MDS(n_components=2, 
        metric=True, 
        n_init=4, 
        max_iter=300, 
        verbose=0, 
        eps=0.001, 
        n_jobs=None, 
        random_state=42, 
        dissimilarity='euclidean')
    
    X_trans = model2d.fit_transform(data2)

    stress = sqrt(model2d.stress_ / np.sum(data2**2))
    print("Kruskal's Stress :")
    print(stress)
    return X_trans
scaled = scaling(data)
x = []
y = []
idx = []
names = []
for i in range(2, len(scaled), 4):
    x.append(scaled[i][0])
    y.append(scaled[i][1])
    names.append(data[i][0])
    idx.append(i)
    
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
ax.scatter(x, y)

for i, n in zip(idx, names):
    if ' ' in n: 
        ax.annotate(n.split()[0][:3].upper()+' '+n.split()[1][:3].upper(), (scaled[i][0], scaled[i][1]))
    else:
        ax.annotate(n.split()[0][:3].upper(), (scaled[i][0], scaled[i][1]))


# %%
Image(filename='Figure_10.png', width=600) 

# %%
Image(filename='Figure_11.png', width=600) 

# %% [markdown]
# Na wykresie, dla lepszej czytelności, przedstawiam tylko co czwartą drużynę z rankingu. W zależności od interpretacji oraz sposobu grupowania, obiekty można zebrać w 3-4 grupy, które powinny być wewntąrz tych grupy w pewnych aspektach do siebie podobne. I tak też Angers i Sheffield United otrzymują podobną liczbę kartek, Marsylia i Sevilla mają prawie identyczną liczbę bramek oraz podobną liczbę strzałów, a Villareal i Milan mają identyczne posiadanie piłki, gdzie Manchester City znajdującę się w tej podgrupie i jednocześnie w niej odstaje, ma największe posiadanie ze wszystkich drużyn w rankingu. Wymienione przykłady mogą świadczyć o tym, że sposób w jaki obiekty zostały pogrupowane, ma rzeczywiste przełożenie w statystykach.


