from modele import klasy_grafu as KlasyGrafu
import json
from pathlib import Path
from os import listdir
from os.path import isfile, join
import random as rand


def node_na_dict(wierzcholek: KlasyGrafu.Domek | KlasyGrafu.Kopalnia):

    slownik: dict = {
        "indeks": wierzcholek.indeks,
        "x": wierzcholek.pozycja[0],
        "y": wierzcholek.pozycja[1],
        "sasiedzi": []
    }

    for sasiad in wierzcholek.sasiedzi:

        slownik_sasiada = {
            "indeks": sasiad.indeks_sasiada,
            "odleglosc": sasiad.odleglosc
        }

        slownik["sasiedzi"].append(slownik_sasiada)

    if isinstance(wierzcholek, KlasyGrafu.Domek):
        slownik["preferencja"] = wierzcholek.preferencja
        slownik["typ"] = "Domek"
    else:
        slownik["pojemnosc"] = wierzcholek.pojemnosc
        slownik["zloze"] = wierzcholek.zloze
        slownik["typ"] = "Kopalnia"

    return slownik


def dict_do_node(wierzcholek: dict):

    node: KlasyGrafu.Domek | KlasyGrafu.Kopalnia

    if wierzcholek["typ"] == "Domek":
        node = KlasyGrafu.Domek(wierzcholek["indeks"], wierzcholek["x"], wierzcholek["y"], wierzcholek["preferencja"])
    else:
        node = KlasyGrafu.Kopalnia(wierzcholek["indeks"], wierzcholek["x"], wierzcholek["y"], wierzcholek["pojemnosc"], wierzcholek["zloze"])

    for sasiad in wierzcholek["sasiedzi"]:
        node.sasiedzi.append(KlasyGrafu.Sasiad(sasiad["indeks"], sasiad["odleglosc"]))

    return node


def zapisz_do_pliku(miasto: KlasyGrafu.Miasto, sciezka: str):

    # Automatyczne generowanie sąsiedztwa dla wizualizacji, jeśli go brakuje
    posiada_sasiadow = any(len(domek.sasiedzi) > 0 for domek in miasto.domki)
    if not posiada_sasiadow and len(miasto.domki) * len(miasto.kopalnie) <= 10000000:
        from math import dist
        for domek in miasto.domki:
            for kopalnia in miasto.kopalnie:
                odleglosc = dist(domek.pozycja, kopalnia.pozycja)
                domek.dodaj_sasiada(kopalnia.indeks, odleglosc)
                kopalnia.dodaj_sasiada(domek.indeks, odleglosc)

    lista = []
    for budynek in miasto:
        lista.append(node_na_dict(budynek))

    Path(sciezka).parent.mkdir(parents = True, exist_ok = True)
    with open(sciezka, "w") as plik:
        plik.write(json.dumps(lista, ensure_ascii=False, indent=4))


def wczytaj_plik(sciezka: str):

    with open(sciezka, "r") as plik:
        dane_json = json.loads(plik.read())

    miasto = KlasyGrafu.Miasto()
    for slownik in dane_json:
        miasto.dodaj(dict_do_node(slownik))

    return miasto


def node_na_string(wierzcholek: KlasyGrafu.Domek | KlasyGrafu.Kopalnia):

    linijka = f"{str(wierzcholek.indeks)} {str(wierzcholek.pozycja[0])} {str(wierzcholek.pozycja[1])}"

    if isinstance(wierzcholek, KlasyGrafu.Domek): linijka += f" D {wierzcholek.preferencja} ."
    else: linijka += f" K {wierzcholek.zloze} {str(wierzcholek.pojemnosc)}"

    # for sasiad in wierzcholek.sasiedzi:
    #     linijka += " " + str(sasiad.indeks_sasiada) + " " + str(sasiad.odleglosc)

    return linijka + "\n"


def string_na_node(wierzcholek: str):

    wlasciwosci = wierzcholek.split(" ")

    node: KlasyGrafu.Domek | KlasyGrafu.Kopalnia

    if wlasciwosci[3] == "D":
        node = KlasyGrafu.Domek(int(wlasciwosci[0]), int(wlasciwosci[1]), int(wlasciwosci[2]), wlasciwosci[4])
    else:
        node = KlasyGrafu.Kopalnia(int(wlasciwosci[0]), int(wlasciwosci[1]), int(wlasciwosci[2]), int(wlasciwosci[5]), wlasciwosci[4])

    # for i in range(6, len(wlasciwosci), 2):
    #     node.sasiedzi.append(Graf.Sasiad(int(wlasciwosci[i]), float(wlasciwosci[i + 1])))

    return node


def zapisz_do_pliku_raw(miasto: KlasyGrafu.Miasto, sciezka: str):

    with open(sciezka, "w") as plik:
        for wierzcholek in miasto:
            plik.write(node_na_string(wierzcholek))


def wczytaj_plik_raw(sciezka: str):

    with open(sciezka, "r") as plik:
        dane = plik.read()

    miasto = KlasyGrafu.Miasto()
    for linijka in dane.split("\n"):
        if linijka == "" : continue
        miasto.dodaj(string_na_node(linijka))

    return miasto


def wczytaj_plik_testowy(rozmiar: int, proporcja: float, perkolacja: float, sciezka: str):

    pliki = [ plik for plik in listdir(sciezka) if isfile(join(sciezka, plik)) ]
    if len(pliki) == 0: raise f"wczytaj_plik_testowy(): Brak plików w \"{sciezka}\""

    wartosci = [ nazwa.split(".")[0].split("_")[1:] for nazwa in pliki ]
    wartosci = [ [int(w) for w in lista] for lista in wartosci ]

    szukany = [rozmiar, proporcja * 100, perkolacja * 100]
    pasujace = [ pliki[indeks] for indeks in range(len(pliki)) if wartosci[indeks] == szukany ]

    if len(pasujace) == 0:

        print("  wczytaj_plik_testowy(): Brak dokładnego pliku! Wczytuję najbardziej pasujący plik.")

        koszty = []
        for indeks in range(len(wartosci)):
            koszt = abs(wartosci[indeks][0]/rozmiar - 1) * 100
            koszt += abs(wartosci[indeks][1] - szukany[1]) + abs(wartosci[indeks][2] - szukany[2])
            koszty.append(koszt)

        minimum = min(koszty)
        pasujace = [ pliki[indeks] for indeks in range(len(pliki)) if koszty[indeks] == minimum ]

    dane = join(sciezka, rand.choice(pasujace))

    return wczytaj_plik_raw(dane)