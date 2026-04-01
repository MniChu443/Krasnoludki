from random import randint, choice
from typing import List
from math import dist

import KlasyGrafu as Graf

domki: List[Graf.Domek] = []
kopalnie: List[Graf.Kopalnia] = []


for siatka_x in range (0, 10):
    for siatka_y in range(0, 10):

        x = siatka_x + randint(0, 9)
        y = siatka_y + randint(0, 9)

        if randint(0, 1) == 0:
            nowy_domek = Graf.Domek(x, y, choice(Graf.materialy))
            domki.append(nowy_domek)
        else:
            nowy_kopalnia = Graf.Kopalnia(x, y, randint(1, 4), choice(Graf.materialy))
            kopalnie.append(nowy_kopalnia)


for polacz_domek in domki:
    for polacz_kopalnie in kopalnie:

        odleglosc = dist((polacz_domek.x, polacz_domek.y), (polacz_kopalnie.x, polacz_kopalnie.y))

        polacz_domek.dodaj_sasiada(polacz_kopalnie, odleglosc)
        polacz_kopalnie.dodaj_sasiada(polacz_domek, odleglosc)


# Sasiedzi pierwszego domka
print(domki[0])
for domek0 in domki[0].sasiedzi:
    print(domek0)