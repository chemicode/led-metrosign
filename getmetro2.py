#This program calls WMATA's API, gets trains and times for Silver Spring
#and pipes them to the led sign via a perl program.
#Called every 30 seconds via a crontab and shellscript
#Hardware dependent, only works with RPI and LEDSign but can simulate and print
#November 2014 Created
#Author: Brian Thomson
from time import strftime
import urllib.request, json, subprocess, argparse, re
import mymetro, mysign

def setupconfig():
        """
        Creates config file for the program, with info on metro data.
        Since the program may be started and stopped and restarted later
        we want to preserve the user information in a permanent place so the
        user doesn't have to setup each time.
        Config info is stored in a JSON file since I'm using the JSON library
        anyways for the Metro API
        """
        station=input("Enter your station code: ")
        walktime=input("How long (minutes) to walk to the metro? ")
        newapi=""
        simulate=""
        while True:
                newapi=input("Change API Code (y/n)? ")
                if re.match("y|yes",newapi,re.IGNORECASE):
                        apikey=input("Enter new API Key: ")
                        break
                elif re.match("n|no",newapi,re.IGNORECASE):
                        try:
                                apikey=json.load(open('config.json'))['apikey']
                        except:
                                apikey=defaultconfig['apikey']
                                print("No config file, defaultin to public key")
                        break
        while True:
                simulate=input("Simulated mode on (turn off when using on Raspberry PI)?\n Enter "'y'" for on and "'n'" for off: ")
                if re.match("n|no",simulate,re.IGNORECASE):
                        simulate=False
                        break
                elif re.match("y|yes",simulate,re.IGNORECASE):
                        simulate=True
                        break
        config={'station':station,'apikey':apikey,'walktime':str(walktime),'loop':'False','simulate':simulate}
        json.dump(config,open('config.json','w'),sort_keys=True,indent=4)

def resetdata():
        """Factroy Defaults, if you will"""
        json.dump(mymetro.defaultconfig,open('config.json','w'),sort_keys=True,indent=4)

def main():
        parser=argparse.ArgumentParser()
        parser.add_argument("-s","--setup", action='store_true', help="enter setup mode")
        parser.add_argument("-r","--reset", action='store_true', help="reset to defaults")
        parser.add_argument("-a","--add", nargs="?", help="Add a custom message") #Add custom message need to make dealing with multiple words easier
        args=parser.parse_args()

        if args.reset:
                resetdata()

        if args.setup:
                setupconfig()

        #add a routine to check for existence of config.JSON
        try:
                metroconf=json.load(open('config.json'))
        except:
                resetdata()
                metroconf=json.load(open('config.json'))
                               
        sign=mysign.mySign()
        metrodat=mymetro.myMetro()
        sign.simulate=bool(metroconf['simulate'])
        
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
                if sign.message==[] or sign.message==[args.add]:
                        sign.addmessage("No Trains!")
                sign.addmessage(strftime("%H:%M"))
                sign.sendmessage()

        except IOError:
                sign.addmessage("IO Error!")
                sign.addmessage("Chk Wifi")
                sign.addmessage(strftime("%H:%M"))
                sign.sendmessage()
                try:
                        subprocess.call(["ifreset.sh"]) #usually resetting WIFI solves connection problems
                except:
                        pass
                
if __name__ == "__main__":
        main()
