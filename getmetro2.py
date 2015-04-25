#This program calls WMATA's API, gets trains and times for Silver Spring
#and pipes them to the led sign via a perl program.
#Called every 30 seconds via a crontab and shellscript
#Hardware dependent, only works with RPI and LEDSign
#November 2014 Created
#Author: Brian Thomson
from time import strftime
import urllib.request #PYTHON3
import json
import subprocess
import argparse

defaultconfig={'station':'B08','apikey':'kfgpmgvfgacx98de9q3xazww','walktime':'6','loop':'False','simulate':'True'}

def setupconfig():
        """
        Creates config file for the program, with info on metro data.
        Since the program may be started and stopped and restarted later
        we want to preserve the user information in a permanent place so the
        user doesn't have to setup each time.
        Config info is stored in a JSON file since I'm using JSON anyways for the Metro API
        """
        station=input("Enter your station code: ")
        walktime=input("How long (minutes) to walk to the metro? ")
        newapi=""
        newapi=input("Change API Code (y/n)? ")
        while newapi!="y" | newapi!="Y" | newapi!="n" | newapi!="N":
                if newapi=="y" | newapi=="Y": #terrible code and must be fixed once I have time with regex!
                        apikey=input("Enter new API Key: ")
                elif newapi=="n" | newapi=="N":
                        apikey=defaultconfig['apikey']
        simulate=input("Simulated mode on (turn off when using on Raspberry PI)?\n Enter "'y'" for on and "'n'" for off: ")
        while simulate!="y" | simulate!="Y" | simulate!="n" | simulate!="N":
                if simulate=="n" | simulate=="N": #ditto above!
                        simulate=False
                elif simulate=="y" | simulate=="Y":
                        simlulate=True
        config={'station':station,'apikey':apikey,'walktime':str(walktime),'loop':'False','simulate':simulate}
        json.dump(config,open('config.json','w'),sort_keys=True,indent=4)

def resetdata():
        """Factroy Defaults, if you will"""
        json.dump(defaultconfig,open('config.json','w'),sort_keys=True,indent=4)

parser=argparse.ArgumentParser()
parser.add_argument("-l","--loop", nargs="?", help="program continuosly loops") #not yet implemented, use cron
parser.add_argument("-s","--setup", nargs="?", help="enter setup mode")
parser.add_argument("-r","--reset", nargs="?", help="reset to defaults")
parser.add_argument("-a","--add", nargs="?", help="Add a custom message") #Add custom message need to make dealing with multiple words easier
args=parser.parse_args()

if args.reset:
        resetdata()

if args.setup:
        setupconfig()

#add a routine to check for existence, go to reset routine, providing defaults
try:
        metroconf=json.load(open('config.json'))
except:
        resetdata()
        metroconf=json.load(open('config.json'))

class myMetro:
        def __init__(self):
                try:
                        metroconf=json.load(open('config.json'))
                except:
                        resetdata()
                        metroconf=json.load(open('config.json'))                       
                self.station=metroconf['station']
                self.apikey=metroconf['apikey']
                self.walktime=int(metroconf['walktime']) #how long it takes to walk to station
        def url(self):
                return "http://api.wmata.com/StationPrediction.svc/json/GetPrediction/"+self.station+"?api_key="+self.apikey

class mySign:
        def __init__(self): #do i need this?  
                metroconf=json.load(open('config.json'))        
                self.simulate=bool(metroconf['simulate']) #Simulated mode prints output, otherwise it outputs to the sign
                #thus it should be false only if it is being deployed on the raspberry PI, with LED sign
                self.message=[]
                self.maxmessage=5
                self.nummessage=0
        def addmessage(self, message):
                if len(self.message)<=self.maxmessage:
                        self.message.append(message)                        
        def messageout(self):
                """Prepares and writes message for STDOUT or LED sign"""
                s=""
                for i,x in enumerate(self.message):
                        s+=x
                        if i <(len(self.message)-1):
                                s+="\n"
                return s
                        
sign=mySign()
metrodat=myMetro()

if sign.simulate==False:
        proc=subprocess.Popen(['perl','signmaster.pl'],stdin=subprocess.PIPE,universal_newlines=True)

if args.add:
        sign.addmessage(args.add)

try:
        response=urllib.request.urlopen(metrodat.url())
        data=json.loads(response.read().decode('utf-8'))['Trains']
        for x in data:
                try:
                        if int(x['Min'])>=metrodat.walktime:
                                sign.addmessage(str(x['Destination']) +" "+  str(x['Min']))   
                #Handle all non-int cases (ARR, BRD, ---, etc)
                except ValueError:
                        pass
                if len(sign.message)>=sign.maxmessage-1:
                        break
        if sign.message==[]:
                sign.addmessage("No Trains!")
        sign.addmessage(strftime("%H:%M"))
        if sign.simulate==False:
                proc.communicate(sign.messageout())
        else:
                print(sign.messageout())
except IOError:
        sign.addmessage("IO Error!")
        sign.addmessage("Chk Wifi")
        if sign.simulate==False:
                proc.communicate(sign.messageout())
                subprocess.call(["ifreset.sh"])
        else:
                print(sign.messageout())
