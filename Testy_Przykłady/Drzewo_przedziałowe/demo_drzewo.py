"""
Prosty przykład pokazujący, jak działa Drzewo Przedziałowe (Segment Tree)!

Ten przykład demonstruje podstawowe operacje:
- Budowę drzewa z początkowej tablicy (inicjalizacja struktury).
- Zapytania o maksimum w zadanym przedziale (Range Maximum Query - RMQ).
- Szybką aktualizację pojedynczego elementu (w czasie logarytmicznym).
- Ponowne wykonanie zapytań po zaktualizowaniu wartości.
"""

import sys
from pathlib import Path

# Dodanie katalogu src do ścieżki
sys.path.append(str(Path(__file__).resolve().parent.parent.parent / "src"))

from algorytmy.drzewo_przedzialowe import SegmentTree  # noqa: E402

# Kolory ANSI do wyróżnienia elementów w terminalu
BOLD = "\033[1m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
RED = "\033[91m"
RESET = "\033[0m"

def uruchom_demo():
    print(f"{BOLD}--- DEMO DRZEWA PRZEDZIALOWEGO (Range Maximum Query) ---{RESET}\n")
    
    dane = [1, 3, 5, 7, 9, 11, 2, 4, 6, 8]
    print(f"Dane poczatkowe: {dane}\n")
    
    print(f"{YELLOW}Budowa drzewa przedzialowego...{RESET}")
    drzewo = SegmentTree(dane)
    
    zapytania = [(0, 4), (5, 9), (0, 9), (1, 3)]
    
    print(f"\n{BOLD}1. Zapytania o maksimum w przedziale:{RESET}")
    for L, R in zapytania:
        wartosc, indeks = drzewo.query(L, R)
        wycinek = dane[L:R+1]
        print(f"   Maksimum w przedziale [{L}, {R}] (czyli {wycinek}): {GREEN}{wartosc}{RESET} (pod indeksem {indeks})")
        
    print(f"\n{BOLD}2. Aktualizacja wartosci:{RESET}")
    index_do_zmiany = 2
    nowa_wartosc = 20
    print(f"   Zmieniamy wartosc pod indeksem {index_do_zmiany} z {dane[index_do_zmiany]} na {YELLOW}{nowa_wartosc}{RESET}...")
    drzewo.update(index_do_zmiany, nowa_wartosc)
    dane[index_do_zmiany] = nowa_wartosc
    print(f"   Dane po aktualizacji: {dane}")
    
    print(f"\n{BOLD}3. Zapytania po aktualizacji:{RESET}")
    for L, R in zapytania:
        wartosc, indeks = drzewo.query(L, R)
        wycinek = dane[L:R+1]
        print(f"   Maksimum w przedziale [{L}, {R}] (czyli {wycinek}): {GREEN}{wartosc}{RESET} (pod indeksem {indeks})")

if __name__ == "__main__":
    uruchom_demo()
