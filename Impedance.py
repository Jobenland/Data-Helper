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
                        ohmicZ2Prime = min([abs(i) for i in Z2Prime[startrange:endrange]])
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
