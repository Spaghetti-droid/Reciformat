import parser.parser as psr

import json
import html
from bs4 import BeautifulSoup
from datetime import datetime

DATETIME_FORMAT = "%d/%m/%Y, %H:%M:%S"

# Note: I've had to put unescapes everywhere at the individual string level because unescape does not work on the whole json string
# I do not understand why it has to be this way, but such is life
class HtmlJsonParser(psr.Parser):
    
    def __init__(self) -> None:
        super().__init__()
        self.recipe = {}
    
    def handles(self, input:str) -> bool:
        # Only one parser for now
        return True
    
    def parse(self, input:str) -> bool:
        soup = BeautifulSoup(input, features="html.parser")
        jsonTags = soup.find_all('script', type='application/ld+json')
        found = False
        for jsonTag in jsonTags:
            jsonObj = json.loads(jsonTag.string)
            if jsonObj['@type'] == 'Recipe':
                self.recipe = jsonObj
                found = True
                break
                
        return found
        
        
    def title(self) -> str:
        return self.recipe.get('name','')
    
    def recipeYield(self) -> str:
        return html.unescape(self.recipe.get('recipeYield',''))
    
    def url(self) -> str:
        return self.recipe.get('url','')
    
    # @abstractmethod
    # def image(self) -> str:
    #     pass
    
    def author(self) -> str:
        author = self.recipe.get('author', {})
        return html.unescape(author.get('name'))
    
    def datePublished(self) -> str:
        date = self.recipe.get('datePublished')
        if date:
            return datetime.fromisoformat(date).strftime(DATETIME_FORMAT)
        return ''
    
    def dateModified(self) -> str:
        date = self.recipe.get('dateModified')
        if date:
            return datetime.fromisoformat(date).strftime(DATETIME_FORMAT)
        return ''
    
    def ingredients(self) -> list:
        return [html.unescape(elem) for elem in self.recipe.get('recipeIngredient', [])]
    
    def steps(self) -> list:
        ret = []
        steps = self.recipe.get('recipeInstructions', [])
        for step in steps:
            if step.get('@type', '') != 'HowToStep':
                print(f"[Warning] Unexpected step type: {step.get('@type', '')}")
            ret.append(html.unescape(step.get('text', '')))
        return ret
        
    
    def description(self) -> str:
        return html.unescape(self.recipe.get('description', ''))
    
    def rating(self) -> str:
        ar = self.recipe.get('aggregateRating', {})
        return ar.get('ratingValue', '')
    
    def ratingCount(self) -> str:
        ar = self.recipe.get('aggregateRating', {})
        return ar.get('ratingCount','')
    
    #TODO convert times to human
    def prepTime(self) -> str:
        return self.recipe.get('prepTime')
    
    def cookTime(self) -> str:
        return self.recipe.get('cookTime')
    
    def totalTime(self) -> str:
        return self.recipe.get('totalTime')
    
    def category(self) -> str:
        return html.unescape(self.recipe.get('recipeCategory'))
    
    
    
    
            
