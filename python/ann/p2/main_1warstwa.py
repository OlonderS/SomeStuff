import numpy as np
import pandas as pd
from sklearn import preprocessing


def sigmoid(x):
    return 1 / (1 + np.exp(-x))


def sigmoid_derivative(x):
    return x * (1 - x)


def wczytanie_danych():
    tabela = pd.read_csv('heart.csv', header=0)
    tabela = tabela.sample(frac=1).reset_index(drop=True)  # wymieszanie danych

    wejscia_treningowe = np.array(tabela.iloc[:200, :-1])
    wejscia_treningowe = preprocessing.normalize(wejscia_treningowe)
    wyjscia_treningowe = np.array(tabela.iloc[:200, -1])
    wyjscia_treningowe = np.reshape(wyjscia_treningowe, (1, 200)).T
    wejscia_testowe = np.array(tabela.iloc[201:len(tabela), :-1])
    wejscia_testowe = preprocessing.normalize(wejscia_testowe)
    wyjscia_testowe = np.array(tabela.iloc[201:len(tabela), -1])
    wyjscia_testowe = np.reshape(wyjscia_testowe, (1, len(tabela) - 201)).T
    return wejscia_treningowe, wyjscia_treningowe, wejscia_testowe, wyjscia_testowe


def testowanie(tempo_uczenia, iteracje):
    wejscia_treningowe, wyjscia_treningowe, wejscia_testowe, wyjscia_testowe = wczytanie_danych()
    wagi = 2 * np.random.random((13, 1)) - 1
    for iteration in range(iteracje):
        warstwa_wejsciowa = wejscia_treningowe
        wyjscia = sigmoid(np.dot(warstwa_wejsciowa, wagi))  # mnożenie skalarne macierzy
        error = wyjscia_treningowe - wyjscia
        poprawki = tempo_uczenia * error * sigmoid_derivative(wyjscia)
        wagi += np.dot(warstwa_wejsciowa.T, poprawki)

    for i in range(17):
        wejscia_treningowe, wyjscia_treningowe, wejscia_testowe, wyjscia_testowe = wczytanie_danych()
        for iteration in range(iteracje):
            warstwa_wejsciowa = wejscia_treningowe
            wyjscia = sigmoid(np.dot(warstwa_wejsciowa, wagi))  # mnożenie skalarne macierzy
            error = wyjscia_treningowe - wyjscia
            poprawki = tempo_uczenia * error * sigmoid_derivative(wyjscia)
            wagi += np.dot(warstwa_wejsciowa.T, poprawki)

    przewidywane_wyjscia = sigmoid(np.dot(wejscia_testowe, wagi))
    licznik = 0
    for ite in range(1, 303 - 201):
        if przewidywane_wyjscia[ite] >= 0.5:
            predykcja = 1
        else:
            predykcja = 0
        if wyjscia_testowe[ite] == predykcja:
            licznik += 1

    return licznik / (303 - 201)


suma = 0
print("Skuteczność sieci 1-warstwowej: ")
for k in range(10):
    skutecznosc = testowanie(0.15, 24000)
    print(round(skutecznosc, 3) * 100, "%")
    suma += skutecznosc

print("Średnia skuteczność sieci 1-warstwowej: ", round(suma/10, 3) * 100, "%")

input()
