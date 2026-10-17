class Pelicula:
    def __init__(self, codigo, titulo,categoria, director, anio, stock):

        if not codigo or not codigo.strip():
            raise ValueError("El código de la película no puede estar vacío.")

        self.__codigo = codigo
        self.titulo = titulo
        self.categoria = categoria
        self.director = director
        self.anio = anio
        self.stock = stock

    @property
    def codigo(self):
        return self.__codigo
    
    @property
    def titulo(self):
        return self.__titulo 
    
    @titulo.setter
    def titulo(self, nuevo):
        if not nuevo or not nuevo.strip():
            raise ValueError("El titulo no puede estar vacio.")
        self.__titulo = nuevo

    @property
    def categoria(self):
        return self.__categoria

    @categoria.setter
    def categoria(self, nueva):
        if not nueva or not nueva.strip():
            raise ValueError("La categoria no puede estar vacia.")
        self.__categoria = nueva

    @property
    def director(self):
        return self.__director 

    @director.setter
    def director(self, nuevo):
        if not nuevo or not nuevo.strip():
            raise ValueError("El director no puede estar vacio.")
        self.__director = nuevo

    @property
    def anio(self):
        return self.__anio

    @anio.setter
    def anio(self, nuevo):
        if nuevo < 1888:
            raise ValueError("El año no es valido.")
        self.__anio = nuevo

    @property
    def stock(self):
        return self.__stock

    @stock.setter
    def stock(self, nueva_cantidad):
        if nueva_cantidad < 0:
            raise ValueError("La cantidad no puede ser menor a 0.")     
        self.__stock = nueva_cantidad 

    def __str__(self):
        return(f"[{self.codigo}] {self.titulo} ({self.anio}) -"
         f"{self.director} | {self.categoria} | Stock: {self.stock}")