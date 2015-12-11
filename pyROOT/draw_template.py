#!/usr/bin/env python
###############################################################
### All imported modules
###############################################################
import ROOT
import os
import sys
import numpy
import math
import tools.plotter as m_plotter
import tools.histos as m_histos
import tools.styles as m_styles
import tools.datasets as m_datasets
import tools.aux as m_aux
pi = 4*math.atan(1)

###############################################################
### Options here
###############################################################
bGenJets = True

###############################################################
### Helper Functions
###############################################################
def CreateDatasetDict(inputPath):
    '''
    '''
    datasetPaths= {}
    for dataset in GetDatasetsList():
        datasetPaths[dataset] = inputPath + "Histos_" + dataset + ".root"
    return datasetPaths


def GetDatasetsList():
    '''
    '''
    datasets = ["ST_s-channel", "DYJetsToLL_M-10to50", "TTWJetsToLNu","T_tW_antitop", "TTZToLLNuNu",
                "ZZ", "WZ", "TTJets", "ttHJetToNonbb_M125", "ST_tW_top", "DYJetsToLL_M-50"]
    return datasets


###############################################################
### General Settings
###############################################################
bRatio        = True
saveFormats   = ["png"]
datasetList   = ["ttHJetToNonbb_M125"]
savePath      = "/afs/cern.ch/user/a/attikis/public/html/"
datasetPaths  = CreateDatasetDict("/afs/cern.ch/user/a/attikis/scratch0/CMSSW_7_5_2/src/UCYHiggsAnalysis/MiniAOD2FlatTree/test/tmp/")


###############################################################
### Histo Definitions
###############################################################
yMin       =   0.0
ptMax      = 200.0
etaMax     =   2.4
nPt_Range  = int(ptMax/5.0)
nEta_Range =  12
EtaLines   = [-1.6, -0.8, +0.8, +1.6]
EtaRange   = [[-etaMax, -1.6, ROOT.kRed+1], [+etaMax, +1.6, ROOT.kRed+1], [-1.6, -0.8, ROOT.kYellow-4], [+0.8, +1.6, ROOT.kYellow-4], [-0.8, +0.8, ROOT.kGreen+1] ]


############################################################### 
### Histogram Options
############################################################### 
Pt = {
    "xLabel": "p_{T}"           , "xUnits": "GeVc^{-1}", "xMin": 0.00, "xMax": ptMax, "binWidthX": None, "xCutLines": [], "xCutBoxes": [], "gridX": True, "logX": False, 
    "yLabel": "Entries / %0.0f" , "yUnits": ""         , "yMin": 1E00, "yMax": None , "binWidthY": None, "yCutLines": [], "yCutBoxes": [], "gridY": True, "logY": True
    , 
    "ratioLabel": "Ratio", "ratio": False, "invRatio": False, "yMinRatio": 0.0 , "yMaxRatio": 2.15 , "normaliseTo": None, "drawOptions": "P", "legOptions": "LP",
    "logYRatio": False, "xLegMin": 0.18, "xLegMax": 0.4, "yLegMin": 0.80, "yLegMax": 0.90
}

Eta = {
    "xLabel": "#eta"           , "xUnits": ""     , "xMin": -etaMax , "xMax": +etaMax, "binWidthX": None, "xCutLines": [0], "gridX": True, "logX": False, 
    "yLabel": "Entries / %0.2f", "yUnits": ""     , "yMin": +1e00, "yMax": None, "binWidthY": None, "yCutLines": [] , "yCutBoxes": [], "gridY": True, "logY": True , 
    "ratioLabel": "Ratio", "ratio": False, "invRatio": False, "yMinRatio": 1e-01, "yMaxRatio": 2.15 , "normaliseTo": None, "drawOptions": "P", "legOptions": "LP", 
    "logYRatio": False, "logXRatio": False, "xLegMin": 0.18, "xLegMax": 0.4, "yLegMin": 0.80, "yLegMax": 0.90, "xCutBoxes": [[-1.0, -1.6, ROOT.kBlue], [+1.0, +1.6, ROOT.kBlue]]
    #"xCutBoxes": [[-1.0, -1.6, ROOT.kBlue], [-1.0, +1.0, ROOT.kRed], [+1.0, +1.6, ROOT.kBlue]]
    #"xCutBoxes": [[-1.0, -1.6, ROOT.kBlue], [+1.0, +1.6, ROOT.kBlue]]
    #"xCutBoxes": [[-1.0, +1.0, ROOT.kRed]]
}


Phi = {
    "xLabel": "#phi"            , "xUnits": "rads" , "xMin": -3.2 , "xMax": +3.2, "binWidthX": None, "xCutLines": [0], "xCutBoxes": [], "gridX": True, "logX": False, 
    "yLabel": "Entries / %0.2f" , "yUnits": ""     , "yMin": +1E00, "yMax": None, "binWidthY": None, "yCutLines": [] , "yCutBoxes": [], "gridY": True, "logY": True, 
    "ratioLabel": "Ratio", "ratio": False, "invRatio": False, "yMinRatio": 0.0 , "yMaxRatio": 2.15 , "normaliseTo": None, "drawOptions": "P", "legOptions": "LP",
    "logYRatio": False, "logXRatio": False, "xLegMin": 0.18, "xLegMax": 0.4, "yLegMin": 0.80, "yLegMax": 0.90
}

Energy = {
    "xLabel": "Energy"          , "xUnits": "GeV", "xMin":   0.0, "xMax": +25.0, "binWidthX": None, "xCutLines": [20], "xCutBoxes": [], "gridX": True, "logX": False, 
    "yLabel": "Entries / %0.2f" , "yUnits": ""   , "yMin": +1E00, "yMax": None , "binWidthY": None, "yCutLines": []  , "yCutBoxes": [], "gridY": True, "logY": True , 
    "ratioLabel": "Ratio", "ratio": False, "invRatio": False, "yMinRatio": 1e-01, "yMaxRatio": 2.15, "normaliseTo": None, "drawOptions": "P", "legOptions": "LP",
    "logYRatio": False, "logXRatio": False, "xLegMin": 0.18, "xLegMax": 0.4, "yLegMin": 0.80, "yLegMax": 0.90
    }


############################################################### 
### Create Histogram Objects
############################################################### 
hGenJet_pt  = m_histos.TH1orTH2( "", "hGenJetPt" , "GenJet" , None, **Pt )
hGenJet_eta = m_histos.TH1orTH2( "", "hGenJetEta", "GenJet" , None, **Eta)
hGenJet_phi = m_histos.TH1orTH2( "", "hGenJetPhi", "GenJet" , None, **Phi)
hGenJet_e   = m_histos.TH1orTH2( "", "hGenJetE"  , "GenJet" , None, **Energy)


###############################################################
### Main
###############################################################
def DoPlots(hList, dataset, bColourPalette=False, saveExt=""):

    p = m_plotter.Plotter( Verbose=False, BatchMode=True )
    p.SetBoolUseDatasetAsLegEntry(bColourPalette)
    p.AddDataset(dataset + ":test", datasetPaths[dataset])

    if (len(p.DatasetToRootFileMap.keys()) > 1):
        p.SetBoolUseDatasetAsLegEntry(True)
    else:
        p.SetBoolUseDatasetAsLegEntry(False)

    p.EnableColourPalette(bColourPalette)
    p.AddHisto(hList)
    p.SetupStatsBox(-1, -1, -1, -1, 000000000)
    p.SetupStatsBox()
    p.Draw(THStackDrawOpt="nostack", bStackInclusive = False, bAddReferenceHisto = True)
    p.SetTLegendHeader(dataset, "" )
    p.SaveHistos(True, savePath, saveFormats, saveExt)

    return

###############################################################
if __name__ == "__main__":

    bColourPalette = True
    if (bGenJets):
        DoPlots( [hGenJet_pt]   , datasetList[0], bColourPalette)
        DoPlots( [hGenJet_eta]  , datasetList[0], bColourPalette )
        DoPlots( [hGenJet_phi]   , datasetList[0], bColourPalette )
        DoPlots( [hGenJet_e]   , datasetList[0], bColourPalette )
        
###############################################################
