#Usando la lista `componentes`:

#1. agregá tres componentes nuevos;
#2. mostrá todos los componentes;
#3. calculá el stock total;
#4. mostrá los componentes con stock menor a 10;
#5. buscá un código con búsqueda secuencial;
#6. contá las comparaciones;
#7. ordená los componentes por código;
#8. realizá la misma búsqueda con búsqueda binaria;
#9. compará la cantidad de comparaciones;
#10. explicá con tus palabras por qué los resultados pueden ser diferentes.




# COMPLETAR EL DESAFÍO FINAL AQUÍ
stocker = 0
comparacion_secuencial= 0
comparacion_binaria = 0



codigousuario = input("ingrese codigo a buscar")
class componente:
  def __init__(self, codigo, nombre, categoria, stock):
      self.codigo = codigo
      self.nombre = nombre
      self.categoria = categoria
      self.stock = stock


  def MostrarST(self):
    print(f"Codigo: {self.codigo} // Nombre: {self.nombre} // Categoria: {self.categoria} // Stock: {self.stock}")


componentes = [
    componente("R001", "Resistencia 1K", "Resistencia", 30),
    componente("C001", "Capacitor 100uF", "Capacitor", 12),
    componente("CI001", "NE555", "Circuito integrado", 4),
    componente("S001", "HC-SR04", "Sensor", 3),
    componente("M001", "Motor DC", "Actuador", 8)
]

componentes.append(componente("R65", "Resistencia 12K", "Resistencia", 7))
componentes.append(componente("R777", "Resistencia 41K", "Resistencia", 1))
componentes.append(componente("R054", "Resistencia 1v", "Resistencia", 17))

componente_ord = sorted(componentes,
    key= lambda componente: componente.codigo
)

inicio = 0
fin = len(componente_ord) -1

while inicio <= fin:
  medio= (inicio + fin) // 2
  comparacion_binaria +=1

  if componente_ord[medio].codigo == codigousuario:
     componente_ord[medio].MostrarST()
     break

  elif componente_ord[medio].codigo > codigousuario:
        fin = medio -1

  else:
        inicio = medio + 1


for componen in componentes:
  componen.MostrarST()
  print()
  stocker = stocker + componen.stock

for componen in componentes:
  if componen.stock <10:
    print("-"*12 +"Componentes con menos de 10 unidades"+"-"*12)
    print (f"Nombre del componente: {componen.nombre}, Stock Actual: {componen.stock}")
print(f"Stock total: {stocker}")

for componen in componentes:
  comparacion_secuencial +=1
  if componen.codigo == codigousuario:
    print("producto encontrado: ")
    print()
    componen.MostrarST()

print(f"cantidad de secuencial: {comparacion_secuencial}")
print(f"Cantidad en binaria: {comparacion_binaria}")


#Los resultados en la busqueda secuencial y binaria pueden ser completamente diferentes.
#Esto se debe a que la busqueda secuencia recorre toda la lista completa tratando de encontrar el codigo
# y para esto realiza multiples iteraciones de codigo en la misma.
#En cuanto la la busqueda binaria, lo que hace es cortar por la mitad la lista a buscar para encontrar el resultado.
#Pero esto, requiere que la lista este completamente ordenada

