'''
The purpose of default files is testing only. 

For production processing use either CRAB or explicit file names in PoolSource.

triggerProcess....: the process containing the HLT information
filePath_EOS......: default input file path for files stored at EOS
'''

# Global dictionaries
config = {
    "74Xdata": {
	"triggerProcess": "HLT", 
	"recoProcess"   : "RECO",
        "globalTag"     : "74X_dataRun2_Prompt_v4", # recommendation from https://twiki.cern.ch/twiki/bin/view/CMS/JECDataMC
        "fileList"      : [],
        "filesPath"     : ""
        },
    "74Xmc": {
        "simProcess"     : "SIM",
        "triggerProcess" : "HLT",
        "recoProcess"    : "RECO",
        "globalTag"      : "74X_mcRun2_asymptotic_v4", #"74X_mcRun2_asymptotic_v2",
        "signalTrigger"  : "HLT_LooseIsoPFTau35_Trk20_Prong1_MET70_v6",
        "fileList"       : [],
        "filesPath"      : ""
        }
    }


class DataVersion:
    def __init__(self, DatasetObject):

        # Get the dataset version
        dataVersion = DatasetObject.dataVersion
        if not dataVersion in config:
            names = config.keys()
            names.sort()
            raise Exception("Unknown dataVersion '%s',  allowed versions are %s" % (dataVersion, ", ".join(names)))

        # Get the configuration according to the data version
        conf = config[dataVersion]

        # Set values
        self.trigger     = conf["triggerProcess"]
        self.recoProcess = conf.get("recoProcess", None)
        self.simProcess  = conf.get("simProcess" , None)
        self.version     = dataVersion
        self.globalTag   = conf["globalTag"]
        self.fileList    = DatasetObject.fileList
        self.filePath    = DatasetObject.fileList[0].rsplit("/", 1)[0]+"/"

        # Collision or MC data?
        if "data" in dataVersion:
            self.is_data = True
        else: 
            self.is_data = False                
            try:
                self.signalTrigger = conf["signalTrigger"]
            except KeyError:
                pass
        

    def PrintConfig(self, bFileList=False):
        print "=== dataVersion.py:"
        d = self.__dict__
        for key in d:
            if (key == "fileList") and (bFileList==False):
                continue
            config = '{:<15} {:<2} {:<40}'.format("\t " + key, ": ", d[key])
            print config
        return

    def isData(self):
        return self.is_data

    def isMC(self):
        return not self.is_data

    def is74X(self):
        return "74X" in self.version

    def getTriggerProcess(self):
        return self.trigger

    def getDefaultSignalTrigger(self):
        '''
        The trigger names in data can change so often that encoding it in the dataVersion is not flexible enough.
        '''
        if self.isData():
            raise Exception("Default signal trigger is available only for MC")
        return self.signalTrigger

    def getRecoProcess(self):
        if not self.recoProcess:
            raise Exception("Reco process name is not available for %s" % self.version)
        return self.recoProcess

    def getSimProcess(self):
        if not self.simProcess:
            raise Exception("Sim process name is not available for %s" % self.version)
        return self.simProcess

    def getGlobalTag(self):
        return self.globalTag
