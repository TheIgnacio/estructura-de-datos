class Pelicula:
    def __init__(self, codigo, titulo,categoria, autor, anio, stock):

        if not codigo or not codigo.strip():
            raise ValueError("El código de la película no puede estar vacío.")
        if not titulo or not titulo.strip():
            raise ValueError("El título de la película no puede estar vacío.")
        if stock < 0:
            raise ValueError("La cantidad no puede ser menor a 0.")

        self._codigo = codigo
        self._titulo = titulo
        self._categoria = categoria
        self._autor = autor
        self._anio = anio
        self._stock = stock

    @property
    def codigo(self):
        return self._codigo
    
    @property
    def titulo(self):
        return self._titulo

    @property
    def categoria(self):
        return self._categoria

    @property
    def autor(self):
        return self._autor

    @property
    def anio(self):
        return self._anio

    @property
    def stock(self):
        return self._stock

    @stock.setter
    def stock(self, nueva_cantidad: int):

        if nueva_cantidad < 0:
            raise ValueError("La cantidad no puede ser menor a 0.")     
        self._stock = nueva_cantidad