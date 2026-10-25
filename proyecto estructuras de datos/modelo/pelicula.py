import json
from pathlib import Path

RUTA_peliculas = Path(__file__).resolve().parent.parent / "datos" / "peliculas.json"


class Pelicula:
    def __init__(self, codigo, titulo, categoria, subcategoria, director, anio, duracion, stock):
        if not codigo or not codigo.strip():
            raise ValueError("El codigo de la pelicula no puede estar vacio.")

        self.__codigo = codigo
        self.titulo = titulo
        self.categoria = categoria
        self.subcategoria = subcategoria   # permite cadena vacia
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
        # La subcategoria puede estar vacia, no es obligatoria
        self.__subcategoria = nueva if nueva else ""

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
        if int(nuevo) < 1888:
            raise ValueError("El anio no es valido.")
        self.__anio = int(nuevo)

    @property
    def duracion(self):
        return self.__duracion

    @duracion.setter
    def duracion(self, nueva):
        if int(nueva) <= 0:
            raise ValueError("La duracion no es valida.")
        self.__duracion = int(nueva)

    @property
    def stock(self):
        return self.__stock

    @stock.setter
    def stock(self, nueva_cantidad):
        if int(nueva_cantidad) < 0:
            raise ValueError("La cantidad no puede ser menor a 0.")
        self.__stock = int(nueva_cantidad)

    def to_dict(self):
        return {
            "codigo": self.__codigo,
            "titulo": self.__titulo,
            "categoria": self.__categoria,
            "subcategoria": self.__subcategoria,
            "director": self.__director,
            "anio": self.__anio,
            "duracion": self.__duracion,
            "stock": self.__stock
        }

    @classmethod
    def from_dict(cls, datos: dict):
        """Crea una Pelicula a partir de un diccionario (leido del .json)"""
        return cls(
            codigo=datos["codigo"],
            titulo=datos["titulo"],
            categoria=datos["categoria"],
            subcategoria=datos.get("subcategoria", ""),
            director=datos["director"],
            anio=datos["anio"],
            duracion=datos["duracion"],
            stock=datos["stock"]
        )

    @classmethod
    def cargar_desde_json(cls, ruta=None):
        destino = Path(ruta) if ruta else RUTA_peliculas
        if not destino.exists():
            return []
        with open(destino, "r", encoding="utf-8") as f:
            datos = json.load(f)
        return [cls.from_dict(item) for item in datos]

    @classmethod
    def guardar_en_json(cls, lista_peliculas, ruta=None):
        destino = Path(ruta) if ruta else RUTA_peliculas
        destino.parent.mkdir(parents=True, exist_ok=True)
        with open(destino, "w", encoding="utf-8") as f:
            json.dump([p.to_dict() for p in lista_peliculas], f, indent=4, ensure_ascii=False)

    def __str__(self):
        return (f"[{self.codigo}] {self.titulo} ({self.anio}) - "
                f"{self.director} | {self.categoria} ({self.subcategoria}) | "
                f"Duracion: {self.duracion} min | Stock: {self.stock}")
