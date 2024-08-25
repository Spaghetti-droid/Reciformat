# Reciformat
Extract a recipe from a site and save it to a local file in a more minimal format. The program can be used with many of the big cooking recipe sites as they all transmit their data using similar structures.   
Currently, the recipe is saved locally as a markdown file which is stored by default in a folder called 'output' in the current working directory.

## Usage

This is a command line program and is run in the terminal either by using the reciformat.py file (on any distribution) or by using the reciformat.exe file (on windows). As usual the -h option gives an overview how to use the program:

    reciformat.exe -h     
    
    Extracts recipe information from a document and reformats it as a new file.                                                                                                                                                                     
    positional arguments:                                                                                                     
        location              Path or URL towards the recipe document                                                                                                                                                                                 
    options:                                                                                                                  
        -h, --help            show this help message and exit                                                                   
        -o OUTPUT, --output OUTPUT                                                                                                                    
                              The directory where the result will be saved. Default: 'output'                                   
        -c, --use-chrome      Some websites need javascript to be accessed. For this we can use a browser that is already                       
                              installed on the machine. Use this option if normal access to the site causes 4xx status                            
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
  
Any missing libraries should be installed with

    pip install <library name>

## Examples

This program is quite easy to use. Just call the executable followed by a URL or path. For instance

    reciformat.exe https://www.bbcgoodfood.com/recipes/easy-brownies

This will result in a file named Easy brownies.md appearing in a folder named output wherever you executed the command.

If you'd rather specify a destination you can use

    reciformat.exe -o path/to/custom_folder https://www.bbcgoodfood.com/recipes/easy-brownies

If you want to load a local html file just give the program the path to the file:

    reciformat.exe path/to/brownies.htm   

If you want to load the website via your local chrome installation (useful for some websites which won't be accessible using the default method): 

    reciformat.exe -c https://www.bbcgoodfood.com/recipes/easy-brownies

## Generating the exe

The exe can be generated using pyinstaller. In the project root directory, execute:
    
    pyinstaller -F reciformat.py
