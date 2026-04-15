import math

def NajkrotszaDrogaKsiecia(points):
    """
    Wyznacza otoczkę wypukłą zbioru punktów (kopalni).
    Punkty to lista krotek (x, y).
    """
    n = len(points)
    if n <= 2:
        return points

    # Sortowanie punktów według współrzędnej x (i y dla remisu)
    points.sort()

    def cross_product(o, a, b):
        # Zwraca iloczyn wektorowy (OA x OB)
        # > 0: skręt w lewo, < 0: skręt w prawo, 0: współliniowe
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

    # Budowanie dolnej części otoczki
    lower = []
    for p in points:
        while len(lower) >= 2 and cross_product(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)

    # Budowanie górnej części otoczki
    upper = []
    for p in reversed(points):
        while len(upper) >= 2 and cross_product(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)

    # Połączenie (ostatni punkt każdej listy jest powtórzony na początku drugiej)
    return lower[:-1] + upper[:-1]

def ObliczDlugoscTrasy(hull):
    # Oblicza całkowitą długość trasy (obwód otoczki)
    perimeter = 0.0
    for i in range(len(hull)):
        p1 = hull[i]
        p2 = hull[(i + 1) % len(hull)]
        perimeter += math.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)
    return perimeter

# Przykład użycia:
mines = [(0, 3), (2, 2), (1, 1), (2, 1), (3, 0), (0, 0), (3, 3)]
route = NajkrotszaDrogaKsiecia(mines)
distance = ObliczDlugoscTrasy(route)