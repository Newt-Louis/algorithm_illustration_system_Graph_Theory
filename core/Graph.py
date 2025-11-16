class Graph:
    def __init__(self):
        self.nodes = {
            'A': (100, 100),
            'B': (250, 100),
            'C': (100, 250),
            'D': (250, 250),
            'E': (400, 250),
        }
        self.edges = {
            'A': ['B', 'C'],
            'B': ['A', 'D'],
            'C': ['A', 'D'],
            'D': ['B', 'C', 'E'],
            'E': ['D']
        }