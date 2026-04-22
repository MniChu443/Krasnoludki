import Generator
import ObslugaJSON
import KsiazeAlgorytm
import Drukarnia


# Generowanie / wczytanie grafu
graf = Generator.wygeneruj_graf(20, 30)
ObslugaJSON.zapisz_do_pliku(graf, "DaneTestowe/test.json")
graf = ObslugaJSON.wczytaj_plik("DaneTestowe/test.json")



# Podział wierzchołków na domki i kopalnie
domki = [w for w in graf if hasattr(w, 'preferencja')]
kopalnie = [w for w in graf if hasattr(w, 'zloze')]

Drukarnia.wypisz_naglowek("GENEROWANIE GRAFU DOMKÓW I KOPALNI")

# Podsumowanie grafu
print(f"  Liczba domków:   {len(domki)}")
print(f"  Liczba kopalni:  {len(kopalnie)}")
print(f"  Razem wierzchołków: {len(graf)}")

# Wypisanie domków
Drukarnia.wypisz_podnaglowek("DOMKI (preferencje krasnoludów)")
print(f"{'Indeks':<8} {'Pozycja':<12} {'Preferencja':<12} {'Sąsiedzi (indeks, odległość)':<30}")
print(f"{'─' * 8} {'─' * 12} {'─' * 12} {'─' * 30}")
for domek in domki:
    print(f"#{domek.indeks:<7} {Drukarnia.formatuj_wspolrzedne(domek):<12} {domek.preferencja:<12} {Drukarnia.wypisz_sasiadow(domek):<30}")

# Wypisanie kopalni
Drukarnia.wypisz_podnaglowek("KOPALNIE (złoża surowców)")
print(f"{'Indeks':<8} {'Pozycja':<12} {'Złoże':<12} {'Miejsc':<8} {'Sąsiedzi (indeks, odległość)':<30}")
print(f"{'─' * 8} {'─' * 12} {'─' * 12} {'─' * 8} {'─' * 30}")
for kopalnia in kopalnie:
    print(f"#{kopalnia.indeks:<7} {Drukarnia.formatuj_wspolrzedne(kopalnia):<12} {kopalnia.zloze:<12} {kopalnia.pojemnosc:<8} {Drukarnia.wypisz_sasiadow(kopalnia):<30}")

# Trasa księcia
Drukarnia.wypisz_naglowek("TRASA KSIĘCIA")

if kopalnie:
    route = KsiazeAlgorytm.najkrotsza_droga_ksiecia(kopalnie)
    distance = KsiazeAlgorytm.oblicz_dlugosc_trasy(route)

    print(f"  Liczba kopalni na trasie: {len(route)}")
    print(f"\n  Kolejne punkty trasy:")
    for i, kopalnia in enumerate(route, 1):
        marker = " 🏁" if i == len(route) else ""
        print(f"    {i:2}. ({kopalnia.pozycja[0]:3.0f}, {kopalnia.pozycja[1]:3.0f}){marker}")

    print(f"\n  {'─' * 40}")
    print(f"  Całkowita długość trasy: {distance:.2f} jednostek")
    print(f"  {'─' * 40}")
else:
    print("  Brak kopalni - trasa niemożliwa do wyznaczenia.")