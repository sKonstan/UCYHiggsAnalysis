'''
The purpose of default files is testing only. 

For production processing use either CRAB or explicit file names in PoolSource.

triggerProcess....: the process containing the HLT information
filePath_EOS......: default input file path for files stored at EOS
filePath_CASTOR...: default input file path for files stored at CASTOR
filePath_LXPLUS...: default input file path for files stored at LXPLUS
'''

# Global dictionaries
config = {
    "74Xdata": {
	"triggerProcess": "HLT", 
	"recoProcess"    : "RECO",
        "globalTag"      : "74X_dataRun2_Prompt_v4", # recommendation from https://twiki.cern.ch/twiki/bin/view/CMS/JECDataMC
        #"filePath_EOS"   : "",
        #"filePath_CASTOR": "",
        #"filePath_LXPLUS": "",
        },
    "74Xmc": {
        "simProcess"     : "SIM",
        "triggerProcess" : "HLT",
        "recoProcess"    : "RECO",
        "globalTag"      : "74X_mcRun2_asymptotic_v4", #"74X_mcRun2_asymptotic_v2",
        "signalTrigger"  : "HLT_LooseIsoPFTau35_Trk20_Prong1_MET70_v6",
        "filePath_EOS"   : "/store/mc/RunIISpring15DR74/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/Asympt25ns_MCRUN2_74_V9-v1/20000/", #example
        #"filePath_CASTOR": "",
        #"filePath_LXPLUS": "",
        }
    }


class DataVersion:
    def __init__(self, dataVersion):
        if not dataVersion in config:
            names = config.keys()
            names.sort()
            raise Exception("Unknown dataVersion '%s',  allowed versions are %s" % (dataVersion, ", ".join(names)))

        conf = config[dataVersion]

        # Set values
        self.trigger     = conf["triggerProcess"]
        self.recoProcess = conf.get("recoProcess", None)
        self.simProcess  = conf.get("simProcess" , None)
        self.version     = dataVersion
        self.globalTag   = conf["globalTag"]

        # If any of these paths are defined assign them to values (value of "f" in loop will be assigned to class variable "self.f")
        for f in ["filePath_EOS", "filePath_CASTOR", "filePath_LXPLUS"]: 
            if f in conf:
                setattr(self, f, conf[f])

        # Collision data
        if "data" in dataVersion:
            self.is_data = True
        # MC
        else: 
            self.is_data = False                
            try:
                self.signalTrigger = conf["signalTrigger"]
            except KeyError:
                pass
                
    def PrintConfig(self):
        print "=== dataVersion.py:"
        d = self.__dict__
        for key in d:
            print "\t\"%s\" = \"%s\"" % (key, d[key])
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

    def getDefaultFileEOS(self):
        if not hasattr(self, "filePath_EOS"):
            print "No default file in EOS for dataVersion " + self.version
            return ""
        return self.filePath_EOS

    def getDefaultFileCASTOR(self):
        if not hasattr(self, "filePath_CASTOR"):
            print "No default file in CASTOR for dataVersion " + self.version
            return ""
        return self.filePath_CASTOR

    def getDefaultFileLXPLUS(self):
        if not hasattr(self, "filePath_LXPLUS"):
            print "No default file in LXPLUS for dataVersion " + self.version
            return ""
        return self.filePath_LXPLUS
