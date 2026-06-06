from narzedzia import obsluga_plikow as ObslugaPlikow
from narzedzia import drukarnia as Drukarnia
from narzedzia import czasomierz as Czasomierz
from algorytmy import ksiaze_algorytm as KsiazeAlgorytm
from algorytmy import najglosniejszy_krasnolud as Krasnolud
from algorytmy import przeplyw as Przeplyw

MainCzas = Czasomierz.Czasomierz()

# Przygotowanie grafu

MainCzas.start("> Wczytywanie miasta z pliku")
miasto = ObslugaPlikow.wczytaj_plik_testowy(50, 0.7, 1, "../dane/test")
#miasto = ObslugaPlikow.wczytaj_plik_raw("../dane/test_0_0_0.txt")
MainCzas.stop()

Drukarnia.pokaz_statystyki(miasto)
# Drukarnia.pokaz_domki(miasto)
# Drukarnia.pokaz_kopalnie(miasto)

print("> Tworzenie grafu dla przepływu")

MainCzas.start()
graf = Przeplyw.SiecPrzeplywowa(miasto)
MainCzas.stop("### SIEC PRZEPLYWOWA WYGENREOWANA")

MainCzas.start()
print(graf.PAROWANIE())
MainCzas.stop("### PAROWANIE ZNALEZIONE")

def reszta():
    # Trasa Księcia
    print("> Wyznaczanie trasy Ksiecia")
    KsiazeAlgorytm.wyznacz_trase_ksiecia(miasto)


    # Najgłośniejszy krasnoludek
    print("> Znajdowanie najglosniejszego krasnoludka")
    glosnosci = [10, 22, 15, 30, 8, 12, 25, 18]
    lewy, prawy = 1, 4
    print(f"  Głośności krasnoludków: {glosnosci}")
    max_glosnosc, indeks = Krasnolud.najglosniejszy(lewy, prawy, glosnosci)
    print(f"  Zapytanie o przedział [{lewy}, {prawy}]: Maksymalna głośność = {max_glosnosc} (indeks {indeks}).")

