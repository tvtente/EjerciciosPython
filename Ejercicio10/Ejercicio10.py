"""Ejercicio 10: ordenar una lista mediante el algoritmo QuickSort."""


def quicksort(lista):
    """Devuelve una nueva lista con sus elementos ordenados."""
    if len(lista) <= 1:
        return lista

    pivote = lista[0]
    izquierda = []
    derecha = []

    for elemento in lista[1:]:
        if elemento < pivote:
            izquierda.append(elemento)
        else:
            derecha.append(elemento)

    return quicksort(izquierda) + [pivote] + quicksort(derecha)


if __name__ == "__main__":
    numeros = [8, 3, 1, 7, 0, 10, 2, 5]

    print("Lista original:", numeros)
    print("Lista ordenada:", quicksort(numeros))
    input("\nPresione Enter para finalizar...")
