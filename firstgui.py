# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'firstgui.ui'
#
# Created by: PyQt5 UI code generator 5.7.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1102, 806)
        MainWindow.setStyleSheet("\n"
"QGroupBox {\n"
"    border: 1px solid red;\n"
"    border-radius: 9px;\n"
"    margin-top: 0.5em;\n"
"}\n"
"\n"
"QGroupBox::title {\n"
"    subcontrol-origin: margin;\n"
"    size: 40px;\n"
"    left: 25px;\n"
"    padding: 0 3px 0 3px;\n"
"}\n"
"\n"
"QScrollArea {\n"
"    border: 1px solid red;\n"
"    border-radius: 1px;\n"
"    margin-top: 0.5em;\n"
"}\n"
"")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(10, 20, 581, 231))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setUnderline(False)
        font.setWeight(75)
        self.groupBox.setFont(font)
        self.groupBox.setObjectName("groupBox")
        self.tdStart = QtWidgets.QPushButton(self.groupBox)
        self.tdStart.setGeometry(QtCore.QRect(440, 180, 93, 28))
        self.tdStart.setStyleSheet("background-color: rgb(0, 170, 0);")
        self.tdStart.setObjectName("tdStart")
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setGeometry(QtCore.QRect(30, 50, 151, 16))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.tdFileText = QtWidgets.QLineEdit(self.groupBox)
        self.tdFileText.setGeometry(QtCore.QRect(30, 100, 531, 21))
        self.tdFileText.setObjectName("tdFileText")
        self.tdBrowse = QtWidgets.QPushButton(self.groupBox)
        self.tdBrowse.setGeometry(QtCore.QRect(440, 140, 93, 28))
        self.tdBrowse.setStyleSheet("background-color: rgb(0, 85, 255);")
        self.tdBrowse.setObjectName("tdBrowse")
        self.label_6 = QtWidgets.QLabel(self.groupBox)
        self.label_6.setGeometry(QtCore.QRect(160, 130, 131, 16))
        font = QtGui.QFont()
        font.setItalic(True)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.decadesTDCheck = QtWidgets.QCheckBox(self.groupBox)
        self.decadesTDCheck.setGeometry(QtCore.QRect(30, 150, 141, 20))
        self.decadesTDCheck.setObjectName("decadesTDCheck")
        self.tDArea = QtWidgets.QLineEdit(self.groupBox)
        self.tDArea.setGeometry(QtCore.QRect(80, 190, 71, 22))
        self.tDArea.setObjectName("tDArea")
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setGeometry(QtCore.QRect(30, 190, 41, 16))
        self.label.setObjectName("label")
        self.tdCombine = QtWidgets.QLineEdit(self.groupBox)
        self.tdCombine.setGeometry(QtCore.QRect(210, 160, 131, 22))
        self.tdCombine.setObjectName("tdCombine")
        self.label_5 = QtWidgets.QLabel(self.groupBox)
        self.label_5.setGeometry(QtCore.QRect(210, 190, 181, 16))
        self.label_5.setObjectName("label_5")
        self.progressBar = QtWidgets.QProgressBar(self.groupBox)
        self.progressBar.setGeometry(QtCore.QRect(190, 50, 371, 16))
        self.progressBar.setMaximum(100)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.groupBox_2 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_2.setGeometry(QtCore.QRect(10, 260, 581, 241))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.groupBox_2.setFont(font)
        self.groupBox_2.setObjectName("groupBox_2")
        self.xrdStart = QtWidgets.QPushButton(self.groupBox_2)
        self.xrdStart.setGeometry(QtCore.QRect(440, 190, 93, 28))
        self.xrdStart.setStyleSheet("background-color: rgb(0, 170, 0);")
        self.xrdStart.setObjectName("xrdStart")
        self.label_3 = QtWidgets.QLabel(self.groupBox_2)
        self.label_3.setGeometry(QtCore.QRect(30, 50, 151, 16))
        self.label_3.setObjectName("label_3")
        self.xrdFileText = QtWidgets.QLineEdit(self.groupBox_2)
        self.xrdFileText.setGeometry(QtCore.QRect(30, 100, 531, 22))
        self.xrdFileText.setObjectName("xrdFileText")
        self.xrdBrowse = QtWidgets.QPushButton(self.groupBox_2)
        self.xrdBrowse.setGeometry(QtCore.QRect(440, 150, 93, 28))
        self.xrdBrowse.setStyleSheet("background-color: rgb(0, 85, 255);")
        self.xrdBrowse.setObjectName("xrdBrowse")
        self.label_7 = QtWidgets.QLabel(self.groupBox_2)
        self.label_7.setGeometry(QtCore.QRect(160, 140, 131, 16))
        font = QtGui.QFont()
        font.setItalic(True)
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")
        self.xrdProgress = QtWidgets.QProgressBar(self.groupBox_2)
        self.xrdProgress.setGeometry(QtCore.QRect(190, 50, 371, 20))
        self.xrdProgress.setProperty("value", 0)
        self.xrdProgress.setObjectName("xrdProgress")
        self.textEdit = QtWidgets.QTextEdit(self.groupBox_2)
        self.textEdit.setGeometry(QtCore.QRect(240, 170, 191, 51))
        self.textEdit.setObjectName("textEdit")
        self.xrdCombined = QtWidgets.QLineEdit(self.groupBox_2)
        self.xrdCombined.setGeometry(QtCore.QRect(60, 170, 113, 22))
        self.xrdCombined.setObjectName("xrdCombined")
        self.label_9 = QtWidgets.QLabel(self.groupBox_2)
        self.label_9.setGeometry(QtCore.QRect(60, 200, 181, 16))
        self.label_9.setObjectName("label_9")
        self.groupBox_3 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_3.setGeometry(QtCore.QRect(10, 520, 581, 231))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.groupBox_3.setFont(font)
        self.groupBox_3.setObjectName("groupBox_3")
        self.fcStart = QtWidgets.QPushButton(self.groupBox_3)
        self.fcStart.setGeometry(QtCore.QRect(440, 180, 93, 28))
        self.fcStart.setStyleSheet("background-color: rgb(0, 170, 0);")
        self.fcStart.setObjectName("fcStart")
        self.label_4 = QtWidgets.QLabel(self.groupBox_3)
        self.label_4.setGeometry(QtCore.QRect(30, 40, 151, 16))
        self.label_4.setObjectName("label_4")
        self.xrdFileText_2 = QtWidgets.QLineEdit(self.groupBox_3)
        self.xrdFileText_2.setGeometry(QtCore.QRect(30, 90, 521, 22))
        self.xrdFileText_2.setObjectName("xrdFileText_2")
        self.fcBrowse = QtWidgets.QPushButton(self.groupBox_3)
        self.fcBrowse.setGeometry(QtCore.QRect(440, 140, 93, 28))
        self.fcBrowse.setStyleSheet("background-color: rgb(0, 85, 255);")
        self.fcBrowse.setObjectName("fcBrowse")
        self.label_8 = QtWidgets.QLabel(self.groupBox_3)
        self.label_8.setGeometry(QtCore.QRect(160, 130, 131, 16))
        font = QtGui.QFont()
        font.setItalic(True)
        self.label_8.setFont(font)
        self.label_8.setObjectName("label_8")
        self.fcProgress = QtWidgets.QProgressBar(self.groupBox_3)
        self.fcProgress.setGeometry(QtCore.QRect(190, 40, 371, 16))
        self.fcProgress.setProperty("value", 0)
        self.fcProgress.setObjectName("fcProgress")
        self.symmCellCheck = QtWidgets.QCheckBox(self.groupBox_3)
        self.symmCellCheck.setGeometry(QtCore.QRect(40, 160, 131, 20))
        self.symmCellCheck.setObjectName("symmCellCheck")
        self.fcArea = QtWidgets.QLineEdit(self.groupBox_3)
        self.fcArea.setGeometry(QtCore.QRect(100, 190, 91, 22))
        self.fcArea.setObjectName("fcArea")
        self.label_11 = QtWidgets.QLabel(self.groupBox_3)
        self.label_11.setGeometry(QtCore.QRect(40, 190, 55, 16))
        self.label_11.setObjectName("label_11")
        self.fcCombine = QtWidgets.QLineEdit(self.groupBox_3)
        self.fcCombine.setGeometry(QtCore.QRect(230, 160, 151, 22))
        self.fcCombine.setObjectName("fcCombine")
        self.label_12 = QtWidgets.QLabel(self.groupBox_3)
        self.label_12.setGeometry(QtCore.QRect(230, 190, 161, 16))
        self.label_12.setObjectName("label_12")
        self.groupBox_4 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_4.setGeometry(QtCore.QRect(610, 420, 451, 331))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.groupBox_4.setFont(font)
        self.groupBox_4.setObjectName("groupBox_4")
        self.label_10 = QtWidgets.QLabel(self.groupBox_4)
        self.label_10.setGeometry(QtCore.QRect(30, 300, 461, 16))
        font = QtGui.QFont()
        font.setPointSize(7)
        font.setItalic(True)
        self.label_10.setFont(font)
        self.label_10.setObjectName("label_10")
        self.textBrowser = QtWidgets.QTextBrowser(self.groupBox_4)
        self.textBrowser.setGeometry(QtCore.QRect(20, 30, 411, 251))
        self.textBrowser.setObjectName("textBrowser")
        self.groupBox_5 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_5.setGeometry(QtCore.QRect(610, 10, 451, 401))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.groupBox_5.setFont(font)
        self.groupBox_5.setObjectName("groupBox_5")
        self.textBrowser_2 = QtWidgets.QTextBrowser(self.groupBox_5)
        self.textBrowser_2.setGeometry(QtCore.QRect(20, 30, 411, 351))
        self.textBrowser_2.setObjectName("textBrowser_2")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1102, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.groupBox.setTitle(_translate("MainWindow", "Temperature Dependence for Symmetrical cells"))
        self.tdStart.setText(_translate("MainWindow", "Start"))
        self.label_2.setText(_translate("MainWindow", "Enter Folder of MDATS"))
        self.tdFileText.setPlaceholderText(_translate("MainWindow", "File Path Willl Update here. Click Browse to browse file system for folder"))
        self.tdBrowse.setText(_translate("MainWindow", "Browse"))
        self.label_6.setText(_translate("MainWindow", "Additional Options"))
        self.decadesTDCheck.setText(_translate("MainWindow", "Frequency Decades"))
        self.tDArea.setText(_translate("MainWindow", "0.155"))
        self.label.setText(_translate("MainWindow", "Area"))
        self.tdCombine.setText(_translate("MainWindow", "Combined-CSV"))
        self.label_5.setText(_translate("MainWindow", "Combined Excel File Name"))
        self.groupBox_2.setTitle(_translate("MainWindow", "XRD Converter"))
        self.xrdStart.setText(_translate("MainWindow", "Start"))
        self.label_3.setText(_translate("MainWindow", "Enter Folder of .out Files"))
        self.xrdFileText.setPlaceholderText(_translate("MainWindow", "File Path Willl Update here. Click Browse to browse file system for folder"))
        self.xrdBrowse.setText(_translate("MainWindow", "Browse"))
        self.label_7.setText(_translate("MainWindow", "Additional Options"))
        self.textEdit.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:7.8pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Note: This Program <span style=\" font-weight:600; text-decoration: underline;\">PERMANITLY</span> removes the headers form the files, Create backups if you want to preserve the header</p></body></html>"))
        self.xrdCombined.setText(_translate("MainWindow", "Combined-CSV"))
        self.label_9.setText(_translate("MainWindow", "Combined Excel File Name"))
        self.groupBox_3.setTitle(_translate("MainWindow", "Full Cell Data Extractor"))
        self.fcStart.setText(_translate("MainWindow", "Start"))
        self.label_4.setText(_translate("MainWindow", "Enter Folder of MDATS"))
        self.xrdFileText_2.setPlaceholderText(_translate("MainWindow", "File Path Willl Update here. Click Browse to browse file system for folder"))
        self.fcBrowse.setText(_translate("MainWindow", "Browse"))
        self.label_8.setText(_translate("MainWindow", "Additional Options"))
        self.symmCellCheck.setText(_translate("MainWindow", "Symmterical Cell"))
        self.fcArea.setText(_translate("MainWindow", "0.155"))
        self.label_11.setText(_translate("MainWindow", "Area"))
        self.fcCombine.setText(_translate("MainWindow", "Combined-CSV"))
        self.label_12.setText(_translate("MainWindow", "Combined Excel File Name"))
        self.groupBox_4.setTitle(_translate("MainWindow", "Readme.md and help"))
        self.label_10.setText(_translate("MainWindow", "MEII - energy.umd.edu       Written and maintained by Jonathan Obenland"))
        self.textBrowser.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:7.8pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        self.textBrowser.setPlaceholderText(_translate("MainWindow", "There has been an error getting help and about. ERROR: 100"))
        self.groupBox_5.setTitle(_translate("MainWindow", "Information and Assistance"))
        self.textBrowser_2.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:7.8pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:14pt;\">Maryland Energy Innovation Institute</span></p>\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:14pt; vertical-align:super;\"><br /></p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><a href=\"energy.umd.edu\"><span style=\" font-size:8pt; text-decoration: underline; color:#0000ff;\">MEII webpage</span></a></p>\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt; text-decoration: underline; color:#0000ff;\"><br /></p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><a href=\"github.com/jobenland\"><span style=\" font-size:8pt; text-decoration: underline; color:#0000ff;\">Github</span></a></p>\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt; text-decoration: underline; color:#0000ff;\"><br /></p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><a href=\"github.com/jobenland\"><span style=\" font-size:8pt; text-decoration: underline; color:#0000ff;\">Submit an Issue</span></a></p></body></html>"))

import Image_rc
