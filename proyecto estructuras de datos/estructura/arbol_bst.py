"""
Módulo de Estructura de Datos: Árbol Binario de Búsqueda (BST)
Adaptado para el Catálogo de Películas del Proyecto Estructura de Datos 2026.
"""
from __future__ import annotations
import json
import sys
from pathlib import Path

# Asegurar que se pueda importar el modelo Pelicula desde cualquier punto
base_dir = Path(__file__).resolve().parent.parent
if str(base_dir) not in sys.path:
    sys.path.append(str(base_dir))

from modelo.pelicula import Pelicula


def _obtener_clave_elemento(elemento, clave: str):
    """Obtiene el valor de la clave ya sea desde un objeto Pelicula o un diccionario."""
    if hasattr(elemento, clave):
        return getattr(elemento, clave)
    elif isinstance(elemento, dict) and clave in elemento:
        return elemento[clave]
    else:
        raise AttributeError(f"El elemento no tiene la clave/atributo '{clave}'")


class NodoBST:
    """
    Un nodo del Árbol Binario de Búsqueda (BST).

    Atributos:
        clave (str): valor por el cual se ordena (ej. código o título de la película).
        elemento: el objeto Pelicula asociado a este nodo.
        izquierda (NodoBST | None): hijo izquierdo (claves menores).
        derecha (NodoBST | None): hijo derecho (claves mayores).
    """

    def __init__(self, clave: str, elemento: Pelicula):
        self.clave = clave
        self.elemento = elemento
        self.izquierda: NodoBST | None = None
        self.derecha: NodoBST | None = None

    # ------------------------------------------------------------------ #
    #  Inserción recursiva                                                #
    # ------------------------------------------------------------------ #

    def insertar(self, clave: str, elemento: Pelicula) -> "NodoBST":
        """
        Inserta un nuevo elemento respetando la regla de orden del BST.

        ¿CÓMO FUNCIONA?
            1. Si la clave es MENOR que la del nodo actual → va a la izquierda.
            2. Si la clave es MAYOR → va a la derecha.
            3. Si la clave es IGUAL → NO se inserta (claves únicas).

        Args:
            clave: la clave de la nueva película.
            elemento: el objeto Pelicula a insertar.

        Returns:
            Este mismo nodo (para facilitar la recursión).
        """
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
        """
        Busca una película por clave, contando las comparaciones realizadas.

        ¿POR QUÉ CONTAMOS COMPARACIONES?
            Para demostrar que el BST balanceado necesita menos pasos
            que la búsqueda secuencial o el BST degenerado.

        Args:
            clave: la clave a buscar (ej. 'MOV-014').
            comparaciones: acumulador (se incrementa en cada nodo visitado).

        Returns:
            Tupla (elemento, comparaciones) si la encuentra.
            Tupla (None, comparaciones) si no la encuentra.
        """
        comparaciones += 1  # cada nodo visitado es una comparación

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
        """
        Calcula la altura del subárbol desde este nodo.

        Altura de una hoja = 0.
        Altura de un nodo = 1 + max(altura izq, altura der).
        """
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
    """
    Recorrido INORDEN: izquierda → raíz → derecha.

    ¿POR QUÉ ES ÚTIL?
        En un BST, el recorrido inorden devuelve las películas
        ORDENADAS de menor a mayor. Es la forma de listar el catálogo
        en orden alfabético por código o título.

    Args:
        nodo: raíz del subárbol a recorrer.
        resultado: lista acumuladora (se crea nueva si no se pasa).

    Returns:
        Lista con los objetos Pelicula en orden.
    """
    if resultado is None:
        resultado = []
    if nodo is not None:
        inorden(nodo.izquierda, resultado)
        resultado.append(nodo.elemento)
        inorden(nodo.derecha, resultado)
    return resultado


def preorden(nodo: NodoBST | None, resultado: list = None) -> list:
    """
    Recorrido PREORDEN: raíz → izquierda → derecha.

    ¿PARA QUÉ SIRVE?
        Es útil para copiar o serializar la estructura del árbol,
        porque primero visita la raíz antes de descender.
    """
    if resultado is None:
        resultado = []
    if nodo is not None:
        resultado.append(nodo.elemento)
        preorden(nodo.izquierda, resultado)
        preorden(nodo.derecha, resultado)
    return resultado


def postorden(nodo: NodoBST | None, resultado: list = None) -> list:
    """
    Recorrido POSTORDEN: izquierda → derecha → raíz.

    ¿PARA QUÉ SIRVE?
        Es útil para eliminar un árbol, porque procesa los hijos
        antes que el padre (así no perdemos referencias).
    """
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
    """
    Construye un BST insertando las películas EN EL ORDEN en que vienen.

    ⚠️  CUIDADO: si el catálogo ya está ordenado por la clave (ej. MOV-001,
    MOV-002, MOV-003...), el árbol resultante será DEGENERADO (una cadena lineal)
    y la búsqueda será tan lenta como en una lista (O(n)).

    Esta función existe para DEMOSTRAR el problema. En el programa real
    se usa construir_bst_balanceado().

    Args:
        catalogo: lista de objetos Pelicula.
        clave: nombre del atributo a usar como clave (ej. "codigo" o "titulo").

    Returns:
        La raíz del BST, o None si el catálogo está vacío.
    """
    if not catalogo:
        return None

    # El primer elemento se convierte en la raíz
    primera_clave = _obtener_clave_elemento(catalogo[0], clave)
    raiz = NodoBST(primera_clave, catalogo[0])

    # Las demás se insertan una a una
    for pelicula in catalogo[1:]:
        val_clave = _obtener_clave_elemento(pelicula, clave)
        raiz.insertar(val_clave, pelicula)

    return raiz


def construir_bst_balanceado(catalogo: list, clave: str) -> NodoBST | None:
    """
    Construye un BST BALANCEADO a partir de un catálogo de películas.

    ¿CÓMO LO HACE?
        1. Ordena el catálogo por la clave.
        2. Toma el elemento del MEDIO como raíz.
        3. Recursivamente, toma el medio de la mitad izquierda (hijo izq)
           y el medio de la mitad derecha (hijo der).

    ¿POR QUÉ FUNCIONA?
        Al poner siempre el elemento del medio como raíz, cada subárbol
        tiene aproximadamente la misma cantidad de nodos a cada lado.
        Eso garantiza una altura de ~log2(n) en vez de n-1.

    Args:
        catalogo: lista de objetos Pelicula.
        clave: nombre del atributo a usar como clave (ej. "codigo" o "titulo").

    Returns:
        La raíz del BST balanceado, o None si el catálogo está vacío.
    """
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


def mostrar_arbol_visual(nodo: NodoBST | None, prefijo: str = "", es_izq: bool = True):
    """Visualización gráfica del árbol binario en consola."""
    if nodo is not None:
        if nodo.derecha:
            mostrar_arbol_visual(nodo.derecha, prefijo + ("│   " if es_izq else "    "), False)
        conector = "└── " if es_izq else "┌── "
        print(prefijo + conector + str(nodo.clave))
        if nodo.izquierda:
            mostrar_arbol_visual(nodo.izquierda, prefijo + ("    " if es_izq else "│   "), True)


# ====================================================================== #
#  Carga de datos y prueba de funcionamiento con Peliculas.json           #
# ====================================================================== #

def cargar_peliculas_desde_json(ruta_archivo=None) -> list[Pelicula]:
    """Carga los objetos Pelicula directamente desde el archivo JSON del proyecto."""
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
    print("  ÁRBOL BINARIO DE BÚSQUEDA (BST) - CATÁLOGO DE PELÍCULAS")
    print("=" * 70)

    # 1. Cargar las películas desde el JSON del proyecto
    catalogo = cargar_peliculas_desde_json()
    print(f"✅ Se cargaron {len(catalogo)} películas desde el archivo JSON.")

    # 2. Construir árbol normal (degenerado porque vienen en orden MOV-001 a MOV-040)
    bst_normal = construir_bst(catalogo, clave="codigo")
    print("\n--- Árbol BST Normal (Secuencial) ---")
    print(f"• Total de nodos: {bst_normal.contar_nodos()}")
    print(f"• Altura del árbol: {bst_normal.altura()} (¡Degenerado! O(n))")

    # 3. Construir árbol balanceado
    bst_balanceado = construir_bst_balanceado(catalogo, clave="codigo")
    print("\n--- Árbol BST Balanceado ---")
    print(f"• Total de nodos: {bst_balanceado.contar_nodos()}")
    print(f"• Altura del árbol: {bst_balanceado.altura()} (¡Óptimo! ~log2(40) ≈ 5)")

    # 4. Demostración de búsqueda: Comparaciones en Normal vs Balanceado
    clave_buscar = "MOV-035"
    print(f"\n" + "=" * 70)
    print(f"🔍 Búsqueda de '{clave_buscar}':")

    pelicula_norm, comp_norm = bst_normal.buscar(clave_buscar)
    pelicula_bal, comp_bal = bst_balanceado.buscar(clave_buscar)

    print(f"1. En BST Normal:      {comp_norm} comparaciones.")
    print(f"2. En BST Balanceado:  {comp_bal} comparaciones.")
    if pelicula_bal:
        print(f"Película encontrada: {pelicula_bal.titulo} ({pelicula_bal.anio}) - {pelicula_bal.categoria}")

    # 5. Demostración de recorrido Inorden
    print("\n" + "=" * 70)
    print("📋 Recorrido INORDEN (Primeras 5 películas ordenadas por código):")
    peliculas_ordenadas = inorden(bst_balanceado)
    for p in peliculas_ordenadas[:5]:
        print(f"   [{p.codigo}] {p.titulo} - {p.categoria}")

