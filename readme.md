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

#### Justificación de los Resultados

Analizando la gráfica, tanto BFS como UCS encontraron la solución de coste óptimo (41), ya que el coste de las acciones es uniforme (o UCS lo garantiza). BFS expandió 325 nodos, mientras que UCS expandió 327, una diferencia mínima. Por otro lado, DFS encontró rápidamente una solución (solo 151 nodos expandidos), pero con mucho coste (459), y eso demuesta que no es completa ni óptima en grafos con ciclos.

---

### 2.2. The N-Queens Iterative Repair Problem (Ej. 1.2)

Se implementó el problema de N-Queens en `problems/nqueens.py`. El objetivo es minimizar la distancia total moviendo las reinas desde una configuración inicial hasta que ninguna ataque a otra.

#### Heurística Admisible (Ej. 1.2.2)

**Descripción de la Heurística:**
[...Aquí describes tu heurística. Por ejemplo: "La heurística implementada, `RepairHeuristic`, cuenta el número total de pares de reinas que se están atacando mutuamente en el estado actual..."]

**Justificación de Admisibilidad:**
[...Aquí justificas por qué es admisible (nunca sobreestima el coste real). Por ejemplo: "Esta heurística es admisible porque para resolver cada conflicto (un par de reinas atacándose), se requiere al menos un movimiento con coste 1. Al contar los pares, `h(n)` nunca será mayor que el coste real para llegar a una solución..."]

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
Incluso en un problema tan pequeño (N=4), las diferencias son evidentes. `hlog-tree-ucs` (búsqueda en árbol) explota en tamaño de frontera (13652) y nodos expandidos (1241) al no detectar estados repetidos. `hlog-tree-astar` mejora esto drásticamente (111 nodos) gracias a la heurística. Finalmente, `hlog-graph-astar` es el más eficiente por un amplio margen (solo 30 nodos), ya que combina la heurística de A* con la detección de estados repetidos (grafos), evitando re-expandir los mismos estados una y otra vez.

---

## 3. Implementación de Algoritmos (Ejercicio 2)

Se implementaron los siguientes algoritmos en la carpeta `algorithms/`, siguiendo los requisitos de la práctica (sucesores en orden lexicográfico, seguimiento de nodos expandidos, etc.).

* **Tree IDS (Ej. 2.1):** Implementado en `algorithms/ids.py`.
* **Tree A\* y Graph A\* (Ej. 2.2):** Implementados en `algorithms/astar.py`.

[...Aquí puedes añadir una breve descripción de tu implementación, por ejemplo, cómo manejaste la frontera en A* (heapq) o el conjunto de explorados en la versión de grafo...]

---

## 4. Evaluación en Pacman (Ejercicio 3)

### 4.1. Heurísticas (Ej. 3.1)

Se implementaron las heurísticas de Manhattan y Euclidean dentro del fichero `problems/pacman.py`.

* **Manhattan Distance:** [Breve descripción de la implementación...]
* **Euclidean Distance:** [Breve descripción de la implementación...]

### 4.2. Comparativa de Algoritmos

[...Inserta aquí la tabla/gráfica comparativa de todos los algoritmos (framework y, si pudiste, los tuyos) sobre todos los layouts de Pacman. Analiza los resultados. Ejemplo: "En layouts pequeños como 'smallMaze', todos los algoritmos óptimos (BFS, UCS, A*, Graph A*) encuentran la misma solución... En layouts grandes como 'bigMaze' o los de Warcraft 3, se evidencia que A* con la heurística Manhattan es el más eficiente..."]

---

## 5. Nota Importante sobre Problemas Técnicos

**Esta es la sección que me pediste explícitamente:**

Durante el desarrollo de la práctica, se implementaron los algoritmos solicitados en el **Ejercicio 2** (Tree IDS, Tree A\* y Graph A\*) en sus respectivos archivos (`ids.py`, `astar.py`). Sin embargo, surgieron problemas técnicos persistentes con el framework `hlogedu-search` que impidieron su ejecución y verificación.

A pesar de seguir la estructura de ficheros (`algorithms/__init__.py`, etc.) y probar múltiples configuraciones del entorno de Python (incluyendo la gestión del `PYTHONPATH` y la corrección de importaciones), el framework **no reconoció los algoritmos implementados** (mostrando errores de tipo "Algorithm not found" o `ImportError`).

Debido a esto:

1.  **No se pudo realizar la comparativa** de nuestros algoritmos implementados contra los del framework, como se solicitaba para validar la implementación (Ej. 2).
2.  **No se pudieron ejecutar nuestros algoritmos** en el problema de Pacman (Ej. 3.3).

Por lo tanto, los resultados del Ejercicio 3 se centran en los algoritmos proporcionados por el framework. El código de los Ejercicios 2.1 y 2.2 se entrega igualmente para su revisión manual, aunque no haya sido posible verificar su salida empíricamente.

---

## 6. Conclusión

[...Aquí haces un resumen de lo que aprendiste. Por ejemplo: "Esta práctica ha permitido comprender en profundidad el modelado de problemas de IA y la diferencia crítica en el rendimiento (coste y nodos expandidos) entre algoritmos de búsqueda informados (A*) y no informados (BFS, UCS)..."]