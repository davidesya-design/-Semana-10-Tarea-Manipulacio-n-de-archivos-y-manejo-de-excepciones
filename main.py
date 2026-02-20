5# main.py

from modelos.producto import Producto
from servicios.inventario import Inventario


def mostrar_menu():
    print("\n===== SISTEMA DE INVENTARIO =====")
    print("1. Añadir producto")
    print("2. Eliminar producto")
    print("3. Actualizar producto")
    print("4. Buscar producto")
    print("5. Listar inventario")
    print("6. Salir")


def add_product(inventario):
    try:
        id_producto = int(input("ID: "))
        nombre = input("Nombre: ").strip()
        if not nombre:
            print("Error: El nombre no puede estar vacío.")
            return
        cantidad = int(input("Cantidad: "))
        precio = float(input("Precio: "))
        
        producto = Producto(id_producto, nombre, cantidad, precio)
        try:
            if inventario.añadir_producto(producto):
                print("Producto añadido correctamente y guardado en inventario.")
        except ValueError as ve:
            # Repetir ID o validaciones del modelo
            print(f"Error: {ve}")
        except PermissionError:
            print("Error: No hay permiso para escribir el archivo de inventario.")
        except OSError as e:
            print(f"Error al escribir en el archivo de inventario: {e}")
    except ValueError as e:
        print(f"Error: {e}")


def delete_product(inventario):
    try:
        id_producto = int(input("ID del producto a eliminar: "))
        try:
            if inventario.eliminar_producto(id_producto):
                print("Producto eliminado correctamente y cambios guardados.")
            else:
                print("Producto no encontrado.")
        except PermissionError:
            print("Error: No hay permiso para modificar el archivo de inventario.")
        except OSError as e:
            print(f"Error al actualizar el archivo de inventario: {e}")
    except ValueError:
        print("Error: ID debe ser un número entero.")


def update_product(inventario):
    try:
        id_producto = int(input("ID del producto a actualizar: "))
        cantidad = input("Nueva cantidad (dejar vacío si no desea cambiar): ").strip()
        precio = input("Nuevo precio (dejar vacío si no desea cambiar): ").strip()
        
        nueva_cantidad = int(cantidad) if cantidad else None
        nuevo_precio = float(precio) if precio else None
        try:
            if inventario.actualizar_producto(id_producto, nueva_cantidad, nuevo_precio):
                print("Producto actualizado correctamente y cambios guardados.")
            else:
                print("Producto no encontrado.")
        except ValueError as ve:
            print(f"Error: {ve}")
        except PermissionError:
            print("Error: No hay permiso para escribir el archivo de inventario.")
        except OSError as e:
            print(f"Error al escribir en el archivo de inventario: {e}")
    except ValueError as e:
        print(f"Error: {e}")


def search_product(inventario):
    nombre = input("Ingrese nombre a buscar: ").strip()
    if not nombre:
        print("Error: Ingrese un nombre válido.")
        return
    
    resultados = inventario.buscar_por_nombre(nombre)
    if resultados:
        print("\nResultados encontrados:")
        for p in resultados:
            print(p)
    else:
        print("No se encontraron productos.")


def list_inventory(inventario):
    productos = inventario.mostrar_todos()
    if productos:
        print("\nInventario actual:")
        for p in productos:
            print(p)
    else:
        print("El inventario está vacío.")


def main():
    inventario = Inventario()
    
    options = {
        1: add_product,
        2: delete_product,
        3: update_product,
        4: search_product,
        5: list_inventory,
    }

    while True:
        mostrar_menu()
        try:
            opcion = int(input("Seleccione una opción: "))
            
            if opcion in options:
                options[opcion](inventario)
            elif opcion == 6:
                print("Saliendo del sistema...")
                break
            else:
                print("Opción inválida.")
        except ValueError:
            print("Error: Ingrese un número válido.")


if __name__ == "__main__":
    main()