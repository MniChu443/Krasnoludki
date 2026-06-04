from modele import klasy_grafu as KlasyGrafu

#funckja znajdz_najblizsza_kopalenie ma za zadanie znalezc najblizsza kopalnie dla kazdego domku
# z uzwgleniem preferencji
# zwraca {kopalnia: indeks_kopalni, dystans: odleglosc}

def znajdz_najblizsza_kopalnie(miasto: KlasyGrafu.Miasto):

    wynik = {}

    for domek in miasto.domki:
        pasujace_kopalnie = []
        for k in miasto.kopalnie:
            if k.zloze == domek.preferencja:
                pasujace_kopalnie.append(k)

        if len(pasujace_kopalnie) == 0:
            pasujace_kopalnie = miasto.kopalnie

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