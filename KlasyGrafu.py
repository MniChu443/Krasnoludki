materialy = ["ZLOTO", "DIAMENTY", "WEGIEL", "REDSTONE", "LAPIS", "ZELAZO"]

class NodeGrafu:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.sasiedzi = []


class Domek(NodeGrafu):

    def __init__(self, x, y, preferencja):
        super().__init__(x, y)
        self.preferencja = preferencja

    def __str__(self):
        return f"Domek w pozycji ({self.x}, {self.y}), krasnal lubi {self.preferencja}"


class Kopalnia(NodeGrafu):

    def __init__(self, x, y, pojemnosc, zloze):
        super().__init__(x, y)
        self.pojemnosc = pojemnosc
        self.zloze = zloze

    def __str__(self):
        return f"Kopalnia w pozycji ({self.x}, {self.y}), pelna {self.zloze} ma {self.pojemnosc} miejsc"