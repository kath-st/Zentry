"""
Estructura de Lista Enlazada genérica para el catálogo dinámico de eventos.
Componente de Cerna Sifuentes - Estructura de Datos
"""

from typing import TypeVar, Generic, Optional, List, Callable
from dataclasses import dataclass

T = TypeVar('T')


@dataclass
class Node(Generic[T]):
    """Nodo de lista enlazada con datos genéricos."""
    data: T
    next: Optional['Node[T]'] = None


class LinkedList(Generic[T]):
    """
    Lista enlazada genérica para almacenar elementos.
    Operaciones: insert, delete, search, traverse, sort
    """

    def __init__(self):
        self.head: Optional[Node[T]] = None
        self._size = 0

    def insert(self, data: T) -> None:
        """Inserta un elemento al final de la lista."""
        new_node = Node(data)
        if not self.head:
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node
        self._size += 1

    def insert_at(self, index: int, data: T) -> None:
        """Inserta un elemento en una posición específica."""
        if index < 0 or index > self._size:
            raise IndexError("Índice fuera de rango")
        
        new_node = Node(data)
        if index == 0:
            new_node.next = self.head
            self.head = new_node
        else:
            current = self.head
            for _ in range(index - 1):
                current = current.next
            new_node.next = current.next
            current.next = new_node
        self._size += 1

    def delete(self, data: T) -> bool:
        """Elimina la primera ocurrencia de un elemento."""
        if not self.head:
            return False

        if self.head.data == data:
            self.head = self.head.next
            self._size -= 1
            return True

        current = self.head
        while current.next:
            if current.next.data == data:
                current.next = current.next.next
                self._size -= 1
                return True
            current = current.next
        return False

    def delete_at(self, index: int) -> Optional[T]:
        """Elimina un elemento en una posición específica."""
        if index < 0 or index >= self._size:
            raise IndexError("Índice fuera de rango")

        if index == 0:
            data = self.head.data
            self.head = self.head.next
            self._size -= 1
            return data

        current = self.head
        for _ in range(index - 1):
            current = current.next
        data = current.next.data
        current.next = current.next.next
        self._size -= 1
        return data

    def get(self, index: int) -> Optional[T]:
        """Obtiene un elemento por índice."""
        if index < 0 or index >= self._size:
            return None

        current = self.head
        for _ in range(index):
            current = current.next
        return current.data if current else None

    def search(self, data: T) -> int:
        """Busca un elemento y retorna su índice, o -1 si no existe."""
        current = self.head
        index = 0
        while current:
            if current.data == data:
                return index
            current = current.next
            index += 1
        return -1

    def search_by(self, predicate: Callable[[T], bool]) -> Optional[T]:
        """Busca un elemento usando una función predicado."""
        current = self.head
        while current:
            if predicate(current.data):
                return current.data
            current = current.next
        return None

    def filter(self, predicate: Callable[[T], bool]) -> 'LinkedList[T]':
        """Filtra elementos según un predicado y retorna nueva LinkedList."""
        result = LinkedList[T]()
        current = self.head
        while current:
            if predicate(current.data):
                result.insert(current.data)
            current = current.next
        return result

    def to_list(self) -> List[T]:
        """Convierte la lista enlazada a una lista de Python."""
        result = []
        current = self.head
        while current:
            result.append(current.data)
            current = current.next
        return result

    def from_list(self, items: List[T]) -> None:
        """Carga elementos desde una lista de Python."""
        self.head = None
        self._size = 0
        for item in items:
            self.insert(item)

    def reverse(self) -> None:
        """Invierte la lista enlazada in-place."""
        prev = None
        current = self.head
        while current:
            next_node = current.next
            current.next = prev
            prev = current
            current = next_node
        self.head = prev

    def merge_sort(self, compare_func: Callable[[T, T], int]) -> 'LinkedList[T]':
        """
        Merge Sort para lista enlazada.
        compare_func(a, b) retorna: -1 si a < b, 0 si a == b, 1 si a > b
        """
        if self._size <= 1:
            return self

        # Convertir a lista, ordenar, y reconstruir
        items = self.to_list()
        self._merge_sort_helper(items, 0, len(items) - 1, compare_func)
        self.from_list(items)
        return self

    def _merge_sort_helper(self, arr: List[T], left: int, right: int,
                           compare_func: Callable[[T, T], int]) -> None:
        """Helper recursivo para merge sort."""
        if left < right:
            mid = (left + right) // 2
            self._merge_sort_helper(arr, left, mid, compare_func)
            self._merge_sort_helper(arr, mid + 1, right, compare_func)
            self._merge(arr, left, mid, right, compare_func)

    def _merge(self, arr: List[T], left: int, mid: int, right: int,
               compare_func: Callable[[T, T], int]) -> None:
        """Helper para merge en merge sort."""
        left_arr = arr[left:mid + 1]
        right_arr = arr[mid + 1:right + 1]
        i = j = 0
        k = left

        while i < len(left_arr) and j < len(right_arr):
            if compare_func(left_arr[i], right_arr[j]) <= 0:
                arr[k] = left_arr[i]
                i += 1
            else:
                arr[k] = right_arr[j]
                j += 1
            k += 1

        while i < len(left_arr):
            arr[k] = left_arr[i]
            i += 1
            k += 1

        while j < len(right_arr):
            arr[k] = right_arr[j]
            j += 1
            k += 1

    def quick_sort(self, compare_func: Callable[[T, T], int]) -> 'LinkedList[T]':
        """
        Quick Sort para lista enlazada.
        compare_func(a, b) retorna: -1 si a < b, 0 si a == b, 1 si a > b
        """
        if self._size <= 1:
            return self

        items = self.to_list()
        self._quick_sort_helper(items, 0, len(items) - 1, compare_func)
        self.from_list(items)
        return self

    def _quick_sort_helper(self, arr: List[T], left: int, right: int,
                           compare_func: Callable[[T, T], int]) -> None:
        """Helper recursivo para quick sort."""
        if left < right:
            pi = self._partition(arr, left, right, compare_func)
            self._quick_sort_helper(arr, left, pi - 1, compare_func)
            self._quick_sort_helper(arr, pi + 1, right, compare_func)

    def _partition(self, arr: List[T], left: int, right: int,
                   compare_func: Callable[[T, T], int]) -> int:
        """Helper para particionar en quick sort."""
        pivot = arr[right]
        i = left - 1

        for j in range(left, right):
            if compare_func(arr[j], pivot) < 0:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]

        arr[i + 1], arr[right] = arr[right], arr[i + 1]
        return i + 1

    def binary_search(self, target: T, compare_func: Callable[[T, T], int]) -> int:
        """
        Búsqueda binaria en lista enlazada (requiere estar ordenada).
        Retorna índice si encontrado, -1 si no existe.
        """
        items = self.to_list()
        left, right = 0, len(items) - 1

        while left <= right:
            mid = (left + right) // 2
            cmp = compare_func(items[mid], target)
            if cmp == 0:
                return mid
            elif cmp < 0:
                left = mid + 1
            else:
                right = mid - 1
        return -1

    def binary_search_by(self, predicate: Callable[[T], bool]) -> Optional[T]:
        """
        Búsqueda binaria usando predicado (para valores específicos).
        """
        items = self.to_list()
        left, right = 0, len(items) - 1

        while left <= right:
            mid = (left + right) // 2
            if predicate(items[mid]):
                return items[mid]
            left = mid + 1
        return None

    def __len__(self) -> int:
        """Retorna el tamaño de la lista."""
        return self._size

    def __iter__(self):
        """Permite iterar sobre la lista."""
        current = self.head
        while current:
            yield current.data
            current = current.next

    def __repr__(self) -> str:
        """Representación en string de la lista."""
        items = self.to_list()
        return f"LinkedList({items})"

    def clear(self) -> None:
        """Limpia toda la lista."""
        self.head = None
        self._size = 0
