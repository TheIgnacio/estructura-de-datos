"""
Módulo de Estructura de Datos: Árbol General de Categorías
Adaptado para el Catálogo de Películas del Proyecto Estructura de Datos 2026.
"""
from __future__ import annotations
import json
import sys
from pathlib import Path

base_dir = Path(__file__).resolve().parent.parent / "proyecto estructuras de datos"
if str(base_dir) not in sys.path:
    sys.path.append(str(base_dir))

from modelo.pelicula import Pelicula


class NodoCategoria:
    """
    Un nodo del árbol general de categorías.

    Cada nodo tiene:
        - nombre (str): nombre de la categoría, ej. "Ciencia Ficción" o "Comedia".
        - subcategorias (list): lista de NodoCategoria hijos.
        - elementos (list): lista de Pelicula que pertenecen a esta categoría.

    Nota: las películas se almacenan principalmente en las categorías HOJA
    (las que no tienen subcategorías). Las categorías intermedias agrupan pero no
    contienen películas directamente.
    """

    def __init__(self, nombre: str):
        self.nombre = nombre
        self.subcategorias: list[NodoCategoria] = []
        self.elementos: list[Pelicula] = []

    def agregar_subcategoria(self, nombre_sub: str) -> "NodoCategoria":
        nuevo = NodoCategoria(nombre_sub)
        self.subcategorias.append(nuevo)
        return nuevo

    def es_hoja(self) -> bool:
        return len(self.subcategorias) == 0

    def mostrar(self, nivel: int = 0):
        prefijo = "    " * nivel
        marcador = "📄" if self.es_hoja() else "📁"
        cantidad = len(self.elementos)
        print(f"{prefijo}{marcador} {self.nombre} ({cantidad} película/s)")

        for sub in self.subcategorias:
            sub.mostrar(nivel + 1)

    def buscar_categoria(self, nombre_buscado: str) -> "NodoCategoria | None":
        if self.nombre.lower() == nombre_buscado.lower():
            return self

        for sub in self.subcategorias:
            resultado = sub.buscar_categoria(nombre_buscado)
            if resultado is not None:
                return resultado

        return None

    def contar_elementos(self) -> int:
        total = len(self.elementos)
        for sub in self.subcategorias:
            total += sub.contar_elementos()
        return total

    def altura(self) -> int:
        if self.es_hoja():
            return 0
        return 1 + max(sub.altura() for sub in self.subcategorias)

    def listar_todos(self) -> list[Pelicula]:
        todos = list(self.elementos)
        for sub in self.subcategorias:
            todos.extend(sub.listar_todos())
        return todos


def construir_arbol_categorias() -> NodoCategoria:
    raiz = NodoCategoria("Catálogo de Películas")

    # --- Rama "Acción" ---
    accion = raiz.agregar_subcategoria("Acción")
    accion.agregar_subcategoria("Superhéroes")
    accion.agregar_subcategoria("Histórico")

    # --- Rama "Ciencia Ficción" ---
    ciencia_ficcion = raiz.agregar_subcategoria("Ciencia Ficción")
    ciencia_ficcion.agregar_subcategoria("Comedia")
    ciencia_ficcion.agregar_subcategoria("Aventura científica")
    ciencia_ficcion.agregar_subcategoria("Ciberpunk")
    ciencia_ficcion.agregar_subcategoria("Espacio")

    # --- Rama "Crimen" ---
    crimen = raiz.agregar_subcategoria("Crimen")
    crimen.agregar_subcategoria("Policial")
    crimen.agregar_subcategoria("Mafia")

    # --- Rama "Drama" ---
    drama = raiz.agregar_subcategoria("Drama")
    drama.agregar_subcategoria("Psicológico")
    drama.agregar_subcategoria("Social")
    drama.agregar_subcategoria("Histórico")

    # --- Rama "Terror" ---
    terror = raiz.agregar_subcategoria("Terror")
    terror.agregar_subcategoria("Psicológico")

    # --- Rama "Aventura" ---
    aventura = raiz.agregar_subcategoria("Aventura")
    aventura.agregar_subcategoria("Fantasía")

    # --- Rama "Animación" ---
    animacion = raiz.agregar_subcategoria("Animación")
    animacion.agregar_subcategoria("Fantasía")

    return raiz


def asignar_peliculas_a_categorias(raiz: NodoCategoria, catalogo: list):
    for pelicula in catalogo:
        cat_nombre = getattr(pelicula, "categoria", "") if hasattr(pelicula, "categoria") else pelicula.get("categoria", "")
        sub_nombre = getattr(pelicula, "subcategoria", "") if hasattr(pelicula, "subcategoria") else pelicula.get("subcategoria", "")

        nodo_padre = raiz.buscar_categoria(cat_nombre)
        if nodo_padre is None:
            nodo_padre = raiz.agregar_subcategoria(cat_nombre)

        if sub_nombre:
            nodo_hoja = nodo_padre.buscar_categoria(sub_nombre)
            if nodo_hoja is None:
                nodo_hoja = nodo_padre.agregar_subcategoria(sub_nombre)
            nodo_hoja.elementos.append(pelicula)
        else:
            nodo_padre.elementos.append(pelicula)


def cargar_peliculas_desde_json(ruta_archivo=None) -> list[Pelicula]:
    if ruta_archivo is None:
        posibles = [
            base_dir / "datos" / "Peliculas.json",
            base_dir / "datos" / "peliculas.json",
            Path("proyecto estructuras de datos/datos/Peliculas.json"),
            Path("datos/Peliculas.json"),
        ]
        for p in posibles:
            if p.exists():
                ruta_archivo = p
                break

    if ruta_archivo is None or not Path(ruta_archivo).exists():
        raise FileNotFoundError(f"No se encontró Peliculas.json en las rutas probadas.")

    with open(ruta_archivo, "r", encoding="utf-8") as archivo:
        datos = json.load(archivo)

    catalogo = []
    for item in datos:
        pelicula = Pelicula(
            item["codigo"],
            item["titulo"],
            item["categoria"],
            item.get("subcategoria", ""),
            item["director"],
            item["anio"],
            item["duracion"],
            item["stock"]
        )
        catalogo.append(pelicula)

    return catalogo


if __name__ == "__main__":
    print("=" * 70)
    print("  ÁRBOL GENERAL DE CATEGORÍAS - CATÁLOGO DE PELÍCULAS")
    print("=" * 70)

    arbol = construir_arbol_categorias()
    catalogo = cargar_peliculas_desde_json()
    print(f"✅ Se cargaron {len(catalogo)} películas desde el archivo JSON.")

    asignar_peliculas_a_categorias(arbol, catalogo)

    print("\n--- Estructura del Árbol (Recorrido Preorden) ---")
    arbol.mostrar()

    print("\n" + "=" * 70)
    print(f"• Altura del árbol: {arbol.altura()}")
    print(f"• Total de películas en el árbol: {arbol.contar_elementos()}")

