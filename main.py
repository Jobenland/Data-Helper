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




class Ui(QtWidgets.QMainWindow):
    
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('firstgui.ui', self)
        path =''
        text = open('README.MD').read()
        self.textBrowser.setPlainText(text)
        self.temp = tempConverter(path)
        
        printer = self.findChild(QtWidgets.QScrollArea,'outPutArea')
        self.tdBrowse.clicked.connect(self.getMdatFoldertd)
        self.xrdBrowse.clicked.connect(self.getMdatFolderxrd)
        self.fcBrowse.clicked.connect(self.getMdatFolderfc)
        
        self.tdStart.clicked.connect(self.printButtonPressed) # Remember to pass the definition/method, not the return value!
        self.xrdStart.clicked.connect(self.xrdSt)
        self.show()

    def xrdSt(self):

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



    def printButtonPressed(self):
        self.consoleTextBrowser.setPlainText('Button Pressed')
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


    
    