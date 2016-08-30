import pickle, datetime

#Save data as a pickle file and flat text file
# expNumber must be set first using openExperiment method
# data can be appeneded to the file by calling process method, datagram is saved as a string and is time stamped

class DataHandler(object):
    def __init__(self):
        self.expNumber = None

    #public methods to be called for openning, closing, and processing a data
    def openExperiment(self, expNumber):
        self.expNumber = expNumber

    def closeExperiment(self, expNumber):
        self.expNumber = "CLOSED"

    def process(self, datagram):
        if datagram == {}: return
        if self.expNumber is None: return
        try:
            identity = datagram.get("identity")
            dataFile = datetime.today().strftime("%b_%d").lower()+self.expNumber+'_'+str(identity)
            with open(dataFile, 'a') as of:
                of.write(pickle.dumps(datagram)+'\n')
            with open(dataFile+'_flat.txt', 'a') as of:
                of.write(json.dumps(datagram)+'\n')
        except Exception, e:
            print e