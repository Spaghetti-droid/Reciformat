from reader.reader import Reader

import requests
import validators

class URLReader(Reader):
    """Gets the document from a URL
    """
    def handles(self, location: str) -> bool:
        if validators.url(location):
            return True
        return False
        
    
    def read(self, location: str) -> str:
        print(f'Making a request to {location}')
        r = requests.get(location)
        print(f'Status: {r.status_code}')
        return r.text