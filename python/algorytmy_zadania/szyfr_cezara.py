#!/usr/bin/env python
# -*- coding: utf-8 -*-

def szyfruj(tekst, klucz):
    """Szyfrowanie tekstu za pomocą szyfru Cezara"""

    szyfrogram = ""
    klucz = klucz % 26
    for znak in tekst:
        ascii = ord(znak) + klucz
        if ord(znak) == 32:
            ascii = 32
        if ascii > 90 and ascii < 97:
            ascii -= 26
        elif ascii > 122:
            ascii -= 26
        szyfrogram += chr(ascii)
    return szyfrogram



def deszyfruj(szyfrogram, klucz):
    tekst = ""
    for znak in szyfrogram:
        ascii = ord(znak) - klucz
        if ord(znak) == 32:
            ascii = 32
        if ascii < 65 and ascii != 32:
            ascii +=26
        if ascii > 90 and ascii < 97 and ascii !=32:
            ascii += 26
        if znak.isdigit():
            ascii -= 26
        tekst += chr(ascii)
    return tekst

# obsłużyć małe i duże litery
# obsłużyć spacje


def main(args):
    tekst = input("Podaj tekst: ")
    klucz = int(input("Podaj klucz: "))
    szyfrogram = szyfruj(tekst, klucz)
    print(szyfrogram)
    print(deszyfruj(szyfrogram, klucz))
    return 0


if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
