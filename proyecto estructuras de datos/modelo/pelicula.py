import json
from pathlib import Path

RUTA_peliculas = Path(__file__).resolve().parent.parent / "datos" / "peliculas.json"
RUTA_PELICULAS = Path(__file__).resolve().parent.parent / "datos" / "peliculas.json"


class Pelicula:
    def __init__(self, codigo, titulo, categoria, subcategoria, director, anio, duracion, stock):
        # Validaciones basicas antes de asignar
        if not codigo or not str(codigo).strip():
            raise ValueError("El codigo de la pelicula no puede estar vacio.")

        self.__codigo = str(codigo).strip()
        self.titulo = titulo           # usa el setter (valida)
        self.categoria = categoria     # usa el setter (valida)
        self.subcategoria = subcategoria  # usa el setter (permite vacio)
        self.director = director       # usa el setter (valida)
        self.anio = anio               # usa el setter (valida >= 1888)
        self.duracion = duracion       # usa el setter (valida > 0)
        self.stock = stock             # usa el setter (valida >= 0)

    # ---------- PROPIEDADES Y SETTERS ----------
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
        if not nuevo or not str(nuevo).strip():
            raise ValueError("El titulo no puede estar vacio.")
        self.__titulo = str(nuevo).strip()

    @property
    def categoria(self):
        return self.__categoria

    @categoria.setter
    def categoria(self, nueva):
        if not nueva or not str(nueva).strip():
            raise ValueError("La categoria no puede estar vacia.")
        self.__categoria = str(nueva).strip()

    @property
    def subcategoria(self):
        return self.__subcategoria

    @subcategoria.setter
    def subcategoria(self, nueva):
        # La subcategoria es opcional, puede estar vacia
        self.__subcategoria = str(nueva).strip() if nueva else ""

    @property
    def director(self):
        return self.__director

    @director.setter
    def director(self, nuevo):
        if not nuevo or not str(nuevo).strip():
            raise ValueError("El director no puede estar vacio.")
        self.__director = str(nuevo).strip()

    @property
    def anio(self):
        return self.__anio

    @anio.setter
    def anio(self, nuevo):
        if int(nuevo) < 1888:
            raise ValueError("El anio no es valido (debe ser >= 1888).")
        self.__anio = int(nuevo)

    @property
    def duracion(self):
        return self.__duracion

    @duracion.setter
    def duracion(self, nueva):
        if int(nueva) <= 0:
            raise ValueError("La duracion debe ser mayor a 0.")
        self.__duracion = int(nueva)

    @property
    def stock(self):
        return self.__stock

    @stock.setter
    def stock(self, nueva_cantidad):
        if int(nueva_cantidad) < 0:
            raise ValueError("El stock no puede ser negativo.")
        self.__stock = int(nueva_cantidad)

    # ---------- SERIALIZACION ----------

    def to_dict(self):
        """Convierte el objeto Pelicula en un diccionario para guardar en JSON."""
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
        """Crea un objeto Pelicula a partir de un diccionario (leido del JSON)."""
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

    # ---------- PERSISTENCIA ----------

    @classmethod
    def cargar_desde_json(cls, ruta=None):
        """Lee el archivo JSON y devuelve una lista de objetos Pelicula."""
        destino = Path(ruta) if ruta else RUTA_peliculas
        if not destino.exists():
            return []
        with open(destino, "r", encoding="utf-8") as f:
            datos = json.load(f)
        return [cls.from_dict(item) for item in datos]

    @classmethod
    def guardar_en_json(cls, lista_peliculas, ruta=None):
        """Guarda la lista completa de peliculas en el archivo JSON."""
        destino = Path(ruta) if ruta else RUTA_peliculas
        destino.parent.mkdir(parents=True, exist_ok=True)
        with open(destino, "w", encoding="utf-8") as f:
            json.dump([p.to_dict() for p in lista_peliculas], f, indent=4, ensure_ascii=False)

    # ---------- REPRESENTACION ----------

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
        return (f"[{self.__codigo}] {self.__titulo} ({self.__anio}) - "
                f"{self.__director} | {self.__categoria} ({self.__subcategoria}) | "
                f"Duracion: {self.__duracion} min | Stock: {self.__stock}")
