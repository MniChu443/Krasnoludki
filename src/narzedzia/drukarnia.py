from modele import klasy_grafu as KlasyGrafu

def wypisz_naglowek(tekst):
    """Wypisuje sformatowany nagłówek sekcji."""
    szerokosc = len(tekst) + 8
    print("\n" + "=" * szerokosc)
    print(f"   {tekst}")
    print("=" * szerokosc + "\n")


def wypisz_podnaglowek(tekst):
    """Wypisuje podnagłówek sekcji."""
    print(f"\n{'─' * 60}")
    print(f"  {tekst}")
    print(f"{'─' * 60}")


def formatuj_wspolrzedne(wierzcholek):
    """Formatuje współrzędne do postaci (xxx, yyy)."""
    return f"({wierzcholek.pozycja[0]:3.0f}, {wierzcholek.pozycja[1]:3.0f})"


def wypisz_sasiadow(wierzcholek):
    """Formatuje listę sąsiadów z odległościami."""
    if not wierzcholek.sasiedzi:
        return "brak"

    sasiady = []
    for s in wierzcholek.sasiedzi:
        sasiady.append(f"#{s.indeks_sasiada} ({s.odleglosc:.2f})")
    return ", ".join(sasiady)


def pokaz_statystyki(miasto: KlasyGrafu.Miasto):
    wypisz_naglowek("PODSUMOWANIE GRAFU DOMKÓW I KOPALNI")

    print(f"  Liczba domków:   {len(miasto.domki)}")
    print(f"  Liczba kopalni:  {len(miasto.kopalnie)}")
    print(f"  Razem wierzchołków: {len(miasto)}\n")


def pokaz_domki(miasto: KlasyGrafu.Miasto):
    wypisz_podnaglowek("DOMKI (preferencje krasnoludów)")

    print(f"{'Indeks':<8} {'Pozycja':<12} {'Preferencja':<12} {'Sąsiedzi (indeks, odległość)':<30}")
    print(f"{'─' * 8} {'─' * 12} {'─' * 12} {'─' * 30}")
    for domek in miasto.domki:
        print(f"#{domek.indeks:<7} {formatuj_wspolrzedne(domek):<12} {domek.preferencja:<12} {wypisz_sasiadow(domek):<30}")


def pokaz_kopalnie(miasto: KlasyGrafu.Miasto):
    wypisz_podnaglowek("KOPALNIE (złoża surowców)")

    print(f"{'Indeks':<8} {'Pozycja':<12} {'Złoże':<12} {'Miejsc':<8} {'Sąsiedzi (indeks, odległość)':<30}")
    print(f"{'─' * 8} {'─' * 12} {'─' * 12} {'─' * 8} {'─' * 30}")

    for kopalnia in miasto.kopalnie:
        print(f"#{kopalnia.indeks:<7} {formatuj_wspolrzedne(kopalnia):<12} {kopalnia.zloze:<12} {kopalnia.pojemnosc:<8} {wypisz_sasiadow(kopalnia):<30}")


def pokaz_otoczke(trasa: list[KlasyGrafu.Kopalnia], dlugosc: float):
    wypisz_naglowek("TRASA KSIĘCIA")

    print(f"  Liczba kopalni na trasie: {len(trasa)}")
    print(f"\n  Kolejne punkty trasy:")

    for i, kopalnia in enumerate(trasa, 1):
        marker = " 🏁" if i == len(trasa) else ""
        print(f"    {i:2}. ({kopalnia.pozycja[0]:3.0f}, {kopalnia.pozycja[1]:3.0f}){marker}")

    print(f"\n  {'─' * 40}")
    print(f"  Całkowita długość trasy: {dlugosc:.2f} jednostek")
    print(f"  {'─' * 40}\n")