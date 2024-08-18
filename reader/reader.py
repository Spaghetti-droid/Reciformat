from abc import ABC, abstractmethod

class Reader(ABC):
    @abstractmethod
    def handles(self, input:str) -> bool:
        pass
    
    @abstractmethod
    def read(self, input:str) -> str:
        pass