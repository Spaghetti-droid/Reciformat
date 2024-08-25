from abc import ABC, abstractmethod

class Reader(ABC):
    """Abstract class representing a reader
    """
    @abstractmethod
    def handles(self, location:str) -> bool:
        """Checks if this reader can read from the given location
        Args:
            location (str): A path or URL or some other identifier
        Returns:
            bool: True if this can read from this location
        """
        pass
    
    @abstractmethod
    def read(self, location:str) -> any:
        """Read the contents of the document at location
        Args:
            location (str): A path or URL or some other identifier
        Returns:
            str: The contents of the document
        """
        pass