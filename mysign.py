import signmaster

class mySign:
    def __init__(self): 
        self.simulate=False #Set simulate=false to start.  If we want to simulate TRUE, we'll change that elsewhere.
        #Simulated outputs results to STDOUT.  Unsimulated sends them to sign via Perl script API
        #thus it should be false only if it is being deployed on the raspberry PI, with LED sign
        self.message=[]
        self.maxmessage=9 #sign holds up to 9 messages
        self.nummessage=0
        self.maxlength=12 #messages of 12 characters or less fit
    def addmessage(self, message):
        #trim message to fit the sign, truncates beyond maxlength
        if len(message)>self.maxlength:
                message=message[0:self.maxlength]
        #add up to maxlength messages
        if len(self.message)<=self.maxmessage:
                self.message.append(message)                        
    def messageout(self):
        #Prepares message to be sent out
        s=""
        for i,x in enumerate(self.message):
                s+=x
                if i <(len(self.message)-1):
                        s+="\n"
        return s
    def sendmessage(self):
        if self.simulate==False:
            #try:
            signmaster.sendmessage(self.message)
            #except:
            #    print("Unable to send message to sign")
        else:
            print(self.messageout())
