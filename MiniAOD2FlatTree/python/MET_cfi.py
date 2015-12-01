import FWCore.ParameterSet.Config as cms

METs = cms.VPSet(
    cms.PSet(
        branchName = cms.untracked.string("MET_Type1"),
        src        = cms.InputTag("slimmedMETs"),
        debugMode  = cms.untracked.bool(True)
    ),
    cms.PSet(
        branchName = cms.untracked.string("MET_Type1_NoHF"),
        src        = cms.InputTag("slimmedMETsNoHF"),
        debugMode  = cms.untracked.bool(True)
    ),
    cms.PSet(
        branchName = cms.untracked.string("MET_Puppi"),
        src        = cms.InputTag("slimmedMETsPuppi"),
        debugMode  = cms.untracked.bool(True)
    ),
)
