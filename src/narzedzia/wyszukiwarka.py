#funkcja zwrajaca indeksy (miejsca) na ktorych
#znajduja sie wyszukiwane frazy

from algorytmy import Boyer_i_Moore

def szukaj(plik, fraza):
    opened = open(plik, "r")
    znalezione = []
    suma_znakow = 0
    while True:
        linia = opened.readline()
        if not linia:
            opened.close()
            break
        indeks = Boyer_i_Moore.boyer_moore(linia, fraza)
        if indeks != -1:
            znalezione.append(indeks + suma_znakow)
        suma_znakow += len(linia)
    return znalezione