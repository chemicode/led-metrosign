#This program calls WMATA's API, gets trains and times for Silver Spring
#and sends them to the led sign via a perl program.
#Perl code now called from via subprocess in Python
#Called every 30 seconds via a crontab and shellscript
#Originally written for Python2
#November 2014 Created
#Author: Brian Thomson
import urllib.request #PYTHON3
import json
import subprocess
#public API key, please get your own for continuously repeated calls
url="http://api.wmata.com/StationPrediction.svc/json/GetPrediction/B08?api_key=kfgpmgvfgacx98de9q3xazww"
proc=subprocess.Popen(['perl','signmaster.pl'],stdin=subprocess.PIPE) #Uncomment before delpoying on PI
s=""
y=0
try:
        response=urllib.request.urlopen(url)
        data=json.loads(response.read().decode('utf-8'))['Trains']
        for x in data:
                y+=1
                try:
                        #I can't make it to the station in < 6 minutes!
                        if int(x['Min'])>=6:
                                s+=str(x['Destination']) +" "+  str(x['Min'])
                                if y < (len(data)):
                                        s+="\n"    
                #Handle all non-int cases with a pass (ARR, BRD, ---, etc)
                except ValueError:
                        pass
        proc.communicate(s) #Uncomment before deploying on PI
        #print(s) #- For testing
except IOError:
        s+="IO Error!"
        s+="\n"
        s+= "Chk Wifi"
        proc.communicate(s) #Uncomment before delpoying on PI
        #print(s)
        subprocess.call(["ifreset.sh"]) #Uncomment before delpoying on PI
