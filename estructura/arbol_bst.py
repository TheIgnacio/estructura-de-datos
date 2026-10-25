
from __future__ import annotations
import json
import sys
from pathlib import Path

base_dir = Path(__file__).resolve().parent.parent / "proyecto estructuras de datos"
if str(base_dir) not in sys.path:
    sys.path.append(str(base_dir))

from modelo.pelicula import Pelicula


def _obtener_clave_elemento(elemento, clave: str):
    
    if hasattr(elemento, clave):
        return getattr(elemento, clave)
    elif isinstance(elemento, dict) and clave in elemento:
        return elemento[clave]
    else:
        raise AttributeError(f"El elemento no tiene la clave/atributo '{clave}'")


class NodoBST:
   

    def __init__(self, clave: str, elemento: Pelicula):
        self.clave = clave
        self.elemento = elemento
        self.izquierda: NodoBST | None = None
        self.derecha: NodoBST | None = None

    # ------------------------------------------------------------------ #
    #  Inserción recursiva                                                #
    # ------------------------------------------------------------------ #

    def insertar(self, clave: str, elemento: Pelicula) -> "NodoBST":
        
        if clave < self.clave:
            if self.izquierda is None:
                self.izquierda = NodoBST(clave, elemento)
            else:
                self.izquierda.insertar(clave, elemento)
        elif clave > self.clave:
            if self.derecha is None:
                self.derecha = NodoBST(clave, elemento)
            else:
                self.derecha.insertar(clave, elemento)
        # Si clave == self.clave, no hacemos nada (clave repetida)
        return self

    # ------------------------------------------------------------------ #
    #  Búsqueda con contador de comparaciones                            #
    # ------------------------------------------------------------------ #

    def buscar(self, clave: str, comparaciones: int = 0):
       
        comparaciones += 1  

        if clave == self.clave:
            return (self.elemento, comparaciones)
        elif clave < self.clave:
            if self.izquierda is None:
                return (None, comparaciones)
            return self.izquierda.buscar(clave, comparaciones)
        else:
            if self.derecha is None:
                return (None, comparaciones)
            return self.derecha.buscar(clave, comparaciones)

    # ------------------------------------------------------------------ #
    #  Métricas del árbol                                                 #
    # ------------------------------------------------------------------ #

    def altura(self) -> int:
       
        alt_izq = self.izquierda.altura() if self.izquierda else -1
        alt_der = self.derecha.altura() if self.derecha else -1
        return 1 + max(alt_izq, alt_der)

    def contar_nodos(self) -> int:
        """Cuenta el total de nodos en el subárbol."""
        total = 1
        if self.izquierda:
            total += self.izquierda.contar_nodos()
        if self.derecha:
            total += self.derecha.contar_nodos()
        return total


# ====================================================================== #
#  Recorridos del BST                                                     #
#                                                                          #
#  Son funciones SUELTAS (no métodos) porque operan sobre el árbol         #
#  entero, que puede ser None (árbol vacío).                               #
# ====================================================================== #

def inorden(nodo: NodoBST | None, resultado: list = None) -> list:
   
    if resultado is None:
        resultado = []
    if nodo is not None:
        inorden(nodo.izquierda, resultado)
        resultado.append(nodo.elemento)
        inorden(nodo.derecha, resultado)
    return resultado


def preorden(nodo: NodoBST | None, resultado: list = None) -> list:
  
    if resultado is None:
        resultado = []
    if nodo is not None:
        resultado.append(nodo.elemento)
        preorden(nodo.izquierda, resultado)
        preorden(nodo.derecha, resultado)
    return resultado


def postorden(nodo: NodoBST | None, resultado: list = None) -> list:
   
    if resultado is None:
        resultado = []
    if nodo is not None:
        postorden(nodo.izquierda, resultado)
        postorden(nodo.derecha, resultado)
        resultado.append(nodo.elemento)
    return resultado


# ====================================================================== #
#  Funciones de CONSTRUCCIÓN del BST                                       #
# ====================================================================== #

def construir_bst(catalogo: list, clave: str) -> NodoBST | None:
   
    if not catalogo:
        return None

   
    primera_clave = _obtener_clave_elemento(catalogo[0], clave)
    raiz = NodoBST(primera_clave, catalogo[0])

   
    for pelicula in catalogo[1:]:
        val_clave = _obtener_clave_elemento(pelicula, clave)
        raiz.insertar(val_clave, pelicula)

    return raiz


def construir_bst_balanceado(catalogo: list, clave: str) -> NodoBST | None:
   
    if not catalogo:
        return None

    # 1. Ordenar por la clave
    ordenado = sorted(catalogo, key=lambda p: _obtener_clave_elemento(p, clave))

    # 2. Construir recursivamente insertando siempre el del medio
    def _construir_recursivo(lista: list) -> NodoBST | None:
        """Función interna recursiva que arma el BST balanceado."""
        if not lista:
            return None

        medio = len(lista) // 2
        pelicula_medio = lista[medio]
        val_clave = _obtener_clave_elemento(pelicula_medio, clave)

        nodo = NodoBST(val_clave, pelicula_medio)
        nodo.izquierda = _construir_recursivo(lista[:medio])
        nodo.derecha = _construir_recursivo(lista[medio + 1:])

        return nodo

    return _construir_recursivo(ordenado)


def cargar_peliculas_desde_json(ruta_archivo=None) -> list[Pelicula]:
    """Carga los objetos Pelicula directamente desde el archivo JSON del proyecto."""
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
    print("  ÁRBOL BINARIO DE BÚSQUEDA (BST) - CATÁLOGO DE PELÍCULAS")
    print("=" * 70)

    # 1. Cargar las películas desde el JSON del proyecto
    catalogo = cargar_peliculas_desde_json()
    print(f"Se cargaron {len(catalogo)} películas desde el archivo JSON.")

    # 2. Construir árbol normal (degenerado)
    bst_normal = construir_bst(catalogo, clave="codigo")
    print("\n--- Árbol BST Normal (Secuencial) ---")
    print(f"Total de nodos: {bst_normal.contar_nodos()}")
    print(f"Altura del árbol: {bst_normal.altura()} (¡Degenerado! O(n))")

    # 3. Construir árbol balanceado
    bst_balanceado = construir_bst_balanceado(catalogo, clave="codigo")
    print("\n--- Árbol BST Balanceado ---")
    print(f"Total de nodos: {bst_balanceado.contar_nodos()}")
    print(f"Altura del árbol: {bst_balanceado.altura()} (¡Óptimo! ~log2(40) ≈ 5)")

    # 4. Demostración de búsqueda: Comparaciones en Normal vs Balanceado
    clave_buscar = "MOV-035"
    print(f"\n" + "=" * 70)
    print(f"Búsqueda de '{clave_buscar}':")

    pelicula_norm, comp_norm = bst_normal.buscar(clave_buscar)
    pelicula_bal, comp_bal = bst_balanceado.buscar(clave_buscar)

    print(f"1. En BST Normal:      {comp_norm} comparaciones.")
    print(f"2. En BST Balanceado:  {comp_bal} comparaciones.")
    if pelicula_bal:
        print(f"Película encontrada: {pelicula_bal.titulo} ({pelicula_bal.anio}) - {pelicula_bal.categoria}")

    # 5. Demostración de recorrido Inorden
    print("\n" + "=" * 70)
    print("Recorrido INORDEN (Primeras 5 películas ordenadas por código):")
    peliculas_ordenadas = inorden(bst_balanceado)
    for p in peliculas_ordenadas[:5]:
        print(f"   [{p.codigo}] {p.titulo} - {p.categoria}")

