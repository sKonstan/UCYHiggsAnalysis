#================================================================================================
# Configuration file for creating a FlatTree from a miniAOD file for analysis in ttH -> multileptons
# For miniAOD instructions see: https://twiki.cern.ch/twiki/bin/view/CMSPublic/WorkBookMiniAOD2015 
#================================================================================================
import FWCore.ParameterSet.Config as cms
import HiggsAnalysis.MiniAOD2FlatTree.tools.git as git
from HiggsAnalysis.MiniAOD2FlatTree.tools.dataOptions import getOptionsDataVersion

process = cms.Process("SkimFile")

#================================================================================================
# Options
#================================================================================================
bDebug        = False
iMaxEvents    = 1000
iReportEvery  = 10

#================================================================================================
# For debugging purposes (Tells user what cmsRun is accessing) 
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
import HiggsAnalysis.MiniAOD2FlatTree.tools.datasetsHelper as datasetsHelper
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(iMaxEvents) )
process.source    = cms.Source("PoolSource",
                               fileNames = datasetsHelper.GetEosRootFilesForDataset("RunIISpring15DR74_ttHJetToNonbb_M125_13TeV_MINIAODSIM"),
)

process.filter = cms.EDFilter('EventFilter')


process.output = cms.OutputModule("PoolOutputModule",
                                  outputCommands = cms.untracked.vstring(
        "keep *",
        ),
                                  fileName = cms.untracked.string("EventFilter.root")
                                  #fileName = cms.untracked.string(process.source.fileNames[0] + "_EventFilter")
                                  )
process.out_step = cms.EndPath(process.output)


#===============================================================================================
# Module Execution
#================================================================================================
process.eventFilter = cms.Path(process.filter)
process.outpath     = cms.EndPath(process.output)

#process.runEDAnalyzer = cms.Path(process.skim)
#process.runEDFilter = cms.Path(process.dump)
