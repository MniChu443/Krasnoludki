import math
import random
from modele import klasy_grafu as KlasyGrafu
from narzedzia import drukarnia as Drukarnia


def najkrotsza_droga_ksiecia(points: list[KlasyGrafu.Kopalnia]):
    #Andrew Algorithm/Monotone chains algorithm O(n log n)
    
    n = len(points)
    if n <= 2:
        return points

    #Sortujemy wszystkie punkty wzgledem osi X, gdy mamy remisy sortujemy według Y
    points.sort(key = lambda k: k.pozycja)

    def cross_product(o, a, b):
        # iloczyn wektorowy, Jezeli wartosc jest >0 skręt w prawo, jezeli wartosc <0 skręt w lewo,
        # a jezeli jest rowna 0 to punkty sa wspoliniowe(leżą na jednej prostej)
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

    #Budujemy dolna czesc otoczki
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


def wyznacz_trase_ksiecia(miasto: KlasyGrafu.Miasto):

    if miasto.kopalnie:
        trasa = najkrotsza_droga_ksiecia(miasto.kopalnie)
        dlugosc = oblicz_dlugosc_trasy(trasa)
        Drukarnia.pokaz_otoczke(trasa, dlugosc)
    else:
        print("  Brak kopalni - trasa niemożliwa do wyznaczenia.")

def rozstaw_na_trasie(hull, odstep=15.0):
    if len(hull) < 2:
        return []

    punkty = []
    nastepny_cel = 0.0  # Dystans do następnego strażnika na bieżącej krawędzi
    
    for i in range(len(hull)):
        p1 = hull[i].pozycja
        p2 = hull[(i + 1) % len(hull)].pozycja
        
        dx = p2[0] - p1[0]
        dy = p2[1] - p1[1]
        dist = math.hypot(dx, dy)
        
        if dist == 0:
            continue
            
        dystans_na_krawedzi = nastepny_cel
        
        while dystans_na_krawedzi <= dist:
            t = dystans_na_krawedzi / dist
            nx = p1[0] + t * dx
            ny = p1[1] + t * dy
            glosnosc = random.randint(5, 50)
            punkty.append({
                "x": nx,
                "y": ny,
                "glosnosc": glosnosc
            })
            dystans_na_krawedzi += odstep
            
        # Przenosimy brakujący dystans na następną krawędź
        nastepny_cel = dystans_na_krawedzi - dist
            
    return punkty

