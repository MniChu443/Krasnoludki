#funkcja zwrajaca indeksy (miejsca) na ktorych
#znajduja sie wyszukiwane frazy

from algorytmy import Boyer_i_Moore

def szukaj(plik, fraza):
    znalezione = []
    suma_znakow = 0

    with open(plik, "r", encoding="utf-8") as opened:
        for linia in opened:
            start = 0
            while start < len(linia):
                indeks = Boyer_i_Moore.boyer_moore(linia[start:], fraza)
                if indeks == -1:
                    break
                znalezione.append(suma_znakow + start + indeks)
                start += indeks + 1
            suma_znakow += len(linia)
    return znalezione