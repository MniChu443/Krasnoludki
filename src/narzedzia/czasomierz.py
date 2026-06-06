from time import time

_czasomierz_start: float = 0
_czasomierz_koniec: float = 0
_czasomierz_dziala: bool = False
_czasomierz_wiadomosc: bool = False

def start(wiadomosc: str = ""):
    global _czasomierz_start, _czasomierz_wiadomosc, _czasomierz_dziala
    if _czasomierz_dziala: raise "Czasomierz działa! Nie można wystartować!"

    _czasomierz_wiadomosc = wiadomosc != ""
    if _czasomierz_wiadomosc: print(f"{wiadomosc}... ", end="")

    _czasomierz_dziala = True
    _czasomierz_start = time()

def stop(wiadomosc: str = ""):
    global _czasomierz_koniec, _czasomierz_wiadomosc, _czasomierz_dziala
    if not _czasomierz_dziala: raise "Czasomierz nie działa! Nie można zatrzymać!"

    _czasomierz_koniec = time()
    _czasomierz_dziala = False

    if wiadomosc != "": print(f"{wiadomosc} [{_czasomierz_koniec - _czasomierz_start}s]")
    elif _czasomierz_wiadomosc: print(f"OK [{_czasomierz_koniec - _czasomierz_start}s]")