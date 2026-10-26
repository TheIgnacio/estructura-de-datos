

class _NodoPila:

    def __init__(self, dato, siguiente=None):
        self.dato = dato
        self.siguiente = siguiente


class Pila:
  
    def __init__(self):
        """Crea una pila vacía."""
        self._tope = None     
        self._tamanio = 0    

    def apilar(self, dato):
       
        nuevo_nodo = _NodoPila(dato, self._tope)
        self._tope = nuevo_nodo
        self._tamanio += 1

    def desapilar(self):
        
        if self.esta_vacia():
            raise IndexError("No se puede desapilar: la pila está vacía.")

        dato = self._tope.dato
        self._tope = self._tope.siguiente  # el tope pasa a ser el de abajo
        self._tamanio -= 1
        return dato

    def ver_tope(self):
        
        if self.esta_vacia():
            raise IndexError("No se puede ver el tope: la pila está vacía.")
        return self._tope.dato

    def esta_vacia(self) -> bool:
        """Devuelve True si la pila no tiene elementos."""
        return self._tope is None

    def tamanio(self) -> int:
        """Devuelve la cantidad de elementos en la pila."""
        return self._tamanio

    def __str__(self) -> str:
        """Representación visual de la pila (desde el tope hacia la base)."""
        elementos = []
        actual = self._tope
        while actual is not None:
            elementos.append(str(actual.dato))
            actual = actual.siguiente
        return " → ".join(elementos) if elementos else "(pila vacía)"


# ====================================================================== #
#  Prueba interactiva del módulo Pila con películas                      #
# ====================================================================== #
if __name__ == "__main__":
    print("=" * 65)
    print("  ESTRUCTURA DE DATOS: PILA (LIFO - ÚLTIMO EN ENTRAR, PRIMERO EN SALIR)")
    print("=" * 65)

    pila = Pila()
    print(f"Estado inicial: {pila}")
    print(f"¿Está vacía?: {pila.esta_vacia()}\n")

    # 1. Apilar películas
    print("--- Apilando 3 películas ---")
    pila.apilar("Volver al Futuro I")
    print(f"Apilada: 'Volver al Futuro I'  | Tope actual: {pila.ver_tope()}")

    pila.apilar("Matrix")
    print(f"Apilada: 'Matrix'              | Tope actual: {pila.ver_tope()}")

    pila.apilar("El Origen")
    print(f"Apilada: 'El Origen'           | Tope actual: {pila.ver_tope()}")

    print(f"\nEstado actual de la pila (del tope a la base):")
    print(f"{pila}")
    print(f"Cantidad de elementos: {pila.tamanio()}\n")

    # 2. Consultar el tope sin sacarlo
    print(f"Película en el tope (sin sacar): '{pila.ver_tope()}'")
    print(f"La cantidad sigue siendo: {pila.tamanio()}\n")

    # 3. Desapilar elementos uno a uno
    print("--- Desapilando elementos (LIFO) ---")
    while not pila.esta_vacia():
        sacada = pila.desapilar()
        print(f"Desapilada: '{sacada}' | Restan: {pila.tamanio()} elemento/s | Pila: {pila}")

    print(f"\n¿Quedó vacía?: {pila.esta_vacia()}")

