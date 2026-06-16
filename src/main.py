from narzedzia import obsluga_plikow as ObslugaPlikow
from narzedzia import drukarnia as Drukarnia
from narzedzia import czasomierz as Czasomierz
from algorytmy import otoczka_wypukla as OtoczkaWypukla
from algorytmy import najglosniejszy_krasnolud as Krasnolud
from algorytmy import przeplyw as Przeplyw

import json

MainCzas = Czasomierz.Czasomierz()

# Przygotowanie grafu

MainCzas.start("> Wczytywanie miasta z pliku")
#miasto = ObslugaPlikow.wczytaj_plik_testowy(3, 0.7, 1, "../dane")
miasto = ObslugaPlikow.wczytaj_plik_raw("dane/test_8_70_100.txt")
MainCzas.stop()

# Zapisanie miasta do pliku JSON dla wizualizacji
ObslugaPlikow.zapisz_do_pliku(miasto, "wizualizacja/dane.json")

Drukarnia.pokaz_statystyki(miasto)
# Drukarnia.pokaz_domki(miasto)
# Drukarnia.pokaz_kopalnie(miasto)

print("> Tworzenie grafu dla przepływu")

MainCzas.start()
graf = Przeplyw.SiecPrzeplywowa(miasto)
MainCzas.stop("### SIEC PRZEPLYWOWA WYGENREOWANA")

MainCzas.start()
pary = graf.PAROWANIE()
MainCzas.stop("### PAROWANIE ZNALEZIONE")
print(pary)

# Trasa Księcia
print("> Wyznaczanie trasy Ksiecia")
trasa = OtoczkaWypukla.najkrotsza_droga_ksiecia(miasto.kopalnie) if miasto.kopalnie else []
dlugosc = OtoczkaWypukla.oblicz_dlugosc_trasy(trasa) if trasa else 0.0
if trasa:
    Drukarnia.pokaz_otoczke(trasa, dlugosc)
else:
    print("  Brak kopalni - trasa niemożliwa do wyznaczenia.")

# Najgłośniejszy krasnoludek (Dekametrowcy na otoczce)
print("> Rozstawianie dekametrowców na otoczce")
dekametrowcy = OtoczkaWypukla.rozstaw_na_trasie(trasa, odstep=15.0)

glosnosci = [d["glosnosc"] for d in dekametrowcy]
if glosnosci:
    lewy = 0
    prawy = len(glosnosci) // 3 if len(glosnosci) > 3 else len(glosnosci) - 1
    print(f"  Rozstawiono {len(glosnosci)} dekametrowców.")
    print(f"  Głośności: {glosnosci}")
    max_glosnosc, indeks = Krasnolud.najglosniejszy(lewy, prawy, glosnosci)
    print(f"  Zapytanie o przedział [{lewy}, {prawy}]: Maksymalna głośność = {max_glosnosc} (indeks {indeks}).")
else:
    lewy, prawy, max_glosnosc, indeks = 0, 0, 0, 0
    print("  Brak dekametrowców (za krótka trasa).")

# Zapisanie wyników algorytmów do osobnego pliku JSON
wyniki = {
    "parowanie": [{"domek_indeks": p[0], "kopalnia_indeks": p[1]} for p in pary],
    "trasa_ksiecia": {
        "kolejnosc_kopalni_indeksy": [k.indeks for k in trasa],
        "dlugosc": dlugosc
    },
    "najglosniejszy_krasnoludek": {
        "przedzial": [lewy, prawy],
        "max_glosnosc": max_glosnosc,
        "indeks": indeks
    },
    "dekametrowcy": dekametrowcy
}

with open("wizualizacja/wyniki_algorytmy.json", "w", encoding="utf-8") as f:
    json.dump(wyniki, f, ensure_ascii=False, indent=4)
print("\n> Zapisano wyniki algorytmów do pliku wizualizacja/wyniki_algorytmy.json")

