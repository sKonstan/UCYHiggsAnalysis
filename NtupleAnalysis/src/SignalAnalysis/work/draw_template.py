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
folder        = "SignalAnalysis_mH125_Run2015D"
analysis      = folder
intLumiInPb   = 888.357
saveFormats   = ["png"]
savePath      = "/Users/attikis/Desktop/"
#savePath      = "/afs/cern.ch/user/a/attikis/public/html/"


#================================================================================================
# Object Definitions
#================================================================================================
auxObject  = aux.AuxClass(verbose)

datasetMapping = {}
datasetMapping["ST_t_channel_top_4f_leptonDecays"]     = "Single t"
datasetMapping["ST_tW_antitop_5f_inclusiveDecays"]     = "Single t"
datasetMapping["ST_t_channel_antitop_4f_leptonDecays"] = "Single t"
datasetMapping["ST_tW_top_5f_inclusiveDecays"]         = "Single t"
datasetMapping["ST_s_channel_4f_leptonDecays"]         = "Single t"
# datasetMapping["ST_s_channel_4f_leptonDecays"]         = "MC "
# datasetMapping["ST_tW_antitop_5f_inclusiveDecays"]     = "MC "
# datasetMapping["ST_tW_top_5f_inclusiveDecays"]         = "MC "
# datasetMapping["ST_t_channel_antitop_4f_leptonDecays"] = "MC "
# datasetMapping["ST_t_channel_top_4f_leptonDecays"]     = "MC "
# datasetMapping["DYJetsToLL_M_10to50"]                  = "MC "
# datasetMapping["DYJetsToLL_M_50"]                      = "MC "
# datasetMapping["TTJets"]                               = "MC "
# datasetMapping["WJetsToLNu"]                           = "MC "
# datasetMapping["WW"]                                   = "MC "
# datasetMapping["WZ"]                                   = "MC "
# datasetMapping["ZZ"]                                   = "MC "


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


Eta = {
    "xLabel": "#eta"           , "xUnits": "", "xMin": -etaMax, "xMax": +etaMax, "binWidthX": None, "xCutLines": [0], "gridX": True, "gridXRatio": False, "logX": False,
    "yLabel": "Entries / %0.2f", "yUnits": "", "yMin": +1e00  , "yMax": None   , "binWidthY": None, "yCutLines": [] , "gridY": True, "gridYRatio": False, "logY": True ,
    "xCutBoxes": [], "yCutBoxes": [],  "ratioLabel": "Ratio"      , "yMinRatio": 0.0, "yMaxRatio": 2.15 , "drawOptions": "P", "legOptions": "LP", 
    "xCutBoxes": [[-1.0, -1.6, ROOT.kBlue], [+1.0, +1.6, ROOT.kBlue]], "yCutBoxes": [], "logYRatio": False, "logXRatio": False,
    "xLegMin": 0.72, "xLegMax": 0.95, "yLegMin": 0.80, "yLegMax": 0.92
}


wCounter = {
    "xMin": 8.0, "xMax": None, "gridX": True, "gridXRatio": True, "logX": False,
    "yLabel": "Events / %0.1f", "yMin": 1.0, "yMax": 1e+8, "yUnits": "", "yCutLines": [], "gridY": True,  "gridYRatio": True, "logY": True, "yCutBoxes": [], "xCutBoxes": [],
    "ratioLabel": "Ratio", "yMinRatio": 0.0, "yMaxRatio": 4.75 , "drawOptions": "HIST9", "legOptions": "F", "logYRatio": False, "logXRatio": False,
    "xLegMin": 0.72, "xLegMax": 0.95, "yLegMin": 0.80, "yLegMax": 0.92, 
}


NJets = {
    "xLabel": "Jets" , "xUnits":"", "xMin": 0.0, "xMax": 10.0, "xCutLines": [3], "gridX": True, "gridXRatio": False, "logX": False,
    "yLabel": "Events / %0.1f", "yMin": 1.0, "yMax": None, "yUnits": "", "yCutLines": [], "gridY": True,  "gridYRatio": True, "logY": True, "yCutBoxes": [], "xCutBoxes": [],
    "ratioLabel": "Ratio", "yMinRatio": 0.0, "yMaxRatio": 3.75 , "drawOptions": "HIST9", "legOptions": "F", "logYRatio": False, "logXRatio": False,
    "xLegMin": 0.72, "xLegMax": 0.95, "yLegMin": 0.80, "yLegMax": 0.92, 
}


NBjets = {
    "xLabel": "b-tagged Jets" , "xUnits":"", "xMin": 0.0, "xMax": 10.0, "xCutLines": [3], "gridX": True, "gridXRatio": False, "logX": False,
    "yLabel": "Events / %0.1f", "yMin": 1.0, "yMax": None, "yUnits": "", "yCutLines": [], "gridY": True,  "gridYRatio": True, "logY": True, "yCutBoxes": [], "xCutBoxes": [],
    "ratioLabel": "Ratio", "yMinRatio": 0.0, "yMaxRatio": 3.75 , "drawOptions": "HIST9", "legOptions": "F", "logYRatio": False, "logXRatio": False,
    "xLegMin": 0.72, "xLegMax": 0.95, "yLegMin": 0.80, "yLegMax": 0.92, 
}


#================================================================================================
# Create Histos Objects
#================================================================================================
Njets_AtJetSelection     = histos.DrawObject( folder + "/CommonPlots", "Njets_AtJetSelection"    , "" , **NJets )
Njets_AfterJetSelections = histos.DrawObject( folder + "/CommonPlots", "Njets_AfterJetSelections", "" , **NJets )
NBjets_AtBtagging        = histos.DrawObject( folder + "/CommonPlots", "NBjets_AtBtagging"       , "" , **NBjets )


#================================================================================================
# Create Counter Objects
#================================================================================================
counter = histos.DrawObject( folder + "/counters/weighted", "counter", ""   , **wCounter )


#================================================================================================
# Function Definition
#================================================================================================
def DoPlots(histo, datasetObjects, savePostfix=""):

    p = plotter.Plotter(verbose, batchMode)
    p.AddDatasets(datasetObjects)
    p.AddDrawObject(histo)
    p.NormaliseHistos("toLuminosity")
    p.AddCmsText("fb", prelim=True)
    p.DatasetAsLegend(True)    
    p.Draw("") # "nostack"
    # p.DrawRatio("", "AP", "Data")
    # p.SetHistosFillStyle(3001)
    # p.Save()
    p.Save(savePath, saveFormats)
    # p.SaveAs(savePath, histo.GetName() + "_test", savePostfix, saveFormats)
    p.Exit()
    
    return


#================================================================================================
# Function Definition
#================================================================================================
def DoCounters(histo, datasetObjects, savePostfix=""):

    p = plotter.Plotter(verbose, batchMode)
    # p.SetupRoot(0, 4, 999, 2000)
    # p.SetupStatsBox("ksiourmen", xPos=0.90, yPos=0.88, width=0.20, height=0.12)
    p.AddDatasets(datasetObjects)
    p.AddDrawObject(histo)
    p.NormaliseHistos("toLuminosity")
    p.AddCmsText("fb", prelim=True)
    p.DatasetAsLegend(True)    
    # p.AddTF1("1000*cos(x)", 0, 200.0, False, {"lineColour": ROOT.kBlack})
    p.DrawRatio("", "AP", "Data")  # "AP,nostack"
    # p.Draw("") # "nostack"
    # p.SetHistosFillStyle(3001)
    p.SetHistoLabelsOption("d") #v, u, d
    p.SetHistoLabelsSizeX(0.5)
    p.SetHistoAxisOffsetX(0.02)
    # p.Save()
    p.Save(savePath, saveFormats)
    # p.SaveAs(savePath, histo.GetName() + "_test", savePostfix, saveFormats)
    p.Exit()
    
    return

#================================================================================================
def main():
    '''
    '''
    
    # Variables
    # histoList    = [AllElectronsEta, PassedElectronsEta]
    # histoList   = [AllElectronsPt, PassedElectronsPt]
    histoList   = [Njets_AtJetSelection, Njets_AfterJetSelections, NBjets_AtBtagging]
    counterList = [counter]

    
    ### Setup Datasets
    datasetManager = dataset.DatasetManager(opts.mcrab, analysis)
    datasetManager.LoadLuminosities("lumi.json")
    datasetManager.SetIntegratedLuminosity(intLumiInPb)
    
    ### Remove Datasets
    # datasetManager.Remove("MuonEG_Run2015D_05Oct2015_v2_246908_260426_25ns_Silver")     #  888.357
    datasetManager.Remove("MuonEG_Run2015C_25ns_05Oct2015_v1_246908_260426_25ns_Silver")  #   16.345
    datasetManager.Remove("MuonEG_Run2015D_PromptReco_v4_246908_260426_25ns_Silver")      # 1103.813
    datasetManager.Remove("ttHJetToNonbb_M125")
    # datasetManager.Remove("ST_s_channel_4f_leptonDecays")
    # datasetManager.Remove("ST_tW_antitop_5f_inclusiveDecays")
    # datasetManager.Remove("ST_tW_top_5f_inclusiveDecays")
    # datasetManager.Remove("ST_t_channel_antitop_4f_leptonDecays")
    # datasetManager.Remove("ST_t_channel_top_4f_leptonDecays")
    datasetManager.Remove("DYJetsToLL_M_10to50")
    datasetManager.Remove("DYJetsToLL_M_50")
    # datasetManager.Remove("TTJets")
    # datasetManager.Remove("WJetsToLNu")
    # datasetManager.Remove("WW")
    # datasetManager.Remove("WZ")
    # datasetManager.Remove("ZZ")

    ### Merge Datasets
    datasetManager.MergeData()
    datasetManager.MergeMany(datasetMapping)

    ### Print Datasets
    datasetManager.PrintSummary()
    # datasetManager.PrintDatasets()

    ### Get Datasets
    datasetObjects = datasetManager.GetAllDatasets()
    # datasetObjects = datasetManager.GetMCDatasets()
    # datasetObjects = [datasetManager.GetDataset("TTJets")]

    if verbose:
        datasetManager.PrintSelections("DYJetsToLL_M_10to50")

    
    # One Histogram on a given canvas (many datasets)
    auxObject.StartTimer("Histo Loop")
    #for h in histoList:
    #    DoPlots( h, datasetObjects)

    for c in counterList:
        DoCounters( c, datasetObjects)

        
    # Many Histograms on a given canvas (many datasets)
    # DoPlots( histoList, datasetObjects)
    

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
    #auxObject.PrintTimers()
