import re
import os
import sys
import copy
import csv
import datetime
import time
import subprocess
import pandas as pd
import itertools as itls
import math
import glob
import natsort
from zipfile import ZipFile
import tkinter
from openpyxl import Workbook
from FileHandler import FileHandler
from Impedance import Impedance
from Galvanodynamic import Galvanodynamic
from Galvanostatic import Galvanostatic
if sys.version_info[0] >= 3:
    import PySimpleGUI as sg
print=sg.Print
print("Batch processor started")
RAW_PATH = ''
FOLDER_PATH = ''
IMPORT_PATH = ''
FILE_LIST = []
EXPORT_PATH = ''

LowerOhmic = 5
UpperOhmic = 25
init_layout = [
    [sg.Text("Would you like to convert an entire folder or select files?")],
    [sg.Button('Select Files'), sg.Button('Choose folder')]
]

folder_layout = [
    [sg.Text('Please select a folder to import from:'), sg.InputText(key='import_folder'), sg.FolderBrowse()],
    [sg.Text('Please select a folder to export to:'), sg.InputText(key='export_folder'), sg.FolderBrowse()],
    [sg.Button('Next'), sg.Exit()]
]

files_layout = [
    [sg.Text('Please select the files you would like to input:'), sg.Input(key='Files'), sg.FilesBrowse()],
    [sg.Text('Please select an output folder'), sg.InputText(key='export_folder'), sg.FolderBrowse()],
    [sg.Exit(), sg.Button('Next')]
]


layout_main = [
    [sg.Text('Batch CSV converter')],
    [sg.Text('Enter any keys for specific file types you want (i.e \'OCV\' or \'600\'), separated by commas')],
    [sg.Input(key='FLAGS')],
    [sg.Exit(), sg.Button('Start')]
]



event = ""
values = ""
w1Next = False
window = sg.Window('Batch CSV Creator', location=(800,600)).Layout(init_layout)
while True:
    event, values = window.Read(timeout=100)
    if event != sg.TIMEOUT_KEY:
        print(event, values)
    if event is None or event == 'Exit':
        break
    if event == 'Choose folder':
        break
    if event == 'Select Files':
        break
window.Close()

if event == 'Choose folder':
    window = sg.Window('Batch CSV Creator', location=(800,600)).Layout(folder_layout)
    while True:
        event_2, values = window.Read(timeout=100)

        if event_2 is None or event_2 == 'Exit':
            break
        if event_2 == 'Next':
            RAW_PATH = values['import_folder']
            if len(RAW_PATH) != 0:
                FILE_LIST = natsort.natsorted(os.listdir(RAW_PATH))
            EXPORT_PATH = values['export_folder']
            IMPORT_PATH = RAW_PATH + '/Data'
            
            try:
                if RAW_PATH:
                    os.mkdir(IMPORT_PATH)
            except FileExistsError:
                print(IMPORT_PATH+"/Data found")
            if os.path.exists(EXPORT_PATH):
                print('Export path found')
            else:
                if EXPORT_PATH:
                    os.mkdir(EXPORT_PATH)
            w1Next = True
            break
    window.Close()

elif event == 'Select Files':
    window = sg.Window('Batch CSV Creator', location=(800,600)).Layout(files_layout)
    while True:
        event, values = window.Read(timeout=100)
        if event != sg.TIMEOUT_KEY:
            print(event, values)
        if event == 'Exit' or event is None:
            break
        if event == 'Next':
            files_list = values['Files'].split(';')
            split_first_file = files_list[0].split('/')
            for i in range(len(split_first_file) - 1):
                RAW_PATH += split_first_file[i]
                RAW_PATH += '/'
            EXPORT_PATH = values['export_folder']
            w1Next = True
            break
    window.Close()
def main(keywords):
    strkey = keywords.strip(' ')
    list_keywords = strkey.split(',')
    new_filelist = []
    for word in list_keywords:
        for file in FILE_LIST:
            if word in file and '.mdat' in file:
                
                new_filelist.append(file)
    new_filelist = list(set(new_filelist))
    print(new_filelist)

    
    fh = FileHandler(IMPORT_PATH, EXPORT_PATH, file_list=new_filelist)
    fh.unzipDirectory(FILE_LIST, RAW_PATH, IMPORT_PATH)
    fh.populate_dicts(IMPORT_PATH)
    fh.ohmicValues = [LowerOhmic, UpperOhmic]
    # obj_gd = Galvanodynamic(fh.dict_dynamic)
    # obj_gs = Galvanostati(fh.dict_static)
    # obj_imp = Impedance(fh.dict_impedance)
    finished_filelist = []
    for file in new_filelist:
        finished_filelist.append(file.strip('.mdat'))
    
    arc = [0,0,0]
    os.chdir(IMPORT_PATH)
    for experiment in natsort.natsorted(finished_filelist):
        os.chdir(IMPORT_PATH + '/' + experiment)
        imp = None
        dyn = None
        stat = None
        
        if len(fh.dict_impedance[experiment]):
            arc[0] += 1
            imp = Impedance(fh.dict_impedance[experiment])
            
        if len(fh.dict_dynamic[experiment]):
            arc[1] += 1
            dyn = Galvanodynamic(fh.dict_dynamic[experiment])

        if len(fh.dict_dynamic[experiment]):
            arc[2] += 1
            stat = Galvanostatic(fh.dict_static[experiment])

        for run_folder in os.listdir(IMPORT_PATH + '/' + experiment):
            os.chdir(IMPORT_PATH + '/' + experiment + '/' + run_folder)
            if imp != None:
                imp.extractData(fh.dict_impedance[experiment], IMPORT_PATH + '/' + experiment + '/' + run_folder,  fh.ohmicValues)
            if dyn != None:
                dyn.extractData(fh.dict_dynamic[experiment], IMPORT_PATH + '/' + experiment + '/' + run_folder)
            if stat != None:
                stat.extractData(fh.dict_static[experiment], IMPORT_PATH + '/' + experiment + '/' + run_folder)

        if dyn != None:
            dyn.createCSV(experiment, EXPORT_PATH)
        if stat != None:
            stat.createCSV(experiment, EXPORT_PATH)
        if imp != None:
            imp.createCSV(experiment, EXPORT_PATH)
    
    fh.combine_CSVs(EXPORT_PATH)
    fh.fix_CSV_time(fh.finishedPath)
    fh.create_xlsx1(fh.finishedPath)
    #fh.clean(fh.finishedPath)
    print(arc)
    finished = sg.Window('Batch CSV Creator', location=(800,600)).Layout([[sg.Text("FINISHED. Your processed data files should be in:")],
                                                                         [sg.Text(fh.finishedPath)],
                                                                         [sg.Exit()]])
    while True:
        event, values = finished.Read(timeout=1000)
        if event != sg.TIMEOUT_KEY:
            print(event,values)
        if event is None or event == 'Exit':
            break
    finished.Close()

def main_window():
    window = sg.Window('Batch CSV Creator', location=(800,600)).Layout(layout_main)

    while True:
        event, values = window.Read(timeout=1000)
        if event != sg.TIMEOUT_KEY:
            print(event, values)
        if event is None or event == 'Exit':
            break
        if event == 'Start':
            KEYWORDS = values['FLAGS']
            processing = sg.Window('Batch CSV Creator').Layout([[sg.Text("Processing...")]])
            main(KEYWORDS)
            processing.Close()
            break
    window.Close()
print(w1Next)
if w1Next:
    main_window()


            