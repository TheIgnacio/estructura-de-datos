# 🎬 Videoclub — TP Final de Estructuras de Datos

## 📌 Descripción del proyecto

Sistema de gestión de un videoclub desarrollado en Python como aplicación de consola.

Permite administrar un catálogo de películas y clientes, organizar las películas por categorías, buscar mediante estructuras de datos y reservar películas desde una cuenta de usuario. El sistema tiene inicio de sesión con dos roles (administrador y usuario) y guarda la información en archivos JSON.

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

## 🔐 Acceso al sistema

Al iniciar, el programa ofrece:

| Opción | Acción |
|---|---|
| 1 | Iniciar sesión (3 intentos) |
| 2 | Registrarse como nuevo cliente |
| 0 | Salir |

El menú que se muestra depende del rol de la cuenta: **administrador** o **usuario**. El registro crea cuentas con rol de usuario y valida que el DNI y el nombre de usuario no estén repetidos.

## 📋 Menús del programa

### Menú de administrador

| Opción | Acción | Estructura |
|---|---|---|
| 1 | Ver lista de películas | Lista |
| 2 | Buscar por categoría, sin distinguir tildes ni mayúsculas (cuenta las comparaciones) | Búsqueda secuencial |
| 3 | Buscar por título (cuenta las comparaciones) | Búsqueda secuencial |
| 4 | Agregar película | Lista |
| 5 | Eliminar película | Lista |
| 6 | Modificar película | Lista |
| 7 | Eliminar cliente | Lista |
| 8 | Explorar por categorías | Árbol general |
| 9 | Listar todo ordenado por código | BST, recorrido inorden |
| 10 | Buscar por código (informa los pasos) | BST balanceado |
| 11 | Deshacer la última operación | Pila |
| 12 | Ver historial de consultas | Cola |
| 0 | Cerrar sesión | — |

### Menú de usuario

| Opción | Acción | Estructura |
|---|---|---|
| 1 | Ver el catálogo completo | Lista |
| 2 | Buscar por título | Búsqueda secuencial |
| 3 | Buscar por categoría, sin distinguir tildes ni mayúsculas | Búsqueda secuencial |
| 4 | Explorar el catálogo por categorías | Árbol general |
| 5 | Buscar por código | BST balanceado |
| 6 | Reservar una película | Lista |
| 7 | Ver mis películas reservadas | Lista |
| 8 | Cancelar una reserva | Lista |
| 9 | Ver mis datos de perfil | — |
| 10 | Ver mi historial de consultas | Cola |
| 0 | Cerrar sesión | — |

Las altas, bajas, modificaciones y reservas se guardan automáticamente en los archivos JSON. Al reservar una película se descuenta una unidad de stock, y al cancelar la reserva se devuelve.

## 🗂️ Estructura del proyecto

El proyecto está organizado en módulos para separar la interfaz de usuario, los modelos, las estructuras de datos, los servicios y los archivos de información.

```text
estructura-de-datos/
├── .gitignore
├── README.md
├── USO-DE-IA.md
└── proyecto estructuras de datos/
    ├── .gitignore
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
        ├── persistencia.py
        └── verificacion.py
```

### Descripción de los archivos y carpetas

| Archivo o carpeta | Descripción |
|---|---|
| `main.py` | Punto de entrada del programa. |
| `UX/Menu.py` | Pantalla de acceso, menú de administrador y menú de usuario. |
| `modelo/pelicula.py` | Clase `Pelicula`: atributos privados con `@property`, validaciones, y carga y guardado en JSON. |
| `modelo/clientes.py` | Clase `Cliente`: datos, usuario, rol, reservas, y carga y guardado en JSON. |
| `estructura/arbol_categorias.py` | Árbol general de categorías y subcategorías. |
| `estructura/arbol_bst.py` | Árbol binario de búsqueda, recorridos y comparación de eficiencia. |
| `estructura/pila.py` | Pila implementada con nodos enlazados. |
| `estructura/cola.py` | Cola implementada con nodos enlazados y tamaño máximo. |
| `servicios/verificacion.py` | Autenticación de usuarios y registro de nuevos clientes. |
| `servicios/persistencia.py` | Funciones de carga de datos de la primera versión. Hoy la lectura y el guardado se hacen desde las clases `Pelicula` y `Cliente`. |
| `datos/peliculas.json` | Catálogo de 40 películas. |
| `datos/clientes.json` | Datos de los clientes, sus cuentas y sus reservas. |
| `USO-DE-IA.md` | Detalle del uso de herramientas de inteligencia artificial. |
| `.gitignore` | Indica qué archivos y carpetas debe ignorar Git (por ejemplo, las carpetas `__pycache__`). |

## ⚙️ Funcionalidades del sistema

Los estados indican el avance del proyecto y se actualizan a medida que se completan las implementaciones.

| Funcionalidad | Estructura o recurso | Estado |
|---|---|---|
| Listar películas | Lista | Implementado |
| Buscar películas por título y por categoría | Lista y búsqueda secuencial | Implementado |
| Contabilizar comparaciones en las búsquedas | Contador de comparaciones | Implementado |
| Agregar, eliminar y modificar películas (con validaciones) | Lista | Implementado |
| Guardar y cargar información | Archivos JSON | Implementado |
| Inicio de sesión con roles y registro de clientes | Lista y archivos JSON | Implementado |
| Reservar y cancelar películas, con control de stock | Lista | Implementado |
| Eliminar clientes | Lista | Implementado |
| Explorar películas por categorías | Árbol general | Implementado |
| Buscar películas por código | Árbol binario de búsqueda | Implementado |
| Obtener un listado ordenado | Recorrido inorden del árbol | Implementado |
| Comparar la eficiencia de búsquedas | Lista y árboles | Implementado en `arbol_bst.py` |
| Deshacer la última operación sobre películas | Pila | Implementado |
| Historial de las últimas consultas | Cola | Implementado |
| Modificar los datos de un cliente | Lista | Pendiente |
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
- Mostrar el árbol desde el menú, con la cantidad de películas de cada subcategoría.
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

- Buscar películas por código e informar cuántos pasos se necesitaron.
- Obtener un listado ordenado por código mediante el recorrido inorden (también hay preorden y postorden).
- Calcular la altura y la cantidad de nodos.
- Construir árboles por inserción sucesiva y árboles balanceados. El menú utiliza el balanceado.

#### Comparación de eficiencia

Los códigos del catálogo ya vienen ordenados (`MOV-001` a `MOV-040`), por lo que al insertarlos en ese orden el árbol queda degenerado, como una lista. Resultado al buscar `MOV-035` con 40 películas:

| Estructura | Altura | Comparaciones |
|---|---:|---:|
| Lista, búsqueda secuencial | — | 35 |
| BST sin balancear | 39 | 35 |
| BST balanceado | 5 | 5 |

Un árbol binario de búsqueda solo es eficiente si está equilibrado. Con 40 elementos, el árbol balanceado pasa de 35 a 5 comparaciones, aproximadamente log₂(40). Por eso el menú arma el árbol balanceado antes de buscar.

### 4. Pila

**Archivo:** `estructura/pila.py`

**Descripción:** estructura LIFO (*Last In, First Out*), en la que el último elemento agregado es el primero en salir. Está implementada con nodos enlazados: `apilar`, `desapilar`, `ver_tope`, `esta_vacia` y `tamanio`.

**Aplicación en el proyecto:**

- Cada alta, baja o modificación de una película que hace el administrador se apila junto con la información necesaria para revertirla.
- La opción "Deshacer la última operación" desapila la acción más reciente y la revierte: quita la película agregada, restaura la eliminada o recupera los datos anteriores de la modificada.

Se eligió una pila porque lo último que se hizo es lo primero que se debe deshacer.

### 5. Cola

**Archivo:** `estructura/cola.py`

**Descripción:** estructura FIFO (*First In, First Out*), en la que el primer elemento agregado es el primero en salir. Está implementada con nodos enlazados y un tamaño máximo: al superarlo, se descarta el elemento más antiguo.

**Aplicación en el proyecto:**

- Guardar el historial de las últimas 5 películas consultadas por cada sesión.
- Al llenarse, la consulta más antigua se descarta para dar lugar a la más reciente.

## 💾 Persistencia de datos

El proyecto utiliza archivos JSON para almacenar información entre ejecuciones.

- `peliculas.json`: datos del catálogo de películas.
- `clientes.json`: datos de los clientes, sus cuentas y sus reservas.
- Las clases `Pelicula` y `Cliente` incluyen los métodos para convertirse a diccionario y para cargarse y guardarse en JSON.

Cada alta, baja, modificación o reserva realizada desde el menú se guarda en el archivo correspondiente.

**Limitación conocida:** las contraseñas se guardan en texto plano en `clientes.json`. Es una simplificación válida para un trabajo académico; en un sistema real deberían almacenarse con un hash.

## 🧪 Pruebas recomendadas

- Iniciar sesión con credenciales incorrectas y comprobar que se bloquea al tercer intento.
- Registrar un cliente nuevo e intentar repetir el DNI o el usuario.
- Como administrador: agregar, modificar y eliminar una película, y deshacer cada operación.
- Intentar agregar un código repetido y datos inválidos (texto en el año, año menor a 1888).
- Cerrar el programa, volver a abrirlo y comprobar que los cambios se conservan.
- Buscar por código con el BST y comparar los pasos con la búsqueda secuencial.
- Consultar varias películas y revisar que el historial conserve solo las últimas 5.
- Como usuario: reservar una película, comprobar que baja el stock, intentar reservarla otra vez y cancelarla.
- Intentar reservar una película sin stock.
- Ejecutar los módulos de árboles, pila y cola y revisar los resultados.
- Ingresar texto en lugar de un número en los menús.

## 📚 Contexto académico

Trabajo Práctico Final de la materia **Estructuras de Datos — UNaB**.

El proyecto integra conceptos de programación, listas, árboles, pilas, colas, búsquedas, recorridos, persistencia y análisis de eficiencia mediante un caso práctico de gestión de un videoclub.

## 🤖 Uso de inteligencia artificial

Detallado en `USO-DE-IA.md`.

## 📌 Estado general del proyecto

**En desarrollo.**

Funcionan el inicio de sesión con roles, la gestión de películas y reservas, el guardado en JSON y las cuatro estructuras (listas, árboles, pila y cola) integradas al menú. Queda completar la gestión de clientes (modificar datos y consultar morosos) y realizar pruebas del funcionamiento completo.
