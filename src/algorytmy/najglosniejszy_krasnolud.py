from algorytmy.drzewo_przedzialowe import SegmentTree

#Wrapper dla @drzewo_przedzialowe.py
def najglosniejszy(lewy: int, prawy: int, glosnosci: list[int]):

    # RMQ - Drzewo przedziałowe
    drzewo = SegmentTree(glosnosci)
    return drzewo.query(lewy, prawy)
