# Data Converter and Analysis


NEW -> use `pip install -r requirements.txt`

This program is a collection of commently used tools when analyzing and manipulating data. I am working on a future option to have multi-threading due to the occasional unresponsive weapon

This program was made with PyQt5


## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

run `main.py` to start the GUI

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
pip install pandas 
pip install PyQt5
pip install bokeh
pip install np
```

Automatic method

```
pip install -r requirements.txt
```

## Running the tests

To ensure that all modules are loaded and everything is working. Launch the program, If it launches with no errors, it is working properly 

## Running the program

when `main.py` is ran, you will be greeted with 3 boxes on the left corresponding to the tools. Both `temperature dependence analysis` and `full cell data converter` both take a folder of Mdats and have varying options under them. Select location of the `mdat` files in a folder and select `start` and the progress bar to the right will update. for `XRD Converter` give the program a folder of `.out` files. *WARNING, XRD Converter will remove the headers, this CAN NOT be undone*

## Deployment

The best way to deploy this software for use in lab is to run locally either through command prompt or a Python Interpreter of your own

## Built With


* [Pandas](https://pandas.pydata.org/) - Used to edit and read CSV's
* [PyQt5qt](https://www.qt.io/developers/) - Used to create a GUI more efficiently
* [NP](http://cs231n.github.io/python-numpy-tutorial/) - Help with scientific calculations

## Contributing

If any Enhancements, Features or Problems arrise, Please submit a request on github

## Versioning

No versioning control has been set up yet but I am working on having this work in the Future 

## Authors

* **Jonathan Obenland** - *Initial work* - [Jonathan Obenland](https://github.com/jobenland)

## Credit
* **flat Icon** - *Data mining Icon* - [flaticon](https://www.flaticon.com/authors/flat-icons)
## License

This project is licensed under the GPL License