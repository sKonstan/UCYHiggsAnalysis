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
bDebug           = False #Default is "False"
bSummary         = False #Default is "False"
bDependencies    = False #Default is "False" 
bDumpCollections = False #Default is "False"

skimType     = "DefaultSkim" #None #"Trigger"
dataVersion  = "74Xmc" #"74Xdata"
dataset      = "RunIISpring15MiniAODv2_ttHJetToNonbb_M125_13TeV_MINIAODSIM"
# dataset      = "RunIISpring15MiniAODv2_TTWJetsToLNu_TuneCUETP8M1_13TeV_MINIAODSIM"
# dataset      = "RunIISpring15MiniAODv2_TTZToLLNuNu_M-10_TuneCUETP8M1_13TeV_MINIAODSIM"
# dataset      = "RunIISpring15MiniAODv2_TTJets_TuneCUETP8M1_13TeV_MINIAODSIM"
# dataset      = "RunIISpring15MiniAODv2_DYJetsToLL_M-10to50_TuneCUETP8M1_13TeV_MINIAODSIM"
# dataset      = "RunIISpring15MiniAODv2_DYJetsToLL_M-50_TuneCUETP8M1_13TeV_MINIAODSIM"
# dataset      = "RunIISpring15MiniAODv2_ZZ_TuneCUETP8M1_13TeV_MINIAODSIM"
# dataset      = "RunIISpring15MiniAODv2_WZ_TuneCUETP8M1_13TeV_MINIAODSIM"
# dataset      = "RunIISpring15MiniAODv2_ST_tW_top_5f_inclusiveDecays_13TeV_MINIAODSIM"
# dataset      = "RunIISpring15MiniAODv2_ST_tW_antitop_5f_inclusiveDecays_13TeV_MINIAODSIM"
# dataset      = "RunIISpring15MiniAODv2_ST_s-channel_4f_leptonDecays_13TeV-MINIAODSIM"
iMaxEvents   = 100 #10000
iReportEvery = 10


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
# Get Dataset version and options. Inform use of dataVersion configurations
#================================================================================================
options, dataVersion = getOptionsDataVersion(dataVersion)
dataVersion.PrintConfig()


#================================================================================================
# Message Logger
#================================================================================================
process.load("FWCore/MessageService/MessageLogger_cfi")
process.MessageLogger.cerr.FwkReport.reportEvery = iReportEvery


#================================================================================================
# Define the input files 
#================================================================================================
import UCYHiggsAnalysis.MiniAOD2FlatTree.tools.datasetsHelper as datasetsHelper
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(iMaxEvents) )
process.source    = cms.Source("PoolSource", fileNames = datasetsHelper.GetEosRootFilesForDataset(dataset) )


#================================================================================================
# Global Tag
#================================================================================================
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_condDBv2_cff')
from Configuration.AlCa.GlobalTag_condDBv2 import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, str(dataVersion.getGlobalTag()), '')
print "=== runMiniAOD2FlatTree_cfg.py:\n\t GlobalTag = \"%s\"" % (dataVersion.getGlobalTag())


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
                                    "HLT_Ele22_eta2p1_WPTight_Gsf_v",
                                    "HLT_Ele22_eta2p1_WP75_Gsf_v",
                                    "HLT_Ele22_eta2p1_WPLoose_Gsf_v",
                                    "HLT_IsoMu17_eta2p1_v",
                                    "HLT_IsoMu18_v",
                                    "HLT_IsoMu20_v",
                                    "HLT_IsoMu20_eta2p1_v",
                                    "HLT_Mu8_v",
                                    "HLT_Mu17_v",
                                    "HLT_Mu24_v",
                                    "HLT_Mu34_v",
                                    "HLT_Dimuon13_PsiPrime_v",
                                    "HLT_Dimuon13_Upsilon_v",
                                    "HLT_Dimuon20_Jpsi_v",
                                    "HLT_Dimuon16_Jpsi_v",
                                    "HLT_Dimuon10_Jpsi_Barrel_v",
                                    "HLT_Dimuon8_PsiPrime_Barrel_v",
                                    "HLT_Dimuon8_Upsilon_Barrel_v",
                                    "HLT_Dimuon0_Phi_Barrel_v",
                                    ),
	                        L1Extra        = cms.InputTag("l1extraParticles:MET"),
	                        TriggerObjects = cms.InputTag("selectedPatTrigger"),
                                TriggerMatch   = cms.untracked.vstring(
                                    "LooseIsoPFTau50_Trk30_eta2p1",
                                ),
                                debugMode      = cms.untracked.bool(bDebug),
	                        filter         = cms.untracked.bool(False) #filter according to trigger bits
                            ),

                            METNoiseFilter = cms.PSet(
                                triggerResults            = cms.InputTag(TrgResultsSource),
                                printTriggerResultsList   = cms.untracked.bool(True),
                                debugMode                 = cms.untracked.bool(bDebug),
                                filtersFromTriggerResults = cms.vstring(
                                    "Flag_CSCTightHaloFilter",
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
                                    branchName = cms.untracked.string("GenWeights"),
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
if (skimType == "Trigger"):
    process.runEDFilter = cms.Path(process.PUInfo * process.skimCounterAll * process.skim * process.skimCounterPassed * process.CustomisationsSequence * process.dump)
else:
    process.runEDFilter = cms.Path(process.CustomisationsSequence * process.dump)


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
