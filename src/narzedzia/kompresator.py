from algorytmy import kodowanie_Huffmana as Huff
import json


def kompresja(plik_wejsciowy, plik_wyjsciowy):
    with open(plik_wejsciowy, 'r', encoding='utf-8') as f:
        tekst = f.read()

    kody = Huff.huffman(tekst)

    zakodowany_tekst = ''
    for znak in tekst:
        zakodowany_tekst += kody[znak]

    dane = {
        'kody': kody,
        'zakodowany_tekst': zakodowany_tekst
    }

    with open(plik_wyjsciowy, 'w', encoding='utf-8') as f:
        json.dump(dane, f, ensure_ascii=False)

