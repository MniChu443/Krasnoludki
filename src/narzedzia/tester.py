from narzedzia import czasomierz as Czas
from narzedzia import generator as Generator
from algorytmy import przeplyw as Przeplyw


class Tester:
    """Klasa do masowego testowania algorytmu rozdzielania pracy"""

    def __init__(self):
        self.czasomierz = Czas.Czasomierz()

    def test(self, wysokosc: int, szerokosc: int, proporcja: float, materialy: list[str], testy: int, plik):
        """Generuje miasto z podanymi właściwościami i zapisuje czasy działania algorytmu do pliku"""

        print(f"> Test x{testy} dla {wysokosc}x{szerokosc} w proporcji {proporcja}, materiały: {materialy}")
        plik.write(f"{testy};{wysokosc};{szerokosc};{proporcja};{len(materialy)}")

        suma_sieci = 0
        suma_algorytmu = 0
        najgorszy_siec = 0
        najlepszy_siec = 999999999
        najgorszy_algorytm = 0
        najlepszy_algorytm = 999999999
        suma_domkow = 0
        suma_kopalni = 0

        for _ in range(testy):

            miasto = Generator.wygeneruj_miasto(szerokosc, wysokosc, proporcja, 1, materialy)
            suma_domkow += len(miasto.domki)
            suma_kopalni += len(miasto.kopalnie)

            self.czasomierz.start()
            graf = Przeplyw.SiecPrzeplywowa(miasto)
            czas_sieci = self.czasomierz.stop()
            suma_sieci += czas_sieci
            if najgorszy_siec < czas_sieci: najgorszy_siec = czas_sieci
            if najlepszy_siec > czas_sieci: najlepszy_siec = czas_sieci

            self.czasomierz.start()
            graf.PAROWANIE()
            czas_algorytmu = self.czasomierz.stop()
            suma_algorytmu += czas_algorytmu
            if najgorszy_algorytm < czas_algorytmu: najgorszy_algorytm = czas_algorytmu
            if najlepszy_algorytm > czas_algorytmu: najlepszy_algorytm = czas_algorytmu

        plik.write(f";{suma_domkow/testy};{suma_kopalni/testy};{suma_sieci/testy};{najgorszy_siec};{najlepszy_siec};{suma_algorytmu/testy};{najgorszy_algorytm};{najlepszy_algorytm}\n")

    def test_ogolny(self, naglowek: bool = False):
        """Masowo generuje testy z podanych wartości cech"""

        wysokosci = [10]
        szerokosci = [10]
        proporcje = [0.7]
        materialy = [4]
        lista = ["ZLOTO", "DIAMENTY", "WEGIEL", "REDSTONE", "LAPIS", "ZELAZO", "MIEDZ", "KWARC"]

        with open("../../dane/dane_testowe.txt", "a") as plik:
            if naglowek: plik.write(f"TESTY;WYSOKOSC;SZEROKOSC;PROPORCJA;MATERIALY;DOMKI;KOPALNIE;SREDNIA SIEC;NAJGORSZA SIEC;NAJLEPSZA SIEC;SREDNIA ALGORYTM;NAJGORSZA ALGORYTM;NAJLEPSZA ALGORYTM\n")

            for w in wysokosci:
                for s in szerokosci:
                    for p in proporcje:
                        for m in materialy:
                            self.test(w, s, p, lista[0:m], 100, plik)


if __name__ == "__main__":
    tester = Tester()
    tester.test_ogolny(False)