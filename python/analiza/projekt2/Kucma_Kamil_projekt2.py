# %% [markdown]
# Dane do projektu zostały pobrane ze strony kaggle: https://www.kaggle.com/datasets/vicsuperman/prediction-of-music-genre
# 
# Przedstawiają one kilkadziesiąt tysięcy utworów muzycznych opisanych za pomocą kilkunastu bardziej lub mniej mierzalnych zmiennych takich jak popularność, tempo czy akustyczność. Do każdego z nich została przypisana jedna z dziesięciu gatunków muzycznych.
# Ze względu na duży rozmiar danych, zarówno pod względem liczby danych, liczby zmiennych i liczby grup, ograniczyłem liczbę danych do pięciu tysięcy, liczbę zmiennych do czterech, które mają największe znaczenie w przydziale do danego gatunku, a liczbę gatunków muzycznych do dwóch, znacząco się różniących. 
# 
# Każdy utwór jest opisany za pomocą zmiennych:
# acousticness: Miara pewności od 0 do 1 określająca, czy utwór jest akustyczny. 1 oznacza pewność, że utwór jest akustyczny.
# danceability: Opisuje, w jakim stopniu utwór nadaje się do tańca w oparciu o kombinację elementów muzycznych, takich jak tempo, stabilność rytmu, siła uderzenia i ogólna regularność. Wartość 0 jest najmniej taneczna, a 1 najbardziej taneczna.
# energy: Energia jest miarą od 0,0 do 1,0 i reprezentuje percepcyjną miarę intensywności i aktywności. Zazwyczaj energiczne utwory wydają się szybkie, głośne i hałaśliwe. 
# instrumentalness - Opisuje stopień w którym muzyka nie zawiera wokalu mówionego. 1 oznacza muzykę bez wokalu, a 0 z ciągłym wokalem.
# music_genre: Gatunek muzyczny, do którego chcemy przydzielić utwór na podstawie pozostałych zmiennych, 0 oznacza muzykę elektroniczną, a 1, muzykę klasyczną
# 
# Dane te chcę wykorzystać do nauki i testowania kilku algorytmów machine learningowych służacych do klasyfikacji obiektów do konkretnych grup, w tym przypadku, do sklasyfikowania utworu o danych parametrach do konkretnego gatunku muzycznego.

# %% [markdown]
# Na początek importuje wszystkie używane w projekcie biblioteki.

# %%

import numpy as np
import csv
import math
import pandas as pd
import statistics
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import sklearn.metrics as metrics
import seaborn as sns
from sklearn.ensemble import RandomForestClassifier
from sklearn import svm
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt
from sklearn.model_selection import GridSearchCV
from sklearn.neighbors import KNeighborsClassifier 
import warnings
warnings.filterwarnings('ignore')


# %% [markdown]
# Następnie wczytuję dane oraz sprawdzam ich podstawowe statystyki. Jednoczenśnie randomizuję kolejność danych, aby uniknąć posortowania danych po zmiennej oznaczającej przydział do kategorii, aby algorytm nie wyuczył się fałszywej tendencji.

# %%
data = pd.read_csv("dane.csv")
data = data.drop('Unnamed: 0', axis=1)
data = data.sample(frac=1).reset_index(drop=True)
print(data.to_string(index=False, max_rows = 10))
print(data.describe())
data.boxplot(column=['acousticness', 'danceability', 'energy', 'instrumentalness'])  


# %% [markdown]
# Każda ze zmiennych przyjmuje wartości od 0 do 1, gdzie zmienna wynikowa przyjmuje dokładnie wartość 0 lub 1. Każda ze zmiennych objaśniających przyjmuje wartości z całego lub prawie całego zakresu 0-1, gdzie w przypadku acousticness i intrumentalness dominują mniejsze wartości, a w przypadku danceability i energy wartości te w częściej są większe od 0,5. Pięć tysięcy danych jest wystarczającą liczbą do nauczenia i przetestowania odpowiednich algorytmów. 

# %%

print(data.isnull().sum())
tmp = data.loc[:, data.columns != 'music_genre']
plt.figure(figsize=(12, 6))
sns.set(style="whitegrid")
corr = tmp.corr()
sns.heatmap(corr,annot=True, cmap="YlGnBu")
mean, std, names = [], [], []
for column in data.loc[:, data.columns != 'music_genre']:
    mean.append(statistics.mean(data[column]))
    std.append(statistics.stdev(data[column]))
    names.append(column)
coef = []
for m, s in zip(mean, std):
    coef.append(s*100/m)
df = pd.DataFrame([coef], columns=names, index=['Wsp.zmien'])
print(df)

i, j = 0, 0
for index, row in data.iterrows():
    if str(data.at[index, 'music_genre']) == '1':
        i+=1
    else:
        j+=1
print('Liczność kategorii muzyka klasyczna: ', i)
print('Liczność kategorii muzyka elektroniczna: ', j)



# %% [markdown]
# W zestawie danych nie ma żadnych brakujących wartości, zmienne objaśniające nie są ze sobą mocno skolerowane (po za energy - acousticness, ale współczynnik nie przekracza wartości 0,9), a współćzynnik zmienności każdej zmiennej ma dużą wartość. Ze względu na zakres wartości, jakie przyjmują zmienne, nie trzeba się martwić o wartości odstające i standaryzację danych. Obie kategorie, choć nie są równoliczne, to nie są skrajnie różnoliczebne, a charakterystyka danych nie rozróżnia znaczenia w popełnianiu błędu w jedną lub drugą stronę - przypisanie muzyki klasycznej do elektronicznej jest takim samym błędem jak elektronicznej do klasycznej.

# %% [markdown]
# 
#                                                                             Metoda k najbliższych sąsiadów - KNN
# Algorytm polega na:
# porównaniu wartości zmiennych objaśniających dla obserwacji C z wartościami tych zmiennych dla każdej obserwacji w zbiorze uczącym.
# wyborze k (ustalona z góry liczba) najbliższych do C obserwacji ze zbioru uczącego.
# uśrednieniu wartości zmiennej objaśnianej dla wybranych obserwacji, w wyniku czego uzyskujemy prognozę.

# %%
x = data.loc[:, data.columns != 'music_genre']
y = data['music_genre']
size = 0.2


# %% [markdown]
# Na początek z całego zestawu danych wyodrębniam zmienną wynikową, a następnie obie części dzielę na zbiory uczące i testowe w częściach kolejno 4/5 i 1/5

# %%
def knn(x, y, size):

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=size)
    no_neighbors = np.arange(1, 25, 2)
    train_accuracy = np.empty(len(no_neighbors))
    test_accuracy = np.empty(len(no_neighbors))

    for i, k in enumerate(no_neighbors):
        knn = KNeighborsClassifier(n_neighbors=k)
        knn.fit(x_train,y_train)
        train_accuracy[i] = knn.score(x_train, y_train)
        test_accuracy[i] = knn.score(x_test, y_test)

    plt.title('Dokładność knn w zależności od k')
    plt.plot(no_neighbors, test_accuracy, label = 'Testing Accuracy')
    plt.plot(no_neighbors, train_accuracy, label = 'Training Accuracy')
    plt.legend()
    plt.xlabel('Number of Neighbors')
    plt.ylabel('Accuracy')
    plt.show()

    gridsearch = GridSearchCV(estimator=KNeighborsClassifier(),
                param_grid={'n_neighbors': range(1, 25, 2),
                            'weights': ['uniform', 'distance']})
    gridsearch.fit(x_train, y_train)
    params = gridsearch.best_params_
    print(params)

    knn = KNeighborsClassifier(n_neighbors=params['n_neighbors'], weights=params['weights'])
    knn.fit(x_train,y_train)
    prediction = knn.predict(x_test)
    y_pred = knn.predict(x_test)
    y_true=y_test

    cm1= confusion_matrix(y_true, y_pred)
    f, ax =plt.subplots(figsize = (5,5))
    sns.heatmap(cm1,annot = True, linewidths= 0.5, linecolor="red", fmt=".0f", ax=ax)
    plt.xlabel("y_pred")
    plt.ylabel("y_true")
    plt.show()

    total1=sum(sum(cm1))
    accuracy1=(cm1[0,0]+cm1[1,1])/total1
    print ('Accuracy : ', accuracy1)
    sensitivity1 = cm1[0,0]/(cm1[0,0]+cm1[0,1])
    print('Sensitivity : ', sensitivity1)
    specificity1 = cm1[1,1]/(cm1[1,0]+cm1[1,1])
    print('Specificity : ', specificity1)
    
knn(x, y, size)


# %% [markdown]
# Na początek tworzę wykres dokładności algorytmu na zbiorze uczącym oraz testowym - w jakiej części algorym dobrze przydzielał klasę do posiadanych danych, w zależności od przyjmowanego parametru k - liczby sąsiadów, przyjmowanych w wartościach nieparzystych, aby unikać losowości przydzielania klasy w przypadkach równolicznych, np. dwóch sąsiadów należy do jednej grupy, a dwóch do drugiej, więc przydział następuje losowo. Patrząc oreintacyjnie na pierwszy wykres, który uwzględnia jedynie zmianę liczby sąsiadów, możnaby przyjąć k = 9 za optymalną wartość. Następnie badam wyniki zarówno pod względem liczby sąsiadów jak i sposobu obliczania odległości - k wynosi tyle samo, a wartość uniform oznacza, że odległości od sąsiadów mają taką samą wagę. Otrzymane wartości dokładności, czułości i specyficzności są duże i pozytywnie świadczą o jakości predykcji. 
# 
# Teraz powtarzam procedurę, tylko dla większej części testowej, a mniejszej uczącej

# %%
size = 0.3
knn(x, y, size)

# %% [markdown]
# Otrzymane wyniki są bardzo podobne, a ze względu na większy zakres danych do testowania, można być bardziej pewnym otrzymanych wyników

# %% [markdown]
#                                                                         Maszyna wektorów nośnych - SVM
# SVM dedykowane jest głównie do zagadnień klasyfikacji, w których jedną klasę separujemy możliwie dużym marginesem od pozostałych klas. Istotą tej metody jest znalezienie wektorów nośnych, definiujących hiperpowierzchnie optymalnie separujące obiekty w homogeniczne grupy.
# 
# W przypadku SVM, główne znaczenie ma wybór rodzaju funkcji jądra. Funkcja jądra to metoda służąca do przyjmowania danych jako danych wejściowych i przekształcania ich w wymaganą formę przetwarzania danych. Funkcją decyzyjną, ze względu na 2 kategorie, jest ovo - one vs one.

# %%

def svm(x, y, size):

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=size)
    
    gridsearch = GridSearchCV(estimator=svm.SVC(),
                param_grid={'kernel': ['linear', 'rbf', 'sigmoid'],
                            'decision_function_shape': ['ovo']})
    gridsearch.fit(x_train, y_train)
    params = gridsearch.best_params_
    print(params)
    
    y_pred = gridsearch.predict(x_test)
    y_true=y_test
    cm1= confusion_matrix(y_true, y_pred)
    f, ax =plt.subplots(figsize = (5,5))
    sns.heatmap(cm1,annot = True, linewidths= 0.5, linecolor="red", fmt=".0f", ax=ax)
    plt.xlabel("y_pred")
    plt.ylabel("y_true")
    plt.show()

    total1=sum(sum(cm1))
    accuracy1=(cm1[0,0]+cm1[1,1])/total1
    print ('Accuracy : ', accuracy1)
    sensitivity1 = cm1[0,0]/(cm1[0,0]+cm1[0,1])
    print('Sensitivity : ', sensitivity1)
    specificity1 = cm1[1,1]/(cm1[1,0]+cm1[1,1])
    print('Specificity : ', specificity1)
    
    
size = 0.2
svm(x, y, size)


# %% [markdown]
# Ponownię dziele zbiór na testowy i uczący oraz szukam najlepszych wartości parametrów - rodzaju funkcji jądra  z funkcji decyzyjnej. Ze względu na tylko dwie kategorie, jedynym i najlepszym wyborem jest funkcja decyzyjna one vs one, a najlepszą funkcją jądra jest rbf i to dla nich otrzymano powyższe wyniki. Otrzymane wartości dokładności, czułości i specyficzności są duże i pozytywnie świadczą o jakości predykcji. 
# 
# I ponownie ten sam algorytm, ale dla innych zakresów danych

# %%

size = 0.3
svm(x, y, size)

# %% [markdown]
#                                                                                     Random forest
# Algorytm polega na konstruowaniu wielu drzew decyzyjnych w czasie uczenia i generowaniu klasy, która jest dominantą klas (klasyfikacja) lub przewidywaną średnią (regresja) poszczególnych drzew. 
# Pierwszym krokiem jest losowanie ze zwracaniem podzbioru danych (przypadków) z dostępnej próby uczącej.
# Następnie, powinniśmy stworzyć drzewo dla wylosowanego wcześniej podzbioru. W tym punkcie trzeba sprawdzić, czy dzielony zbiór jest jednorodny oraz czy nie jest zbyt mały, by go podzielić. Należy wylosować pewną liczbę zmiennych objaśniających oraz znaleźć najlepszy podział z wykorzystaniem wylosowanego podzbioru zmiennych. Zbiór ten później dzielimy na dwie części.
# Jeżeli liczba drzew osiągnie zadane maksimum lub błąd w próbie testowej przestanie maleć, należy zakończyć uczenie. W przeciwnym przypadku, należy wrócić do pierwszego kroku. W ogólności: drzewa "głosują" nad rozwiązaniem, wybór następuje zwykłą większością głosów.

# %%

def rand_forest(x, y, size):

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=size)
    n = np.arange(2, 25, 2)
    train_accuracy = np.empty(len(n))
    test_accuracy = np.empty(len(n))

    for i, k in enumerate(n):
        rf = RandomForestClassifier(n_estimators=k)
        rf.fit(x_train,y_train)
        train_accuracy[i] = rf.score(x_train, y_train)
        test_accuracy[i] = rf.score(x_test, y_test)

    plt.title('Dokładność random forest w zależności od k')
    plt.plot(n, test_accuracy, label = 'Testing Accuracy')
    plt.plot(n, train_accuracy, label = 'Training Accuracy')
    plt.legend()
    plt.xlabel('Liczba drzew')
    plt.ylabel('Accuracy')
    plt.show()

    gridsearch = GridSearchCV(estimator=RandomForestClassifier(),
                param_grid={'n_estimators': range(2, 25, 2),
                            'criterion': ['gini', 'entropy', 'log_loss']})
    gridsearch.fit(x_train, y_train)
    params = gridsearch.best_params_
    print(params)

    rf = RandomForestClassifier(n_estimators=params['n_estimators'], criterion=params['criterion'])
    rf.fit(x_train,y_train)
    prediction = rf.predict(x_test)
    y_pred = rf.predict(x_test)
    y_true=y_test

    cm1= confusion_matrix(y_true, y_pred)
    f, ax =plt.subplots(figsize = (5,5))
    sns.heatmap(cm1,annot = True, linewidths= 0.5, linecolor="red", fmt=".0f", ax=ax)
    plt.xlabel("y_pred")
    plt.ylabel("y_true")
    plt.show()

    total1=sum(sum(cm1))
    accuracy1=(cm1[0,0]+cm1[1,1])/total1
    print ('Accuracy : ', accuracy1)
    sensitivity1 = cm1[0,0]/(cm1[0,0]+cm1[0,1])
    print('Sensitivity : ', sensitivity1)
    specificity1 = cm1[1,1]/(cm1[1,0]+cm1[1,1])
    print('Specificity : ', specificity1)

size = 0.2
rand_forest(x, y, size)

# %% [markdown]
# Podobnie jak w przypadki knn, na początek sprawdzam wyniki w zależności od przyjmowanej liczby drzew. Patrząc na wykres, można dojść do podobynch wniosków, które zwraca estymacja parametrów, uwzględniająca również wybór odpowiedniej funckji mierzącej jakość podziału drzew - 'entropy'. Otrzymane wartości dokładności, czułości i specyficzności są duże i pozytywnie świadczą o jakości predykcji. 
# 
# To samo wykonuję dla innego podziału danych

# %%
size = 0.3
rand_forest(x, y, size)

# %%



