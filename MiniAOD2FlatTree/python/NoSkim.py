import FWCore.ParameterSet.Config as cms

skim = cms.EDFilter("AnalysisSkim",
                    TriggerResults = cms.InputTag("TriggerResults::HLT"),
                    HLTPaths       = cms.vstring(
        "HLT_LooseIsoPFTau50_Trk30_eta2p1_MET80_JetIdCleaned_v",
        "HLT_Mu8_v",
        "HLT_Mu17_v",
        ),
                    JetCollection  = cms.InputTag("slimmedJets"),
                    JetUserFloats  = cms.vstring(
	"pileupJetId:fullDiscriminant",
        ),
                    JetEtCut       = cms.double(0.0),
                    JetEtaCut      = cms.double(9999.9),
                    NJets          = cms.int32(0),
                    debugMode      = cms.bool(False)
                    )
