from modele import klasy_grafu as KlasyGrafu


class Polaczenie:

    def __init__(self, indeks: int, przepustowosc: int):
        self.sasiad = indeks
        self.przepustowosc = przepustowosc

    def __str__(self):
        return f" -{self.przepustowosc}-> {self.sasiad}"

    def __repr__(self):
        return str(self)


class Wierzcholek:

    def __init__(self, indeks: int):
        self.indeks = indeks
        self.polaczenia = []

    def __str__(self):
        sasiedzi = ""
        for p in self.polaczenia: sasiedzi += f"{p}"
        return f"({self.indeks}){sasiedzi}"

    def __repr__(self):
        return str(self)

    def dodaj_polaczenie(self, indeks: int, przepustowosc: int):
        self.polaczenia.append(Polaczenie(indeks, przepustowosc))


class GrafDwudzielny:

    def __init__(self, graf: list[KlasyGrafu.Domek | KlasyGrafu.Kopalnia]):

        self.lista_wierzcholkow = []
        self.ujscie = Wierzcholek(len(graf))
        self.zrodlo = Wierzcholek(len(graf) + 1)

        self.indeksy_domkow = []
        self.indeksy_kopalni = []

        for indeks in range(len(graf)):
            nowy = Wierzcholek(indeks)

            if type(graf[indeks]) == KlasyGrafu.Domek:
                self.indeksy_domkow.append(indeks)
                self.zrodlo.dodaj_polaczenie(indeks, 1)
            else:
                self.indeksy_kopalni.append(indeks)
                nowy.dodaj_polaczenie(self.ujscie.indeks, graf[indeks].pojemnosc)

            self.lista_wierzcholkow.append(nowy)

        self.lista_wierzcholkow.append(self.ujscie)
        self.lista_wierzcholkow.append(self.zrodlo)

        for indeks_domku in self.indeksy_domkow:
            for indeks_kopalni in self.indeksy_kopalni:

                self.lista_wierzcholkow[indeks_domku].dodaj_polaczenie(indeks_kopalni, 1)

    def __str__(self):
        wierzcholki = ""
        for w in self.lista_wierzcholkow: wierzcholki += f"{w}\n"
        return wierzcholki

    def __repr__(self):
        return str(self)