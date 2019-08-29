from FileHandler import FileHandler
import os
import datetime
import pandas as pd
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



