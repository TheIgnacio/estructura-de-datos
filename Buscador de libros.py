class Libro:
    def __init__(self,codigo,titulo,categoria,cantidad):
        self.codigo = codigo
        self.titulo = titulo
        self.categoria = categoria
        self.cantidad = cantidad

    def mostrar(self):
        print(f"Codigo: {self.codigo} // Titulo: {self.titulo} // Categoria: {self.categoria} // Cantidad: {self.cantidad}")

    def disponible(self):
            if self.cantidad >0:
                return True
            else:
                return False

def busqueda_binaria(lista, codigo):
    inicio = 0
    fin = len(lista) - 1
    comparaciones = 0

    while inicio <= fin:

        medio = (inicio + fin) // 2
        comparaciones += 1

        if lista[medio].codigo == codigo:
            return lista[medio], comparaciones

        elif lista[medio].codigo > codigo:
            fin = medio - 1

        else:
            inicio = medio + 1

    return None, comparaciones
    

def buscar_codigo(libros,codigo):
    busqueda_secuencial = 0
    for libro in libros:
    
        busqueda_secuencial += 1
        if codigo == libro.codigo:
            return libro,busqueda_secuencial

    return None,busqueda_secuencial

def buscar_titulo(libros,titulo_buscado):
    for libro in libros:
        if titulo_buscado == libro.titulo:
            return libro 
    return None

def buscar_categoria(libros,categoria_buscada):
    ret = []
    for libro in libros:
        if categoria_buscada == libro.categoria:
            ret.append(libro)
    return ret



def buscar_stock_bajo(libros,limite):
    ret = []
    for libro in libros:
        if libro.cantidad <= limite:
            ret.append(libro)
    return ret
        

 




libros= []



libros.append(Libro("L004", "El Principito", "Infantil", 10))
libros.append(Libro("L001", "Don Quijote", "Novela", 5))
libros.append(Libro("L006", "1984", "Ciencia ficción", 8))
libros.append(Libro("L002", "Cien años de soledad", "Novela", 7))
libros.append(Libro("L005", "Harry Potter", "Fantasía", 12))
libros.append(Libro("L003", "El Hobbit", "Fantasía", 6))


lista_ord = sorted(libros, key = lambda libro: libro.codigo)
#lista_ord = libros.sort(key = lambda libro: libro.codigo)


Codigo_buscar =input("Ingrese el codigo del libro a buscar: ").upper()
Titulo_buscado =input("ingrese el titulo del libro a buscar: ").title()
categoria_buscada=input("Ingrese la categoria del libro a buscar: ").title()
stock_buscado = int(input("Ingrese el stock a buscar: "))


##busquedas de libro

encontrado_categoria= buscar_categoria(libros, categoria_buscada)

libroBi, comparacionesBi =busqueda_binaria(lista_ord, Codigo_buscar)

libroSec, comparacionesSec = buscar_codigo(libros, Codigo_buscar)

libroTitulo = buscar_titulo(libros,Titulo_buscado)

libros_stock = buscar_stock_bajo(libros,stock_buscado)

######################################################################################

print()
print("=" * 72)
print("Libros con el titulo buscado")
if libroTitulo != None:
        libroTitulo.mostrar()
else:
    print("No se encontro el libro")
print()
print("=" * 72)

print(f"Libros con Stock bajo: ")
for libro in libros_stock:
    libro.mostrar()

print()
print("=" * 72)

print(f"Libros con la categoria buscada: ")
for libro in encontrado_categoria:
    libro.mostrar()

print()
print("=" * 72)

print("Resultado de la busqueda por codigo:")

if libroSec != None:
    libroSec.mostrar()
else:
    print("Libro no encontrado")

print()
print("=" * 72)

print("Comparaciones secuenciales:", comparacionesSec)

if libroBi != None:
    libroBi.mostrar()
else:
    print("Libro no encontrado")

print("Comparaciones binarias:", comparacionesBi)

