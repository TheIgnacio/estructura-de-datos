import json
from pathlib import Path

RUTA_clientes = Path(__file__).resolve().parent.parent / "datos" / "clientes.json"



class Cliente:
    def __init__(self, nombre, apellido, dni, telefono, direccion, peliculas_reservadas=None):
        if not nombre or not nombre.strip():
            raise ValueError("El nombre del cliente no puede estar vacio")
        if not apellido or not apellido.strip():
            raise ValueError("El apellido del cliente no puede estar vacio")
        if not dni or not dni.strip():
            raise ValueError("El dni del cliente no puede estar vacio")
        if not telefono or not telefono.strip():
            raise ValueError("El telefono del cliente no puede estar vacio")
        if not direccion or not direccion.strip():
            raise ValueError("La direccion del cliente no puede estar vacio")

        self._nombre = nombre
        self._apellido = apellido
        self.dni = dni
        self.telefono = telefono
        self.direccion = direccion
        self.peliculas_reservadas = peliculas_reservadas if peliculas_reservadas is not None else []

    def datos_clientes (self):
        return f"Nombre: {self._nombre}, Apellido: {self._apellido}, DNI: {self.dni}, Telefono: {self.telefono}, Direccion: {self.direccion}"

    def agregar_reserva(self,codigo_pelicula):
        if codigo_pelicula not in self.peliculas_reservadas:
            self.peliculas_reservadas.append(codigo_pelicula)
            return ("Reserva Agregada con exito")
        else:
            return("El cliente ya tiene reservada esta pelicula")

    def eliminar_reserva(self,codigo_pelicula):
        if codigo_pelicula in self.peliculas_reservadas:
            self.peliculas_reservadas.remove(codigo_pelicula)
            return "Reserva eliminada correctamente."
        else: 
            return "No se encontro reserva para eliminar"
        
    def mostrar_reservas(self,dni):
        if self.dni == dni:
            return self.peliculas_reservadas
        else:
            return "No se encontraron reservas para el DNI proporcionado."


    def to_dict(self):
        return {"nombre" : self._nombre,
                "apellido" : self._apellido,
                "dni" : self.dni,
                "telefono": self.telefono,
                "direccion": self.direccion,
                "peliculas_reservadas" :self.peliculas_reservadas
        }

    @classmethod
    def from_dict(cls, datos: dict):
        """Crea un cliente a partir del diccionario .json"""
        return cls(
            nombre=datos["nombre"],
            apellido=datos["apellido"],
            dni=datos["dni"],
            telefono=datos["telefono"],
            direccion=datos["direccion"], 
            peliculas_reservadas=datos.get("peliculas_reservadas", [])
        )
    @classmethod
    def cargar_desde_json(cls,ruta=None):
        destino = Path(ruta) if ruta else RUTA_clientes
        with open(destino,"r", encoding="utf-8") as f:
            datos = json.load(f)
        return [cls.from_dict(item) for item in datos]

    