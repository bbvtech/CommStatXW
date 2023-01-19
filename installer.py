
#!/usr/bin/env python3
import subprocess
import sys
import os


def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

firstmodule = "pyqt5"
secondmodule = "PyQtWebEngine"
thirdmodule = "feedparser"
forthmodule = "file-read-backwards"
fifthmodule = "folium"
sixthmodule = "configparser"
seventhmodule = "psutil"
install(firstmodule)
install(secondmodule)
install(thirdmodule)
install(forthmodule)
install(fifthmodule)
install(sixthmodule)
install(seventhmodule)



