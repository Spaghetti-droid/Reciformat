from abc import ABC, abstractmethod
from datetime import datetime

class Parser(ABC):
    @abstractmethod
    def handles(self, input:str) -> bool:
        pass
    
    @abstractmethod
    def parse(self, input:str) -> bool:
        pass
    
    @abstractmethod
    def title(self) -> str:
        pass
    
    @abstractmethod
    def recipeYield(self) -> str:
        pass
    
    @abstractmethod
    def url(self) -> str:
        pass
    
    # @abstractmethod
    # def image(self) -> str:
    #     pass
    
    @abstractmethod
    def author(self) -> str:
        pass
    
    @abstractmethod
    def datePublished(self) -> str:
        pass
    
    @abstractmethod
    def dateModified(self) -> str:
        pass
    
    @abstractmethod
    def ingredients(self) -> list:
        pass
    
    @abstractmethod
    def steps(self) -> list:
        pass
    
    @abstractmethod
    def description(self) -> str:
        pass
    
    @abstractmethod
    def rating(self) -> str:
        pass
    
    @abstractmethod
    def ratingCount(self) -> str:
        pass
    
    @abstractmethod
    def prepTime(self) -> str:
        pass
    
    @abstractmethod
    def cookTime(self) -> str:
        pass
    
    @abstractmethod
    def totalTime(self) -> str:
        pass
    
    @abstractmethod
    def category(self) -> str:
        pass