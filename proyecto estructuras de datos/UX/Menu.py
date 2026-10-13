
opcion = -1
while opcion != 0:

    print("1. Ver lista de Peliculas 1")
    print("2. Buscar por Categoria 2 ")
    print("3. Agregar Pelicula 3")
    print("4. Eliminar Pelicula 4")
    print("5. Modificar Pelicula 5")
    print()

    print("0. salir 0")
    opcion = int(input("Ingrese una opcion: "))

    if opcion == 1:
        print()
        print("Lista de Peliculas")
        print()
    
    elif opcion == 2:
        print()
        print("Buscada por categoria")
        print()

    elif opcion == 3:
        print()
        print("agregar pelicula")
        print()

    elif opcion == 4:
        print()
        print("pelicula eliminada")
        print()

    elif opcion == 5:
        print()
        print("Modificar pelicula")
        print()

    elif opcion == 0:
        print("salir")
        exit()

    else:
        print("opcion no valida")

        