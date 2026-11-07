import sys
from pathlib import Path

# Permite importar desde la raiz del proyecto
base = Path(__file__).resolve().parent.parent
if str(base) not in sys.path:
    sys.path.append(str(base))

from modelo.pelicula import Pelicula
from modelo.clientes import Cliente
from estructura.arbol_categorias import armar_arbol
from estructura.arbol_bst import construir_bst_balanceado, inorden
from estructura.pila import Pila
from estructura.cola import Cola
from servicios.verificacion import autenticar_usuario, registrar_nuevo_cliente


def limpiar_texto(texto):
    """Normaliza texto: minusculas y sin tildes para busquedas."""
    texto = texto.lower()
    reemplazos = {"á": "a", "é": "e", "í": "i", "ó": "o", "ú": "u", "ñ": "n"}
    for orig, reemplazo in reemplazos.items():
        texto = texto.replace(orig, reemplazo)
    return texto


# Alias para compatibilidad con otros modulos
cargar_peliculas = Pelicula.cargar_desde_json


# ====================================================================== #
#  MENÚ DE ADMINISTRADOR (Gestión completa, ABM, estructuras)            #
# ====================================================================== #
def menu_administrador(peliculas, clientes):
    """Loop del menú exclusivo para usuarios con rol 'admin'."""
    pila_deshacer = Pila()
    historial = Cola(5)

    opcion = -1
    while opcion != 0:
        print("\n" + "=" * 48)
        print("     VIDEOCLUB - PANEL DE ADMINISTRADOR")
        print("=" * 48)
        print("  1. Ver lista de Peliculas")
        print("  2. Buscar por Categoria")
        print("  3. Buscar por Titulo")
        print("  4. Agregar Pelicula")
        print("  5. Eliminar Pelicula")
        print("  6. Modificar Pelicula")
        print("  7. Eliminar Cliente")
        print("  8. Explorar por Categorias (Arbol)")
        print("  9. Listar todo ordenado (BST inorden)")
        print(" 10. Buscar por Codigo (BST)")
        print(" 11. Deshacer ultima operacion (Pila)")
        print(" 12. Ver historial de consultas (Cola)")
        print()
        print("  0. Cerrar Sesion")
        print("=" * 48)

        try:
            opcion = int(input("Ingrese una opcion: "))
        except ValueError:
            print("\n[!] Debe ingresar un numero valido.\n")
            continue

        # 1. Ver lista de peliculas
        if opcion == 1:
            print("\n--- Lista de Peliculas ---")
            if not peliculas:
                print("No hay peliculas registradas.")
            else:
                for p in peliculas:
                    print(p)
            print()

        # 2. Buscar por categoria
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

        # 3. Buscar por titulo
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

        # 4. Agregar pelicula
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
                pila_deshacer.apilar(("agregar", nueva))
                print(f"[OK] Pelicula '{titulo}' agregada y guardada con exito.")
            except ValueError as e:
                print(f"Error al crear pelicula: {e}")
            print()

        # 5. Eliminar pelicula
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
                    pila_deshacer.apilar(("eliminar", pelicula_encontrada))
                    print("[OK] Pelicula eliminada correctamente.")
                else:
                    print("Operacion cancelada.")
            print()

        # 6. Modificar pelicula
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
                print("Presione Enter directamente para conservar el valor actual.")

                nuevo_titulo = input(f"Nuevo titulo [{pelicula_encontrada.titulo}]: ").strip()
                nueva_cat = input(f"Nueva categoria [{pelicula_encontrada.categoria}]: ").strip()
                nueva_subcat = input(f"Nueva subcategoria [{pelicula_encontrada.subcategoria}]: ").strip()
                nuevo_dir = input(f"Nuevo director [{pelicula_encontrada.director}]: ").strip()
                nuevo_anio = input(f"Nuevo anio [{pelicula_encontrada.anio}]: ").strip()
                nueva_dur = input(f"Nueva duracion [{pelicula_encontrada.duracion}]: ").strip()
                nuevo_stock = input(f"Nuevo stock [{pelicula_encontrada.stock}]: ").strip()

                try:
                    copia_vieja = Pelicula(
                        pelicula_encontrada.codigo, pelicula_encontrada.titulo,
                        pelicula_encontrada.categoria, pelicula_encontrada.subcategoria,
                        pelicula_encontrada.director, pelicula_encontrada.anio,
                        pelicula_encontrada.duracion, pelicula_encontrada.stock
                    )

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
                    pila_deshacer.apilar(("modificar", copia_vieja))
                    print("[OK] Pelicula modificada y guardada correctamente.")
                except ValueError as e:
                    print(f"Error al modificar: {e}")
            print()

        # 7. Eliminar cliente
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

        # 8. Explorar por categorías
        elif opcion == 8:
            print("\n--- Explorar por Categorias ---")
            arbol = armar_arbol(peliculas)
            subopcion = -1
            while subopcion != 0:
                print("\n1. Ver arbol de categorias")
                print("2. Buscar peliculas por categoria")
                print("0. Volver al menu principal")
                try:
                    subopcion = int(input("Opcion: "))
                except ValueError:
                    print("Opcion invalida")
                    continue
                if subopcion == 1:
                    arbol.mostrar()
                elif subopcion == 2:
                    nombre = input("Ingrese nombre de categoria: ").strip()
                    nodo = arbol.buscar_categoria(nombre)
                    if nodo:
                        resultado = nodo.listar_todos()
                        print(f"Peliculas en '{nombre}' ({len(resultado)}):")
                        for p in resultado:
                            print(f"- {p.titulo} ({p.anio})")
                    else:
                        print(f"No se encontro la categoria '{nombre}'")
            print()

        # 9. Listar todo ordenado (BST inorden)
        elif opcion == 9:
            print("\n--- Catalogo Ordenado por Codigo (BST) ---")
            arbol_bst = construir_bst_balanceado(peliculas, "codigo")
            catalogo_ordenado = inorden(arbol_bst)
            for p in catalogo_ordenado:
                print(f"[{p.codigo}] {p.titulo} ({p.anio}) - Stock: {p.stock}")
            print(f"\nTotal: {len(catalogo_ordenado)} peliculas.")
            print()

        # 10. Buscar por código (BST)
        elif opcion == 10:
            print("\n--- Buscar Pelicula por Codigo (BST) ---")
            codigo_buscar = input("Ingrese codigo a buscar: ").strip().upper()
            arbol_bst = construir_bst_balanceado(peliculas, "codigo")
            resultado, pasos = arbol_bst.buscar(codigo_buscar)
            if resultado:
                print(f"\n[OK] Pelicula encontrada en {pasos} paso(s):")
                print(f"  Titulo:      {resultado.titulo}")
                print(f"  Categoria:   {resultado.categoria}")
                print(f"  Director:    {resultado.director}")
                print(f"  Anio:        {resultado.anio}")
                print(f"  Duracion:    {resultado.duracion} min")
                print(f"  Stock:       {resultado.stock}")
                historial.encolar(resultado.titulo)
            else:
                print(f"\n[!] No se encontro pelicula con codigo '{codigo_buscar}' (busqueda finalizo en {pasos} pasos).")
            print()

        # 11. Deshacer última operación (Pila)
        elif opcion == 11:
            print("\n--- Deshacer Ultima Operacion ---")
            if pila_deshacer.esta_vacia():
                print("No hay acciones para deshacer.")
            else:
                accion, obj = pila_deshacer.desapilar()
                if accion == "agregar":
                    peliculas.remove(obj)
                    print(f"Se desizo la creacion de la pelicula: {obj.titulo}")
                elif accion == "eliminar":
                    peliculas.append(obj)
                    print(f"Se restauro la pelicula: {obj.titulo}")
                elif accion == "modificar":
                    for i, p in enumerate(peliculas):
                        if p.codigo == obj.codigo:
                            peliculas[i] = obj
                            break
                    print(f"Se restauraron los datos anteriores de: {obj.titulo}")
                Pelicula.guardar_en_json(peliculas)
            print()

        # 12. Ver historial de consultas (Cola)
        elif opcion == 12:
            print("\n--- Historial de Peliculas Consultadas (Cola) ---")
            if historial.esta_vacia():
                print("Todavia no hiciste busquedas.")
            else:
                for b in historial.listar():
                    print(f"- {b}")
            print()

        elif opcion == 0:
            print("\nCerrando sesion de Administrador...")


# ====================================================================== #
#  MENÚ DE USUARIO / CLIENTE (Catálogo, Búsquedas y Reservas)            #
# ====================================================================== #
def menu_usuario(cliente_actual: Cliente, peliculas, clientes):
    """Loop del menú para clientes comunes."""
    historial = Cola(5)
    opcion = -1

    while opcion != 0:
        print("\n" + "=" * 48)
        print(f"   VIDEOCLUB - BIENVENIDO/A, {cliente_actual._nombre.upper()}")
        print("=" * 48)
        print("  1. Ver Catalogo Completo de Peliculas")
        print("  2. Buscar Pelicula por Titulo")
        print("  3. Buscar Pelicula por Categoria")
        print("  4. Explorar Catalogo por Arbol de Categorias")
        print("  5. Buscar Pelicula por Codigo (BST)")
        print("  6. Reservar una Pelicula")
        print("  7. Ver Mis Peliculas Reservadas")
        print("  8. Cancelar una Reserva")
        print("  9. Ver Mis Datos de Perfil")
        print(" 10. Ver Mi Historial de Consultas (Cola)")
        print()
        print("  0. Cerrar Sesion")
        print("=" * 48)

        try:
            opcion = int(input("Ingrese una opcion: "))
        except ValueError:
            print("\n[!] Debe ingresar un numero valido.\n")
            continue

        # 1. Ver catálogo
        if opcion == 1:
            print("\n--- Catalogo de Peliculas Disponibles ---")
            for p in peliculas:
                estado = f"Disponible (Stock: {p.stock})" if p.stock > 0 else "SIN STOCK"
                print(f"[{p.codigo}] {p.titulo} ({p.anio}) | {p.categoria} | {estado}")
            print()

        # 2. Buscar por título
        elif opcion == 2:
            print("\n--- Buscar por Titulo ---")
            tit = input("Titulo a buscar: ").strip()
            if not tit:
                print("El titulo no puede estar vacio.")
            else:
                tit_l = limpiar_texto(tit)
                encontradas = [p for p in peliculas if tit_l in limpiar_texto(p.titulo)]
                print(f"Se encontraron {len(encontradas)} resultado(s):")
                for p in encontradas:
                    print(f"  [{p.codigo}] {p.titulo} - Dir: {p.director} (Stock: {p.stock})")
                    historial.encolar(p.titulo)
            print()

        # 3. Buscar por categoría
        elif opcion == 3:
            print("\n--- Buscar por Categoria ---")
            cat = input("Categoria a buscar: ").strip()
            if not cat:
                print("La categoria no puede estar vacia.")
            else:
                cat_l = limpiar_texto(cat)
                encontradas = [p for p in peliculas if cat_l in limpiar_texto(p.categoria) or (p.subcategoria and cat_l in limpiar_texto(p.subcategoria))]
                print(f"Se encontraron {len(encontradas)} resultado(s):")
                for p in encontradas:
                    print(f"  [{p.codigo}] {p.titulo} | {p.categoria} ({p.subcategoria}) - Stock: {p.stock}")
            print()

        # 4. Explorar por árbol de categorías
        elif opcion == 4:
            print("\n--- Explorar por Categorias ---")
            arbol = armar_arbol(peliculas)
            arbol.mostrar()
            cat_sel = input("\nIngrese nombre de categoria para ver sus peliculas (o Enter para volver): ").strip()
            if cat_sel:
                nodo = arbol.buscar_categoria(cat_sel)
                if nodo:
                    pelis_nodo = nodo.listar_todos()
                    print(f"\nPeliculas en '{cat_sel}' ({len(pelis_nodo)}):")
                    for p in pelis_nodo:
                        print(f"- [{p.codigo}] {p.titulo} ({p.anio}) - Stock: {p.stock}")
                else:
                    print(f"No se encontro la categoria '{cat_sel}'.")
            print()

        # 5. Buscar por código BST
        elif opcion == 5:
            print("\n--- Buscar por Codigo (BST) ---")
            cod_buscar = input("Codigo (ej: MOV-001): ").strip().upper()
            arbol_bst = construir_bst_balanceado(peliculas)
            resultado, pasos = arbol_bst.buscar(cod_buscar)
            if resultado:
                print(f"\n[OK] Encontrada en {pasos} paso(s):")
                print(f"  {resultado.titulo} ({resultado.anio})")
                print(f"  Director: {resultado.director} | Duracion: {resultado.duracion} min")
                print(f"  Stock disponible: {resultado.stock}")
                historial.encolar(resultado.titulo)
            else:
                print(f"No se encontro pelicula con codigo '{cod_buscar}'.")
            print()

        # 6. Reservar una película
        elif opcion == 6:
            print("\n--- Reservar Pelicula ---")
            cod_reserva = input("Ingrese el codigo de la pelicula a reservar: ").strip().upper()
            pelicula_target = None
            for p in peliculas:
                if p.codigo == cod_reserva:
                    pelicula_target = p
                    break

            if pelicula_target is None:
                print(f"No existe ninguna pelicula con el codigo '{cod_reserva}'.")
            elif cod_reserva in cliente_actual.peliculas_reservadas:
                print(f"Ya tienes una reserva activa para '{pelicula_target.titulo}'.")
            elif pelicula_target.stock <= 0:
                print(f"Lo sentimos, no hay stock disponible para '{pelicula_target.titulo}'.")
            else:
                # Confirmación
                print(f"Pelicula: {pelicula_target.titulo} | Stock actual: {pelicula_target.stock}")
                conf = input("¿Confirmar reserva? (s/n): ").strip().lower()
                if conf == "s":
                    # 1. Agrega al cliente
                    cliente_actual.agregar_reserva(cod_reserva)
                    # 2. Descuenta stock
                    pelicula_target.stock -= 1
                    # 3. Guarda cambios en disco
                    Cliente.guardar_en_json(clientes)
                    Pelicula.guardar_en_json(peliculas)
                    print(f"¡Reserva confirmada con exito! Codigo reservado: {cod_reserva}")
                else:
                    print("Reserva cancelada.")
            print()

        # 7. Ver mis reservas
        elif opcion == 7:
            print("\n--- Mis Peliculas Reservadas ---")
            reservas = cliente_actual.mostrar_reservas()
            if isinstance(reservas, list) and reservas:
                print(f"Tienes {len(reservas)} pelicula(s) reservada(s):")
                for cod in reservas:
                    peli = next((p for p in peliculas if p.codigo == cod), None)
                    nombre = peli.titulo if peli else "Titulo no encontrado"
                    print(f"  • [{cod}] {nombre}")
            else:
                print("Actualmente no tienes reservas activas.")
            print()

        # 8. Cancelar reserva
        elif opcion == 8:
            print("\n--- Cancelar Reserva ---")
            if not cliente_actual.peliculas_reservadas:
                print("No tienes reservas activas para cancelar.")
            else:
                print("Tus reservas actuales:")
                for cod in cliente_actual.peliculas_reservadas:
                    peli = next((p for p in peliculas if p.codigo == cod), None)
                    print(f"  • [{cod}] {peli.titulo if peli else ''}")

                cod_canc = input("\nIngrese el codigo de la reserva a cancelar: ").strip().upper()
                if cod_canc not in cliente_actual.peliculas_reservadas:
                    print(f"No tienes ninguna reserva con el codigo '{cod_canc}'.")
                else:
                    conf = input(f"¿Seguro que deseas cancelar la reserva de [{cod_canc}]? (s/n): ").strip().lower()
                    if conf == "s":
                        cliente_actual.eliminar_reserva(cod_canc)
                        # Devolver el stock a la película
                        peli = next((p for p in peliculas if p.codigo == cod_canc), None)
                        if peli:
                            peli.stock += 1
                        Cliente.guardar_en_json(clientes)
                        Pelicula.guardar_en_json(peliculas)
                        print("[OK] Reserva cancelada y stock restaurado correctamente.")
                    else:
                        print("Operacion cancelada.")
            print()

        # 9. Ver mis datos de perfil
        elif opcion == 9:
            print("\n--- Mi Perfil ---")
            print(f"  Usuario:   {cliente_actual.usuario}")
            print(f"  Nombre:    {cliente_actual._nombre} {cliente_actual._apellido}")
            print(f"  DNI:       {cliente_actual.dni}")
            print(f"  Telefono:  {cliente_actual.telefono}")
            print(f"  Direccion: {cliente_actual.direccion}")
            print(f"  Rol:       {cliente_actual.rol}")
            print(f"  Reservas:  {len(cliente_actual.peliculas_reservadas)}")
            print()

        # 10. Historial de consultas
        elif opcion == 10:
            print("\n--- Mi Historial de Consultas Recientes (Cola) ---")
            if historial.esta_vacia():
                print("No has realizado consultas todavia.")
            else:
                for b in historial.listar():
                    print(f"- {b}")
            print()

        elif opcion == 0:
            print(f"\nHasta luego, {cliente_actual._nombre}. Sesion cerrada.")


# ====================================================================== #
#  PUNTO DE ENTRADA: LOGIN Y REGISTRO                                    #
# ====================================================================== #
def iniciar_menu():
    """Loop principal de acceso al videoclub: Login, Registro o Salir."""
    # Carga inicial desde archivos JSON
    peliculas = Pelicula.cargar_desde_json()
    clientes = Cliente.cargar_desde_json()

    opcion_inicio = -1
    while opcion_inicio != 0:
        print("\n" + "=" * 48)
        print("          SISTEMA DE VIDEOCLUB")
        print("=" * 48)
        print("  1. Iniciar Sesion")
        print("  2. Registrarse como Nuevo Cliente")
        print()
        print("  0. Salir del Sistema")
        print("=" * 48)

        try:
            opcion_inicio = int(input("Seleccione una opcion: "))
        except ValueError:
            print("\n[!] Ingrese un numero valido.")
            continue

        # 1. Iniciar sesión
        if opcion_inicio == 1:
            intentos = 3
            cliente_logeado = None

            while intentos > 0:
                print(f"\n--- Iniciar Sesion (Intentos restantes: {intentos}) ---")
                usuario_input = input("Usuario: ").strip()
                password_input = input("Contrasenia: ").strip()

                cliente_logeado = autenticar_usuario(usuario_input, password_input, clientes)

                if cliente_logeado is not None:
                    break
                else:
                    intentos -= 1
                    print("[-] Usuario o contrasenia incorrectos.")

            if cliente_logeado is not None:
                # Verificación de rol para bifurcar al menú correspondiente
                if cliente_logeado.rol.lower() == "admin":
                    menu_administrador(peliculas, clientes)
                else:
                    menu_usuario(cliente_logeado, peliculas, clientes)
            else:
                print("\n[!] Superaste el limite de intentos. Volviendo al menu principal.")

        # 2. Registrar nuevo cliente
        elif opcion_inicio == 2:
            print("\n--- Registro de Nuevo Cliente ---")
            nombre = input("Nombre: ").strip()
            apellido = input("Apellido: ").strip()
            dni = input("DNI (sin puntos): ").strip()
            telefono = input("Telefono: ").strip()
            direccion = input("Direccion: ").strip()
            usuario = input("Elija un nombre de usuario: ").strip()
            password = input("Elija una contrasenia: ").strip()

            exito, mensaje, nuevo = registrar_nuevo_cliente(
                nombre, apellido, dni, telefono, direccion, usuario, password, clientes
            )

            if exito:
                print(f"\n[OK] {mensaje} Ya puedes iniciar sesion con tu usuario '{nuevo.usuario}'.")
            else:
                print(f"\n[ERROR] {mensaje}")

        elif opcion_inicio == 0:
            print("\nGracias por usar el sistema del Videoclub. ¡Hasta pronto!")

        else:
            print("\nOpcion no valida. Intente Nuevamente.")


if __name__ == "__main__":
    iniciar_menu()
