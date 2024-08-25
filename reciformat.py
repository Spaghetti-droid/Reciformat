import argparse
from pathlib import Path

import formatter.markdownFormatter as mdf
from reader.pathReader import PathReader
from reader.urlReader import URLReader
from reader.seleniumReader import SeleniumReader
from parser.parser import Parser
from parser.jsonParser import JsonParser, HtmlJsonParser

### Init constants ###

DEFAULT_OUTPUT = "output"

def initArgParser() -> argparse.Namespace:
    """Defines the arguments that the program can use

    Returns:
        argparse.Namespace: The argument values the user specified to the application
    """
    parser = argparse.ArgumentParser(prog="reciformat.py", description="Extracts recipe information from a document and reformats it as a new file.")
    parser.add_argument("location", help="Path or URL towards the recipe document")
    parser.add_argument("-o", "--output", help="The directory where the result will be saved. Default: " + str(DEFAULT_OUTPUT), default=DEFAULT_OUTPUT)
    parser.add_argument("-c", "--use-chrome", action='store_true', dest="useChrome", help="Some websites need javascript to be accessed. Use this option if normal access to the site causes 4xx status errors")
    return parser.parse_args()

def initReaderList(args:argparse.Namespace) -> list:
    readers = []
    if args.useChrome:
        readers.append(SeleniumReader())
    else:
        readers.append(URLReader())
        
    readers.append(PathReader())
    
    return readers

ARGS = initArgParser()
READERS = initReaderList(ARGS)
PARSERS = [HtmlJsonParser(), JsonParser()]

### Execution ###

def main():  
    doc = read(ARGS.location)
    parser = parse(doc)
    formatted = mdf.format(parser)
    print(formatted)
    write(ARGS.output, f'{parser.title()}.md', formatted)
    

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
    raise ValueError(f'Document format not supported')

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