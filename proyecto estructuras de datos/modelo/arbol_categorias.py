"""
Módulo para el Árbol de Categorías y Subcategorías.
Proyecto: Estructura de Datos 2026 - Catálogo de Películas
"""
import json
from pathlib import Path


def limpiar_texto(texto):
    """Normaliza texto quitando tildes y pasando a minúsculas para búsquedas flexibles."""
    if not texto:
        return ""
    texto = texto.lower().strip()
    reemplazos = (
        ("á", "a"), ("é", "e"), ("í", "i"), ("ó", "o"), ("ú", "u"), ("ñ", "n")
    )
    for con_tilde, sin_tilde in reemplazos:
        texto = texto.replace(con_tilde, sin_tilde)
    return texto


class NodoCategoria:
    """
    Representa un nodo en el árbol (puede ser la raíz, una categoría o una subcategoría).
    Contiene:
    - nombre: Nombre de la categoría o subcategoría.
    - subcategorias: Lista de nodos hijos (NodoCategoria).
    - peliculas: Lista de películas asociadas a este nodo específico.
    """
    def __init__(self, nombre):
        self.nombre = nombre
        self.subcategorias = []  # Nodos hijos (NodoCategoria)
        self.peliculas = []      # Películas guardadas en esta categoría/subcategoría

    def agregar_subcategoria(self, subcategoria_nodo):
        """Agrega un nodo hijo si no existe previamente por nombre."""
        for hijo in self.subcategorias:
            if limpiar_texto(hijo.nombre) == limpiar_texto(subcategoria_nodo.nombre):
                return hijo
        self.subcategorias.append(subcategoria_nodo)
        return subcategoria_nodo

    def agregar_pelicula(self, pelicula):
        """Asocia una película a este nodo."""
        self.peliculas.append(pelicula)

    def es_hoja(self):
        """Retorna True si no tiene subcategorías hijas."""
        return len(self.subcategorias) == 0

    def buscar(self, nombre):
        """
        Búsqueda en profundidad (DFS) insensible a mayúsculas y acentos.
        Retorna el NodoCategoria si coincide, o None.
        """
        if limpiar_texto(self.nombre) == limpiar_texto(nombre):
            return self
        
        for hijo in self.subcategorias:
            encontrado = hijo.buscar(nombre)
            if encontrado is not None:
                return encontrado
        return None

    def total_peliculas(self):
        """Calcula el total de películas de este nodo sumando las de sus subcategorías."""
        total = len(self.peliculas)
        for hijo in self.subcategorias:
            total += hijo.total_peliculas()
        return total

    def obtener_todas_las_peliculas(self):
        """Retorna una lista con todas las películas de este nodo y sus subárboles."""
        resultado = list(self.peliculas)
        for hijo in self.subcategorias:
            resultado.extend(hijo.obtener_todas_las_peliculas())
        return resultado

    def __repr__(self):
        return (f"NodoCategoria('{self.nombre}', subcategorias={len(self.subcategorias)}, "
                f"peliculas={len(self.peliculas)})")


class ArbolCategorias:
    """
    Árbol general (n-ario) que gestiona la jerarquía:
    Raíz -> Categorías Principales -> Subcategorías -> Películas
    """
    def __init__(self, nombre_raiz="Catálogo General de Películas"):
        self.raiz = NodoCategoria(nombre_raiz)

    def buscar(self, nombre):
        """Busca cualquier categoría o subcategoría en el árbol por su nombre."""
        return self.raiz.buscar(nombre)

    def agregar_categoria_subcategoria(self, nombre_categoria, nombre_subcategoria):
        """
        Inserta una categoría principal (hija de raíz) y una subcategoría (hija de categoría).
        Retorna el nodo de la subcategoría.
        """
        nombre_cat = nombre_categoria.strip() if nombre_categoria else "Sin Categoría"
        nombre_sub = nombre_subcategoria.strip() if nombre_subcategoria else "General"

        # 1. Buscar o crear la categoría principal bajo la raíz
        nodo_cat = self.raiz.buscar(nombre_cat)
        if nodo_cat is None or nodo_cat == self.raiz:
            nodo_cat = NodoCategoria(nombre_cat)
            self.raiz.agregar_subcategoria(nodo_cat)

        # 2. Buscar o crear la subcategoría bajo la categoría padre
        nodo_sub = None
        for hijo in nodo_cat.subcategorias:
            if limpiar_texto(hijo.nombre) == limpiar_texto(nombre_sub):
                nodo_sub = hijo
                break

        if nodo_sub is None:
            nodo_sub = NodoCategoria(nombre_sub)
            nodo_cat.agregar_subcategoria(nodo_sub)

        return nodo_sub

    def agregar_pelicula(self, pelicula):
        """
        Agrega una película ubicándola automáticamente en su Categoría y Subcategoría.
        'pelicula' puede ser un diccionario o un objeto Pelicula.
        """
        if isinstance(pelicula, dict):
            cat = pelicula.get("categoria", "Sin Categoría")
            subcat = pelicula.get("subcategoria", "General")
        else:
            cat = getattr(pelicula, "categoria", "Sin Categoría")
            subcat = getattr(pelicula, "subcategoria", "General")

        nodo_sub = self.agregar_categoria_subcategoria(cat, subcat)
        nodo_sub.agregar_pelicula(pelicula)
        return nodo_sub

    def cargar_desde_json(self, ruta_archivo=None):
        """
        Carga las películas desde el archivo Peliculas.json del proyecto
        y construye todo el árbol de categorías y subcategorías.
        """
        if ruta_archivo is None:
            posibles_rutas = [
                Path(__file__).resolve().parent.parent / "datos" / "Peliculas.json",
                Path(__file__).resolve().parent / "datos" / "Peliculas.json",
                Path("datos/Peliculas.json"),
                Path("proyecto estructuras de datos/datos/Peliculas.json"),
            ]
            for p in posibles_rutas:
                if p.exists():
                    ruta_archivo = p
                    break

        if ruta_archivo is None or not Path(ruta_archivo).exists():
            raise FileNotFoundError(f"No se encontró el archivo de películas en: {ruta_archivo}")

        with open(ruta_archivo, "r", encoding="utf-8") as f:
            datos = json.load(f)

        for item in datos:
            self.agregar_pelicula(item)

        print(f"✅ Se cargaron exitosamente {len(datos)} películas en el árbol desde '{ruta_archivo}'.")

    def obtener_ruta(self, nombre_categoria, nodo_actual=None, ruta_actual=None):
        """
        Retorna la ruta jerárquica hasta una categoría/subcategoría.
        Ejemplo: ['Catálogo General', 'Ciencia Ficción', 'Espacio']
        """
        if nodo_actual is None:
            nodo_actual = self.raiz
        if ruta_actual is None:
            ruta_actual = []

        nueva_ruta = ruta_actual + [nodo_actual.nombre]

        if limpiar_texto(nodo_actual.nombre) == limpiar_texto(nombre_categoria):
            return nueva_ruta

        for hijo in nodo_actual.subcategorias:
            res = self.obtener_ruta(nombre_categoria, hijo, nueva_ruta)
            if res is not None:
                return res
        return None

    def obtener_peliculas_por_categoria(self, nombre_categoria):
        """
        Busca un nodo (categoría o subcategoría) y devuelve todas las películas
        asociadas a él y a sus subcategorías descendientes.
        """
        nodo = self.buscar(nombre_categoria)
        if nodo is None:
            return []
        return nodo.obtener_todas_las_peliculas()

    def mostrar(self, nodo=None, prefijo="", es_ultimo=True, mostrar_peliculas=False):
        """
        Imprime el árbol jerárquicamente.
        - mostrar_peliculas=False: muestra solo categorías, subcategorías y la cantidad de películas.
        - mostrar_peliculas=True: además lista los títulos de cada película.
        """
        if nodo is None:
            nodo = self.raiz

        conector = "└── " if es_ultimo else "├── "
        total_pels = nodo.total_peliculas()

        if nodo == self.raiz:
            print(f"📦 {nodo.nombre} (Total: {total_pels} películas)")
        elif len(nodo.subcategorias) > 0:
            print(f"{prefijo}{conector}📁 {nodo.nombre} ({total_pels} películas)")
        else:
            print(f"{prefijo}{conector}📂 {nodo.nombre} ({len(nodo.peliculas)} películas)")

        nuevo_prefijo = prefijo + ("    " if es_ultimo else "│   ")

        if mostrar_peliculas and len(nodo.peliculas) > 0:
            total_items = len(nodo.peliculas)
            for j, pel in enumerate(nodo.peliculas):
                con_pel = "└── " if (j == total_items - 1 and len(nodo.subcategorias) == 0) else "├── "
                titulo = pel["titulo"] if isinstance(pel, dict) else getattr(pel, "titulo", str(pel))
                codigo = pel.get("codigo", "") if isinstance(pel, dict) else getattr(pel, "codigo", "")
                anio = pel.get("anio", "") if isinstance(pel, dict) else getattr(pel, "anio", "")
                print(f"{nuevo_prefijo}{con_pel}🎬 [{codigo}] {titulo} ({anio})")

        total_hijos = len(nodo.subcategorias)
        for i, hijo in enumerate(nodo.subcategorias):
            ultimo = (i == total_hijos - 1)
            self.mostrar(hijo, nuevo_prefijo, ultimo, mostrar_peliculas=mostrar_peliculas)

