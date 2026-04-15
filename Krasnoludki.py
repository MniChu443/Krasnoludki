import Generator
import ObslugaJSON
import KsiazeAlgorytm


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


def formatuj_wspolrzedne(x, y):
    """Formatuje współrzędne do postaci (xxx, yyy)."""
    return f"({x:3.0f}, {y:3.0f})"


def wypisz_sasiadow(wierzcholek):
    """Formatuje listę sąsiadów z odległościami."""
    if not wierzcholek.sasiedzi:
        return "brak"

    sasiady = []
    for s in wierzcholek.sasiedzi:
        sasiady.append(f"#{s.indeks_sasiada} ({s.odleglosc:.2f})")
    return ", ".join(sasiady)


graf = Generator.wygeneruj_graf()
ObslugaJSON.zapisz_do_pliku(graf, "DaneTestowe/test.json")
graf = ObslugaJSON.wczytaj_plik("DaneTestowe/test.json")

# Podział wierzchołków na domki i kopalnie
domki = [w for w in graf if hasattr(w, 'preferencja')]
kopalnie = [w for w in graf if hasattr(w, 'zloze')]

wypisz_naglowek("GENEROWANIE GRAFU DOMKÓW I KOPALNI")

# Podsumowanie grafu
print(f"  Liczba domków:   {len(domki)}")
print(f"  Liczba kopalni:  {len(kopalnie)}")
print(f"  Razem wierzchołków: {len(graf)}")

# Wypisanie domków
wypisz_podnaglowek("DOMKI (preferencje krasnoludów)")
print(f"{'Indeks':<8} {'Pozycja':<12} {'Preferencja':<12} {'Sąsiedzi (indeks, odległość)':<30}")
print(f"{'─' * 8} {'─' * 12} {'─' * 12} {'─' * 30}")
for domek in domki:
    print(f"#{domek.indeks:<7} {formatuj_wspolrzedne(domek.x, domek.y):<12} {domek.preferencja:<12} {wypisz_sasiadow(domek):<30}")

# Wypisanie kopalni
wypisz_podnaglowek("KOPALNIE (złoża surowców)")
print(f"{'Indeks':<8} {'Pozycja':<12} {'Złoże':<12} {'Miejsc':<8} {'Sąsiedzi (indeks, odległość)':<30}")
print(f"{'─' * 8} {'─' * 12} {'─' * 12} {'─' * 8} {'─' * 30}")
for kopalnia in kopalnie:
    print(f"#{kopalnia.indeks:<7} {formatuj_wspolrzedne(kopalnia.x, kopalnia.y):<12} {kopalnia.zloze:<12} {kopalnia.pojemnosc:<8} {wypisz_sasiadow(kopalnia):<30}")

# Trasa księcia
wypisz_naglowek("TRASA KSIĘCIA")

if kopalnie:
    kopalnie_pozycje = [(w.x, w.y) for w in kopalnie]
    route = KsiazeAlgorytm.NajkrotszaDrogaKsiecia(kopalnie_pozycje)
    distance = KsiazeAlgorytm.ObliczDlugoscTrasy(route)

    print(f"  Liczba kopalni na trasie: {len(route)}")
    print(f"\n  Kolejne punkty trasy:")
    for i, (x, y) in enumerate(route, 1):
        marker = " 🏁" if i == len(route) else ""
        print(f"    {i:2}. ({x:3.0f}, {y:3.0f}){marker}")

    print(f"\n  {'─' * 40}")
    print(f"  Całkowita długość trasy: {distance:.2f} jednostek")
    print(f"  {'─' * 40}")
else:
    print("  Brak kopalni - trasa niemożliwa do wyznaczenia.")