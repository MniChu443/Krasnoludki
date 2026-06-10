from typing import List, Tuple, Optional

class SegmentTree:
   #Range Maximum Query -zapytania o przedzialy w czasie O(log n)

    def __init__(self, data: List[int]):
        
        self.n = len(data)
        # Drzewo przechowuje krotki (maksymalna_wartość, indeks_w_oryginalnej_tablicy)
        # Optymalny rozmiar tablicy dla drzewa przedziałowego to 4 * n
        self.tree: List[Optional[Tuple[int, int]]] = [None] * (4 * self.n)
        if self.n > 0:
            self._build(data, 0, 0, self.n - 1)

    def _build(self, data: List[int], node: int, start: int, end: int):
        
        if start == end:
            # Węzeł-liść, przypisujemy mu wartość i indeks z tablicy początkowej
            self.tree[node] = (data[start], start)
        else:
            mid = (start + end) // 2
            left_child = 2 * node + 1
            right_child = 2 * node + 2
            
            # Budowa poddrzew
            self._build(data, left_child, start, mid)
            self._build(data, right_child, mid + 1, end)
            
            # Węzeł wewnętrzny przyjmuje maksimum ze swoich dzieci
            left_val = self.tree[left_child]
            right_val = self.tree[right_child]
            
            if left_val[0] >= right_val[0]:
                self.tree[node] = left_val
            else:
                self.tree[node] = right_val

    def query(self, left: int, right: int) -> Tuple[int, int]:
       
        if left < 0 or right >= self.n or left > right:
            raise ValueError("Nieprawidłowe granice zapytania o przedział")
            
        return self._query_recursive(0, 0, self.n - 1, left, right)

    def _query_recursive(self, node: int, start: int, end: int, left: int, right: int) -> Tuple[int, int]:
        
        # 1. Przedział węzła zawiera się całkowicie w zapytaniu
        if left <= start and right >= end:
            return self.tree[node]
            
        # 2. Przedział węzła znajduje się poza przedziałem zapytania
        if end < left or start > right:
            return (-float('inf'), -1)
            
        # 3. Częściowe pokrycie przedziałów, konieczne wejście głębiej do dzieci węzła
        mid = (start + end) // 2
        left_child = 2 * node + 1
        right_child = 2 * node + 2
        
        left_res = self._query_recursive(left_child, start, mid, left, right)
        right_res = self._query_recursive(right_child, mid + 1, end, left, right)
        
        if left_res[0] >= right_res[0]:
            return left_res
        else:
            return right_res
