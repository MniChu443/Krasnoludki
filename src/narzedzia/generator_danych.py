import sys
from pathlib import Path

#Dodanie katalogu głównego projektu do pythona aby dynamicznie szukać ścieżek
sys.path.append(str(Path(__file__).resolve().parent.parent))

from narzedzia import generator as Generator
from narzedzia import obsluga_plikow as ObslugaJSON

#Ustalenie ścieżki do katalogu z danymi
SCIEZKA_DANYCH = str(Path(__file__).resolve().parent.parent.parent / "dane")

def sciezka_katalogu(katalog: str):
    return f"{SCIEZKA_DANYCH}/{katalog}"


def wygeneruj_i_zapisz_miasto(nazwa: str, szerokosc: int, wysokosc: int, proporcja: float, perkolacja: float, sciezka: str = SCIEZKA_DANYCH, materialy: list[str] = None):

    chcemy_sasiadow = False #(szerokosc * wysokosc <= 2500)
    miasto = Generator.wygeneruj_miasto(szerokosc, wysokosc, proporcja, perkolacja, materialy, chcemy_sasiadow)
    if len(miasto) == 2: return
    ObslugaJSON.zapisz_do_pliku_raw(miasto, f"{sciezka}/{nazwa}.txt")
    #ObslugaJSON.zapisz_do_pliku(miasto, f"{sciezka}/{nazwa}.json")


def wygeneruj_dane_testowe(lista_rozmiarow: list[int], lista_proporcji: list[float], lista_perkolacji: list[float], sciezka: str = SCIEZKA_DANYCH):

    print("> Generowanie danych testowych...")
    Path(sciezka).mkdir(parents=True, exist_ok=True)

    ilosc = "/" + str(len(lista_rozmiarow) * len(lista_proporcji) * len(lista_perkolacji)) + "]"
    indeks = 1

    for rozmiar in lista_rozmiarow:
        for proporcja in lista_proporcji:
            for perkolacja in lista_perkolacji:

                nazwa = f"test_{str(rozmiar)}_{str(proporcja * 100).split('.')[0]}_{str(perkolacja * 100).split('.')[0]}"
                wygeneruj_i_zapisz_miasto(nazwa, rozmiar, rozmiar, proporcja, perkolacja, sciezka)

                print(f"   Wygenerowano i zapisano graf [{str(indeks)}{ilosc}")
                indeks += 1

    print("> Wygenerowano wszystkie grafy!")


def _WYGENERUJ():

    ROZMIARY = [8]
    PROPORCJE = [0.7]
    PERKOLACJE = [1]

    wygeneruj_dane_testowe(ROZMIARY, PROPORCJE, PERKOLACJE)


if __name__ == "__main__":
    _WYGENERUJ()