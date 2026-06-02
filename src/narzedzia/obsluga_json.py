from modele import klasy_grafu as Graf
from typing import List
import json


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


from pathlib import Path

def zapisz_do_pliku(lista_wierzcholkow: List[Graf.Domek | Graf.Kopalnia], sciezka: str):

    lista = []
    for wierzcholek in lista_wierzcholkow:
        lista.append(node_na_dict(wierzcholek))

    Path(sciezka).parent.mkdir(parents=True, exist_ok=True)
    with open(sciezka, "w") as plik:
        plik.write(json.dumps(lista, ensure_ascii=False, indent=4))


def wczytaj_plik(sciezka: str):

    with open(sciezka, "r") as plik:
        dane_json = json.loads(plik.read())

    lista = []
    for slownik in dane_json:
        lista.append(dict_do_node(slownik))

    return lista