#!/usr/bin/env python
from UCYHiggsAnalysis.NtupleAnalysis.main import PSet
import UCYHiggsAnalysis.NtupleAnalysis.parameters.scaleFactors as scaleFactors


#====== General parameters
histoLevel = "Debug"  # Options: Systematics, Vital, Informative, Debug

#====== Electrons
eleSelection  = PSet(
    ElePtCut  = 7.0,
    EleEtaCut = 2.5,
)

#====== Muons
muSelection    = PSet(
    muonPtCut  = 5.0,
    muonEtaCut = 2.4,
)

#====== Bjets
jetSelection  = PSet(
    jetPtCut  = 0.0,
    jetEtaCut = 2.4,
)

#====== Bjets
bjetSelection  = PSet(
    bjetPtCut  = 25.0,
    bjetEtaCut =  2.4,
)


#====== Build all selections group
allSelections = PSet(
    histogramAmbientLevel = histoLevel,
    #Trigger               = trg,
    ElectronSelection     = eleSelection,
    MuonSelection         = muSelection,
    JetSelection          = jetSelection,
    BJetSelection         = bjetSelection,
    #CommonPlots           = commonPlotsOptions,
)
