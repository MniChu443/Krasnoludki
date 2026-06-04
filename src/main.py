from narzedzia import obsluga_plikow as ObslugaPlikow
from narzedzia import drukarnia as Drukarnia
from algorytmy import ksiaze_algorytm as KsiazeAlgorytm
from algorytmy import najglosniejszy_krasnolud as Krasnolud
from algorytmy import przeplyw as Przeplyw


# Przygotowanie grafu
print("> Wczytywanie grafu z pliku")
graf = ObslugaPlikow.wczytaj_plik_testowy(5, 0.75, 1, "../dane/test")
Drukarnia.pokaz_statystyki(graf)
Drukarnia.pokaz_domki(graf)
Drukarnia.pokaz_kopalnie(graf)

print("\n\n\n\n\n")

dwudzielny = Przeplyw.GrafDwudzielny(graf)
print(dwudzielny)


# # Trasa Księcia
# print("> Wyznaczanie trasy Ksiecia")
# KsiazeAlgorytm.wyznacz_trase_ksiecia(graf)
#
#
# # Najgłośniejszy krasnoludek
# print("> Znajdowanie najglosniejszego krasnoludka")
# glosnosci = [10, 22, 15, 30, 8, 12, 25, 18]
# lewy, prawy = 1, 4
# print(f"  Głośności krasnoludków: {glosnosci}")
# max_glosnosc, indeks = Krasnolud.najglosniejszy(lewy, prawy, glosnosci)
# print(f"  Zapytanie o przedział [{lewy}, {prawy}]: Maksymalna głośność = {max_glosnosc} (indeks {indeks}).")

