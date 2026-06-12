from narzedzia import kompresator

#trzeba dodac mozliwosc wyboru sciezki/dodac katalogi do kompresji
opcja = input("Co zamierzasz?\n 1. Skompresowac plik\n 2. Dekompresowac plik\n 0. Wyjscie\n")
if opcja == "1":
    plik = input("Podaj nazwe pliku do skompresowania:\n")
    kompresator.kompresja(plik)
elif opcja == "2":
    nowy_plik = input("Podaj nowa nazwe zdekompresowanego pliku:\n")
    kody = input("Podaj nazwe pliku z kodem:\n")
    paczka = input("Podaj nazwe zakodowanego pliku:\n")
    kompresator.dekompresja(nowy_plik, kody, paczka)
elif opcja == "0":
    exit()