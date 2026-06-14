from algorytmy import kodowanie_Huffmana as Huff
import json

#funkcje konwersji na bajty i na bity potrzebne do kompresji
def bity_na_bajty(bity):
    temp = (8 - len(bity) % 8) % 8
    bity += '0' * temp

    dane = bytearray()
    dane.append(temp)

    for i in range(0, len(bity), 8):
        bajt = bity[i:i+8]
        dane.append(int(bajt, 2))

    return bytes(dane)

def bajty_na_bity(dane):
    temp = dane[0]
    bity = ''

    for bajt in dane[1:]:
        bity += format(bajt, '08b')

    if temp:
        bity = bity[:-temp]

    return bity

#funkcja kompresowania uzywajaca kodowania Huffmana
def kompresja(plik_wejsciowy):
    with open(plik_wejsciowy, 'r', encoding='utf-8') as plik:
        tekst = plik.read()

    kody = Huff.huffman(tekst)

    zakodowany_tekst = ''.join(kody[znak] for znak in tekst)


    with open(plik_wejsciowy + ".huff", 'wb') as plik:
        plik.write(bity_na_bajty(zakodowany_tekst))
    with open(plik_wejsciowy + ".huffcode", 'w', encoding='utf-8') as plik:
        json.dump(kody, plik, ensure_ascii=False, indent=4)

#funkcja dekompresowania uzywajaca kodowania Huffmana
def dekompresja(nowy_plik, plik_z_kodami, plik_zakodowany):
    with open(plik_z_kodami, 'r', encoding='utf-8') as plik:
        kody = json.load(plik)
    with open(plik_zakodowany, 'rb') as plik:
        temp = plik.read()
    zakodowany = bajty_na_bity(temp)
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