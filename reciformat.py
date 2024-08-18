import argparse
import html
from pathlib import Path

import formatter.markdownFormatter as mdf
from reader.pathReader import PathReader
from parser.parser import Parser
from parser.htmlJsonParser import HtmlJsonParser

# TODO download images?

DEFAULT_OUTPUT = "output"
READERS = [PathReader()]
PARSERS = [HtmlJsonParser()]

def initArgParser() -> argparse.Namespace:
    """Defines the arguments that the program can use

    Returns:
        argparse.Namespace: The argument values the user specified to the application
    """
    parser = argparse.ArgumentParser(prog="reciformat.py", description="Extracts recipe information from a document and reformats it as a new file.")
    parser.add_argument("location", help="Path or URL towards the recipe document")
    parser.add_argument("-o", "--output", help="The directory where the result will be saved. Default: " + str(DEFAULT_OUTPUT), default=DEFAULT_OUTPUT)
    return parser.parse_args()


def main():    
    args = initArgParser()
    doc = read(args.location)
    parser = parse(doc)
    formatted = mdf.format(parser)
    print(formatted)
    write(args.output, f'{parser.title()}.md', formatted)
    

def read(loc:str) -> str:
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

def parse(doc:str) -> Parser:
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