from pathlib import Path
from narzedzia import generator as Generator
from narzedzia import obsluga_plikow as ObslugaJSON


SCIEZKA_DANYCH = "../../dane"

def sciezka_katalogu(katalog: str):
    return f"{SCIEZKA_DANYCH}/{katalog}"


def wygeneruj_i_zapisz_graf(nazwa: str, szerokosc: int, wysokosc: int, proporcja: float, perkolacja: float, sciezka: str = SCIEZKA_DANYCH):

    graf = Generator.wygeneruj_graf(szerokosc, wysokosc, proporcja, perkolacja)
    if len(graf) == 2: return
    ObslugaJSON.zapisz_do_pliku_raw(graf, f"{sciezka}/{nazwa}.txt")


def wygeneruj_dane_testowe(lista_rozmiarow: list[int], lista_proporcji: list[float], lista_perkolacji: list[float], sciezka: str = SCIEZKA_DANYCH):

    print("> Generowanie danych testowych...")
    Path(sciezka).mkdir()

    ilosc = "/" + str(len(lista_rozmiarow) * len(lista_proporcji) * len(lista_perkolacji)) + "]"
    indeks = 1

    for rozmiar in lista_rozmiarow:
        for proporcja in lista_proporcji:
            for perkolacja in lista_perkolacji:

                nazwa = f"test_{str(rozmiar)}_{str(proporcja * 100).split(".")[0]}_{str(perkolacja * 100).split(".")[0]}"
                wygeneruj_i_zapisz_graf(nazwa, rozmiar, rozmiar, proporcja, perkolacja, sciezka)

                print(f"   Wygenerowano i zapisano graf [{str(indeks)}{ilosc}")
                indeks += 1

    print("> Wygenerowano wszystkie grafy!")


def _WYGENERUJ():

    ROZMIARY = [5, 10, 20, 50, 100, 1000]
    PROPORCJE = [0.7, 0.8, 0.9, 1]
    PERKOLACJE = [0.1, 0.3, 0.5, 0.7, 1]

    wygeneruj_dane_testowe(ROZMIARY, PROPORCJE, PERKOLACJE, sciezka_katalogu("test"))