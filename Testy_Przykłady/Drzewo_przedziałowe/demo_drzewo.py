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
    L, R = 2, 6
    wartosc, indeks = drzewo.query(L, R)
    wycinek = dane[L:R+1]
    print(f"\n{BOLD}1. Zapytanie o lokalne maksimum w przedziale [{L}, {R}]:{RESET}")
    print(f"   Wycinek tablicy: {wycinek}")
    print(f"   Znalezione maksimum: {GREEN}{wartosc}{RESET} (pod indeksem {indeks})")
        
    print(f"\n{BOLD}2. Aktualizacja wewnątrz przedziału:{RESET}")
    index_wewnatrz = 4
    nowa_wartosc_wewnatrz = 50
    print(f"   Zmieniamy wartosc pod indeksem {index_wewnatrz} z {dane[index_wewnatrz]} na {YELLOW}{nowa_wartosc_wewnatrz}{RESET}...")
    drzewo.update(index_wewnatrz, nowa_wartosc_wewnatrz)
    dane[index_wewnatrz] = nowa_wartosc_wewnatrz
    
    wartosc, indeks = drzewo.query(L, R)
    wycinek = dane[L:R+1]
    print(f"   Ponawiamy zapytanie dla [{L}, {R}]. Wycinek: {wycinek}")
    print(f"   Nowe maksimum przedziału: {GREEN}{wartosc}{RESET} (pod indeksem {indeks})")
    print(f"   {CYAN}(Algorytm prawidłowo wyłapał nową największą wartość wewnątrz przedziału){RESET}")

    print(f"\n{BOLD}3. Aktualizacja na zewnątrz przedziału:{RESET}")
    index_zewnatrz = 10
    nowa_wartosc_zewnatrz = 100
    print(f"   Zmieniamy wartosc pod indeksem {index_zewnatrz} z {dane[index_zewnatrz]} na {YELLOW}{nowa_wartosc_zewnatrz}{RESET} (To teraz globalne maksimum!)...")
    drzewo.update(index_zewnatrz, nowa_wartosc_zewnatrz)
    dane[index_zewnatrz] = nowa_wartosc_zewnatrz
    
    wartosc, indeks = drzewo.query(L, R)
    wycinek = dane[L:R+1]
    print(f"   Ponawiamy zapytanie dla [{L}, {R}]. Wycinek: {wycinek}")
    print(f"   Maksimum przedziału to nadal: {GREEN}{wartosc}{RESET} (pod indeksem {indeks})")
    print(f"   {CYAN}(Algorytm jest odporny na ogromne wartości poza badanym przedziałem i szuka tylko lokalnie!){RESET}")
        
    zapisz_wizualizacje(dane, L, R, wartosc, indeks)

def zapisz_wizualizacje(dane, ostatnie_L, ostatnie_R, ostatni_wartosc, ostatni_indeks):
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
        
    sciezka_ataku = []
    if ostatnie_L <= ostatnie_R:
        sciezka_ataku.append({"x": dekametrowcy[ostatnie_L]["x"], "y": dekametrowcy[ostatnie_L]["y"]})
        for i in range(ostatnie_L + 1, ostatnie_R):
             sciezka_ataku.append({"x": dekametrowcy[i]["x"], "y": dekametrowcy[i]["y"]})
        if ostatnie_L != ostatnie_R:
             sciezka_ataku.append({"x": dekametrowcy[ostatnie_R]["x"], "y": dekametrowcy[ostatnie_R]["y"]})

    wyniki = {
        "parowanie": [],
        "trasa_ksiecia": {
            "kolejnosc_kopalni_indeksy": trasa_ksiecia,
            "dlugosc": (len(dane) - 1) * odstep
        },
        "najglosniejszy_krasnoludek": {
            "przedzial": [ostatnie_L, ostatnie_R],
            "max_glosnosc": ostatni_wartosc,
            "indeks": ostatni_indeks,
            "sciezka_ataku": sciezka_ataku
        },
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
