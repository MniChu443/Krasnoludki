import KlasyGrafu as Graf

#funckja znajdz_najblizsza_kopalenie ma za zadanie znalezc najblizsza kopalnie dla kazdego domku
# z uzwgleniem preferencji
# zwraca {kopalnia: indeks_kopalni, dystans: odleglosc}

def znajdz_najblizsza_kopalnie(lista_wierzcholkow):

    wierzcholki = {}

    domki = []
    kopalnie = []

    for v in lista_wierzcholkow:
        wierzcholki[v.indeks] = v

        if isinstance(v, Graf.Domek):
            domki.append(v)
        elif isinstance(v, Graf.Kopalnia):
            kopalnie.append(v)

    wynik = {}

    for domek in domki:
        pasujace_kopalnie = []
        for k in kopalnie:
            if k.zloze == domek.preferencja:
                pasujace_kopalnie.append(k)

        if len(pasujace_kopalnie) == 0:
            pasujace_kopalnie = kopalnie

        najlepsza_kopalnia = None
        najlepszy_dystans = 999999999

        for k in pasujace_kopalnie:
            for sasiad in domek.sasiedzi:
                if sasiad.indeks_sasiada == k.indeks:
                    if sasiad.odleglosc < najlepszy_dystans:
                        najlepszy_dystans = sasiad.odleglosc
                        najlepsza_kopalnia = k.indeks

        if najlepsza_kopalnia is None:
            wynik[domek.indeks] = {
                "kopalnia": None,
                "dystans": None
            }
        else:
            wynik[domek.indeks] = {
                "kopalnia": najlepsza_kopalnia,
                "dystans": najlepszy_dystans
            }

    return wynik