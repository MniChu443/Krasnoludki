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
    
    # Wykorzystamy głośności zbliżone do prawdziwych dekametrowców
    dane = [10, 22, 15, 30, 8, 12, 25, 18, 42, 14, 35, 21, 5, 26, 6]
    print(f"Dane poczatkowe (15 elementów): {dane}\n")
    
    print(f"{YELLOW}Budowa drzewa przedzialowego...{RESET}")
    drzewo = SegmentTree(dane)
    
    # Zapytanie o lokalne maksimum
    zapytania_lista = [
        (2, 6),   # Max: 30
        (8, 11),  # Max: 42
        (0, 4),   # Max: 30 (To jest wazne! Tutaj maksimum to tez 30 na indeksie 3)
        (0, 14)   # Max: 42 (Globalne, pokrywa sie z indeksem 8)
    ]
    
    print(f"\n{BOLD}1. Przykładowe zapytania (RMQ) na różnych przedziałach:{RESET}")
    
    historia_zapytan = []
    
    for L, R in zapytania_lista:
        wartosc, indeks = drzewo.query(L, R)
        wycinek = dane[L:R+1]
        print(f"   Maksimum w przedziale [{L:2}, {R:2}] (czyli {wycinek}): {GREEN}{wartosc}{RESET} (pod indeksem {indeks})")
        historia_zapytan.append({
            "L": L,
            "R": R,
            "wartosc": wartosc,
            "indeks": indeks
        })
        
    zapisz_wizualizacje(dane, historia_zapytan)

def zapisz_wizualizacje(dane, historia_zapytan):
    import json
    
    miasto = []
    
    dekametrowcy = []
    trasa_ksiecia = []
    
    start_x = 20
    start_y = 100
    odstep = 15
    
    for i, glosnosc in enumerate(dane):
        x = start_x + i * odstep
        y = start_y
        
        miasto.append({
            "indeks": i,
            "pozycja": [x, y],
            "x": x,
            "y": y,
            "typ": "Kopalnia",
            "pojemnosc": 2,
            "zloze": "ZELAZO",
            "sasiedzi": []
        })
        
        trasa_ksiecia.append(i)
        
        dekametrowcy.append({
            "x": x,
            "y": y,
            "glosnosc": glosnosc,
            "krawedz": i if i < len(dane) - 1 else i - 1
        })
        
    wszystkie_ataki = []
    for zapytanie in historia_zapytan:
        L = zapytanie["L"]
        R = zapytanie["R"]
        sciezka_ataku = []
        if L <= R:
            sciezka_ataku.append({"x": dekametrowcy[L]["x"], "y": dekametrowcy[L]["y"]})
            for i in range(L + 1, R):
                 sciezka_ataku.append({"x": dekametrowcy[i]["x"], "y": dekametrowcy[i]["y"]})
            if L != R:
                 sciezka_ataku.append({"x": dekametrowcy[R]["x"], "y": dekametrowcy[R]["y"]})
                 
        wszystkie_ataki.append({
            "przedzial": [L, R],
            "max_glosnosc": zapytanie["wartosc"],
            "indeks": zapytanie["indeks"],
            "sciezka_ataku": sciezka_ataku
        })

    wyniki = {
        "parowanie": [],
        "trasa_ksiecia": {
            "kolejnosc_kopalni_indeksy": trasa_ksiecia,
            "dlugosc": (len(dane) - 1) * odstep
        },
        "najglosniejszy_krasnoludek": wszystkie_ataki,
        "dekametrowcy": dekametrowcy
    }
    
    katalog_glowny = Path(__file__).resolve().parent.parent.parent
    wizualizacja_dir = katalog_glowny / "wizualizacja"
    
    with open(wizualizacja_dir / "dane.json", "w", encoding="utf-8") as f:
        json.dump(miasto, f, ensure_ascii=False, indent=4)
        
    with open(wizualizacja_dir / "wyniki_algorytmy.json", "w", encoding="utf-8") as f:
        json.dump(wyniki, f, ensure_ascii=False, indent=4)
        
    print(f"\n{CYAN}--- ZAPISANO WIZUALIZACJE ---{RESET}")
    print("Otwórz lub odśwież (Ctrl+F5) 'wizualizacja/index.html' w przeglądarce, aby zobaczyć symulację zapytania o przedział w formie linii dekametrowców!")

if __name__ == "__main__":
    uruchom_demo()
