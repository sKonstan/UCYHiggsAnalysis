#!/usr/bin/env python
from UCYHiggsAnalysis.NtupleAnalysis.main import PSet
# import UCYHiggsAnalysis.NtupleAnalysis.parameters.scaleFactors as scaleFactors


#================================================================================================  
# General parameters
#================================================================================================  
histoLevel = "Debug"  #[Systematics, Vital, Informative, Debug]


#================================================================================================  
# Trigger
#================================================================================================  
# No need to specify version numbers, they are automatically scanned in range 1--100 (remove the '_v' suffix)
trigger = PSet(
    triggerOR = ["HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ",
                 "HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ",
                 "HLT_IsoMu20",
                 "HLT_IsoTkMu20",
                 "HLT_Ele17_Ele12_CaloIdL_TrackIdL_IsoVL_DZ",
                 "HLT_Ele23_WPLoose_Gsf",
                 "HLT_Mu17_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL",
                 "HLT_Mu8_TrkIsoVVL_Ele17_CaloIdL_TrackIdL_IsoVL",
                 "HLT_DiMu9_Ele9_CaloIdL_TrackIdL",
                 "HLT_Mu8_DiEle12_CaloIdL_TrackIdL",
                 "HLT_TripleMu_12_10_5",
                 "HLT_Ele16_Ele12_Ele8_CaloIdL_TrackIdL",
                 ],
    triggerOR2 = [],
    )


#================================================================================================  
# MET filter
#================================================================================================  
metFilter = PSet(
    discriminators = ["hbheNoiseTokenRun2Loose", # Loose is recommended
                      "hbheIsoNoiseToken",       # under scrutiny
                      "Flag_CSCTightHaloFilter",
                      "Flag_eeBadScFilter",
                      "Flag_goodVertices"]
    )


#================================================================================================  
# Electron selection
#================================================================================================  
electronSelection = PSet(
    PtCut         = 7.0,
    EtaCut        = 2.5,
    RelIsolString = "loose", # [veto, none, loose, medium, tight]
    electronID    = "mvaEleID_PHYS14_PU20bx25_nonTrig_V1_wp90", # [?]
)


#================================================================================================  
# Muon selection
#================================================================================================  
muonSelection = PSet(
    PtCut         = 5.0,
    EtaCut        = 2.4,
    RelIsolString = "loose",      # [veto, none, loose, medium, tight ]
    muonID        = "muIDMedium", # [muIDLoose, muIDMedium, muIDTight ]
)


#================================================================================================  
# Tau selection
#================================================================================================  
tauSelection = PSet(
    TrgMatch    = False,
    TrgDeltaR   =   0.1, # DeltaR for matching offline tau with trigger tau
    PtCut       =  20.0,
    EtaCut      =   2.4, # 2.1
    LdgTrkPtCut =   5.0,
    Nprongs     =  -1,   # [1, 2, 3, 12, 13, 23, 123 or -1 (all) ]
    Rtau        =   0.0, # [0.0 to 1.0 (to disable set to 0.0)   ]
    againstElectronDiscr = "againstElectronLooseMVA5",  # [againstElectronVLooseMVA5, againstElectronMediumMVA5, againstElectronTightMVA5]
    againstMuonDiscr     = "againstMuonLoose3",         # [againstMuonLoose3, againstMuonTight3]
    isolationDiscr       = "byLooseCombinedIsolationDeltaBetaCorr3Hits", # [byLoose..., byMedium..., byTight...]
  )

# # tau misidentification scale factors
# scaleFactors.assignTauMisidentificationSF(tauSelection, "eToTau", "full", "nominal")
# scaleFactors.assignTauMisidentificationSF(tauSelection, "muToTau", "full", "nominal")
# scaleFactors.assignTauMisidentificationSF(tauSelection, "jetToTau", "full", "nominal")
# # tau trigger SF
# scaleFactors.assignTauTriggerSF(tauSelection, "nominal")



#================================================================================================  
# Jet selection
#================================================================================================  
jetSelection = PSet(
    PtCut             = 20.0,
    EtaCut            =  2.5, 
    TauMatchDeltaR    =  0.4,         # FIXME: Should i remove this? Is tau-jet included in SelectedJets?
    NJetsCutValue     =  3,
    NJetsCutDirection = ">=",         # [==, !=, <, <=, >, >=]
    jetType           = "PFCHSJets", # [PFCHSJets, PuppiJets] 
    #jetType           = "Jets",       # obsolete with new Ntuples
    jetIDDiscr        = "IDtight",    # [IDloose, IDtight, IDtightLeptonVeto]
    jetPUIDDiscr      = "",           # [does not work at the moment]
)

 
#================================================================================================  
# B-jet selection (Jets passing the "jetSelection" PSets are checked if they can be b-tagged)
#================================================================================================  
bjetSelection = PSet(
    NJetsCutValue         = 1,
    NJetsCutDirection     = ">=",  #[==, !=, <, <=, >, >=]
    BjetDiscr             = "pfCombinedInclusiveSecondaryVertexV2BJetTags",
    BjetDiscrWorkingPoint = "Loose",
)


#================================================================================================  
# MET selection
#================================================================================================  
metSelection = PSet(
    METCutValue                 = 70.0,
    METCutDirection             = ">=",        # [==, !=, <, <=, >, >=]
    METSignificanceCutValue     = -1000.0,
    METSignificanceCutDirection = ">",         # [==, !=, <, <=, >, >=]
    METType                     = "MET_Type1", # [MET_Type1, MET_Type1_NoHF, MET_Puppi, GenMET, L1MET, HLTMET, CaloMET]
    PhiCorrections              = False        # [FIXME: no effect yet]
)
# MET trigger SF
# scaleFactors.assignMETTriggerSF(metSelection, bjetSelection.bjetDiscrWorkingPoint, "nominal")


#================================================================================================  
# Common plots options
#================================================================================================  
commonPlots = PSet(
    # histogramSplitting = [PSet(label="tauPt", binLowEdges=[60, 70, 80, 100, 120], useAbsoluteValues=False)],
    histogramSplitting = [],
    # Bin settings (final bin setting done in datacardGenerator, there also variable bin width is supported)
    NVerticesBins = PSet(nBins=60, axisMin= 0.0, axisMax= 60.0),
    PtBins        = PSet(nBins=50, axisMin= 0.0, axisMax=500.0),
    EtaBins       = PSet(nBins=60, axisMin=-3.0, axisMax=  3.0),
    PhiBins       = PSet(nBins=72, axisMin=-3.1415926, axisMax=3.1415926),
    RtauBins      = PSet(nBins=55, axisMin= 0.0, axisMax=  1.1),
    NJetsBins     = PSet(nBins=20, axisMin= 0.0, axisMax= 20.0),
    MetBins       = PSet(nBins=80, axisMin= 0.0, axisMax=800.0),
    BjetDiscrBins = PSet(nBins=20, axisMin=-1.0, axisMax=  1.0),
    enablePUDependencyPlots = True,
)


#================================================================================================  
# Create the PSet with all selections
#================================================================================================  
ttbarSelections = PSet(
    histogramAmbientLevel = histoLevel,
    Trigger               = trigger,
    METFilter             = metFilter,
    ElectronSelection     = electronSelection,
    MuonSelection         = muonSelection,
    TauSelection          = tauSelection,
    JetSelection          = jetSelection,
    BJetSelection         = bjetSelection,
    METSelection          = metSelection,
    CommonPlots           = commonPlots,
)
