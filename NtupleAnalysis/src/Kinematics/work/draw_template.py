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
ratio         = True
myLumi        = 2.26 # in fb
folder        = "Kinematics"
analysis      = folder
saveFormats   = ["png"] #, "pdf"]
savePath      = ""


#================================================================================================
# Object Definitions
#================================================================================================
auxObject = aux.AuxClass(verbose)


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
PtRange   = [ [0.0, 20.0, ROOT.kRed+1], [40.0, 80.0, ROOT.kTeal+1] ]

#================================================================================================
# Histogram Options
#================================================================================================
#Pt = {
#    "xLabel": "p_{T}"           , "xUnits": "GeVc^{-1}", "xMin": 0.00 , "xMax": ptMax, "binWidthX": None, "xCutLines": [], "xCutBoxes": [], "gridX": True, "logX": False, 
#    "yLabel": "Entries / %0.0f" , "yUnits": ""         , "yMin": 1E-05, "yMax": 1E+00, "binWidthY": None, "yCutLines": [], "yCutBoxes": [], "gridY": True, "logY": True , 
#    "ratioLabel": "Ratio", "yMinRatio": 0.0 , "yMaxRatio": 2.15 , "drawOptions": "HIST", "legOptions": "FL",
#    "logYRatio": False, "logXRatio": False, "xLegMin": 0.75, "xLegMax": 0.95, "yLegMin": 0.80, "yLegMax": 0.92
#}


#Pt = {
#    "xLabel": "p_{T}"           , "xUnits": "GeVc^{-1}", "xMin": 0.00 , "xMax": ptMax, "binWidthX": None, "xCutLines": [], "xCutBoxes": [], "gridX": True, "logX": False, 
#    "yLabel": "Entries / %0.0f" , "yUnits": ""         , "yMin": 1E-01, "yMax": None , "binWidthY": None, "yCutLines": [], "yCutBoxes": [], "gridY": True, "logY": True , 
#    "ratioLabel": "Ratio", "yMinRatio": 0.0 , "yMaxRatio": 2.15 , "drawOptions": "HIST", "legOptions": "FL",
#    "logYRatio": False, "logXRatio": False, "xLegMin": 0.75, "xLegMax": 0.95, "yLegMin": 0.80, "yLegMax": 0.92
#}


Pt = {
    "xLabel": "p_{T}"           , "xUnits": "GeVc^{-1}", "xMin": 0.00 , "xMax": ptMax, "binWidthX": None, "xCutLines": [10], "xCutBoxes": PtRange, "gridX": True, "logX": False, 
    "yLabel": "Entries / %0.0f" , "yUnits": ""         , "yMin": 1E-01, "yMax": None , "binWidthY": None, "yCutLines": [1], "yCutBoxes": [], "yCutLinesRatio": True, "gridY": True, "logY": True , 
    "ratioLabel": "Ratio", "yMinRatio": 0.0 , "yMaxRatio": 2.15 , "drawOptions": "HIST", "legOptions": "FL",
    "logYRatio": False, "logXRatio": False, "xLegMin": 0.75, "xLegMax": 0.95, "yLegMin": 0.80, "yLegMax": 0.92
}


Eta = {
    "xLabel": "#eta"           , "xUnits": ""     , "xMin": -etaMax , "xMax": +etaMax, "binWidthX": None, "xCutLines": [0], "gridX": True, "logX": False, "xCutBoxes": [],  
    "yLabel": "Entries / %0.2f", "yUnits": ""     , "yMin": +1e00   , "yMax": None   , "binWidthY": None, "yCutLines": [] , "gridY": True, "logY": True , "yCutBoxes": [],  
    "ratioLabel": "Ratio"      , "yMinRatio": 1e-01, "yMaxRatio": 2.15 , "drawOptions": "P", "legOptions": "LP", 
    "xCutBoxes": [[-1.0, -1.6, ROOT.kBlue], [+1.0, +1.6, ROOT.kBlue]], "yCutBoxes": [], "logYRatio": False, "logXRatio": False, "xLegMin": 0.75, "xLegMax": 0.95, "yLegMin": 0.80, "yLegMax": 0.92
}


#================================================================================================
# Create Histos OBjects
#================================================================================================
PassedElectronsPt   = histos.DrawObject( folder, "PassedElectronsPt", "passed", **Pt )
AllElectronsPt      = histos.DrawObject( folder, "AllElectronsPt"   , "all"   , **Pt )

PassedElectronsEta  = histos.DrawObject( folder, "PassedElectronsEta", "passed", **Eta )
AllElectronsEta     = histos.DrawObject( folder, "AllElectronsEta"   , "all"   , **Eta )



#================================================================================================
# Function Definition
#================================================================================================
def DoPlots(histo, datasetObjects, intLumi, bColourPalette=False, savePostfix=""):

    p = plotter.Plotter(verbose, batchMode)
    p.SetupRoot(0, 4, 999, 2000)
    # p.SetupStatsBox("ksiourmen", xPos=0.90, yPos=0.88, width=0.20, height=0.12)
    # p.SetAttribute("verbose", True)
    
    p.AddDatasets(datasetObjects)
    p.DatasetAsLegend(True)
    p.AddDrawObject(histo)
    
    p.NormaliseHistos("toLuminosity")
    # p.NormaliseHistos("byXSection")
    # p.NormaliseHistos("toOne")

    
    p.CreateCanvas(ratio)
    # p.AddTF1("1000*cos(x)", 0, 200.0, False, {"lineColour": ROOT.kBlack})
    p.AddCmsText("13", intLumi, prelim=True)
    # p.Draw(THStackDrawOpt="nostack", includeStack = False, bAddReferenceHisto = True)
    p.Draw(THStackDrawOpt="stack", includeStack = False, bAddReferenceHisto = True)
    # p.Draw()

    
    p.Save()    
    # p.SaveAs(savePath, histo.GetName() + "_test", savePostfix, saveFormats)

    
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
    auxObject.StartTimer("Dataset Manager")
    datasetManager = dataset.DatasetManager(opts.mcrab, analysis)
    datasetManager.LoadLuminosities("lumi.json")
    # datasetObjects = datasetManager.GetAllDatasets()
    datasetObjects = datasetManager.GetMCDatasets()
    # datasetObjects   = [datasetManager.GetDataset("ttHJetToNonbb_M125")]
    datasetManager.SetLuminosityForMC( datasetManager.GetLuminosity() ) #myLumi
    intLumi        = datasetManager.GetLuminosityString("fb") 
    # datasetManager.PrintSummary()
    # datasetManager.PrintDatasets()
    # datasetManager.PrintSelections("DYJetsToLL_M_10to50")
    
    # One Histogram on a given canvas (many datasets)
    for h in histoList:
        DoPlots( h, datasetObjects, intLumi, False )
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
    IsBatchMode()
    auxObject.PrintTimers()
#================================================================================================
