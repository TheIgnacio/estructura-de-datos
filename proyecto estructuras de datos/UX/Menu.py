import sys
from pathlib import Path

# Agrega la raiz del proyecto al path para que los imports funcionen
base = Path(__file__).resolve().parent.parent
sys.path.append(str(base))

from modelo.pelicula import Pelicula
from modelo.clientes import Cliente

# ---------------------------------------------------------------
# Carga inicial: las clases ya saben leer su propio JSON
# ---------------------------------------------------------------
peliculas = Pelicula.cargar_desde_json()
clientes = Cliente.cargar_desde_json()


def limpiar_texto(texto):
    """Convierte a minusculas y saca tildes para busquedas."""
    texto = texto.lower()
    for original, reemplazo in {"á":"a","é":"e","í":"i","ó":"o","ú":"u","ñ":"n"}.items():
        texto = texto.replace(original, reemplazo)
    return texto


# ---------------------------------------------------------------
# Loop principal del menu
# ---------------------------------------------------------------
opcion = -1
while opcion != 0:

    print("=" * 42)
    print("       VIDEOCLUB - MENU PRINCIPAL")
    print("=" * 42)
    print("  1. Ver lista de Peliculas")
    print("  2. Buscar por Categoria")
    print("  3. Buscar por Titulo")
    print("  4. Agregar Pelicula")
    print("  5. Eliminar Pelicula")
    print("  6. Modificar Pelicula")
    print("  7. Eliminar Cliente")
    print()
    print("  0. Salir")
    print("=" * 42)

    try:
        opcion = int(input("Ingrese una opcion: "))
    except ValueError:
        print("Por favor ingrese un numero valido.")
        opcion = -1
        continue

    # ------------------------------------------------------------------
    # Opcion 1: Ver todas las peliculas
    # ------------------------------------------------------------------
    if opcion == 1:
        print()
        print("--- Lista de peliculas ---")
        if not peliculas:
            print("No hay peliculas cargadas.")
        else:
            for p in peliculas:
                print(p)   # usa __str__ de Pelicula
        print()

    # ------------------------------------------------------------------
    # Opcion 2: Buscar por categoria
    # ------------------------------------------------------------------
    elif opcion == 2:
        print()
        print("--- Buscar por categoria ---")
        categoria_buscar = input("Ingrese la categoria a buscar: ").strip()
        if not categoria_buscar:
            print("La categoria no puede estar vacia.")
        else:
            categoria_buscar = limpiar_texto(categoria_buscar)
            encontradas = []
            comparaciones = 0
            for p in peliculas:
                comparaciones += 1
                if categoria_buscar in limpiar_texto(p.categoria):
                    encontradas.append(p)
            print(f"Se encontraron {len(encontradas)} pelicula(s) en '{categoria_buscar}':")
            for p in encontradas:
                print(f"  {p}")
            print(f"Comparaciones realizadas: {comparaciones}")
        print()

    # ------------------------------------------------------------------
    # Opcion 3: Buscar por titulo
    # ------------------------------------------------------------------
    elif opcion == 3:
        print()
        print("--- Buscar por titulo ---")
        titulo_buscar = input("Ingrese el titulo a buscar: ").strip()
        if not titulo_buscar:
            print("El titulo no puede estar vacio.")
        else:
            titulo_buscar = limpiar_texto(titulo_buscar)
            encontradas = []
            comparaciones = 0
            for p in peliculas:
                comparaciones += 1
                if titulo_buscar in limpiar_texto(p.titulo):
                    encontradas.append(p)
            print(f"Se encontraron {len(encontradas)} pelicula(s) con '{titulo_buscar}':")
            for p in encontradas:
                print(f"  {p}")
            print(f"Comparaciones realizadas: {comparaciones}")
        print()

    # ------------------------------------------------------------------
    # Opcion 4: Agregar pelicula
    # ------------------------------------------------------------------
    elif opcion == 4:
        print()
        print("--- Agregar pelicula ---")
        cod = input("Codigo (ej: MOV-041): ").strip()
        if not cod:
            print("El codigo no puede estar vacio.")
            continue
        if any(p.codigo == cod for p in peliculas):
            print("Ese codigo ya existe. No se puede duplicar.")
            continue

        titulo = input("Titulo: ").strip()
        categoria = input("Categoria: ").strip()
        subcategoria = input("Subcategoria (Enter para dejar vacio): ").strip()
        director = input("Director: ").strip()

        try:
            anio = int(input("Anio de estreno: "))
            duracion = int(input("Duracion en minutos: "))
            stock = int(input("Stock disponible: "))
        except ValueError:
            print("Anio, duracion y stock deben ser numeros enteros.")
            continue

        try:
            nueva = Pelicula(cod, titulo, categoria, subcategoria, director, anio, duracion, stock)
            peliculas.append(nueva)
            Pelicula.guardar_en_json(peliculas)
            print(f"[OK] '{titulo}' agregada y guardada correctamente.")
        except ValueError as e:
            print(f"Error al crear la pelicula: {e}")
        print()

    # ------------------------------------------------------------------
    # Opcion 5: Eliminar pelicula
    # ------------------------------------------------------------------
    elif opcion == 5:
        print()
        print("--- Eliminar pelicula ---")
        cod = input("Codigo de la pelicula a eliminar: ").strip()

        pelicula_encontrada = None
        for p in peliculas:
            if p.codigo == cod:
                pelicula_encontrada = p
                break

        if pelicula_encontrada is None:
            print("No se encontro ninguna pelicula con ese codigo.")
        else:
            print(f"Pelicula encontrada: {pelicula_encontrada}")
            confirmacion = input("Confirma la eliminacion? (s/n): ").strip().lower()
            if confirmacion == "s":
                peliculas.remove(pelicula_encontrada)
                Pelicula.guardar_en_json(peliculas)
                print("[OK] Pelicula eliminada correctamente.")
            else:
                print("Operacion cancelada.")
        print()

    # ------------------------------------------------------------------
    # Opcion 6: Modificar pelicula
    # ------------------------------------------------------------------
    elif opcion == 6:
        print()
        print("--- Modificar pelicula ---")
        cod = input("Codigo de la pelicula a modificar: ").strip()

        pelicula_encontrada = None
        for p in peliculas:
            if p.codigo == cod:
                pelicula_encontrada = p
                break

        if pelicula_encontrada is None:
            print("No se encontro ninguna pelicula con ese codigo.")
        else:
            print(f"Pelicula encontrada: {pelicula_encontrada}")
            print("Que campo desea modificar?")
            print("  1. Titulo      2. Categoria   3. Subcategoria")
            print("  4. Director    5. Anio        6. Duracion     7. Stock")
            try:
                campo = int(input("Numero del campo: "))
                if campo == 1:
                    pelicula_encontrada.titulo = input("Nuevo titulo: ").strip()
                elif campo == 2:
                    pelicula_encontrada.categoria = input("Nueva categoria: ").strip()
                elif campo == 3:
                    pelicula_encontrada.subcategoria = input("Nueva subcategoria: ").strip()
                elif campo == 4:
                    pelicula_encontrada.director = input("Nuevo director: ").strip()
                elif campo == 5:
                    pelicula_encontrada.anio = int(input("Nuevo anio: "))
                elif campo == 6:
                    pelicula_encontrada.duracion = int(input("Nueva duracion en minutos: "))
                elif campo == 7:
                    pelicula_encontrada.stock = int(input("Nuevo stock: "))
                else:
                    print("Opcion de campo no valida.")
                    continue
                Pelicula.guardar_en_json(peliculas)
                print("[OK] Pelicula modificada y guardada.")
            except ValueError as e:
                print(f"Error: {e}")
        print()

    # ------------------------------------------------------------------
    # Opcion 7: Eliminar cliente
    # ------------------------------------------------------------------
    elif opcion == 7:
        print()
        print("--- Eliminar Cliente ---")
        dni_buscar = input("DNI del cliente a eliminar (sin puntos): ").strip()

        cliente_encontrado = None
        for c in clientes:
            if c.dni == dni_buscar:
                cliente_encontrado = c
                break

        if cliente_encontrado is None:
            print("No se encontro ningun cliente con ese DNI.")
        else:
            print(f"Cliente encontrado: {cliente_encontrado.datos_clientes()}")
            confirmacion = input("Confirma la eliminacion? (s/n): ").strip().lower()
            if confirmacion == "s":
                clientes.remove(cliente_encontrado)
                Cliente.guardar_en_json(clientes)
                print("[OK] Cliente eliminado correctamente.")
            else:
                print("Operacion cancelada. No se borraron datos.")
        print()

    # ------------------------------------------------------------------
    elif opcion == 0:
        print("Hasta luego!")

    else:
        print("Opcion no valida. Intente de nuevo.")
