#!/usr/bin/env python
from UCYHiggsAnalysis.NtupleAnalysis.main import PSet
import UCYHiggsAnalysis.NtupleAnalysis.parameters.scaleFactors as scaleFactors


#====== General parameters
histoLevel = "Debug"  # Options: Systematics, Vital, Informative, Debug

#====== Trigger
trg = PSet(
  # No need to specify version numbers, they are automatically scanned in range 1--100 (remove the '_v' suffix)
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


#====== MET filter
metFilter = PSet(
  discriminators = ["hbheNoiseTokenRun2Loose", # Loose is recommended
                    "hbheIsoNoiseToken", # under scrutiny
                    "Flag_CSCTightHaloFilter",
                    "Flag_eeBadScFilter",
                    "Flag_goodVertices"]
)

#====== Electron selection
electronSelection  = PSet(
    trigger_match  = False,
    trigger_dR     = 0.1,   # DeltaR for matching offline tau with trigger tau
    ptCut          = 7.0,
    etaCut         = 2.5,
    discriminators = ["Electrons_mvaEleID_PHYS14_PU20bx25_nonTrig_V1_wp80"]
    )

#====== Muon selection
muonSelection = PSet(
    trigger_match  = False,
    trigger_dR     = 0.1,   # DeltaR for matching offline tau with trigger tau
    ptCut          = 5.0,
    etaCut         = 2.4,
    discriminators = ["Muons_muIDLoose"]
    )


#====== Tau selection
tauSelection = PSet(
    trigger_match  = True,
    trigger_dR     = 0.1,   # DeltaR for matching offline tau with trigger tau
    ptCut          = 60.0,
    etaCut         = 2.1,
    tauLdgTrkPtCut = 30.0,
    prongs         = 123,    # options: 1, 2, 3, 12, 13, 23, 123 or -1 (all)
    electronDiscr  = "againstElectronTightMVA5",
    muonDiscr      = "againstMuonTight3",
    isolationDiscr = "byLooseCombinedIsolationDeltaBetaCorr3Hits",
    )

# tau misidentification scale factors
scaleFactors.assignTauMisidentificationSF(tauSelection, "eToTau", "full", "nominal")
scaleFactors.assignTauMisidentificationSF(tauSelection, "muToTau", "full", "nominal")
scaleFactors.assignTauMisidentificationSF(tauSelection, "jetToTau", "full", "nominal")
# tau trigger SF
scaleFactors.assignTauTriggerSF(tauSelection, "nominal")

#====== Jet selection
jetSelection = PSet(
    jetType                   = "Jets", # options: Jets (AK4PFCHS), JetsPuppi (AK4Puppi)
    ptCut                     = 30.0,
    etaCut                    = 2.5,
    tauMatching_dR            = 0.4,
    multiplicity_CutValue     = 3,
    multiplicity_CutDirection = ">=", # options: ==, !=, <, <=, >, >=
    discriminator_ID          = "IDtight", # options: IDloose, IDtight, IDtightLeptonVeto
    discriminator_PU          = "", # does not work at the moment 
)
 
#====== B-jet selection
bjetSelection = PSet(
    multiplicity_CutValue = 1,
    ptCut                 = 25.0,
    etaCut                = 2.5,
    multiplicity_CutDir   = ">=", # options: ==, !=, <, <=, >, >=
    discriminator         = "pfCombinedInclusiveSecondaryVertexV2BJetTags",
    discriminatorWP       = "Loose",
)

#====== MET selection
metSelection = PSet(
    METCutValue                 = 120.0,
    METCutDirection             = ">", # options: ==, !=, <, <=, >, >=
    METSignificanceCutValue     = -1000.0,
    METSignificanceCutDirection = ">", # options: ==, !=, <, <=, >, >=
    METType                     = "MET_Type1", # options: MET_Type1, MET_Type1_NoHF, MET_Puppi, GenMET, L1MET, HLTMET, CaloMET
    applyPhiCorrections         = False  # FIXME: no effect yet
)


#====== Common plots options
commonPlotsOptions = PSet(
    # Splitting of histograms as function of one or more parameters: 
    # Example: histogramSplitting = [PSet(label="tauPt", binLowEdges=[60, 70, 80, 100, 120], useAbsoluteValues=False)],
    histogramSplitting = [],
    # Bin settings (final bin setting done in datacardGenerator, there also variable bin width is supported)
    nVerticesBins = PSet( nBins=60, axisMin= 0.0      , axisMax=60.0      ),
    ptBins        = PSet( nBins=50, axisMin= 0.0      , axisMax=500.0     ),
    etaBins       = PSet( nBins=60, axisMin=-3.0      , axisMax=3.0       ),
    phiBins       = PSet( nBins=72, axisMin=-3.1415926, axisMax=3.1415926 ),
    njetsBins     = PSet( nBins=20, axisMin= 0.0      , axisMax=20.0      ),
    metBins       = PSet( nBins=80, axisMin= 0.0      , axisMax=800.0     ),
    bjetDiscrBins = PSet( nBins=20, axisMin=-1.0      , axisMax=1.0       ),
    topMassBins   = PSet( nBins=60, axisMin= 0.0      , axisMax=600.0     ),
    # Enable/Disable some debug-level plots
    enablePUDependencyPlots = True,
)

#====== Build all selections group
allSelections = PSet(
    histoAmbientLevel = histoLevel,
    Trigger           = trg,
    METFilter         = metFilter,
    TauSelection      = tauSelection,
    ElectronSelection = electronSelection,
    MuonSelection     = muonSelection,
    JetSelection      = jetSelection,
    BJetSelection     = bjetSelection,
    METSelection      = metSelection,
    CommonPlots       = commonPlotsOptions,
 )
