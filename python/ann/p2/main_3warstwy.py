import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn import preprocessing


class WarstwaNeuronow:
    def __init__(self, wagi_x):
        self.wagi = wagi_x


class SiecNeuronowa:
    def __init__(self, warstwa1, warstwa2, warstwa3):
        self.warstwa1 = warstwa1
        self.warstwa2 = warstwa2
        self.warstwa3 = warstwa3

    # Funkcja sigmoid, zwraca wartości z przedziału (0, 1)
    @staticmethod
    def __sigmoid(x):
        return 1 / (1 + np.exp(-x))

    # Pochodna funkcji sigmoid
    # Wskazuje jak bardzo pewni jesteśmy obecnych wag
    @staticmethod
    def __sigmoid_pochodna(x):
        return x * (1 - x)

    # Uczymy sieć neuronową, wprowadzając poprawki w wagach z każdą iteracją
    def uczenie(self, wejscia_treningowe, wyjscia_treningowe, iteracje_treningowe, tempo_uczenia):
        for t in range(iteracje_treningowe):
            # Przekazanie wejsc do naszej sieci neuronowej w celu policzenia wyjsc
            wyjscia_warstwa1, wyjscia_warstwa2, wyjscia_warstwa3 = self.licz(wejscia_treningowe)

            # Liczymy błąd dla warstwy 2 (różnica między oczekiwanymi a przewidzianymi wyjściami)
            bledy_warstwa3 = wyjscia_treningowe - wyjscia_warstwa3
            zmiana_warstwa3 = bledy_warstwa3 * self.__sigmoid_pochodna(wyjscia_warstwa3)

            bledy_warstwa2 = zmiana_warstwa3.dot(self.warstwa3.wagi.T)
            zmiana_warstwa2 = bledy_warstwa2 * self.__sigmoid_pochodna(wyjscia_warstwa2)
            # Liczymy błąd dla warstwy 1 (Dzięki wagom warstwy 1 możemy stwierdzić
            # jak bardzo warstwa 1 wpłynęła na błąd warstwy drugiej).
            bledy_warstwa1 = zmiana_warstwa2.dot(self.warstwa2.wagi.T)
            zmiana_warstwa1 = bledy_warstwa1 * self.__sigmoid_pochodna(wyjscia_warstwa1)
            # Wyliczanie poprawek
            poprawki_warstwa1 = wejscia_treningowe.T.dot(zmiana_warstwa1)
            poprawki_warstwa2 = wyjscia_warstwa1.T.dot(zmiana_warstwa2)
            poprawki_warstwa3 = wyjscia_warstwa2.T.dot(zmiana_warstwa3)

            # Poprawienie wag
            self.warstwa1.wagi += tempo_uczenia * poprawki_warstwa1
            self.warstwa2.wagi += tempo_uczenia * poprawki_warstwa2
            self.warstwa3.wagi += tempo_uczenia * poprawki_warstwa3

    # Proces liczenia wyjsc
    def licz(self, wejscia):
        wyjscia_warstwa1 = self.__sigmoid(np.dot(wejscia, self.warstwa1.wagi))
        wyjscia_warstwa2 = self.__sigmoid(np.dot(wyjscia_warstwa1, self.warstwa2.wagi))
        wyjscia_warstwa3 = self.__sigmoid(np.dot(wyjscia_warstwa2, self.warstwa3.wagi))
        return wyjscia_warstwa1, wyjscia_warstwa2, wyjscia_warstwa3

    # Wypisanie wag sieci neuronowej
    def zwroc_wagi(self):
        return self.warstwa1.wagi, self.warstwa2.wagi, self.warstwa3.wagi


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


def testowanie(neuron1, neuron2, tempo_uczenia, iteracje, powtorzenia):
    wejscia_treningowe, wyjscia_treningowe, wejscia_testowe, wyjscia_testowe = wczytanie_danych()

    wagi_warstwa1 = 2 * np.random.random((13, neuron1)) - 1
    wagi_warstwa2 = 2 * np.random.random((neuron1, neuron2)) - 1
    wagi_warstwa3 = 2 * np.random.random((neuron2, 1)) - 1
    layer1 = WarstwaNeuronow(wagi_warstwa1)
    layer2 = WarstwaNeuronow(wagi_warstwa2)
    layer3 = WarstwaNeuronow(wagi_warstwa3)
    neural_network = SiecNeuronowa(layer1, layer2, layer3)

    neural_network.uczenie(wejscia_treningowe, wyjscia_treningowe, iteracje, tempo_uczenia)

    for it in range(powtorzenia):
        wagi2_warstwa1, wagi2_warstwa2, wagi2_warstwa3 = neural_network.zwroc_wagi()
        wejscia_treningowe, wyjscia_treningowe, wejscia_testowe, wyjscia_testowe = wczytanie_danych()
        warstwa1 = WarstwaNeuronow(wagi2_warstwa1)
        warstwa2 = WarstwaNeuronow(wagi2_warstwa2)
        warstwa3 = WarstwaNeuronow(wagi2_warstwa3)
        neural_network = SiecNeuronowa(warstwa1, warstwa2, warstwa3)
        neural_network.uczenie(wejscia_treningowe, wyjscia_treningowe, iteracje, tempo_uczenia)

    ukryte, ukryte2, przewidywane_wyjscia = neural_network.licz(wejscia_testowe)

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
print("Skuteczność sieci 3-warstwowej: ")
for k in range(10):
    skutecznosc = testowanie(2, 4, 0.15, 24000, 17)
    print(round(skutecznosc, 3) * 100, "%")
    suma += skutecznosc

print("Średnia skuteczność sieci 3-warstwowej: ", round(suma/10, 3) * 100, "%")

input()
