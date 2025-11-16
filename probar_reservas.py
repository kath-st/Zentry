# probar_reservas.py
import os
import django
import sys
from datetime import timedelta

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "zentry.settings")
django.setup()

from django.utils import timezone
from django.contrib.auth.models import User
from eventos.models import *
from eventos.modulo.reservas.services import GestorDeReservas


# =====================================================
# FUNCIONES DE CONSOLA
# =====================================================

def limpiar():
    os.system("cls" if os.name == "nt" else "clear")

def pausar():
    input("\nPresiona ENTER para continuar...")


# =====================================================
# FORMATO DE ASIENTO "A1" → (fila, columna)
# =====================================================
def parsear_asiento(texto):
    """
    Convierte "A1" o "C12" en ("A", 1)
    """
    texto = texto.strip().upper()

    fila = ""
    columna = ""

    for c in texto:
        if c.isalpha():
            fila += c
        elif c.isdigit():
            columna += c

    if fila == "" or columna == "":
        return None

    return fila, int(columna)


# =====================================================
# MENÚ: SELECCIONAR EVENTO
# =====================================================
def seleccionar_evento():
    print("\n=== EVENTOS DISPONIBLES ===")
    eventos = Evento.objects.all().order_by("fecha")

    for e in eventos:
        print(f"{e.id}) {e.titulo} - {e.fecha.strftime('%Y-%m-%d %H:%M')}")

    ev_id = input("ID del evento: ").strip()

    if not ev_id.isdigit():
        print("ID inválido.")
        return None

    try:
        return Evento.objects.get(id=int(ev_id))
    except:
        print("Evento no encontrado.")
        return None


# =====================================================
# MENÚ: SELECCIONAR ZONA
# =====================================================
def seleccionar_zona(evento):
    print("\n=== ZONAS DEL LOCAL ===")
    zonas = Zona.objects.filter(ubicacion=evento.ubicacion)

    for z in zonas:
        precio = PrecioPorZona.objects.get(evento=evento, zona=z).precio
        print(f"{z.id}) {z.nombre} - S/ {precio}")

    z_id = input("ID de la zona: ").strip()

    if not z_id.isdigit():
        print("ID inválido.")
        return None

    try:
        return Zona.objects.get(id=int(z_id))
    except:
        print("Zona no encontrada.")
        return None


# =====================================================
# LISTAR ASIENTOS DISPONIBLES
# =====================================================
def mostrar_asientos(evento, zona):
    print(f"\n=== ASIENTOS DISPONIBLES: {zona.nombre} ===")

    ocupados = Reserva.objects.filter(evento=evento, activo=True).values_list("asiento_id", flat=True)
    asientos = Asiento.objects.filter(zona=zona).order_by("fila", "columna")

    filas = sorted(list(set(a.fila for a in asientos)))

    for f in filas:
        fila_asientos = asientos.filter(fila=f)
        linea = f"{f}:  "

        for a in fila_asientos:
            if a.id in ocupados:
                linea += "[XX] "
            else:
                linea += f"[{a.columna}] "
        print(linea)


# =====================================================
# PROGRAMA PRINCIPAL
# =====================================================
def main():
    limpiar()
    print("=== TEST DE RESERVAS — ZENTRY ===")

    # Crear usuario de prueba si no existe
    usuario, _ = User.objects.get_or_create(username="test_console")

    gestor = GestorDeReservas()

    # 1. Seleccionar evento
    evento = None
    while evento is None:
        evento = seleccionar_evento()

    # 2. Seleccionar zona
    zona = None
    while zona is None:
        zona = seleccionar_zona(evento)

    # 3. Mostrar asientos
    mostrar_asientos(evento, zona)

    # 4. Crear sesión de compra
    sesion = gestor.iniciar_sesion_compra(usuario, evento)
    print(f"\nSesión creada. Expira en: {sesion.expiracion}")

    # 5. Reservar asientos interactivos
    print("\nIngresa asientos como A1, B3, C12. Escribe FIN para terminar.")

    seleccionados = []

    while True:
        asiento_txt = input("Asiento: ").strip()

        if asiento_txt.upper() == "FIN":
            break

        fila_columna = parsear_asiento(asiento_txt)

        if fila_columna is None:
            print("Formato inválido. Ejemplo válido: A1, C12")
            continue

        fila, col = fila_columna

        try:
            asiento = Asiento.objects.get(zona=zona, fila=fila, columna=col)
        except:
            print("Ese asiento no existe.")
            continue

        try:
            reserva = gestor.reservar_asiento(evento, asiento.id, usuario, sesion)
            seleccionados.append(reserva)
            print(f"✓ Asiento {fila}{col} reservado.")
        except Exception as e:
            print(f"Error: {e}")

    # 6. Confirmar compra
    if not seleccionados:
        print("No seleccionaste asientos. Saliendo...")
        return

    print("\nTus reservas:")
    for r in seleccionados:
        print(f"- {r.asiento.fila}{r.asiento.columna}")

    confirmar = input("\n¿Confirmar compra? (s/n): ").lower()

    if confirmar == "s":
        ids = [r.id for r in seleccionados]
        compra = gestor.confirmar_compra(ids, usuario, "Tarjeta")
        print(f"\nCompra realizada! ID compra: {compra.id}")
    else:
        print("Compra cancelada.")

    pausar()


# =====================================================
if __name__ == "__main__":
    main()
