#!/usr/bin/env python
from UCYHiggsAnalysis.NtupleAnalysis.main import PSet
# import UCYHiggsAnalysis.NtupleAnalysis.parameters.scaleFactors as scaleFactors


#================================================================================================  
# General parameters
#================================================================================================  
histoLevel = "Debug"  # Options: Systematics, Vital, Informative, Debug


#================================================================================================  
# Trigger
#================================================================================================  
# No need to specify version numbers, they are automatically scanned in range 1--100 (remove the '_v' suffix)
trg = PSet(
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
    RelIsolString = "tight", # (options: veto, none, loose, medium, tight)
    electronID    = "mvaEleID_PHYS14_PU20bx25_nonTrig_V1_wp90", # (options: ?)

)


#================================================================================================  
# Muon selection
#================================================================================================  
muonSelection = PSet(
    PtCut         = 5.0,
    EtaCut        = 2.4,
    RelIsolString = "tight",     # [options: veto, none, loose, medium, tight ]
    muonID        = "muIDTight", # [options: muIDLoose, muIDMedium, muIDTight ]
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
    Nprongs     =  -1,   # [options: 1, 2, 3, 12, 13, 23, 123 or -1 (all) ]
    Rtau        =   0.0, # [options: 0.0 to 1.0 (to disable set to 0.0)   ]
    againstElectronDiscr = "againstElectronTightMVA5",  # [options: againstElectronVLooseMVA5, againstElectronMediumMVA5, againstElectronTightMVA5]
    againstMuonDiscr     = "againstMuonTight3",         # [options: againstMuonLoose3, againstMuonTight3]
    isolationDiscr       = "byLooseCombinedIsolationDeltaBetaCorr3Hits", # [options: 'byLoose..., byMedium..., byTight...]
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
               jetType = "Jets", # options: Jets (AK4PFCHS), JetsPuppi (AK4Puppi)
              jetPtCut = 30.0,
             jetEtaCut = 2.5,
     tauMatchingDeltaR = 0.4,
  numberOfJetsCutValue = 3,
  numberOfJetsCutDirection = ">=", # options: ==, !=, <, <=, >, >=
            jetIDDiscr = "IDtight", # options: IDloose, IDtight, IDtightLeptonVeto
          jetPUIDDiscr = "", # does not work at the moment 
)

 
#================================================================================================  
# B-jet selection
#================================================================================================  
bjetSelection = PSet(
             #bjetDiscr = "combinedInclusiveSecondaryVertexV2BJetTags",
             bjetDiscr = "pfCombinedInclusiveSecondaryVertexV2BJetTags",
 bjetDiscrWorkingPoint = "Loose",
 numberOfBJetsCutValue = 1,
 numberOfBJetsCutDirection = ">=", # options: ==, !=, <, <=, >, >=
)

#================================================================================================  
# MET selection
#================================================================================================  
metSelection = PSet(
           METCutValue = 120.0,
       METCutDirection = ">", # options: ==, !=, <, <=, >, >=
  METSignificanceCutValue = -1000.0,
  METSignificanceCutDirection = ">", # options: ==, !=, <, <=, >, >=
               METType = "MET_Type1", # options: MET_Type1, MET_Type1_NoHF, MET_Puppi, GenMET, L1MET, HLTMET, CaloMET
   applyPhiCorrections = False  # FIXME: no effect yet
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
       nVerticesBins = PSet(nBins=60, axisMin=0., axisMax=60.),
              ptBins = PSet(nBins=50, axisMin=0., axisMax=500.),
             etaBins = PSet(nBins=60, axisMin=-3.0, axisMax=3.0),
             phiBins = PSet(nBins=72, axisMin=-3.1415926, axisMax=3.1415926),
            rtauBins = PSet(nBins=55, axisMin=0., axisMax=1.1),
           njetsBins = PSet(nBins=20, axisMin=0., axisMax=20.),
             metBins = PSet(nBins=80, axisMin=0., axisMax=800.),
       bjetDiscrBins = PSet(nBins=20, axisMin=-1.0, axisMax=1.0),
  enablePUDependencyPlots = True,
)


#================================================================================================  
# Create the PSet with all selections
#================================================================================================  
allSelections = PSet(
 histogramAmbientLevel = histoLevel,
               Trigger = trg,
             METFilter = metFilter,
     ElectronSelection = electronSelection,
         MuonSelection = muonSelection,
          TauSelection = tauSelection,
          JetSelection = jetSelection,
         BJetSelection = bjetSelection,
          METSelection = metSelection,
           CommonPlots = commonPlots,
)
