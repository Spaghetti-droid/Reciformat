from abc import ABC, abstractmethod
from parser.parser import Parser

class Formatter(ABC):
    """Abstract class representing a Formatter
    """
    @abstractmethod
    def format(self, parser:Parser) -> str:
        """ Format the data contained in the parser into a string
        Args:
            parser (Parser): contains the data to format
        Returns:
            str: Formatted data
        """
        pass
    
    @abstractmethod
    def suffix(self) -> str:
        """ 
        Returns:
            str: a suffix to append to a file storing the output of this formatter. Usually an extension such as ".md"
        """
        pass
    
    def opt(self, prefix: str, value: str, suffix:str = '') -> str:
        """Returns prefix+value+suffix, but only if value is not empty
        Args:
            prefix (str):
            value (str): 
            suffix (str, optional): Defaults to ''.

        Returns:
            str: The arguments concatenated or ''
        """
        if not value:
            return ''
        if isinstance(value, list):
            value = ', '.join(value)
        return f'{prefix}{value}{suffix}'
    
    def optList(self, l:list) -> str:
        """Join all non-empty strings in list together with the string '   \n'
        Args:
            l (list): A list of strings
        Returns:
            str: non-empty list elements joined by '   \n'
        """
        l = [e for e in l if e]
        return '   \n'.join(l)