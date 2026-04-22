import random as rand
from typing import List
from math import dist
import KlasyGrafu as Graf


def wygeneruj_graf(szerokosc = 10, wysokosc = 10):
    """
    Generuje graf na siatce szerokosc x wysokosc, wstawiajac jeden wierzcholek w losowym miejscu pola siatki
    :return: Lista obiektów Kopalni i Domków
    """


    domki: List[Graf.Domek] = []
    kopalnie: List[Graf.Kopalnia] = []

    indeks = 0
    for siatka_x in range (0, szerokosc):
        for siatka_y in range(0, wysokosc):

            x = siatka_x + rand.randint(0, 9)
            y = siatka_y + rand.randint(0, 9)

            if rand.randint(0, 1) == 0:
                nowy_domek = Graf.Domek(indeks, x, y, rand.choice(Graf.materialy))
                domki.append(nowy_domek)
            else:
                nowy_kopalnia = Graf.Kopalnia(indeks, x, y, rand.randint(1, 4), rand.choice(Graf.materialy))
                kopalnie.append(nowy_kopalnia)

            indeks += 1

    for polacz_domek in domki:
        for polacz_kopalnie in kopalnie:

            odleglosc = dist((polacz_domek.x, polacz_domek.y), (polacz_kopalnie.x, polacz_kopalnie.y)) + rand.random() * 2 - 1

            polacz_domek.dodaj_sasiada(polacz_kopalnie.indeks, odleglosc)
            polacz_kopalnie.dodaj_sasiada(polacz_domek.indeks, odleglosc)

    return domki + kopalnie