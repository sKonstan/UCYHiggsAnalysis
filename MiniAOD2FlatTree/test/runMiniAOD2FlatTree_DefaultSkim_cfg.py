#================================================================================================
# Configuration file for creating a FlatTree from a miniAOD file for analysis in ttH -> multileptons
# For miniAOD instructions see: https://twiki.cern.ch/twiki/bin/view/CMSPublic/WorkBookMiniAOD2015 
#================================================================================================
import FWCore.ParameterSet.Config as cms
import UCYHiggsAnalysis.MiniAOD2FlatTree.tools.git as git
from UCYHiggsAnalysis.MiniAOD2FlatTree.tools.dataOptions import getOptionsDataVersion

#================================================================================================
# Options
#================================================================================================
bSummary         = False #Default is "False"
bDependencies    = False #Default is "False" 
bDumpCollections = False #Default is "False"
iMaxEvents       = 10000
iReportEvery     = 10
skimType         = "NoSkim" #"NoSkim #"Trigger" #"DefaultSkim"
dataset          = "/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM"
#dataset          = "/TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v3/MINIAODSIM"
#dataset          = "/DYJetsToLL_M-10to50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM"
#dataset          = "/WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM"
#dataset          = "/DoubleMuon/Run2015D-PromptReco-v4/MINIAOD"

# For Debugging Purposes:
bDebug      = False   #Default is "False"
RunNum_1    = 1       #Default is "None"
LumiBlock_1 = 2       #Default is "None"
EvtNum_1    = 240     #Default is "None" 
RunNum_2    = 1       #Default is "None"
LumiBlock_2 = 2       #Default is "None"
EvtNum_2    = 260     #Default is "None"

#================================================================================================
# Setup the process
#================================================================================================
process         = cms.Process("MiniAOD2FlatTree")
process.options = cms.untracked.PSet(
    SkipEvent         = cms.untracked.vstring('ProductNotFound'),
    wantSummary       = cms.untracked.bool(bSummary),
    printDependencies = cms.untracked.bool(bDependencies),
)


#================================================================================================
# Tracer service is for debugging purposes (Tells user what cmsRun is accessing) 
#================================================================================================
if (bDebug):
    process.Tracer = cms.Service("Tracer")


#================================================================================================
# Message Logger
#================================================================================================
process.load("FWCore/MessageService/MessageLogger_cfi")
process.MessageLogger.cerr.FwkReport.reportEvery = iReportEvery


#================================================================================================
# Define the input files 
#================================================================================================
import UCYHiggsAnalysis.MiniAOD2FlatTree.tools.datasets as datasets
myDatasets = datasets.Datasets(False)
if (bDebug):
    print "=== runMiniAOD2FlatTree_DefaultSkim_cfg.py:\n\t ", myDatasets.GetDatasetObject(dataset).fileList

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(iMaxEvents) )
process.source    = cms.Source("PoolSource",
                               fileNames       = myDatasets.GetDatasetObject(dataset).fileList,
                               #fileNames = cms.untracked.vstring("/store/mc/RunIISpring15MiniAODv2/WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/40000/90A2FB38-586D-E511-B2EF-0025905B85AA.root"),
                               #eventsToProcess = cms.untracked.VEventRange('%s:%s:%s-%s:%s:%s' % (RunNum_1, LumiBlock_1, EvtNum_1, RunNum_2, LumiBlock_2, EvtNum_2) ),
                               )

#================================================================================================
# Get Dataset version and options. Inform use of dataVersion configurations
#================================================================================================
options, dataVersion = getOptionsDataVersion( myDatasets.GetDatasetObject(dataset), useDefaultSignalTrigger=True, bDebug=bDebug)
dataVersion.PrintConfig()


#================================================================================================
# Global Tag
#================================================================================================
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_condDBv2_cff')
from Configuration.AlCa.GlobalTag_condDBv2 import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, str(dataVersion.getGlobalTag()), '')
if (bDebug):
    print "=== runMiniAOD2FlatTree_DefaultSkim_cfg.py:\n\t GlobalTag = \"%s\"" % (dataVersion.getGlobalTag())


#================================================================================================
# Set up Flat-Tree dumper
#================================================================================================
process.load("UCYHiggsAnalysis/MiniAOD2FlatTree/Electron_cfi")
process.load("UCYHiggsAnalysis/MiniAOD2FlatTree/Jet_cfi")
process.load("UCYHiggsAnalysis/MiniAOD2FlatTree/MET_cfi")
process.load("UCYHiggsAnalysis/MiniAOD2FlatTree/Muon_cfi")
process.load("UCYHiggsAnalysis/MiniAOD2FlatTree/PUInfo_cfi") 
process.load("UCYHiggsAnalysis/MiniAOD2FlatTree/Tau_cfi")

### Fixme
TrgResultsSource = "TriggerResults::PAT"
if dataVersion.isData():
    TrgResultsSource = "TriggerResults::RECO"
if (bDebug):
    print "=== runMiniAOD2FlatTree_cfg.py:\n\t Trigger source has been set to \"%s\"" % (TrgResultsSource)


process.dump = cms.EDFilter('MiniAOD2FlatTreeFilter',
                            OutputFileName      = cms.string("miniAOD2FlatTree.root"),
                            PUInfoInputFileName = process.PUInfo.OutputFileName,
                            CodeVersion         = cms.string(git.getCommitId()),
                            DataVersion         = cms.string(str(dataVersion.version)),
                            CMEnergy            = cms.int32(13),
                            Skim                = cms.PSet(
                                Counters = cms.VInputTag( #the counters are read from lumiblock1 instead of events!
	                            "skimCounterAll",
                                    "skimCounterPassed"
                                ),
                            ),

                            EventInfo = cms.PSet(
                                PileupSummaryInfoSrc    = process.PUInfo.PileupSummaryInfoSrc, 
	                        LHESrc                  = cms.untracked.InputTag("externalLHEProducer"),
	                        OfflinePrimaryVertexSrc = cms.InputTag("offlineSlimmedPrimaryVertices"),
                                branchName              = cms.untracked.string("EventInfo"),
                                debugMode               = cms.untracked.bool(bDebug)
                            ),
                            
                            Trigger = cms.PSet(
	                        TriggerResults = cms.InputTag("TriggerResults::HLT"),
	                        TriggerBits    = cms.vstring(
            "HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_v",
            "HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ_v",            
            "HLT_IsoMu20_v",
            "HLT_IsoTkMu20_v",
            "HLT_Ele17_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_v",
            "HLT_Ele23_WPLoose_Gsf_v",
            "HLT_Ele23_CaloIdL_TrackIdL_IsoVL_v", #MC
            "HLT_Mu17_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_v",
            "HLT_Mu8_TrkIsoVVL_Ele17_CaloIdL_TrackIdL_IsoVL_v",
            "HLT_DiMu9_Ele9_CaloIdL_TrackIdL_v",
            "HLT_Mu8_DiEle12_CaloIdL_TrackIdL_v",
            "HLT_TripleMu_12_10_5_v",
            "HLT_Ele16_Ele12_Ele8_CaloIdL_TrackIdL_v",
            ),
	                        L1Extra        = cms.InputTag("l1extraParticles:MET"),
	                        TriggerObjects = cms.InputTag("selectedPatTrigger"),
                                TriggerMatch   = cms.untracked.vstring(
            "HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_v",
            "HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ_v",            
            "HLT_IsoMu20_v",
            "HLT_IsoTkMu20_v",
            "HLT_Ele17_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_v",
            "HLT_Ele23_WPLoose_Gsf_v",
            "HLT_Ele23_CaloIdL_TrackIdL_IsoVL_v", #MC
            "HLT_Mu17_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_v",
            "HLT_Mu8_TrkIsoVVL_Ele17_CaloIdL_TrackIdL_IsoVL_v",
            "HLT_DiMu9_Ele9_CaloIdL_TrackIdL_v",
            "HLT_Mu8_DiEle12_CaloIdL_TrackIdL_v",
            "HLT_TripleMu_12_10_5_v",
            "HLT_Ele16_Ele12_Ele8_CaloIdL_TrackIdL_v",
            ),
                                debugMode      = cms.untracked.bool(bDebug),
	                        filter         = cms.untracked.bool(False) #filter according to trigger bits
                            ),

                            METNoiseFilter = cms.PSet(
                                branchName                = cms.untracked.string("METFilter"),
                                triggerResults            = cms.InputTag(TrgResultsSource),
                                printTriggerResultsList   = cms.untracked.bool(False),
                                debugMode                 = cms.untracked.bool(bDebug),
                                filtersFromTriggerResults = cms.vstring(
            #"Flag_CSCTightHaloFilter", # HIP
            #"Flag_goodVertices",       # HIP
            #"Flag_eeBadScFilter",      # HIP
            "Flag_HBHENoiseFilter",
            "Flag_HBHENoiseIsoFilter",
            "Flag_CSCTightHaloFilter", #crash
            "Flag_goodVertices",
            "Flag_eeBadScFilter",
                                ),
                                hbheNoiseTokenRun2LooseSource = cms.InputTag('HBHENoiseFilterResultProducer','HBHENoiseFilterResultRun2Loose'),
                                hbheNoiseTokenRun2TightSource = cms.InputTag('HBHENoiseFilterResultProducer','HBHENoiseFilterResultRun2Tight'),
                                hbheIsoNoiseTokenSource       = cms.InputTag('HBHENoiseFilterResultProducer','HBHEIsoNoiseFilterResult'),
                            ),

                            # Imported from _cff.py files
                            Taus      = process.Taus,                             
                            Electrons = process.Electrons,
                            Muons     = process.Muons,
                            Jets      = process.Jets,
                            METs      = process.METs,

                            GenWeights = cms.VPSet(
                                cms.PSet(
                                    branchName = cms.untracked.string("GenWeight"),
                                    src        = cms.InputTag("generator"),
                                    debugMode  = cms.untracked.bool(bDebug),
                                    filter     = cms.untracked.bool(False)
                                )
                            ),
                            
                            GenJets = cms.VPSet(      
                                cms.PSet(
                                    branchName             = cms.untracked.string("GenJets"),
                                    src                    = cms.InputTag("slimmedGenJets"), # ak4 (anti-kT, R=0.4)
                                    debugMode              = cms.untracked.bool(bDebug),
                                    saveGenJetConstituents = cms.untracked.bool(False),
                                )
                            ),

                            GenParticles = cms.VPSet(      
                                cms.PSet(
                                    branchName          = cms.untracked.string("GenParticles"),
                                    src                 = cms.InputTag("prunedGenParticles"),
                                    debugMode           = cms.untracked.bool(bDebug),
                                    saveAllGenParticles = cms.untracked.bool(True),
                                    saveGenElectrons    = cms.untracked.bool(False),
                                    saveGenMuons        = cms.untracked.bool(False),
                                    saveGenTaus         = cms.untracked.bool(False),
                                    saveGenNeutrinos    = cms.untracked.bool(False)
                                )
                            ),

                            Tracks = cms.VPSet(
                                cms.PSet(
                                    branchName               = cms.untracked.string("PFcandidates"),
                                    src                      = cms.InputTag("packedPFCandidates"),
                                    OfflinePrimaryVertexSrc  = cms.InputTag("offlineSlimmedPrimaryVertices"),
                                    ptCut                    = cms.untracked.double(0.0), # pt < value [GeV/c]
                                    etaCut                   = cms.untracked.double(2.5), # abs(eta) < value
                                    IPvsPVz                  = cms.untracked.double(5),   # abs(IPz-PVz) < value
                                    saveOnlyChargedParticles = cms.untracked.bool(True),
                                    debugMode                = cms.untracked.bool(bDebug),
                                    )
                                ),

                            #GenMETs = cms.VPSet( #obsolete
                            #    cms.PSet(                                                                                                                                     
                            #        branchName = cms.untracked.string("GenMET"),
                            #        src        = cms.InputTag("genMetTrue"),
                            #        debugMode  = cms.untracked.bool(True),
                            #        filter     = cms.untracked.bool(False)
                            #    )                                                                                                               
                            #),
)


#================================================================================================
# Setup skim counters
#================================================================================================ 
if (skimType != None):
    process.load("UCYHiggsAnalysis.MiniAOD2FlatTree.%s_cfi" % (skimType))
process.skimCounterAll    = cms.EDProducer("EventCountProducer")
process.skimCounterPassed = cms.EDProducer("EventCountProducer")


#================================================================================================
# Setup customizations (produces process.CustomisationsSequence which needs to be included to path)
#================================================================================================
from UCYHiggsAnalysis.MiniAOD2FlatTree.CommonFragments import produceCustomisations
produceCustomisations(process)


#===============================================================================================
# Module Execution
#================================================================================================
process.runEDFilter = cms.Path(process.PUInfo * process.skimCounterAll * process.skim * process.skimCounterPassed * process.CustomisationsSequence * process.dump)


#===============================================================================================
# Dumps all the collections stored
# [EndPath defines group of modules which are to run after all other labelled Paths have been run]
#================================================================================================ 
if (bDumpCollections):
    process.output = cms.OutputModule("PoolOutputModule",
                                      outputCommands = cms.untracked.vstring("keep *", ),
                                      fileName       = cms.untracked.string("miniAOD.root")
                                      )
    process.out_step = cms.EndPath(process.output)
