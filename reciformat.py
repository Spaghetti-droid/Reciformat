import argparse

DEFAULT_OUTPUT = "output"

def initArgParser() -> argparse.Namespace:
    """Defines the arguments that the program can use

    Returns:
        argparse.Namespace: The argument values the user specified to the application
    """
    parser = argparse.ArgumentParser(prog="reciformat.py", description="Extracts recipe information from a document and reformats it as a new file.")
    parser.add_argument("location", help="Path or URL towards the recipe document")
    parser.add_argument("-o", "--output", help="The directory where the result will be saved. Default: " + str(DEFAULT_OUTPUT), default=DEFAULT_OUTPUT)


def main():
    pass

if __name__ == "__main__":
    main()