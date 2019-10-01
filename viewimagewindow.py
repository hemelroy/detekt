from PyQt5 import QtCore, QtGui, QtWidgets

class ImageWindow(object):
    
    def setupUi(self, OtherWindow):
        OtherWindow.setObjectName("OtherWindow")
        OtherWindow.resize(1000, 1000)
        self.centralwidget = QtWidgets.QWidget(OtherWindow)
        self.centralwidget.setObjectName("centralwidget")
       
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.defaultText = QtWidgets.QLabel(self.centralwidget)
        
        self.label.setGeometry(QtCore.QRect(1, 1, 999, 999))
        self.defaultText.setGeometry(QtCore.QRect(1, 1, 300, 300))
        font = QtGui.QFont()
        font.setPointSize(22)
        self.defaultText.setFont(font)
        self.defaultText.setObjectName("label2")
        self.defaultText.setText("No image selected")
        OtherWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(OtherWindow)
        self.statusbar.setObjectName("statusbar")
        OtherWindow.setStatusBar(self.statusbar)

        self.retranslateUi(OtherWindow)
        QtCore.QMetaObject.connectSlotsByName(OtherWindow)

    def retranslateUi(self, OtherWindow):
        _translate = QtCore.QCoreApplication.translate
        OtherWindow.setWindowTitle(_translate("OtherWindow", "MainWindow"))
        #self.label.setText(_translate("OtherWindow", "Welcome To This Window"))
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.defaultText.setAlignment(QtCore.Qt.AlignCenter)
        #self.label.setPixmap(QtGui.QPixmap("images/birb.jpeg"))

    def showImage(self, viewImgPath):
        self.label.setPixmap(QtGui.QPixmap(viewImgPath))
        if viewImgPath:
            self.defaultText.hide()
            

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    OtherWindow = QtWidgets.QMainWindow()
    ui = ImageWindow()
    ui.setupUi(OtherWindow)
    OtherWindow.show()
    sys.exit(app.exec_())