from narzedzia import generator as Generator
from narzedzia import obsluga_plikow as ObslugaPlikow
from algorytmy import ksiaze_algorytm as KsiazeAlgorytm
from narzedzia import drukarnia as Drukarnia
from modele import klasy_grafu as KlasyGrafu
from algorytmy.drzewo_przedzialowe import SegmentTree


# wczytanie grafu

print("> Wczytywanie grafu z pliku")
graf = ObslugaPlikow.wczytaj_plik_testowy(1000, 0.75, 1, "../dane/test")
Drukarnia.pokaz_statystyki(graf)
#Drukarnia.pokaz_domki(graf)
#Drukarnia.pokaz_kopalnie(graf)


# Wyznaczanie trasy księcia
# kopalnie = [w for w in graf if type(w) is KlasyGrafu.Kopalnia]
#
# if kopalnie:
#     trasa = KsiazeAlgorytm.najkrotsza_droga_ksiecia(kopalnie)
#     dlugosc = KsiazeAlgorytm.oblicz_dlugosc_trasy(trasa)
#     Drukarnia.pokaz_otoczke(trasa, dlugosc)
# else:
#     print("  Brak kopalni - trasa niemożliwa do wyznaczenia.")
#
# print("\n--- Najgłośniejszy krasnoludek ---")
#
# # RMQ - Drzewo przedziałowe
# glosnosci = [10, 22, 15, 30, 8, 12, 25, 18]
# print(f"Głośności krasnoludków: {glosnosci}")
#
# drzewo = SegmentTree(glosnosci)
# lewy, prawy = 1, 4
# max_glosnosc, indeks = drzewo.query(lewy, prawy)
#
# print(f"Zapytanie o przedział [{lewy}, {prawy}]: Maksymalna głośność = {max_glosnosc} (indeks {indeks}).")