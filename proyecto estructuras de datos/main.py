from servicios.persistencia import cargar_catalogo
from ui.menu import Menu
def main():

    catalogo = cargar_catalogo("datos/Peliculas.json")

    menu = Menu(catalogo, archivo_json="datos/Peliculas.json")