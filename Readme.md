<<<<<<< HEAD
# CommStatX Ver 0.09 Released 01/24/23
<h3 style="color: #4485b8;">CommStatX Ver 0.09 add on software for JS8Call groups&nbsp;&nbsp;<img src="https://github.com/W5DMH/CommStatX/blob/main/CommStatXBeta.png?raw=true" alt="CommStatX 0.09" width="300" height="170" /></h3>

CommstatX is a Python version of the CommStat software <b>designed to run on Mint 20.3 AND Raspberry Pi4 64bit Bullseye/b><br>
=======
# CommStatXW 0.062 for Win10 & Win 11 Released 01/19/23
<h3 style="color: #4485b8;">CommStatXW Ver 0.062 add on software for JS8Call groups&nbsp;&nbsp;<img src="https://github.com/W5DMH/CommStatXR/blob/main/CommStatXBeta.png?raw=true" alt="CommStatXW 0.062" width="300" height="170" /></h3>
>>>>>>> parent of c7f4cb7 (Update Readme.md)
<br><br>
NOTE : If you are upgrading, first delete your existing commstatx folder and then skip right to the <br>
Commstatx INSTALL PROCEDURE
<br><br>
Probably best to update python a bit before starting: <br>
<b>in a terminal type : python3 -m pip install --upgrade pip </b><br><br>


<b>Commstatx INSTALL PROCEDURE</B>
when the above command completes, make sure you are in your home folder and then : <br>
<b>Type : git clone https://github.com/W5DMH/commstatx.git </b>
<br><br>
When the above command completes
<b>Type: cd commstatx</b>
<br><br>
<b>type: python3 install.py </b>(running install is not necessary on upgrades) 
<br><br>
After a successful install (this installs all of the necessary Python modules, please watch for errors!) 

<b>type: python3 commstatx.py</b>   <br><br>

you should see a settings window that must be populated with a callsign, and a path to the 
JS8Call log directory (use JS8Call "LOG" menu item and "Open Log Directory" to get the path and
make sure there is in fact a DIRECTED.TXT file there ....the path should be something 
like /home/dan/.local/share/JS8Call    do not enter the trailing slash or the file name. <br>
<B>Commstatx WILL THROW AN ERROR WHEN YOU SAVE YOUR SETTINGS THIS IS OK!</B>
<br><br>

After that is complete you should be able to run CommStatx by retyping:<br>
<b> type : python3 commstatx.py </b>

<<<<<<< HEAD
<br><br><br>
=======
 
<h3>Here is a link to the archive file:&nbsp;<a href="https://github.com/W5DMH/CommStatXW/raw/main/commstatx.zip" target="_blank" rel="noopener">CommStatXW 0.062 for Win10 & Win11 </a></h3>
<hr />
>>>>>>> parent of c7f4cb7 (Update Readme.md)

Get CommStat Support at: <br>
https://groups.io/g/CommStat

I must give credit to m0iax for his JS8CallAPISupport Script as that is what makes the transmitting possible.See the rest of his JS8Call Tools here : https://github.com/m0iax
<br>
