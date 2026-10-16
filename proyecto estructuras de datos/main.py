from servicios.persistencia import cargar_catalogo
from UX.Menu import Menu
def main():

    catalogo = cargar_catalogo("datos/Peliculas.json")

    menu = Menu(catalogo, archivo_json="datos/Peliculas.json")