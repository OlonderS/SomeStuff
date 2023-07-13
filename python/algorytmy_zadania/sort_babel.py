#!/usr/bin/env python
# -*- coding: utf-8 -*-

from random import randint


def wypelnij(tab, n, m):
    ile = 0
    while ile < n:
        liczba = randint(0, m)
        if tab.count(liczba) == 0:
            tab.append(liczba)
            ile += 1
    return tab


def bubble_sort_najm(tab, n):
    for i in range(1, len(tab)):
        for j in range(1, len(tab)):
            if tab[j] < tab[j - 1]:
                tab[j], tab[j - 1] = tab[j - 1], tab[j]
    return tab


def bubble_sort_najw(tab, n):
    for i in range(1, len(tab)):
        for j in range(1, len(tab)):
            if tab[j] > tab[j - 1]:
                tab[j], tab[j - 1] = tab[j - 1], tab[j]
    return tab


def main(args):
    ile = 10
    tab = [ile]
    max = int(input("Jaka maksymalna liczbe do wlozenia do tabeli: "))
    print("Tabela przed sortowaniem: ", wypelnij(tab, ile, max))
    print("Tabela po sortowaniu_najm: ", bubble_sort_najm(tab, ile))
    print("Tabela po sortowaniu_najw: ", bubble_sort_najw(tab, ile))

    return 0


if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
