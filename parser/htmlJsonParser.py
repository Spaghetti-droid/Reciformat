from parser.parser import Parser, InstructionSection

import re
import json
import html
from bs4 import BeautifulSoup
from datetime import datetime

DURATION_PATTERN = re.compile(r'P([^T]*)(?:T(.*))')
DURATION_SUB_PATTERN = re.compile(r'(\d+(?:\.\d+)?)(\w)')
DATETIME_FORMAT = "%d/%m/%Y, %H:%M:%S"
RECIPE = 'Recipe'
TYPE_TAG = '@type'

class JsonSection(InstructionSection):        
    def __init__(self, name:str = '') -> None:
        self.name = name
        self.steps = []
        
    def getName(self) -> str:
        return self.name
    
    def getSteps(self) -> list:
        return self.steps
        
    def add(self, steps:list) -> None:
        for step in steps:
            if isinstance(step, str):
                self.steps.append(step)
            elif isinstance(step, dict):
                self.addObj(step)
    
    def addObj(self, step:dict) -> None:
        type = step.get(TYPE_TAG)
        if type == 'HowToStep':
            self.steps.append(step.get('text', ''))
        elif type == 'HowToSection':
            subsection = JsonSection(step.get('name',''))
            subsection.add(step.get('itemListElement', []))
            self.steps.append(subsection)
        else:
            print(f'[Warning] Step type not recognised: {type}')
            
class HtmlJsonParser(Parser):
    """Parses documents which hold recipes as JSONs with HTML pages
    """
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
            # In my test files, json is double escaped.
            jsonStr = html.unescape(html.unescape(jsonTag.string))
            fullJson = json.loads(jsonStr)
            # Most of the time there is one part per tag, and the @graph field doesn't exist. Most of the time.
            jsonParts = fullJson.get('@graph')
            if not jsonParts:
                jsonParts = fullJson
            
            if not isinstance(jsonParts, list):
                jsonParts = [jsonParts]
            for jsonPart in jsonParts:
                if jsonPart.get(TYPE_TAG) == RECIPE or (isinstance(jsonPart, list) and RECIPE in jsonPart):
                    self.recipe = jsonPart
                    found = True
                    break
                
        return found
        
        
    def title(self) -> str:
        return self.recipe.get('name','')
    
    def recipeYield(self) -> str:
        return self.recipe.get('recipeYield','')
    
    def url(self) -> str:
        return self.recipe.get('url','')
    
    # @abstractmethod
    # def image(self) -> str:
    #     pass
    
    def author(self) -> str:
        author = self.recipe.get('author', {})
        if isinstance(author, str):
            return author
        if isinstance(author, list):
            return ', '.join([el.get('name', '') for el in author])
        return author.get('name', '')
    
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
        return self.recipe.get('recipeIngredient', [])
    
    def steps(self) -> InstructionSection:
        steps =  self.recipe.get('recipeInstructions', [])
        top = JsonSection()
        top.add(steps)
        return top        
    
    def description(self) -> str:
        return self.recipe.get('description', '')
    
    def rating(self) -> str:
        ar = self.recipe.get('aggregateRating', {})
        return ar.get('ratingValue', '')
    
    def ratingCount(self) -> str:
        ar = self.recipe.get('aggregateRating', {})
        return ar.get('ratingCount','')
    
    def prepTime(self) -> str:
        return HtmlJsonParser.toHumanDuration(self.recipe.get('prepTime'))
    
    def cookTime(self) -> str:
        return HtmlJsonParser.toHumanDuration(self.recipe.get('cookTime'))
    
    def totalTime(self) -> str:
        return HtmlJsonParser.toHumanDuration(self.recipe.get('totalTime'))
    
    def category(self) -> str:
        return HtmlJsonParser.toHumanDuration(self.recipe.get('recipeCategory'))
    
    @staticmethod
    def toHumanDuration(time:str) -> str:
        """Convert from the ISO 8601 duration format to human readable
        Args:
            time (str): ISO 8601 duration (eg 'PT15M')
        Returns:
            str: The human readable version of time (eg '15 minutes')
        """
        m = DURATION_PATTERN.fullmatch(time)
        if m:
            ret = []
            longDuration = m.group(1)
            if longDuration:
                for (number, unit) in DURATION_SUB_PATTERN.findall(longDuration):
                    ret.append(HtmlJsonParser.toHuman(number, unit, True))
             
            shortDuration = m.group(2)   
            if shortDuration:
                for (number, unit) in DURATION_SUB_PATTERN.findall(shortDuration):
                    ret.append(HtmlJsonParser.toHuman(number, unit, False))
                    
            return ', '.join(ret)
        
        print(f'[WARNING] Duration in unexpected format!')
        return time
       
    @staticmethod
    def toHuman(number:str, unit:str, isLong:bool) -> str:
        """Combine number and unit into one string, and convert the unit to the human-readable version
        Args:
            number (str): a number
            unit (str): An ISO 8601 duration unit
            isLong (bool): If true the unit is taken to indicate a period longer than a day, 
                            otherwise it is taken to be a period shorter than a day
        Returns:
            str: Concatenated string with unit converted to human-readable form
        """
        ret = number
        if isLong:
            ret += ' ' + HtmlJsonParser.longUnit(unit)
        else:
            ret += ' ' + HtmlJsonParser.shortUnit(unit)
        if float(number)>1:
            ret += 's'
        return ret
    
    @staticmethod
    def longUnit(unit:str) -> str:
        """Convert unit to a human-readable form
        Args:
            unit (str): Y, M, W, or D
        Returns:
            str: year, month, week, or day. 
                If the input is not recognised as one of the letters listed above, the input is returned unmodified.
        """
        match(unit):
            case 'Y':
                return 'year'
            case 'M':
                return 'month'
            case 'W':
                return 'week'
            case 'D': 
                return 'day'
            case _:
                print(f'[WARNING] Unit not recognised: {unit}')
                return unit
    @staticmethod      
    def shortUnit(unit:str) -> str:
        """Convert unit to a human-readable form
        Args:
            unit (str): H, M, or S
        Returns:
            str: hour, minute, or second.
                If the input is not recognised as one of the letters listed above, the input is returned unmodified.
        """
        match(unit):
            case 'H':
                return 'hour'
            case 'M':
                return 'minute'
            case 'S':
                return 'second'
            case _:
                print(f'[WARNING] Unit not recognised: {unit}')
                return unit
        
        
    
    
    
    
            
