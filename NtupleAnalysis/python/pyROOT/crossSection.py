'''
Cross sections from:
[1] https://twiki.cern.ch/twiki/bin/view/CMS/SummaryTable1G25ns
[2] https://indico.cern.ch/event/439995/session/0/contribution/6/attachments/1143460/1638648/diboson_final.pdf
[3] https://twiki.cern.ch/twiki/bin/view/CMS/SummaryTable1G25ns#DY_Z
[4] https://twiki.cern.ch/twiki/bin/view/CMS/SummaryTable1G25ns#Single_top
[5] http://cms.cern.ch/iCMS/jsp/db_notes/noteInfo.jsp?cmsnoteid=CMS%20AN-2015/321
[6] https://twiki.cern.ch/twiki/bin/view/CMS/SummaryTable1G25ns#H_X_for_SUSY
[7] https://twiki.cern.ch/twiki/bin/view/LHCPhysics/TtbarNNLO

Usage Example:
from UCYHiggsAnalysis.NtupleAnalysis.pyROOT.crossSection import xSections
print xSections.crossSection("QCD_Pt_30to50", "13")
'''

#================================================================================================
# Imports
#================================================================================================
import sys


#================================================================================================
# Class Definition
#================================================================================================
class CrossSection:
    '''
    Cross section of a single process (physical dataset)
    '''
    def __init__(self, name, energyDictionary, verbose=False):
        '''
        The parameter "name" is the Name of the physics process. The parameter "energyDictionary" is 
        a  Dictionary of energy -> cross section (energy as string in TeV, cross section as float in pb)
        '''
        self.verbose    = verbose
        self.name       = name
        self.energyDict = {}
        for key, value in energyDictionary.iteritems():
            setattr(self, key, value)
        return

    
    def SetAttribute(self, attr, value):
        self.Verbose()
        return setattr(self, attr, value)

    
    def GetAttribute(self, attr):
        self.Verbose()
        if hasattr(self, attr):
            return getattr(self, attr)
        else:
            raise Exception("Class object '%s' does not have attribute '%s'" % (self.GetSelfName(), attr))

    def Verbose(self, message=""):
        '''
        Custome made verbose system. Will print all messages in the messageList
        only if the verbosity boolean is set to true.
        '''
        if self.verbose:
            print "=== %s:" % (self.__class__.__name__ + "." + sys._getframe(1).f_code.co_name + "()")
            if message!="":
                print "\t", message
        return


    def Print(self, message=""):
        '''
        Custome made print system. Will print the message even if the verbosity boolean is set to false.
        '''
        print "=== %s:" % (self.__class__.__name__ + "." + sys._getframe(1).f_code.co_name + "()")
        if message!="":
            print "\t", message
        return

    
    def PrintList(self, messageList=[""], printSelf=True):
        '''
        Custome made print system. Will print all messages in the messageList even if the verbosity boolean is set to false.
        '''
        for counter, message in enumerate(messageList):
            if counter == 0 and printSelf:
                self.Print(message)
            else:
                print "\t", message
        return


    def PrintWarning(self, msg, keystroke):
        '''                                                                                                                                                          
        Print a warning and make sure user sees it by requiring a keystroke
        '''
        self.Print()
        
        response = raw_input("\t" + msg + ". Press \"%s\" to quit, any other key to proceed: " % (keystroke))
        if response== "q":
            sys.exit()
        else:
            return
        return
    
        
    def PrintAttributes(self):
        '''
        Call this function to print all class attributes.
        '''
        self.Print("Attributes: %s" % (self.__dict__))
        return


    def Get(self, energy):
        '''
        Get the cross section for the given energy (in TeV)
        '''
        try:
            return getattr(self, energy)
        except AttributeError:
            msg = "No cross section set for process %s for energy %s. EXIT" % (self.name, energy)
            self.Print(msg)
            sys.exit()
        
        return


#================================================================================================
# Class Definition
#================================================================================================
class CrossSectionList:
    '''
    List of CrossSection objects
    '''
    def __init__(self, *args):
        self.crossSections = args[:]
        return

    
    def GetSelfName(self):
        return self.__class__.__name__


    def GetFunctionName(self):
        return sys._getframe(1).f_code.co_name + "()"


    def SetAttribute(self, attr, value):
        self.Verbose()
        return setattr(self, attr, value)

    
    def GetAttribute(self, attr):
        self.Verbose()
        if hasattr(self, attr):
            return getattr(self, attr)
        else:
            raise Exception("Class object '%s' does not have attribute '%s'" % (self.GetSelfName(), attr))

    def Verbose(self, message=""):
        '''
        Custome made verbose system. Will print all messages in the messageList
        only if the verbosity boolean is set to true.
        '''
        if self.verbose:
            print "=== %s:" % ( self.GetSelfName() + "." + self.GetFunctionName() )
            if message!="":
                print "\t", message
        return


    def Print(self, message=""):
        '''
        Custome made print system. Will print the message even if the verbosity boolean is set to false.
        '''
        print "=== %s:" % ( self.GetSelfName() + "." + self.GetFunctionName() )
        if message!="":
            print "\t", message
        return

    
    def PrintList(self, messageList=[""], printSelf=True):
        '''
        Custome made print system. Will print all messages in the messageList even if the verbosity boolean is set to false.
        '''
        for counter, message in enumerate(messageList):
            if counter == 0 and printSelf:
                self.Print(message)
            else:
                print "\t", message
        return


    def PrintWarning(self, msg, keystroke):
        '''                                                                                                                                                          
        Print a warning and make sure user sees it by requiring a keystroke
        '''
        self.Print()
        
        response = raw_input("\t" + msg + ". Press \"%s\" to quit, any other key to proceed: " % (keystroke))
        if response== "q":
            sys.exit()
        else:
            return
        return
    
        
    def PrintAttributes(self):
        '''
        Call this function to print all class attributes.
        '''
        self.Print("Attributes: %s" % (self.__dict__))
        return


    def crossSection(self, name, energy):
        for obj in self.crossSections:
            if name == obj.name:
                return obj.Get(energy)
        return None


#================================================================================================    
xSections = CrossSectionList(
    CrossSection("WW", {
        "13": 63.21, # [2]
    }),
    CrossSection("WZ", {
        "13": 22.82, # [2]
    }),
    CrossSection("ZZ", {
        "13": 10.32,  # [2]
    }),
    CrossSection("ZZZ", {
        "13": 0.01398, # [1]
    }),
    CrossSection("WZZ", {
        "13": 0.05565, # [1]
    }),
    CrossSection("WWZ", {
        "13": 0.1651,  # [1]
    }),
    CrossSection("TTJets", {
        "13": 831.76,  # [7] [m(top) = 172.5 GeV/c^2]
    }),
    CrossSection("WJetsToLNu", {
        "13": 61526.7, # [1]
    }),
    CrossSection("DYJetsToLL_M_10to50", {
        "13" :18610.0, # [3]
    }),
    CrossSection("DYJetsToLL_M_50", {
        "13": 6025.2, # [3]
    }),
    CrossSection("ST_tW_top_5f_inclusiveDecays", {
            "13": 35.6, #  [4], [1], [5]
            }),
    CrossSection("ST_tW_antitop_5f_inclusiveDecays", {
        "13": 35.6,  # [4], [1], [5]
    }),
    CrossSection("ST_t_channel_top_4f_leptonDecays", {
            "13": 44.33, # [4]
            }),
    CrossSection("ST_t_channel_antitop_4f_leptonDecays", {
            "13": 26.38 #[4], [5] has 26.71
            }),
    CrossSection("ST_t_channel_4f_leptonDecays", {
            "13": 70.69, # [4]
            }),
    CrossSection("ST_s_channel_4f_leptonDecays", {
            "13": 3.36, # [4], [5] has 3.75
            }),
    CrossSection("ttHJetToNonbb_M125", {
            "13": 0.215, # [6], [5] has 0.2586
            }),
)
