import sys
from pathlib import Path
from datetime import datetime

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

cargar_peliculas = Pelicula.cargar_desde_json

# ====================================================================== #
#  GESTIÓN DE RECARGOS POR DEVOLUCIÓN TARDÍA - CARY                      #
# ====================================================================== #
def gestionar_recargos(clientes):
    """Permite al administrador ver recargos, agregar o condonar - igual a lista negra de Mariana"""
    VALOR_DIA = 500
    subopcion = -1
    while subopcion != 0:
        print("\n" + "=" * 50)
        print("     GESTION DE RECARGOS POR DEVOLUCION TARDIA")
        print("=" * 50)
        print("  1. Ver clientes con Recargo")
        print("  2. Calcular recargo manual por dias de atraso")
        print("  3. Condonar recargo (quitar deuda)")
        print()
        print("  0. Volver al Panel de Administrador")
        print("=" * 50)
        try:
            subopcion = int(input("Seleccione una opcion: "))
        except ValueError:
            print("\n[!] Debe ingresar un numero valido.")
            continue

        if subopcion == 1:
            print("\n--- Clientes con Recargo ---")
            con_recargo = [c for c in clientes if c.recargo_acumulado > 0]
            if not con_recargo:
                print("Actualmente no hay clientes con recargo.")
            else:
                print(f"Total con recargo: {len(con_recargo)}")
                for c in con_recargo:
                    dias = c.calcular_dias_atraso()
                    print(f"  • DNI: {c.dni:<10} | {c._nombre} {c._apellido:<15} | Debe: ${c.recargo_acumulado} | Vence: {c.fecha_limite} | Atraso hoy: {dias} dias")
            print()

        elif subopcion == 2:
            print("\n--- Calcular Recargo Manual ---")
            busqueda = input("Ingrese DNI o Usuario del cliente: ").strip()
            if not busqueda:
                print("El dato no puede estar vacio.")
                continue
            cliente_target = None
            for c in clientes:
                if c.dni == busqueda or c.usuario.lower() == busqueda.lower():
                    cliente_target = c
                    break
            if cliente_target is None:
                print(f"No se encontro cliente '{busqueda}'.")
            else:
                try:
                    dias = int(input(f"Ingrese dias de atraso para {cliente_target._nombre} (valor ${VALOR_DIA} x dia): "))
                    if dias <=0:
                        print("Los dias deben ser mayor a 0")
                        continue
                    recargo = dias * VALOR_DIA
                    print(f"Calculo: {dias} dias x ${VALOR_DIA} = ${recargo}")
                    conf = input(f"¿Confirmar recargo de ${recargo} a {cliente_target._nombre}? (s/n): ").lower()
                    if conf == "s":
                        cliente_target.recargo_acumulado += recargo
                        # Si no tiene fecha, le ponemos hoy como vencida
                        if not cliente_target.fecha_limite:
                            cliente_target.fecha_limite = datetime.now().strftime("%d/%m/%Y")
                        Cliente.guardar_en_json(clientes)
                        print(f"[OK] Recargo aplicado. Total adeudado: ${cliente_target.recargo_acumulado}")
                    else:
                        print("Operacion cancelada")
                except ValueError:
                    print("Debe ingresar un numero")
            print()

        elif subopcion == 3:
            print("\n--- Condonar Recargo ---")
            busqueda = input("Ingrese DNI o Usuario del cliente a condonar: ").strip()
            if not busqueda:
                print("El dato no puede estar vacio.")
                continue
            cliente_target = None
            for c in clientes:
                if c.dni == busqueda or c.usuario.lower() == busqueda.lower():
                    cliente_target = c
                    break
            if cliente_target is None:
                print(f"No se encontro cliente '{busqueda}'.")
            elif cliente_target.recargo_acumulado == 0:
                print(f"{cliente_target._nombre} no tiene recargos pendientes.")
            else:
                print(f"Cliente: {cliente_target._nombre} {cliente_target._apellido} | Debe: ${cliente_target.recargo_acumulado}")
                conf = input("¿Confirmar condonacion total? (s/n): ").lower()
                if conf == "s":
                    cliente_target.recargo_acumulado = 0
                    cliente_target.fecha_limite = ""
                    Cliente.guardar_en_json(clientes)
                    print(f"[OK] Recargo condonado para {cliente_target._nombre}")
                else:
                    print("Operacion cancelada")
            print()

        elif subopcion == 0:
            print("\nVolviendo al Panel...")
        else:
            print("\nOpcion no valida")

# ====================================================================== #
#  MENÚ DE ADMINISTRADOR                                                  #
# ====================================================================== #
def menu_administrador(peliculas, clientes):
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
        print(" 13. Gestionar Recargos por Devolucion Tardia") # <-- NUEVO TUYO IGUAL A LA 13 DE MARIANA
        print()
        print("  0. Cerrar Sesion")
        print("=" * 48)
        try:
            opcion = int(input("Ingrese una opcion: "))
        except ValueError:
            print("\n[!] Debe ingresar un numero valido.\n")
            continue

        if opcion == 1:
            print("\n--- Lista de Peliculas ---")
            if not peliculas:
                print("No hay peliculas registradas.")
            else:
                for p in peliculas:
                    print(p)
            print()
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
                    copia_vieja = Pelicula(pelicula_encontrada.codigo, pelicula_encontrada.titulo, pelicula_encontrada.categoria, pelicula_encontrada.subcategoria, pelicula_encontrada.director, pelicula_encontrada.anio, pelicula_encontrada.duracion, pelicula_encontrada.stock)
                    if nuevo_titulo: pelicula_encontrada.titulo = nuevo_titulo
                    if nueva_cat: pelicula_encontrada.categoria = nueva_cat
                    if nueva_subcat: pelicula_encontrada.subcategoria = nueva_subcat
                    if nuevo_dir: pelicula_encontrada.director = nuevo_dir
                    if nuevo_anio: pelicula_encontrada.anio = int(nuevo_anio)
                    if nueva_dur: pelicula_encontrada.duracion = int(nueva_dur)
                    if nuevo_stock: pelicula_encontrada.stock = int(nuevo_stock)
                    Pelicula.guardar_en_json(peliculas)
                    pila_deshacer.apilar(("modificar", copia_vieja))
                    print("[OK] Pelicula modificada y guardada correctamente.")
                except ValueError as e:
                    print(f"Error al modificar: {e}")
            print()
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
                if subopcion == 1: arbol.mostrar()
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
        elif opcion == 9:
            print("\n--- Catalogo Ordenado por Codigo (BST) ---")
            arbol_bst = construir_bst_balanceado(peliculas, "codigo")
            catalogo_ordenado = inorden(arbol_bst)
            for p in catalogo_ordenado:
                print(f"[{p.codigo}] {p.titulo} ({p.anio}) - Stock: {p.stock}")
            print(f"\nTotal: {len(catalogo_ordenado)} peliculas.")
            print()
        elif opcion == 10:
            print("\n--- Buscar Pelicula por Codigo (BST) ---")
            codigo_buscar = input("Ingrese codigo a buscar: ").strip().upper()
            arbol_bst = construir_bst_balanceado(peliculas, "codigo")
            resultado, pasos = arbol_bst.buscar(codigo_buscar)
            if resultado:
                print(f"\n[OK] Pelicula encontrada en {pasos} paso(s):")
                print(f"  Titulo: {resultado.titulo}")
                historial.encolar(resultado.titulo)
            else:
                print(f"\n[!] No se encontro pelicula con codigo '{codigo_buscar}'")
            print()
        elif opcion == 11:
            print("\n--- Deshacer Ultima Operacion ---")
            if pila_deshacer.esta_vacia():
                print("No hay acciones para deshacer.")
            else:
                accion, obj = pila_deshacer.desapilar()
                if accion == "agregar": peliculas.remove(obj)
                elif accion == "eliminar": peliculas.append(obj)
                elif accion == "modificar":
                    for i, p in enumerate(peliculas):
                        if p.codigo == obj.codigo:
                            peliculas[i] = obj
                            break
                Pelicula.guardar_en_json(peliculas)
                print(f"Se deshizo: {accion}")
            print()
        elif opcion == 12:
            print("\n--- Historial de Peliculas Consultadas (Cola) ---")
            if historial.esta_vacia(): print("Todavia no hiciste busquedas.")
            else:
                for b in historial.listar(): print(f"- {b}")
            print()
        elif opcion == 13:
            gestionar_recargos(clientes)
        elif opcion == 0:
            print("\nCerrando sesion de Administrador...")

# ====================================================================== #
#  MENÚ DE USUARIO                                                        #
# ====================================================================== #
def menu_usuario(cliente_actual: Cliente, peliculas, clientes):
    historial = Cola(5)
    opcion = -1
    while opcion != 0:
        print("\n" + "=" * 48)
        print(f"   VIDEOCLUB - BIENVENIDO/A, {cliente_actual._nombre.upper()}")
        if cliente_actual.recargo_acumulado > 0:
            print(f"   [!] TENES RECARGO PENDIENTE: ${cliente_actual.recargo_acumulado}")
        print("=" * 48)
        print("  1. Ver Catalogo Completo")
        print("  2. Buscar por Titulo")
        print("  3. Buscar por Categoria")
        print("  4. Explorar por Arbol de Categorias")
        print("  5. Buscar por Codigo (BST)")
        print("  6. Reservar Pelicula")
        print("  7. Ver Mis Reservas")
        print("  8. Cancelar Reserva / Devolver (con recargo)")
        print("  9. Ver Mi Perfil y Recargos")
        print(" 10. Ver Mi Historial (Cola)")
        print()
        print("  0. Cerrar Sesion")
        print("=" * 48)
        try:
            opcion = int(input("Ingrese una opcion: "))
        except ValueError:
            print("\n[!] Debe ingresar un numero valido.\n")
            continue

        if opcion == 1:
            print("\n--- Catalogo ---")
            for p in peliculas:
                estado = f"Disponible (Stock: {p.stock})" if p.stock > 0 else "SIN STOCK"
                print(f"[{p.codigo}] {p.titulo} ({p.anio}) | {estado}")
            print()
        elif opcion == 2:
            tit = input("Titulo a buscar: ").strip()
            if tit:
                tit_l = limpiar_texto(tit)
                encontradas = [p for p in peliculas if tit_l in limpiar_texto(p.titulo)]
                print(f"Se encontraron {len(encontradas)} resultado(s):")
                for p in encontradas:
                    print(f"  [{p.codigo}] {p.titulo} - Stock: {p.stock}")
                    historial.encolar(p.titulo)
            print()
        elif opcion == 3:
            cat = input("Categoria a buscar: ").strip()
            if cat:
                cat_l = limpiar_texto(cat)
                encontradas = [p for p in peliculas if cat_l in limpiar_texto(p.categoria) or (p.subcategoria and cat_l in limpiar_texto(p.subcategoria))]
                print(f"Se encontraron {len(encontradas)} resultado(s):")
                for p in encontradas:
                    print(f"  [{p.codigo}] {p.titulo} - Stock: {p.stock}")
            print()
        elif opcion == 4:
            arbol = armar_arbol(peliculas)
            arbol.mostrar()
            cat_sel = input("\nCategoria para ver peliculas (Enter para volver): ").strip()
            if cat_sel:
                nodo = arbol.buscar_categoria(cat_sel)
                if nodo:
                    pelis_nodo = nodo.listar_todos()
                    print(f"\nPeliculas en '{cat_sel}' ({len(pelis_nodo)}):")
                    for p in pelis_nodo: print(f"- [{p.codigo}] {p.titulo} - Stock: {p.stock}")
            print()
        elif opcion == 5:
            cod_buscar = input("Codigo (ej: MOV-001): ").strip().upper()
            arbol_bst = construir_bst_balanceado(peliculas, "codigo")
            resultado, pasos = arbol_bst.buscar(cod_buscar)
            if resultado:
                print(f"\n[OK] Encontrada en {pasos} paso(s): {resultado.titulo}")
                historial.encolar(resultado.titulo)
            else:
                print(f"No se encontro '{cod_buscar}'.")
            print()
        elif opcion == 6:
            print("\n--- Reservar Pelicula ---")
            if cliente_actual.recargo_acumulado > 0:
                print(f"[!] Tenes un recargo pendiente de ${cliente_actual.recargo_acumulado}. No podes reservar hasta pagar.")
                print()
                continue
            cod_reserva = input("Codigo de pelicula a reservar: ").strip().upper()
            pelicula_target = None
            for p in peliculas:
                if p.codigo == cod_reserva:
                    pelicula_target = p
                    break
            if pelicula_target is None: print(f"No existe '{cod_reserva}'.")
            elif cod_reserva in cliente_actual.peliculas_reservadas: print(f"Ya tenes reserva para '{pelicula_target.titulo}'.")
            elif pelicula_target.stock <= 0: print(f"Sin stock para '{pelicula_target.titulo}'.")
            else:
                conf = input(f"¿Confirmar reserva de {pelicula_target.titulo}? (s/n): ").lower()
                if conf == "s":
                    cliente_actual.agregar_reserva(cod_reserva)
                    pelicula_target.stock -= 1
                    # Asignar fecha limite de 7 dias
                    from datetime import timedelta
                    limite = datetime.now() + timedelta(days=7)
                    cliente_actual.fecha_limite = limite.strftime("%d/%m/%Y")
                    Cliente.guardar_en_json(clientes)
                    Pelicula.guardar_en_json(peliculas)
                    print(f"¡Reserva ok! Devolver antes de: {cliente_actual.fecha_limite} o pagas $500 x dia")
                else: print("Cancelada")
            print()
        elif opcion == 7:
            print("\n--- Mis Reservas ---")
            reservas = cliente_actual.mostrar_reservas()
            if isinstance(reservas, list) and reservas:
                print(f"Tienes {len(reservas)} reservada(s):")
                for cod in reservas:
                    peli = next((p for p in peliculas if p.codigo == cod), None)
                    print(f"  • [{cod}] {peli.titulo if peli else ''}")
                if cliente_actual.fecha_limite:
                    print(f"  Fecha limite devolucion: {cliente_actual.fecha_limite}")
                    dias = cliente_actual.calcular_dias_atraso()
                    if dias > 0:
                        print(f"  [!] ATRASO ACTUAL: {dias} dias = ${dias*500} de recargo")
            else: print("No tienes reservas")
            print()
        elif opcion == 8:
            print("\n--- Cancelar Reserva / Devolver ---")
            if not cliente_actual.peliculas_reservadas:
                print("No tienes reservas para cancelar.")
            else:
                print("Tus reservas:")
                for cod in cliente_actual.peliculas_reservadas:
                    peli = next((p for p in peliculas if p.codigo == cod), None)
                    print(f"  • [{cod}] {peli.titulo if peli else ''}")
                cod_canc = input("\nCodigo a devolver: ").strip().upper()
                if cod_canc not in cliente_actual.peliculas_reservadas:
                    print(f"No tienes reserva '{cod_canc}'")
                else:
                    dias_atraso = cliente_actual.calcular_dias_atraso()
                    recargo = 0
                    if dias_atraso > 0:
                        recargo = dias_atraso * 500
                        print(f"\n[!] DEVOLUCION TARDIA: {dias_atraso} dias de atraso")
                        print(f"Recargo a aplicar: {dias_atraso} x $500 = ${recargo}")
                    conf = input(f"¿Confirmar devolucion? (s/n): ").lower()
                    if conf == "s":
                        cliente_actual.eliminar_reserva(cod_canc)
                        peli = next((p for p in peliculas if p.codigo == cod_canc), None)
                        if peli: peli.stock += 1
                        if recargo > 0:
                            cliente_actual.recargo_acumulado += recargo
                            print(f"[OK] Devuelto con recargo de ${recargo}. Total deuda: ${cliente_actual.recargo_acumulado}")
                        else:
                            print("[OK] Devolucion a tiempo, sin recargo")
                            if not cliente_actual.peliculas_reservadas:
                                cliente_actual.fecha_limite = ""
                        Cliente.guardar_en_json(clientes)
                        Pelicula.guardar_en_json(peliculas)
                    else: print("Cancelada")
            print()
        elif opcion == 9:
            print("\n--- Mi Perfil ---")
            print(f"  Usuario: {cliente_actual.usuario}")
            print(f"  Nombre: {cliente_actual._nombre} {cliente_actual._apellido}")
            print(f"  DNI: {cliente_actual.dni}")
            print(f"  Rol: {cliente_actual.rol}")
            print(f"  Reservas: {len(cliente_actual.peliculas_reservadas)}")
            print(f"  Fecha limite: {cliente_actual.fecha_limite if cliente_actual.fecha_limite else 'Sin reservas activas'}")
            print(f"  Recargo acumulado: ${cliente_actual.recargo_acumulado}")
            if cliente_actual.recargo_acumulado > 0:
                dias = cliente_actual.calcular_dias_atraso()
                print(f"  Dias atraso hoy: {dias}")
            print()
        elif opcion == 10:
            print("\n--- Mi Historial ---")
            if historial.esta_vacia(): print("No has hecho consultas")
            else:
                for b in historial.listar(): print(f"- {b}")
            print()
        elif opcion == 0:
            print(f"\nHasta luego, {cliente_actual._nombre}")

def iniciar_menu():
    peliculas = Pelicula.cargar_desde_json()
    clientes = Cliente.cargar_desde_json()
    opcion_inicio = -1
    while opcion_inicio != 0:
        print("\n" + "=" * 48)
        print("          SISTEMA DE VIDEOCLUB")
        print("=" * 48)
        print("  1. Iniciar Sesion")
        print("  2. Registrarse")
        print()
        print("  0. Salir")
        print("=" * 48)
        try:
            opcion_inicio = int(input("Seleccione una opcion: "))
        except ValueError:
            print("\n[!] Ingrese un numero valido.")
            continue
        if opcion_inicio == 1:
            intentos = 3
            cliente_logeado = None
            while intentos > 0:
                print(f"\n--- Iniciar Sesion (Intentos: {intentos}) ---")
                usuario_input = input("Usuario: ").strip()
                password_input = input("Contrasenia: ").strip()
                cliente_logeado = autenticar_usuario(usuario_input, password_input, clientes)
                if cliente_logeado is not None: break
                else:
                    intentos -= 1
                    print("[-] Usuario o contrasenia incorrectos.")
            if cliente_logeado is not None:
                if cliente_logeado.rol.lower() == "admin":
                    menu_administrador(peliculas, clientes)
                else:
                    menu_usuario(cliente_logeado, peliculas, clientes)
            else:
                print("\n[!] Limite de intentos")
        elif opcion_inicio == 2:
            print("\n--- Registro ---")
            nombre = input("Nombre: ").strip()
            apellido = input("Apellido: ").strip()
            dni = input("DNI: ").strip()
            telefono = input("Telefono: ").strip()
            direccion = input("Direccion: ").strip()
            usuario = input("Usuario: ").strip()
            password = input("Contrasenia: ").strip()
            exito, mensaje, nuevo = registrar_nuevo_cliente(nombre, apellido, dni, telefono, direccion, usuario, password, clientes)
            if exito: print(f"\n[OK] {mensaje}")
            else: print(f"\n[ERROR] {mensaje}")
        elif opcion_inicio == 0:
            print("\nGracias por usar el Videoclub!")
        else:
            print("\nOpcion no valida")

if __name__ == "__main__":
    iniciar_menu()