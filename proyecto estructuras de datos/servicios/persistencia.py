import sys
from pathlib import Path

# Sube un nivel (a la raíz del proyecto) para encontrar la carpeta 'modelo'
sys.path.append(str(Path(__file__).resolve().parent.parent))

import json
from modelo.clientes import Cliente

import json
from modelo.pelicula import  Pelicula


def cargar_clientes(ruta_archivo: str) -> list:
    with open(ruta_archivo, "r", encoding="utf-8") as archivo:
        datos = json.load(archivo)

    catalogo_clientes = []
    for item in datos:
        cliente = Cliente(
            item["nombre"],
            item["apellido"],
            item["dni"],
            item["telefono"],
            item["direccion"],
            item.get("peliculas_reservadas", [])
        )
        catalogo_clientes.append(cliente)

    return catalogo_clientes

def cargar_catalogo(ruta_archivo: str) -> list:
    with open(ruta_archivo, "r", encoding="utf-8") as archivo:
        datos = json.load(archivo)

    catalogo = []
    for item in datos:
        pelicula = Pelicula(
            titulo=item["titulo"],
            director=item["director"],
            anio=item["anio"],
            duracion=item["duracion"],
            stock=item["stock"],
            genero=item["genero"],
            disponible=item["disponible"]
        )
        catalogo.append(pelicula)

    return catalogo