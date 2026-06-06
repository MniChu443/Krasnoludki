from time import time

class Czasomierz:

    def __init__(self):
        self.czasomierz_start: float = 0
        self.czasomierz_koniec: float = 0
        self.czasomierz_dziala: bool = False
        self.czasomierz_wiadomosc: bool = False

    def start(self, wiadomosc: str = ""):
        if self.czasomierz_dziala: raise "Czasomierz działa! Nie można wystartować!"

        self.czasomierz_wiadomosc = wiadomosc != ""
        if self.czasomierz_wiadomosc: print(f"{wiadomosc}... ", end="")

        self.czasomierz_dziala = True
        self.czasomierz_start = time()

    def stop(self, wiadomosc: str = ""):
        if not self.czasomierz_dziala: raise "Czasomierz nie działa! Nie można zatrzymać!"

        self.czasomierz_koniec = time()
        self.czasomierz_dziala = False

        if wiadomosc != "": print(f"{wiadomosc} [{self.czasomierz_koniec - self.czasomierz_start}s]")
        elif self.czasomierz_wiadomosc: print(f"OK [{self.czasomierz_koniec - self.czasomierz_start}s]")