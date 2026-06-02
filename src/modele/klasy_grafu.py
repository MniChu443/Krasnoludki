from typing import List

materialy = ["ZLOTO", "DIAMENTY", "WEGIEL", "REDSTONE", "LAPIS", "ZELAZO"]


class Sasiad:

    def __init__(self, sasiad: int, odleglosc: float):
        self.indeks_sasiada = sasiad
        self.odleglosc = odleglosc

    def __str__(self):
        return f"Wierzcholek nr {self.indeks_sasiada} w odleglosci {self.odleglosc}"

    def __repr__(self):
        return str(self)


class NodeGrafu:

    def __init__(self, indeks: int, x: float, y: float):
        self.indeks = indeks
        self.pozycja = (x, y)
        self.sasiedzi: List[Sasiad] = []

    def dodaj_sasiada(self, sasiad: int, odleglosc: float):
        nowy_sasiad = Sasiad(sasiad, odleglosc)
        self.sasiedzi.append(nowy_sasiad)


class Domek(NodeGrafu):

    def __init__(self, indeks: int, x: float, y: float, preferencja: str):
        super().__init__(indeks, x, y)
        self.preferencja = preferencja

    def __str__(self):
        return f"Domek w pozycji ({self.pozycja[0]}, {self.pozycja[1]}), krasnal lubi {self.preferencja}"

    def __repr__(self):
        return str(self)


class Kopalnia(NodeGrafu):

    def __init__(self, indeks: int, x: int, y: int, pojemnosc: int, zloze: str):
        super().__init__(indeks, x, y)
        self.pojemnosc = pojemnosc
        self.zloze = zloze

    def __str__(self):
        return f"Kopalnia w pozycji ({self.pozycja[0]}, {self.pozycja[1]}), pelna {self.zloze} ma {self.pojemnosc} miejsc"

    def __repr__(self):
        return str(self)