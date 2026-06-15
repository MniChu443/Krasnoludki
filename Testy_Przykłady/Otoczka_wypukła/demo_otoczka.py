"""
Prosty przykład pokazujący, jak Algorytm Andrew radzi sobie z wyznaczaniem Trasy Księcia!

Ten przykład zawiera wszystkie przypadki, które sprawiają problemy innym algorytmom:
- Normalne wierzchołki: idealnie wyznaczają zewnętrzne granice królestwa.
- Kopalnie schowane wewnątrz: Główne założenie 
- Kopalnie na jednej prostej (współliniowe): Zamiast zatrzymywać się po drodze, odrzuca środkowe punkty.
- Duplikaty i kolizje: jeśli dwie kopalnie leżą w tym samym miejscu, algorytm po prostu ignoruje nadmiar i jedzie dalej.
"""

import sys
from pathlib import Path

# Dodanie katalogu src do ścieżki
sys.path.append(str(Path(__file__).resolve().parent.parent.parent / "src"))

from algorytmy import otoczka_wypukla as OtoczkaWypukla
from modele.klasy_grafu import Kopalnia

# Kolory ANSI do wyróżnienia elementów w terminalu
BOLD = "\033[1m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
RED = "\033[91m"
RESET = "\033[0m"

def uruchom_demo():
    # Przygotowanie punktów testowych
    kopalnie = [
        Kopalnia(1, 0, 0, 100, "ZLOTO"),
        Kopalnia(2, 5, 0, 100, "DIAMENTY"),
        Kopalnia(3, 5, 5, 100, "WEGIEL"),
        Kopalnia(4, 0, 5, 100, "REDSTONE"),
        Kopalnia(5, 2, 2, 100, "LAPIS"),      # Wewnątrz
        Kopalnia(6, 4, 1, 100, "ZELAZO"),     # Wewnątrz
        Kopalnia(7, 1, 4, 100, "ZELAZO"),     # Wewnątrz
        Kopalnia(8, 2, 0, 100, "DIAMENTY"),   # Współliniowy na krawędzi (między 0,0 a 5,0)
    ]

    print(f"{BOLD}1. Punkty wejsciowe (Kopalnie na mapie):{RESET}")
    for k in kopalnie:
        status = "wewnetrzny" if k.indeks in [5, 6, 7] else ("wspolliniowy" if k.indeks == 8 else "skrajny")
        print(f"   - Kopalnia #{k.indeks}: pozycja ({k.pozycja[0]}, {k.pozycja[1]}), surowiec: {k.zloze:8} ({status})")
    otoczka = OtoczkaWypukla.najkrotsza_droga_ksiecia(kopalnie)
    obwod = OtoczkaWypukla.oblicz_dlugosc_trasy(otoczka)

    print(f"\n{BOLD}2. Kolejnosc punktow na Trasie Ksiecia:{RESET}")
    for i, k in enumerate(otoczka, 1):
        print(f"   Krok {i}: Kopalnia #{k.indeks} na pozycji ({k.pozycja[0]}, {k.pozycja[1]}) -> zloze: {k.zloze}")

    otoczka_indeksy = {k.indeks for k in otoczka}
    odrzucone_wewnetrzne = [k.indeks for k in kopalnie if k.indeks not in otoczka_indeksy and k.indeks in [5, 6, 7]]
    odrzucone_wspolliniowe = [k.indeks for k in kopalnie if k.indeks not in otoczka_indeksy and k.indeks == 8]

    wew_str = ", ".join(f"#{idx}" for idx in odrzucone_wewnetrzne)
    wsp_str = ", ".join(f"#{idx}" for idx in odrzucone_wspolliniowe)

    print(f"\n{BOLD}3. Podsumowanie trasy:{RESET}")
    print(f"   - Liczba kopalni w otoczce: {GREEN}{len(otoczka)}{RESET} z 8 wejsciowych")
    print(f"   - Calkowita dlugosc trasy (obwod): {GREEN}{obwod:.2f} jednostek{RESET}")
    print(f"   - Odrzucone kopalnie wewnetrzne (bezpiecznie schowane): {RED}{wew_str}{RESET}")
    print(f"   - Odrzucone punkty wspolliniowe (optymalizacja odcinkow prostych): {RED}{wsp_str}{RESET}")


if __name__ == "__main__":
    uruchom_demo()
