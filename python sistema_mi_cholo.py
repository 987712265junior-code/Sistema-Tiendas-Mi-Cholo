import csv
from pathlib import Path

CARPETA = Path(__file__).parent
ARCHIVO_PRODUCTOS = CARPETA / 'productos.csv'
ARCHIVO_VENTAS = CARPETA / 'ventas.csv'
COLUMNAS_PRODUCTOS = ['codigo', 'nombre', 'precio', 'stock']
COLUMNAS_VENTAS = ['id', 'codigo', 'cantidad', 'total']

# INTEGRANTE 5: Archivos CSV
def cargar_csv(archivo):
    if not archivo.exists():
        return []
    try:
        with open(archivo, 'r', encoding='utf-8', newline='') as f:
            return list(csv.DictReader(f))
    except (OSError, csv.Error) as error:
        print('Error al leer el archivo:', error)
        return []


def guardar_csv(archivo, datos, columnas):
    try:
        with open(archivo, 'w', encoding='utf-8', newline='') as f:
            escritor = csv.DictWriter(f, fieldnames=columnas)
            escritor.writeheader()
            escritor.writerows(datos)
        return True
    except (OSError, csv.Error) as error:
        print('Error al guardar el archivo:', error)
        return False


productos = cargar_csv(ARCHIVO_PRODUCTOS)
ventas = cargar_csv(ARCHIVO_VENTAS)


# INTEGRANTE 3: Busqueda secuencial y ordenamiento burbuja
def buscar_producto(codigo):
    codigo = codigo.strip().upper()
    for producto in productos:
        if producto['codigo'] == codigo:
            return producto
    return None


def consultar_producto():
    codigo = input('Codigo a buscar: ')
    producto = buscar_producto(codigo)
    if producto is None:
        print('Producto no encontrado')
    else:
        print('Codigo:', producto['codigo'])
        print('Nombre:', producto['nombre'])
        print('Precio: S/', producto['precio'])
        print('Stock:', producto['stock'])


def ordenar_productos():
    cantidad = len(productos)
    for i in range(cantidad - 1):
        for j in range(cantidad - 1 - i):
            if productos[j]['codigo'] > productos[j + 1]['codigo']:
                auxiliar = productos[j]
                productos[j] = productos[j + 1]
                productos[j + 1] = auxiliar
    if guardar_csv(ARCHIVO_PRODUCTOS, productos, COLUMNAS_PRODUCTOS):
        print('Productos ordenados por codigo:')
        mostrar_inventario()
    else:
        print('No se pudo guardar el ordenamiento')


# INTEGRANTE 1: Registro de productos
def registrar_producto():
    if len(productos) >= 100:
        print('Limite de 100 productos alcanzado')
        return
    codigo = input('Codigo (ejemplo P001): ').strip().upper()
    nombre = input('Nombre: ').strip()
    if codigo == '' or nombre == '':
        print('El codigo y el nombre son obligatorios')
        return
    if buscar_producto(codigo) is not None:
        print('El codigo ya esta registrado')
        return
    try:
        precio = float(input('Precio S/: '))
        stock = int(input('Stock inicial: '))
    except ValueError:
        print('Ingrese precio y stock numericos validos')
        return
    if precio <= 0 or stock < 0:
        print('El precio debe ser positivo y el stock no puede ser negativo')
        return
    producto = {'codigo': codigo, 'nombre': nombre,
                'precio': str(round(precio, 2)), 'stock': str(stock)}
    productos.append(producto)
    if guardar_csv(ARCHIVO_PRODUCTOS, productos, COLUMNAS_PRODUCTOS):
        print('Producto registrado correctamente')
    else:
        productos.pop()
# INTEGRANTE 2: Registro de ventas
def registrar_venta():
    codigo = input('Codigo del producto: ')
    producto = buscar_producto(codigo)
    if producto is None:
        print('Producto no encontrado')
        return
    print('Producto:', producto['nombre'])
    print('Precio: S/', producto['precio'])
    try:
        cantidad = int(input('Cantidad a vender: '))
        stock_actual = int(producto['stock'])
        precio = float(producto['precio'])
    except ValueError:
        print('Cantidad o datos numericos invalidos')
        return
    if cantidad <= 0 or cantidad > stock_actual:
        print('Cantidad invalida o stock insuficiente')
        return
    total = round(cantidad * precio, 2)
    siguiente_id = 1
    for venta_anterior in ventas:
        try:
            numero = int(venta_anterior['id'])
            if numero >= siguiente_id:
                siguiente_id = numero + 1
        except (ValueError, KeyError):
            print('Existe un identificador de venta incorrecto')
            return
    venta = {'id': str(siguiente_id), 'codigo': producto['codigo'],
             'cantidad': str(cantidad), 'total': str(total)}
    # Primero se guarda el inventario actualizado.
    producto['stock'] = str(stock_actual - cantidad)
    if not guardar_csv(ARCHIVO_PRODUCTOS, productos, COLUMNAS_PRODUCTOS):
        producto['stock'] = str(stock_actual)
        return
    ventas.append(venta)
    if guardar_csv(ARCHIVO_VENTAS, ventas, COLUMNAS_VENTAS):
        print('Venta registrada: S/', total)
        print('Stock restante:', producto['stock'])
    else:
        ventas.pop()
        producto['stock'] = str(stock_actual)
        if not guardar_csv(ARCHIVO_PRODUCTOS, productos, COLUMNAS_PRODUCTOS):
            print('ATENCION: revise los archivos CSV antes de continuar')
        else:
            print('La venta no se registro')


# INTEGRANTE 4: Inventario e ingresos
def mostrar_inventario():
    print('\n===== INVENTARIO =====')
    if len(productos) == 0:
        print('No hay productos registrados')
    else:
        for producto in productos:
            print(producto['codigo'], '-', producto['nombre'],
                  '| Precio: S/', producto['precio'],
                  '| Stock:', producto['stock'])
def mostrar_ingresos():
    ingresos = 0
    try:
        for venta in ventas:
            ingresos = ingresos + float(venta['total'])
        print('Ingresos acumulados: S/', round(ingresos, 2))
    except (ValueError, KeyError):
        print('Error: revise los datos del archivo de ventas')


# INTEGRANTE 5: Menu principal
def menu():
    opcion = ''
    while opcion != '5':
        print('\n===== TIENDAS MI CHOLO =====')
        print('1. Registrar productos')
        print('2. Registrar ventas')
        print('3. Buscar y ordenar productos')
        print('4. Consultar inventario e ingresos')
        print('5. Salir')
        opcion = input('Seleccione una opcion: ').strip()
        if opcion == '1':
            registrar_producto()
        elif opcion == '2':
            registrar_venta()
        elif opcion == '3':
            print('1. Buscar producto')
            print('2. Ordenar productos')
            subopcion = input('Seleccione una opcion: ').strip()
            if subopcion == '1':
                consultar_producto()
            elif subopcion == '2':
                ordenar_productos()
            else:
                print('Subopcion invalida')
        elif opcion == '4':
            mostrar_inventario()
            mostrar_ingresos()
        elif opcion == '5':
            print('Fin del sistema')
        else:
            print('Opcion invalida')


if __name__ == '__main__':
    menu()
