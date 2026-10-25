
class _NodoCola:
   

    def __init__(self, dato, siguiente=None):
        self.dato = dato
        self.siguiente = siguiente


class Cola:
   

    def __init__(self, maximo: int = 5):
       
        self._frente = None    # primer nodo (el más viejo)
        self._final = None     # último nodo (el más nuevo)
        self._tamanio = 0
        self._maximo = maximo

    def encolar(self, dato):
        
        nuevo_nodo = _NodoCola(dato)

        if self.esta_vacia():
            # Primer elemento: frente y final son el mismo
            self._frente = nuevo_nodo
            self._final = nuevo_nodo
        else:
            # El nodo actual del final apunta al nuevo
            self._final.siguiente = nuevo_nodo
            self._final = nuevo_nodo

        self._tamanio += 1

        # Si superamos el tamaño máximo permitido, descartamos el más viejo
        if self._tamanio > self._maximo:
            self.desencolar()

    def desencolar(self):
        """
        Saca y devuelve el elemento del frente (el más viejo).

        Returns:
            El dato del frente.

        Raises:
            IndexError: si la cola está vacía.
        """
        if self.esta_vacia():
            raise IndexError("No se puede desencolar: la cola está vacía.")

        dato = self._frente.dato
        self._frente = self._frente.siguiente  # el frente pasa al siguiente

        # Si la cola quedó vacía, el final también queda en None
        if self._frente is None:
            self._final = None

        self._tamanio -= 1
        return dato

    def esta_vacia(self) -> bool:
        """Devuelve True si la cola no tiene elementos."""
        return self._frente is None

    def tamanio(self) -> int:
        """Devuelve la cantidad de elementos actuales en la cola."""
        return self._tamanio

    def listar(self) -> list:
        """
        Devuelve todos los elementos de la cola en orden (del más viejo
        al más nuevo) SIN sacarlos.

        Returns:
            Lista con los datos de la cola.
        """
        elementos = []
        actual = self._frente
        while actual is not None:
            elementos.append(actual.dato)
            actual = actual.siguiente
        return elementos

    def __str__(self) -> str:
        """Representación visual de la cola (desde el frente hacia el final)."""
        elementos = self.listar()
        if not elementos:
            return "(cola vacía)"
        return " → ".join(str(e) for e in elementos)


# ====================================================================== #
#  Prueba interactiva del módulo Cola con películas                      #
# ====================================================================== #
if __name__ == "__main__":
    print("=" * 65)
    print("  ESTRUCTURA DE DATOS: COLA (FIFO) CON TAMAÑO MÁXIMO")
    print("=" * 65)

    # Creamos una cola para el historial de películas (máximo 5)
    historial = Cola(maximo=5)
    print(f"Estado inicial: {historial}")
    print(f"¿Está vacía?: {historial.esta_vacia()}\n")

    # 1. Encolamos 3 películas
    print("--- Agregando 3 películas al historial ---")
    historial.encolar("Volver al Futuro I")
    historial.encolar("Matrix")
    historial.encolar("El Padrino")
    print(f"Cola actual: {historial}")
    print(f"Cantidad actual: {historial.tamanio()} de {historial._maximo}\n")

    # 2. Encolamos más películas para superar el límite de 5
    print("--- Agregando 3 películas más (supera el límite de 5) ---")
    historial.encolar("Interestelar")
    historial.encolar("El Origen")
    print(f"Con 5 películas: {historial}")

    print("\nAgregamos una sexta: 'Gladiador'...")
    historial.encolar("Gladiador")
    print("¡Atención! Como el máximo es 5, se descartó automáticamente la más vieja ('Volver al Futuro I').")
    print(f"Cola actual: {historial}\n")

    # 3. Desencolar un elemento manualmente
    print("--- Desencolando el elemento más viejo ---")
    salio = historial.desencolar()
    print(f"Salió del frente: '{salio}'")
    print(f"Cola resultante: {historial}")
    print(f"Nuevo tamaño: {historial.tamanio()}")

