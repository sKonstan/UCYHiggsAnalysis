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

import UCYHiggsAnalysis.NtupleAnalysis.pyROOT.multicrab as multicrab
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
ratio         = True
energy        = "13"
folder        = "Kinematics"
saveFormats   = ["png"]
savePath      = ""
#pi = 4*math.atan(1)


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


#================================================================================================
# Create Histos OBjects
#================================================================================================
AllElectronsPt      = histos.TH1orTH2( folder, "AllElectronsPt"   , "all"    , None, **Pt )
PassedElectronsPt   = histos.TH1orTH2( folder, "PassedElectronsPt", "passed ", None, **Pt )

AllElectronsEta     = histos.TH1orTH2( folder, "PassedElectronsPt", "Canvas Legend", None, **Eta )
PassedElectronsEta  = histos.TH1orTH2( folder, "PassedElectronsPt", "Canvas Legend", None, **Eta )


#================================================================================================
# Function Definition
#================================================================================================
def DoPlots(histo, datasetObjects, bColourPalette=False, saveExt=""):

    p = plotter.Plotter( Verbose=False, BatchMode=True )
    p.SetBoolUseDatasetAsLegEntry(bColourPalette)
    p.AddDatasets(datasetObjects)

    if (len(datasetObjects) > 1):
        p.SetBoolUseDatasetAsLegEntry(True)
    else:
        p.SetBoolUseDatasetAsLegEntry(False)

    p.EnableColourPalette(bColourPalette)
    p.AddHisto(histo)
    p.SetupStatsBox(-1, -1, -1, -1, 000000000)
    p.SetupStatsBox()
    p.Draw(THStackDrawOpt="nostack", bStackInclusive = False, bAddReferenceHisto = True)
    p.SetTLegendHeader("test", "" )
    p.SaveHistos(True, savePath, saveFormats, saveExt)
    return


#================================================================================================
def main():
    '''
    '''

    args         = {}
    datasetObjects = []
    histoList    = [PassedElectronsPt, AllElectronsPt]
    mcrab        = multicrab.Multicrab(verbose=False)
    datasetNames = mcrab.GetDatasetsFromMulticrabDir(opts.mcrab, **args)
    
    for dName in datasetNames:
        rootFile = mcrab.GetDatasetRootFile(opts.mcrab, dName)
        dObject  = dataset.Dataset(dName, energy, rootFile, verbose=False, **args)
        datasetObjects.append(dObject)

    for h in histoList:
        DoPlots( h, datasetObjects, True )
        break



#================================================================================================
if __name__ == "__main__":

    parser = OptionParser(usage="Usage: %prog [options]",add_help_option=False,conflict_handler="resolve")
    parser.add_option("-m", "--mcrab"  , dest="mcrab"  , action="store", help="Path to the multicrab directory for input")
    parser.add_option("-d", "--dataset", dest="dataset", action="store", help="Name of the dataset to be plotted")
    #parser.add_option("-e", "--error"  , dest="errorlevel", action="store", help="Maximum relative uncertainty per bin (default=10%%)", default=0.10)
    (opts, args) = parser.parse_args()

    if opts.mcrab == None:
        raise Exception("Please provide input multicrab directory with -m")
    if not os.path.exists(opts.mcrab):
        raise Exception("The input root file '%s' does not exist!" % opts.mcrab)
    #if opts.dataset == None:
    #    raise Exception("Please provide dataset name with -d")

    main()

        
#########################################################
