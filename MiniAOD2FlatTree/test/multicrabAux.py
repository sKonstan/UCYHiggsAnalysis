#================================================================================================
# Author .........: Alexandros X. Attikis 
# Institute ......: University Of Cyprus (UCY)
# Email ..........: attikis@cern.ch
#================================================================================================
'''
CRAB3 Advanced Tutorial (26 June 2014): https://indico.cern.ch/event/389464/
Running CMSSW code on the Grid using CRAB3: https://twiki.cern.ch/twiki/bin/view/CMSPublic/WorkBookCRAB3Tutorial
'''

#================================================================================================
# All imported modules
#================================================================================================
### System modules
import os, sys
import array
import math
import copy
import inspect
import glob
from optparse import OptionParser
from itertools import cycle


#================================================================================================
# Declarations here
#================================================================================================
lumiMask50ns       = "/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions15/13TeV/Cert_246908-255031_13TeV_PromptReco_Collisions15_50ns_JSON_v2.txt"
lumiMask25ns       = "/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions15/13TeV/Cert_246908-260426_13TeV_PromptReco_Collisions15_25ns_JSON.txt"
lumiMask25nsSilver = "/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions15/13TeV/Cert_246908-260426_13TeV_PromptReco_Collisions15_25ns_JSON_Silver.txt"

datasetsMiniAODv2_WJets = []
datasetsMiniAODv2_WJets.append( Dataset('/WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM')              )
datasetsMiniAODv2_WJets.append( Dataset('/WJetsToLNu_HT-100To200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM')   )
datasetsMiniAODv2_WJets.append( Dataset('/WJetsToLNu_HT-200To400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM')   )
datasetsMiniAODv2_WJets.append( Dataset('/WJetsToLNu_HT-400To600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM')   )
datasetsMiniAODv2_WJets.append( Dataset('/WJetsToLNu_HT-600To800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM')   )
datasetsMiniAODv2_WJets.append( Dataset('/WJetsToLNu_HT-800To1200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM')  )
datasetsMiniAODv2_WJets.append( Dataset('/WJetsToLNu_HT-1200To2500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM') )
datasetsMiniAODv2_WJets.append( Dataset('/WJetsToLNu_HT-2500ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM')  )

datasetsMiniAODv2_Top = []
datasetsMiniAODv2_Top.append( Dataset('/TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v3/MINIAODSIM')                         )
datasetsMiniAODv2_Top.append( Dataset('/ST_tW_antitop_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM')     )
datasetsMiniAODv2_Top.append( Dataset('/ST_tW_top_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v2/MINIAODSIM')         )
datasetsMiniAODv2_Top.append( Dataset('/ST_t-channel_top_4f_leptonDecays_13TeV-powheg-pythia8_TuneCUETP8M1/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM')     )
datasetsMiniAODv2_Top.append( Dataset('/ST_t-channel_antitop_4f_leptonDecays_13TeV-powheg-pythia8_TuneCUETP8M1/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM') )
datasetsMiniAODv2_Top.append( Dataset('/ST_s-channel_4f_leptonDecays_13TeV-amcatnlo-pythia8_TuneCUETP8M1/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM')       )

#================================================================================================
# Define class here
#================================================================================================
class DatasetClass(object):
    def __init__(self, url, dbs="global", dataVersion="74Xmc", lumiMask=lumiMask25ns, verbose = False):
        self.URL         = url
        self.DBS         = dbs
        self.dataVersion = dataVersion
        self.lumiMask    = lumiMask
        self.bVerbose    = verbose
        self.Verbose()
        
    def Verbose(self, messageList=None):
        '''
        Custome made verbose system. Will print all messages in the messageList
        only if the verbosity boolean is set to true.
        '''
        if self.bVerbose == False:
            return
        
        print "%s:" % (self.__class__.__name__ + "." + sys._getframe(1).f_code.co_name + "()")
        if messageList==None:
            return
        else:
            for message in messageList:
                print "\t", message
        return


    def Print(self, messageList=[""]):
        '''
        Custome made print system. Will print all messages in the messageList
        even if the verbosity boolean is set to false.
        '''
        print "%s:" % (self.__class__.__name__ + "." + sys._getframe(1).f_code.co_name + "()")
        for message in messageList:
            print "\t", message
        return


    def SetVerbose(self, verbose):
        '''
        Manually enable/disable verbosity.
        '''
        self.verbose = verbose
        self.Verbose(["Verbose mode = ", self.verbose])
        return


    def isData(self):
        '''
        Tells if sample is data or not.
        '''
        if "data" in self.dataVersion:
            return True
        return False


    def _SetupDatasets(self):
        '''
        '''
        self.Verbose()
        #self.Verbose(["Unknown Dataset '%s'." % (dataset), "Please ensure that dataset names used are valid. EXIT"])
        #sys.exit()

        return

#================================================================================================
