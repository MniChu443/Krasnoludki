from narzedzia import generator as Generator
from narzedzia import obsluga_json as ObslugaJSON
from algorytmy import ksiaze_algorytm as KsiazeAlgorytm
from narzedzia import drukarnia as Drukarnia
from modele import klasy_grafu as KlasyGrafu


# Generowanie / wczytanie grafu
graf = Generator.wygeneruj_graf(5, 5)
ObslugaJSON.zapisz_do_pliku(graf, "../data/wyjscie/test.json")
graf = ObslugaJSON.wczytaj_plik("../data/wyjscie/test.json")
Drukarnia.pokaz_statystyki(graf)
Drukarnia.pokaz_domki(graf)
Drukarnia.pokaz_kopalnie(graf)

# Trasa księcia
kopalnie = [w for w in graf if type(w) is KlasyGrafu.Kopalnia]

if kopalnie:
    trasa = KsiazeAlgorytm.najkrotsza_droga_ksiecia(kopalnie)
    dlugosc = KsiazeAlgorytm.oblicz_dlugosc_trasy(trasa)
    Drukarnia.pokaz_otoczke(trasa, dlugosc)
else:
    print("  Brak kopalni - trasa niemożliwa do wyznaczenia.")