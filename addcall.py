#!/usr/bin/python
import os
import sqlite3
from configparser import ConfigParser
import re
from time import strftime

from PyQt5.QtCore import QDateTime, Qt
from PyQt5.QtWidgets import QMessageBox
from PyQt5 import QtCore, QtGui, QtWidgets
import random
import datetime
import js8callAPIsupport
from datetime import datetime


serverip = ""
serverport = ""
callsign = ""
grid = ""
selectedgroup = ""




class Ui_FormAddCall(object):
    def setupUi(self, FormAddCall):
        self.MainWindow = FormAddCall
        FormAddCall.setObjectName("FormAddCall")
        FormAddCall.resize(735, 260)
        font = QtGui.QFont()
        font.setPointSize(10)
        FormAddCall.setFont(font)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("USA-32.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        FormAddCall.setWindowIcon(icon)
        self.lineEdit_2 = QtWidgets.QLineEdit(FormAddCall)
        self.lineEdit_2.setGeometry(QtCore.QRect(185, 100, 60, 22))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lineEdit_2.setFont(font)
        self.lineEdit_2.setMaxLength(6)
        self.lineEdit_2.setObjectName("lineEdit_2")
                
        self.lineEdit_3 = QtWidgets.QLineEdit(FormAddCall)
        self.lineEdit_3.setGeometry(QtCore.QRect(185, 135, 60, 22))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lineEdit_3.setFont(font)
        self.lineEdit_3.setMaxLength(6)
        self.lineEdit_3.setObjectName("lineEdit_3")
        
        self.lineEdit_4 = QtWidgets.QLineEdit(FormAddCall)
        self.lineEdit_4.setGeometry(QtCore.QRect(185, 170, 60, 22))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lineEdit_4.setFont(font)
        self.lineEdit_4.setMaxLength(7)
        self.lineEdit_4.setObjectName("lineEdit_4")
        
        self.label = QtWidgets.QLabel(FormAddCall)
        self.label.setGeometry(QtCore.QRect(75, 15, 626, 81))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(FormAddCall)
        self.label_2.setGeometry(QtCore.QRect(90, 100, 95, 25))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        
        self.label_3 = QtWidgets.QLabel(FormAddCall)
        self.label_3.setGeometry(QtCore.QRect(90, 135, 95, 25))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        
        self.label_4 = QtWidgets.QLabel(FormAddCall)
        self.label_4.setGeometry(QtCore.QRect(90, 170, 95, 25))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        
        self.label_5 = QtWidgets.QLabel(FormAddCall)
        self.label_5.setGeometry(QtCore.QRect(260, 135, 95, 25))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        
        self.label_6 = QtWidgets.QLabel(FormAddCall)
        self.label_6.setGeometry(QtCore.QRect(260, 170, 95, 25))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        
        
        
        self.pushButton = QtWidgets.QPushButton(FormAddCall)
        self.pushButton.setGeometry(QtCore.QRect(541, 176, 75, 24))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(FormAddCall)
        self.pushButton_2.setGeometry(QtCore.QRect(641, 176, 75, 24))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setObjectName("pushButton_2")

        self.retranslateUi(FormAddCall)
        QtCore.QMetaObject.connectSlotsByName(FormAddCall)

        self.getConfig()
        self.serveripad = serverip
        self.servport = int(serverport)
        self.api = js8callAPIsupport.js8CallUDPAPICalls((self.serveripad),
                                                        int(self.servport))
        self.pushButton_2.clicked.connect(self.MainWindow.close)
        self.pushButton.clicked.connect(self.transmit)

        self.MainWindow.setWindowFlags(
            QtCore.Qt.Window |
            QtCore.Qt.CustomizeWindowHint |
            QtCore.Qt.WindowTitleHint |
            QtCore.Qt.WindowCloseButtonHint |
            QtCore.Qt.WindowStaysOnTopHint
        )




    def retranslateUi(self, FormAddCall):
        global callsign
        _translate = QtCore.QCoreApplication.translate
        FormAddCall.setWindowTitle(_translate("FormAddCall", "CommStatX Add a new Callsign "))
        self.lineEdit_2.setText(_translate("FormAddCall", callsign))
        self.lineEdit_3.setText(_translate("FormAddCall", ""))
        self.lineEdit_4.setText(_translate("FormAddCall", ""))
        
        self.label.setText(_translate("FormAddCall", "<html><head/><body><p>This form will create a string that Commstatx stations will recognize and add your <br>callsign to the CallArchive file so you can be listed in the members window.</p></body></html>"))
        self.label_2.setText(_translate("FormAddCall", "Callsign to Add : "))
        self.label_3.setText(_translate("FormAddCall", "Your Latitude : "))
        self.label_4.setText(_translate("FormAddCall", "Your Longitude : "))
        self.label_5.setText(_translate("FormAddCall", "(Example 43.31 )"))
        self.label_6.setText(_translate("FormAddCall", "(Example -83.47)" ))
        
        
        self.pushButton.setText(_translate("FormAddCall", "Transmit"))
        self.pushButton_2.setText(_translate("FormAddCall", "Cancel"))


    def getConfig(self):
        global serverip
        global serverport
        global grid
        global callsign
        global selectedgroup
        if os.path.exists("config.ini"):
            config_object = ConfigParser()
            config_object.read("config.ini")
            userinfo = config_object["USERINFO"]
            systeminfo = config_object["DIRECTEDCONFIG"]
            callsign = format(userinfo["callsign"])
            callsignSuffix = format(userinfo["callsignsuffix"])
            group1 = format(userinfo["group1"])
            group2 = format(userinfo["group2"])
            grid = format(userinfo["grid"])
            path = format(systeminfo["path"])
            serverip = format(systeminfo["server"])
            serverport = format(systeminfo["port"])
            selectedgroup = format(userinfo["selectedgroup"])
        
        self.lineEdit_2.setText(callsign)





    def transmit(self):
        global selectedgroup
        global callsign

        calltoadd = format(self.lineEdit_2.text())
        calltoadd = calltoadd.replace(" ", "")
        calllat = format(self.lineEdit_3.text())
        calllong = format(self.lineEdit_4.text())
        newcall = re.sub("[^A-Za-z0-9*\-\s]+", " ", calltoadd)
        print(newcall+"test")
        if re.match('[AKNW][A-Z]{0,2}[0-9][A-Z]{1,3}',calltoadd):
            print ("callsign is a valid structure")
        else:
            print("New Callsign Latitude is not correct format")
            self.lineEdit_2.setText("")
            msg = QMessageBox()
            msg.setWindowTitle("CommStatX error")
            msg.setText( "Callsign format is not correct")
            msg.setIcon(QMessageBox.Critical)
            msg.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)
            x = msg.exec_()  # this will show our messagebox
            return
        #print(calllat)
        #calllat1 = re.sub("[0-9]?[0-9]?(\.[0-9][0-9]",calllat)
        #print(calllat1)
        if re.match('^[0-9]?[0-9]?\.[0-9]?[0-9]*$', calllat):
            print ("Latitude contains correct number structure")
        else:
            print("New Callsign Latitude is not correct format")
            self.lineEdit_3.setText("")
            msg = QMessageBox()
            msg.setWindowTitle("CommStatX error")
            msg.setText( "Latitude format is not correct")
            msg.setIcon(QMessageBox.Critical)
            msg.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)
            x = msg.exec_()  # this will show our messagebox
            return
        
        
        if re.match('^\-[0-9]?[0-9]?[0-9]?\.[0-9]?[0-9]*$', calllong):
            print ("Longitude contains correct number structure")
        else:
            print("New Callsign Longitude is not correct format")
            self.lineEdit_4.setText("")
            msg = QMessageBox()
            msg.setWindowTitle("CommStatX error")
            msg.setText( "Longitude format is not correct")
            msg.setIcon(QMessageBox.Critical)
            msg.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)
            x = msg.exec_()  # this will show our messagebox
            return
        
        
        


        if len(calltoadd) < 4 :
            msg = QMessageBox()
            msg.setWindowTitle("CommStatX error")
            msg.setText( "Callsign text too short")
            msg.setIcon(QMessageBox.Critical)
            msg.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)
            x = msg.exec_()  # this will show our messagebox
        if len(calllat) < 5 :
            msg = QMessageBox()
            msg.setWindowTitle("CommStatX error")
            msg.setText( "Latitude text too short or wrong format")
            msg.setIcon(QMessageBox.Critical)
            msg.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)
            x = msg.exec_()  # this will show our messagebox
        
        if len(calllong) < 5 :
            msg = QMessageBox()
            msg.setWindowTitle("CommStatX error")
            msg.setText( "Longitude text too short or wrong format")
            msg.setIcon(QMessageBox.Critical)
            msg.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)
            x = msg.exec_()  # this will show our messagebox
            return
        
        group = "@"+selectedgroup

        message = ""+group + "," + calltoadd + ","+calllat+","+calllong+",{C%}"
        messageType = js8callAPIsupport.TYPE_TX_SEND
        messageString = message

        #res = QMessageBox.question(FormAddCall, "Question", "Are you sure?", QMessageBox.Yes | QMessageBox.No)
        msg = QMessageBox()
        msg.setWindowTitle("CommStatX TX")
        msg.setText("CommStatX will transmit : " + message)
        msg.setIcon(QMessageBox.Information)
        msg.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)
        x = msg.exec_()
        
        now = datetime.now()
        datetimenow = now.strftime("%Y-%m-%d %H:%M:%S")
        test = str(datetimenow)
        print(calltoadd,calllat,calllong,test)
        call = calltoadd
        lat = calllat
        long = calllong
        timerec = datetimenow
        self.sendMessage(messageType, messageString)
        self.addcalldb(call,lat,long,timerec)
        

        self.closeapp()

    
    def addcalldb(self,call, lat, long, timerec):
        conn = sqlite3.connect("callarchive.db3")
        cur = conn.cursor()
        addcall = call
        print(call,lat,long,timerec)
        lastheard = timerec
        addlat = float(lat)
        addlong = float(long)
        #gridLat = 0.0;
        #gridLong = 0.0;

        rowsQuery = "SELECT Count() FROM Call_Data Where Call  = '" + call + "'"
        cur.execute(rowsQuery)
        numberOfRows = cur.fetchone()[0]
        if numberOfRows == 1:
            callgridlat = "SELECT gridlat FROM Call_Data Where Call  = '" + call + "'"
            cur.execute(callgridlat)
            gridLatint = cur.fetchone()[0]
            gridLat = float(gridLatint)

            callgridlong = "SELECT gridlong FROM Call_Data Where Call  = '" + call + "'"
            cur.execute(callgridlong)
            gridLongint = cur.fetchone()[0]
            gridLong = float(gridLongint)
            print("Callsign :"+call+ "  is already in Database, nothing to do")
            cur.close()
            return

            #print(lastheard, call, memgrp1, memgrp2, gridLat, gridLong)
            #conn2 = sqlite3.connect("traffic.db3")
            #cur2 = conn2.cursor()
            #cur2.execute("INSERT OR REPLACE INTO members_Data (date, callsign, groupname1, groupname2, gridlat, gridlong) VALUES(?, ?, ?, ?, ?, ?)",(lastheard, call, memgrp1,memgrp2, gridLat, gridLong))
            #conn2.commit()
            #cur2.close()

        else:
            cur.execute("INSERT OR REPLACE INTO Call_Data (Call, gridlat, gridlong, utc) VALUES(?, ?, ?, ?)",(addcall, addlat, addlong, lastheard))
            conn.commit()
            cur.close()
            print("Inserted callsign :"+call+" into CallArchive.db3") 
            
            return
    
    
    
    
    
    def closeapp(self):
        self.MainWindow.close()

    def sendMessage(self, messageType, messageText):
        self.api.sendMessage(messageType, messageText)
        #self.api.sendInfoToJS8Call(messageType,messageText) 


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    FormAddCall = QtWidgets.QWidget()
    ui = Ui_FormAddCall()
    ui.setupUi(FormAddCall)
    FormAddCall.show()
    sys.exit(app.exec_())
