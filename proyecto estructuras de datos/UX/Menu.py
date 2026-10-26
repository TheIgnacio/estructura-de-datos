import sys
import json
from pathlib import Path

# Subimos dos niveles para llegar a la raíz del proyecto
base = Path(__file__).resolve().parent.parent
sys.path.append(str(base))

from modelo.pelicula import Pelicula

ruta = base / "datos" / "peliculas.json"


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
    
    # IMPORTANTE: Convertimos los objetos Pelicula a diccionarios antes de guardar
    lista_diccionarios = []
    for p in peliculas:
        lista_diccionarios.append({
            "codigo": p.codigo,
            "titulo": p.titulo,
            "categoria": p.categoria,
            "subcategoria": p.subcategoria,
            "director": p.director,
            "anio": p.anio,
            "duracion": p.duracion,
            "stock": p.stock
        })

    with open(ruta, "w", encoding="utf-8") as archivo:
        json.dump(lista_diccionarios, archivo, indent=4, ensure_ascii=False)


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
    
    try:
        opcion = int(input("Ingrese una opcion: "))
    except ValueError:
        print("\n[!] Debe ingresar un número válido.\n")
        continue

    if opcion == 1:
        print()
        print("--- Lista de peliculas ---")
        if not peliculas:
            print("No hay películas registradas.")
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
            comparaciones = 0
            
            for p in peliculas:
                comparaciones += 1
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
            comparaciones = 0

            for p in peliculas:
                comparaciones += 1
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
        cod = input("Ingrese codigo de la pelicula: ")
        if cod in [p.codigo for p in peliculas]:
            print("El codigo ya existe.")
            continue
        else:
            print("Codigo valido.")
            
        titulo = input("Ingrese titulo de la pelicula: ")
        categoria = input("Ingrese categoria de la pelicula: ")
        subcategoria = input("Ingrese subcategoria de la pelicula: ")
        director = input("Ingrese director de la pelicula: ")
        
        try:
            anio = int(input("Ingrese año de estreno de la pelicula: "))
            duracion = int(input("Ingrese duracion (en minutos): "))
            stock = int(input("Ingrese stock disponible: "))
        except ValueError:
            print("Año, duración y stock deben ser números enteros. Operación cancelada.")
            continue

        # Creamos el objeto, lo agregamos a la lista y guardamos
        nueva_pelicula = Pelicula(cod, titulo, categoria, subcategoria, director, anio, duracion, stock)
        peliculas.append(nueva_pelicula)
        guardar_peliculas(peliculas)
        print(f"¡Película '{titulo}' agregada y guardada con éxito!")
        print()

    elif opcion == 5:
        print()
        print("--- Eliminar pelicula ---")
        cod = input("Ingrese el codigo de la pelicula a eliminar: ")
        encontrada = False
        
        for i, p in enumerate(peliculas):
            if p.codigo == cod:
                peliculas.pop(i)
                guardar_peliculas(peliculas)
                print(f"Pelicula con codigo '{cod}' eliminada correctamente.")
                encontrada = True
                break
                
        if not encontrada:
            print("No se encontró ninguna película con ese código.")
        print()

    elif opcion == 6:
        print()
        print("--- Modificar pelicula ---")
        cod = input("Ingrese el codigo de la pelicula a modificar: ")
        encontrada = False
        
        for p in peliculas:
            if p.codigo == cod:
                encontrada = True
                print(f"Modificando a: {p.titulo}")
                print("Deje el campo vacío si no desea modificarlo.")
                
                nuevo_titulo = input(f"Nuevo titulo [{p.titulo}]: ")
                if nuevo_titulo:
                    p.titulo = nuevo_titulo
                    
                nueva_cat = input(f"Nueva categoria [{p.categoria}]: ")
                if nueva_cat:
                    p.categoria = nueva_cat
                    
                nueva_subcat = input(f"Nueva subcategoria [{p.subcategoria}]: ")
                if nueva_subcat:
                    p.subcategoria = nueva_subcat
                    
                nuevo_dir = input(f"Nuevo director [{p.director}]: ")
                if nuevo_dir:
                    p.director = nuevo_dir
                    
                nuevo_anio = input(f"Nuevo año [{p.anio}]: ")
                if nuevo_anio:
                    try:
                        p.anio = int(nuevo_anio)
                    except ValueError:
                        print("Valor inválido para el año, se mantiene el anterior.")
                        
                nueva_dur = input(f"Nueva duracion [{p.duracion}]: ")
                if nueva_dur:
                    try:
                        p.duracion = int(nueva_dur)
                    except ValueError:
                        print("Valor inválido para la duración, se mantiene la anterior.")
                        
                nuevo_stock = input(f"Nuevo stock [{p.stock}]: ")
                if nuevo_stock:
                    try:
                        p.stock = int(nuevo_stock)
                    except ValueError:
                        print("Valor inválido para el stock, se mantiene el anterior.")
                        
                guardar_peliculas(peliculas)
                print("¡Película modificada y guardada con éxito!")
                break
                
        if not encontrada:
            print("No se encontró ninguna película con ese código.")
        print()

    elif opcion == 0:
        print("Saliendo del sistema...")

    else:
        print("Opción no válida. Intente nuevamente.\n")