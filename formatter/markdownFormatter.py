from parser.parser import Parser
import html

def format(p:Parser) -> str:
    return f"""
        
# {p.title()}

<{p.url()}>     
{optList([opt('Author ', p.author()), opt('Published ', p.datePublished()), opt('Modified ', p.datePublished())])}  

{p.description()}  

{optList([opt('Yields: ', p.recipeYield()), opt('Prep: ', p.prepTime()), opt('Cooking time: ', p.cookTime()), opt('Total: ', p.totalTime())])}

## Ingredients

{bulletPoints(p.ingredients())}

## Instructions

{itemised(p.steps())}    
"""
    
def opt(prefix: str, value: str, postfix:str = '') -> str:
    if not value:
        return ''
    return f'{prefix}{value}{postfix}'

def optList(l:list) -> str:
    l = [e for e in l if e]
    return '   \n'.join(l)

def bulletPoints(l: list) -> str:
    ret = ''
    for elem in l:
        ret += f' - {elem}\n'
    return ret

def itemised(l: list) -> str:
    ret = ''
    i = 1
    for elem in l:
        ret += f' {i}. {elem}\n'
        i += 1
    return ret