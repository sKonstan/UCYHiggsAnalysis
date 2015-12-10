import FWCore.ParameterSet.Config as cms

PUInfo = cms.EDAnalyzer('PUInfo',
                        OutputFileName       = cms.string("PileUp.root"),
                        PileupSummaryInfoSrc = cms.InputTag("slimmedAddPileupInfo"), #"addPileupInfo"
                        debugMode            = cms.untracked.bool(False)
                        )
