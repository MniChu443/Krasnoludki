from przeplyw import SiecPrzeplywowa
from modele import klasy_grafu as KlasyGrafu
from narzedzia import czasomierz as Czasomierz

Czas = Czasomierz.Czasomierz()

def znajdz_najblizsza_kopalnie(miasto: KlasyGrafu.Miasto):
    Czas.start("  Obliczanie optymalnego przypisania (Ford-Fulkerson)")
    
    siec = SiecPrzeplywowa(miasto)
    pary = siec.PAROWANIE()
    
    wynik = {}
    kopalnie_map = {k.indeks: k for k in miasto.kopalnie}
    
    for d_idx, k_idx in pary:
        domek = next(d for d in miasto.domki if d.indeks == d_idx)
        kopalnia = kopalnie_map[k_idx]
        wynik[d_idx] = {
            "kopalnia": k_idx,
            "dystans": domek.odleglosc(kopalnia)
        }
    
    Czas.stop("Zakończono obliczenia parowania")
            
    return wynik