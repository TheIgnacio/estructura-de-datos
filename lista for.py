""" Mini práctica
1.  Creá una lista con cinco mediciones numéricas.
2.  Mostrá todos sus valores con un ciclo for.
3.  Calculá el total, el promedio, el máximo y el mínimo.
4.  Agregá una nueva medición y volvé a calcular los resultados """
mediciones = [24,10,12,32,41]

for medicion in mediciones:
    print(medicion)

total= sum(mediciones)
promedio= total / len(mediciones)
print(f"promedio = {promedio}")
maximo = print(f"Máximo: {max(mediciones)}")
minimo = print(f"Mínimo: {min(mediciones)}")

mediciones.append(100)

for medicion in mediciones:
    print(medicion)

total= sum(mediciones)
promedio= total / len(mediciones)
print(f"promedio = {promedio}")
maximo = max(mediciones)
minimo = min(mediciones)

print(f"Máximo: {maximo}")
print(f"Mínimo: {minimo}")

"""  Creá una pila de acciones con los valores: "Abrir archivo", "Editar", "Guardar". Extraé una acción y observá cuál 
sale.
2.  Creá una cola de tres estudiantes que esperan atención. Extraé un estudiante y observá cuál sale.
3.  Explicá con tus palabras por qué los resultados son diferentes.
 """

acciones = ["Abrir archivo", "Editar", "Guardar"]
print(acciones)
sacar_accion = acciones.pop(1)

for accion in acciones:
    print (f"pendientes: {accion}")


from collections import deque
estudiantes = deque(["juan","ana","carolina","oriana"])
print(f"Estudiantes: {estudiantes}")
estudiantes = estudiantes.popleft()

print(estudiantes)

""" Historial de acciones para implementar Deshacer (CTRL+Z)   ==
Entraria una pila, ya que se necesita que se almacene elementos en la memoria para despues poder realizar un UNDO 
y restablecer lo ultimo borrado o eliminado """

""" Personas esperando atención por orden de llegada. ===
En este caso usaria una estructura de tipo cola,por que seria por orden de llegada. 
Se atenderia al primer paciente en llegar y despues al siguiente y asi. hasta que no quede ninguno pendiente. """

""" Red de rutas entre distintas ciudades. ===
En este caso se usaria lo que serian grafos, ya que cada nodo seria como una ciudad y la union de ellos seria la conexion 
entre estas o si no un camino para llegar a estas mismas derivando a otras ciudades. """

""" Registro ordenado de mediciones de un sensor ===
En este caso se usaria una estructura de tipo lista, ya que se necesita almacenar los datos de manera ordenada y
poder acceder a ellos de manera secuencial para su análisis y procesamiento. Las listas permiten agregar, eliminar y modificar 
elementos de manera eficiente, lo que es útil para mantener un registro actualizado de las mediciones del sensor. 
Además, se pueden realizar operaciones como calcular el promedio, máximo y mínimo de las mediciones almacenadas en la lista.     """   


""" Autoevaluación
1.  Definí con tus palabras qué es una estructura de datos.
2.  Mencioná una diferencia entre una lista, una pila y una cola.
3.  Dá un ejemplo cotidiano de LIFO y otro de FIFO.
4.  ¿Qué operación realiza pop en el ejemplo de la pila?
5.  ¿Por qué deque es conveniente para implementar colas?
6.  Elegí una estructura para representar rutas entre ciudades y explicá por qué.
7.  ¿Por qué no existe una única estructura de datos que sea la mejor para todos los problemas? """

""" 1=Una estructura de datos es una forma de organizar y almacenar datos de manera eficiente para almacenar,acceder y manipular de forma optima la informacion.
2= Una lista es una coleccion de elementos para almacenar de manera ordenada y editable. La pila es una estructura LIFO (Last In First Out) 
donde el ultimo elemento agregado es el primero en salir. En cuanto la cola es al contrario de la pila, en este caso lo primero que llega es lo
primero en salir. 

3= Un ejemplo de LIFO seria el control+z  de la pc, este revierte el ultimo cambio realizado, y el fifo puede ser una fila de personas
esperando a que las atiendan ya que primero atienden al primero en llegar

4= La operacion pop en el ejemplo de la pila elimina el ultimo elemento agregado a la pila y lo devuelve como resultado.
5= Deque es conveniente para implementar colas porque permite agregar y eliminar elementos de ambos extremos de manera eficiente, 
lo que facilita la implementación de una estructura FIFO (First In First Out) para manejar la atención de los estudiantes.
6= Para representar rutas entre ciudades se puede utilizar una estructura de tipo grafo, ya que permite modelar las conexiones entre diferentes nodos
 (ciudades) y sus relaciones.
 7= No existe una única estructura de datos que sea la mejor para todos los problemas porque cada problema tiene sus propias características y requisitos.
Algunas estructuras de datos son más eficientes para ciertos tipos de operaciones, mientras que otras son más adecuadas para diferentes escenarios. 
Por lo tanto, es importante elegir la estructura de datos adecuada según las necesidades específicas del problema a resolver. """


