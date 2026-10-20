
import csv
from pathlib import Path

# Archivos donde se almacenan los datos
CARPETA = Path(__file__).parent
ARCHIVO_PRODUCTOS = CARPETA / "productos.csv"
ARCHIVO_VENTAS = CARPETA / "ventas.csv"


# INTEGRANTE 4: Manejo de archivos CSV
def cargar_csv(archivo):
    if not archivo.exists():
        return []

    try:
        with open(archivo, "r", encoding="utf-8", newline="") as f:
            return list(csv.DictReader(f))
    except (OSError, csv.Error) as error:
        print("Error al leer archivo:", error)
        return []


def guardar_csv(archivo, datos, columnas):
    try:
        with open(archivo, "w", encoding="utf-8", newline="") as f:
            escritor = csv.DictWriter(f, fieldnames=columnas)
            escritor.writeheader()
            escritor.writerows(datos)
        return True
    except (OSError, csv.Error) as error:
        print("Error al guardar:", error)
        return False


productos = cargar_csv(ARCHIVO_PRODUCTOS)
ventas = cargar_csv(ARCHIVO_VENTAS)


# INTEGRANTE 3: Busqueda de productos
def buscar_producto(codigo):
    codigo = codigo.strip().upper()

    for producto in productos:
        if producto["codigo"] == codigo:
            return producto

    return None


# INTEGRANTE 1: Registro de productos
def registrar_producto():
    codigo = input("Codigo (P001): ").strip().upper()
    nombre = input("Nombre: ").strip()

    if not codigo or not nombre or buscar_producto(codigo):
        print("Codigo duplicado o datos vacios")
        return

    try:
        precio = float(input("Precio S/: "))
        stock = int(input("Stock inicial: "))

        if precio <= 0 or stock < 0:
            print("Precio o stock invalido")
            return

        producto = {
            "codigo": codigo,
            "nombre": nombre,
            "precio": str(precio),
            "stock": str(stock)
        }

        productos.append(producto)

        if guardar_csv(ARCHIVO_PRODUCTOS, productos,
                       ["codigo", "nombre", "precio", "stock"]):
            print("Producto registrado correctamente")
        else:
            productos.pop()

    except ValueError:
        print("Ingrese numeros validos")


# INTEGRANTE 2: Registro de ventas
def registrar_venta():
    codigo = input("Codigo del producto: ")
    producto = buscar_producto(codigo)

    if producto is None:
        print("Producto no encontrado")
        return

    try:
        cantidad = int(input("Cantidad a vender: "))
        stock = int(producto["stock"])
        precio = float(producto["precio"])

        if cantidad <= 0 or cantidad > stock:
            print("Cantidad invalida o stock insuficiente")
            return

        total = round(cantidad * precio, 2)

        venta = {
            "id": str(len(ventas) + 1),
            "codigo": producto["codigo"],
            "cantidad": str(cantidad),
            "total": str(total)
        }

        # Guardar primero la venta y despues el inventario
        ventas.append(venta)
        if not guardar_csv(ARCHIVO_VENTAS, ventas,
                          ["id", "codigo", "cantidad", "total"]):
            ventas.pop()
            return

        producto["stock"] = str(stock - cantidad)

        if guardar_csv(ARCHIVO_PRODUCTOS, productos,
                       ["codigo", "nombre", "precio", "stock"]):
            print("Venta registrada: S/", total)
            print("Stock restante:", producto["stock"])
        else:
            print("Aviso: revisar archivos de venta e inventario")

    except ValueError:
        print("Cantidad o datos numericos invalidos")


# INTEGRANTE 3: Busqueda, ordenamiento e inventario
def consultar_producto():
    codigo = input("Codigo a buscar: ")
    producto = buscar_producto(codigo)

    if producto:
        print("Producto:", producto["nombre"])
        print("Precio: S/", producto["precio"])
        print("Stock:", producto["stock"])
    else:
        print("Producto no encontrado")


def ordenar_productos():
    for producto in sorted(productos, key=lambda p: p["codigo"]):
        print(producto["codigo"], "-", producto["nombre"])


def mostrar_inventario():
    for producto in productos:
        print(producto["codigo"], "-", producto["nombre"],
              "| Stock:", producto["stock"])


# INTEGRANTE 4: Ingresos y menu principal
def mostrar_ingresos():
    total = sum(float(venta["total"]) for venta in ventas)
    print("Ingresos acumulados: S/", round(total, 2))


def menu():
    while True:
        print("\n===== TIENDAS MI CHOLO =====")
        print("1. Registrar producto")
        print("2. Registrar venta")
        print("3. Buscar producto")
        print("4. Ordenar productos")
        print("5. Consultar inventario")
        print("6. Consultar ingresos")
        print("7. Salir")

        opcion = input("Seleccione una opcion: ").strip()

        if opcion == "1":
            registrar_producto()
        elif opcion == "2":
            registrar_venta()
        elif opcion == "3":
            consultar_producto()
        elif opcion == "4":
            ordenar_productos()
        elif opcion == "5":
            mostrar_inventario()
        elif opcion == "6":
            mostrar_ingresos()
        elif opcion == "7":
            print("Fin del sistema")
            break
        else:
            print("Opcion invalida")


if __name__ == "__main__":
    menu()
