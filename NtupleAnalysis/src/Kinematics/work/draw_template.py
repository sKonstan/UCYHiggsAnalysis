#!/usr/bin/env python
'''
Usage:
./draw_template.py
 

Description:
This script is used to ... 


TWiki:
https://twiki.cern.ch/twiki/bin/viewauth/CMS/TTHMultileptonsPlusHadronicTau
'''

#================================================================================================
# Imports
#================================================================================================
import ROOT
import os
import sys
import numpy
import math
from optparse import OptionParser

import UCYHiggsAnalysis.NtupleAnalysis.pyROOT.multicrab as m_multicrab
import UCYHiggsAnalysis.NtupleAnalysis.pyROOT.plotter as m_plotter
import UCYHiggsAnalysis.NtupleAnalysis.pyROOT.histos as m_histos
import UCYHiggsAnalysis.NtupleAnalysis.pyROOT.styles as m_styles
import UCYHiggsAnalysis.NtupleAnalysis.pyROOT.datasets as m_datasets
import UCYHiggsAnalysis.NtupleAnalysis.pyROOT.aux as m_aux
pi = 4*math.atan(1)


#================================================================================================
# Helper Functions
#================================================================================================
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


#================================================================================================
# General Settings
#================================================================================================
bRatio        = True
saveFormats   = ["png"]
datasetList   = ["ttHJetToNonbb_M125"]
savePath      = "/afs/cern.ch/user/a/attikis/public/html/"
datasetPaths  = CreateDatasetDict("/afs/cern.ch/user/a/attikis/scratch0/CMSSW_7_5_2/src/UCYHiggsAnalysis/MiniAOD2FlatTree/test/tmp/")


#================================================================================================
# Histogram Definitions
#================================================================================================
yMin       =   0.0
ptMax      = 200.0
etaMax     =   2.4
nPt_Range  = int(ptMax/5.0)
nEta_Range =  12
EtaLines   = [-1.6, -0.8, +0.8, +1.6]
EtaRange   = [[-etaMax, -1.6, ROOT.kRed+1], [+etaMax, +1.6, ROOT.kRed+1], [-1.6, -0.8, ROOT.kYellow-4], [+0.8, +1.6, ROOT.kYellow-4], [-0.8, +0.8, ROOT.kGreen+1] ]


#================================================================================================
# Histogram Options
#================================================================================================
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


#================================================================================================
# Create Histos OBjects
#================================================================================================
folder = "Kinematics"
AllElectronsPt    = m_histos.TH1orTH2( folder, "AllElectronsPt"   , "Canvas Legend", None, **Pt )
PassedElectronsPt = m_histos.TH1orTH2( folder, "PassedElectronsPt", "Canvas Legend", None, **Pt )

AllElectronsEta     = m_histos.TH1orTH2( folder, "PassedElectronsPt", "Canvas Legend", None, **Eta )
PassedElectronsEta  = m_histos.TH1orTH2( folder, "PassedElectronsPt", "Canvas Legend", None, **Eta )


#================================================================================================
# Function Definition
#================================================================================================
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

#================================================================================================
def main():
    '''
    '''

    # Find module names
    mcrab = m_multicrab.Multicrab(verbose=False)
    myNames = mcrab.FindModuleNames(opts.mcrab, "Kinematics")

    # Get dataset managers
    for n in myNames:
        datasets = dataset.getDatasetsFromMulticrabDirs([opts.mcrab], analysisName=n)
        for dset in datasets.getMCDatasets():
            if dset.name.startswith(opts.dataset):
                doPlot(n, dset, opts.errorlevel)
                #DoPlots( [hGenJet_e], datasetList, bColourPalette )


#================================================================================================
if __name__ == "__main__":

    parser = OptionParser(usage="Usage: %prog [options]",add_help_option=False,conflict_handler="resolve")
    parser.add_option("-m", "--mcrab"  , dest="mcrab"     , action="store", help="Path to the multicrab directory for input")
    parser.add_option("-d", "--dataset", dest="dataset"   , action="store", help="Name of the dataset to be plotted")
    #parser.add_option("-e", "--error"  , dest="errorlevel", action="store", help="Maximum relative uncertainty per bin (default=10%%)", default=0.10)
    (opts, args) = parser.parse_args()

    if opts.mcrab == None:
        raise Exception("Please provide input multicrab directory with -m")
    if not os.path.exists(opts.mcrab):
        raise Exception("The input root file '%s' does not exist!" % opts.mcrab)
    if opts.dataset == None:
        raise Exception("Please provide dataset name with -d")

    main()

        
#########################################################
