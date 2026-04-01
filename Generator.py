from random import randint, choice
import KlasyGrafu as Graf

domki = []
kopalnie = []

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

