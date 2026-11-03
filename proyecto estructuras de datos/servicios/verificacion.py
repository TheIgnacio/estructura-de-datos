import sys
from pathlib import Path

base_dir = Path(__file__).resolve().parent.parent
if str(base_dir) not in sys.path:
    sys.path.append(str(base_dir))

from modelo.clientes import Cliente

def autenticar_usuario(usuario: str, password: str, lista_clientes: list[Cliente] = None) -> Cliente | None:
    """
    Busca si existe un cliente con el usuario y contraseña proporcionados.

    Retorna:
        Cliente si las credenciales son válidas, o None en caso contrario.
    """
    if lista_clientes is None:
        lista_clientes = Cliente.cargar_desde_json()

    usuario_limpio = usuario.strip().lower()
    password_limpio = password.strip()

    for cliente in lista_clientes:
        if cliente.usuario.lower() == usuario_limpio and cliente.password == password_limpio:
            return cliente
    return None


def registrar_nuevo_cliente(
    nombre: str,
    apellido: str,
    dni: str,
    telefono: str,
    direccion: str,
    usuario: str,
    password: str,
    lista_clientes: list[Cliente] = None
) -> tuple[bool, str, Cliente | None]:
    """
    Registra un nuevo cliente con rol 'usuario', validando que no se repitan DNI ni usuario.

    Retorna:
        (éxito: bool, mensaje: str, nuevo_cliente: Cliente | None)
    """
    if lista_clientes is None:
        lista_clientes = Cliente.cargar_desde_json()

    dni_limpio = dni.strip()
    usuario_limpio = usuario.strip().lower()

    # Validaciones de existencia previa
    for c in lista_clientes:
        if c.dni == dni_limpio:
            return False, f"El DNI '{dni_limpio}' ya se encuentra registrado.", None
        if c.usuario.lower() == usuario_limpio:
            return False, f"El nombre de usuario '{usuario_limpio}' ya está en uso.", None

    try:
        nuevo_cliente = Cliente(
            nombre=nombre,
            apellido=apellido,
            dni=dni_limpio,
            telefono=telefono,
            direccion=direccion,
            peliculas_reservadas=[],
            usuario=usuario_limpio,
            password=password.strip(),
            rol="usuario"
        )
        lista_clientes.append(nuevo_cliente)
        Cliente.guardar_en_json(lista_clientes)
        return True, "Cliente registrado con éxito.", nuevo_cliente
    except ValueError as e:
        return False, f"Error en los datos ingresados: {e}", None


# Prueba rápida local
if __name__ == "__main__":
    print("Probando autenticación:")
    admin = autenticar_usuario("admin", "admin123")
    if admin:
        print(f"[OK] Admin logeado: {admin.datos_clientes()} | Rol: {admin.rol}")
    else:
        print("[ERROR] No se pudo autenticar al admin")

    usuario = autenticar_usuario("lucas.gonzalez", "123")
    if usuario:
        print(f"[OK] Usuario logeado: {usuario.datos_clientes()} | Rol: {usuario.rol}")
    else:
        print("[ERROR] No se pudo autenticar al usuario común")
