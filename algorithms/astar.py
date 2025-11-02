import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

import heapq

from search_algorithm import SearchAlgorithm
from node import Node

class TreeAStar(SearchAlgorithm):
    """
    Implementa el algoritmo A* para búsqueda en árbol.
    """

    def __init__(self, problem, heuristic=None):
        super().__init__(problem)
        self.heuristic = heuristic or problem.heuristic
        if not self.heuristic:
            raise ValueError("La búsqueda A* requiere una función heurística.")
        
        self.expanded_nodes = 0
        self._generated_count = 0 

    def f(self, node):
        """f(n) = g(n) + h(n)"""
        return node.path_cost + self.heuristic(node.state)

    def search(self):
        """
        Realiza la búsqueda A* en árbol.
        """
        # Reiniciar contadores
        self.expanded_nodes = 0
        self._generated_count = 0
        
        try:
            start_state = self.problem.get_start_states()[0]
        except IndexError:
            return None  # No hay estado inicial
            
        root = Node(state=start_state)
        root.location = "root"
        
        fringe = [] # cola de prioridad (heapq)
        f_root = self.f(root)

        # Añadir contador de desempate a raray
        heapq.heappush(fringe, (f_root, self._generated_count, root))
        self._generated_count += 1

        while fringe:
            _, _, node = heapq.heappop(fringe)

            if self.problem.is_goal_state(node.state):
                return node

            current_expansion_order = self.expanded_nodes
            node.expanded_order = current_expansion_order
            self.expanded_nodes += 1
            
            # Generar sucesores en orden lexicográfico
            successors = sorted(self.problem.successors(node.state))

            for action, result_state, cost in successors:
                child = Node(
                    state=result_state,
                    parent=node,
                    action=action,
                    path_cost=node.path_cost + cost
                )

                # Asignar atributos al *hijo*
                child.expanded_order = current_expansion_order
                child.location = f"depth_{child.depth}_node_{current_expansion_order}"

                f_child = self.f(child)
                # Añadir contador de desempate
                heapq.heappush(fringe, (f_child, self._generated_count, child))
                self._generated_count += 1
                
        return None

    def tree_search(self):
        """Interface method for tree search"""
        return self.search()