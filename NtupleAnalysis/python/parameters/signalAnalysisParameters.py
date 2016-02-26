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
                      "hbheIsoNoiseToken", # under scrutiny
                      "Flag_CSCTightHaloFilter",
                      "Flag_eeBadScFilter",
                      "Flag_goodVertices"]
    )


#================================================================================================  
# Tau selection
#================================================================================================  
tauSelection = PSet(
  applyTriggerMatching = True,
   triggerMatchingCone = 0.1,   # DeltaR for matching offline tau with trigger tau
              tauPtCut = 60.0,
             tauEtaCut = 2.1,
        tauLdgTrkPtCut = 30.0,
                prongs = 123,    # options: 1, 2, 3, 12, 13, 23, 123 or -1 (all)
                  rtau = 0.0,   # to disable set to 0.0
  againstElectronDiscr = "againstElectronTightMVA5",
      againstMuonDiscr = "againstMuonTight3",
        isolationDiscr = "byLooseCombinedIsolationDeltaBetaCorr3Hits",
  
)

# # tau misidentification scale factors
# scaleFactors.assignTauMisidentificationSF(tauSelection, "eToTau", "full", "nominal")
# scaleFactors.assignTauMisidentificationSF(tauSelection, "muToTau", "full", "nominal")
# scaleFactors.assignTauMisidentificationSF(tauSelection, "jetToTau", "full", "nominal")
# # tau trigger SF
# scaleFactors.assignTauTriggerSF(tauSelection, "nominal")


#================================================================================================  
# Electron veto
#================================================================================================  
eVeto = PSet(
         electronPtCut = 15.0,
        electronEtaCut = 2.5,
            electronID = "mvaEleID_PHYS14_PU20bx25_nonTrig_V1_wp90", # highest (wp90) for vetoing (2012: wp95)
     electronIsolation = "veto", # loosest possible for vetoing ("veto"), "tight" for selecting
)


#================================================================================================  
# Muon veto
#================================================================================================  
muVeto = PSet(
             muonPtCut = 10.0,
            muonEtaCut = 2.5,
                muonID = "muIDLoose", # loosest option for vetoing (options: muIDLoose, muIDMedium, muIDTight)
         muonIsolation = "veto", # loosest possible for vetoing ("veto"), "tight" for selecting
)


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
commonPlotsOptions = PSet(
  # Splitting of histograms as function of one or more parameters
  # Example: histogramSplitting = [PSet(label="tauPt", binLowEdges=[60, 70, 80, 100, 120], useAbsoluteValues=False)],
  histogramSplitting = [],
  # By default, inclusive (i.e. fake tau+genuine tau) and fake tau histograms are produced. Set to true to also produce genuine tau histograms (Note: will slow down running and enlarge resulting files).
  enableGenuineTauHistograms = False, 
  # Bin settings (final bin setting done in datacardGenerator, there also variable bin width is supported)
       nVerticesBins = PSet(nBins=60, axisMin=0., axisMax=60.),
              ptBins = PSet(nBins=50, axisMin=0., axisMax=500.),
             etaBins = PSet(nBins=60, axisMin=-3.0, axisMax=3.0),
             phiBins = PSet(nBins=72, axisMin=-3.1415926, axisMax=3.1415926),
        deltaPhiBins = PSet(nBins=18, axisMin=0., axisMax=180.), # used in 2D plots, i.e. putting high number of bins here will cause troubles
            rtauBins = PSet(nBins=55, axisMin=0., axisMax=1.1),
           njetsBins = PSet(nBins=20, axisMin=0., axisMax=20.),
             metBins = PSet(nBins=80, axisMin=0., axisMax=800.),
       bjetDiscrBins = PSet(nBins=20, axisMin=-1.0, axisMax=1.0),
   angularCuts1DBins = PSet(nBins=52, axisMin=0., axisMax=260.),
         topMassBins = PSet(nBins=60, axisMin=0., axisMax=600.),
           WMassBins = PSet(nBins=60, axisMin=0., axisMax=300.),
              mtBins = PSet(nBins=160, axisMin=0., axisMax=800.), # 5 GeV bin width for tail fitter
         invmassBins = PSet(nBins=50, axisMin=0., axisMax=500.),
  # Enable/Disable some debug-level plots
  enablePUDependencyPlots = True,
)


#================================================================================================  
# Create the PSet with all selections
#================================================================================================  
allSelections = PSet(
 histogramAmbientLevel = histoLevel,
               Trigger = trg,
             METFilter = metFilter,
          TauSelection = tauSelection,
     ElectronSelection = eVeto,
         MuonSelection = muVeto,
          JetSelection = jetSelection,
         BJetSelection = bjetSelection,
          METSelection = metSelection,
           CommonPlots = commonPlotsOptions,
)
