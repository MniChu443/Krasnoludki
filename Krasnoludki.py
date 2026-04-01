import Generator
import ObslugaJSON


# graf = Generator.wygeneruj_graf()
# ObslugaJSON.zapisz_do_pliku(graf, "DaneTestowe/test.json")
graf = ObslugaJSON.wczytaj_plik("DaneTestowe/test.json")
print(graf)