#!/usr/bin/env python
# -*- coding: utf-8 -*-



from __future__ import division


def main(args):
    reszty = []
    liczba = int(input("Podaj liczbe(dec): "))
    podstawa = int(input("Podaj podstawe(dec): "))

    while liczba > 0:
        reszta = liczba % podstawa
        reszty.append(reszta)
        liczba = int(liczba / podstawa)

    reszty.reverse()  #  odwrócenie kolejności
    print(reszty)

    return 0


if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
