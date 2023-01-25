#!/usr/bin/env python3
import subprocess
import sys
import os 



def runsettings():
    subprocess.call(["python3", "settings.py"])


def install(package):

    
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
    except subprocess.CalledProcessError as e:
        #print("this is the except install error: "+str(e.returncode))
        if e.returncode > 0:
            print(" Installation failed, copy and paste this screen \n into https://groups.io/g/CommStat for support exiting now")
            sys.exit()
            #Exception("failed installation, cannot conntinue") 


    
    
def test_python():
        try:
            if int(sys.version_info[0]) < 3:
                print("You are using Python "+str(sys.version_info[0]))
                print("Commstatx requires Python 3.9 or newer, install cannot continue")
                #raise Exception("Wrong Python version, cannot continue installation, please upgrade Python")
                sys.exit()
    
            if int(sys.version_info[1]) < 8:
                print("You are using Python 3."+str(sys.version_info[1]))
                print("Commstatx requires Python 3.8 or newer")
                #raise Exception("Wrong Python cannot continue")
                sys.exit()
            else:
                print("Appropriate version of Python found : Python 3."+str(sys.version_info[1])+", continuing installation")

        except :
            print("Exception while testing Python version, cannot continue installation")
            sys.exit()
        
        firstmodule = "pyqt5"
        secondmodule = "PyQtWebEngine"
        thirdmodule = "feedparser"
        forthmodule = "file-read-backwards"
        fifthmodule = "folium"
        install(firstmodule)
        install(secondmodule)
        install(thirdmodule)
        install(forthmodule)
        install(fifthmodule)


test_python()



#os.chdir(os.path.dirname(__file__))
#print(os.getcwd())

runsettings()



