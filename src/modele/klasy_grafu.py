from __future__ import annotations
from math import dist

MATERIALY_TESTOWE = ["ZLOTO", "DIAMENTY", "WEGIEL", "REDSTONE", "LAPIS", "ZELAZO"]


class Sasiad:
    """Klasa z informacją o innym wierzchołku"""

    def __init__(self, sasiad: int, odleglosc: float):
        self.indeks_sasiada = sasiad
        self.odleglosc = odleglosc

    def __str__(self):
        return f"Wierzcholek nr {self.indeks_sasiada} w odleglosci {self.odleglosc}"

    def __repr__(self):
        return str(self)


class Budynek:
    """Bazowa klasa dla budynku"""

    def __init__(self, indeks: int, x: float, y: float):
        self.indeks = indeks
        self.pozycja = (x, y)
        self.sasiedzi: list[Sasiad] = []

    def dodaj_sasiada(self, sasiad: int, odleglosc: float):
        nowy_sasiad = Sasiad(sasiad, odleglosc)
        self.sasiedzi.append(nowy_sasiad)

    def odleglosc(self, node: Budynek):
        return dist((self.pozycja[0], self.pozycja[1]), (node.pozycja[0], node.pozycja[1]))


class Domek(Budynek):
    """Klasa domku z informacją o mieszkającym w nim krasnoludku"""

    def __init__(self, indeks: int, x: float, y: float, preferencja: str):
        super().__init__(indeks, x, y)
        self.preferencja = preferencja

    def __str__(self):
        return f"Domek w pozycji ({self.pozycja[0]}, {self.pozycja[1]}), krasnal lubi {self.preferencja}"

    def __repr__(self):
        return str(self)


class Kopalnia(Budynek):
    """Klasa z informacjami o kopalni"""

    def __init__(self, indeks: int, x: int, y: int, pojemnosc: int, zloze: str):
        super().__init__(indeks, x, y)
        self.pojemnosc = pojemnosc
        self.zloze = zloze

    def __str__(self):
        return f"Kopalnia w pozycji ({self.pozycja[0]}, {self.pozycja[1]}), pelna {self.zloze} ma {self.pojemnosc} miejsc"

    def __repr__(self):
        return str(self)


class Miasto:
    """Klasa zbioru domków i kopalni z informacją o dostępnych surowcach"""

    def __init__(self, materialy: list[str] = None):
        self.domki: list[Domek] = []
        self.kopalnie: list[Kopalnia] = []

        if materialy is None: materialy = MATERIALY_TESTOWE
        self.materialy: list[str] = materialy

    def __iter__(self):
        return iter(self.domki + self.kopalnie)

    def __len__(self):
        return len(self.domki) + len(self.kopalnie)

    def __getitem__(self, item):
        return (self.domki + self.kopalnie)[item]

    def dodaj(self, budynek: Domek | Kopalnia):
        if isinstance(budynek, Domek): self.domki.append(budynek)
        else: self.kopalnie.append(budynek)
