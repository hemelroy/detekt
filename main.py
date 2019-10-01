# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QThread
from datetime import datetime
import dboperations
import cv2
import numpy
import time
from viewimagewindow import ImageWindow
import threading
from functools import partial
import pandas as pd


class Ui_MainWindow(object):
    
    def openViewFullImageWindow(self, normalImage):
        self.window = QtWidgets.QMainWindow()
        self.ui = ImageWindow()
        self.ui.setupUi(self.window)
        if normalImage:
            self.ui.showImage(viewImgPath)
        else:
            self.ui.showImage(viewDetectImgPath)
        self.window.show()
        
        
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1120, 739)
        MainWindow.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        MainWindow.setStyleSheet("QMainWindow {background: url('ringback3.png') green no-repeat;}");
        #MainWindow.setStyleSheet("QMainWindow {background-color: green;}");
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("camera.PNG"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setAutoFillBackground(False)
        self.centralwidget.setObjectName("centralwidget")
        
    #dateLabel
        self.dateLabel = QtWidgets.QLabel(self.centralwidget)
        self.dateLabel.setGeometry(QtCore.QRect(370, 220, 55, 16))
        font = QtGui.QFont()
        font.setFamily("Georgia")
        font.setPointSize(10)
        self.dateLabel.setFont(font)
        self.dateLabel.setStyleSheet("color: white;")
        self.dateLabel.setObjectName("dateLabel")
        
    #objectDetectedLabel
        self.objectDetectedLabel = QtWidgets.QLabel(self.centralwidget)
        self.objectDetectedLabel.setGeometry(QtCore.QRect(370, 130, 161, 31))
        font = QtGui.QFont()
        font.setFamily("Georgia")
        font.setPointSize(10)
        self.objectDetectedLabel.setFont(font)
        self.objectDetectedLabel.setStyleSheet("color: white;")
        self.objectDetectedLabel.setObjectName("objectDetectedLabel")
    
    #Title Label
        self.titleLabel = QtWidgets.QLabel(self.centralwidget)
        self.titleLabel.setGeometry(QtCore.QRect(220, 20, 571, 61))
        self.titleLabel.setStyleSheet("color: white;")
        #add a text-shadow: -5px -5px 0 #05386B, 5px -5px 0 #05386B, -5px 1px 0 #05386B, 5px 5px 0 #05386B;
        font = QtGui.QFont()
        font.setFamily("Cambria")
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.titleLabel.setFont(font)
        self.titleLabel.setObjectName("titleLabel")
        
        
    #List Widget
        self.listWidget = QtWidgets.QListWidget(self.centralwidget)
        self.listWidget.setGeometry(QtCore.QRect(40, 140, 281, 431))
        self.listWidget.setObjectName("listWidget")
        self.listWidget.setStyleSheet("background-color: #5CDB95;")
        self.listWidget.itemActivated.connect(previewDetails)
        
    #Calendar Widget
        self.calendarWidget = QtWidgets.QCalendarWidget(self.centralwidget)
        self.calendarWidget.setGeometry(QtCore.QRect(370, 250, 392, 236))
        self.calendarWidget.setObjectName("calendarWidget")
        self.calendarWidget.setStyleSheet("background-color: #EDF5E1; color: #379683;")
        #self.calendarWidget.setStyleSheet("background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop: 0 #05386B, stop: 1 #333333);}")
        self.calendarWidget.clicked[QtCore.QDate].connect(self.showDate) #date click event
        
    #Time Label
        self.timeLabel = QtWidgets.QLabel(self.centralwidget)
        self.timeLabel.setGeometry(QtCore.QRect(370, 180, 61, 16))
        font = QtGui.QFont()
        font.setFamily("Georgia")
        font.setPointSize(10)
        self.timeLabel.setFont(font)
        self.timeLabel.setObjectName("timeLabel")
        self.timeLabel.setStyleSheet("color: white;")
        font.setBold(True)
        
    #viewImageBtn
        self.viewImageBtn = QtWidgets.QPushButton(self.centralwidget)
        self.viewImageBtn.setGeometry(QtCore.QRect(370, 500, 121, 28))
        self.viewImageBtn.setStyleSheet("color: #EDF5E1; background-color: #05386B; border-style: outset; border-width: 2px; border-radius: 10px; border-color: #EDF5E1; font: bold 14px; min-width: 10em; padding: 6px;")
        font = QtGui.QFont()
        font.setFamily("Georgia")
        font.setPointSize(10)
        self.viewImageBtn.setFont(font)
        self.viewImageBtn.setObjectName("viewImageBtn")
        self.viewImageBtn.clicked.connect(partial(self.openViewFullImageWindow, True))
        
    #objectField
        self.objectField = QtWidgets.QLabel(self.centralwidget)
        self.objectField.setGeometry(QtCore.QRect(540, 130, 221, 31))
        font = QtGui.QFont()
        font.setFamily("Georgia")
        font.setPointSize(10)
        self.objectField.setFont(font)
        self.objectField.setFrameShape(QtWidgets.QFrame.Box)
        self.objectField.setText("")
        self.objectField.setStyleSheet("color: white;")
        self.objectField.setObjectName("objectField")
        
    #timeField
        self.timeField = QtWidgets.QLabel(self.centralwidget)
        self.timeField.setGeometry(QtCore.QRect(540, 170, 221, 31))
        font = QtGui.QFont()
        font.setFamily("Georgia")
        font.setPointSize(10)
        self.timeField.setFont(font)
        self.timeField.setFrameShape(QtWidgets.QFrame.Box)
        self.timeField.setText("")
        self.timeField.setStyleSheet("color: white;")
        self.timeField.setObjectName("timeField")
        
    #startDetectBtn
        self.startDetectBtn = QtWidgets.QPushButton(self.centralwidget)
        self.startDetectBtn.setGeometry(QtCore.QRect(920, 120, 131, 28))
        font = QtGui.QFont()
        font.setFamily("Georgia")
        font.setPointSize(10)
        self.startDetectBtn.setFont(font)
        self.startDetectBtn.setObjectName("startDetectBtn")
        self.startDetectBtn.setStyleSheet("color: #EDF5E1; background-color: #05386B; border-style: outset; border-width: 2px; border-radius: 10px; border-color: #EDF5E1; font: bold 14px; min-width: 10em; padding: 6px;")
        # for video timer implementation: self.startDetectBtn.clicked.connect(self.controlTimer)
        self.startDetectBtn.clicked.connect(openCamWindow)
        
    #openPlotBtn    
        self.openPlotBtn = QtWidgets.QPushButton(self.centralwidget)
        self.openPlotBtn.setGeometry(QtCore.QRect(920, 200, 93, 28))
        font = QtGui.QFont()
        font.setFamily("Georgia")
        font.setPointSize(10)
        self.openPlotBtn.setFont(font)
        self.openPlotBtn.setObjectName("openPlotBtn")
        self.openPlotBtn.setStyleSheet("color: #EDF5E1; background-color: #05386B; border-style: outset; border-width: 2px; border-radius: 10px; border-color: #EDF5E1; font: bold 14px; min-width: 10em; padding: 6px;")
        self.openPlotBtn.clicked.connect(openPlot)
        
    #deleteBtn
        self.deleteBtn = QtWidgets.QPushButton(self.centralwidget)
        self.deleteBtn.setGeometry(QtCore.QRect(920, 240, 93, 28))
        font = QtGui.QFont()
        font.setFamily("Georgia")
        font.setPointSize(10)
        self.deleteBtn.setFont(font)
        self.deleteBtn.setObjectName("deleteBtn")
        self.deleteBtn.setStyleSheet("color: #EDF5E1; background-color: #05386B; border-style: outset; border-width: 2px; border-radius: 10px; border-color: #EDF5E1; font: bold 14px; min-width: 10em; padding: 6px;")
        
    #viewDetectBtn
        self.viewDetectBtn = QtWidgets.QPushButton(self.centralwidget)
        self.viewDetectBtn.setGeometry(QtCore.QRect(580, 500, 171, 28))
        font = QtGui.QFont()
        font.setFamily("Georgia")
        font.setPointSize(10)
        self.viewDetectBtn.setFont(font)
        self.viewDetectBtn.setObjectName("viewDetectBtn")
        self.viewDetectBtn.setStyleSheet("color: #EDF5E1; background-color: #05386B; border-style: outset; border-width: 2px; border-radius: 10px; border-color: #EDF5E1; font: bold 14px; min-width: 10em; padding: 6px;")
        self.viewDetectBtn.clicked.connect(partial(self.openViewFullImageWindow,False))
        
        
    #stopDetectBtn
        self.stopDetectBtn = QtWidgets.QPushButton(self.centralwidget)
        self.stopDetectBtn.setGeometry(QtCore.QRect(920, 160, 131, 28))
        font = QtGui.QFont()
        font.setFamily("Georgia")
        font.setPointSize(10)
        self.stopDetectBtn.setFont(font)
        self.stopDetectBtn.setObjectName("stopDetectBtn")
        self.stopDetectBtn.setStyleSheet("color: #EDF5E1; background-color: #05386B; border-style: outset; border-width: 2px; border-radius: 10px; border-color: #EDF5E1; font: bold 14px; min-width: 10em; padding: 6px;")
        #self.stopDetectBtn.clicked.connect(testthread)
        
    #previewLabel
        self.previewLabel = QtWidgets.QLabel(self.centralwidget)
        self.previewLabel.setGeometry(QtCore.QRect(800, 280, 71, 16))
        font = QtGui.QFont()
        font.setFamily("Georgia")
        font.setPointSize(10)
        self.previewLabel.setFont(font)
        self.previewLabel.setStyleSheet("color: white;")
        self.previewLabel.setObjectName("previewLabel")


    #imagePreview
        self.imagePreview = QtWidgets.QLabel(self.centralwidget)
        self.imagePreview.setGeometry(QtCore.QRect(800, 320, 301, 261))
        self.imagePreview.setFrameShape(QtWidgets.QFrame.Box)
        self.imagePreview.setText("")
        self.imagePreview.setObjectName("imagePreview")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1120, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        
        
        

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Detekt"))
        self.dateLabel.setText(_translate("MainWindow", "Date:"))
        self.objectDetectedLabel.setText(_translate("MainWindow", "Object(s) Detected:"))
        self.titleLabel.setText(_translate("MainWindow", "Detekt - Motion Detector Application"))
        self.timeLabel.setText(_translate("MainWindow", "Time:"))
        self.viewImageBtn.setText(_translate("MainWindow", "View Full Image"))
        self.startDetectBtn.setText(_translate("MainWindow", "Start Detector"))
        self.openPlotBtn.setText(_translate("MainWindow", "Open Plot"))
        self.deleteBtn.setText(_translate("MainWindow", "Delete"))
        self.viewDetectBtn.setText(_translate("MainWindow", "View Detector Image"))
        self.stopDetectBtn.setText(_translate("MainWindow", "Stop Detector"))
        self.previewLabel.setText(_translate("MainWindow", "Preview:"))
      
            
    def showDate(self, date):
        date = date.toString()[4:]
        #print(date)
        datelist = date.split(' ')
        
        if datelist[0] == 'Jan':
            datelist[0] = '01'
        elif datelist[0] == 'Feb':
            datelist[0] = '02'
        elif datelist[0] == 'Mar':
            datelist[0] = '03'
        elif datelist[0] == 'Apr':
            datelist[0] = '04'
        elif datelist[0] == 'May':
            datelist[0] = '05'
        elif datelist[0] == 'Jun':
            datelist[0] = '06'
        elif datelist[0] == 'Jul':
            datelist[0] = '07'
        elif datelist[0] == 'Aug':
            datelist[0] = '08'
        elif datelist[0] == 'Sep':
            datelist[0] = '09'
        elif datelist[0] == 'Oct':
            datelist[0] = '10'
        elif datelist[0] == 'Nov':
            datelist[0] = '11'
        else:
            datelist[0] = '12'
            
        date = datelist[2] + '-' + datelist[0] + '-' + datelist[1]
        print(date)
        addToList(date)
        
def addToList(date):
    rows = dboperations.viewList(date)
    ui.listWidget.clear()
    for row in rows:
        #element = row[0]+"-"+row[1]
        ui.listWidget.addItem(str(row[0])+"-"+row[1])
    print(rows)
#    for i in range(10):
#        ui.listWidget.addItem('Item %s' % (i + 1))
        
def showToday():
    ui.listWidget.clear()
    dt = datetime.now()
    #today = f'{dt.year}-{dt.month}-{dt.day}'
    today = dt.strftime('%Y-%m-%d')
    print(today)
    addToList(today)
    
def previewDetails(item):
    lstString = item.text()
    lstString = lstString.split('-')
    imgPath = dboperations.viewPreview(int(lstString[0]),str(lstString[1]))
    global viewImgPath 
    global viewDetectImgPath
    
    #Update image details
    viewImgPath = str(imgPath[0][0])
    viewDetectImgPath = str(imgPath[0][1])
    ui.imagePreview.setAlignment(QtCore.Qt.AlignCenter)
    ui.imagePreview.setPixmap(QtGui.QPixmap(imgPath[0][0]).scaledToWidth(300))
    #ui.imagePreview.setPixmap(QtGui.QPixmap("images/sample.jpeg"))
    ui.timeField.setText(str(imgPath[0][2]))
    
    #Update object field details
    objectInfo = ''
    details = dboperations.getObjectDetails(int(lstString[0]))
    for objectName, quantity in details:
        objectInfo+=str(objectName)+' (x'+str(quantity)+'), '
        
    ui.objectField.setText(objectInfo)
        
    
def openCamWindow():
    import custom_image_detect

    video_capture.release()
    cv2.destroyAllWindows()

def openPlot(): 
    csvfile = dboperations.get_csv(viewImgPath)
    times_df = pd.read_csv(csvfile)
    print(times_df.head())

    from bokeh.plotting import figure, show, output_file
    from bokeh.models import HoverTool, ColumnDataSource

    #Format datetime in dataframe
    times_df['Start'] = pd.to_datetime(times_df['Start'])
    times_df['End'] = pd.to_datetime(times_df['End'])
    times_df["Start_str"] = times_df["Start"].dt.strftime("%Y-%m-%d %H-%M-%S")
    times_df["End_str"] = times_df["End"].dt.strftime("%Y-%m-%d %H-%M-%S")

    col_dt_src = ColumnDataSource(times_df)

    #plot graph
    plot = figure(x_axis_type = 'datetime', height = 100, width = 500, sizing_mode= "scale_both", title = "Object Detection History")
    plot.yaxis.minor_tick_line_color = None
    plot.ygrid[0].ticker.desired_num_ticks = 1
    plot.title.text_font_size = "30pt"

    hover = HoverTool(tooltips = [("Object Entrance Time", "@Start_str"), ("Object Exit Time", "@End_str")])
    plot.add_tools(hover)

    q = plot.quad(left = "Start", right = "End", bottom = 0, top = 1, color = "blue", source = col_dt_src)

    output_file("MotionGraph.html")
    show(plot)
    
    
if __name__ == "__main__":
    import sys
    viewImgPath = ''
    viewDetectImgPath = ''
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    showToday()
    MainWindow.show()
    sys.exit(app.exec_())