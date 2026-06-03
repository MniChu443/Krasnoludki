import random as rand
from typing import List
from math import dist
from modele import klasy_grafu as Graf


def wygeneruj_graf(szerokosc: int = 10, wysokosc: int = 10, proporcja: float = 0.5, perkolacja: float = 1, generuj_sasiadow: bool = False):
    """
    Generuje graf na siatce szerokosc x wysokosc, wstawiajac jeden wierzcholek w losowym miejscu pola siatki
    proporcja: 0 - same kopalnie, 1 - same domki
    :return: Lista obiektów Kopalni i Domków
    """

    if szerokosc <= 0: raise "Szerokosc musi byc liczba naturalna (" + str(szerokosc) + ")"
    if wysokosc <= 0: raise "Wysokosc musi byc liczba naturalna (" + str(wysokosc) + ")"
    if not 0 <= proporcja <= 1: raise "Proporcja musi byc w przedziale 0-1 (" + str(proporcja) + ")"
    if not 0 <= perkolacja <= 1: raise "Perkolacja musi byc w przedziale 0-1 (" + str(perkolacja) + ")"

    domki: List[Graf.Domek] = []
    kopalnie: List[Graf.Kopalnia] = []

    indeks = 0
    for siatka_x in range (0, szerokosc):
        for siatka_y in range(0, wysokosc):

            if rand.uniform(0, 1) > perkolacja:
                continue

            x = siatka_x * 10 + rand.randint(0, 9)
            y = siatka_y * 10 + rand.randint(0, 9)

            if rand.uniform(0, 1) < proporcja:
                nowy_domek = Graf.Domek(indeks, x, y, rand.choice(Graf.materialy))
                domki.append(nowy_domek)
            else:
                nowy_kopalnia = Graf.Kopalnia(indeks, x, y, rand.randint(1, 4), rand.choice(Graf.materialy))
                kopalnie.append(nowy_kopalnia)

            indeks += 1

    if len(domki) == 0: domki.append(Graf.Domek(indeks, 0, 0, rand.choice(Graf.materialy)))
    if len(kopalnie) == 0: kopalnie.append(Graf.Kopalnia(indeks, 0, 0, rand.randint(1, 4), rand.choice(Graf.materialy)))

    if not generuj_sasiadow:
        return domki + kopalnie

    for polacz_domek in domki:
        for polacz_kopalnie in kopalnie:

            # Obliczanie odległości między kopalnią i domkiem (możliwe dewiacje)
            odleglosc = dist((polacz_domek.pozycja[0], polacz_domek.pozycja[1]), (polacz_kopalnie.pozycja[0], polacz_kopalnie.pozycja[1])) # + rand.random() * 2 - 1

            polacz_domek.dodaj_sasiada(polacz_kopalnie.indeks, odleglosc)
            polacz_kopalnie.dodaj_sasiada(polacz_domek.indeks, odleglosc)

    return domki + kopalnie