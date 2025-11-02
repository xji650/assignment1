# Primera Práctica - Inteligencia Artificial

Inteligencia Artificial (IA) 2025-2026

EPS - UdL - Igualada

XiaoLong Ji


---

## 1. Introducción

El objetivo de esta práctica es diseñar problemas de búsqueda bien definidos, implementar algoritmos de búsqueda fundamentales (Tree IDS y A*) y evaluar su rendimiento comparativo en diferentes escenarios, utilizando el framework `hlogedu-search`.

Este informe detalla el definicion de los problemas de "Kiwis and Dogs" y "N-Queens Iterative Repair", la implementación de los algoritmos de búsqueda, y una evaluación de su rendimiento en el problema de Pacman (con dos heirísticas).

---

## 2. Modelado de Problemas (Ejercicio 1)

### 2.1. The Kiwis and Dogs Problem (Ej. 1.1)

Para este problema, a partir de la plantilla con partes del codigo, se ha implementado funciones como `def get_coord(self, v)` (porque nos pide que lo hagamos), `def is_goal_state(self, state)`, `def is_valid_state(self, _)`, `def _check_conditions(self, state, conditions)` y  `@actions`.

El problema que he tenido aquí, basicamente, en la parte de diseñar funcion para acciones. Al princio de ha implementato dos acciones genéricos uno para kiwi y otro para perro. Pero ha habido problema con el coste, ya que habia que definir el parametro coste, pero como no era constante, no era posible definirlo. Para probar que el enfoque estaba bien, puse coste = 1, y funcionaba. Una vez todo correcto, hice acciones para cada uno de arestas de cada animal con su propio coste.

#### Resultados (Algoritmos del Framework)

Se ejecutaron los algoritmos base del framework (`hlog-*`) sobre el problema implementado. A continuación, se presentan los resultados obtenidos:

| Algoritmo | Max fringe size | Solution Cost | Solution Length | Search nodes expanded |
| :--- | :--- | :--- | :--- | :--- |
| **BFS** | 69 | 41 | 11 | 325 |
| **DFS** | 174 | 459 | 98 | 151 |
| **UCS** | 83 | 41 | 11 | 327 |

No aparece informacion del árbol, ya que tardaba mucho. Con el árbol, expandiría mucho más nodos y fringe que con el grafo.

#### Resultados

Analizando la gráfica, tanto BFS como UCS encontraron la solución de coste óptimo (41), ya que el coste de las acciones es uniforme (o UCS lo garantiza). BFS expandió 325 nodos, mientras que UCS expandió 327, una diferencia mínima. Por otro lado, DFS encontró rápidamente una solución (solo 151 nodos expandidos), pero con mucho coste (459), y eso demuesta que no es completa ni óptima en grafos con ciclos.

---

### 2.2. The N-Queens Iterative Repair Problem (Ej. 1.2)

Se implementó el problema de N-Queens en `problems/nqueens.py`. El objetivo es minimizar la distancia total moviendo las reinas desde una configuración inicial hasta que ninguna ataque a otra.

#### Heurística Admisible (Ej. 1.2.2)

**Descripción de la Heurística:**

La heurística implementada, `RepairHeuristic`, consiste en calcular el número mínimo de reinas que necesitas mover para resolver todos los conflictos de fila. No tiene en cuenta las diagonales, solo las filas.

El objetivo final (sin reinas atacándose) requiere que todas las reinas estén en filas únicas. Esta heurística calcula el coste mínimo para resolver solo esa parte del problema.

**Justificación de Admisibilidad:**
Esta heurística es admisible porque para resolver cada conflicto (un par de reinas atacándose), se requiere al menos un movimiento con coste 1. Al contar los pares, `h(n)` nunca será mayor que el coste real para llegar a una solución.

Dado que la heurística ignora por completo los movimientos extra necesarios para solucionar las diagonales, nunca puede sobreestimar el coste total real. Por lo tanto, $h(state) \le h^*(state)$, lo que la hace admisible.

#### Resultados (UCS vs. A*)

A continuación, se presentan los resultados de una ejecución de ejemplo para `N=4` y `seed=123`. La práctica completa requeriría un análisis con más valores de N y diferentes seeds, pero esta muestra ya ilustra las diferencias de rendimiento.

**Resultados para N=4, seed=123**
| Algoritmo | Max fringe size | Solution Cost | Solution Length | Search nodes expanded |
| :--- | :--- | :--- | :--- | :--- |
| **`graph-ucs`** | 162 | 3 | 4 | 117 |
| **`graph-astar`** | 135 | 3 | 4 | 30 |
| **`tree-ucs`** | 13652 | 3 | 4 | 1241 |
| **`tree-astar`** | 1222 | 3 | 4 | 111 |

**Justificación de los Resultados:**
En `hlog-tree-ucs` (búsqueda en árbol) explota en tamaño de frontera (13652) y nodos expandidos (1241) al no detectar estados repetidos. `hlog-tree-astar` mejora esto drásticamente (111 nodos) gracias a la heurística. Finalmente, `hlog-graph-astar` es el más eficiente por un amplio margen (solo 30 nodos), ya que combina la heurística de A* con la detección de estados repetidos (grafos), evitando re-expandir los mismos estados una y otra vez.

Resumiendo un poco, su puede ver que sea con heurística o sin, usando grafo siempre es más eficiente, ja que evita estados repetidos.

---

## 3. Implementación de Algoritmos (Ejercicio 2)

Se implementaron los siguientes algoritmos en la carpeta `algorithms/`, siguiendo los requisitos de la práctica (sucesores en orden lexicográfico, seguimiento de nodos expandidos, etc.).

* **Tree IDS (Ej. 2.1):** Implementado en `algorithms/ids.py`.

Para la implementación de TreeIDS (Iterative Deepening Search), el algoritmo se basa en un bucle principal (search) que llama repetidamente a una función de Búsqueda en Profundidad Limitada (DLS), llamada depth_limited_search. Este bucle incrementa el límite de profundidad (limit) en cada iteración, comenzando desde 0, hasta que la búsqueda de DLS devuelve una solución.

El núcleo de la búsqueda (depth_limited_search) gestiona la frontera de exploración (fringe) como una pila LIFO (Last-In, First-Out), utilizando una lista estándar de Python y sus métodos append() (para añadir) y pop() (para extraer). Esto implementa la estrategia de Búsqueda en Profundidad (DFS).

Para cumplir con el requisito de expandir los nodos en orden lexicográfico, la implementación primero obtiene y ordena la lista de sucesores (sorted(...)), y luego la invierte (reversed(...)) antes de añadirlos a la pila uno por uno. Esto garantiza que el primer nodo en ser extraído de la pila (pop()) sea el que corresponde al primer sucesor en orden lexicográfico. Además, se lleva un contador global (self.expanded_nodes) para asignar los atributos expanded_order y location a cada nodo hijo en el momento de su generación.

* **Tree A\* (Ej. 2.2):** Implementados en `algorithms/astar.py`.

Para la implementación de A*, se ha enfocado sobre todo en fringe, ya que es el componente central. Se ha utilizado una cola de prioridad, implementada mediante el módulo heapq de Python.

Esta cola de prioridad no almacena directamente los nodos, sino tuplas que permiten al heapq ordenarlos correctamente. 

Se ha centrado en el valor de la función de evaluación $f(n)$, que se calcula sumando el coste del camino real desde el inicio ($g(n)$, node.path_cost) y el valor de la heurística ($h(n)$, self.heuristic(node.state)).

Además, para garantizar un desempate estable (FIFO) y evitar errores de Python al comparar dos objetos Node con el mismo valor $f(n)$, la tupla incluye un contador de generación (_generated_count). Así, la tupla que se inserta en la frontera tiene la forma: (f_cost, generation_count, node).


### Problemas

El framework hlogedu-search intenta cargar archivo (ej. algorithms/astar.py) como un script. Cuando Python ejecuta ese script, su "ruta de búsqueda" de módulos (sys.path) no incluye la carpeta algorithms/ donde reside el propio script.

Por lo tanto, cuando el script llega a las líneas: from search_algorithm import SearchAlgorithm from node import Node Python no encuentra esos archivos (porque están en algorithms/, no en la raíz del proyecto) y lanza un ModuleNotFoundError.

2. Solución:

El bloque de código soluciona esto manualmente:

- current_dir = os.path.dirname(os.path.abspath(__file__)): Obtiene la ruta absoluta a la carpeta que contiene este archivo (o sea, .../assignment1/algorithms).

- if current_dir not in sys.path: Comprueba si esa ruta (la carpeta algorithms/) ya está en la lista de lugares donde Python busca módulos.

- sys.path.append(current_dir): Si no lo está, la añade a la lista.

Resultado: Después de ejecutar este bloque, ya no me salta error, pero sigo sin podere ejecutar mi codigo con el framework.


---

## 4. Evaluación en Pacman (Ejercicio 3)

### 4.1. Heurísticas (Ej. 3.1)

Se implementaron las heurísticas de Manhattan y Euclidean dentro del fichero `problems/pacman.py`.

* **Manhattan Distance:** 

Calcula la distancia Manhattan desde Pacman a la comida. 

h(n) = |pac_r - food_r| + |pac_c - food_c|

Es admisible porque Pacman se mueve en 4 direcciones (coste 1)
    y no puede moverse en diagonal. Esta es la distancia real más corta
    en una cuadrícula sin paredes. Como las paredes solo pueden
    hacer el camino más largo, esta heurística NUNCA sobreestima el
    coste real.

* **Euclidean Distance:** 

Calcula la distancia Euclidiana (línea recta) a la comida.

h(n) = sqrt((pac_r - food_r)^2 + (pac_c - food_c)^2)

Calcula la distancia Euclidiana (línea recta) a la comida.
    h(n) = sqrt((pac_r - food_r)^2 + (pac_c - food_c)^2)

    Es admisible porque la distancia en línea recta es, por definición,
    la distancia más corta posible entre dos puntos. Cualquier
    camino real en la cuadrícula (con o sin paredes) será
    igual o más largo que esta distancia. Nunca sobreestima.


