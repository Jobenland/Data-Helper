from FileHandler import FileHandler
import os
import datetime
import pandas as pd
import itertools as itls
import glob
import time
import natsort
import copy
ENCODING = "ISO-8859-1"
LOOKUP_FILE_BASE = "File Base:"
LOOKUP_DATE = "Date:"
LOOKUP_TIME = "Time:"
LOOKUP_END_HEADER = "End Header:"
EURO_MACHINE_FILE_BASE = "EIS_OCV_600_aging"
NA_MACHINE_FILE_BASE = "EIS_OCV_IV_Aging_600"

IMP_600_OLD = "IMP_IV_600"
IMP_600_NEW = "OCV_IV_600"

IMPEDANCE_TAG = "IMPEDANCE"
STATIC_TAG = "STATIC"
DYNAMIC_TAG = "DYNAMIC"

class Impedance(FileHandler):
    def __init__(self, fileList):
        self.listFiles = copy.deepcopy(fileList)
        #for file in fileList:
        #    self.listFiles.append(file)
#
        self.electrodeASRList = []
        self.totalASRList = []
        self.ohmicList = []
        self.file_dict = fileList
        self.timeSeconds = []
        self.timeHours = []
        self.ZPrime = []
        self.Z2Prime = []
        self.Z2PrimeShort = []
        self.Z2PrimeABS = []

    def extractData(self, fl, directory):
        fileList = natsort.natsorted(fl)
        os.chdir(directory)
        intTime = []
        ohmicZ2Prime = 0
        ohmicZPrime = 0
        ohmicMin = 0
        headerFound = False
        totalASR = 0
        print('FILES: ', len(fileList))
        print(fileList)
        for files in fileList:
            if '.z' in files:
                
                with open(files, 'r', encoding=ENCODING) as f:
                    for row in f:
                        if LOOKUP_END_HEADER in row:
                            headerFound = True
                            continue
                        elif headerFound:
                            self.ZPrime.append(float(row.split('\t')[4]))
                            self.Z2Prime.append(float(row.split('\t')[5]))
                    self.Z2PrimeShort = self.Z2Prime[5:25]
                    self.Z2PrimeABS = [abs(i) for i in self.Z2PrimeShort]

                    ohmicZ2Prime = min(self.Z2PrimeABS)

                    if ohmicZ2Prime in self.Z2Prime:
                        ohmicZPrime = self.Z2Prime.index(ohmicZ2Prime)
                    else:
                        ohmicZPrime = self.Z2Prime.index(-ohmicZ2Prime)

                    ohmicMin = self.ZPrime[ohmicZPrime]
                    ASRMax = max(self.ZPrime[ohmicZPrime:])
                    eASR = ASRMax - ohmicMin
                    self.electrodeASRList.append(eASR)
                    self.totalASRList.append(ASRMax)
                    self.ohmicList.append(ohmicMin)
                    dateTimeTuple = self.getMetaData(files)
                    dateTime = datetime.datetime.strptime("{} {}".format(dateTimeTuple[0], dateTimeTuple[1]), '%m/%d/%Y %I:%M:%S %p')
                    self.timeSeconds.append(float(time.mktime(dateTime.timetuple())))
            headerFound = False
        minTime = min(self.timeSeconds)
        self.timeHours = [((self.timeSeconds[i]-minTime)/3600) for i in range(len(self.timeSeconds))]
        #print("Impedance data extraction complete")
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