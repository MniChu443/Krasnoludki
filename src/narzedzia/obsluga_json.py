from modele import klasy_grafu as Graf
from typing import List
import json
from pathlib import Path


def node_na_dict(wierzcholek: Graf.Domek | Graf.Kopalnia):

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

    if type(wierzcholek) is Graf.Domek:
        slownik["preferencja"] = wierzcholek.preferencja
        slownik["typ"] = "Domek"
    elif type(wierzcholek) is Graf.Kopalnia:
        slownik["pojemnosc"] = wierzcholek.pojemnosc
        slownik["zloze"] = wierzcholek.zloze
        slownik["typ"] = "Kopalnia"

    return slownik


def dict_do_node(wierzcholek: dict):

    node: Graf.Domek | Graf.Kopalnia

    if wierzcholek["typ"] == "Domek":
        node = Graf.Domek(wierzcholek["indeks"], wierzcholek["x"], wierzcholek["y"], wierzcholek["preferencja"])
    elif wierzcholek["typ"] == "Kopalnia":
        node = Graf.Kopalnia(wierzcholek["indeks"], wierzcholek["x"], wierzcholek["y"], wierzcholek["pojemnosc"], wierzcholek["zloze"])

    for sasiad in wierzcholek["sasiedzi"]:
        node.sasiedzi.append(Graf.Sasiad(sasiad["indeks"], sasiad["odleglosc"]))

    return node


def zapisz_do_pliku(lista_wierzcholkow: List[Graf.Domek | Graf.Kopalnia], sciezka: str):

    lista = []
    for wierzcholek in lista_wierzcholkow:
        lista.append(node_na_dict(wierzcholek))

    Path(sciezka).parent.mkdir(parents = True, exist_ok = True)
    with open(sciezka, "w") as plik:
        plik.write(json.dumps(lista, ensure_ascii=False, indent=4))


def wczytaj_plik(sciezka: str):

    with open(sciezka, "r") as plik:
        dane_json = json.loads(plik.read())

    lista = []
    for slownik in dane_json:
        lista.append(dict_do_node(slownik))

    return lista


def node_na_string(wierzcholek: Graf.Domek | Graf.Kopalnia):

    linijka = str(wierzcholek.indeks) + " " + str(wierzcholek.pozycja[0]) + " " + str(wierzcholek.pozycja[1])

    if type(wierzcholek) is Graf.Domek: linijka += " D " + wierzcholek.preferencja + " ."
    else: linijka += " K " + wierzcholek.zloze + " " + str(wierzcholek.pojemnosc)

    # for sasiad in wierzcholek.sasiedzi:
    #     linijka += " " + str(sasiad.indeks_sasiada) + " " + str(sasiad.odleglosc)

    return linijka + "\n"


def string_na_node(wierzcholek: str):

    wlasciwosci = wierzcholek.split(" ")

    node: Graf.Domek | Graf.Kopalnia

    if wlasciwosci[3] == "D":
        node = Graf.Domek(int(wlasciwosci[0]), int(wlasciwosci[1]), int(wlasciwosci[2]), wlasciwosci[4])
    else:
        node = Graf.Kopalnia(int(wlasciwosci[0]), int(wlasciwosci[1]), int(wlasciwosci[2]), int(wlasciwosci[5]), wlasciwosci[4])

    # for i in range(6, len(wlasciwosci), 2):
    #     node.sasiedzi.append(Graf.Sasiad(int(wlasciwosci[i]), float(wlasciwosci[i + 1])))

    return node


def zapisz_do_pliku_raw(lista_wierzcholkow: List[Graf.Domek | Graf.Kopalnia], sciezka: str):

    with open(sciezka, "w") as plik:
        for wierzcholek in lista_wierzcholkow:
            plik.write(node_na_string(wierzcholek))


def wczytaj_plik_raw(sciezka: str):

    with open(sciezka, "r") as plik:
        dane = plik.read()

    lista = []
    for linijka in dane.split("\n"):
        if linijka == "" : continue
        lista.append(string_na_node(linijka))

    return lista