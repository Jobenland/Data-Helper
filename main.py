from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QFileDialog
import os
import sys
import sys
import tkinter
from tkinter import ttk
import abc
import os
import csv
import os, sys
import numpy as np
import pandas as pd
import pandas
import glob as gb
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
        self.textBrowser.setPlainText(text)
        self.infoWindow.setText(open('Information/idle.html').read())
        self.temp = tempConverter(path)
        
        printer = self.findChild(QtWidgets.QScrollArea,'outPutArea')
        self.tdBrowse.clicked.connect(self.getMdatFoldertd)
        self.xrdBrowse.clicked.connect(self.getMdatFolderxrd)
        self.fcBrowse.clicked.connect(self.getMdatFolderfc)
        self.drtBrowse.clicked.connect(self.getMdatFolderdrt)

        self.tdStart.clicked.connect(self.printButtonPressed) # Remember to pass the definition/method, not the return value!
        self.xrdStart.clicked.connect(self.xrdSt)
        self.fcStart.clicked.connect(self.fcSt)
        self.drtStart.clicked.connect(self.DRT)
        
        self.show()
    def DRT(self):
        #base=os.getcwd()
        #self.infoWindow.setText(open('Information/drt.html').read())
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
        #self.infoWindow.setText(open('Information/idle.html').read())
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
        td.fileReader(newZDir,decades,area)
        progressbarval += 12.5
        self.progressBar.setValue(progressbarval)
        td.createMultiX(newZDir,path)
        progressbarval += 12.5
        self.progressBar.setValue(progressbarval)
        td.generateSheets(newZDir,csvname)
        os.chdir(base)
        self.infoWindow.setText(open('Information/idle.html').read())

    
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
            dataDRT = {'Frequency' : intFreq, 'Z Prime Ohmic Corrected' : zPrimeARC, 'Z Double Prime Area Corrected' : zDoublePrimeARC}
            dt = pd.DataFrame(data=dataDRT)
            fileName = nameoffile + 'DRT-Preproccessing.csv'
            dt.to_csv(fileName,index=False,header=None)
            print(file, " has been parsed. continuing to next file...")
            
    
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

        

app = QtWidgets.QApplication(sys.argv)
window = Ui()
app.exec_()


    
    