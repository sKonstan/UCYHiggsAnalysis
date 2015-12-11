#!/usr/bin/env python
'''
CRAB3 Advanced Tutorial: https://indico.cern.ch/event/389464/
Running CMSSW on Grid for CRAB3: https://twiki.cern.ch/twiki/bin/view/CMSPublic/WorkBookCRAB3Tutorial
'''

#================================================================================================
# Import modules
#================================================================================================
import sys
import UCYHiggsAnalysis.MiniAOD2FlatTree.tools.datasetsHelper as datasetsHelper


#================================================================================================
# Global declarations
#================================================================================================
lumiMask50ns       = "/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions15/13TeV/Cert_246908-255031_13TeV_PromptReco_Collisions15_50ns_JSON_v2.txt"
lumiMask25ns       = "/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions15/13TeV/Cert_246908-260426_13TeV_PromptReco_Collisions15_25ns_JSON.txt"
lumiMask25nsSilver = "/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions15/13TeV/Cert_246908-260426_13TeV_PromptReco_Collisions15_25ns_JSON_Silver.txt"


#================================================================================================
# Class  declaration
#================================================================================================
class Dataset:
    def __init__(self, url, dbs="global", dataVersion="74Xmc", lumiMask=lumiMask25ns, fileList = []):
        self.DAS         = url
        self.DBS         = dbs
        self.dataVersion = dataVersion
        self.lumiMask    = lumiMask
        self.fileList    = fileList

    def isData(self):
        '''
        Tells you if dataset is real data or not (isMC).
        '''
        if "data" in self.dataVersion:
            return True
        return False
    

#================================================================================================
# Class  declaration
#================================================================================================
class Datasets:
    def __init__(self, debugMode=False):
        self.bDebugMode               = debugMode
        self.DataDatasets_MiniAODv2   = []
        self.McDatasets_MiniAODv2     = []
        self.AllDatasets_MiniAODv2    = []
        self.DatasetObjects_MiniAODv2 = []
        self.CreateDatasets_MiniAODv2()
        #self.CreateDatasetObjectLists()

    def DebugMode(self, messageList=None):
        '''
        Custome made verbose system. Will print all messages in the messageList
        only if the verbosity boolean is set to true.
        '''
        if self.bDebugMode == False:
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

        self.MsgCounter = self.MsgCounter  + 1
        print "[%s] %s:" % (self.MsgCounter, self.__class__.__name__ + "." + sys._getframe(1).f_code.co_name + "()")
        for message in messageList:
            print "\t", message
        return


    def GetDatasetObjects(self, miniAODversion="RunIISpring15MiniAODv2"):
        '''
        Get all dataset objects for a given miniAOD verstions
        '''
        self.DebugMode()
        
        datasetObjects = []
        datasetNames   = []
        if miniAODversion=="RunIISpring15MiniAODv2":
            datasetNames.extend(self.DataDatasets_MiniAODv2)
            datasetNames.extend(self.McDatasets_MiniAODv2)        

        # For-loop: All dataset names
        for dataset in datasetNames:
            datasetObjects.append(self.GetDatasetObject(dataset))

        return datasetObjects

        
    def CreateDatasets_MiniAODv2(self):
        '''
        Create all Dataset objects for the MiniAODv2 version and save them all in a deducated list.
        '''
        self.DebugMode()

        self.DataDatasets_MiniAODv2 = []
        self.McDatasets_MiniAODv2   = [
            '/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM',
            '/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2_ext1-v1/MINIAODSIM',
            '/TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v3/MINIAODSIM'                        ,
            '/ST_tW_antitop_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM'    ,
            '/ST_tW_top_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v2/MINIAODSIM'        ,
            '/ST_t-channel_top_4f_leptonDecays_13TeV-powheg-pythia8_TuneCUETP8M1/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM'    ,
            '/ST_t-channel_antitop_4f_leptonDecays_13TeV-powheg-pythia8_TuneCUETP8M1/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM',
            '/ST_s-channel_4f_leptonDecays_13TeV-amcatnlo-pythia8_TuneCUETP8M1/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM'      ,
            '/DYJetsToLL_M-10to50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM'       ,
            '/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM'           ,
            '/DYJetsToLL_M-50_HT-100to200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM',
            '/DYJetsToLL_M-50_HT-200to400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM',
            '/DYJetsToLL_M-50_HT-400to600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v2/MINIAODSIM',
            '/DYJetsToLL_M-50_HT-600toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM',
            '/WW_TuneCUETP8M1_13TeV-pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM',
            '/WZ_TuneCUETP8M1_13TeV-pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM',
            '/ZZ_TuneCUETP8M1_13TeV-pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM',
            '/WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM'             ,
            '/WJetsToLNu_HT-100To200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM'  ,
            '/WJetsToLNu_HT-200To400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM'  ,
            '/WJetsToLNu_HT-400To600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM'  ,
            '/WJetsToLNu_HT-600To800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM'  ,
            '/WJetsToLNu_HT-800To1200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM' ,
            '/WJetsToLNu_HT-1200To2500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM',
            '/WJetsToLNu_HT-2500ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM' ,
            ]           

        # Merge MC and Data Dataset lists
        self.AllDatasets_MiniAODv2.extend(self.McDatasets_MiniAODv2)
        self.AllDatasets_MiniAODv2.extend(self.DataDatasets_MiniAODv2)

        # For-loop: All MC datasets
        for dataset in self.McDatasets_MiniAODv2:
            self.DatasetObjects_MiniAODv2.append( Dataset( dataset) )

        # For-loop: All Data datasets
        for dataset in self.DataDatasets_MiniAODv2:
            self.Print(["This is still under construction. Need to decide how to assign lumiMask to each dataset. EXIT"])
            exit(0)
            self.DatasetObjects_MiniAODv2.append( Dataset( dataset, dataVersion="74Xdata", lumiMask=lumiMask25ns) )
            self.DatasetObjects_MiniAODv2.append( Dataset( dataset, dataVersion="74Xdata", lumiMask=lumiMask25nsSilver) )
            self.DatasetObjects_MiniAODv2.append( Dataset( dataset, dataVersion="74Xdata", lumiMask=lumiMask25nsSilver) )
        return


    def GetDatasetObject(self, dataset):
        '''
        '''
        self.DebugMode()

        for d in self.DatasetObjects_MiniAODv2:
            if d.DAS == dataset:
                return d
        raise Exception("The dataset '%s' is not valid. Please select one of the following options:\n\t%s" % (dataset, "\n\t".join(self.AllDatasets_MiniAODv2)) )
    

#    def CreateDatasetObjectLists(self):
#        '''
#        '''
#        self.DebugMode()
#        
#        self.McDatasets_MiniAODv2_Top.append(GetDatasetObject('/TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v3/MINIAODSIM'                        ) )
#        self.McDatasets_MiniAODv2_Top.append(GetDatasetObject('/ST_tW_antitop_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM'    ) )
#        self.McDatasets_MiniAODv2_Top.append(GetDatasetObject('/ST_tW_top_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v2/MINIAODSIM'        ) )
#        self.McDatasets_MiniAODv2_Top.append(GetDatasetObject('/ST_t-channel_top_4f_leptonDecays_13TeV-powheg-pythia8_TuneCUETP8M1/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM'    ) )
#        self.McDatasets_MiniAODv2_Top.append(GetDatasetObject('/ST_t-channel_antitop_4f_leptonDecays_13TeV-powheg-pythia8_TuneCUETP8M1/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM') )
#        self.McDatasets_MiniAODv2_Top.append(GetDatasetObject('/ST_s-channel_4f_leptonDecays_13TeV-amcatnlo-pythia8_TuneCUETP8M1/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM'      ) )
#
#        
#            GetDatasetObject('/DYJetsToLL_M-10to50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM'       ) )
#            GetDatasetObject('/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM'           ) )
#            GetDatasetObject('/DYJetsToLL_M-50_HT-100to200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM') )
#            GetDatasetObject('/DYJetsToLL_M-50_HT-200to400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM') )
#            GetDatasetObject('/DYJetsToLL_M-50_HT-400to600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v2/MINIAODSIM') )
#            GetDatasetObject('/DYJetsToLL_M-50_HT-600toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM') )
#            GetDatasetObject('/WW_TuneCUETP8M1_13TeV-pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM') )
#            GetDatasetObject('/WZ_TuneCUETP8M1_13TeV-pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM') )
#            GetDatasetObject('/ZZ_TuneCUETP8M1_13TeV-pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM') )
#            GetDatasetObject('/WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM'             ) )
#            GetDatasetObject('/WJetsToLNu_HT-100To200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM'  ) )
#            GetDatasetObject('/WJetsToLNu_HT-200To400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM'  ) )
#            GetDatasetObject('/WJetsToLNu_HT-400To600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM'  ) )
#            GetDatasetObject('/WJetsToLNu_HT-600To800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM'  ) )
#            GetDatasetObject('/WJetsToLNu_HT-800To1200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM' ) )
#            GetDatasetObject('/WJetsToLNu_HT-1200To2500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM') )
#            GetDatasetObject('/WJetsToLNu_HT-2500ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM' ) )
#
#        return
