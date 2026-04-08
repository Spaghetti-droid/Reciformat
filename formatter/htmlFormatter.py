from parser.parser import Parser, InstructionSection
from formatter.formatter import Formatter

"""
HTML structure:
    - Standard headers
    - <head> segment containing
        * various <meta> tags
        * <title> (lower caps, - instead of space, no special chars)
        * <style>
    - <body> segment containing
        * <h1> The title (escaped)
        * <p> containing 
            - <a href=...> holding URL
            - text <br /> holding Author, Published, Modified
        * <p> containing description
        * <p> containing text <br /> for Yields, Prep, Cooking time, Total
        * <h2> Ingredients
        * <ul> <li> text </li> ... </ul> containing ingredients 
        * <h2> instructions
        * <ol type="1"> <li> text </li> </o1> containing instructions
        * Optionally further <ol>s each with a title of h3 or smaller based on depth 
"""

class HTMLFormatter(Formatter):

    def suffix(self) -> str:
        return ".html"
    
    def optList(self, l:list) -> str:
        """Join all non-empty strings in list together with the string '   \n'
        Args:
            l (list): A list of strings
        Returns:
            str: non-empty list elements joined by '   \n'
        """
        return optParagraph(super().optList(l))

    def format(self, p:Parser) -> str:
        """Format the data in p as an html document
        The format below is inspired by pandoc's conversion of this program's md files
        """
        return f"""
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" lang="" xml:lang="">
<head>
  <meta charset="utf-8" />
  <meta name="generator" content="reciformat" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=yes" />
  <title>{p.title()}</title>        
{STYLE_HEADERS}
</head>
<body>

<h1>{p.title()}</h1> 
   
{self.optList([optUrl(p.url()), self.opt('Author: ', p.author(), '<br />'), self.opt('Published: ', p.datePublished(), '<br />'), self.opt('Modified: ', p.datePublished(), '<br />')])}  

<p>{p.description()}</p>  

{self.optList([self.opt('Yields: ', p.recipeYield(), '<br />'), self.opt('Prep: ', p.prepTime(), '<br />'), self.opt('Cooking time: ', p.cookTime(), '<br />'), self.opt('Total: ', p.totalTime(), '<br />')])}

<h2>Ingredients</h2>

{bulletPoints(p.ingredients())}

<h2>Instructions</h2>

{instructions(p.steps())}    

</body>
</html>
"""
# End HTMLFormatter class

def optParagraph(s:str) -> str:
    if s:
        return f"<p>\n{s}\n</p>"
    return ''

def optUrl(url:str) -> str:
    if url:
        return f"<a href=\"{url}\"\nclass=\"uri\">{url}</a><br />"
    return ''

def bulletPoints(l: list) -> str:
    """Formats elements in list as markdown bullet points
    Args:
        l (list): A list of strings
    Returns:
        str: Bullet points, one for each list element
    """
    if not l:
      return ''
    
    ret = '<ul>\n'
    for elem in l:
        ret += f'<li>{elem}</li>\n'
    ret += '</ul>'
    return ret

def instructions(sec: InstructionSection, depth:int = 0) -> str:
    """Take Instruction section and format the information. 
        Intended usage is to call the top section with depth 0, lower levels being handled recursively
    Args:
        sec (InstructionSection): An object representing a section of the instructions
        depth (int, optional): Depth of the section. Top is 0, a subsection is 1, subsub is 2, etc... Defaults to 0.

    Returns:
        str: Formatted string
    """
    stepsStr = ''
    if sec.getName() and depth:
        stepsStr += f'\n<h{2+depth}>{sec.getName()}</h{2+depth}>\n\n'
    
    steps = sec.getSteps()
    if not steps:
      return stepsStr
    
    stepsStr += '<ol type="1">\n'
    for step in sec.getSteps():
        if isinstance(step, str):
            stepsStr += f'<li>{step}</li>\n'
        elif isinstance(step, InstructionSection):
            stepsStr += instructions(step, depth+1)
            
    stepsStr += '</ol>'
    
    return stepsStr


STYLE_HEADERS="""
  <style>
    html {
      color: #1a1a1a;
      background-color: #fdfdfd;
    }
    body {
      margin: 0 auto;
      max-width: 36em;
      padding-left: 50px;
      padding-right: 50px;
      padding-top: 50px;
      padding-bottom: 50px;
      hyphens: auto;
      overflow-wrap: break-word;
      text-rendering: optimizeLegibility;
      font-kerning: normal;
    }
    @media (max-width: 600px) {
      body {
        font-size: 0.9em;
        padding: 12px;
      }
      h1 {
        font-size: 1.8em;
      }
    }
    @media print {
      html {
        background-color: white;
      }
      body {
        background-color: transparent;
        color: black;
        font-size: 12pt;
      }
      p, h2, h3 {
        orphans: 3;
        widows: 3;
      }
      h2, h3, h4 {
        page-break-after: avoid;
      }
    }
    p {
      margin: 1em 0;
    }
    a {
      color: #1a1a1a;
    }
    a:visited {
      color: #1a1a1a;
    }
    img {
      max-width: 100%;
    }
    svg {
      height: auto;
      max-width: 100%;
    }
    h1, h2, h3, h4, h5, h6 {
      margin-top: 1.4em;
    }
    h5, h6 {
      font-size: 1em;
      font-style: italic;
    }
    h6 {
      font-weight: normal;
    }
    ol, ul {
      padding-left: 1.7em;
      margin-top: 1em;
    }
    li > ol, li > ul {
      margin-top: 0;
    }
    blockquote {
      margin: 1em 0 1em 1.7em;
      padding-left: 1em;
      border-left: 2px solid #e6e6e6;
      color: #606060;
    }
    code {
      font-family: Menlo, Monaco, Consolas, 'Lucida Console', monospace;
      font-size: 85%;
      margin: 0;
      hyphens: manual;
    }
    pre {
      margin: 1em 0;
      overflow: auto;
    }
    pre code {
      padding: 0;
      overflow: visible;
      overflow-wrap: normal;
    }
    .sourceCode {
     background-color: transparent;
     overflow: visible;
    }
    hr {
      background-color: #1a1a1a;
      border: none;
      height: 1px;
      margin: 1em 0;
    }
    table {
      margin: 1em 0;
      border-collapse: collapse;
      width: 100%;
      overflow-x: auto;
      display: block;
      font-variant-numeric: lining-nums tabular-nums;
    }
    table caption {
      margin-bottom: 0.75em;
    }
    tbody {
      margin-top: 0.5em;
      border-top: 1px solid #1a1a1a;
      border-bottom: 1px solid #1a1a1a;
    }
    th {
      border-top: 1px solid #1a1a1a;
      padding: 0.25em 0.5em 0.25em 0.5em;
    }
    td {
      padding: 0.125em 0.5em 0.25em 0.5em;
    }
    header {
      margin-bottom: 4em;
      text-align: center;
    }
    #TOC li {
      list-style: none;
    }
    #TOC ul {
      padding-left: 1.3em;
    }
    #TOC > ul {
      padding-left: 0;
    }
    #TOC a:not(:hover) {
      text-decoration: none;
    }
    code{white-space: pre-wrap;}
    span.smallcaps{font-variant: small-caps;}
    div.columns{display: flex; gap: min(4vw, 1.5em);}
    div.column{flex: auto; overflow-x: auto;}
    div.hanging-indent{margin-left: 1.5em; text-indent: -1.5em;}
    /* The extra [class] is a hack that increases specificity enough to
       override a similar rule in reveal.js */
    ul.task-list[class]{list-style: none;}
    ul.task-list li input[type="checkbox"] {
      font-size: inherit;
      width: 0.8em;
      margin: 0 0.8em 0.2em -1.6em;
      vertical-align: middle;
    }
    .display.math{display: block; text-align: center; margin: 0.5rem auto;}
  </style>
"""