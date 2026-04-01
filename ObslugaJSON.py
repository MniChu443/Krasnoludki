import KlasyGrafu as Graf
from typing import List
import json


def node_na_dict(wierzcholek: Graf.Domek | Graf.Kopalnia, indeks: int):

    slownik: dict = {
        "indeks": indeks,
        "x": wierzcholek.x,
        "y": wierzcholek.y,
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
    elif type(wierzcholek) is Graf.Kopalnia:
        slownik["pojemnosc"] = wierzcholek.pojemnosc
        slownik["zloze"] = wierzcholek.zloze

    return slownik


def zapisz_do_pliku(lista_wierzcholkow: List[Graf.Domek | Graf.Kopalnia], nazwa: str):

    lista = []
    for indeks, wierzcholek in enumerate(lista_wierzcholkow):
        lista.append(node_na_dict(wierzcholek, indeks))

    print(json.dumps(lista))
