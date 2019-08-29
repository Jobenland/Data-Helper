from FileHandler import FileHandler
import os
import datetime
import pandas as pd
import csv
import itertools as itls
import glob
import time
import copy
import natsort
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

