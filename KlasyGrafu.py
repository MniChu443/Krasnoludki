from typing import List

materialy = ["ZLOTO", "DIAMENTY", "WEGIEL", "REDSTONE", "LAPIS", "ZELAZO"]


class Sasiad:

    def __init__(self, node: NodeGrafu, odleglosc: float):
        self.node = node
        self.odleglosc = odleglosc

    def __str__(self):
        return f"{self.node} w odleglosci {self.odleglosc}"


class NodeGrafu:

    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y
        self.sasiedzi: List[Sasiad] = []

    def dodaj_sasiada(self, sasiad: NodeGrafu, odleglosc: float):
        nowy_sasiad = Sasiad(sasiad, odleglosc)
        self.sasiedzi.append(nowy_sasiad)


class Domek(NodeGrafu):

    def __init__(self, x: float, y: float, preferencja: str):
        super().__init__(x, y)
        self.preferencja = preferencja

    def __str__(self):
        return f"Domek w pozycji ({self.x}, {self.y}), krasnal lubi {self.preferencja}"


class Kopalnia(NodeGrafu):

    def __init__(self, x: int, y: int, pojemnosc: int, zloze: str):
        super().__init__(x, y)
        self.pojemnosc = pojemnosc
        self.zloze = zloze

    def __str__(self):
        return f"Kopalnia w pozycji ({self.x}, {self.y}), pelna {self.zloze} ma {self.pojemnosc} miejsc"