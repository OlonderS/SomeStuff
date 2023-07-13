#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  horner.py


def horner_it(st, tbwsp, x):
    wynik = tbwsp[0]
    for i in range(1, st + 1):
        wynik = wynik * x + tbwsp[i]
    return wynik

def horner_rek(st, tbwsp, x):
    if st == 0:
        return tbwsp[0]
    return horner_rek(st - 1, tbwsp, x) * x + tbwsp [st]

def main(args):
    tbwsp = []
    stopien = 3
    x = int(input("Podaj wartosc argumentu: "))
    for i in range(0, 4):
        tmp = int(input("Podaj wspolczynnik wielomianu: "))
        tbwsp.append(tmp)

    print("Wynik wielomianu wynosi: ", horner_it(stopien, tbwsp, x))
    print("Wynik wielomianu wynosi: ", horner_rek(stopien, tbwsp, x))
    return 0


if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
