#!/usr/bin/env python
# -*- coding: utf-8 -*-

def szyfruj(tekst, haslo):
    szyfrogram = []
    litery = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    numer_litery = 0

    for i in tekst:
        index = litery.find(i)  # szuka w liscie litery indexu 'i' z tekstu
        if index != -1:  # jesli litera z tekstu nie znalazla sie w alfabecie
            index += litery.find(haslo[numer_litery])
            # jesli wyjdziemy poza 26(litery alfabetu) to dzielimy modulo przez 26 i dodajemy reszte
            index %= 26
            szyfrogram.append(litery[index])
            numer_litery += 1  # przechodzimy do kolejnej litery w hasle
            if numer_litery == len(haslo):
                numer_litery = 0
        else:
            szyfrogram.append(i)

    return "".join(szyfrogram)


def deszyfruj(szyfrogram, haslo):
    tekst = []
    litery = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    numer_litery = 0

    for i in szyfrogram:
        index = litery.find(i)
        if index != -1:
            index -= litery.find(haslo[numer_litery])
            index %= 26
            tekst.append(litery[index])
            numer_litery += 1
            if numer_litery == len(haslo):
                numer_litery = 0
        else:
            tekst.append(i)

    return "".join(tekst)


def main(args):
    tekst = input("Podaj tekst: ")
    haslo = input("Podaj hasło: ")
    tekst = tekst.upper()
    haslo = haslo.upper()

    szyfrogram = szyfruj(tekst, haslo)

    print("Zaszyfrowane: ", szyfrogram)
    print("Deszyfrowane: ", deszyfruj(szyfrogram, haslo))

    return 0
# =ZNAK(JEŻELI(WIERSZ(A1)+KOLUMNA(A1)+63>90;WIERSZ(A1)+KOLUMNA(A1)+63-26;WIERSZ(A1)+KOLUMNA(A1)+63))

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
