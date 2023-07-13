#!/usr/bin/env python
# -*- coding: utf-8 -*-

from random import randint

def losuj (ileliczb, maksliczb):
    liczby = []
    ile = 0  # ilość wylosowanych liczb
    while ile < ileliczb:
    #  for i in range(ileliczb):
        liczba = randint(0, maksliczb)
        if liczby.count(liczba) == 0:
            liczby.append(liczba)
            ile += 1
    #  print(liczby)
    return liczby

def pobierz_typy(ileliczb):
    typy = set()   # pusty zbiór
    # for i in range(ileliczb):
    ile = 0  # ilość podanych typów
    while ile < ileliczb:
        typ = int(input("Podaj typ: "))
        if typ not in typy:
            typy.add(typ)
            ile += 1

    #  print(typy)
    return typy

def main(args):
    try:
        ileliczb = int(input("Ile liczb chcesz zgadnąć?: "))
        maksliczb = int(input("Podaj górny zakres: "))

        while ileliczb > maksliczb:
            ileliczb = int(input("Ile liczb chcesz zgadnąć z %s?" % maksliczb))
    except ValueError:
        print("Błędne dane!")
        exit()


    liczby = losuj(ileliczb, maksliczb)
    typy = pobierz_typy(ileliczb)
    print("Wylosowane liczby: ", liczby)
    print("Twoje typy: ", typy)
    trafione = set(liczby) & typy
    print("Trafione ", len(trafione), "liczby")

    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))

