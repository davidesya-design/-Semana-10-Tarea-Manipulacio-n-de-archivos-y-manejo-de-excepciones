# servicios/inventario.py

from modelos.producto import Producto
from pathlib import Path
import os


class Inventario:
    """Gestiona la lista de productos del inventario con persistencia en archivo.

    El inventario se guarda en un archivo de texto llamado `inventario.txt` en
    la raíz del proyecto. Cada línea del archivo representa un producto con el
    formato: id;nombre;cantidad;precio

    El código maneja excepciones comunes de archivos (FileNotFoundError,
    PermissionError, OSError) y realiza tolerancia a líneas corruptas al cargar.
    """

    def __init__(self):
        self.__productos = []
        # Determinar ruta del archivo en la raíz del proyecto
        base_dir = Path(__file__).resolve().parents[1]
        self._archivo = base_dir / "inventario.txt"
        self.__cargar_desde_archivo()

    def __cargar_desde_archivo(self):
        """Carga productos desde `inventario.txt`.

        Si el archivo no existe, se crea vacío. Las líneas que no cumplen el
        formato esperado se ignoran (se notifica por consola) para evitar que
        un archivo parcialmente corrupto bloquee la aplicación.
        """
        try:
            # Crear archivo si no existe
            if not self._archivo.exists():
                try:
                    self._archivo.touch()
                except PermissionError:
                    print(f"Aviso: No se pudo crear {self._archivo} (permiso denegado).")
                    return

            with self._archivo.open("r", encoding="utf-8") as f:
                for linea in f:
                    linea = linea.strip()
                    if not linea:
                        continue
                    partes = linea.split(";")
                    if len(partes) != 4:
                        print(f"Linea ignorada (formato inválido): {linea}")
                        continue
                    try:
                        id_p = int(partes[0])
                        nombre = partes[1]
                        cantidad = int(partes[2])
                        precio = float(partes[3])
                        producto = Producto(id_p, nombre, cantidad, precio)
                        self.__productos.append(producto)
                    except Exception as e:
                        print(f"Linea ignorada (error al parsear): {linea} -> {e}")
        except PermissionError:
            print(f"Aviso: No se pudo leer {self._archivo} (permiso denegado).")
        except OSError as e:
            print(f"Aviso: Error al acceder a {self._archivo}: {e}")

    def __guardar_todos(self):
        """Escribe todos los productos en el archivo, sobrescribiendo su contenido.

        Devuelve True si la operación tuvo éxito, o lanza la excepción capturada
        para que el llamador la gestione (se recomienda manejo en la UI).
        """
        try:
            # Escribimos en modo 'w' para mantener el archivo consistente
            with self._archivo.open("w", encoding="utf-8") as f:
                for p in self.__productos:
                    linea = f"{p.get_id()};{p.get_nombre()};{p.get_cantidad()};{p.get_precio()}\n"
                    f.write(linea)
            return True
        except PermissionError:
            raise
        except OSError:
            raise

    def añadir_producto(self, producto: Producto):
        """Añade un producto validando que el ID sea único y lo persiste.

        Si la persistencia falla, revierte el cambio en memoria y propaga la
        excepción para que la capa de UI notifique al usuario.
        """
        if any(p.get_id() == producto.get_id() for p in self.__productos):
            raise ValueError("Ya existe un producto con ese ID.")

        # Añadir en memoria
        self.__productos.append(producto)
        try:
            self.__guardar_todos()
            return True
        except Exception:
            # Revertir en memoria
            self.__productos = [p for p in self.__productos if p.get_id() != producto.get_id()]
            raise

    def eliminar_producto(self, id_producto: int):
        """Elimina un producto por su ID y persiste el cambio.

        Retorna True si se eliminó, False si no se encontró. Si la escritura
        falla, revierte el cambio y propaga la excepción.
        """
        encontrado = None
        for p in self.__productos:
            if p.get_id() == id_producto:
                encontrado = p
                break
        if not encontrado:
            return False

        # Remover y guardar
        self.__productos.remove(encontrado)
        try:
            self.__guardar_todos()
            return True
        except Exception:
            # Revertir
            self.__productos.append(encontrado)
            raise

    def actualizar_producto(self, id_producto: int, nueva_cantidad=None, nuevo_precio=None):
        """Actualiza cantidad o precio de un producto por ID y persiste.

        Si la escritura falla, revierte los cambios en memoria y propaga la
        excepción para que la UI la muestre.
        """
        for p in self.__productos:
            if p.get_id() == id_producto:
                # Guardar estado anterior para posible reversión
                old_cantidad = p.get_cantidad()
                old_precio = p.get_precio()
                try:
                    if nueva_cantidad is not None:
                        p.set_cantidad(nueva_cantidad)
                    if nuevo_precio is not None:
                        p.set_precio(nuevo_precio)
                    self.__guardar_todos()
                    return True
                except Exception:
                    # Revertir cambios en memoria
                    p.set_cantidad(old_cantidad)
                    p.set_precio(old_precio)
                    raise
        return False

    def buscar_por_nombre(self, nombre: str):
        """Busca productos por coincidencia parcial del nombre."""
        nombre_lower = nombre.lower()
        return [p for p in self.__productos if nombre_lower in p.get_nombre().lower()]

    def mostrar_todos(self):
        """Devuelve todos los productos registrados."""
        return self.__productos