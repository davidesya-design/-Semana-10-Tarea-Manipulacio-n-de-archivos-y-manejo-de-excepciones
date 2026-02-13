# servicios/inventario.py

from modelos.producto import Producto


class Inventario:
    """Gestiona la lista de productos del inventario."""

    def __init__(self):
        self.__productos = []

    def añadir_producto(self, producto: Producto):
        """Añade un producto validando que el ID sea único."""
        if any(p.get_id() == producto.get_id() for p in self.__productos):
            raise ValueError("Ya existe un producto con ese ID.")
        self.__productos.append(producto)

    def eliminar_producto(self, id_producto: int):
        """Elimina un producto por su ID."""
        for p in self.__productos:
            if p.get_id() == id_producto:
                self.__productos.remove(p)
                return True
        return False

    def actualizar_producto(self, id_producto: int, nueva_cantidad=None, nuevo_precio=None):
        """Actualiza cantidad o precio de un producto por ID."""
        for p in self.__productos:
            if p.get_id() == id_producto:
                if nueva_cantidad is not None:
                    p.set_cantidad(nueva_cantidad)
                if nuevo_precio is not None:
                    p.set_precio(nuevo_precio)
                return True
        return False

    def buscar_por_nombre(self, nombre: str):
        """Busca productos por coincidencia parcial del nombre."""
        nombre_lower = nombre.lower()
        return [p for p in self.__productos if nombre_lower in p.get_nombre().lower()]

    def mostrar_todos(self):
        """Devuelve todos los productos registrados."""
        return self.__productos