#!/usr/bin/env python
'''
Usage:
./draw_template.py -m analysis_15Feb2016_10h01m18s/
 

Description:
This script plots histograms from an analysis directory.


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
import UCYHiggsAnalysis.NtupleAnalysis.pyROOT.plotter as plotter
import UCYHiggsAnalysis.NtupleAnalysis.pyROOT.histos as histos
import UCYHiggsAnalysis.NtupleAnalysis.pyROOT.aux as aux


#================================================================================================
# Settings
#================================================================================================
verbose       = False
batchMode     = True
myLumi        = 2.26 # in fb
folder        = "Kinematics"
analysis      = folder
saveFormats   = ["png"] #, "pdf"]
savePath      = ""


#================================================================================================
# Object Definitions
#================================================================================================
auxObject  = aux.AuxClass(verbose)


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
PtRange    = [ [40.0, 80.0, ROOT.kRed] ]
EvtRange   = [ [1E2, 1E4, ROOT.kBlack] ]
#EvtRange   = [ [0.5, 1.5, ROOT.kBlack] ]


#================================================================================================
# Histogram Options
#================================================================================================
Pt = {
    "xLabel": "p_{T}"           , "xUnits": "GeVc^{-1}", "xMin": 0.00 , "xMax": ptMax, "binWidthX": None, "xCutLines": [], "xCutBoxes": [], "gridX": True, "logX": False, 
    "yLabel": "Entries / %0.0f" , "yUnits": ""         , "yMin": 1E-01, "yMax": None , "binWidthY": None, "yCutLines": [], "yCutBoxes": [], "gridY": True, "logY": True,
    "ratioLabel": "Ratio", "yMinRatio": 0.0 , "yMaxRatio": 2.15 , "drawOptions": "HIST9", "legOptions": "F", 
    "logYRatio": False, "logXRatio": False, "xLegMin": 0.70, "xLegMax": 0.95, "yLegMin": 0.78, "yLegMax": 0.93, "gridXRatio": True, "gridYRatio": True,
}

PtTest = {
    "xLabel": "p_{T}"           , "xUnits": "GeVc^{-1}", "xMin": 0.00 , "xMax": ptMax, "binWidthX": None, "xCutLines": [20], "xCutBoxes": PtRange  , "gridX": True, "logX": False, 
    "yLabel": "Entries / %0.0f" , "yUnits": ""         , "yMin": 1E-01, "yMax": None , "binWidthY": None, "yCutLines": [10], "yCutBoxes": EvtRange, "gridY": True, "logY": True,
    "ratioLabel": "Ratio", "yMinRatio": 0.0 , "yMaxRatio": 2.15 , "drawOptions": "HIST9", "legOptions": "F", 
    "logYRatio": False, "logXRatio": False, "xLegMin": 0.70, "xLegMax": 0.95, "yLegMin": 0.78, "yLegMax": 0.93, "gridXRatio": True, "gridYRatio": True,
}


Eta = {
    "xLabel": "#eta"           , "xUnits": "", "xMin": -etaMax, "xMax": +etaMax, "binWidthX": None, "xCutLines": [0], "gridX": True, "gridXRatio": False, "logX": False,
    "yLabel": "Entries / %0.2f", "yUnits": "", "yMin": +1e00  , "yMax": None   , "binWidthY": None, "yCutLines": [] , "gridY": True, "gridYRatio": False, "logY": True ,
    "xCutBoxes": [], "yCutBoxes": [],  "ratioLabel": "Ratio"      , "yMinRatio": 0.0, "yMaxRatio": 2.15 , "drawOptions": "P", "legOptions": "LP", 
    "xCutBoxes": [[-1.0, -1.6, ROOT.kBlue], [+1.0, +1.6, ROOT.kBlue]], "yCutBoxes": [], "logYRatio": False, "logXRatio": False,
    "xLegMin": 0.75, "xLegMax": 0.95, "yLegMin": 0.80, "yLegMax": 0.92
}


#================================================================================================
# Create Histos OBjects
#================================================================================================
PassedElectronsPt   = histos.DrawObject( folder, "PassedElectronsPt" , "passed", **Pt )
PassedElectronsEta  = histos.DrawObject( folder, "PassedElectronsEta", "passed", **Eta )
AllElectronsPt      = histos.DrawObject( folder, "AllElectronsPt"    , "all"   , **Pt )
AllElectronsEta     = histos.DrawObject( folder, "AllElectronsEta"   , "all"   , **Eta )


#================================================================================================
# Function Definition
#================================================================================================
def DoPlots(histo, datasetObjects, intLumi, savePostfix=""):

    p = plotter.Plotter(verbose, batchMode)
    p.SetupRoot(0, 4, 999, 2000)
    # p.SetupStatsBox("ksiourmen", xPos=0.90, yPos=0.88, width=0.20, height=0.12)
    p.AddDatasets(datasetObjects)
    p.AddDrawObject(histo)
    p.NormaliseHistos("toLuminosity") # "byXSection", "toOne"
    p.AddCmsText("13", intLumi, prelim=True)
    p.DatasetAsLegend(True)    

    # p.AddTF1("1000*cos(x)", 0, 200.0, False, {"lineColour": ROOT.kBlack})
    # p.DrawRatio("stack", "nostackAP", "Data")
    p.DrawRatio("stack", "nostackAP", "ttHJetToNonbb_M125")    
    # p.Draw("stack") # "nostack"
    # p.SetHistosFillStyle(3001)
    # p.DrawStackInclusive()

    # p.SaveAs(savePath, histo.GetName() + "_test", savePostfix, saveFormats)
    # p.Save()
    p.Save("", ["png"])    
    p.Exit()
    
    return

#================================================================================================
def main():
    '''
    '''

    # Variables
    #histoList = [AllElectronsEta, PassedElectronsEta]
    histoList = [AllElectronsPt, PassedElectronsPt]
    
    # Datasets
    auxObject.StartTimer("Dataset Manager")
    datasetManager = dataset.DatasetManager(opts.mcrab, analysis)
    datasetManager.LoadLuminosities("lumi.json")
    datasetManager.MergeData()
    datasetObjects = datasetManager.GetAllDatasets()
    # datasetObjects = datasetManager.GetMCDatasets()
    # datasetObjects   = [datasetManager.GetDataset("ttHJetToNonbb_M125")]
    datasetManager.SetLuminosityForMC( datasetManager.GetLuminosity() ) #myLumi
    intLumi        = datasetManager.GetLuminosityString("fb") 
    datasetManager.PrintSummary()
    # datasetManager.PrintDatasets()
    # datasetManager.PrintSelections("DYJetsToLL_M_10to50")
    
    # One Histogram on a given canvas (many datasets)
    for h in histoList:
        DoPlots( h, datasetObjects, intLumi)
    # Many Histograms on a given canvas (many datasets)
    #DoPlots( histoList, datasetObjects, False )

    

#================================================================================================
if __name__ == "__main__":
    
    parser = OptionParser(usage="Usage: %prog [options]",add_help_option=False,conflict_handler="resolve")
    parser.add_option("-m", "--mcrab"  , dest="mcrab"  , action="store", help="Path to the multicrab directory for input")
    (opts, args) = parser.parse_args()

    if opts.mcrab == None:
        raise Exception("Please provide input multicrab directory with -m")
    if not os.path.exists(opts.mcrab):
        raise Exception("The input root file '%s' does not exist!" % opts.mcrab)

    auxObject.StartTimer("Total")
    main()
    auxObject.PrintTimers()
#================================================================================================
