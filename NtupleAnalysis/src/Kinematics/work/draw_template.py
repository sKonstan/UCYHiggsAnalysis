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

import UCYHiggsAnalysis.NtupleAnalysis.pyROOT.dataset as dataset
#import UCYHiggsAnalysis.NtupleAnalysis.pyROOT.crossSection as crossSection
import UCYHiggsAnalysis.NtupleAnalysis.pyROOT.plotter as plotter
import UCYHiggsAnalysis.NtupleAnalysis.pyROOT.histos as histos
import UCYHiggsAnalysis.NtupleAnalysis.pyROOT.styles as styles
import UCYHiggsAnalysis.NtupleAnalysis.pyROOT.aux as aux

from UCYHiggsAnalysis.NtupleAnalysis.pyROOT.crossSection import xSections


#================================================================================================
# General Settings
#================================================================================================
verbose       = False
batchMode     = False
ratio         = False
myLumi        = 2.26 # in fb
folder        = "Kinematics"
analysis      = folder
saveFormats   = ["png"] #, "pdf"]
savePath      = ""


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
#Pt = {
#    "xLabel": "p_{T}"           , "xUnits": "GeVc^{-1}", "xMin": 0.00 , "xMax": ptMax, "binWidthX": None, "xCutLines": [], "xCutBoxes": [], "gridX": True, "logX": False, 
#    "yLabel": "Entries / %0.0f" , "yUnits": ""         , "yMin": 1E-05, "yMax": 1E+00, "binWidthY": None, "yCutLines": [], "yCutBoxes": [], "gridY": True, "logY": True , 
#    "ratioLabel": "Ratio", "ratio": False, "invRatio": False, "yMinRatio": 0.0 , "yMaxRatio": 2.15 , "normalise": "toOne"  , "drawOptions": "HIST", "legOptions": "FL",
#    "logYRatio": False, "logXRatio": False, "xLegMin": 0.75, "xLegMax": 0.95, "yLegMin": 0.80, "yLegMax": 0.92
#}


#Pt = {
#    "xLabel": "p_{T}"           , "xUnits": "GeVc^{-1}", "xMin": 0.00 , "xMax": ptMax, "binWidthX": None, "xCutLines": [], "xCutBoxes": [], "gridX": True, "logX": False, 
#    "yLabel": "Entries / %0.0f" , "yUnits": ""         , "yMin": 1E-01, "yMax": None , "binWidthY": None, "yCutLines": [], "yCutBoxes": [], "gridY": True, "logY": True , 
#    "ratioLabel": "Ratio", "ratio": False, "invRatio": False, "yMinRatio": 0.0 , "yMaxRatio": 2.15 , "normalise": "byXSection"  , "drawOptions": "HIST", "legOptions": "FL",
#    "logYRatio": False, "logXRatio": False, "xLegMin": 0.75, "xLegMax": 0.95, "yLegMin": 0.80, "yLegMax": 0.92
#}


Pt = {
    "xLabel": "p_{T}"           , "xUnits": "GeVc^{-1}", "xMin": 0.00 , "xMax": ptMax, "binWidthX": None, "xCutLines": [], "xCutBoxes": [], "gridX": True, "logX": False, 
    "yLabel": "Entries / %0.0f" , "yUnits": ""         , "yMin": 1E-01, "yMax": None , "binWidthY": None, "yCutLines": [], "yCutBoxes": [], "gridY": True, "logY": True , 
    "ratioLabel": "Ratio", "ratio": False, "invRatio": False, "yMinRatio": 0.0 , "yMaxRatio": 2.15 , "normalise": "toLuminosity"  , "drawOptions": "HIST", "legOptions": "FL",
    "logYRatio": False, "logXRatio": False, "xLegMin": 0.75, "xLegMax": 0.95, "yLegMin": 0.80, "yLegMax": 0.92
}


Eta = {
    "xLabel": "#eta"           , "xUnits": ""     , "xMin": -etaMax , "xMax": +etaMax, "binWidthX": None, "xCutLines": [0], "gridX": True, "logX": False, "xCutBoxes": [],  
    "yLabel": "Entries / %0.2f", "yUnits": ""     , "yMin": +1e00   , "yMax": None   , "binWidthY": None, "yCutLines": [] , "gridY": True, "logY": True , "yCutBoxes": [],  
    "ratioLabel": "Ratio"      , "ratio": False   , "invRatio": False, "yMinRatio": 1e-01, "yMaxRatio": 2.15 , "normalise": "toLuminosity", "drawOptions": "P", "legOptions": "LP", 
    "xCutBoxes": [[-1.0, -1.6, ROOT.kBlue], [+1.0, +1.6, ROOT.kBlue]], "yCutBoxes": [], "logYRatio": False, "logXRatio": False, "xLegMin": 0.75, "xLegMax": 0.95, "yLegMin": 0.80, "yLegMax": 0.92
}


#================================================================================================
# Create Histos OBjects
#================================================================================================
PassedElectronsPt   = histos.TH1orTH2( folder, "PassedElectronsPt", "passed", **Pt )
AllElectronsPt      = histos.TH1orTH2( folder, "AllElectronsPt"   , "all"   , **Pt )

PassedElectronsEta  = histos.TH1orTH2( folder, "PassedElectronsEta", "passed", **Eta )
AllElectronsEta     = histos.TH1orTH2( folder, "AllElectronsEta"   , "all"   , **Eta )



#================================================================================================
# Function Definition
#================================================================================================
def DoPlots(histo, datasetObjects, intLumi, bColourPalette=False, savePostfix=""):

    p = plotter.Plotter(verbose, batchMode)
    p.SetupRoot()
    # p.SetupStatsBox("ksiourmen", xPos=0.40, yPos=0.5)
    p.AddDatasets(datasetObjects)
    p.DatasetAsLegend(True)
    p.AddHisto(histo)
    # p.SetupStatsBox(0.90, 0.88, 0.20, 0.12, 111111111)
    # p.Draw(THStackDrawOpt="nostack", includeStack = False, bAddReferenceHisto = True)
    # p.Draw(THStackDrawOpt="stack", includeStack = False, bAddReferenceHisto = True)
    p.Draw()
    p.AddPreliminaryText("13", intLumi)
    #p.SaveAs(savePath, savePostfix, saveFormats)
    p.Save()
    # p.PrintElapsedTime(units = "seconds")
    return


#================================================================================================
def IsBatchMode():
    '''
    Forces user to press 'q' before exiting ROOT from batch mode.
    '''
    if batchMode:
        key = ""
        while key != "q":
            key = raw_input("\r=== draw_template.py:\n\t Press 'q' to quit ROOT: ")
        sys.exit()
    return


#================================================================================================
def main():
    '''
    '''

    # Variables
    args           = {}
    #histoList      = [AllElectronsPt, PassedElectronsPt, AllElectronsEta, PassedElectronsEta]
    histoList      = [AllElectronsPt, PassedElectronsPt]

    # Datasets
    datasetManager = dataset.DatasetManager(opts.mcrab, analysis)
    datasetManager.LoadLuminosities("lumi.json")
    # datasetObjects = datasetManager.GetAllDatasets()
    datasetObjects = datasetManager.GetMCDatasets()
    datasetManager.SetLuminosityForMC( datasetManager.GetLuminosity() ) #myLumi
    intLumi        = datasetManager.GetLuminosityString("fb") 
    datasetManager.PrintSummary()
    # datasetManager.PrintDatasets()
    # datasetManager.PrintSelections("DYJetsToLL_M_10to50")
    
    # One Histogram on a given canvas (many datasets)
    for h in histoList:
        DoPlots( h, datasetObjects, intLumi, False )

    # Many Histograms on a given canvas (many datasets)
    # DoPlots( histoList, datasetObjects, False )



#================================================================================================
if __name__ == "__main__":

    parser = OptionParser(usage="Usage: %prog [options]",add_help_option=False,conflict_handler="resolve")
    parser.add_option("-m", "--mcrab"  , dest="mcrab"  , action="store", help="Path to the multicrab directory for input")
    parser.add_option("-d", "--dataset", dest="dataset", action="store", help="Name of the dataset to be plotted")
    (opts, args) = parser.parse_args()

    if opts.mcrab == None:
        raise Exception("Please provide input multicrab directory with -m")
    if not os.path.exists(opts.mcrab):
        raise Exception("The input root file '%s' does not exist!" % opts.mcrab)
    #if opts.dataset == None:
    #   raise Exception("Please provide dataset name with -d")

    main()
    IsBatchMode()
    
#================================================================================================
