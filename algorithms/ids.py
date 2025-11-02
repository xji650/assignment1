import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

from search_algorithm import SearchAlgorithm
from node import Node


class TreeIDS(SearchAlgorithm):

    def __init__(self, problem):
        super().__init__(problem)
        # Count of generated/expanded nodes (semantics: increment when generating children)
        self.expanded_nodes = 0

    def search(self):
        """Iterative Deepening Search (IDS)."""
        depth = 0
        while True:
            result = self.depth_limited_search(depth)
            if result is not None:  # Found a solution
                return result
            depth += 1  # Increment depth for next iteration

    def depth_limited_search(self, limit):
        """Depth-Limited Search (DLS) with depth limit `limit`.

        Returns the goal node if found, otherwise None.
        """
        try:
            start_state = self.problem.get_start_states()[0]
        except IndexError:
            return None # No hay estado inicial
        node = Node(start_state)

        # Optional metadata used elsewhere in the project
        node.expanded_order = 0
        node.location = "root"

        # Fringe as LIFO stack (DFS)
        fringe = [node]

        while fringe:
            current_node = fringe.pop()

            # Goal test
            if self.problem.is_goal_state(current_node.state):
                return current_node

            # Expand if within depth limit
            if current_node.depth < limit:
                # Generate successors in lexicographical order
                successors = sorted(self.problem.successors(current_node.state))
                # Reverse to preserve lexicographic order when using stack (LIFO)
                for action, result_state, cost in reversed(successors):
                    child = Node(result_state, current_node, action, current_node.path_cost + cost)
                    child.expanded_order = self.expanded_nodes
                    child.location = f"depth_{child.depth}_node_{self.expanded_nodes}"
                    fringe.append(child)
                    # Increment the generated/expanded counter for bookkeeping
                    self.expanded_nodes += 1

        # Return None if no solution found within the given limit
        return None

    def tree_search(self):
        """Interface method for IDS (alias)."""
        return self.search()

