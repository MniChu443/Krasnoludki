import math
from modele import klasy_grafu as KlasyGrafu


def najkrotsza_droga_ksiecia(points: list[KlasyGrafu.Kopalnia]):
    """
    Wyznacza otoczkę wypukłą zbioru punktów (kopalni).
    Punkty to lista Kopalni.
    """
    n = len(points)
    if n <= 2:
        return points

    # Sortowanie punktów według współrzędnej x (i y dla remisu)
    points.sort(key = lambda k: k.pozycja)

    def cross_product(o, a, b):
        # Zwraca iloczyn wektorowy (OA x OB)
        # > 0: skręt w lewo, < 0: skręt w prawo, 0: współliniowe
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

    # Budowanie dolnej części otoczki
    lower = []
    for p in points:
        while len(lower) >= 2 and cross_product(lower[-2].pozycja, lower[-1].pozycja, p.pozycja) <= 0:
            lower.pop()
        lower.append(p)

    # Budowanie górnej części otoczki
    upper = []
    for p in reversed(points):
        while len(upper) >= 2 and cross_product(upper[-2].pozycja, upper[-1].pozycja, p.pozycja) <= 0:
            upper.pop()
        upper.append(p)

    # Połączenie (ostatni punkt każdej listy jest powtórzony na początku drugiej)
    return lower[:-1] + upper[:-1]


def oblicz_dlugosc_trasy(hull):
    # Oblicza całkowitą długość trasy (obwód otoczki)
    perimeter = 0.0
    for i in range(len(hull)):
        p1 = hull[i].pozycja
        p2 = hull[(i + 1) % len(hull)].pozycja
        perimeter += math.sqrt((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2)
    return perimeter
