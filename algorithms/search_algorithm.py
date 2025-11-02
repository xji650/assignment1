class SearchAlgorithm:
    def __init__(self, problem):
        self.problem = problem
        self.expanded_nodes = 0
        
    def search(self):
        raise NotImplementedError("Subclasses must implement search method")
        
    def tree_search(self):
        return self.search()