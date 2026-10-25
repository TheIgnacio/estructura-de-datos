import json
from pathlib import Path

RUTA_PELICULAS = Path(__file__).resolve().parent.parent / "datos" / "peliculas.json"


class Pelicula:
    def __init__(self, codigo, titulo, categoria, subcategoria, director, anio, duracion, stock):

        if not codigo or not codigo.strip():
            raise ValueError("El código de la película no puede estar vacío.")

        if not titulo or not titulo.strip():
            raise ValueError ("El titulo de la pelicula no puede estar vacio")

        if not categoria or not categoria.strip():
            raise ValueError("La categoria de la pelicula no puede estar vacia")

        if not subcategoria or not subcategoria.strip():
            raise ValueError ("La subcategoria no puede estar vacia")

        if not director or not director.strip():
            raise ValueError("El director no puede estar vacio")

        if not anio or not str(anio).isdigit():
            raise ValueError ("El año tiene que ser en digitos.")

        if not duracion or not str(duracion).isdigit():
            raise ValueError ("La duracion tiene que ser en digitos y no numeros negativos.")

        if int(stock) < 0:
            raise ValueError ("El stock no tiene que ser menor a 0 y tiene que escribirse el digito")


        self.__codigo = codigo
        self.titulo = titulo

        self.categoria = categoria
        self.subcategoria = subcategoria
        self.director = director
        self.anio = anio
        self.duracion = duracion
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
    def subcategoria(self):
        return self.__subcategoria

    @subcategoria.setter
    def subcategoria(self, nueva):
        if not nueva or not nueva.strip():
            raise ValueError("La subcategoria no puede estar vacia.")
        self.__subcategoria = nueva

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
    def duracion(self):
        return self.__duracion

    @duracion.setter
    def duracion(self, nueva):
        if nueva <= 0:
            raise ValueError("La duración no es valida.")
        self.__duracion = nueva

    @property
    def stock(self):
        return self.__stock

    @stock.setter
    def stock(self, nueva_cantidad):
        if nueva_cantidad < 0:
            raise ValueError("La cantidad no puede ser menor a 0.")     
        self.__stock = nueva_cantidad 

    def to_dict(self):
        """Convierte este objeto película en un diccionario para JSON."""
        return {
            "codigo": self.codigo,
            "titulo": self.titulo,
            "categoria": self.categoria,
            "subcategoria": self.subcategoria,
            "director": self.director,
            "anio": self.anio,
            "duracion": self.duracion,
            "stock": self.stock
        }

    @classmethod
    def from_dict(cls, datos: dict):
        """Crea una película a partir de un diccionario del JSON."""
        return cls(
            codigo=datos["codigo"],
            titulo=datos["titulo"],
            categoria=datos["categoria"],
            subcategoria=datos.get("subcategoria", ""),
            director=datos["director"],
            anio=datos["anio"],
            duracion=datos.get("duracion", 120),
            stock=datos["stock"]
        )

    def guardar_pelicula(self, ruta=None):
        """Guarda esta película en el archivo JSON (si ya existe la actualiza, si no la agrega)."""
        destino = Path(ruta) if ruta else RUTA_PELICULAS
        destino.parent.mkdir(parents=True, exist_ok=True)

        datos = []
        if destino.exists():
            try:
                with open(destino, "r", encoding="utf-8") as f:
                    datos = json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                datos = []

        # Si ya existe por código la actualiza; si no, la agrega
        encontrada = False
        for i, item in enumerate(datos):
            if item.get("codigo") == self.codigo:
                datos[i] = self.to_dict()
                encontrada = True
                break
        if not encontrada:
            datos.append(self.to_dict())

        with open(destino, "w", encoding="utf-8") as f:
            json.dump(datos, f, indent=4, ensure_ascii=False)

    @classmethod
    def cargar_desde_json(cls, ruta=None):
        """Lee el archivo JSON y crea una lista de objetos Pelicula usando from_dict."""
        destino = Path(ruta) if ruta else RUTA_PELICULAS
        with open(destino, "r", encoding="utf-8") as f:
            datos = json.load(f)
        return [cls.from_dict(item) for item in datos]

    def __str__(self):
        return (f"[{self.codigo}] {self.titulo} ({self.anio}) - "
                f"{self.director} | {self.categoria} ({self.subcategoria}) | Duración: {self.duracion} min | Stock: {self.stock}")
                