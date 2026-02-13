# modelos/producto.py

class Producto:
    """Representa un producto en el inventario."""

    def __init__(self, id_producto: int, nombre: str, cantidad: int, precio: float):
        """Inicializa un nuevo producto."""
        self.__id = id_producto
        self.__nombre = nombre
        self.set_cantidad(cantidad)  # Valida cantidad
        self.set_precio(precio)      # Valida precio

    # Getters
    def get_id(self):
        return self.__id

    def get_nombre(self):
        return self.__nombre

    def get_cantidad(self):
        return self.__cantidad

    def get_precio(self):
        return self.__precio

    # Setters
    def set_nombre(self, nombre: str):
        self.__nombre = nombre

    def set_cantidad(self, cantidad: int):
        if cantidad < 0:
            raise ValueError("La cantidad no puede ser un número negativo.")
        self.__cantidad = cantidad

    def set_precio(self, precio: float):
        if precio < 0:
            raise ValueError("El precio no puede ser negativo.")
        self.__precio = precio

    def __str__(self):
        return f"ID: {self.__id} | Nombre: {self.__nombre} | Cantidad: {self.__cantidad} | Precio: ${self.__precio:.2f}"