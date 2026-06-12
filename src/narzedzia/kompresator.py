from algorytmy import kodowanie_Huffmana as Huff
import json

#funkcja kompresowania uzywajaca kodowania Huffmana
def kompresja(plik_wejsciowy):
    with open(plik_wejsciowy, 'r', encoding='utf-8') as plik:
        tekst = plik.read()

    kody = Huff.huffman(tekst)

    zakodowany_tekst = ''
    for znak in tekst:
        zakodowany_tekst += kody[znak]


    with open(plik_wejsciowy + ".huff", 'w', encoding='utf-8') as plik:
        plik.write(zakodowany_tekst)
    with open(plik_wejsciowy + ".kody", 'w', encoding='utf-8') as plik:
        json.dump(kody, plik, ensure_ascii=False, indent=4)

#funkcja dekompresowania uzywajaca kodowania Huffmana
def dekompresja(nowy_plik, plik_z_kodami, plik_zakodowany):
    with open(plik_z_kodami, 'r', encoding='utf-8') as plik:
        kody = json.load(plik)
    with open(plik_zakodowany, 'r', encoding='utf-8') as plik:
        zakodowany = plik.read()

    odwrotne_kody = {kod: znak for znak, kod in kody.items()}

    if len(odwrotne_kody) == 0:
        with open(nowy_plik, 'w', encoding='utf-8') as plik:
            plik.write('')
        return

    if len(odwrotne_kody) == 1:
        znak = list(odwrotne_kody.values())[0]
        odkodowany = znak * len(zakodowany)
        with open(nowy_plik, 'w', encoding='utf-8') as plik:
            plik.write(odkodowany)
        return

    aktualny_kod = ''
    odkodowany = ''

    for bit in zakodowany:
        aktualny_kod += bit
        if aktualny_kod in odwrotne_kody:
            odkodowany += odwrotne_kody[aktualny_kod]
            aktualny_kod = ''
    if aktualny_kod != '':
        raise ValueError("Plik nie jesy poprawnie zakodowany")

    with open(nowy_plik, 'w', encoding='utf-8') as plik:
        plik.write(odkodowany)