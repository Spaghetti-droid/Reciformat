import argparse
from pathlib import Path
from enum import Enum

from formatter.formatter import Formatter
from formatter.markdownFormatter import MDFormatter
from formatter.htmlFormatter import HTMLFormatter
from reader.pathReader import PathReader
from reader.urlReader import URLReader
from reader.seleniumReader import SeleniumReader
from parser.parser import Parser
from parser.jsonParser import JsonParser, HtmlJsonParser

### Init constants ###

class Format(Enum):
    """
    All output formats supported by reciformat
    """
    HTML = 'html'
    MD = 'md'

def initArgParser(defaultFormat:Format) -> argparse.Namespace:
    """Defines the arguments that the program can use

    Returns:
        argparse.Namespace: The argument values the user specified to the application
    """
    parser = argparse.ArgumentParser(prog="reciformat.py", description="Extracts recipe information from a document and reformats it as a new file.")
    parser.add_argument("location", help="Path or URL towards the recipe document")
    parser.add_argument("-f", "--format", help=f"Format of output document. Can be 'html' or 'md' (for markdown). Default: {defaultFormat.value}.", type=Format, default=defaultFormat)
    parser.add_argument("-o", "--output", help="A directory where the result should be output.")
    parser.add_argument("-c", "--use-chrome", action='store_true', dest="useChrome", help="Some websites need javascript to be accessed. For this we can use a browser that is already installed on the machine. Use this option if normal access to the site causes 4xx status errors")
    return parser.parse_args()

def initReaderList(args:argparse.Namespace) -> list:
    readers = []
    if args.useChrome:
        readers.append(SeleniumReader())
    else:
        readers.append(URLReader())
        
    readers.append(PathReader())
    
    return readers

DEFAULT_FORMAT = Format.HTML
ARGS = initArgParser(DEFAULT_FORMAT)
READERS = initReaderList(ARGS)
PARSERS = [HtmlJsonParser(), JsonParser()]

### Execution ###

def main():  
    # Choose formatter first to avoid querying url if format is invalid
    formatter = chooseFormatter(ARGS.format)
    doc = read(ARGS.location)
    parser = parse(doc)
    formatted = formatter.format(parser)
    print(formatted)
    if ARGS.output:
        write(ARGS.output, f'{parser.title()}{formatter.suffix()}', formatted)
    

def read(loc:str) -> any:
    """Read the document at loc
    Args:
        loc (str): location of the document. Can be a URL or a path
    Raises:
        ValueError: If location format is not supported
    Returns:
        str: The contents of the document
    """
    for r in READERS:
        if r.handles(loc):
            return r.read(loc)
    raise ValueError(f'Location not supported: {loc}')

def parse(doc:any) -> Parser:
    """Parse the document to a standard form for reformatting
    Args:
        doc (str): Document contents
    Raises:
        ValueError: If no parser can read the document
    Returns:
        Parser: A parser containing all info that was found in the document
    """
    for p in PARSERS:
        if p.handles(doc) and p.parse(doc):
            return p
    raise ValueError('Document format not supported')

def chooseFormatter(format: str) -> Formatter:
    """
    Choose the formatter that matches the requested format. Raise an exception if a 
    matching Formatter cannot be found.
    """
    match format:
        case Format.HTML:
            return HTMLFormatter()
        case Format.MD:
            return MDFormatter()
        case _:
            raise ValueError(f"Output format not recognised: {format}")
            

def write(folderstr:str, name:str, formatted:str) -> None:
    """Write the formatted document to a file
    Args:
        folderstr (str): Path to folder
        name (str): new File name
        formatted (str): Formatted contents
    """
    folder = Path(folderstr)
    folder.mkdir(exist_ok=True, parents=True)
    file = folder / name
    with open(file, 'x', encoding='utf-8') as f:
        f.write(formatted)

if __name__ == "__main__":
    main()