import sys
import time
import random
from pathlib import Path

from algorytmy import otoczka_wypukla as OtoczkaWypukla
from modele.klasy_grafu import Kopalnia

# Dodanie katalogu src do ścieżki
sys.path.append(str(Path(__file__).resolve().parent.parent.parent / "src"))



# Kolory ANSI do wyróżnienia elementów w terminalu
BOLD = "\033[1m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
RED = "\033[91m"
RESET = "\033[0m"


def naiwna_otoczka_wypukla(punkty):
    """Naiwne wyznaczanie otoczki wypukłej o złożoności O(N^3).
    Dla każdej pary punktów sprawdza, czy wszystkie inne leżą po tej samej stronie prostej.
    """
    n = len(punkty)
    if n <= 2:
        return punkty

    otoczka = set()
    for i in range(n):
        for j in range(n):
            if i == j:
                continue

            p_i = punkty[i].pozycja
            p_j = punkty[j].pozycja

            wszystkie_po_jednej_stronie = True
            pierwszy_znak = None

            for k in range(n):
                if k == i or k == j:
                    continue
                p_k = punkty[k].pozycja

                # Iloczyn wektorowy (cross product) określający położenie punktu k względem linii i -> j
                iloczyn = (p_j[0] - p_i[0]) * (p_k[1] - p_i[1]) - (p_j[1] - p_i[1]) * (p_k[0] - p_i[0])

                if abs(iloczyn) < 1e-9:
                    continue  # Pomijamy współliniowe

                znak = 1 if iloczyn > 0 else -1
                if pierwszy_znak is None:
                    pierwszy_znak = znak
                elif znak != pierwszy_znak:
                    wszystkie_po_jednej_stronie = False
                    break

            if wszystkie_po_jednej_stronie:
                otoczka.add(punkty[i])
                otoczka.add(punkty[j])

    return list(otoczka)


def generuj_losowe_kopalnie(N):
    kopalnie = []
    for i in range(N):
        x = random.uniform(0, 1000)
        y = random.uniform(0, 1000)
        kopalnie.append(Kopalnia(i, x, y, 100, "ZLOTO"))
    return kopalnie


def uruchom_benchmark():
    print(f"\n{BOLD}{YELLOW}------------------------------------------------------------{RESET}")
    print(f"{BOLD}{YELLOW}          TEST CZASOWY: ALGORYTM ANDREW VS NAIWNY O(N^3)    {RESET}")
    print(f"{BOLD}{YELLOW}------------------------------------------------------------{RESET}\n")

    #Dla 1000 Podejscie Naiwne = około 40 sekund 
    testy_rozmiary = [50, 100, 200, 400,]
    
    print(f"{BOLD}{'Liczba kopalni (N)':<20} | {'Algorytm Andrew O(N log N)':<35} | {'Podejscie naiwne O(N^3)':<32} | {'Przyspieszenie':<15}{RESET}")
    print("-" * 110)

    for N in testy_rozmiary:
        punkty = generuj_losowe_kopalnie(N)

        # 1. Test algorytmu Andrew
        t_start = time.perf_counter()
        OtoczkaWypukla.najkrotsza_droga_ksiecia(punkty)
        t_andrew = time.perf_counter() - t_start

        # 2. Test podejścia naiwnego
        t_start = time.perf_counter()
        naiwna_otoczka_wypukla(punkty)
        t_naiwny = time.perf_counter() - t_start

        przyspieszenie = t_naiwny / t_andrew if t_andrew > 0 else 0

        # Formatowanie czasów do wyświetlenia
        str_andrew = f"{t_andrew * 1000:.3f} ms ({t_andrew:.3f} s)"
        str_naiwny = f"{t_naiwny * 1000:.3f} ms ({t_naiwny:.3f} s)"
        str_przyspieszenie = f"{przyspieszenie:.1f}x"

        print(f"{N:<20} | {GREEN}{str_andrew:<35}{RESET} | {RED}{str_naiwny:<32}{RESET} | {CYAN}{str_przyspieszenie:<15}{RESET}")
    print(f"\n{BOLD}{YELLOW}---------------------------------------------------{RESET}\n")


if __name__ == "__main__":
    uruchom_benchmark()
