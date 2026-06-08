#funkcja zwraca indeks pierwszego znalezionego dopasowania wzorca w tekście
#jeśli nie znaleziono dopasowania, zwraca -1

#algorytm sluzy do wyszkuiwania w teksie oraz do kompresji(?)

def boyer_moore(tekst: str, wzorzec: str):
    dlugosc_tekstu = len(tekst)
    dlugosc_wzorca = len(wzorzec)
    if dlugosc_wzorca == 0:
        return 0
    if dlugosc_wzorca > dlugosc_tekstu:
        return -1

    ostatnie_wystapienie = {}
    for indeks, znak in enumerate(wzorzec):
        ostatnie_wystapienie[znak] = indeks

    przesuniecia = [0] * (dlugosc_wzorca + 1)
    granice = [0] * (dlugosc_wzorca + 1)
    i = dlugosc_wzorca
    j = dlugosc_wzorca + 1
    granice[i] = dlugosc_wzorca + 1
    while i > 0:
        while j <= dlugosc_wzorca and wzorzec[i - 1] != wzorzec[j - 1]:
            if przesuniecia[j] == 0:
                przesuniecia[j] = j - i
            j = granice[j]
        i -= 1
        j -= 1
        granice[i] = j

    j = granice[0]
    for i in range(dlugosc_wzorca + 1):
        if przesuniecia[i] == 0:
            przesuniecia[i] = j
        if i == j:
            j = granice[j]
    poczatek = 0


    while poczatek <= dlugosc_tekstu - dlugosc_wzorca:
        indeks_wzorca = dlugosc_wzorca - 1
        while indeks_wzorca >= 0 and wzorzec[indeks_wzorca] == tekst[poczatek + indeks_wzorca]:
            indeks_wzorca -= 1

        if indeks_wzorca < 0:
            return poczatek
        znak_tekstu = tekst[poczatek + indeks_wzorca]

        ostatni_indeks = ostatnie_wystapienie.get(znak_tekstu, -1)

        przesuniecie_zlego_znaku = indeks_wzorca - ostatni_indeks

        przesuniecie_dobrego_sufiksu = przesuniecia[indeks_wzorca + 1]

        poczatek += max(1, przesuniecie_zlego_znaku, przesuniecie_dobrego_sufiksu)
    return -1