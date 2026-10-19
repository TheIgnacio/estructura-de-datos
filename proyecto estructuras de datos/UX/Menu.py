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
                    item.get("subcategoria", ""),
                    item["director"],
                    item["anio"],
                    item["duracion"],
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

    print("1. Ver lista de Peliculas")
    print("2. Buscar por Categoria")
    print("3. Buscar por Titulo")
    print("4. Agregar Pelicula")
    print("5. Eliminar Pelicula")
    print("6. Modificar Pelicula")
    print()

    print("0. Salir")
    opcion = int(input("Ingrese una opcion: "))

    if opcion == 1:
        print()
        print("--- Lista de peliculas ---")
        for p in peliculas:
            print(f"Codigo: [{p.codigo}], Titulo: {p.titulo}, Categoria: {p.categoria}, Subcategoria: {p.subcategoria}, Director: {p.director}, Año: {p.anio}, Duracion: {p.duracion}, Stock: {p.stock}")
        print()   
 
    
    elif opcion == 2:
        print()
        print("--- Buscar por categoria ---")
        categoria_buscar = input("Ingrese la categoria a buscar: ")
        categoria_buscar = limpiar_texto(categoria_buscar)
        if not categoria_buscar:
            print("La categoria no puede estar vacia")
        else:
            peliculas_encontradas = []
            comparaciones = 0   #Inicia contador de comparaciones
            
            for p in peliculas:
                comparaciones += 1 #Se cuenta cada comparacion realizada
                if categoria_buscar in limpiar_texto(p.categoria):
                    peliculas_encontradas.append(p)
            print(f"Se encontraron {len(peliculas_encontradas)} peliculas en la categoria '{categoria_buscar}':")
            for p in peliculas_encontradas:
                print(f"Codigo: [{p.codigo}], Titulo: {p.titulo}, Categoria: {p.categoria}, Subcategoria: {p.subcategoria}, Director: {p.director}, Año: {p.anio}, Duracion: {p.duracion}, Stock: {p.stock}")
            print(f"Comparaciones realizadas: {comparaciones}")
        print()


    elif opcion == 3:
        print()
        print("--- Buscar por titulo ---")
        titulo_buscar = input("Ingrese el titulo a buscar: ")
        titulo_buscar = limpiar_texto(titulo_buscar)
        if not titulo_buscar:
            print("El titulo no puede estar vacio")
        else:
            peliculas_encontradas = []
            comparaciones = 0   #Inicia contador de comparaciones

            for p in peliculas:
                comparaciones += 1 #Se cuenta cada comparacion realizada
                if titulo_buscar in limpiar_texto(p.titulo):
                    peliculas_encontradas.append(p)
            print(f"Se encontraron {len(peliculas_encontradas)} peliculas con el titulo '{titulo_buscar}':")
            for p in peliculas_encontradas:
                print(f"Codigo: [{p.codigo}], Titulo: {p.titulo}, Categoria: {p.categoria}, Subcategoria: {p.subcategoria}, Director: {p.director}, Año: {p.anio}, Duracion: {p.duracion}, Stock: {p.stock}")
            print(f"Comparaciones realizadas: {comparaciones}")
        print()

    elif opcion == 4:
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
        subcategoria = input("ingrese subcategoria de la pelicula")
        autor = input("ingrese autor de la pelicula")
        try:
            anio = int(input("ingrese año de estreno de la pelicula"))
        except ValueError:
            print("El año debe ser un numero")
            continue
        duracion = int(input("ingrese duracion de la pelicula"))
        stock = int(input("ingrese stock de la pelicula"))

        print()

    elif opcion == 5:
        print()
        print("pelicula eliminada")
        print()

    elif opcion == 6:
        print()
        print("Modificar pelicula")
        print()

    elif opcion == 0:
        print("salir")
        exit()

    else:
        print("opcion no valida")

        