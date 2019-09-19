from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QFileDialog
import os
import sys
import tkinter
from tkinter import ttk
import abc
import csv
import numpy as np
import pandas as pd
import glob 
import datetime, time
import itertools as itls
import time
from zipfile import ZipFile
import xlsxwriter
from bokeh.plotting import figure, output_file, show
from bokeh.models import ColumnDataSource
import fnmatch
import zipfile
import shutil
import math
import re
from scipy.optimize import fsolve, minimize
from scipy.integrate import quad
from scipy.linalg import toeplitz
from scipy import sparse
from np import conj
from np import transpose
from oct2py import octave
import osqp
import matplotlib.pyplot as plot
import natsort
import copy
from openpyxl import Workbook
import pyexcel
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

LOOKUP_FILE_BASE = "File Base:"
LOOKUP_DATE = "Date:"
LOOKUP_TIME = "Time:"
LOOKUP_END_HEADER = "End Header:"
EURO_MACHINE_FILE_BASE = "EIS_OCV_600_aging"
NA_MACHINE_FILE_BASE = "EIS_OCV_IV_Aging_600"

IMP_600_OLD = "IMP_IV_600"
IMP_600_NEW = "OCV_IV_600"


class Ui(QtWidgets.QMainWindow):
    
    def __init__(self):
        super(Ui, self).__init__()
        base = os.getcwd()
        uic.loadUi('gui.ui', self)
        path =''
        text = open('README.MD').read()
        #infoIdle = open('Information/idle.html').read()
        infoTD = open('Information/td.html').read()
        infoXRD = open('Information/xrd.html').read()
        infoFC = open('Information/fc.html').read()
        try:
            infoMC = open('Information/mc.html').read()
        except:
            print("TODO: Make html for mass converter")
        self.textBrowser.setPlainText(text)
        self.infoWindow.setText(open('Information/idle.html').read())
        self.temp = tempConverter(path)
        
        printer = self.findChild(QtWidgets.QScrollArea,'outPutArea')
        self.tdBrowse.clicked.connect(self.getMdatFoldertd)
        self.xrdBrowse.clicked.connect(self.getMdatFolderxrd)
        self.fcBrowse.clicked.connect(self.getMdatFolderfc)
        self.drtBrowse.clicked.connect(self.getMdatFolderdrt)
        self.mcBrowse.clicked.connect(self.getMdatFoldermc)
        self.mcOutput.clicked.connect(self.getOutputFoldermc)
        self.tdStart.clicked.connect(self.printButtonPressed) # Remember to pass the definition/method, not the return value!
        self.xrdStart.clicked.connect(self.xrdSt)
        self.fcStart.clicked.connect(self.fcSt)
        self.drtStart.clicked.connect(self.DRT)
        self.mcStart.clicked.connect(self.mc)
        
        self.show()
    def mc(self):
        base=os.getcwd()
        progressbarval = 0
        self.infoWindow.setText(open('Information/mc.html').read())
        #Jonathan: You need to make a GUI checkbox, and connect that checkbox to this aging variable
        # If you do not do this, a pretty big feature will be broken
        progressbarval += 10
        self.fcProgress_2.setValue(progressbarval)
        if self.mcAging.isChecked():
            AGING = True
        else:
            AGING = False


        # This section grabs and parses the file import and export paths, creates FILE_LISt
        progressbarval += 10
        self.fcProgress_2.setValue(progressbarval)
        RAW_PATH = self.mcFileText.text()
        if len(RAW_PATH) != 0:
            FILE_LIST = natsort.natsorted(os.listdir(RAW_PATH))
        EXPORT_PATH = self.mcExportPath.text() #JONATHON: You need to add this box/variable, this is for the folder it will output to
        IMPORT_PATH = RAW_PATH + '/Data'

        # Error checking for inputted paths
        progressbarval += 10
        self.fcProgress_2.setValue(progressbarval)
        try:
            if RAW_PATH:
                os.mkdir(IMPORT_PATH)
        except FileExistsError:
            print(IMPORT_PATH+"/Data Found")
        if os.path.exists(EXPORT_PATH):
            print("Export path found")
        else:
            if EXPORT_PATH:
                os.mkdir(EXPORT_PATH)
        
        # Checking keywords, and creating new_filelist based on keywords
        strkey = self.lineEdit.text().strip(' ') #Not sure if you have made the flags/keywords variable yet, but it needs to exist
        list_keywords = strkey.split(',')
        new_filelist = []
        progressbarval += 10
        self.fcProgress_2.setValue(progressbarval)
        for word in list_keywords:
            for file in FILE_LIST:
                if word in file and '.mdat' in file:
                    new_filelist.append(file)

        
        new_filelist = list(set(new_filelist)) #Removes duplicates from the filelist
        print(new_filelist)
        if IMPORT_PATH == '':
            IMPORT_PATH = RAW_PATH + '/Data'
        
        fh = FileHandler(IMPORT_PATH, EXPORT_PATH, file_list=new_filelist)
        fh.unzipDirectory(FILE_LIST, RAW_PATH, IMPORT_PATH)
        
        fh.populate_dicts(IMPORT_PATH)
    
        finished_filelist = []
        progressbarval += 10
        self.fcProgress_2.setValue(progressbarval)
        for file in new_filelist:
            finished_filelist.append(file.strip('.mdat'))
        
        arc = [0,0,0]
        os.chdir(IMPORT_PATH)
        GalvanoHolder = Galvanodynamic(['EMPTY'])
        progressbarval += 10
        self.fcProgress_2.setValue(progressbarval)
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
                    imp.extractData(fh.dict_impedance[experiment], IMPORT_PATH + '/' + experiment + '/' + run_folder, EXPORT_PATH, AGING)
                if dyn != None:
                    vals = dyn.extractData(fh.dict_dynamic[experiment], IMPORT_PATH + '/' + experiment + '/' + run_folder, EXPORT_PATH, AGING)
                    if not AGING:
                        for v in vals:
                            GalvanoHolder.fileDataList.append(v)
                if stat != None:
                    stat.extractData(fh.dict_static[experiment], IMPORT_PATH + '/' + experiment + '/' + run_folder)
    
            if dyn != None:
                dyn.createCSV(experiment, EXPORT_PATH)
            if stat != None:
                stat.createCSV(experiment, EXPORT_PATH)
            if imp != None:
                imp.createCSV(experiment, EXPORT_PATH)
        progressbarval += 10
        self.fcProgress_2.setValue(progressbarval)
        if not AGING and os.path.exists(EXPORT_PATH + '/imp_file_csvs'):
            temp_Impedance = Impedance(['EMPTY'])
            temp_Impedance.createSummary(EXPORT_PATH + '/imp_file_csvs')
            temp_Impedance = None
            if os.path.exists(EXPORT_PATH + '/dyn_file_csvs'):
                GalvanoHolder.createSummary(EXPORT_PATH + '/dyn_file_csvs')
        progressbarval += 10
        self.fcProgress_2.setValue(progressbarval)
        fh.combine_CSVs(EXPORT_PATH)
        fh.fix_CSV_time(fh.finishedPath)
        fh.create_xlsx1(fh.finishedPath)
        
        progressbarval += 10
        self.fcProgress_2.setValue(progressbarval)
        if not AGING:
            fh.combineNonAgingCSVs(EXPORT_PATH, fh.finishedPath)
    
        progressbarval += 10
        self.fcProgress_2.setValue(progressbarval)
        fh.convertToTxT(IMPORT_PATH)
        #fh.clean(fh.finishedPath)
        print(arc)
        os.chdir(base)
        self.infoWindow.setText(open('Information/idle.html').read())
    def DRT(self):
        base=os.getcwd()
        self.infoWindow.setText(open('Information/drt.html').read())
        input_directory = self.drtFilePath.text()
        regularization = self.drtRegularization.text()

        output_directory = input_directory + '/out'
        if not os.path.exists(input_directory):
            os.mkdir(input_directory)
        if not os.path.exists(output_directory):
            os.mkdir(output_directory)

        os.chdir(input_directory)
        file_list = os.listdir(input_directory)
        progressbarval=0
        step = 100 / len(os.listdir(input_directory))
        tstep = step
        
        for file in file_list:
            tstep += step
            self.drtProgress.setValue(tstep)
            if os.path.isfile(file):
                f = File_In(input_directory +'/'+ file, output_directory, regularization=regularization)
        print("DRT FINISHED")
        os.chdir(base)
        self.infoWindow.setText(open('Information/idle.html').read())
    def fcSt(self):
        path = self.xrdFileText_2.text()
        csvname = self.fcCombine.text()
        progressbarval = 0
        area = float(self.fcArea.text())

        if self.symmCellCheck.isChecked():
            symmCell = True
        else:
            symmCell = False

        if symmCell == True:
            self.infoWindow.setText(open('Information/fc.html').read())
            base = os.getcwd()
            symmcellFC = fcConvert(path)
            progressbarval += 20
            self.fcProgress.setValue(progressbarval)
            symmcellFC.convertMdatToZip(path)
            progressbarval += 20
            self.fcProgress.setValue(progressbarval)
            symmcellFC.unzipFiles(path)
            progressbarval += 20
            self.fcProgress.setValue(progressbarval)
            gdL,gsL,iL = symmcellFC.getExperimentName(path)
            progressbarval += 20
            self.fcProgress.setValue(progressbarval)
            symmcellFC.impedanceFileReader(iL, path,area)
            progressbarval += 20
            self.fcProgress.setValue(progressbarval)
            symmcellFC.createCSV(path)
            os.chdir(base)
            self.infoWindow.setText(open('Information/idle.html').read())


        if symmCell == False:
            self.infoWindow.setText(open('Information/fc.html').read())
            base = os.getcwd()
            fullcellFC = fcConvert(path)
            progressbarval += 14.2857143
            self.fcProgress.setValue(progressbarval)
            fullcellFC.convertMdatToZip(path)
            progressbarval += 14.2857143
            self.fcProgress.setValue(progressbarval)
            fullcellFC.unzipFiles(path)
            progressbarval += 14.2857143
            self.fcProgress.setValue(progressbarval)
            gdL,gsL,iL = fullcellFC.getExperimentName(path)
            progressbarval += 14.2857143
            self.fcProgress.setValue(progressbarval)
            fullcellFC.galvanodynamicFileReader(gdL, path)
            progressbarval += 14.2857143
            self.fcProgress.setValue(progressbarval)
            fullcellFC.galvanostaticFileReader(gsL, path)
            progressbarval += 14.2857143
            self.fcProgress.setValue(progressbarval)
            fullcellFC.impedanceFileReader(iL, path, area)
            progressbarval += 14.2857143
            self.fcProgress.setValue(progressbarval)
            fullcellFC.createCSV(path)
            os.chdir(base)
            self.infoWindow.setText(open('Information/idle.html').read())



    def xrdSt(self):
        self.infoWindow.setText(open('Information/xrd.html').read())
        base = os.getcwd()
        path = self.xrdFileText.text()
        csvname = self.xrdCombined.text()
        progressbarval=0
        progressbarval+=16.6666667
        self.xrdProgress.setValue(progressbarval)
        xrd = xrdConvert(path)
        progressbarval+=16.6666667
        self.xrdProgress.setValue(progressbarval)
        listOut = xrd.createListOut(path)
        progressbarval+=16.6666667
        self.xrdProgress.setValue(progressbarval)
        xrd.removeHeader(listOut,path)
        progressbarval+=16.6666667
        self.xrdProgress.setValue(progressbarval)
        listOfCSV,listOfComb,titleList = xrd.xrdCsv(listOut)
        progressbarval+=16.6666667
        self.xrdProgress.setValue(progressbarval)
        xrd.multXrdSupport(listOfComb,titleList)
        progressbarval+=16.6666667
        self.xrdProgress.setValue(progressbarval)
        xrd.generateSheets(listOfCSV,csvname)
        os.chdir(base)
        self.infoWindow.setText(open('Information/idle.html').read())



    def printButtonPressed(self):
        self.infoWindow.setText(open('Information/td.html').read())
        base = os.getcwd()
        #self.consoleTextBrowser.setPlainText('Button Pressed')
        # This is executed when the button is pressed
        path = self.tdFileText.text()
        areaString = self.tDArea.text()
        area = float(areaString)
        csvname = self.tdCombine.text()
        progressbarval = 0
        if self.decadesTDCheck.isChecked():
            decades = True
        else:
            decades = False
        progressbarval += 12.5
        self.progressBar.setValue(progressbarval)
        td = tempConverter(path)
        progressbarval += 12.5
        self.progressBar.setValue(progressbarval)
        td.convertMdatToZip(path)
        progressbarval += 12.5
        self.progressBar.setValue(progressbarval)
        td.unzipFiles(path)
        progressbarval += 12.5
        self.progressBar.setValue(progressbarval)
        td.convertzToTxt(path)
        progressbarval += 12.5
        self.progressBar.setValue(progressbarval)
        newZDir = td.extractedFolder(path)
        progressbarval += 12.5
        self.progressBar.setValue(progressbarval)
        os.chdir(newZDir)
        os.mkdir("DRT-Preprocessing")
        td.fileReader(newZDir,decades,area)
        progressbarval += 12.5
        self.progressBar.setValue(progressbarval)
        td.createMultiX(newZDir,path)
        progressbarval += 12.5
        self.progressBar.setValue(progressbarval)
        td.generateSheets(newZDir,csvname)
        os.chdir(base)
        self.infoWindow.setText(open('Information/idle.html').read())
    def getOutputFoldermc(self):
        pathToWallpaperDir = os.path.normpath(
            QFileDialog.getExistingDirectory(self))
        fileview = self.findChild(QtWidgets.QLineEdit, 'mcExportPath')
        fileview.setText(pathToWallpaperDir) 
    def getMdatFoldermc(self):
        pathToWallpaperDir = os.path.normpath(
            QFileDialog.getExistingDirectory(self))
        fileview = self.findChild(QtWidgets.QLineEdit, 'mcFileText')
        fileview.setText(pathToWallpaperDir)
    
    def getMdatFoldertd(self):
        pathToWallpaperDir = os.path.normpath(
            QFileDialog.getExistingDirectory(self))
        fileview = self.findChild(QtWidgets.QLineEdit, 'tdFileText')  
        fileview.setText(pathToWallpaperDir)
    
    def getMdatFolderxrd(self):
        pathToWallpaperDir = os.path.normpath(
            QFileDialog.getExistingDirectory(self))
        fileview = self.findChild(QtWidgets.QLineEdit, 'xrdFileText')  
        fileview.setText(pathToWallpaperDir)
    
    def getMdatFolderfc(self):
        pathToWallpaperDir = os.path.normpath(
            QFileDialog.getExistingDirectory(self))
        #TODO fix object name
        fileview = self.findChild(QtWidgets.QLineEdit, 'xrdFileText_2')  
        fileview.setText(pathToWallpaperDir)

    def getMdatFolderdrt(self):
        pathToWallpaperDir = os.path.normpath(QFileDialog.getExistingDirectory(self))
        #TODO change object name once fixed
        fileview = self.findChild(QtWidgets.QLineEdit, 'drtFilePath')
        fileview.setText(pathToWallpaperDir)
class File_Handler:
    def __init__(self):
        print('initialized')   
class File_In(File_Handler):
    def __init__(self, file_in, dir_out, is_sym=False, regularization=1e-4):
        
        m = osqp.OSQP()

        try:
            H, f, freq_out, freq, epsilon = octave.main(file_in, regularization, nout=5)
            print("Non-convert to float")
        except:
            H, f, freq_out, freq, epsilon = octave.main(file_in, float(regularization), nout=5)
            print("convert to float")
        #col_g, col_t = octave.main(file_in, nout=2)
        
        self.lb_re = np.zeros((freq.size + 2, 1))
        self.ub_re = np.Inf*np.ones((freq.size + 2, 1))
        #
#
        sH = sparse.csc_matrix(H)
#
        f_c = conj(transpose(f))
#
        m.setup(P=sH, q=f_c, max_iter=10000,  eps_abs=1e-10,  eps_rel=1e-10)
               
#
        results = m.solve()
        x= results.x
        for i in range(x.size):
            if x[i] < 0:
                x[i] =0
        
#
        #
        #
        file_out = file_in.split('/')
        file_out = file_out[len(file_out) -1].strip('.csv')
        gamma_tau, tau = octave.main2(x, freq_out, freq, epsilon, dir_out, file_out, nout=2)

        plot.semilogx(tau, gamma_tau)
        plot.ylim([0, max(gamma_tau[self.find_nearest(tau, 1e-4):gamma_tau.size - 1])])
        plot.xlim([1e-4, max(tau)])
        plot.savefig(dir_out + '/' + file_out + '.png')
        plot.clf()
        

        ##.a_re, self.a_im, self.ZPrime, self.Z2Prime, self.m_re, self.m_im, mhelp.lambd)
        ##h, c = octave.quad_format_combined(self.a_
        #sol = solvers.qp(H,f, solver='MOSEK')
 

        
        
        
        #df = pd.DataFrame({'L': col_g_1, 'R': col_t_1, 'gamma(tau)', })


        #self.xridge = octave.doprog(h, c, self.lb_re, self.ub_re, self.x_re_0, options)
        
        #self.x_ridge = octave.quadprog(self.arr_h_f_comb[0], self.arr_h_f_comb[1], [], [], [], [], self.lb_re, self.ub_re, self.x_re_0, options)
        #self.x_ridge, obj, flag, output, l = octave.qp(self.x_re_0, self.arr_h_f_comb[0], self.arr_h_f_comb[1], [], [], self.lb_re, self.ub_re, options)
    
        #self.df = pd.DataFrame({'L': self.arr_h_f_comb[0][0],'h_1': self.arr_h_f_comb[0][1], 'f_0': self.arr_h_f_comb[1][0],'f_1': self.arr_h_f_comb[1][1]})
        #self.df.to_csv('/home/nick/Projects/DRTConverter/out.csv')
    def find_nearest(self, array, value):
        array = np.asarray(array)
        idx = (np.abs(array - value)).argmin()
        return idx

class fcConvert():
    def __init__(self, path):
        self.filename = path
        self.arrayOfImpFiles = []
        self.impedanceElectrodeASRList = []
        self.impedanceTotalASRList = []
        self.impedanceOhmicList = []
        self.impedanceTimeInSecounds = []
        self.impedanceTimeInHours = []
        self.listOfCSV = []
        self.listOfComb = []
        self.olist = []
        self.nolist = []
        self.tasr = []
        self.acohmic = []
        self.acnonohmic = []
        self.actasr = []
        self.filename =[]
        self.otherthinglist = []
    #converts all mdats to a given zip
    def convertMdatToZip(self,files):
        pattern = '*.mdat'
        for (root,dirs,files) in os.walk(files):
            for filename in fnmatch.filter(files,pattern):
                infilename = os.path.join(root,filename)
                oldbase = os.path.splitext(filename)
                newname = infilename.replace('.mdat', '.zip')
                output = os.rename(infilename, newname)
    
    #unzips all files and puts them in respective folders
    def unzipFiles(self,files):
        pattern = '*.zip'
        for root, dirs, files in os.walk(files):
            for filename in fnmatch.filter(files, pattern):
                print(os.path.join(root,filename))
                zipfile.ZipFile(os.path.join(root,filename)).extractall(os.path.join(root, os.path.splitext(filename)[0]))

    #lists files in a given directory          
    def listFiles(self,files):
        try:
            print("listing files ...")
            os.chdir(files)
            it = sorted(glob.glob('*.*'))
            return(it)
        except OSError:
            print("The OS could not detect that file path")

    #gets the experiment names and adds them to a list
    def getExperimentName(self,files):
        galvanodynamicList = []
        galvanostaticList = []
        impedanceList = []
        os.chdir(files)
        allFolders = [d for d in os.listdir('.') if os.path.isdir(d)]
        for folder in allFolders:
            folderInUnzip = os.path.join(files, folder)
            os.chdir(folderInUnzip)
            runFolders = [d for d in os.listdir('.') if os.path.isdir(d)]
            for runFolder in runFolders:
                filesInRun = os.path.join(folderInUnzip,runFolder)
                os.chdir(filesInRun)
                fileList = self.listFiles(filesInRun)
            for file in fileList:
                with open(file, 'r', encoding = 'ISO-8859-1') as f:       
                    for row in f:
                        if 'Exp Name:' in row:
                            strippedExperimentName = row.strip('Exp Name: \n')
                            if strippedExperimentName == 'Galvanodynamic':
                                galvanodynamicList.append(file)
                                print("found galvanodynamic file: ",file)
                                #return strippedExperimentName,file
                            elif strippedExperimentName == 'Galvanostatic':
                                galvanostaticList.append(file)
                                print("found galvanostatic file: ", file)
                                #return strippedExperimentName,file
                            elif strippedExperimentName == 'Impedanc':
                                for row in f:
                                    if 'End Information' in row:
                                        strippedImpedanceType = row.strip('End Information: \n')
                                        if strippedImpedanceType == 'DC File Columns':
                                            print(file, ' is DC and will be ignored')
                                        if strippedImpedanceType == 'AC File Columns':
                                            impedanceList.append(file) 
                                            print("found AC impedance file: ",file)
        print("all files have been analyzed. Reading data...")
        return galvanodynamicList,galvanostaticList,impedanceList

    #takes all galvanodynamic files and gets the data from them
    def galvanodynamicFileReader(self,gdL,files):
        os.chdir(files)
        path = files
        dfTS,dfTH,dfPPD,dfABS =([] for i in range(4))
        peakPowerDensityList,correctedTimeList=([] for i in range(2))
        for gdFile in gdL:
            print("next file to handle is ",gdFile)
            os.chdir(path)
            print("looking for " , gdFile)
            for root, dirs, files in os.walk(path):
                if gdFile in files:
                    print("System found ", gdFile)
                    newFilePath = os.path.join(root,gdFile)
                    os.chdir(root)
                    stringTime,stringCurrent,stringVoltage,dateTimeList=([] for i in range(4))
                    with open (gdFile, 'r', encoding = 'ISO-8859-1') as f:
                        for row in f:
                            if 'End Header:' in row:
                                strippedEndHeaderData = row.strip('End Header: \n')
                                for x in f:
                                    stringTime.append(x.split('\t')[0])
                                    stringCurrent.append(x.split('\t')[2])
                                    stringVoltage.append(x.split('\t')[1])
                        if stringTime != []:
                            intTime = [float(i) for i in stringTime]
                            intCurrent = [float(i) for i in stringCurrent]
                            intVoltage = [float(i) for i in stringVoltage]
                            intPower = [intCurrent[i]*intVoltage[i] for i in range(len(intCurrent))]
                            peakPowerDensityList=max(intPower)
                        elif stringTime ==[]:
                            print("empty sequence")
                    if stringTime != []:
                        #variable setting and appending to global arrays
                        print("data stored for ",gdFile," parsing data to usable information")
                        timeD = self.getTime(gdFile)
                        dateD = self.getDate(gdFile)
                        dateTimeString = dateD + ' ' + timeD
                        dateTimeFormat = datetime.datetime.strptime(dateTimeString, '%m/%d/%Y %I:%M:%S %p')
                        dateTimeList.append(dateTimeFormat)
                        correctedTime = time.mktime(dateTimeFormat.timetuple())
                        correctedTimeList.append(correctedTime)
                        timeMin = min(correctedTimeList)
            timeInSecounds = ([correctedTimeList[i]-correctedTimeList[0] for i in range(len(correctedTimeList))])
            dfTS.append(timeInSecounds)
            timeInHours = ([((correctedTimeList[i]-timeMin)/3600) for i in range(len(correctedTimeList))])
            dfTH.append(timeInHours)
            dfPPD.append(peakPowerDensityList)
            dfABS.append(correctedTimeList)            
        os.chdir(path)
        print("Creating the CSV...")
        fileN = 'GalvanoDynamic.csv'
        dataf = {'Time': timeInSecounds, 'Time-Hours': timeInHours,'Peak Power Density':dfPPD, 'ABS-Time':correctedTimeList}
        df = pd.DataFrame(data=dataf)
        df.to_csv(fileN, index = False)

    #gets the galvanostatic files and gets the data
    def galvanostaticFileReader(self,gsL, files):
        print("reading galvanostatic files...")
        os.chdir(files)
        path = files
        intTime,intvolt,timeInHours,dateTimeList,floatTime,timeInSecounds,intRelativeTime = ([] for i in range(7))
        for gsFile in gsL:
            print("next file to handle is ",gsFile)
            os.chdir(path)
            print("looking for " , gsFile)
            for root, dirs, files in os.walk(path):
                if gsFile in files:
                    os.chdir(root)
                    stringTime,stringVoltage = ([] for i in range(2))
                    minExpTime = -1
                    with open(gsFile,'r', encoding = 'ISO-8859-1') as f:
                        lingen = itls.islice(f,0,None,60) 
                        for row in f:
                            if 'End Header:' in row:   
                                    for x in lingen:
                                        stringTime.append(x.split('\t')[0])
                                        stringVoltage.append(x.split('\t')[1])
                        if stringTime != []:
                            for i in stringTime:
                                intTime.append(float(i))
                            for i in stringVoltage:
                                intvolt.append(float(i))
                    if stringTime !=[]:
                        print("data stored for ",gsFile," parsing data to usable information")
                        timeD = self.getTime(gsFile)
                        dateD = self.getDate(gsFile)
                        dateTimeString = dateD + ' ' + timeD
                        dateTimeFormat = datetime.datetime.strptime(dateTimeString, '%m/%d/%Y %I:%M:%S %p')

                        dateTimeList.append(dateTimeFormat)
                        timeInSecounds.append(float(time.mktime(dateTimeFormat.timetuple())))
        for i in range(len(intTime)):
            intRelativeTime.append(intTime[i] - intTime[0])
        mintime = min(intRelativeTime)    
        for i in intRelativeTime:
            timeInHours.append((i-mintime) / 3600)
        os.chdir(path)
        print("Creating the CSV...")
        fileN = 'GalvanoStatic.csv'
        dataf = {'Time-Hours': timeInHours, 'Voltage':intvolt}
        df = pd.DataFrame(data=dataf)
        df.to_csv(fileN,index = False)

    #gets the impedance files and gets the data from them
    def impedanceFileReader(self,iL, files,intArea):
        os.chdir(files)
        path = files 
        electrodeASRList,totalASRList, ohmicList, dateTimeList, floatTime, timeInSecounds, timeInHour,tsarAC,electronAC = ([] for i in range(9))
        i=0
        for iFile in iL:
            
            i+=1
            print("next file to handle is ",iFile)
            os.chdir(path)
            print("looking for " , iFile)
            for root, dirs, files in os.walk(path):
                if iFile in files:
                    os.chdir(root)
                    stringZPrime,stringZDoublePrime = ([] for i in range(2))
                    with open(iFile,'r', encoding = 'ISO-8859-1') as f:
                        for row in f:
                            if 'End Header:' in row:
                                for x in f:
                                    stringZPrime.append(x.split('\t')[4])
                                    #intZPrime.append(float(x.split('\t)[4]))
                                    stringZDoublePrime.append(x.split('\t')[5])
                                if stringZPrime !=[]:
                                    intZPrime = [float(i) for i in stringZPrime]
                                    intzDoublePrime = [float(i) for i in stringZDoublePrime]
                                    startRange, endRange = self.getRange(intzDoublePrime)
                                    if endRange == -1:
                                        zDoublePrimeShort = max(intzDoublePrime)
                                        zDoublePrimeABS = zDoublePrimeShort
                                        ohmicZDoublePrime = zDoublePrimeShort
                                    if endRange > 0:
                                        intStart = int(startRange)
                                        intEnd = int(endRange)
                                        zDoublePrimeShort = intzDoublePrime[intStart:intEnd]

                                    #zDoublePrimeShort = intzDoublePrime[5:25]
                                        zDoublePrimeABS = [abs(i) for i in zDoublePrimeShort]
                                        ohmicZDoublePrime = min(zDoublePrimeABS)
                                elif stringZPrime == []:
                                    print("empty sequence")
                        if stringZPrime != []:
                            print("data stored for ",iFile,". parsing data to usable information")
                            ohmicZDoublePrime = min(zDoublePrimeABS)
                            if ohmicZDoublePrime in intzDoublePrime:
                                ohmicZPrimeIndex = intzDoublePrime.index(ohmicZDoublePrime)
                            else:
                                ohmicZPrimeIndex = intzDoublePrime.index(-ohmicZDoublePrime)
                            #ammending things and setting things   
                            ohmicMin = intZPrime[ohmicZPrimeIndex]
                            totalASR = max(intZPrime[ohmicZPrimeIndex:])
                            electrodeASR = totalASR-ohmicMin                        
                            electrodeASRList.append(electrodeASR)                       
                            totalASRList.append(totalASR)                    
                            ohmicList.append(ohmicMin)
                            #timeT = getTime(iFile)
                            #dateD = getDate(iFile)

                            #________NICKS DATATIME_______#
                            #dataTimeTuple = getMetaData(iFile)
                            #dataTine = datetine.datetime.strptime("{} {}".format(dateTimeTuple[0], dateTimeTuple[1], '%m/%d/%Y %I:%M:%S %p'))
                            #timeInSecounds.append(float(time.mktime(dateTime.timetuple())))
                            #minTime = min(timeInSecounds)
                            #________NICKS DATATIME_______#
                            t_d_array = self.getMetaData(iFile)
                            timeT = t_d_array[1]
                            dateD = t_d_array[0]
                            dateTimeString = dateD + ' ' + timeT
                            dateTimeFormat = datetime.datetime.strptime(dateTimeString, '%m/%d/%Y %I:%M:%S %p')
                            dateTimeList.append(dateTimeFormat)
                            correctedTime = time.mktime(dateTimeFormat.timetuple())
                            floatTime.append(float(correctedTime))                    
                            timeInSecounds.append(correctedTime)
                            minTime = min(timeInSecounds)         
                            impedanceTimeInHours = [((timeInSecounds[i]-minTime)/3600) for i in range(len(timeInSecounds))]
                            tsarAC.append(float(intArea*totalASR))
                            electronAC.append(float(intArea*electrodeASR))
        os.chdir(path)
        print("creating the CSV...")
        fileN = "Impedance.csv"
        dataf = { 'time' :timeInSecounds, "time(hours)":impedanceTimeInHours, 'Electrode' : electrodeASRList , 'Ohmic':ohmicList ,'tasr': totalASRList, 'tsarAC' : tsarAC, 'ElectrodeAC' : electronAC}
        df = pd.DataFrame(data=dataf)
        df.to_csv(fileN,index = False)

    def getRange(self,intZDoublePrime):
        PG=[]
        NG=[]
        t=0
        for i in range(len(intZDoublePrime)):
            if intZDoublePrime[i] > 0:
                t+1
            elif intZDoublePrime[i] < 0:
                if intZDoublePrime[i-1] >0:
                    indexx = i-1
                    break
        for i in range(len(intZDoublePrime)):
            if intZDoublePrime[i] < 0:
                PG.append(i)
            elif intZDoublePrime[i] > 0:
                NG.append(i)
            elif intZDoublePrime[i] == 0:
                OH = intZDoublePrime[i]
                break
        if NG == [] and PG != []:
            startRange = min(intZDoublePrime)
            endRange = -1
        if NG != [] and PG != []:
            j = (len(NG))
            startRange = indexx
            endRange = startRange + 1
        return(startRange,endRange)

    #gets the date in the file
    def getDate(self,file):
        with open(file,'r',encoding = "ISO-8859-1") as f:
            for row in f:
                if 'Date:' in row:
                    strippedDate= row.strip('Date: \n')
                    return strippedDate

    #gets the time in the file
    def getTime(self,file):
        with open(file,'r',encoding = "ISO-8859-1") as f:
                for row in f:
                    if 'Time:' in row:
                        strippedTime= row.strip('Time: \n')
                        return strippedTime
    def convertDate(self,europeanDate):
        splitDate = europeanDate.split("/")
        return splitDate[1] + "/" + splitDate[0] + "/" + splitDate[2]

    def getMetaData(self,filename):
        multistatVersionFound = False
        convertDateB = False
        LOOKUP_DATE = "Date:"
        LOOKUP_TIME = "Time:"
        stringDate = ''
        stringTime = ''
        stf = False
        sdf = False
        with open(filename, 'r') as file:
            for line in file:
                if '1.7a-mem1' in line:
                    multistatVersionFound = True
                    convertDateB = True
                if '1.7f' in line or '1.6c' in line:
                    multistatVersionFound = True
                    convertDateB = False
                if multistatVersionFound and LOOKUP_DATE in line:
                    stringDate = line.split()[1]
                    if convertDateB:
                        stringDate = self.convertDate(stringDate)
                    sdf = True
                elif multistatVersionFound and LOOKUP_TIME in line and 'Start' not in line and 'Delta' not in line and 'Offset' not in line and 'Total' not in line and 'Step' not in line:
                    stringTime = line.split()
                    stf = True
                if sdf and stf:
                    break
        return [stringDate, stringTime[1] + ' ' + stringTime[2]]

    def createCSV(self,files):
        #TODO
        print("All CSV's Have been created click ok to close the window.")
        print("Maryland Energy Innovation Institute -> written by Jonathan Obenland ")

class tempConverter():
    def __init__(self,path):
        self.filename = path
        self.arrayOfImpFiles = []
        self.impedanceElectrodeASRList = []
        self.impedanceTotalASRList = []
        self.impedanceOhmicList = []
        self.impedanceTimeInSecounds = []
        self.impedanceTimeInHours = []
        self.listOfCSV = []
        self.listOfComb = []
        self.olist = []
        self.nolist = []
        self.tasr = []
        self.acohmic = []
        self.acnonohmic = []
        self.actasr = []
        self.filename =[]
        self.otherthinglist = []
        
    def convertzToTxt(self,files):
        pattern = '*.z'
        for (root,dirs,files) in os.walk(files):
            for filename in fnmatch.filter(files,pattern):
                infilename = os.path.join(root,filename)
                oldbase = os.path.splitext(filename)
                newname = infilename.replace('.z', '.txt')
                try:
                    output = os.rename(infilename, newname)
                except FileExistsError:
                    pass

    def generateSheets(self,newZDir,csvname):
        print('System STANDBY. Awaiting user input')
        
        
        print('Ready to ammend to ', csvname)
        writer = pd.ExcelWriter(csvname + '.xlsx', engine= 'xlsxwriter')
        
        for csv in self.listOfCSV:
            filename, file_extension = os.path.splitext(csv)
            if filename == "Resistance Table.csv":
                print("ignoring system file...")
                break
            print('found ', filename, ' adding to ',csvname) 
            df = pd.read_csv(csv)
            sheetName = filename
            if 'EIS_OCV' in filename:
                sheetName = sheetName.strip('EIS_OCV')
                sheetNameSplit = sheetName.split('_')
                sheetName = sheetNameSplit[0]+sheetNameSplit[1]+sheetNameSplit[2]
            try:      
                df.to_excel(writer, sheet_name=sheetName)
            except xlsxwriter.exceptions.DuplicateWorksheetName:
                print("Duplicate name found, adding DUP to name and ammending...")
                sheetName = sheetNameSplit[0]+sheetNameSplit[1]+sheetNameSplit[2] + "DUP"
                print("duplicate sheet name ",sheetName, " added")
                df.to_excel(writer, sheet_name=sheetName)
        writer.save()

    def createMultiX(self,newZDir,defaultDir):
        titleList=[]
        rTable = 'Resistance Table.csv'
        rt = {'Filename':self.filename,
            'Ohmic': self.olist,
            'NonOhmic' : self.nolist,
            'Tasr' : self.tasr,
            'Area Corrected Ohmic' : self.acohmic,
            'Area Corrected Non Ohmic' : self.acnonohmic,
            'Area Corrected Tasr' : self.actasr}
        dt = pd.DataFrame(data=rt)
        dt.to_csv(rTable,index = False)
        self.listOfCSV.append(rTable)

    def extractedFolder(self,files):
        newDirName = files
        os.chdir(newDirName)
        #pulling all .z files from the extracted folders into a new folder
        combAll = 'Extracted_Z_Files_And_CSV'
        if not os.path.exists(combAll):
            os.mkdir(combAll)
            print("Directory " , combAll ,  " Created ")
        else:    
            print("Directory " , combAll ,  " already exists")    
        newZDir = newDirName + '/' + combAll
        for root, dirs, files in os.walk((os.path.normpath(newDirName)), topdown=False):
            for name in files:
                if name.endswith('.txt'):
                    try:
                        print (name, 'has a z extension. moving to combined folder')
                        SourceFolder = os.path.join(root,name)
                        shutil.copy2(SourceFolder,newZDir)
                    except shutil.SameFileError:
                        print(name , " was found with the same file name")       
        return(newZDir)
    
    #Converts the MDATS to ZIPS to be unzipped
    def convertMdatToZip(self,files):
        pattern = '*.mdat'
        for (root,dirs,files) in os.walk(files):
            for filename in fnmatch.filter(files,pattern):
                infilename = os.path.join(root,filename)
                oldbase = os.path.splitext(filename)
                newname = infilename.replace('.mdat', '.zip')
                output = os.rename(infilename, newname)
    
    #Unzips the newly zipped files
    def unzipFiles(self,files):
        pattern = '*.zip'
        for root, dirs, files in os.walk(files):
            for filename in fnmatch.filter(files, pattern):
                print(os.path.join(root,filename))
                zipfile.ZipFile(os.path.join(root,filename)).extractall(os.path.join(root, os.path.splitext(filename)[0]))
    
    #TODO make sure this isnt needed and remove
    #THIS is never called
    def listOfImpFiles(self,files):
        fileList = os.listdir(files)
        os.chdir(files)
        for file in fileList:
            with open(file, "r", encoding = 'ISO-8859-1') as f:
                for row in f:
                    if 'Exp Name:' in row:
                        strippedExperimentName = row.strip('Exp Name: \n')
                        if strippedExperimentName == 'Impedanc':
                            for row in f:
                                if 'End Information' in row:
                                    strippedImpedanceType = row.strip('End Information: \n')
                                    if strippedImpedanceType == 'AC File Columns':
                                        arrayOfImpFiles.append(file)
        return arrayOfImpFiles
    
    #Reads and does math on the files passed in
    def fileReader(self,impFiles,decades,area):
        
        
        os.chdir(impFiles)
        listF = os.listdir(impFiles)
        i=0
        for file in listF:
            i+=1
            stringFreq = []
            stringTS = []
            stringZPrime = []
            stringZDoublePrime = []
            decFreqIndex = []
            decFreq=[]
            decZP = []
            decZDP = []
            skip = False
            try:
                with open (file, 'r', encoding = 'ISO-8859-1') as f:
                    for row in f:
                        if 'End Header:' in row:
                            for x in f:
                                stringFreq.append(x.split('\t')[0])
                                stringTS.append(x.split('\t')[3])
                                stringZPrime.append(x.split('\t')[4])
                                stringZDoublePrime.append(x.split('\t')[5])
                            intFreq = [float(i) for i in stringFreq]
                            intTS = [float(i) for i in stringTS]
                            intZPrime = [float(i) for i in stringZPrime]
                            intZDoublePrime = [float(i) for i in stringZDoublePrime]
                            startRange,endRange = self.getRange(intZDoublePrime)

                            if endRange == -1:
                                zDoublePrimeShort = max(intZDoublePrime)
                                zDoublePrimeABS = zDoublePrimeShort
                                ohmicZDoublePrime = zDoublePrimeShort
                            elif endRange > 0:
                                intStart = int(startRange)
                                intEnd = int(endRange)
                                zDoublePrimeShort = intZDoublePrime[intStart:intEnd]
                                zDoublePrimeABS= [abs(i) for i in zDoublePrimeShort]
                                ohmicZDoublePrime = min(zDoublePrimeABS)
                    intArea = (float(area))
                    if ohmicZDoublePrime in intZDoublePrime:
                        ohmicZPrimeIndex = intZDoublePrime.index(ohmicZDoublePrime)
                        ohmicZPrime = intZPrime[ohmicZPrimeIndex]
                    else:
                        ohmicZPrimeIndex = intZDoublePrime.index(-ohmicZDoublePrime)
                        ohmicZPrime = intZPrime[ohmicZPrimeIndex]
                    zPrimeOC = [((intZPrime[i])-(ohmicZPrime)) for i in range(len(intZPrime))]
                    zPrimeARC= [((zPrimeOC[i])*(intArea)) for i in range(len(intZPrime))]
                    zDoublePrimeARC = [((intZDoublePrime[i])*(intArea)) for i in range(len(intZDoublePrime))]
                    positiveZDoublePrime = [-x for x in zDoublePrimeARC]
                    if decades==True:
                        for val in intFreq:
                            dectest = math.log10(val)
                            try:
                                dosomething = dectest - math.floor(dectest)
                                if dosomething > 0.0 :
                                    pass
                                elif dosomething == 0.0:
                                    decFreq.append(val)
                                    #indexx = intFreq.index(val)
                                    decFreqIndex.append(intFreq.index(val))
                            except:
                                print("not a decade")
                        for dec in decFreqIndex:
                            decZP.append(zPrimeARC[dec])
                            decZDP.append(zDoublePrimeARC[dec])
                        nameoffile, file_extension = os.path.splitext(file)
                        datadec = { 'Frequency' : decFreq, 'Z Prime' : decZP, 'Z Double Prime' : decZDP}
                        dec = pd.DataFrame(data=datadec)
                        fileName = nameoffile +'-Decades.csv'
                        dec.to_csv(fileName,index = False)
            except PermissionError:
                print("this was a folder")
                skip = True

            if skip == False:
                self.olist.append(ohmicZPrime)
                self.nolist.append(intZPrime[-1]-ohmicZPrime)
                self.tasr.append(intZPrime[-1])
                self.acohmic.append(ohmicZPrime*intArea)
                self.acnonohmic.append((intZPrime[-1]-ohmicZPrime)*intArea)
                self.actasr.append(intZPrime[-1]*intArea)
                self.filename.append(file)
                nameoffile, file_extension = os.path.splitext(file)
                comb = [(zPrimeARC[i],positiveZDoublePrime[i]) for i in range(len(zPrimeARC))]
                dataf = { 'Frequency' :intFreq,'Time In Seconds' : intTS, 'Z Prime' : intZPrime, 'Z Double Prime' : intZDoublePrime, 'Z Prime Ohmic Corrected' : zPrimeOC,
                'z Prime Area Corrected' : zPrimeARC, 'Z Double Prime Area Corrected' : zDoublePrimeARC, '+- Z Double Prime' : positiveZDoublePrime, 'DUAL COL' : comb} #column headings for the excel file
                df = pd.DataFrame(data=dataf)
                fileName = nameoffile +'.csv'
                df.to_csv(fileName,index = False)
                self.listOfCSV.append(fileName)
                self.listOfComb.append(comb)
                os.chdir("DRT-Preprocessing")
                dataDRT = {'Frequency' : intFreq, 'Z Prime Ohmic Corrected' : zPrimeARC, 'Z Double Prime Area Corrected' : zDoublePrimeARC}
                dt = pd.DataFrame(data=dataDRT)
                noRun1 = nameoffile.strip('Run01')
                fileName = noRun1 + 'DRTPP.csv'
                dt.to_csv(fileName,index=False,header=None)
                print(file, " has been parsed. continuing to next file...")
                os.chdir(impFiles)

            
    
    #Helper function to get the range of the location of the ohmic
    def getRange(self,intZDoublePrime):
        PG=[]
        NG=[]
        t=0
        for i in range(len(intZDoublePrime)):
            if intZDoublePrime[i] > 0:
                t+1
            elif intZDoublePrime[i] < 0:
                if intZDoublePrime[i-1] >0:
                    indexx = i-1
                    break
        for i in range(len(intZDoublePrime)):
            if intZDoublePrime[i] < 0:
                PG.append(i)
            elif intZDoublePrime[i] > 0:
                NG.append(i)
            elif intZDoublePrime[i] == 0:
                OH = intZDoublePrime[i]
                break
        if NG == [] and PG != []:
            startRange = min(intZDoublePrime)
            endRange = -1
        if NG != [] and PG != []:
            j = (len(NG))
            startRange = indexx
            endRange = startRange + 1
        return(startRange,endRange)

class xrdConvert():
    def __init__(self,path):
        self.filename = path
        self.arrayOfImpFiles = []
        self.impedanceElectrodeASRList = []
        self.impedanceTotalASRList = []
        self.impedanceOhmicList = []
        self.impedanceTimeInSecounds = []
        self.impedanceTimeInHours = []
        self.listOfCSV = []
        self.listOfComb = []
        self.olist = []
        self.nolist = []
        self.tasr = []
        self.acohmic = []
        self.acnonohmic = []
        self.actasr = []
        self.filename =[]
        self.otherthinglist = []

    def createListOut(self,files):
        listOut = []
        os.chdir(files)
        fileList = os.listdir(files)  
        for file in fileList:
            filename, file_extension = os.path.splitext(file)     
            if file_extension == '.out':
                print(file ," Is a useable OUT file. Reading... ")
                listOut.append(file)
            if file_extension != '.out':
                print(file ," Is not a usable OUT file. Ignoring...")
            else:
                print(file, " Is Unrecognized by OS. Ignoring...")
        return listOut
    
    def removeHeader(self,listOut,files):
        os.chdir(files)
        for outFile in listOut:
            with open (outFile, 'r', encoding = 'ISO-8859-1') as openedFile:
                rowNumber=0
                for row in openedFile:
                    rowNumber+=1
                    try:
                        removedFormatting = row.replace('\n','')
                        removedFormatting = removedFormatting.replace('\t','')
                        removedFormatting = removedFormatting.replace(' ', '')
                        float(removedFormatting)
                        print('end of header indicated at ', rowNumber-1, ' Getting following data...')
                        endHeaderRow = rowNumber-1
                        break
                    except ValueError:
                        print('row ', row, ' was not end of header. Retrying next row...')
            print('Opening file and ammending lines')
            removeHeader = open(outFile, 'r')
            dataToRemove = removeHeader.readlines()
            removeHeader.close
            print('System STANDBY. awaiting user approval...')
            
            print('Deleting lines 0 -> ' , endHeaderRow)
            del dataToRemove[0:endHeaderRow]
            print('Deleted. Rewriting files...')
            headerLess = open(outFile,'w')
            headerLess.writelines(dataToRemove)
            headerLess.close()
            print ("Header Successfully Removed")

    def xrdCsv(self,listOut):
        listOfCSV = []
        listOfComb = []
        titleList = []
        fileCount =0
        for outFile in listOut:
            filename, file_extension = os.path.splitext(outFile)
            titleList.append(filename)
            stringAngle=[]
            stringIntensity=[]
            normalizedIntensity=[]
            print('Opening ',outFile,'. Getting Data...')
            with open (outFile, 'r', encoding = 'ISO-8859-1') as f:           
                for row in f:
                    for x in f:
                        sentence = " ".join(re.split("\s+", x, flags=re.UNICODE))
                        stringAngle.append(sentence.split(' ')[0])
                        stringIntensity.append(sentence.split(' ')[1])
                    intAngle = [float(i) for i in stringAngle]
                    intIntensity = [float(i) for i in stringIntensity]
                    maxIntensity = max(intIntensity)
                    normalizedIntensity = [((intIntensity[i])/(maxIntensity)) for i in range(len(intAngle))]
                print('All Data Found. Creating CSV...')
                csvName = filename +'.csv'
                comb = filename + 'Combined'
                comb = [(intAngle[i],(normalizedIntensity[i]+(1.1*fileCount))) for i in range(len(normalizedIntensity))]
                dataf = {'Angle' : intAngle, 'Intensity' : intIntensity, 'Normalized Intensity' : normalizedIntensity, 'Multi-XRD Support' : comb}
                df = pd.DataFrame(data=dataf)
                df.to_csv(csvName, index = False)
                print( csvName, ' created. adding to CSV creation list...')
                listOfCSV.append(csvName)
                listOfComb.append(comb)
                fileCount+=1
        return listOfCSV,listOfComb,titleList

    def generateSheets(self,listOfCSV,csvname):
        print('System STANDBY. awaiting user input')
        
        print('Ready to ammend to ', csvname)
        writer = pd.ExcelWriter(csvname + '.xlsx', engine = 'xlsxwriter')
        for csv in listOfCSV:
            filename, file_extension = os.path.splitext(csv)
            print('found ', filename, ' adding to ',csvname) 
            df = pd.read_csv(csv)
            df.to_excel(writer, sheet_name=filename)
        writer.save()  

    def multXrdSupport(self,listOfComb,titleList):
        fileN = "Multi XRD Support.csv"
        for arr in range(len(listOfComb)):
            if arr == 0:
                dataf = {titleList[0] : listOfComb[arr]}
                df = pd.DataFrame(data=dataf)
            if arr != 0:
                head = titleList[arr]
                df[head] = listOfComb[arr]
                df.to_csv(fileN, index = False)
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
            if p_dir[0] == '/':
                p_dir = p_dir[1:]
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

# Class for Nicks full cell batch extractor for Galvanostatic files
class Impedance(FileHandler):
    def __init__(self, fileList):
        self.listFiles = []
        for file in fileList:
            self.listFiles.append(file)

        self.electrodeASRList = []
        self.totalASRList = []
        self.ohmicList = []

        self.timeSeconds = []
        self.timeHours = []
        #ZPrime = []
        #ZPrime = []
        ZPrimeShort = []
        ZPrimeABS = []

    # Written by Jobenland
    def getRange(self, intZDoublePrime):
        PG=[]
        NG=[]
        t=0
        #first part tests point and the next point
        #to find positive then negative
        startRange = 0
        for i in range(len(intZDoublePrime)):
            if intZDoublePrime[i] > 0:
                t+1
            elif intZDoublePrime[i] < 0:
                if intZDoublePrime[i-1] >0:
                    indexx = i-1
                    break

        #makes lists for all the positive corresponding index
        #makes lists for all the negative corresponding index
        for i in range(len(intZDoublePrime)):
            if intZDoublePrime[i] < 0:
                PG.append(i)
            elif intZDoublePrime[i] > 0:
                NG.append(i)
            elif intZDoublePrime[i] == 0:
                OH = intZDoublePrime[i]
                break
    
       #checking to make sure that the graph has both
       #positive and negative values
        if NG == [] and PG != []:
            startRange = min(intZDoublePrime)
            endRange = -1
        if NG != [] or PG != []:
            j = (len(NG))
            startRange = int(min(intZDoublePrime))
            endRange = startRange + 1
        try:
            return(startRange,endRange)
        except UnboundLocalError:
            return(0,1)
    def extractData(self, fileList, directory, output_directory, is_aging):
        os.chdir(directory)
        intTime = []
        ohmicZ2Prime = 0
        ohmicZPrimeIndex = 0

        ohmicZPrime = 0
        ohmicMin = 0
        headerFound = False
        totalASR = 0
        fileList = natsort.natsorted(fileList)
            
        for files in fileList:
            ZPrime = []
            Z2Prime = []
            frequency = []
            if '.z' in files:
                
                with open(directory + '/' + files, 'r', encoding=ENCODING) as f:
                    for row in f:
                        if LOOKUP_END_HEADER in row:
                            headerFound = True
                            continue
                        elif headerFound:
                            ZPrime.append(float(row.split('\t')[4]))
                            Z2Prime.append(float(row.split('\t')[5]))
                            frequency.append(float(row.split('\t')[1]))
                    startrange, endrange = self.getRange(Z2Prime)
                    
                    if endrange > 0:

                        # IS THIS THIS RIGHT
                        ohmicZ2Prime = min([abs(i) for i in Z2Prime[startrange:endrange]])
                        ###########################

                        mv1 = 0
                        mv2 = 0
                        firstval = False
                        #for values in Z2Prime:
                        #    if values < 0 and  not firstval:
                        #        mv1 = values
                        #        firstval = True
                        #    if firstval and (values > mv1):
                        #        ohmicZ2Prime = mv1
                        #        print("New ohmic minimum found")
                        #    else:
                        #        mv1 = values
                    elif endrange == -1:
                        ohmicZ2Prime = min(Z2Prime)

                    

                    if ohmicZ2Prime in Z2Prime:
                        ohmicZPrimeIndex = Z2Prime.index(ohmicZ2Prime)
                    else:
                        ohmicZPrimeIndex = Z2Prime.index(-ohmicZ2Prime)

                    ohmicMin = ZPrime[ohmicZPrimeIndex]
                    ASRMax = max(ZPrime[ohmicZPrimeIndex:])
                    eASR = ASRMax - ohmicMin
                    if eASR == 0:
                        print(files)
                        print(ZPrime)
                        print(Z2Prime)

                    self.electrodeASRList.append(eASR)
                    self.totalASRList.append(ASRMax)
                    self.ohmicList.append(ohmicMin)

                    dateTimeTuple = self.getMetaData(files, directory)
                    dateTime = datetime.datetime.strptime("{} {}".format(dateTimeTuple[0], dateTimeTuple[1]), '%m/%d/%Y %I:%M:%S %p')
                    self.timeSeconds.append(float(time.mktime(dateTime.timetuple())))
                    minTime = min(self.timeSeconds)

                    self.timeHours = [((self.timeSeconds[i]-minTime)/3600) for i in range(len(self.timeSeconds))]

                    #Z CSV creation
                    if not is_aging:
                        dataf = {
                            'Frequency': frequency,
                            'ZPrime': ZPrime,
                            'ZDoublePrime': Z2Prime
                        }
                        self.createSingleFileCSV(dataf, files, output_directory)
                        print("IMPEDANCE createSingleFileCSV called")
            headerFound = False
        #print("Impedance data extraction complete")
    
    def calculateFromCSV(self, file):
        dataf = pd.read_csv(file, names=['Frequency', 'ZPrime', 'ZDoublePrime'])
        Frequency = dataf.Frequency.tolist()[1:]
        ZPrime = dataf.ZPrime.tolist()[1:]
        Z2Prime = dataf.ZDoublePrime.tolist()[1:]

        for i in range(len(ZPrime)):
            ZPrime[i] = float(ZPrime[i])
            Z2Prime[i] = float(Z2Prime[i])
            Frequency[i] = float(Frequency[i])

        startRange, endrange = self.getRange(Z2Prime)

        if endrange > 0:
            ohmicZ2Prime = min([abs(i) for i in Z2Prime[startRange:endrange]])
            mv1 = 0
            mv2 = 0
            firstval = False
            for values in Z2Prime:
                if values < 0 and  not firstval:
                    mv1 = values
                    firstval = True
                if firstval and (values > mv1):
                    ohmicZ2Prime = mv1
                    print("New ohmic minimum found")
                else:
                    mv1 = values
        elif endrange == -1:
            ohmicZ2Prime = min(Z2Prime)
        
        if ohmicZ2Prime in Z2Prime:
            ohmicZPrimeIndex = Z2Prime.index(ohmicZ2Prime)
        else:
            ohmicZPrimeIndex = Z2Prime.index(-ohmicZ2Prime)
        ohmicMin = ZPrime[ohmicZPrimeIndex]
        ASRMax = max(ZPrime[ohmicZPrimeIndex:])
        eASR = ASRMax - ohmicMin

        return [file, eASR, ASRMax, ohmicMin]
    def createCSV(self, fileName, directory):
        os.chdir(directory)
        fn = fileName + '_' + IMPEDANCE_TAG + '.csv'

        dataf = {
            'Time': self.timeSeconds,
            'Time-Hours': self.timeHours,
            'Electrode': self.electrodeASRList,
            'Ohmic': self.ohmicList,
            'TASR': self.totalASRList
        }
        if len(self.timeSeconds) != 0:
            df = pd.DataFrame(data=dataf)
            df.to_csv(fn, index=False)
            print("Created", fn)
    def createSingleFileCSV(self, dataframe, filename, export_directory):
        export_dir = export_directory + '/' + "imp_file_csvs"
        try:
            os.mkdir(export_dir)
        except(FileExistsError):
            pass
        os.chdir(export_dir)
        df = pd.DataFrame(data=dataframe)
        df.to_csv(filename.replace('.z', '.csv'), index=False)
    def createSummary(self, directory):
        os.chdir(directory)
        dataList = []
        for csv in natsort.natsorted(os.listdir(directory)):
            dataList.append(self.calculateFromCSV(directory + '/' + csv))
        fn_list = []
        eASR_list = []
        ASRM_list = []
        ohmicMin_List = []
        for data in dataList:
            fn_list.append(data[0])
            eASR_list.append(data[1])
            ASRM_list.append(data[2])
            ohmicMin_List.append(data[3])
        for i in range(len(fn_list)):
            fn_list[i] = fn_list[i].split('/')[len(fn_list[i].split('/')) - 1]
        dataf= {
            'File': fn_list,
            'Electrode_ASR': eASR_list,
            'ASR_Max': ASRM_list,
            'Ohmic': ohmicMin_List
        }
        summary_frame = pd.DataFrame(data=dataf)
        summary_frame.to_csv('1_Summary.csv', index=False)

# Class for Nicks full cell batch extractor for Galvanostatic files                    
class Galvanostatic(FileHandler):
    def __init__(self, fileList):
        self.listFiles = copy.deepcopy(fileList)
        self.voltageList = []
        self.minExpTime = -1
        self.timeSince1970 = []

        self.timeSeconds = []
        self.timeHours = []
        self.expTime = []
    def extractData(self, fl, directory):
        fileList = natsort.natsorted(fl)
        if len(fileList) > 0:
            os.chdir(directory)
            intTime = []

            for files in fileList:

                with open(files, 'r', encoding=ENCODING) as f:
                    lineGen = itls.islice(f, 0, None, 60)
                    for row in f:
                        if LOOKUP_END_HEADER in row:
                            for x in lineGen:
                                x_split = x.split('\t')
                                intTime.append(float(x_split[0]))
                                self.voltageList.append(float(x_split[1]))

                dateTimeTuple = self.getMetaData(files, directory)
                dateTime = datetime.datetime.strptime("{} {}".format(dateTimeTuple[0], dateTimeTuple[1]), '%m/%d/%Y %I:%M:%S %p')
                self.timeSeconds.append(float(time.mktime(dateTime.timetuple())))

            if self.minExpTime == -1:
                self.minExpTime = intTime[0]

            for i in intTime:
                self.expTime.append(i - self.minExpTime)

            

            

            # For i in (time since experiment started), 
            for i in self.expTime:
                self.timeSince1970.append((i + self.timeSeconds[0]))
            minTime = min(self.timeSince1970)
            for i in self.timeSince1970:
                self.timeHours.append((i - minTime) / 3600)
                
    
    def createCSV(self, filename, directory):

        os.chdir(directory)
        fn = filename + '_' + STATIC_TAG + '.csv'
        dataf = {
        "ABS_TIME": self.timeSince1970, # 165
        'Time_Min': self.expTime, # 165
        'Time-Hours': self.timeHours,  # 165
        'Voltage': self.voltageList}   # 105
        if len(self.expTime) != 0:
            df = pd.DataFrame(data=dataf)
            df.to_csv(fn, index = False)
            print("Created", fn)

# Class for Nicks full cell batch extractor for Galvanodynamic files
class Galvanodynamic(FileHandler):

    def __init__(self, fileList):
        
        self.listFiles = []
        for file in fileList:
            self.listFiles.append(file)
        self.timeSeconds = []
        self.adjustedTimeSeconds = []
        self.realTime = []
        self.timeHours = []
        self.peakPowerDensityList = []
        self.CorrectedTimeList = []
        self.fileDataList = []
    def createSingleFileCSV(self, dataframe, filename, export_directory):
        
        export_dir = export_directory + '/' + "dyn_file_csvs" 
        try:
            os.mkdir(export_dir)
        except(FileExistsError):
            pass
        os.chdir(export_dir)
        dataf = pd.DataFrame(data=dataframe)
        if '.cor' in filename:
            dataf.to_csv(filename.replace('.cor', '.csv'), index=False)
        elif '.txt' in filename:
            dataf.to_csv(filename.replace('.txt', '.csv'), index=False)
    def extractData(self, fileList, directory, output_directory, is_aging):
        os.chdir(directory)
        fileList = natsort.natsorted(fileList)
        ret_val = []
        if len(fileList):
            for file in fileList:
                voltage = []
                current = []
                power = []
                ocv = 0
                dataFound = False
                if file :
                    with open(directory + '/' + file, 'r', encoding=ENCODING) as f:
                        for row in f:
                            if 'Open Circuit Potential' in row:
                                ocv = float(row.split(':')[1].strip('\t'))
                            if LOOKUP_END_HEADER in row:
                                dataFound = True
                            elif dataFound:
                                split_line = row.split('\t')
                                self.timeSeconds.append(float(split_line[0]))
                                voltage.append(float(split_line[1]))
                                current.append(float(split_line[2]))
                                power.append(float(split_line[1]) * float(split_line[2]))
                    if len(power):
                        self.peakPowerDensityList.append(max(power))
                    else:
                        self.peakPowerDensityList.append(0)
                    metaData = self.getMetaData(file, directory)
                    dateTime = datetime.datetime.strptime("{} {}".format(metaData[0], metaData[1]), '%m/%d/%Y %I:%M:%S %p')
                    self.realTime.append(float(time.mktime(dateTime.timetuple())))

                    if not is_aging:
                        dataf = {
                            'Voltage': voltage,
                            'Current': current,
                            'Power': power
                        }
                        self.createSingleFileCSV(dataf, file, output_directory)
                        if power and ocv:  
                            ret_val.append(self.calculateFromCSV(file, ocv, max(power)))
            timeMin = min(self.realTime)
            for i in self.realTime:
                self.adjustedTimeSeconds.append(i - timeMin)
            for i in self.adjustedTimeSeconds:
                self.timeHours.append(i / 3600)
        if not is_aging:
            return ret_val
        else:
            return None
    def createCSV(self, filename, directory):
        os.chdir(directory)
        fn = filename + '_' + DYNAMIC_TAG + '.cor'
        dataf = {
        'ABS_TIME': self.realTime,
        'Time': self.adjustedTimeSeconds,
        "Time-Hours": self.timeHours, 
        'PPD': self.peakPowerDensityList
        }
        if len(self.adjustedTimeSeconds) != 0:
            df = pd.DataFrame(data=dataf)
            if '.cor' in fn:
                df.to_csv(fn.replace('.cor', '.csv'), index = False)
            elif '.txt' in fn:
                df.to_csv(fn.replace('.txt', '.csv'), index = False)
            print("Created", fn)
    def calculateFromCSV(self, file, ocv, ppd):
        return [file, ocv, ppd]
    def createSummary(self, directory):
        os.chdir(directory)
        file_l = []
        ppd_l = []
        ocv_l = []

        for i in self.fileDataList:
            file_l.append(i[0])
            ppd_l.append(i[2])
            ocv_l.append(i[1])
        dataf = {
            'File': file_l,
            'PPD': ppd_l,
            'OCV': ocv_l
        }
        df = pd.DataFrame(data=dataf)
        df.to_csv('1_Summary.csv', index=False)



        
        

app = QtWidgets.QApplication(sys.argv)
window = Ui()
app.exec_()


    
    