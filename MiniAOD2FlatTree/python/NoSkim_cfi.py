import FWCore.ParameterSet.Config as cms

skim = cms.EDFilter("AnalysisSkim",
                    TriggerResults = cms.InputTag("TriggerResults::HLT"),
                    HLTPaths       = cms.vstring(""),
                    JetCollection  = cms.InputTag("slimmedJets"),
                    JetUserFloats  = cms.vstring("pileupJetId:fullDiscriminant"),
                    JetEtCut       = cms.double(0.0),
                    JetEtaCut      = cms.double(99999.9),
                    NJets          = cms.int32(0),
                    debugMode      = cms.bool(False)
                    )
