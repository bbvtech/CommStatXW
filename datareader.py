import os.path
from configparser import ConfigParser
from PyQt5.QtWidgets import QMessageBox
from PyQt5 import QtCore
import shutil
import numpy as np
import re
import sqlite3
from datetime import datetime, timedelta
import time
import psutil




def getConfig():
    if os.path.exists("config.ini"):
        global callsign
        global callsignSuffix
        global group1
        global group2
        global grid
        global path
        config_object = ConfigParser()
        config_object.read("config.ini")
        userinfo = config_object["USERINFO"]
        # print("callsign is {}".format(userinfo["callsign"]))
        #print("callsignsuffix is {}".format(userinfo["callsignsuffix"]))
        #print("group1 is {}".format(userinfo["group1"]))
        #print("group2 is {}".format(userinfo["group2"]))
        #print("grid is {}".format(userinfo["grid"]))
        systeminfo = config_object["DIRECTEDCONFIG"]
        #print("file path  is {}".format(systeminfo["path"]))
        callsign = format(userinfo["callsign"])
        callsignSuffix = format(userinfo["callsignsuffix"])
        group1 = format(userinfo["group1"])
        group2 = format(userinfo["group2"])
        if len(group2) < 4:
            group2 = group1
        grid = format(userinfo["grid"])
        path = format(systeminfo["path"])

    else:
        msg = QMessageBox()
        msg.setWindowTitle("CommStatX error")
        msg.setText("Config file is missing!")
        msg.setIcon(QMessageBox.Critical)
        x = msg.exec_()  # this will show our messagebox
        return


getConfig()



def copyDirected():
    filepath = path+"\DIRECTED.TXT"
    shutil.copy2(filepath, 'copyDIRECTED.TXT')  # complete target filename given
    #shutil.copy2('/src/file.ext', '/dst/dir')  # target filename is /dst/dir/file.ext
#copyDirected()


def getmember(call, memgrp1, memgrp2, timerec):

    conn = sqlite3.connect("callarchive.db3")
    cur = conn.cursor()
    lastheard = timerec
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
        cur.close()

        #print(lastheard, call, memgrp1, memgrp2, gridLat, gridLong)
        conn2 = sqlite3.connect("traffic.db3")
        cur2 = conn2.cursor()
        cur2.execute("INSERT OR REPLACE INTO members_Data (date, callsign, groupname1, groupname2, gridlat, gridlong) VALUES(?, ?, ?, ?, ?, ?)",(lastheard, call, memgrp1,memgrp2, gridLat, gridLong))
        conn2.commit()
        cur2.close()
        print("member added"+ callsign)

    else:
        return
def getheard(call, timerec):

    conn = sqlite3.connect("callarchive.db3")
    cur = conn.cursor()
    lastheard = timerec
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
        cur.close()

        #print(lastheard, call, gridLat, gridLong)
        conn2 = sqlite3.connect("traffic.db3")
        cur2 = conn2.cursor()
        cur2.execute("INSERT OR REPLACE INTO heard_Data (date, callsign, gridlat, gridlong) VALUES(?, ?, ?, ?)",(lastheard, call, gridLat, gridLong))
        conn2.commit()
        cur2.close()

    else:
        return




def parseDirected():
    membergrp1 = ""
    membergrp2 = ""

    conn = sqlite3.connect("traffic.db3")
    cur = conn.cursor()
    datafile = open("copyDIRECTED.TXT", "r")
    lines = datafile.readlines()
    last_lines = lines[-50:]
    for num, str in enumerate(last_lines, 1):
        try:
            if group1 in str:
                currentgrp = group1
                print("group1 is in string : "+currentgrp)
                membergrp1 = group1

            if group2 in str:
                currentgrp = group2
                membergrp2 = group2
                print("group2 is in string : " + currentgrp)


            if  group1 or group2 in currentgrp:

                if "{^%}" in str: #THIS IS BULLETINS
                    #arr = line.split('\t')
                     #str.replace('\t', ', ')
                    arr = str.split('\t')
                    utc = arr[0]
                    callsignmix = arr[4]
                    arr2 = callsignmix.split(',')
                    count = len(arr) + len(arr2)
                    if count != 9:
                        continue
                    id = arr2[1]
                    callsignlong = arr2[0]
                    arr3 = callsignlong.split(':')
                    callsignlg = arr3[0]
                    arr4 = callsignlg.split('/')
                    callsign = arr4[0]
                    bulletin = arr2[2]
                    #print(currentgrp)
                    #print(arr)

                    cur.execute("INSERT OR REPLACE INTO bulletins_Data (datetime, idnum, groupid, callsign, message) VALUES(?, ?, ?, ?, ? )", (utc, id, currentgrp, callsign, bulletin))
                    conn.commit()
                    getmember(callsign, membergrp1,membergrp2, utc)
                    print ("Added Bulletin from :"+callsign+" ID :"+id+" Added callsign to members")
                    continue



                if "{&%}" in str: #THIS IS STATREP
                    mylist = ['1','2','3','4']
                    arr = str.split('\t')
                    utc = arr[0]
                    callsignmix = arr[4]
                    arr2 = callsignmix.split(',')
                    count = len(arr) + len(arr2)
                    #print (count)
                    if count != 12:
                        print("message failed field count")
                        continue
                    id = arr2[1]
                    callsignlong = arr2[0]
                    arr3 = callsignlong.split(':')
                    callsignlg = arr3[0]
                    arr4 = callsignlg.split('/')
                    callsign = arr4[0]
                    curgrid = arr2[1]
                    prec1 = arr2[2]
                    if prec1 == "1":
                        prec = "Routine"

                    if prec1 == "2":
                        prec = "Priority"

                    if prec1 == "3":
                        prec = "Immediate"

                    if prec1 == "4":
                        prec = "Flash"
                    #for item in mylist:
                    #    if item in prec1:
                    #        print("StatRep failed for null precedence field :"+str)
                    #        continue
                     #   else:
                      #      print("here is the else statement")
                      
                    if prec1 not in ["1","2","3","4"] :
                        print("StatRep failed for null precedence field : \n"+str)
                        continue
                    
                    srid = arr2[3]
                    
                    srcode = arr2[4]
                    arr5 = list(srcode)
                    status = arr5[0]
                    if status not in ["1","2","3"] :
                        print("StatRep failed for null status field : \n"+str)
                        continue
                    commpwr = arr5[1]
                    if commpwr not in ["1","2","3"]:
                        print("StatRep failed for null commpwr field : \n"+str)
                        continue
                    pubwtr = arr5[2]
                    if pubwtr not in ["1","2","3"]:
                        print("StatRep failed for null pubwtr field :\n"+str)
                        continue
                    med = arr5[3]
                    if med not in ["1","2","3"]:
                        print("StatRep failed for null med field :\n"+str)
                        continue
                    ota = arr5[4]
                    if ota not in ["1","2","3"]:
                        print("StatRep failed for null ota field :\n"+str)
                        continue
                    trav = arr5[5]
                    if trav not in["1","2","3"] :
                        print("StatRep failed for null trav field :\n"+str)
                        continue
                    net = arr5[6]
                    if net not in ["1","2","3"]:
                        print("StatRep failed for null net field :\n"+str)
                        continue
                    fuel = arr5[7]
                    if fuel not in ["1","2","3"]:
                        print("StatRep failed for null fuel field :\n"+str)
                        continue
                    food = arr5[8]
                    if food not in ["1","2","3"]:
                        print("StatRep failed for null food field :\n"+str)
                        continue
                    crime = arr5[9]
                    if crime not in ["1","2","3"] :
                        print("StatRep failed for null crime field :\n"+str)
                        continue
                    civil = arr5[10]
                    if civil not in ["1","2","3"]:
                        print("StatRep failed for null or missing civil field :\n"+str)
                        continue
                    pol = arr5[11]
                    if pol not in ["1","2","3"]:
                        print("StatRep failed for null pol field :\n"+str)
                        continue
                        
                    comments = arr2[5]
                    cur.execute("INSERT OR REPLACE INTO Statrep_Data (datetime, callsign, groupname, grid, SRid, prec, status, commpwr, pubwtr, med, ota, trav, net, fuel , food, crime, civil, political, comments) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?,?, ?, ?, ?, ?, ?, ?, ?, ?, ? )", (utc, callsign, currentgrp, curgrid, srid, prec, status, commpwr, pubwtr, med, ota, trav, net, fuel, food, crime, civil, pol, comments))
                    conn.commit()
                    getmember(callsign, membergrp1,membergrp2, utc)
                    #print(arr2)
                    print ("Added StatRep from :"+callsign+" ID :"+srid+" Added callsign to members list \n"+str)
                    continue
                if "{*%}" in str:  #THIS IS MARQUEE
                    arr = str.split('\t')
                    utc = arr[0]
                    callsignmix = arr[4]
                    arr2 = callsignmix.split(',')
                    count = len(arr) + len(arr2)
                    if count != 10:
                        continue
                    id = arr2[1]
                    callsignlong = arr2[0]
                    arr3 = callsignlong.split(':')
                    callsignlg = arr3[0]
                    arr4 = callsignlg.split('/')
                    callsign = arr4[0]
                    color = arr2[2]
                    marquee = arr2[3]
                    print("marquee to be written - id :"+id+" callsign :"+callsign+" groupname :"+currentgrp+" time :"+utc+" color :"+color+" mesaage : "+marquee)
                    cur.execute("INSERT OR REPLACE INTO marquees_Data (idnum, callsign, groupname, date, color, message) VALUES(?, ?, ?, ?, ?, ?)", (id, callsign, currentgrp, utc, color, marquee))
                    conn.commit()
                    getmember(callsign, membergrp1,membergrp2, utc)
                    print(count)
                    print("Added Marquee from :"+callsign+" ID :"+id+" Added callsign to members list \n"+str)
                    continue
                if "{~%}" in str:  # THIS IS CHECKIN
                    arr = str.split('\t')
                    utc = arr[0]
                    callsignmix = arr[4]
                    arr2 = callsignmix.split(',')
                    count = len(arr) + len(arr2)
                    if count != 8:
                        continue
                    id = arr2[1]
                    callsignlong = arr2[0]
                    arr3 = callsignlong.split(':')
                    callsignlg = arr3[0]
                    arr4 = callsignlg.split('/')
                    callsign = arr4[0]

                    traffic = arr2[1]
                    conn5 = sqlite3.connect("callarchive.db3")
                    cur5 = conn5.cursor()
                    rowsQuery = "SELECT Count() FROM Call_Data Where Call  = '" + callsign + "'"
                    cur5.execute(rowsQuery)
                    numberOfRows = cur5.fetchone()[0]
                    if numberOfRows == 1:
                        callgridlat = "SELECT gridlat FROM Call_Data Where Call  = '" + callsign + "'"
                        cur5.execute(callgridlat)
                        gridLatint = cur5.fetchone()[0]
                        gridLat = float(gridLatint)

                        callgridlong = "SELECT gridlong FROM Call_Data Where Call  = '" + callsign + "'"
                        cur5.execute(callgridlong)
                        gridLongint = cur5.fetchone()[0]
                        gridLong = float(gridLongint)
                        cur5.close()

                        # print(lastheard, call, gridLat, gridLong)
                        conn2 = sqlite3.connect("traffic.db3")
                        cur2 = conn2.cursor()
                        cur2.execute(
                            "INSERT OR REPLACE INTO checkins_Data (date, callsign, groupname, traffic, gridlat, gridlong) VALUES(?, ?, ?, ?, ? , ? )",
                            (utc,callsign, currentgrp, traffic, gridLat, gridLong))
                        conn2.commit()
                        cur2.close()
                        getmember(callsign, membergrp1,membergrp2, utc)
                        print("Added Checkin from callsign :"+callsign+" Added callsign to members list \n" +str)

                    else:
                        print("Found callsign:"+callsign+" Found group :"+currentgrp+ " failed parse, unable to add msg to database \n "+str)
                        continue








                    #cur.execute("INSERT OR REPLACE INTO checkins_Data (date, callsign, groupname, traffic) VALUES(?, ?, ?, ?)",(utc, callsign, currentgrp, traffic))
                    #conn.commit()
                    #getmember(callsign, membergrp1,membergrp2, utc)
                    #print(arr2[1])
                else:
                    try:
                        arr = str.split('\t')
                        utc = arr[0]
                        callsignmix = arr[4]
                        arr2 = callsignmix.split(',')
                        callsignlong = arr2[0]
                        arr3 = callsignlong.split(':')
                        callsignlg = arr3[0]
                        arr4 = callsignlg.split('/')
                        callsign = arr4[0]
                        if len(callsign) > 3 and len(callsign) < 7:
                            getheard(callsign, utc)
                        else:
                            print ("Failed to parse callsign "+callsign+" , message did not meet Commstatx criteria \n"+str)
                            continue
                    except IndexError:
                        continue
        except IndexError:
            continue

def checkIfProcessRunning(processName):
    '''
    Check if there is any running process that contains the given name processName.
    '''
    #Iterate over the all the running process
    for proc in psutil.process_iter():
        try:
            # Check if process name contains the given name string.
            if processName.lower() in proc.name().lower():
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False;


copyDirected()
parseDirected()
now = datetime.now()
print(now)
def runreaders():
    while True:
        getConfig()
        copyDirected()
        parseDirected()
        now = datetime.now()
        print(now)
        if checkIfProcessRunning('SQLiteSpy.exe'):
            print('Yes CommStatX is still running')
        else:
            print('No CommStatX has stopped')
            quit()
            #import sys
            #sys.exit()
        #time.sleep(30)


#runreaders()











