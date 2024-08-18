from reader.reader import Reader

import re
from pathlib import Path

PATH_PATTERN = r'[\/\\]?(?:[^\/\\\n]+[\/\\]?)+'

class PathReader(Reader):
    
    def handles(self, input: str) -> bool:
        return re.fullmatch(PATH_PATTERN, input)
    
    def read(self, input: str) -> str:
        path = Path(input)
        if not path.is_file():
            raise ValueError(f'Not a file: {path}')
        with open(path, encoding='utf-8') as f:
            return f.read()