import FWCore.ParameterSet.Config as cms

skim = cms.EDFilter("AnalysisSkim",
                    TriggerResults = cms.InputTag("TriggerResults::HLT"),
                    HLTPaths       = cms.vstring(
        "HLT_Ele17_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_v*",
        "HLT_Ele23_WPLoose_Gsf_v*", #"HLT_BIT_HLT_Ele23_WPLoose_Gsf_v*"
        "HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_v*",
        "HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ_v*",
        "HLT_IsoMu20_v*", #"HLT_BIT_IsoMu20_v*"
        "HLT_IsoTkMu20_v*",
        "HLT_Mu17_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_v",
        "HLT_Mu8_TrkIsoVVL_Ele17_CaloIdL_TrackIdL_IsoVL_v",
        "HLT_Ele23_WPLoose_Gsf_v*", # Only Data in 74X, both Data and MC in 76X
        # Not used by ttH-leptonic (?)
        "HLT_Ele23_CaloIdL_TrackIdL_IsoVL_v", #MC
        "HLT_DiMu9_Ele9_CaloIdL_TrackIdL_v",
        "HLT_Mu8_DiEle12_CaloIdL_TrackIdL_v",
        "HLT_TripleMu_12_10_5_v",
        "HLT_Ele16_Ele12_Ele8_CaloIdL_TrackIdL_v",
        ),
                    JetCollection  = cms.InputTag("slimmedJets"),
                    JetUserFloats  = cms.vstring(
	"pileupJetId:fullDiscriminant",
        ),
                    JetEtCut       = cms.double(0.0),    # 20.0
                    JetEtaCut      = cms.double(9999.9), #  2.4
                    NJets          = cms.int32(0),       #  0
                    debugMode      = cms.bool(False)     # False
                    )
