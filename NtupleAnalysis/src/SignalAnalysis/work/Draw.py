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
intLumiInPb   = 10000
saveFormats   = ["png"]
#savePath      = "/Users/attikis/Desktop/"
savePath      = "/afs/cern.ch/user/s/skonstan/public/html/"


#================================================================================================
# Object Definitions
#================================================================================================
auxObject  = aux.AuxClass(verbose)

mergeDict = {}
#mergeDict["ST_t_channel_top_4f_leptonDecays"]     = "Single t"
#mergeDict["ST_tW_antitop_5f_inclusiveDecays"]     = "Single t"
#mergeDict["ST_t_channel_antitop_4f_leptonDecays"] = "Single t"
#mergeDict["ST_tW_top_5f_inclusiveDecays"]         = "Single t"
#mergeDict["ST_s_channel_4f_leptonDecays"]         = "Single t"
#mergeDict["WW"] = "Diboson"
#mergeDict["WZ"] = "Diboson"
#mergeDict["ZZ"] = "Diboson"


removeList = []
removeList.append("MuonEG_Run2015D_05Oct2015_v2_246908_260426_25ns_Silver")
removeList.append("MuonEG_Run2015C_25ns_05Oct2015_v1_246908_260426_25ns_Silver")
removeList.append("MuonEG_Run2015D_PromptReco_v4_246908_260426_25ns_Silver")
#removeList.append("ttHJetToNonbb_M125")
removeList.append("ST_s_channel_4f_leptonDecays")
removeList.append("ST_tW_antitop_5f_inclusiveDecays")
removeList.append("ST_tW_top_5f_inclusiveDecays")
removeList.append("ST_t_channel_antitop_4f_leptonDecays")
removeList.append("ST_t_channel_top_4f_leptonDecays")
#removeList.append("DYJetsToLL_M_10to50")
#removeList.append("DYJetsToLL_M_50")
#removeList.append("TTJets")
#removeList.append("WJetsToLNu")
#removeList.append("WW")
#removeList.append("WZ")
#removeList.append("ZZ")


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


#================================================================================================
# Histogram Options
#================================================================================================
NumJets={
    "xLabel": "Numb Jets"           , "xUnits": "", "xMin": 0.00 , "xMax": 20, "binWidthX": None, "xCutLines": [], "xCutBoxes": [], "gridX": True, "logX": False,
    "yLabel": "Entries / %0.0f" , "yUnits": ""         , "yMin": 1E-01, "yMax": None , "binWidthY": None, "yCutLines": [], "yCutBoxes": [], "gridY": True, "logY": True,
    "ratioLabel": "Ratio", "yMinRatio": 0.0 , "yMaxRatio": 2.15 ,
    "logYRatio": False, "logXRatio": False, "xLegMin": 0.70, "xLegMax": 0.95, "yLegMin": 0.78, "yLegMax": 0.93, "gridXRatio": True, "gridYRatio": True,
}

NumLep={
    "xLabel": "Numb Lep"           , "xUnits": "", "xMin": 0.00 , "xMax": 15, "binWidthX": None, "xCutLines": [], "xCutBoxes": [], "gridX": True, "logX": False,
    "yLabel": "Entries / %0.0f" , "yUnits": ""         , "yMin": 1E-01, "yMax": None , "binWidthY": None, "yCutLines": [], "yCutBoxes": [], "gridY": True, "logY": True,
    "ratioLabel": "Ratio", "yMinRatio": 0.0 , "yMaxRatio": 2.15 ,
    "logYRatio": False, "logXRatio": False, "xLegMin": 0.70, "xLegMax": 0.95, "yLegMin": 0.78, "yLegMax": 0.93, "gridXRatio": True, "gridYRatio": True,
}

NumEvts={
    "xLabel": "Numb Evts"           , "xUnits": "", "xMin": 0.5 , "xMax": 1.5, "binWidthX": None, "xCutLines": [], "xCutBoxes": [], "gridX": True, "logX": False,
    "yLabel": "Entries / %0.0f" , "yUnits": ""         , "yMin": 1E03, "yMax": None , "binWidthY": None, "yCutLines": [], "yCutBoxes": [], "gridY": True, "logY": True,
    "ratioLabel": "Ratio", "yMinRatio": 0.0 , "yMaxRatio": 2.15 ,
    "logYRatio": False, "logXRatio": False, "xLegMin": 0.70, "xLegMax": 0.95, "yLegMin": 0.78, "yLegMax": 0.93, "gridXRatio": True, "gridYRatio": True,
}

NumEvts1={
    "xLabel": "Numb Evts"           , "xUnits": "", "xMin": 0.5 , "xMax": 1.5, "binWidthX": None, "xCutLines": [], "xCutBoxes": [], "gridX": True, "logX": False,
    "yLabel": "Entries / %0.0f" , "yUnits": ""         , "yMin": 1E06, "yMax": None , "binWidthY": None, "yCutLines": [], "yCutBoxes": [], "gridY": True, "logY":True,
    "ratioLabel": "Ratio", "yMinRatio": 0.0 , "yMaxRatio": 2.15 ,
    "logYRatio": False, "logXRatio": False, "xLegMin": 0.70, "xLegMax": 0.95, "yLegMin": 0.78, "yLegMax": 0.93, "gridXRatio": True, "gridYRatio": True,
}


Pt = {
    "xLabel": "p_{T}"           , "xUnits": "GeVc^{-1}", "xMin": 0.00 , "xMax": ptMax, "binWidthX": None, "xCutLines": [], "xCutBoxes": [], "gridX": True, "logX": False,
    "yLabel": "Entries / %0.0f" , "yUnits": ""         , "yMin": 1E-01, "yMax": None , "binWidthY": None, "yCutLines": [], "yCutBoxes": [], "gridY": True, "logY": True,
    "ratioLabel": "Ratio", "yMinRatio": 0.0 , "yMaxRatio": 2.15 ,
    "logYRatio": False, "logXRatio": False, "xLegMin": 0.70, "xLegMax": 0.95, "yLegMin": 0.78, "yLegMax": 0.93, "gridXRatio": True, "gridYRatio": True,
}

DEne = {
    "xLabel": "p_{T}"           , "xUnits": "GeVc^{-1}", "xMin": -100 , "xMax": 100, "binWidthX": None, "xCutLines": [], "xCutBoxes": [], "gridX": True, "logX": False,
    "yLabel": "Entries / %0.0f" , "yUnits": ""         , "yMin": 1E-01, "yMax": None , "binWidthY": None, "yCutLines": [], "yCutBoxes": [], "gridY": True, "logY": True,
    "ratioLabel": "Ratio", "yMinRatio": 0.0 , "yMaxRatio": 2.15 ,
    "logYRatio": False, "logXRatio": False, "xLegMin": 0.70, "xLegMax": 0.95, "yLegMin": 0.78, "yLegMax": 0.93, "gridXRatio": True, "gridYRatio": True,
}

Eta = {
    "xLabel": "#eta"           , "xUnits": "", "xMin": -1.5*etaMax, "xMax": +1.5*etaMax, "binWidthX": None, "xCutLines": [], "gridX": True, "gridXRatio": False, "logX": False,
    "yLabel": "Entries / %0.2f", "yUnits": "", "yMin": +1e00  , "yMax": None   , "binWidthY": None, "yCutLines": [] , "gridY": True, "gridYRatio": False, "logY": True ,
    "ratioLabel": "Ratio"      , "yMinRatio": 0.0, "yMaxRatio": 2.15 ,
    "logYRatio": False, "logXRatio": False,
    "xLegMin": 0.75, "xLegMax": 0.95, "yLegMin": 0.80, "yLegMax": 0.92
}


DEta = {
    "xLabel": "D #eta"           , "xUnits": "", "xMin": -etaMax, "xMax": etaMax, "binWidthX": None, "xCutLines": [ ], "gridX": True, "gridXRatio": False, "logX": False,
    "yLabel": "Entries /e_ %0.2f", "yUnits": "", "yMin": +1e00  , "yMax": None   , "binWidthY": None, "yCutLines": [] , "gridY": True, "gridYRatio": False, "logY": True ,
    "ratioLabel": "Ratio"      , "yMinRatio": 0.0, "yMaxRatio": 2.15 ,
    "logYRatio": False, "logXRatio": False,
    "xLegMin": 0.75, "xLegMax": 0.95, "yLegMin": 0.80, "yLegMax": 0.92
}

DPhi = {
    "xLabel": "Dphi"           , "xUnits": "", "xMin": -etaMax, "xMax": etaMax, "binWidthX": None, "xCutLines": [ ], "gridX": True, "gridXRatio": False, "logX": False,
    "yLabel": "Entries / %0.2f", "yUnits": "", "yMin": +1e00  , "yMax": None   , "binWidthY": None, "yCutLines": [] , "gridY": True, "gridYRatio": False, "logY": True ,
    "ratioLabel": "Ratio"      , "yMinRatio": 0.0, "yMaxRatio": 2.15 ,
     "logYRatio": False, "logXRatio": False,
    "xLegMin": 0.75, "xLegMax": 0.95, "yLegMin": 0.80, "yLegMax": 0.92
}

DR = {
    "xLabel": "DR"           , "xUnits": "", "xMin": 0, "xMax": +3*etaMax, "binWidthX": None, "xCutLines": [ ], "gridX": True, "gridXRatio": False, "logX": False,
    "yLabel": "Entries / %0.2f", "yUnits": "", "yMin": +1e00  , "yMax": None   , "binWidthY": None, "yCutLines": [] , "gridY": True, "gridYRatio": False, "logY": True ,
    "ratioLabel": "Ratio"      , "yMinRatio": 0.0, "yMaxRatio": 2.15 ,
    "logYRatio": False, "logXRatio": False,
    "xLegMin": 0.75, "xLegMax": 0.95, "yLegMin": 0.80, "yLegMax": 0.92
}

ImpPar = {
    "xLabel": "d0"           , "xUnits": "", "xMin": 0, "xMax": None, "binWidthX": None, "xCutLines": [ ], "gridX": True, "gridXRatio": False, "logX": False,
    "yLabel": "Entries / %0.2f", "yUnits": "", "yMin": 1.0 , "yMax": None   , "binWidthY": None, "yCutLines": [] , "gridY": True, "gridYRatio": False, "logY": True ,
    "ratioLabel": "Ratio"      , "yMinRatio": 0.0, "yMaxRatio": 2.15 ,
    "logYRatio": False, "logXRatio": False,
    "xLegMin": 0.75, "xLegMax": 0.95, "yLegMin": 0.80, "yLegMax": 0.92
}

MEt = {
    "xLabel": "MEt"           , "xUnits": "GeVc^{-1}", "xMin": 0.00 , "xMax": ptMax*3, "binWidthX": None, "xCutLines": [], "xCutBoxes": [], "gridX": True, "logX": False,
    "yLabel": "Entries / %0.0f" , "yUnits": ""         , "yMin": 1E-01, "yMax": None , "binWidthY": None, "yCutLines": [], "yCutBoxes": [], "gridY": True, "logY": True,
    "ratioLabel": "Ratio", "yMinRatio": 0.0 , "yMaxRatio": 2.15 ,
    "logYRatio": False, "logXRatio": False, "xLegMin": 0.70, "xLegMax": 0.95, "yLegMin": 0.78, "yLegMax": 0.93, "gridXRatio": True, "gridYRatio": True,
}

wCounter = {
    "xMin": 7.0, "xMax": None, "gridX": True, "gridXRatio": True, "logX": False,
    "yLabel": "Events / %0.1f", "yMin": 1.0, "yMax": None, "yUnits": "", "yCutLines": [], "gridY": True,  "gridYRatio": True, "logY": True, "yCutBoxes": [], "xCutBoxes": [],
    "ratioLabel": "Ratio", "yMinRatio": 0.0, "yMaxRatio": 2.15 ,  "logYRatio": False, "logXRatio": False,
    "xLegMin": 0.75, "xLegMax": 0.95, "yLegMin": 0.80, "yLegMax": 0.92,
}

PassedEvts = {
    "xLabel": "" , "xUnits": "", "xMin": 0, "xMax": 5, "binWidthX": None, "xCutLines": [ ], "gridX": True, "gridXRatio": False, "logX": False,
    "yLabel": "Entries / %0.2f", "yUnits": "", "yMin": +1e00  , "yMax": None   , "binWidthY": None, "yCutLines": [] , "gridY": True, "gridYRatio": False, "logY": True ,
    "ratioLabel": "Ratio"      , "yMinRatio": 0.0, "yMaxRatio": 2.15 ,
    "logYRatio": False, "logXRatio": False,
    "xLegMin": 0.75, "xLegMax": 0.95, "yLegMin": 0.80, "yLegMax": 0.92
}
MVA={
    "xLabel": "MVA"           , "xUnits": "", "xMin":-0.5, "xMax": 1.5, "binWidthX": None, "xCutLines": [], "xCutBoxes": [], "gridX": True, "logX": False,
    "yLabel": "Entries / %0.0f" , "yUnits": ""         , "yMin": 1E-01, "yMax": None , "binWidthY": None, "yCutLines": [], "yCutBoxes": [], "gridY": True, "logY": True,
    "ratioLabel": "Ratio", "yMinRatio": 0.0 , "yMaxRatio": 2.15 ,
    "logYRatio": False, "logXRatio": False, "xLegMin": 0.70, "xLegMax": 0.95, "yLegMin": 0.78, "yLegMax": 0.93, "gridXRatio": True, "gridYRatio": True,
}
 
#================================================================================================                                                                                                                      

#================================================================================================
# Create Histos Objects
#================================================================================================
hAllMLepPt_op = histos.DrawObject( folder, "AllMLepPt_op" , "all", **Pt )
hAllMLepPt_same = histos.DrawObject( folder, "AllMLepPt_same" , "all", **Pt )
hAllMLepJPt_op  = histos.DrawObject( folder, "AllMLepJPt_op" , "all", **Pt )
hAllMLepJPt_same  = histos.DrawObject( folder, "AllMLepJPt_same" , "all", **Pt )
hPassedMLepNJets_op = histos.DrawObject( folder,"PassedMLepNJets_op","passed",**NumJets )
hPassedMLepNJets_same = histos.DrawObject( folder,"PassedMLepNJets_same","passed",**NumJets )
hAllMLepNJets_op = histos.DrawObject( folder,"AllMLepNJets_op","all",**NumJets)
hAllMLepNJets_same = histos.DrawObject( folder,"AllMLepNJets_same","all",**NumJets)
hAllMET=histos.DrawObject( folder, "AllMET" , "all", **MEt )
hMLepMET=histos.DrawObject( folder, "MLepMET" , "all", **MEt )
hMETcut=histos.DrawObject( folder, "METcut" , "all", **MEt )
hAllMLepEta_op=histos.DrawObject(folder,"AllMLepEta_op","all",**Eta)
hAllMLepEta_same=histos.DrawObject(folder,"AllMLepEta_same","all",**Eta)
hAllMLepJEta_op=histos.DrawObject(folder,"AllMLepJEta_op","all",**Eta)
hAllMLepJEta_same=histos.DrawObject(folder,"AllMLepJEta_same","all",**Eta)
hAllMLepleadLepPt_op=histos.DrawObject(folder,"AllMLepleadLepPt_op","all",**Pt)
hAllMLepleadLepPt_same=histos.DrawObject(folder,"AllMLepleadLepPt_same","all",**Pt)
hAllMLepsubleadLepPt_op=histos.DrawObject(folder,"AllMLepsubleadLepPt_opposite","all",**Pt)
hAllMLepsubleadLepPt_same=histos.DrawObject(folder,"AllMLepsubleadLepPt_same","all",**Pt)
hAllMLepNLep_op=histos.DrawObject(folder,"AllMLepNLep_op","all",**NumLep)
hAllMLepNLep_same=histos.DrawObject(folder,"AllMLepNLep_same","all",**NumLep)
hAllMLepNBotToLep_op=histos.DrawObject(folder,"AllMLepNBotToLep_op","all",**NumLep)
hAllMLepNBotToLep_same=histos.DrawObject(folder,"AllMLepNBotToLep_same","all",**NumLep)

hPassedMLepNLep_op=histos.DrawObject(folder,"PassedMLepNLep_op","passed",**NumLep)
hPassedMLepNLep_same=histos.DrawObject(folder,"PassedMLepNLep_same","passed",**NumLep)
hPassedMLepPt_op= histos.DrawObject( folder, "PassedMLepPt_op" , "passed", **Pt )
hPassedMLepPt_same= histos.DrawObject( folder, "PassedMLepPt_same" , "passed", **Pt )
hMLep_MET_op=histos.DrawObject( folder, "MLepMET_op" , "all", **MEt )
hMLep_MET_same=histos.DrawObject( folder, "MLepMET_same" , "all", **MEt )


numlep=histos.DrawObject(folder,"numlep","all",**NumLep)

hW62Pt=histos.DrawObject(folder,"W62Pt","all",**Pt)
hJets_DEne=histos.DrawObject(folder, "Jets_DEne","all", **DEne)
hJets_DEta=histos.DrawObject(folder, "Jets_DEta","all", **DEta)
hJets_DPhi=histos.DrawObject(folder, "Jets_DPhi","all", **DPhi)
hJets_DR=histos.DrawObject(folder, "Jets_DR","all", **DR)
hLepImpPar=histos.DrawObject(folder,"LepImpPar","all",**ImpPar)

hJets_DEne_lt10=histos.DrawObject(folder, "Jets_DEne_lt10","all", **DEne)
hJets_DEne_10_25=histos.DrawObject(folder, "Jets_DEne_10_25","all", **DEne)
hJets_DEne_25_40=histos.DrawObject(folder, "Jets_DEne_25_40","all", **DEne)
hJets_DEne_40_55=histos.DrawObject(folder, "Jets_DEne_40_55","all", **DEne)
hJets_DEne_55_70=histos.DrawObject(folder, "Jets_DEne_55_70","all", **DEne)
hJets_DEne_70_85=histos.DrawObject(folder, "Jets_DEne_70_85","all", **DEne)
hJets_DEne_85_100=histos.DrawObject(folder, "Jets_DEne_85_100","all", **DEne)
hJets_DEne_gt100=histos.DrawObject(folder, "Jets_DEne_gt100","all", **DEne)

hPassedEvents=histos.DrawObject(folder,"PassedEvents","passed",**PassedEvts)

hMVA_EleFromW=histos.DrawObject(folder,"MVA_EleFromW","passed",**MVA)
hMVA_EleFromBot=histos.DrawObject(folder,"MVA_EleFromBot","passed",**MVA)
hMVA_EleFake=histos.DrawObject(folder,"MVA_EleFake","passed",**MVA)


hAllMLepleadLepPt=histos.DrawObject(folder,"AllMLepLeadLepPt","all",**Pt)
hAllMLepsubleadLepPt=histos.DrawObject(folder,"AllMLepSubleadLepPt","all",**Pt)

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
    p.NormaliseHistos("toLuminosity") #
    p.AddCmsText("fb", prelim=True)
    p.DatasetAsLegend(True) 
    p.Draw("A,P,nostack") #, "A,P,nostack", "ttHJetToNonbb_M125")
    #p.Draw("nostack")  #",HIST,9,nostack,<dataset>"
    p.SetHistoLabelsSizeX(0.5)
    #p.SetHistosFillStyle(3001)
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
    # p.Draw("HIST,9")
    p.Draw("HIST,9") #, "A,P,nostack", "Data")
    # p.SetHistosFillStyle(3001)
    p.SetHistoLabelsOption("d") #v, u, d
    p.SetHistoLabelsSizeX(0.5)
    # p.SetHistoAxisOffsetX(0.03)

    # p.Save()
    p.Save(savePath, saveFormats)
    # p.SaveAs(savePath, histo.GetName() + "_test", savePostfix, saveFormats)
    p.Exit()
    
    return

#================================================================================================
def main():
    '''
    '''
    
    ### Define Lists
    #xxx
    #histoList = [hAllMLepPt_op, hAllMLepJPt_op, hAllMLepEta_op, hAllMLepJEta_op,  hAllMLepleadLepPt_op, hAllMLepsubleadLepPt_op, hAllMLepNLep_op]
    #histoList = [hAllMLepPt_same, hAllMLepJPt_same, hAllMLepEta_same, hAllMLepJEta_same,  hAllMLepleadLepPt_same, hAllMLepsubleadLepPt_same, hAllMLepNLep_same]
    #histoList=[numlep,hAllMET,hAllMLepNBotToLep_op,hAllMLepNBotToLep_same,hLepImpPar,hPassedMLepNLep_op, hPassedMLepNLep_same, hPassedMLepPt_op, hPassedMLepPt_same]              
    #histoList=[ hJets_DEne, hJets_DEta, hJets_DPhi, hJets_DR,hLepImpPar, hJets_DEne_lt10, hJets_DEne_10_25, hJets_DEne_25_40, hJets_DEne_40_55, hJets_DEne_55_70, hJets_DEne_70_85, hJets_DEne_85_100, hJets_DEne_gt100]
    histoList =[hAllMET, hMLepMET, hPassedEvents]
    #histoList = [hMVA_EleFromW,hMVA_EleFromBot, hMVA_EleFake,hAllMLepNJets_op,hAllMLepNJets_same,hAllMLepleadLepPt,hAllMLepsubleadLepPt]
    counterList = [counter]
    
    
    ### Setup Datasets
    datasetManager = dataset.DatasetManager(opts.mcrab, analysis)
    datasetManager.LoadLuminosities("lumi.json")


    
    ### Remove Datasets
    datasetManager.Remove(removeList)
    datasetManager.SetIntLuminosity(intLumiInPb)
    
    ### Merge Datasets
    #datasetManager.MergeData()
    #datasetManager.MergeMany(mergeDict)

    
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
    for h in histoList:
        DoPlots( h, datasetObjects)

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
