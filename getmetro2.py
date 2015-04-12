#This program calls WMATA's API, gets trains and times for Silver Spring
#and prints the results to <STDIN>
#Perl code now called from via subprocess in Python
#Called every 30 seconds via a crontab and shellscript
#Originally written for Python2
#4-11-15 Started using actual revision control
#3-22-15 Fixed IOError exception handling
#3-1-15 Added handling exceptions to deal with internet outages
#November 2014 Created
#Author: Brian Thomson
import urllib
#import urllib.request PYTHON3
import json
import subprocess
#public API key, please get your own for continuously repeated calls
url="http://api.wmata.com/StationPrediction.svc/json/GetPrediction/B08?api_key=kfgpmgvfgacx98de9q3xazww"
proc=subprocess.Popen(['perl','signmaster.pl'],stdin=subprocess.PIPE) #Uncomment before delpoying on PI
s=""
try:
        #Python2 next 2 lines - differences in URLLLIB
        response=urllib.urlopen(url)
        data=json.loads(response.read())['Trains']
        #Python3 next 2 lines - note that data request is now a bytestream
        #response=urllib.request.urlopen(url)
        #data=json.loads(response.read().decode('utf-8'))['Trains']
        #print "Car".rjust(3),"Destination".rjust(10),"Min".rjust(3)
        for x in range(0, len(data)):
                #I can't make it to the station in < 6 minutes!
                if int(data[x]['Min'])>=6:
                        s+=str(data[x]['Destination']) +" "+  str(data[x]['Min'])
                        if x < (len(data)-1):
                                s+="\n"
        proc.communicate(s) #Uncomment before deploying on PI
        #print(s) - For testing 

except IOError:
        s+="IO Error!"
        s+="\n"
        s+= "Chk Wifi"
        proc.communicate(s) #Uncomment before delpoying on PI
        #print(s)
        subprocess.call(["ifreset.sh"]) #Uncomment before delpoying on PI
