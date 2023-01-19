# CommStatXW 0.061 for Win10 & Win 11 Released 01/19/23
<h3 style="color: #4485b8;">CommStatXW Ver 0.061 add on software for JS8Call groups&nbsp;&nbsp;<img src="https://github.com/W5DMH/CommStatXR/blob/main/CommStatXBeta.png?raw=true" alt="CommStatXW 0.061" width="300" height="170" /></h3>
<br><br>
<b>NOTE : If you are upgrading, please delete your existing commstax folder</b> 
<br><br>
CommstatXW is a Python version of the CommStat software designed to run on Windows 10 & Windows 11 operating systems. 
It is required for Python to be installed (best installed as administrator) 
Here is the link https://www.python.org/ftp/python/3.9.8/python-3.9.8-amd64.exe

Probably best to update python a bit before starting: (NOTE this step is not necessary for upgrades)<br>
<b>in a command prompt terminal type : python -m pip install --upgrade pip </b> <br>

Download the zip file to wherever you want it and unzip it and it will create the folder "commstatx", go into that folder and using command prompt terminal run install.py: <br>
<b>type: python installer.py </b>(NOTE: this step is not necessary if upgrading)<br>
After a successful install (this installs all of the necessary Python modules) in a command prompt terminal : <br>
<b>type: python commstatx.py</b>    

You should see a settings window that must be populated with a callsign, and a path to the 
JS8Call log directory (use JS8Call "LOG" menu item and "Open Log Directory" to get the path and
make sure there is in fact a DIRECTED.TXT file there, the path should be something like : 
c:\users\yourname\appdata\local\js8call <b>do not enter the trailing slash or the file name.</b> 

After that is complete you should be able to run CommStatx by retyping in the command prompt terminal:<br>
<b> type : python commstatx.py </b>
<br>
<BR>

 
<h3>Here is a link to the archive file:&nbsp;<a href="https://github.com/W5DMH/CommStatXW/raw/main/commstatx.zip" target="_blank" rel="noopener">CommStatXW 0.061 for Win10 & Win11 </a></h3>
<hr />

Get CommStat Support at: <br>
https://groups.io/g/CommStat

I must give credit to m0iax for his JS8CallAPISupport Script as that is what makes the transmitting possible.See the rest of his JS8Call Tools here : https://github.com/m0iax
<br>
