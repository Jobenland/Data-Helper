# XRD Converter

Video Example: https://youtu.be/qTCuPCO7a90

NEW -> use `pip install -r requirements.txt`

This program takes a folder of raw .out xrd files and removes the header, generates a csv, and adds all xrd files to an xlsx worksheet


## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

put all `.out` files in a folder to reference in the program

### Prerequisites

Programs and other things needed to run this program
```
Python 3.x
Pip
```

### Installing

A step by step series of examples that tell you how to get a development env running

Manuel Method
```
pip install tkinter (not right name) coming soon
pip install pandas 
pip install PySimpleGUI
pip install bokeh
pip install np
```

Automatic method

```
pip install -r requirements.txt
```
Coming soon(instead of cloning from github)...
```
pip install XRD-Converter
```

## Running the tests

To ensure that all modules are loaded and everything is working. Launch the program, If it launches with no errors, it is working properly 

## Running the program

Video Example: https://youtu.be/qTCuPCO7a90

The best way to install and run the program is to clone this repo to your home directory by typing `git clone https://github.com/Jobenland/XRD-Convert`. Once the directory has been cloned, change the directory `cd XRD-Convert` to the directory of the repository. Ensure you are in the directory by typing `dir` and checking the output for a file called `XRDConvert.py`. Type `python --version` or `python3 -version` and ensure the output version is at least 3.x.

to start the program, type `python xrdconvert.py` or `python3 xrdconvert.py` and hit enter. The program will greet the user with a UI asking for a folder containg the `.out` files. select this folder and hit ok. After this is done the program will load the files into memory and warn the user that the header is going to be removed. This action can NOT be undone and WILL edit the file. Backup your files before hitting ok on the prompts. At the end, The program will ask the user to type a name for the combined `.xlsx` file. Type the name and then let the program run to completion.

## Deployment

The best way to deploy this software for use in lab is to run locally either through command prompt or a Python Interpreter of your own
## Built With

* [Pandas](https://pandas.pydata.org/) - Used to edit and read CSV's
* [PySimpleGUI](https://pypi.org/project/PySimpleGUI/) - Used to create a GUI more efficiently
* [TKinter](https://docs.python.org/3/library/tkinter.html) - Used as backend GUI framework and support
* [Bokeh](https://bokeh.pydata.org/en/latest/) - Used as plotting software for the plot function
* [NP](http://cs231n.github.io/python-numpy-tutorial/) - Help with scientific calculations

## Contributing

If any Enhancements, Features or Problems arrise, Please submit a request on github

## Versioning

No versioning control has been set up yet but I am working on having this work in the Future 

## Authors

* **Jonathan Obenland** - *Initial work* - [Jonathan Obenland](https://github.com/jobenland)

## License

This project is licensed under the GPL License
