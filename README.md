# Reciformat
Extract a recipe from a site and print it to your terminal or save it to a local file in a more minimal format. The program can be used with many of the big cooking recipe sites as they all transmit their data using similar structures.

## Usage

This is a command line program and is run in the terminal either by using the reciformat.py file (on any distribution) or by using the reciformat.exe file (on windows). As usual the -h option gives an overview how to use the program:

    python reciformat.py -h
        usage: reciformat.py [-h] [-f FORMAT] [-o OUTPUT] [-c] location

        Extracts recipe information from a document and reformats it as a new
        file.

        positional arguments:
        location             Path or URL towards the recipe document

        options:
        -h, --help           show this help message and exit
        -f, --format FORMAT  Format of output document. Can be 'html' or
                            'md' (for markdown). Default: html.
        -o, --output OUTPUT  A directory where the result should be output.
        -c, --use-chrome     Some websites need javascript to be accessed.
                            For this we can use a browser that is already
                            installed on the machine. Use this option if
                            normal access to the site causes 4xx status
                            errors

## Installing

### Using the exe file

Copy the exe to where you want it

### Using source files

Copy the source files and directories to where you want them. 

#### Requirements and dependencies

The .py version of reciformat needs **python 3.12** to run. Probably. I haven't tested earlier versions. It also depends on the following libraries that you will need to install:
 - beautifulsoup4
 - requests
 - validators
 - selenium
  
Use the requirements.txt file to add missing dependencies

    pip install -r requirements.txt

## Examples

For all examples below "python reciformat.py" can be exchanged for "reciformat.exe".
This program is quite easy to use. Just call the executable followed by a URL or path. For instance

    python reciformat.py https://www.bbcgoodfood.com/recipes/easy-brownies

This will print the extracted recipe in html format to your terminal. If you'd rather write to a file, the easiest way is to redirect stdout. For example:

    python reciformat.py https://www.bbcgoodfood.com/recipes/easy-brownies > easy-brownies.html
would write the html to "easy-brownies.html" in the current directory.
Alternatively you can specify a destination folder with the -o option:

    python reciformat.py -o /path/to/a_folder https://www.bbcgoodfood.com/recipes/easy-brownies

This will create a file named "Easy brownies.html" at the chosen destination.

If you want to load a local html file just give the program the path to the file:

    python reciformat.py path/to/brownies.htm   

If you want to load the website via your local chrome installation (useful for some websites which won't be accessible using the default method): 

    python reciformat.py -c https://www.bbcgoodfood.com/recipes/easy-brownies

## Generating the exe

The exe can be generated using pyinstaller. In the project root directory, execute:
    
    pyinstaller -F reciformat.py
