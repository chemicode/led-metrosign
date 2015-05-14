import json

defaultconfig={'station':'B08','apikey':'kfgpmgvfgacx98de9q3xazww','walktime':'6','loop':'False','simulate':'True'}
#I've hardcoded my default configuration for the program, for resetting purposes or in case the config.json file is deleted

class myMetro:
    """
    Class for personal metro data.  Most of this is obtained from config file,
    at least currently.
    """

    def __init__(self):
        try:
            metroconf=json.load(open('config.json'))
        except:
            print("Error loading JSON, defaulting to standard config")
            #I've hardcoded my default configuration for the program, for resetting purposes or in case the config.json file is deleted
            metroconf=defaultconfig
        self.station=metroconf['station']
        self.apikey=metroconf['apikey']
        self.walktime=int(metroconf['walktime']) #how long it takes to walk to station
    def url(self):
        return "http://api.wmata.com/StationPrediction.svc/json/GetPrediction/"+self.station+"?api_key="+self.apikey
