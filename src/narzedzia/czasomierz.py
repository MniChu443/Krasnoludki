from time import time

class Czasomierz:
    """Klasa mierząca czas działania algorytmów"""

    def __init__(self):
        self.czasomierz_start: float = 0
        self.czasomierz_koniec: float = 0
        self.czasomierz_dziala: bool = False
        self.czasomierz_wiadomosc: bool = False
        self.pomin = False

    def start(self, wiadomosc: str = ""):
        if self.pomin: return
        if self.czasomierz_dziala: raise "Czasomierz działa! Nie można wystartować!"

        self.czasomierz_wiadomosc = wiadomosc != ""
        if self.czasomierz_wiadomosc: print(f"{wiadomosc}... ", end="")

        self.czasomierz_dziala = True
        self.czasomierz_start = time()

    def stop(self, wiadomosc: str = ""):
        if self.pomin: return 0
        if not self.czasomierz_dziala: raise "Czasomierz nie działa! Nie można zatrzymać!"

        self.czasomierz_koniec = time()
        self.czasomierz_dziala = False
        czas = self.czasomierz_koniec - self.czasomierz_start

        if wiadomosc != "": print(f"{wiadomosc} [{czas}s]")
        elif self.czasomierz_wiadomosc: print(f"OK [{czas}s]")

        return czas