from abc import ABC, abstractmethod

class IBaseAlgorithmStrategy(ABC):
    @abstractmethod
    def run(self,graph,start_node):
        pass

    @abstractmethod
    def render_step(self, canvas, graph, all_steps, index):
        pass