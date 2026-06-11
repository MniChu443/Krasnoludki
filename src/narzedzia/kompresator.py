from algorytmy import kodowanie_Huffmana as Huff
import json


def kompresja(plik_wejsciowy, plik_wyjsciowy):
    with open(plik_wejsciowy, 'r', encoding='utf-8') as plik:
        tekst = plik.read()

    kody = Huff.huffman(tekst)

    zakodowany_tekst = ''
    for znak in tekst:
        zakodowany_tekst += kody[znak]

    dane = {
        'kody': kody,
        'zakodowany_tekst': zakodowany_tekst
    }

    with open(plik_wyjsciowy, 'w', encoding='utf-8') as plik:
        json.dump(dane, plik, ensure_ascii=False)


def odkoduj_plik_huffmanem(plik_wejsciowy, plik_wyjsciowy):
    with open(plik_wejsciowy, 'r', encoding='utf-8') as plik:
        dane = json.load(plik)

    kody = dane['kody']
    zakodowany = dane['zakodowany_tekst']

    odwrotne_kody = {kod: znak for znak, kod in kody.items()}

    if len(odwrotne_kody) == 0:
        with open(plik_wyjsciowy, 'w', encoding='utf-8') as plik:
            plik.write('')
        return

    if len(odwrotne_kody) == 1:
        znak = list(odwrotne_kody.values())[0]
        odkodowany = znak * len(zakodowany)
        with open(plik_wyjsciowy, 'w', encoding='utf-8') as plik:
            plik.write(odkodowany)
        return

    aktualny_kod = ''
    odkodowany = ''

    for bit in zakodowany:
        aktualny_kod += bit
        if aktualny_kod in odwrotne_kody:
            odkodowany += odwrotne_kody[aktualny_kod]
            aktualny_kod = ''

    with open(plik_wyjsciowy, 'w', encoding='utf-8') as plik:
        plik.write(odkodowany)