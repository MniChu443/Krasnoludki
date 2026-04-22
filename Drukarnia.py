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