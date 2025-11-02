class Node:
    def __init__(self, state, parent=None, action=None, path_cost=0):
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost
        self.depth = parent.depth + 1 if parent else 0
        self.expanded_order = 0
        self.location = ""
        
    def __lt__(self, other):
        # For heapq to compare nodes when primary keys are equal
        return id(self) < id(other)
        
    def path(self):
        """Return list of nodes from root to current node"""
        node, path = self, []
        while node:
            path.append(node)
            node = node.parent
        return list(reversed(path))