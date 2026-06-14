#algorytm Huffmana - tworzy drzewo z liter wystepujacych w tekscie, dzieki któremu litery
#mozna kodowac binarnie - najmniej pamieci zajmuja litery wystepujace najczesciej

from collections import Counter
import heapq
import itertools

#klasa node wykorzystywana do budowy drzewa
class NodeTree(object):
    def __init__(self, left=None, right=None):
        self.left = left
        self.right = right

    def children(self):
        return (self.left, self.right)

    def __str__(self):
        return '%s_%s' % (self.left, self.right)

#funkcja do budowania drzewa
def drzewo_huffmana(node, left=True, binString=''):
    if type(node) is str:
        return {node: binString}
    (l, r) = node.children()
    drzewiec = dict()
    drzewiec.update(drzewo_huffmana(l, True, binString + '0'))
    drzewiec.update(drzewo_huffmana(r, False, binString + '1'))
    return drzewiec

#funkcja glowna, na wejsciu przyjmuje string, na wyjsciu zwraca slownik z zakodowanymi literami
#stringa podanego na wejsciu
def huffman(string):
    freq = {}
    for c in string:
        if c in freq:
            freq[c] += 1
        else:
            freq[c] = 1

    licznik = itertools.count()

    heap = []

    for znak, czestosc in freq.items():
        heapq.heappush(heap, (czestosc, next(licznik), znak))

    while len(heap) > 1:
        c1, _, key1 = heapq.heappop(heap)
        c2, _, key2 = heapq.heappop(heap)

        node = NodeTree(key1, key2)

        heapq.heappush(
            heap,
            (c1 + c2, next(licznik), node)
        )

    return drzewo_huffmana(heap[0][2])


