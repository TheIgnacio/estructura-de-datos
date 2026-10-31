# 🎬 Videoclub — TP Final de Estructuras de Datos

## 📌 Descripción del proyecto

Sistema de gestión de un videoclub desarrollado en Python como aplicación de consola.

Permite administrar un catálogo de películas y clientes, organizar las películas por categorías y realizar búsquedas mediante estructuras de datos. La información se almacena en archivos JSON, por lo que se conserva al cerrar el programa.

Trabajo final de la materia **Estructuras de Datos — UNaB**.

## 🎯 Objetivos

- Aplicar los conceptos de estructuras de datos estudiados en la materia.
- Implementar listas, árboles, pilas y colas.
- Organizar el código mediante módulos y programación orientada a objetos.
- Analizar y comparar la eficiencia de diferentes métodos de búsqueda.
- Practicar el trabajo colaborativo mediante Git y GitHub.

## 👨‍💻 Integrantes

- Carina Ruiz
- Hernan Alegre
- Gisela Morales
- Mariana Gimenez
- Eric Ignacio Claros

## 🛠️ Tecnologías utilizadas

- **Lenguaje:** Python 3.
- **Editor:** Visual Studio Code.
- **Control de versiones:** Git.
- **Repositorio remoto:** GitHub.
- **Persistencia de datos:** archivos JSON.

No se requieren librerías externas.

## ▶️ Cómo ejecutar el proyecto

1. Clonar o descargar el repositorio.
2. Abrir la carpeta del proyecto en Visual Studio Code.
3. Abrir una terminal.
4. Ingresar a la carpeta que contiene `main.py`:

   ```bash
   cd "proyecto estructuras de datos"
   ```

5. Ejecutar el programa:

   ```bash
   python main.py
   ```

   En Windows también se puede utilizar:

   ```bash
   py main.py
   ```

Para probar las estructuras de datos por separado (cada módulo trae una demostración):

```bash
python estructura/arbol_bst.py
python estructura/arbol_categorias.py
python estructura/pila.py
python estructura/cola.py
```

## 📋 Menú del programa

| Opción | Acción |
|---|---|
| 1 | Ver lista de películas |
| 2 | Buscar por categoría (cuenta las comparaciones) |
| 3 | Buscar por título (cuenta las comparaciones) |
| 4 | Agregar película |
| 5 | Eliminar película |
| 6 | Modificar película |
| 7 | Eliminar cliente |
| 8 | Explorar por categorías (árbol de categorías) |
| 0 | Salir |

Las altas, bajas y modificaciones se guardan automáticamente en los archivos JSON.

## 🗂️ Estructura del proyecto

El proyecto está organizado en módulos para separar la interfaz de usuario, los modelos, las estructuras de datos y los archivos de información.

```text
estructura-de-datos/
├── .gitignore
├── README.md
├── USO-DE-IA.md
└── proyecto estructuras de datos/
    ├── main.py
    ├── UX/
    │   ├── __init__.py
    │   └── Menu.py
    ├── datos/
    │   ├── clientes.json
    │   └── peliculas.json
    ├── estructura/
    │   ├── __init__.py
    │   ├── arbol_bst.py
    │   ├── arbol_categorias.py
    │   ├── cola.py
    │   └── pila.py
    ├── modelo/
    │   ├── __init__.py
    │   ├── clientes.py
    │   └── pelicula.py
    └── servicios/
        ├── __init__.py
        └── persistencia.py
```

### Descripción de los archivos y carpetas

| Archivo o carpeta | Descripción |
|---|---|
| `main.py` | Punto de entrada del programa. |
| `UX/Menu.py` | Menú de consola y la interacción con el usuario. |
| `modelo/pelicula.py` | Clase `Pelicula`: atributos privados con `@property`, validaciones, y carga y guardado en JSON. |
| `modelo/clientes.py` | Clase `Cliente`: datos, reservas de películas, y carga y guardado en JSON. |
| `estructura/arbol_categorias.py` | Árbol general de categorías y subcategorías. |
| `estructura/arbol_bst.py` | Árbol binario de búsqueda, recorridos y comparación de eficiencia. |
| `estructura/pila.py` | Pila implementada con nodos enlazados. |
| `estructura/cola.py` | Cola implementada con nodos enlazados y tamaño máximo. |
| `servicios/persistencia.py` | Funciones de carga de datos de la primera versión. Hoy la lectura y el guardado se hacen desde las clases `Pelicula` y `Cliente`. |
| `datos/peliculas.json` | Catálogo de 40 películas. |
| `datos/clientes.json` | Datos de los clientes y sus reservas. |
| `USO-DE-IA.md` | Detalle del uso de herramientas de inteligencia artificial. |
| `.gitignore` | Indica qué archivos y carpetas debe ignorar Git. |

## ⚙️ Funcionalidades del sistema

Los estados indican el avance del proyecto y se actualizan a medida que se completan las implementaciones.

| Funcionalidad | Estructura o recurso | Estado |
|---|---|---|
| Listar películas | Lista | Implementado |
| Buscar películas por título y por categoría | Lista y búsqueda secuencial | Implementado |
| Contabilizar comparaciones en las búsquedas | Contador de comparaciones | Implementado |
| Agregar, eliminar y modificar películas (con validaciones) | Lista | Implementado |
| Guardar y cargar información | Archivos JSON | Implementado |
| Eliminar clientes | Lista | Implementado |
| Explorar películas por categorías | Árbol general | Implementado |
| Buscar películas por código | Árbol binario de búsqueda | Módulo implementado; falta integrarlo al menú |
| Obtener un listado ordenado | Recorrido inorden del árbol | Módulo implementado; falta integrarlo al menú |
| Comparar la eficiencia de búsquedas | Lista y árboles | Implementado en `arbol_bst.py`; falta integrarlo al menú |
| Deshacer la última operación | Pila | Clase implementada; falta integrarla al menú |
| Historial de las últimas búsquedas | Cola | Clase implementada; falta integrarla al menú |
| Agregar y modificar clientes, gestionar reservas | Lista | Pendiente |
| Consultar clientes morosos | Lista | Pendiente |

## 🧱 Estructuras de datos utilizadas

### 1. Listas

**Descripción:** permiten almacenar una colección ordenada de elementos y recorrerla para consultar, agregar o quitar información.

**Aplicación en el proyecto:**

- Almacenar el catálogo de películas.
- Mantener la colección de clientes.
- Registrar las reservas de cada cliente.
- Recorrer el catálogo para buscar películas.
- Comparar la búsqueda secuencial con la búsqueda mediante árboles.

La búsqueda secuencial examina los elementos hasta encontrar el buscado o llegar al final de la lista.

### 2. Árbol general de categorías

**Archivo:** `estructura/arbol_categorias.py`

**Descripción:** estructura jerárquica en la que cada nodo puede tener cualquier cantidad de hijos.

**Aplicación en el proyecto:**

- Organizar películas por categoría y subcategoría.
- Mostrar el árbol desde la opción 8 del menú, con la cantidad de películas de cada subcategoría.
- Buscar categorías y calcular la altura del árbol.

Jerarquía de categorías:

```text
Cine
├── Ciencia Ficción
│   ├── Comedia
│   ├── Aventura científica
│   ├── Ciberpunk
│   └── Espacio
├── Crimen
│   ├── Policial
│   └── Mafia
├── Acción
│   ├── Superhéroes
│   └── Histórico
├── Drama
│   ├── Psicológico
│   ├── Social
│   └── Histórico
├── Terror
│   └── Psicológico
├── Aventura
│   └── Fantasía
└── Animación
    └── Fantasía
```

### 3. Árbol binario de búsqueda (BST)

**Archivo:** `estructura/arbol_bst.py`

**Descripción:** árbol en el que cada nodo tiene como máximo dos hijos. Las claves menores se ubican a la izquierda y las mayores a la derecha, de modo que cada comparación descarta media rama.

**Aplicación en el proyecto:**

- Buscar películas por código contando las comparaciones realizadas.
- Obtener un listado ordenado mediante el recorrido inorden (también hay preorden y postorden).
- Calcular la altura y la cantidad de nodos.
- Construir árboles por inserción sucesiva y árboles balanceados.

#### Comparación de eficiencia

Los códigos del catálogo ya vienen ordenados (`MOV-001` a `MOV-040`), por lo que al insertarlos en ese orden el árbol queda degenerado, como una lista. Resultado al buscar `MOV-035` con 40 películas:

| Estructura | Altura | Comparaciones |
|---|---:|---:|
| Lista, búsqueda secuencial | — | 35 |
| BST sin balancear | 39 | 35 |
| BST balanceado | 5 | 5 |

Un árbol binario de búsqueda solo es eficiente si está equilibrado. Con 40 elementos, el árbol balanceado pasa de 35 a 5 comparaciones, aproximadamente log₂(40).

### 4. Pila

**Archivo:** `estructura/pila.py`

**Descripción:** estructura LIFO (*Last In, First Out*), en la que el último elemento agregado es el primero en salir. Está implementada con nodos enlazados: `apilar`, `desapilar`, `ver_tope`, `esta_vacia` y `tamanio`.

**Aplicación prevista:**

- Registrar las últimas operaciones realizadas.
- Deshacer la última operación, conservando la información necesaria para revertirla.

### 5. Cola

**Archivo:** `estructura/cola.py`

**Descripción:** estructura FIFO (*First In, First Out*), en la que el primer elemento agregado es el primero en salir. Está implementada con nodos enlazados y un tamaño máximo: al superarlo, se descarta el elemento más antiguo.

**Aplicación prevista:**

- Guardar el historial de las últimas búsquedas, conservando solo las más recientes.

## 💾 Persistencia de datos

El proyecto utiliza archivos JSON para almacenar información entre ejecuciones.

- `peliculas.json`: datos del catálogo de películas.
- `clientes.json`: datos de los clientes y sus reservas.
- Las clases `Pelicula` y `Cliente` incluyen los métodos para convertirse a diccionario y para cargarse y guardarse en JSON.

Cada alta, baja o modificación realizada desde el menú se guarda en el archivo correspondiente.

## 🧪 Pruebas recomendadas

- Listar las películas disponibles.
- Buscar un título existente y otro inexistente.
- Agregar una película, cerrar el programa, volver a abrirlo y comprobar que sigue en el catálogo.
- Intentar agregar un código repetido y datos inválidos (texto en el año, año menor a 1888).
- Modificar y eliminar una película.
- Explorar las categorías y comprobar la cantidad de películas de cada una.
- Ejecutar los módulos de árboles, pila y cola y revisar los resultados.
- Ingresar texto en lugar de un número en el menú.

## 📚 Contexto académico

Trabajo Práctico Final de la materia **Estructuras de Datos — UNaB**.

El proyecto integra conceptos de programación, listas, árboles, pilas, colas, búsquedas, recorridos, persistencia y análisis de eficiencia mediante un caso práctico de gestión de un videoclub.

## 🤖 Uso de inteligencia artificial

Detallado en `USO-DE-IA.md`.

## 📌 Estado general del proyecto

**En desarrollo.**

Funcionan la gestión de películas, el guardado en JSON, la eliminación de clientes y la exploración por categorías. Queda integrar al menú el árbol binario de búsqueda, la pila y la cola, completar la gestión de clientes (alta, modificación, reservas y morosos) y realizar pruebas del funcionamiento completo.
