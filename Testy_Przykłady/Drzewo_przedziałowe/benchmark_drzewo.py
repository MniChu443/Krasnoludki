"""
Porównuje czas działania Drzewa Przedziałowego
(zapytania w czasie O(log N)) z naiwnym przeszukiwaniem tablicy 
(zapytania w czasie O(N)). Pokazuje, że dla dużej liczby zapytań
Drzewo Przedziałowe drastycznie przyspiesza działanie algorytmu.
"""

import sys
import time
import random
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

def naiwne_zapytanie(data, left, right):
    """Naiwne wyznaczanie maksimum w czasie O(N)."""
    maks = data[left]
    idx = left
    for i in range(left + 1, right + 1):
        if data[i] > maks:
            maks = data[i]
            idx = i
    return maks, idx

def uruchom_benchmark():
    print(f"\n{BOLD}{YELLOW}------------------------------------------------------------{RESET}")
    print(f"{BOLD}{YELLOW}      TEST CZASOWY: DRZEWO PRZEDZIAŁOWE O(log N) VS NAIWNE O(N)      {RESET}")
    print(f"{BOLD}{YELLOW}------------------------------------------------------------{RESET}\n")

    testy_rozmiary = [1000, 5000, 10000, 50000]
    liczba_zapytan = 1000  # Stala liczba zapytań dla każdego testu
    
    print(f"{BOLD}{'Rozmiar tablicy (N)':<20} | {'Drzewo Przedzialowe O(Q log N)':<35} | {'Podejscie naiwne O(Q * N)':<32} | {'Przyspieszenie':<15}{RESET}")
    print("-" * 110)

    for N in testy_rozmiary:
        dane = [random.randint(0, 1000000) for _ in range(N)]
        
        # Generujemy te same zapytania dla obu algorytmów
        zapytania_lista = [(random.randint(0, N//2), random.randint(N//2, N-1)) for _ in range(liczba_zapytan)]

        # 1. Test Drzewa Przedziałowego (budowa + zapytania)
        t_start = time.perf_counter()
        drzewo = SegmentTree(dane)
        for L, R in zapytania_lista:
            drzewo.query(L, R)
        t_drzewo = time.perf_counter() - t_start

        # 2. Test podejścia naiwnego
        t_start = time.perf_counter()
        dane_naiwne = list(dane)
        for L, R in zapytania_lista:
            naiwne_zapytanie(dane_naiwne, L, R)
        t_naiwny = time.perf_counter() - t_start

        przyspieszenie = t_naiwny / t_drzewo if t_drzewo > 0 else 0

        # Formatowanie czasów do wyświetlenia
        str_drzewo = f"{t_drzewo * 1000:.3f} ms"
        str_naiwny = f"{t_naiwny * 1000:.3f} ms ({t_naiwny:.3f} s)"
        str_przyspieszenie = f"{przyspieszenie:.1f}x"

        print(f"{N:<20} | {GREEN}{str_drzewo:<35}{RESET} | {RED}{str_naiwny:<32}{RESET} | {CYAN}{str_przyspieszenie:<15}{RESET}")
    print(f"\n{BOLD}{YELLOW}------------------------------------------------------------{RESET}\n")

if __name__ == "__main__":
    uruchom_benchmark()
