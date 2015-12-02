import FWCore.ParameterSet.Config as cms

Muons = cms.VPSet(
    cms.PSet(
        branchName     = cms.untracked.string("Muons"),
        src            = cms.InputTag("slimmedMuons"),
        debugMode      = cms.untracked.bool(False),
        discriminators = cms.vstring()
    )
)
