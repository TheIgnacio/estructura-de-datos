import sys
from pathlib import Path

# Permite importar desde la raiz del proyecto
base = Path(__file__).resolve().parent.parent
if str(base) not in sys.path:
    sys.path.append(str(base))

from modelo.pelicula import Pelicula
from modelo.clientes import Cliente

# ---------------------------------------------------------------
# Carga inicial usando metodos de las clases
# ---------------------------------------------------------------
peliculas = Pelicula.cargar_desde_json()
clientes = Cliente.cargar_desde_json()


def limpiar_texto(texto):
    """Normaliza texto: minusculas y sin tildes para busquedas."""
    texto = texto.lower()
    reemplazos = {"á": "a", "é": "e", "í": "i", "ó": "o", "ú": "u", "ñ": "n"}
    for orig, reemplazo in reemplazos.items():
        texto = texto.replace(orig, reemplazo)
    return texto


# ---------------------------------------------------------------
# Loop principal del menu
# ---------------------------------------------------------------
opcion = -1
while opcion != 0:
    print("=" * 45)
    print("       VIDEOCLUB - MENU PRINCIPAL")
    print("=" * 45)
    print("  1. Ver lista de Peliculas")
    print("  2. Buscar por Categoria")
    print("  3. Buscar por Titulo")
    print("  4. Agregar Pelicula")
    print("  5. Eliminar Pelicula")
    print("  6. Modificar Pelicula")
    print("  7. Eliminar Cliente")
    print()
    print("  0. Salir")
    print("=" * 45)

    try:
        opcion = int(input("Ingrese una opcion: "))
    except ValueError:
        print("\n[!] Debe ingresar un numero valido.\n")
        opcion = -1
        continue

    # ------------------------------------------------------------------
    # 1. Ver lista de peliculas
    # ------------------------------------------------------------------
    if opcion == 1:
        print("\n--- Lista de Peliculas ---")
        if not peliculas:
            print("No hay peliculas registradas.")
        else:
            for p in peliculas:
                print(p)
        print()

    # ------------------------------------------------------------------
    # 2. Buscar por categoria
    # ------------------------------------------------------------------
    elif opcion == 2:
        print("\n--- Buscar por Categoria ---")
        cat_buscar = input("Ingrese la categoria a buscar: ").strip()
        if not cat_buscar:
            print("La categoria no puede estar vacia.")
        else:
            cat_limpia = limpiar_texto(cat_buscar)
            encontradas = []
            comparaciones = 0
            for p in peliculas:
                comparaciones += 1
                if cat_limpia in limpiar_texto(p.categoria) or (p.subcategoria and cat_limpia in limpiar_texto(p.subcategoria)):
                    encontradas.append(p)

            print(f"Se encontraron {len(encontradas)} pelicula(s) asociadas a '{cat_buscar}':")
            for p in encontradas:
                print(f"  {p}")
            print(f"Comparaciones realizadas: {comparaciones}")
        print()

    # ------------------------------------------------------------------
    # 3. Buscar por titulo
    # ------------------------------------------------------------------
    elif opcion == 3:
        print("\n--- Buscar por Titulo ---")
        tit_buscar = input("Ingrese el titulo a buscar: ").strip()
        if not tit_buscar:
            print("El titulo no puede estar vacio.")
        else:
            tit_limpio = limpiar_texto(tit_buscar)
            encontradas = []
            comparaciones = 0
            for p in peliculas:
                comparaciones += 1
                if tit_limpio in limpiar_texto(p.titulo):
                    encontradas.append(p)

            print(f"Se encontraron {len(encontradas)} pelicula(s) con '{tit_buscar}':")
            for p in encontradas:
                print(f"  {p}")
            print(f"Comparaciones realizadas: {comparaciones}")
        print()

    # ------------------------------------------------------------------
    # 4. Agregar pelicula
    # ------------------------------------------------------------------
    elif opcion == 4:
        print("\n--- Agregar Pelicula ---")
        cod = input("Codigo (ej: MOV-041): ").strip()
        if not cod:
            print("El codigo no puede estar vacio.")
            continue
        if any(p.codigo == cod for p in peliculas):
            print("Ese codigo ya existe. No se puede duplicar.")
            continue

        titulo = input("Titulo: ").strip()
        categoria = input("Categoria: ").strip()
        subcategoria = input("Subcategoria (Enter para vacio): ").strip()
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
            print(f"[OK] Pelicula '{titulo}' agregada y guardada con exito.")
        except ValueError as e:
            print(f"Error al crear pelicula: {e}")
        print()

    # ------------------------------------------------------------------
    # 5. Eliminar pelicula
    # ------------------------------------------------------------------
    elif opcion == 5:
        print("\n--- Eliminar Pelicula ---")
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
            confirmacion = input("¿Confirma la eliminacion? (s/n): ").strip().lower()
            if confirmacion == "s":
                peliculas.remove(pelicula_encontrada)
                Pelicula.guardar_en_json(peliculas)
                print("[OK] Pelicula eliminada correctamente.")
            else:
                print("Operacion cancelada.")
        print()

    # ------------------------------------------------------------------
    # 6. Modificar pelicula
    # ------------------------------------------------------------------
    elif opcion == 6:
        print("\n--- Modificar Pelicula ---")
        cod = input("Codigo de la pelicula a modificar: ").strip()
        pelicula_encontrada = None
        for p in peliculas:
            if p.codigo == cod:
                pelicula_encontrada = p
                break

        if pelicula_encontrada is None:
            print("No se encontro ninguna pelicula con ese codigo.")
        else:
            print(f"\nModificando: {pelicula_encontrada}")
            print("Presione Enter directamente para conservar el valor actual entre corchetes.")

            nuevo_titulo = input(f"Nuevo titulo [{pelicula_encontrada.titulo}]: ").strip()
            nueva_cat = input(f"Nueva categoria [{pelicula_encontrada.categoria}]: ").strip()
            nueva_subcat = input(f"Nueva subcategoria [{pelicula_encontrada.subcategoria}]: ").strip()
            nuevo_dir = input(f"Nuevo director [{pelicula_encontrada.director}]: ").strip()
            nuevo_anio = input(f"Nuevo anio [{pelicula_encontrada.anio}]: ").strip()
            nueva_dur = input(f"Nueva duracion [{pelicula_encontrada.duracion}]: ").strip()
            nuevo_stock = input(f"Nuevo stock [{pelicula_encontrada.stock}]: ").strip()

            try:
                if nuevo_titulo:
                    pelicula_encontrada.titulo = nuevo_titulo
                if nueva_cat:
                    pelicula_encontrada.categoria = nueva_cat
                if nueva_subcat:
                    pelicula_encontrada.subcategoria = nueva_subcat
                if nuevo_dir:
                    pelicula_encontrada.director = nuevo_dir
                if nuevo_anio:
                    pelicula_encontrada.anio = int(nuevo_anio)
                if nueva_dur:
                    pelicula_encontrada.duracion = int(nueva_dur)
                if nuevo_stock:
                    pelicula_encontrada.stock = int(nuevo_stock)

                Pelicula.guardar_en_json(peliculas)
                print("[OK] Pelicula modificada y guardada correctamente.")
            except ValueError as e:
                print(f"Error al modificar: {e}")
        print()

    # ------------------------------------------------------------------
    # 7. Eliminar cliente
    # ------------------------------------------------------------------
    elif opcion == 7:
        print("\n--- Eliminar Cliente ---")
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
            confirmacion = input("¿Confirma la eliminacion del cliente? (s/n): ").strip().lower()
            if confirmacion == "s":
                clientes.remove(cliente_encontrado)
                Cliente.guardar_en_json(clientes)
                print("[OK] Cliente eliminado correctamente.")
            else:
                print("Operacion cancelada. No se borraron datos.")
        print()

    # ------------------------------------------------------------------
    # 0. Salir
    # ------------------------------------------------------------------
    elif opcion == 0:
        print("Saliendo del sistema... ¡Hasta luego!")

    else:
        print("Opcion no valida. Intente nuevamente.")
