from parser.parser import Parser

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

{itemised(p.steps())}    
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

def itemised(l: list) -> str:
    """Formats elements in list as an ordered list
    Args:
        l (list): list of strings
    Returns:
        str: A numbered list, one entry per element
    """
    ret = ''
    i = 1
    for elem in l:
        ret += f' {i}. {elem}\n'
        i += 1
    return ret