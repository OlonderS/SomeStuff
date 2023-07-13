#!/usr/bin/env python
# -*- coding: utf-8 -*-

from math import floor


def wyszukaj_liniowo(l, el):
    for i in range(0, len(l)):
        if l[i] == el:
            return i
    return -1


def wyszukaj_bin_it(lista, el):
    """tylko gdy tabela jest posortowana"""
    lewy, prawy = 0, len(lista) - 1
    while lewy < prawy:
        srodek = floor((lewy + prawy) / 2)
        # print(srodek)
        if el <= lista[srodek]:
            prawy = srodek
        else:
            lewy = srodek + 1
    if lista[lewy] == el:
        return lewy
    else:
        return -1


def wyszukaj_bin_rek(lewy, prawy, lista, el):
    if lewy > prawy:
        return -1  # nie ma elementu

    srodek = floor((lewy + prawy) / 2)
    if el == lista[srodek]:
        return srodek  # element w środku

    if el < lista[srodek]:
        return wyszukaj_bin_rek(lewy, srodek - 1, lista, el)
    else:
        return wyszukaj_bin_rek(srodek + 1, prawy, lista, el)


def main(args):
    lista = [4, 3, 7, 0, 2, 3, 1, 9, -4]
    lista.sort()  # sortuje tabele od najmniejszej
    # print(lista)

    el = int(input("Jaki element chcesz wyszukać: "))

    assert wyszukaj_bin_it(lista, 6) == -1
    assert wyszukaj_bin_it(lista, 3) == 4
    assert wyszukaj_bin_it(lista, -4) == 0
    assert wyszukaj_bin_it(lista, 4) == 6

    print(wyszukaj_bin_it(lista, el))
    print(wyszukaj_bin_rek(0, len(lista) - 1, lista, el))

    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
