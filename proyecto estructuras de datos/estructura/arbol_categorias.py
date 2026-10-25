
from __future__ import annotations
import json
import sys
from pathlib import Path

# Permite importar desde la raíz del proyecto
base_dir = Path(__file__).resolve().parent.parent
if str(base_dir) not in sys.path:
    sys.path.append(str(base_dir))

from modelo.pelicula import Pelicula


class NodoCategoria:
    

    def __init__(self, nombre: str):
        """
        Crea un nodo de categoría vacío.

        Args:
            nombre: nombre de la categoría (ej. "Acción").
        """
        self.nombre = nombre
        self.subcategorias: list[NodoCategoria] = []   
        self.elementos: list[Pelicula] = []           

    # ------------------------------------------------------------------ #
    #  Operaciones sobre la estructura                                    #
    # ------------------------------------------------------------------ #

    def agregar_subcategoria(self, nombre_sub: str) -> "NodoCategoria":
       
        nuevo = NodoCategoria(nombre_sub)
        self.subcategorias.append(nuevo)
        return nuevo

    def es_hoja(self) -> bool:
      
        return len(self.subcategorias) == 0

    # ------------------------------------------------------------------ #
    #  Recorridos                                                         #
    # ------------------------------------------------------------------ #

    def mostrar(self, nivel: int = 0):
       
        # Indentación: 4 espacios por nivel
        prefijo = "    " * nivel
        # Símbolo visual según si es hoja o no
        marcador = "[HOJA] " if self.es_hoja() else "[CAT] "
        cantidad = len(self.elementos)
        print(f"{prefijo}{marcador} {self.nombre} ({cantidad} película/s)")

        # Llamada recursiva a cada hijo (recorrido preorden)
        for sub in self.subcategorias:
            sub.mostrar(nivel + 1)

    def buscar_categoria(self, nombre_buscado: str) -> "NodoCategoria | None":
       
        # Caso base: este nodo es el buscado
        if self.nombre.lower() == nombre_buscado.lower():
            return self

        # Caso recursivo: buscar en cada subárbol hijo
        for sub in self.subcategorias:
            resultado = sub.buscar_categoria(nombre_buscado)
            if resultado is not None:
                return resultado

        # No se encontró en ningún subárbol
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
      
        todos = list(self.elementos)  # copia de los propios
        for sub in self.subcategorias:
            todos.extend(sub.listar_todos())
        return todos


# ====================================================================== #
#  Funciones para armar la jerarquía completa del catálogo de películas  #
# ====================================================================== #

def construir_arbol_categorias() -> NodoCategoria:
    """
    Construye y devuelve el árbol de categorías del videoclub / catálogo de películas.

    Jerarquía:
        Catálogo de Películas
        ├── Acción
        │   ├── Superhéroes
        │   └── Histórico
        ├── Ciencia Ficción
        │   ├── Comedia
        │   ├── Aventura científica
        │   ├── Ciberpunk
        │   └── Espacio
        ├── Crimen
        │   ├── Policial
        │   └── Mafia
        ├── Drama
        │   ├── Psicológico
        │   ├── Social
        │   └── Histórico
        ├── Terror
        │   └── Psicológico
        ├── Aventura
        │   └── Fantasía
        └── Animación
            └── Fantasía

    Returns:
        NodoCategoria raíz ("Catálogo de Películas").
    """
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

        # 1. Buscamos la categoría principal bajo la raíz
        nodo_padre = raiz.buscar_categoria(cat_nombre)
        if nodo_padre is None:
            nodo_padre = raiz.agregar_subcategoria(cat_nombre)

        # 2. Si tiene subcategoría, buscamos la hoja dentro de esa categoría padre
        if sub_nombre:
            nodo_hoja = nodo_padre.buscar_categoria(sub_nombre)
            if nodo_hoja is None:
                nodo_hoja = nodo_padre.agregar_subcategoria(sub_nombre)
            nodo_hoja.elementos.append(pelicula)
        else:
            # Si no tiene subcategoría, la película se guarda en la categoría padre
            nodo_padre.elementos.append(pelicula)


# ====================================================================== #
#  Carga de datos y prueba interactiva                                   #
# ====================================================================== #

def cargar_peliculas_desde_json(ruta_archivo=None) -> list[Pelicula]:
    
    if ruta_archivo is None:
        posibles = [
            base_dir / "datos" / "Peliculas.json",
            base_dir / "datos" / "peliculas.json",
            Path("datos/Peliculas.json"),
            Path("proyecto estructuras de datos/datos/Peliculas.json"),
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

    # 1. Construir la estructura del árbol de categorías
    arbol = construir_arbol_categorias()

    # 2. Cargar las películas desde el JSON
    catalogo = cargar_peliculas_desde_json()
    print(f"✅ Se cargaron {len(catalogo)} películas desde el archivo JSON.")

    # 3. Asignar las películas a sus respectivas hojas
    asignar_peliculas_a_categorias(arbol, catalogo)

    # 4. Mostrar el árbol completo con sus cantidades
    print("\n--- Estructura del Árbol (Recorrido Preorden) ---")
    arbol.mostrar()

    # 5. Métricas del árbol
    print("\n" + "=" * 70)
    print(f"• Altura del árbol: {arbol.altura()}")
    print(f"• Total de películas en el árbol: {arbol.contar_elementos()}")

    # 6. Demostración de búsqueda por categoría intermedia
    # Al buscar "Ciencia Ficción", listar_todos() devuelve las películas de todas sus subcategorías
    print("\n" + "=" * 70)
    cat_buscar = "Ciencia Ficción"
    nodo_encontrado = arbol.buscar_categoria(cat_buscar)
    if nodo_encontrado:
        print(f"🔍 Películas dentro de la categoría '{cat_buscar}' (Total: {nodo_encontrado.contar_elementos()}):")
        for pel in nodo_encontrado.listar_todos():
            print(f"   • [{pel.codigo}] {pel.titulo} ({pel.subcategoria})")

    # 7. Demostración de búsqueda por subcategoría hoja
    sub_buscar = "Superhéroes"
    nodo_sub = arbol.buscar_categoria(sub_buscar)
    if nodo_sub:
        print(f"\n🔍 Películas dentro de la subcategoría hoja '{sub_buscar}' (Total: {len(nodo_sub.elementos)}):")
        for pel in nodo_sub.elementos:
            print(f"   • [{pel.codigo}] {pel.titulo} ({pel.anio}) - Dir: {pel.director}")

