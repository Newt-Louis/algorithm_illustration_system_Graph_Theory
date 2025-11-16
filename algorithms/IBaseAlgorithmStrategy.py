from abc import ABC, abstractmethod

class IBaseAlgorithmStrategy(ABC):
    @abstractmethod
    def run(self,graph,start_node):
        pass