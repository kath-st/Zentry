from eventos.models import Asiento

def numero_a_letras(n):
    """
    Convierte números a letras
    1 -> A
    2 -> B
    """
    resultado = ""
    while n > 0:
        n, resto = divmod(n - 1, 26)
        resultado = chr(65 + resto) + resultado
    return resultado


def generar_asientos_para_zona(zona):
    """
    Genera los asientos para una zona:
    - filas convertidas a letras (A, B, C...)
    - columnas 1..N
    Ejemplo: C-12
    """
    for numero_fila in range(1, zona.filas + 1):
        fila_letra = numero_a_letras(numero_fila)

        for columna in range(1, zona.columnas + 1):
            Asiento.objects.create(
                zona=zona,
                fila=fila_letra,
                columna=columna
            )