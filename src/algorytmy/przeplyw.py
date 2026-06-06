from modele import klasy_grafu as KlasyGrafu
from narzedzia import czasomierz as Czas


class Polaczenie:

    def __init__(self, indeks: int, przepustowosc: int, odleglosc: float, przeplyw: int = 0, wsteczna: bool = False):
        self.sasiad = indeks
        self.przepustowosc = przepustowosc
        self.odleglosc = odleglosc
        self.przeplyw = przeplyw
        self.wsteczna = wsteczna

    def kopia(self) -> Polaczenie:
        return Polaczenie(self.sasiad, self.przepustowosc, self.odleglosc, self.przeplyw)

    def __str__(self):
        if self.wsteczna: return f"<-{self.przeplyw}/{self.przepustowosc}- {self.sasiad}"
        if self.odleglosc == 0: return f"-{self.przeplyw}/{self.przepustowosc}-> {self.sasiad}"
        return f"-{self.przeplyw}/{self.przepustowosc}-> {self.sasiad} ({self.odleglosc:.1f})"

    def __repr__(self):
        return str(self)


class Wierzcholek:

    def __init__(self, indeks: int):
        self.indeks = indeks
        self.polaczenia: list[Polaczenie] = []

    def __str__(self):
        sasiedzi = ""
        puste = ""
        for p in self.polaczenia:
            if p.przeplyw <= 0:
                puste += f" | {p}"
                continue
            sasiedzi += f" | {p}"
        if puste != "": sasiedzi += f"\n\033[90m   ↳ {puste}\033[0m"
        return f"({self.indeks:3}){sasiedzi}"

    def __repr__(self):
        return str(self)

    def __iter__(self):
        return iter(self.polaczenia)

    def __len__(self):
        return len(self.polaczenia)

    def __getitem__(self, item):
        return self.polaczenia[item]

    def do(self, sasiad: int) -> Polaczenie:
        for polaczenie in self.polaczenia:
            if polaczenie.sasiad == sasiad: return polaczenie
        raise f"Sąsiad nie istnieje! {self.indeks}.do({sasiad})"

    def dodaj_polaczenie(self, indeks: int, przepustowosc: int, odleglosc: float = 0, przeplyw: int = 0, wsteczna: bool = False):
        self.polaczenia.append(Polaczenie(indeks, przepustowosc, odleglosc, przeplyw, wsteczna))


class GrafDwudzielny:

    def __init__(self, miasto: KlasyGrafu.Miasto):

        self.ujscie = Wierzcholek(len(miasto))
        self.zrodlo = Wierzcholek(len(miasto) + 1)
        self.graf: list[Wierzcholek] = []

        self.polacz_budynki(miasto)

    def polacz_budynki(self, miasto):

        graf_tymczasowy: list[Wierzcholek | None] = [ None for _ in range(len(miasto)) ]

        Czas.start("  Łączenie kopalnia-ujście")
        for kopalnia in miasto.kopalnie:
            nowy = Wierzcholek(kopalnia.indeks)
            nowy.dodaj_polaczenie(self.ujscie.indeks, kopalnia.pojemnosc)

            graf_tymczasowy[kopalnia.indeks] = nowy
        Czas.stop()

        Czas.start("  Łączenie domek-kopalnia i źródło-domek")
        for domek in miasto.domki:
            nowy = Wierzcholek(domek.indeks)
            self.zrodlo.dodaj_polaczenie(domek.indeks, 1)

            for kopalnia in miasto.kopalnie:
                if domek.preferencja != kopalnia.zloze: continue
                nowy.dodaj_polaczenie(kopalnia.indeks, 1, kopalnia.odleglosc(domek))

            graf_tymczasowy[domek.indeks] = nowy
        Czas.stop()

        for wierzcholek in graf_tymczasowy:
            if wierzcholek is None: raise "Błąd: Nie wczytano wszystkich budynków"
            self.graf.append(wierzcholek)

        self.graf.append(self.ujscie)
        self.graf.append(self.zrodlo)

    def __str__(self):
        wierzcholki = ""
        for w in self.graf: wierzcholki += f"{w}\n"
        return wierzcholki

    def __repr__(self):
        return str(self)


class SiecPrzeplywowa:

    def __init__(self, miasto: KlasyGrafu.Miasto):

        self.dwudzielny = GrafDwudzielny(miasto)
        self.siec_rezydualna: list[Wierzcholek] = []

        self.wygeneruj_siec_rezydualna()

        self.ujscie = self.siec_rezydualna[self.dwudzielny.ujscie.indeks]
        self.zrodlo = self.siec_rezydualna[self.dwudzielny.zrodlo.indeks]

    def wygeneruj_siec_rezydualna(self):

        Czas.start("  Kopiowanie wierzchołków")
        for wierzcholek in self.dwudzielny.graf:
            kopia_wierzcholka = Wierzcholek(wierzcholek.indeks)
            for polaczenie in wierzcholek:
                kopia_polaczenia = polaczenie.kopia()
                kopia_polaczenia.przeplyw = polaczenie.przepustowosc
                kopia_wierzcholka.polaczenia.append(kopia_polaczenia)
            self.siec_rezydualna.append(kopia_wierzcholka)
        Czas.stop()

        Czas.start("  Dodawanie wstecznych połączeń")
        for wierzcholek in self.dwudzielny.graf:
            for polaczenie in wierzcholek:
                self.siec_rezydualna[polaczenie.sasiad].dodaj_polaczenie(wierzcholek.indeks, polaczenie.przepustowosc,
                                                                         -polaczenie.odleglosc, 0, True)
        Czas.stop()

        Czas.start("  Sortowanie połączeń")
        for wierzcholek in self.siec_rezydualna:
            wierzcholek.polaczenia.sort( key = lambda x: x.sasiad )
        Czas.stop()

    def bfs_sciezka_powiekszajaca(self) -> list[int] | None:

        odwiedzone: list[bool] = [ False for _ in self.siec_rezydualna ]
        cofanie: list[int | None] = [ None for _ in self.siec_rezydualna ]
        kolejka: list[int] = [self.zrodlo.indeks]

        while len(kolejka) > 0:
            indeks = kolejka.pop(0)
            odwiedzone[indeks] = True

            sprawdzany = self.siec_rezydualna[indeks]

            for polaczenie in sprawdzany.polaczenia:
                if odwiedzone[polaczenie.sasiad]: continue
                if polaczenie.przeplyw <= 0: continue

                kolejka.append(polaczenie.sasiad)
                cofanie[polaczenie.sasiad] = sprawdzany.indeks

                if polaczenie.sasiad == self.ujscie.indeks: break

        if cofanie[self.ujscie.indeks] is None:
            return None

        sciezka = []
        indeks = self.ujscie.indeks
        while indeks is not None:
            sciezka.append(indeks)
            indeks = cofanie[indeks]
        sciezka.reverse()

        return sciezka

    def mozliwy_przeplyw(self, sciezka: list[int]):

        minimum = 999999999
        for indeks in range(len(sciezka) - 1):
            przeplyw = self.siec_rezydualna[sciezka[indeks]].do(sciezka[indeks + 1]).przeplyw
            if przeplyw < minimum: minimum = przeplyw

        return minimum

    def zmniejsz_sciezke(self, sciezka: list[int]):

        przeplyw = self.mozliwy_przeplyw(sciezka)
        for indeks in range(len(sciezka) - 1):
            self.siec_rezydualna[sciezka[indeks]].do(sciezka[indeks + 1]).przeplyw -= przeplyw
            self.siec_rezydualna[sciezka[indeks + 1]].do(sciezka[indeks]).przeplyw += przeplyw

    def ff_maksymalny_przeplyw(self):

        print("> Wyznaczanie maksymalnego przepływu")
        while True:
            Czas.start("  Szukanie ścieżki powiększającej")
            sciezka = self.bfs_sciezka_powiekszajaca()
            Czas.stop()
            if sciezka is None: break
            print(f"  Znaleziono ścieżkę pomniejszającą {sciezka}")
            self.zmniejsz_sciezke(sciezka)
        print("  Znaleziono maksymalny przepływ")

    def bf_ujemny_cykl(self) -> list[int] | None:

        dystanse: list[float] = [ 999999999 for _ in range(len(self.siec_rezydualna)) ]
        dystanse[self.zrodlo.indeks] = 0
        rodzice: list[int] = [ -1 for _ in range(len(self.siec_rezydualna)) ]
        ujemny_cykl: int = -1

        for _ in range(len(self.siec_rezydualna)):

            ujemny_cykl = -1

            for wierzcholek in self.siec_rezydualna:
                for polaczenie in wierzcholek:

                    if polaczenie.przeplyw <= 0: continue

                    odleglosc: float = dystanse[wierzcholek.indeks] + wierzcholek.do(polaczenie.sasiad).odleglosc
                    if dystanse[polaczenie.sasiad] <= odleglosc: continue

                    rodzice[polaczenie.sasiad] = wierzcholek.indeks
                    dystanse[polaczenie.sasiad] = odleglosc
                    ujemny_cykl = polaczenie.sasiad

            if ujemny_cykl == -1: return None

        for _ in range(len(self.siec_rezydualna)):
            ujemny_cykl = rodzice[ujemny_cykl]

        cykl: list[int] = [ujemny_cykl]
        while True:
            ujemny_cykl = rodzice[ujemny_cykl]
            cykl.append(ujemny_cykl)
            if ujemny_cykl == cykl[0]: break

        cykl.reverse()

        return cykl

    def cc_minimalna_odleglosc(self):

        print("> Znajdowanie lepszej odległości")
        while True:
            Czas.start()
            cykl = self.bf_ujemny_cykl()
            if cykl is None:
                Czas.stop("  Brak ujemnego cyklu")
                break
            self.zmniejsz_sciezke(cykl)
            Czas.stop(f"  Cykl ujemny wykryty {cykl}")

    def przekonwertuj_przeplyw(self):

        for wierzcholek in self.dwudzielny.graf:
            for polaczenie in wierzcholek:
                x = self.siec_rezydualna[polaczenie.sasiad].do(wierzcholek.indeks)
                if x.wsteczna:
                    polaczenie.przeplyw = x.przeplyw

    def PAROWANIE(self) -> list[tuple[int, int]]:

        self.ff_maksymalny_przeplyw()
        self.cc_minimalna_odleglosc()

        self.przekonwertuj_przeplyw()
        pary = []

        Czas.start("> Generowanie par")
        for wierzcholek in self.dwudzielny.graf:
            if wierzcholek.indeks == self.zrodlo.indeks: continue

            for polaczenie in wierzcholek:
                if polaczenie.sasiad == self.ujscie.indeks: continue
                if polaczenie.przeplyw <= 0: continue
                pary.append((wierzcholek.indeks, polaczenie.sasiad))
        Czas.stop()

        return pary

    def __str__(self):
        wierzcholki = ""
        for w in self.siec_rezydualna: wierzcholki += f"{w}\n"
        return wierzcholki

    def __repr__(self):
        return str(self)