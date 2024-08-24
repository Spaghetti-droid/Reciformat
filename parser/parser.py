from abc import ABC, abstractmethod
from datetime import datetime

class InstructionSection(ABC):
    """Represents a section in the instructions
    """
    
    @abstractmethod
    def getName(self) -> str:
        """
        Returns:
            str: Section name
        """
        pass
    
    @abstractmethod
    def getSteps(self) -> list:
        """
        Returns:
            list: List of steps. These can either be strings or other InstructionSections
        """
        pass

class Parser(ABC):
    """Abstract class representing a Parser
    """
    @abstractmethod
    def handles(self, input:str) -> bool:
        """Checks if the parser thinks it can parse the document
        Args:
            input (str): the document contents
        Returns:
            bool: True if this document can be handled by the parser
        """
        pass
    
    @abstractmethod
    def parse(self, input:str) -> bool:
        """Parse the document, extracting all fields of interest from it
        Args:
            input (str): The document contents
        Returns:
            bool: True if parsing was successful. False otherwise.
        """
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
    def steps(self) -> InstructionSection:
        """
        Returns:
            InstructionSection: The top instruction section that lists all steps to perform
        """
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