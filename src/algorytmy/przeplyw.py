from modele import klasy_grafu as KlasyGrafu


class Polaczenie:

    def __init__(self, indeks: int, przepustowosc: int, odleglosc: float):
        self.sasiad = indeks
        self.przepustowosc = przepustowosc
        self.odleglosc = odleglosc

    def __str__(self):
        return f"-{self.przepustowosc}-> {self.sasiad}"

    def __repr__(self):
        return str(self)


class Wierzcholek:

    def __init__(self, indeks: int):
        self.indeks = indeks
        self.polaczenia = []

    def __str__(self):
        sasiedzi = ""
        for p in self.polaczenia: sasiedzi += f" | {p}"
        return f"({self.indeks}){sasiedzi}"

    def __repr__(self):
        return str(self)

    def dodaj_polaczenie(self, indeks: int, przepustowosc: int, odleglosc: float = 0):
        self.polaczenia.append(Polaczenie(indeks, przepustowosc, odleglosc))


class GrafDwudzielny:

    def __init__(self, miasto: KlasyGrafu.Miasto):

        self.ujscie = Wierzcholek(len(miasto))
        self.zrodlo = Wierzcholek(len(miasto) + 1)
        self.lista_wierzcholkow = [self.ujscie, self.zrodlo]

        self.indeksy_domkow: list[int] = []
        self.indeksy_kopalni: list[int] = []
        self.zloza_kopalni: list[str] = []

        for kopalnia in miasto.kopalnie:
            nowy = Wierzcholek(kopalnia.indeks)
            nowy.dodaj_polaczenie(self.ujscie.indeks, kopalnia.pojemnosc)

            self.indeksy_kopalni.append(kopalnia.indeks)
            self.zloza_kopalni.append(kopalnia.zloze)
            self.lista_wierzcholkow.append(nowy)

        for domek in miasto.domki:
            nowy = Wierzcholek(domek.indeks)
            self.zrodlo.dodaj_polaczenie(domek.indeks, 1)

            for indeks, indeks_kopalni in enumerate(self.indeksy_kopalni):
                if domek.preferencja != self.zloza_kopalni[indeks]: continue
                nowy.dodaj_polaczenie(indeks_kopalni, 1)

            self.indeksy_domkow.append(domek.indeks)
            self.lista_wierzcholkow.append(nowy)

    def __str__(self):
        wierzcholki = ""
        for w in self.lista_wierzcholkow: wierzcholki += f"{w}\n"
        return wierzcholki

    def __repr__(self):
        return str(self)