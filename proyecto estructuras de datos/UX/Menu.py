import sys
from pathlib import Path

# Agrega la raiz del proyecto al path para poder importar modelo/
base = Path(__file__).resolve().parent.parent
sys.path.append(str(base))

from modelo.pelicula import Pelicula
from modelo.clientes import Cliente

# ---------------------------------------------------------------
# Carga inicial desde los archivos JSON usando los metodos de las clases
# ---------------------------------------------------------------
peliculas = Pelicula.cargar_desde_json()
clientes = Cliente.cargar_desde_json()


def limpiar_texto(texto):
    """Normaliza texto: minusculas y sin tildes, para comparaciones."""
    texto = texto.lower()
    reemplazos = {"á": "a", "é": "e", "í": "i", "ó": "o", "ú": "u", "ñ": "n"}
    for original, reemplazo in reemplazos.items():
        texto = texto.replace(original, reemplazo)
    return texto


# ---------------------------------------------------------------
# Loop principal del menu
# ---------------------------------------------------------------
opcion = -1
while opcion != 0:

    print("=" * 40)
    print("   VIDEOCLUB - MENU PRINCIPAL")
    print("=" * 40)
    print("1. Ver lista de Peliculas")
    print("2. Buscar por Categoria")
    print("3. Buscar por Titulo")
    print("4. Agregar Pelicula")
    print("5. Eliminar Pelicula")
    print("6. Modificar Pelicula")
    print("7. Eliminar Cliente")
    print()
    print("0. Salir")
    print("=" * 40)

    try:
        opcion = int(input("Ingrese una opcion: "))
    except ValueError:
        print("Por favor ingrese un numero valido.")
        opcion = -1
        continue

    # ------------------------------------------------------------------
    if opcion == 1:
        print()
        print("--- Lista de peliculas ---")
        if not peliculas:
            print("No hay peliculas cargadas.")
        for p in peliculas:
            print(f"Codigo: [{p.codigo}], Titulo: {p.titulo}, Categoria: {p.categoria}, "
                f"Subcategoria: {p.subcategoria}, Director: {p.director}, "
                f"Anio: {p.anio}, Duracion: {p.duracion} min, Stock: {p.stock}")
        print()

    # ------------------------------------------------------------------
    elif opcion == 2:
        print()
        print("--- Buscar por categoria ---")
        categoria_buscar = input("Ingrese la categoria a buscar: ").strip()
        categoria_buscar = limpiar_texto(categoria_buscar)
        if not categoria_buscar:
            print("La categoria no puede estar vacia.")
        else:
            encontradas = []
            comparaciones = 0
            for p in peliculas:
                comparaciones += 1
                if categoria_buscar in limpiar_texto(p.categoria):
                    encontradas.append(p)
            print(f"Se encontraron {len(encontradas)} peliculas en la categoria '{categoria_buscar}':")
            for p in encontradas:
                print(f"  [{p.codigo}] {p.titulo} - {p.director} ({p.anio})")
            print(f"Comparaciones realizadas: {comparaciones}")
        print()

    # ------------------------------------------------------------------
    elif opcion == 3:
        print()
        print("--- Buscar por titulo ---")
        titulo_buscar = input("Ingrese el titulo a buscar: ").strip()
        titulo_buscar = limpiar_texto(titulo_buscar)
        if not titulo_buscar:
            print("El titulo no puede estar vacio.")
        else:
            encontradas = []
            comparaciones = 0
            for p in peliculas:
                comparaciones += 1
                if titulo_buscar in limpiar_texto(p.titulo):
                    encontradas.append(p)
            print(f"Se encontraron {len(encontradas)} peliculas con '{titulo_buscar}' en el titulo:")
            for p in encontradas:
                print(f"  [{p.codigo}] {p.titulo} - {p.director} ({p.anio})")
            print(f"Comparaciones realizadas: {comparaciones}")
        print()

    # ------------------------------------------------------------------
    elif opcion == 4:
        print()
        print("--- Agregar pelicula ---")
        cod = input("Ingrese codigo (ej: MOV-041): ").strip()
        if not cod:
            print("El codigo no puede estar vacio.")
            continue
        if cod in [p.codigo for p in peliculas]:
            print("Ese codigo ya existe. No se puede agregar una pelicula duplicada.")
            continue

        titulo = input("Titulo: ").strip()
        categoria = input("Categoria: ").strip()
        subcategoria = input("Subcategoria (puede dejarlo vacio): ").strip()
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
            print(f"[OK] Pelicula '{titulo}' agregada y guardada.")
        except ValueError as e:
            print(f"Error: {e}")
        print()

    # ------------------------------------------------------------------
    elif opcion == 5:
        print()
        print("--- Eliminar pelicula ---")
        cod = input("Ingrese el codigo de la pelicula a eliminar: ").strip()
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
    elif opcion == 6:
        print()
        print("--- Modificar pelicula ---")
        cod = input("Ingrese el codigo de la pelicula a modificar: ").strip()
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
            print("  1. Titulo")
            print("  2. Categoria")
            print("  3. Subcategoria")
            print("  4. Director")
            print("  5. Anio")
            print("  6. Duracion")
            print("  7. Stock")
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
                    print("Opcion no valida.")
                    continue
                Pelicula.guardar_en_json(peliculas)
                print("[OK] Pelicula modificada y guardada.")
            except ValueError as e:
                print(f"Error: {e}")
        print()

    # ------------------------------------------------------------------
    elif opcion == 7:
        print()
        print("--- Eliminar Cliente ---")
        dni_buscar = input("Ingrese el DNI del cliente (sin puntos): ").strip()

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
