from parser.parser import Parser, InstructionSection

def format(p:Parser) -> str:
    """Format the data in p as a markdown document
    """
    return f"""
        
# {p.title()}

{opt('<', p.url(), '>   ')}     
{optList([opt('Author ', p.author()), opt('Published ', p.datePublished()), opt('Modified ', p.datePublished())])}  

{p.description()}  

{optList([opt('Yields: ', p.recipeYield()), opt('Prep: ', p.prepTime()), opt('Cooking time: ', p.cookTime()), opt('Total: ', p.totalTime())])}

## Ingredients

{bulletPoints(p.ingredients())}

## Instructions

{instructions(p.steps())}    
"""
    
def opt(prefix: str, value: str, suffix:str = '') -> str:
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

def optList(l:list) -> str:
    """Join all non-empty strings in list together with the string '   \n'
    Args:
        l (list): A list of strings
    Returns:
        str: non-empty list elements joined by '   \n'
    """
    l = [e for e in l if e]
    return '   \n'.join(l)

def bulletPoints(l: list) -> str:
    """Formats elements in list as markdown bullet points
    Args:
        l (list): A list of strings
    Returns:
        str: Bullet points, one for each list element
    """
    ret = ''
    for elem in l:
        ret += f' - {elem}\n'
    return ret

def instructions(sec: InstructionSection, depth:int = 0) -> str:
    stepsStr = ''
    if sec.getName() and depth:
        stepsStr += f'\n##{'#'*depth} {sec.getName()}\n\n'
    
    i = 1
    for step in sec.getSteps():
        if isinstance(step, str):
            stepsStr += f' {i}. {step}\n'
            i += 1
        elif isinstance(step, InstructionSection):
            stepsStr += instructions(step, depth+1)
    
    return stepsStr