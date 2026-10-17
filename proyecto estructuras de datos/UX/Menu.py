import json
import sys
from pathlib import Path

base = Path(__file__).resolve().parent.parent
sys.path.append(str(base))
from modelo.pelicula import Pelicula

ruta = base /"datos"/"peliculas.json"


def cargar_peliculas():

    if not ruta.exists():
        return []
    try:
        with open(ruta, "r", encoding="utf-8") as archivo:
            datos = json.load(archivo)

            lista_peliculas = []
            for item in datos:
                p = Pelicula(
                    item["codigo"],
                    item["titulo"],
                    item["categoria"],
                    item["autor"],
                    item["anio"],
                    item["stock"]
                )
                lista_peliculas.append(p)
            return lista_peliculas
    except (json.JSONDecodeError, FileNotFoundError):
        return []

def guardar_peliculas(peliculas):

    ruta.parent.mkdir(parents=True, exist_ok=True)
    with open(ruta, "w", encoding = "utf-8") as archivo:
        json.dump(peliculas, archivo, indent=4, ensure_ascii=False) 

peliculas = cargar_peliculas()

def limpiar_texto(texto):
    texto = texto.lower()
    texto = texto.replace("á", "a")
    texto = texto.replace("é", "e")
    texto = texto.replace("í", "i")
    texto = texto.replace("ó", "o")
    texto = texto.replace("ú", "u")
    texto = texto.replace("ñ", "n")
    return texto


opcion = -1
while opcion != 0:

    print("1. Ver lista de Peliculas 1")
    print("2. Buscar por Categoria 2 ")
    print("3. Agregar Pelicula 3")
    print("4. Eliminar Pelicula 4")
    print("5. Modificar Pelicula 5")
    print()

    print("0. salir 0")
    opcion = int(input("Ingrese una opcion: "))

    if opcion == 1:
        print()
        print("--- Lista de peliculas ---")
        for p in peliculas:
            print(f"Codigo: [{p.codigo}], Titulo: {p.titulo}, Categoria: {p.categoria}, Autor: {p.autor}, Año: {p.anio}, Stock: {p.stock}")
        print()   
 
    
    elif opcion == 2:
        print()
        print("--- Lista de peliculas ---")
        categoria_buscar = input("Ingrese la categoria a buscar: ")
        categoria_buscar = limpiar_texto(categoria_buscar)
        if not categoria_buscar:
            print("La categoria no puede estar vacia")
        else:
            peliculas_encontradas = []
            for p in peliculas:
                if categoria_buscar in limpiar_texto(p.categoria):
                    peliculas_encontradas.append(p)
            print(f"Se encontraron {len(peliculas_encontradas)} peliculas en la categoria '{categoria_buscar}':")
            for p in peliculas_encontradas:
                print(f"Codigo: [{p.codigo}], Titulo: {p.titulo}, Autor: {p.autor}, Año: {p.anio}, Stock: {p.stock}")
        
        print()

    elif opcion == 3:
        print()
        print("--- Agregar pelicula ---")
        cod = input("Ingrese codigo de la pelicula")
        if cod in [p.codigo for p in peliculas]:
            print("El codigo ya existe")
            continue
        else:
            print("Codigo valido")
        titulo = input("ingrese titulo de la pelicula")
        categoria = input("ingrese categoria de la pelicula")
        autor = input("ingrese autor de la pelicula")
        try:
            anio = int(input("ingrese año de estreno de la pelicula"))
        except ValueError:
            print("El año debe ser un numero")
            continue
        stock = int(input("ingrese stock de la pelicula"))

        print()

    elif opcion == 4:
        print()
        print("pelicula eliminada")
        print()

    elif opcion == 5:
        print()
        print("Modificar pelicula")
        print()

    elif opcion == 0:
        print("salir")
        exit()

    else:
        print("opcion no valida")

        