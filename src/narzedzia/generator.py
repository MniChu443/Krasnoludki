import random as rand
from math import dist
from modele import klasy_grafu as KlasyGrafu


def wygeneruj_miasto(szerokosc: int = 10, wysokosc: int = 10, proporcja: float = 0.5, perkolacja: float = 1, materialy: list[str] = None, generuj_sasiadow: bool = False):
    """
    Generuje graf na siatce szerokosc x wysokosc, wstawiajac jeden wierzcholek w losowym miejscu pola siatki
    proporcja: 0 - same kopalnie, 1 - same domki
    :return: Lista obiektów Kopalni i Domków
    """

    if szerokosc <= 0: raise "Szerokosc musi byc liczba naturalna (" + str(szerokosc) + ")"
    if wysokosc <= 0: raise "Wysokosc musi byc liczba naturalna (" + str(wysokosc) + ")"
    if not 0 <= proporcja <= 1: raise "Proporcja musi byc w przedziale 0-1 (" + str(proporcja) + ")"
    if not 0 <= perkolacja <= 1: raise "Perkolacja musi byc w przedziale 0-1 (" + str(perkolacja) + ")"

    miasto = KlasyGrafu.Miasto(materialy)

    indeks = 0
    for siatka_x in range (0, szerokosc):
        for siatka_y in range(0, wysokosc):

            if rand.uniform(0, 1) > perkolacja:
                continue

            x = siatka_x * 10 + rand.randint(0, 9)
            y = siatka_y * 10 + rand.randint(0, 9)

            if rand.uniform(0, 1) < proporcja:
                nowy = KlasyGrafu.Domek(indeks, x, y, rand.choice(miasto.materialy))
            else:
                nowy = KlasyGrafu.Kopalnia(indeks, x, y, rand.randint(1, 4), rand.choice(miasto.materialy))

            miasto.dodaj(nowy)

            indeks += 1

    if len(miasto.domki) == 0: miasto.domki.append(KlasyGrafu.Domek(indeks, 0, 0, rand.choice(miasto.materialy)))
    if len(miasto.kopalnie) == 0: miasto.kopalnie.append(KlasyGrafu.Kopalnia(indeks, 0, 0, rand.randint(1, 4), rand.choice(miasto.materialy)))

    if not generuj_sasiadow:
        return miasto

    """
    TO PONIŻEJ ZOSTANIE USUNIĘTE
    """

    for polacz_domek in miasto.domki:
        for polacz_kopalnie in miasto.kopalnie:

            # Obliczanie odległości między kopalnią i domkiem (możliwe dewiacje)
            odleglosc = dist((polacz_domek.pozycja[0], polacz_domek.pozycja[1]), (polacz_kopalnie.pozycja[0], polacz_kopalnie.pozycja[1])) # + rand.random() * 2 - 1

            polacz_domek.dodaj_sasiada(polacz_kopalnie.indeks, odleglosc)
            polacz_kopalnie.dodaj_sasiada(polacz_domek.indeks, odleglosc)

    return miasto