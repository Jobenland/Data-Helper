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
if sys.version_info[0] >= 3:
    import PySimpleGUI as sg
from pyexcel.cookbook import merge_all_to_a_book

IMPEDANCE_COLNAMES = [
    "Time", 
    "Time-Hours", 
    "Electrode", 
    "Ohmic", 
    "TASR"
    ]
DYNAMIC_COLNAMES = [
    "ABS_TIME",
    "Time_Min",
    "Time-Hours",
    "PPD"
    ]
STATIC_COLNAMES = [
    "ABS_TIME",
    "Time_Min",
    "Time-Hours",
    "Voltage"
    ]
ENCODING = "ISO-8859-1"
IMPEDANCE_TAG = "IMPEDANCE"
STATIC_TAG = "STATIC"
DYNAMIC_TAG = "DYNAMIC"

class FileHandler:
    def __init__(self, import_dir, export_dir, file_list=None):

        self.directory_export = export_dir
        self.directory_import = import_dir

        if not os.path.isdir(self.directory_import):
            os.mkdir(self.directory_import)
        self.list_experiment = []
        if file_list != None:
            self.list_experiment = file_list
        else:
            self.list_experiment = self.import_file_names(self.directory_import)

        self.dict_impedance = {}
        self.dict_dynamic = {}
        self.dict_static = {}
        self.finishedPath = ''
        self.ohmicValues = [5, 25]

    def reset_file_lists(self):
        self.list_impedance = []
        self.list_dynamic = []
        self.list_static = []
    # Takes a string (directory name) and returns a list(file name strings)
    def import_file_names(self, directory):
        return natsort.natsorted(os.listdir(directory))
 
    def unzipFile(self, zip_name, directory):
        #print("Unzipping file ", zipName)
        zipcounter = 0
        if zip_name and directory and ('.zip' or '.mdat' in zip_name):
            p_dir = '/' + directory.strip("/Data")
            if p_dir[0] == '/'
                p_dir = p_dir[1:]:
            zipcounter +=1 
            with ZipFile(p_dir + '/' + zip_name, 'r') as zipObj:
                zipObj.extractall(directory + '/' + zip_name.strip('.mdat'))
                #print("Zip extraction completed")
        else:
            print("Invalid filename or directory")
    def unzipDirectory(self, file_list, in_directory, out_directory):
        if os.path.isdir(in_directory) and os.path.isdir(out_directory):
            os.chdir(in_directory)
            exp_list = []
            counter = 0
            for file in file_list:
                if (('.mdat' or '.zip') in file):
                    exp_list.append(file.split('.')[0])
                    try:
                        os.mkdir(out_directory + '/' + exp_list[counter])
                    except FileExistsError:
                        os.chdir(out_directory + '/' + exp_list[counter])

                    except FileNotFoundError:
                        print(file + " not found")
                    if file:
                        self.unzipFile(file, out_directory)
                    counter += 1


    def populate_dicts(self, directory):
        os.chdir(directory)
        for exp in natsort.natsorted(os.listdir(directory)):
            self.dict_dynamic[exp] = []
            self.dict_impedance[exp] = []
            self.dict_static[exp] = []
            for folder in os.listdir(directory + '/' + exp):

                for file in natsort.natsorted(os.listdir(directory + '/' + exp + '/' + folder)):
                    
                    with open(directory + '/' + exp + '/' + folder + '/' + file, 'r', encoding=ENCODING) as f:
                        if '.mpro' not in file:
                            for row in f:
                                if 'galvanostatic' in row.lower():
                                    if file not in self.dict_static[exp]:
                                        self.dict_static[exp].append(file)
                                elif 'galvanodynamic' in row.lower():
                                    if file not in self.dict_dynamic[exp]:
                                        self.dict_dynamic[exp].append(file)
                                elif 'impedance' in row.lower():
                                    if file not in self.dict_impedance[exp]:
                                        self.dict_impedance[exp].append(file)
                                    
    def convert_date(self, euro_date):
        split_date = euro_date.split("/")
        return split_date[1] + "/" + split_date[0] + "/" + split_date[2]


    def combine_CSVs(self, directory):
        self.finishedPath = directory + '/' + 'finished'
        if os.path.exists(self.finishedPath):
            print('finished path found')
        else:
            os.mkdir(self.finishedPath)
        os.chdir(directory)
        new_file_name = ""
        file_list = natsort.natsorted(os.listdir(directory))
        
        f_type_dict = {}
        f_key = ""

        for file in file_list:
            
            if '.csv' in file:
                temp_string = str(re.findall(r"\D(\d{3})\D", " "+file+" ")[0])
                if 'IMPEDANCE' in file.upper():
                    f_key = "IMPEDANCE+" + temp_string
                    if temp_string + "_IMPEDANCE" in file:
                        new_file_name = file.replace(temp_string + "_IMPEDANCE", temp_string + '_1_IMPEDANCE')
                    elif 'initial_IMPEDANCE' in file:
                        new_file_name = file.replace('initial_IMPEDANCE', 'initial_1_IMPEDANCE')
                    elif 'aging_IMPEDANCE' in file:
                        new_file_name = file.replace('aging_IMPEDANCE', 'aging1_IMPEDANCE')
                    else:
                        new_file_name = file

                elif 'DYNAMIC' in file.upper():
                    f_key = "DYNAMIC+" + temp_string
                    if temp_string + "_DYNAMIC" in file:
                        new_file_name = file.replace(temp_string + "_DYNAMIC", temp_string + '_1_DYNAMIC')
                    elif 'initial_DYNAMIC' in file:
                        new_file_name = file.replace('initial_DYNAMIC', 'initial_1_DYNAMIC')
                    elif 'aging_DYNAMIC' in file:
                        new_file_name = file.replace('aging_DYNAMIC', 'aging1_DYNAMIC')
                    else:
                        new_file_name = file

                elif 'STATIC' in file.upper():
                    f_key = "STATIC+" + temp_string
                    if temp_string + "_STATIC" in file:
                        new_file_name = file.replace(temp_string + "_STATIC", temp_string + '_1_STATIC')
                    elif 'initial_STATIC' in file:
                        new_file_name = file.replace('initial_STATIC', 'initial_1_STATIC')
                    elif 'aging_STATIC' in file:
                        new_file_name = file.replace('aging_STATIC', 'aging1_STATIC')
                    else:
                        new_file_name = file

                else:
                    print("File type not found (combineCSVs) for file:", file)

                if new_file_name:
                    os.rename(file, new_file_name)

                # If the key is in the dictonary, add the new file to the list at that key
                if  f_key not in f_type_dict:
                    f_type_dict[f_key] = []
                    f_type_dict[f_key].append(new_file_name)

                # Otherwise, create a new key with the value of a blank list and append the file to that list
                else:
                    f_type_dict[f_key].append(new_file_name)

                f_key = ""

        flist = []
        for key in f_type_dict:
            key = list(set(key))
        for key in f_type_dict:
            for f in f_type_dict[key]:
                if os.path.exists(directory + '/' + f):
                    flist.append(f)
            flist = [x for x in flist if x]
            if len(flist):
                flist = natsort.natsorted(flist)
                end_val = flist[len(flist) -1]
                if ('1_' in end_val) and (('11' not in end_val) and ('10' not in end_val) and ('12' not in end_val)):
                    flist.insert(0, end_val)
                    flist.pop(len(flist) - 1)
                print(flist)
                combined_csv = pd.concat([pd.read_csv(directory + '/' + f) for f in flist])
                combined_csv.to_csv(self.finishedPath + '/' + key.split('+')[0] + '_' + key.split('+')[1] + '.csv')
                flist = []
                print(key.split('+')[0], 'created.')
    
    def fix_CSV_time(self, file_path):
        os.chdir(file_path)
        list_files = natsort.natsorted(os.listdir(file_path))
        colnames = []
        for fileName in list_files:
            if 'IMP' in fileName:
                colnames = IMPEDANCE_COLNAMES
                dataf = pd.read_csv(fileName, names=colnames)
                time_s = dataf.Time.tolist()[1:]
                time_s_f = []
                for i in time_s:
                    try:
                        time_s_f.append(float(i))
                    except(ValueError):
                        continue
                time_minimum = min(time_s_f)
                time_hour = []

                for t in range(len(time_s)):
                    time_hour.append((time_s_f[t] - time_minimum) / 3600)

                new_dataf = {
                    'Time_Seconds': dataf.Time.tolist()[1:],
                    'Time_Hours': time_hour,
                    'Electrode': dataf.Electrode.tolist()[1:],
                    'Ohmic': dataf.Ohmic.tolist()[1:],
                    'TASR': dataf.TASR.tolist()[1:]
                }

                new_frame = pd.DataFrame(data=new_dataf)
                new_frame.sort_values(by='Time_Seconds')
                new_frame.to_csv(fileName.replace('.csv', '_f.csv'), index=False)
                os.remove(fileName)
            if DYNAMIC_TAG in fileName:
                colnames = DYNAMIC_COLNAMES
                dataf = pd.read_csv(fileName, names=colnames)
                time_s = dataf.ABS_TIME.tolist()[1:]
                time_s_f = []
                for i in time_s:
                    try:
                        time_s_f.append(float(i))
                    except(ValueError):
                        continue
                time_minimum = min(time_s_f)
                
                time_hours = []
                time_min = dataf.Time_Min.tolist()

                for i in range(1, len(time_min)):
                    time_min[i] = math.floor(float(time_min[i]))

                for t in range(len(time_s)):
                    time_hours.append((time_s_f[t] - time_minimum) / 3600)

                new_dataf = {
                    'ABS_TIME': dataf.ABS_TIME.tolist()[1:],
                    'Time_Min': time_min[1:],
                    'Time-Hours': time_hours,
                    'PPD': dataf.PPD.tolist()[1:]
                }

                new_frame = pd.DataFrame(data=new_dataf)
                new_frame.sort_values(by='ABS_TIME')
                new_frame.to_csv(fileName.replace('.csv', '_f.csv'), index=False)
                os.remove(fileName)
            if 'STATIC' in fileName:
                colnames = STATIC_COLNAMES
                dataf = pd.read_csv(fileName, names=colnames)
                time_s = dataf.ABS_TIME.tolist()[1:]
                time_s_f = []
                for i in time_s:
                    try:
                        time_s_f.append(float(i))
                    except(ValueError):
                        continue
                time_minimum = min(time_s_f)
                time_min = dataf.Time_Min.tolist()
                for i in range(1, len(time_min)):
                    time_min[i] = math.floor(float(time_min[i]))
                time_hours = []
                for t in range(len(time_s_f)):
                    time_hours.append((time_s_f[t] - time_minimum) / 3600)

                new_dataf = {
                    'ABS_TIME': dataf.ABS_TIME.tolist()[1:],
                    'Time_Min': time_min[1:],
                    'Time-Hours': time_hours,
                    'Voltage': dataf.Voltage.tolist()[1:]
                }

                new_frame = pd.DataFrame(data=new_dataf)
                new_frame.sort_values(by='ABS_TIME')
                new_frame.to_csv(fileName.replace('.csv', '_f.csv'), index=False)
                os.remove(fileName)
                print(fileName, 'time fixed')

    def create_xlsx1(self, directory):
        merge_all_to_a_book(glob.glob(directory + '/*.csv'), "combined.xlsx")
        print("COMBINED XLSX CREATED - DONE")
    def clean(self, directory):
        for f in os.listdir(directory):
            if '.csv' in f:
                os.remove(directory + '/' + f)
    def convertDate(self, europeanDate):
        splitDate = europeanDate.split("/")
        return splitDate[1] + "/" + splitDate[0] + "/" + splitDate[2]
    def getMetaData(self, filename, directory):
        multistatVersionFound = False
        convertDateB = False
        LOOKUP_DATE = "Date:"
        LOOKUP_TIME = "Time:"
        stringDate = ''
        stringTime = ''
        stf = False
        sdf = False
        with open(directory + '/' + filename, 'r', encoding=ENCODING) as file:
            for line in file:
                if '1.7a-mem1' in line:
                    multistatVersionFound = True
                    convertDateB = True
                if '1.7f' or '1.6c' in line:
                    multistatVersionFound = True
                    convertDateB = False
                if multistatVersionFound and LOOKUP_DATE in line:
                    stringDate = line.split()[1]
                    if convertDateB:
                        stringDate = self.convertDate(stringDate)
                    sdf = True
                elif multistatVersionFound and LOOKUP_TIME in line and 'Delta' not in line and 'Offset' not in line and 'Start' not in line and 'Total' not in line:
                    stringTime = line.split()
                    stf = True
                if sdf and stf:
                    break
        return [stringDate, stringTime[1] + ' ' + stringTime[2]]
    def convertToTxT(self, directory):
        os.chdir(directory)

        for folders in os.listdir(directory):

            for f in os.listdir(directory + '/' + folders):
                
                for files in os.listdir(directory + '/' + folders + '/' + f):
                    os.chdir(directory + '/' + folders + '/' + f)
                    if '.z' in files:
                        os.rename(files, files.replace('im.z', '.txt'))
                    if '.cor' in files:
                        os.rename(files, files.replace('.cor', '.txt'))
    def combineNonAgingCSVs(self, csv_directory, output_directory):
        #Traverse through the folders containing the non-aging CSVs
        #csv directory is the directory the contains the folders with the z/cor csvs
        imp_directory = csv_directory + '/imp_file_csvs'
        dyn_directory = csv_directory + '/dyn_file_csvs'
        os.chdir(output_directory)

        if os.path.exists(imp_directory):
            os.chdir(imp_directory)
            #for file in natsort.natsorted(os.listdir(imp_directory)):
            merge_all_to_a_book(natsort.natsorted(os.listdir(imp_directory)), output_directory + "/combined_impedance.xlsx")

        if os.path.exists(dyn_directory):
            os.chdir(dyn_directory)
            #for file in natsort.natsorted(os.listdir(dyn_directory)):
            merge_all_to_a_book(natsort.natsorted(os.listdir(dyn_directory)), output_directory + "/combined_dynamic.xlsx")
                    
        