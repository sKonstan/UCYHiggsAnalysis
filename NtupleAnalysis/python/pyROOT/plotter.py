#================================================================================================
# All imported modules
#================================================================================================
# System modules
import os, sys
import array
import math
import copy
import inspect
import glob
from optparse import OptionParser
import itertools
import numpy
from array import array
import re
import collections

import ROOT
from ROOT import std

import UCYHiggsAnalysis.NtupleAnalysis.pyROOT.text as text
import UCYHiggsAnalysis.NtupleAnalysis.pyROOT.aux as aux
import UCYHiggsAnalysis.NtupleAnalysis.pyROOT.histos as histos
import UCYHiggsAnalysis.NtupleAnalysis.pyROOT.tdrstyle as tdrstyle
from UCYHiggsAnalysis.NtupleAnalysis.pyROOT.dataset import Dataset
from UCYHiggsAnalysis.NtupleAnalysis.pyROOT.dataset import DatasetMerged


#================================================================================================
# Define class
#================================================================================================
class Plotter(object): 
    def __init__(self, verbose=False, batchMode=True):
        self.verbose           = verbose
        self.batchMode         = batchMode
        self.textObject        = text.TextClass(verbose)
        self.auxObject         = aux.AuxClass(verbose)
        self.drawList          = []
        self.drawListRatio     = []
        self.canvasFactor      = 1.25
        self.padDivisionPoint  = 1-1/self.canvasFactor
        self.THStackData       = ROOT.THStack("THStackData"    , "Stack of Data Histos")
        self.THStackMC         = ROOT.THStack("THStackMC"      , "Stack of MC Histos")
        self.THStackRatio      = ROOT.THStack("THStackRatio"   , "Stack of Ratio Histos")
        self.TMultigraph       = ROOT.TMultiGraph("TMultigraph", "ROOT.TMultiGraph holding various ROOT.TGraphs")
        self.MergedDatasets    = []
        self.McDatasets        = []
        self.DataDatasets      = []
        self.SetupRoot()
        return
    
    
    def GetDataDatasets(self):
        '''
        Return a list with all "Data"-type Dataset objects 
        '''
        self.Verbose()
        return self.DataDatasets

    
    def GetMergedDatasets(self):
        '''
        Return a list with all "Data"-type Dataset objects 
        '''
        self.Verbose()
        return self.MergedDatasets
    

    def GetMcDatasets(self):
        '''
        Return a list with all "MC"-type Dataset objects 
        '''
        self.Verbose()
        return self.McDatasets

    
    def GetDatasets(self):
        '''
        Return a list with all "MC"-type Dataset objects 
        '''
        self.Verbose()
        return self.Datasets
        

    def _GetRatioReferenceHisto(self, refDataset):
        self.Verbose()

        if refDataset.lower() == "data":
            histo  = None
            colour = None
            for d in self.GetDataDatasets():
                if histo == None:
                    histo  = copy.deepcopy(d.histo.THisto)
                    colour = d.histo.THisto.GetLineColor()
                else:
                    histo.Add(d.histo.THisto)
            return (histo, colour)
        else:
            for h in self.GetHistos():
                if h.dataset.name == refDataset:
                    histo  = copy.deepcopy(h.THisto)
                    colour = h.THisto.GetLineColor()
                    return (histo, colour)
        raise Exception("Cannot call DrawRatio(). The reference dataset '%s' cannot be found!" % (refDataset) )


    def _DrawHistos(self, stackOpts):
        '''
        Draw the THDumbie, draw the THStack and update the canvas.

        Drawing options: http://root.cern.ch/root/html/THistPainter.html
        '''
        self.Verbose("Drawing Histogram Stack")

        if hasattr(self, 'TPadPlot'):
            self.TPadPlot.cd()

        if "nostack" in stackOpts:
            pass
        elif "stack" in stackOpts:
            raise Exception("Unexplained THStack behaviour with options \"stack\". Use \"\" instead to have histograms painted stacked on top of each other")
            
        self.THDumbie.THisto.Draw()
        self.THStackMC.Draw(self.GetDrawOpts() + ", same")
        self.THStackData.Draw("AP,same,e1")
        self.UpdateCanvas()
        return


    def _DrawHistosRatio(self, stackOpts):
        '''
        Draw the THRatio, draw the THStackRatio and update the canvas.

        Drawing options: http://root.cern.ch/root/html/THistPainter.html
        '''
        self.Verbose("Drawing Histogram Stack")

        if not hasattr(self, 'TPadRatio'):
            raise Exception("Cannot draw ratio histograms. A dedicaded TPad was not created.")

        self.TPadRatio.cd()
        self.THRatio.THisto.Draw()
        self.THStackRatio.Draw(self.GetDrawOptsRatio() + ", same")
        self.UpdateCanvas()
        return
        
        
    def DatasetAsLegend(self, flag):
        self.Verbose()
        self.DatasetInLegend = flag
        return

    
    #================================================================================================
    def Verbose(self, message=""):
        '''
        Custome made verbose system. Will print all messages in the messageList
        only if the verbosity boolean is set to true.
        '''
        if self.verbose:
            print "=== %s:" % (self.__class__.__name__ + "." + sys._getframe(1).f_code.co_name + "()")
            if message!="":
                print "\t", message
        return


    def Print(self, message=""):
        '''
        Custome made print system. Will print the message even if the verbosity boolean is set to false.
        '''
        print "=== %s:" % (self.__class__.__name__ + "." + sys._getframe(1).f_code.co_name + "()")
        if message!="":
            print "\t", message
        return

    
    def PrintList(self, messageList=[""], printSelf=True):
        '''
        Custome made print system. Will print all messages in the messageList even if the verbosity boolean is set to false.
        '''
        for counter, message in enumerate(messageList):
            if counter == 0 and printSelf:
                self.Print(message)
            else:
                print "\t", message
        return


    def PrintWarning(self, msg, keystroke):
        '''                                                                                                                                                          
        Print a warning and make sure user sees it by requiring a keystroke
        '''
        self.Print()
        
        response = raw_input("\tWARNING! " + msg + ". Press \"%s\" to quit, any other key to proceed: " % (keystroke))
        if response== "q":
            sys.exit()
        else:
            return
        return
    
        
    def PrintAttributes(self):
        '''
        Call this function to print all class attributes.
        '''
        self.Print("Attributes: %s" % (self.__dict__))
        return


    def SetAttribute(self, attr, value):
        '''
        I should avoid using this function and instead write functions dedicated to Setting or Getting 
        a specific class variable value. The reason? Well, in principle there are no private variables in python, 
        so you can access all variables directly without getters and set them via setattr or directly if they are already initialized.

        But there are 2 good reasons for writing specific functions:
        1) Documentation in terms of user interface. Writing explicit getters and setters keeps your code clean 
        and contained and discourages wild editing of values
        
        2) speed of code (setattr looks through a list of strings to find the variable)
        ''' 
        self.Verbose()
        return setattr(self, attr, value)

    
    def GetAttribute(self, attr):
        '''
        I should avoid using this function and instead write functions dedicated to Setting or Getting 
        a specific class variable value. The reason? Well, in principle there are no private variables in python, 
        so you can access all variables directly without getters and set them via setattr or directly if they are already initialized.

        But there are 2 good reasons for writing specific functions:
        1) Documentation in terms of user interface. Writing explicit getters and setters keeps your code clean 
        and contained and discourages wild editing of values
        
        2) speed of code (setattr looks through a list of strings to find the variable)
        ''' 
        self.Verbose()
        if hasattr(self, attr):
            return getattr(self, attr)
        else:
            raise Exception("Class object does not have attribute '%s'" % (attr))
    
    
    def _CreateCanvas(self, twoPads=False):
        '''
        Create a name for a TCanvas and then create it. 
        This name will later on be used to save the canvas under a user specific format ("png", "pdf", "eps", etc..)
        '''                    
        self.Verbose()

        if hasattr(self, 'TCanvas'):
            return
            #raise Exception("The class object already has a 'TCanvas' attribute.")


        # First customise all histograms (otherwise cannot create THDumbie)
        self.CustomiseHistos()

        self.THDumbie = self.CreateDumbieHisto("THDumbie")
        canvasName    = "Canvas:"+self.THDumbie.GetAttribute("name")

        if not twoPads:
            self.Verbose("Creating a TCanvas with name '%s'" % (self.THDumbie.GetAttribute("name")) )
            self.TCanvas = ROOT.TCanvas( canvasName, canvasName, 1)
            self.TCanvas.cd()
        else:
            self.Verbose("Creating a 2-pad TCanvas with name '%s'" % (self.THDumbie.GetAttribute("name")) )
            self.THRatio = self.CreateDumbieHisto("THRatio")
            self._CustomiseTHRatio()
            self.TCanvas = ROOT.TCanvas( canvasName, canvasName, ROOT.gStyle.GetCanvasDefW(), int(ROOT.gStyle.GetCanvasDefH()*self.canvasFactor))
            self.TCanvas.Divide(1,2)
            self.THDumbie.RemoveBinLabelsX()
            self.THDumbie.RemoveTitleX()
            self._CreateTPads()
            self.TPadPlot.cd()

        self._SetGridAxes(twoPads)
        self._SetLogAxes(twoPads)
        self._CreateLegend()
        self.UpdateCanvas()
        return


    def _CreateTPads(self):
        '''
        Create the plot, ratio and cover pads.
        '''
        self.Verbose()

        self._CreateTPadPlot()
        self._CreateTPadRatio()
        self._CreateTPadCover()
        return


    def SetupStatsBox(self, options, xPos=0.94, yPos=0.84, width=0.20, height=0.12):
        '''
        The parameter mode can be = ksiourmen  (default = 000001111)
        k = 1 (2); kurtosis printed (kurtosis and kurtosis error printed)
        s = 1 (2); skewness printed (skewness and skewness error printed)
        i = 1 (2); integral of bins printed (integral of bins with option "width" printed)
        o = 1;     number of overflows printed
        u = 1;     number of underflows printed
        r = 1 (2); rms printed (rms and rms error printed)
        m = 1 (2); mean value printed (mean and mean error values printed)
        e = 1;     number of entries printed
        n = 1;     name of histogram is printed
    
        Example: 
        gStyle->SetOptStat(11);
        prints only name of histogram and number of entries.
        '''
        self.Verbose()

        # Beautifications/Styling
        ROOT.gStyle.SetStatBorderSize(0)
        ROOT.gStyle.SetStatColor(ROOT.kWhite)
        ROOT.gStyle.SetStatStyle(0) # 3001
        ROOT.gStyle.SetStatTextColor(ROOT.kBlack)
        ROOT.gStyle.SetStatFontSize(15)
        
        # Dimensions
        ROOT.gStyle.SetStatY(yPos)
        ROOT.gStyle.SetStatX(xPos)
        ROOT.gStyle.SetStatW(width)
        ROOT.gStyle.SetStatH(height)
        ROOT.gStyle.SetOptStat(options)
        return

    
    def SetupRoot(self, optStat=0, maxDigits=4, nContours=999, errIgnoreLevel=2000):

        '''
        Setup ROOT before doing anything else. Reset ROOT settings, disable statistics box,
        apply Techical Design Report (TDR) style.

        The available options for the Error-Ignore-Level are (const Int_t):
        kUnset    =  -1
        kPrint    =   0
        kInfo     =   1000
        kWarning  =   2000
        kError    =   3000
        kBreak    =   4000
        kSysError =   5000
        kFatal    =   6000

        NOTE: 
        When you are NOT in batch mode (self.batchMode = False), a canvas creation generates a window.
        '''
        self.Verbose()
        if hasattr(self, 'rootIsSet'):
            self.Print("ROOT already set. Doing nothing")
            return

        self.Verbose("Resetting ROOT, setting TDR style, and setting:")

        info   = []
        align  = "{:<15} {:<10}"
        info.append( align.format("OptStat"        , ": " + str( optStat) ) )
        info.append( align.format("MaxDigits"      , ": " + str( maxDigits) ) ) 
        info.append( align.format("NumberContours" , ": " + str( nContours) ) )
        info.append( align.format("gerrIgnoreLevel", ": " + str( errIgnoreLevel) ) )
        if (self.verbose):
            self.PrintList(info, False)
        
        ROOT.gROOT.Reset()
        ROOT.gROOT.SetBatch(self.batchMode)
        ROOT.gStyle.SetOptStat(optStat)
        ROOT.gStyle.SetNumberContours(nContours)
        ROOT.TGaxis.SetMaxDigits(maxDigits)
        ROOT.gErrorIgnoreLevel = errIgnoreLevel
        tdrstyle.TDRStyle()
        self.rootIsSet = True
        
        return


    def GetHistoFromFile(self, rootFile, histo):
        '''
        '''
        self.Verbose("Getting histogram '%s' from '%s'" % (histo.name, rootFile.GetName()) )

        if histo.path == "":
            prefix = ""
        else:
            prefix = histo.path + "/"
        histoPath = prefix + histo.name
        return rootFile.Get(histoPath)


    def CustomiseHistos(self):
        self.Verbose("Customising all histograms")

        if not hasattr(self, 'histosNormed'):
            raise Exception("Cannot customise histograms. Need to call first NormaliseHistos() and then CustomiseHistos()")

        for d in self.Datasets:
            d.histo.ApplyStyles()
        return

    
    def NormaliseHistos(self, normOption):
        self.Verbose("Normalising all histograms '%s'" % (normOption) )
    
        if not hasattr(self, 'Datasets'):
            raise Exception("Cannot normalise histograms as no datasets exist. Check that you have added some datasets")
            
        for dataset in self.Datasets:
            self._NormaliseHisto(dataset, normOption)

        self.histosNormed = True
        self.normOption   = normOption
        return


    def _NormaliseHisto(self, dataset, normOpt):
        '''
        Normalise the histoObject passed to this function according to user-specified criteria. 
        '''
        self.Verbose()

        if dataset.histo==None:
            raise Exception("The dataset '%s' has no histograms assigned to it" % (dataset.GetName()) )
        
        normOpts = ["", "toOne", "byXSection", "toLuminosity"]
        if normOpt not in normOpts:
            raise Exception("Unsupported option '%s'. Please choose one of the following options:\n\t \"%s\"" % (normOpt, "\", \"".join(opt for opt in normOpts) ) )

        if normOpt == "":
            return
        elif normOpt == "toOne":
            dataset.histo.NormaliseToOne()
            return
        elif normOpt == "byXSection":
            if dataset.GetIsData():
                return
            dataset.histo.NormaliseToFactor( dataset.GetNormFactor() )
        elif normOpt == "toLuminosity":
            if dataset.GetIsData():
                return
            dataset.histo.NormaliseToFactor( dataset.GetNormFactor() * dataset.GetIntLuminosity() )
        else:
            raise Exception("Unknown histoObject normalisation option '%s'.!" % (dataset.histo.normalise))
        return


    def GetLegLabel(self, hObject):
        '''
        '''
        self.Verbose()
        
        if not hasattr(self, 'DatasetInLegend'):
            return hObject.GetAttribute("legLabel")
        else:
            if self.DatasetInLegend:
                return hObject.GetAttribute("dataset").GetLatexName()


    def GetLegOptions(self):
        self.Verbose()
        
        if "HIST" in self.GetDrawOpts():
            return "F"
        else:
            return "LP"


    def GetLegOptionsRatio(self):
        self.Verbose()
        
        if "HIST" in self.GetDrawOptsRatio():
            return "F"
        else:
            return "LP"
        

    def AddDataset(self, dataset):
        '''
        Add a new dataset and associate it to a root file.
        '''
        self.Verbose()
        
        if not hasattr(self, 'Datasets'):
            self.Datasets = []
        
        self.Verbose("Adding dataset \"%s\" (%s) to dataset list" % (dataset.GetName(), type(dataset).__name__))        

        # Append dataset to apppropriate dataset list
        self.Datasets.append(dataset)
        if dataset.GetIsMC():
            self.McDatasets.append(dataset)
        else:
            self.DataDatasets.append(dataset)
        return


    def AddDatasets(self, datasetObjects):
        '''
        Add all datasets in the datasetObjects list to the plotter
        '''
        self.Verbose("Adding '%s' Datasets (or DatasetMerged) objects to the plotter object" % (len(datasetObjects) ) )

        for dm in datasetObjects:
            if isinstance(dm, Dataset):
                self.AddDataset(dm)
            elif isinstance(dm, DatasetMerged):
                self.MergedDatasets.append(dm)
                for d in dm.GetDatasets():
                    self.AddDataset(d)
            else:
                raise Exception("Cannot add object of type \"%s\" to dataset list" % (type(dm)))
        return


    def AddCmsText(self, lumiUnits = "fb", prelim=True):
        '''
        Add the default CMS text on the canvas. Several defaults are available. 
        For available options see the class TextClass(object) under tools/text.py.
        '''
        self.Verbose("Adding CMS Text to draw object list")
        
        if hasattr(self, 'TPadPlot'):
            self.TPadPlot.cd()

        if prelim:
            self.textObject.AddDefaultText("preliminary", "")
        else:
            self.textObject.AddDefaultText("publication", "")

        lumi = -1
        for d in self.GetDatasets():
            energy  = d.GetEnergyString()
            intLumi = d.GetIntLumiString(lumiUnits)
            if lumi < 0:
                lumi = intLumi
            elif lumi != intLumi:
                print d.GetName()
            
        self.textObject.AddDefaultText("lumi"  , lumi  )
        self.textObject.AddDefaultText("energy", energy)
        self.ExtendDrawLists(self.textObject.GetTextList(), addToRatio=False)        
        return
    

    def _IsValidSavePath(self, savePath):
        '''
        Make sure that the parameter "savePath" is a valid path and ends with at "/"
        '''
        if not isinstance(savePath, str):
            raise Exception("The save path '%s' is not an instance of string! Please make sure the path provided is a string." % (savePath) )
        
        if savePath=="":
            return

        if not savePath.endswith("/"):
            savePath += "/" 
        if not os.path.exists(savePath):
            raise Exception("The path '%s' does not exist! Please make sure the provided path is correct." % (savePath) )
        return


    def GetDatasets(self):
        self.Verbose()
        return self.Datasets

    
    def GetDatasetNames(self):
        self.Verbose()
        dNames = []
        for d in self.GetDatasets():
            dNames.append( d.GetName() )
        return dNames
    
        
    def SetLegendHeader(self, text):
        self.Verbose()
        self.TLegend.SetHeader(text)
        return

    
    def GetHistos(self):
        self.Verbose()
        hList = []
        for d in self.Datasets:
            hList.append(d.histo)
        return hList
    
    
    def _SaveAs(self, savePath, saveName, saveFormats=["png", "C", "eps", "pdf"]):
        '''
        Loop over all formats and save the canvas to 
        '''
        self.Verbose()

        if saveName!=None:
            saveName = savePath + saveName
        else:
            saveName = savePath + self.TCanvas.GetName().split(":")[-1]

        self.TCanvas.SetName(saveName)
        self.UpdateCanvas()
            
        for ext in saveFormats:
            name =  saveName + "." + ext
            self.TCanvas.SaveAs(name)
            print "\t%s" % name
        return

    
    def SaveAs(self, savePath=os.getcwd() + "/", saveName="", savePostfix="", saveFormats=["png", "C", "eps", "pdf"]):
        '''
        Save canvas to a specified path and with the desirable format.
        '''
        self.Print()
        
        if not hasattr(self, 'TCanvas'):
            raise Exception("Cannot save TCanvas. You first have to create one")
                
        self._IsValidSavePath(savePath)
        self._SaveAs(savePath, saveName, saveFormats)
        return


    def Save(self, savePath=os.getcwd() + "/", saveFormats=["png", "eps", "pdf"]):
        '''
        Save canvas with the default canvas (histogram) name to the current working directory
        '''
        self.Print()
        
        if not hasattr(self, 'TCanvas'):
            raise Exception("Cannot save TCanvas. You first have to create one")

        self._IsValidSavePath(savePath)
        self._SaveAs(savePath, None, saveFormats)
        return



    def Exit(self, keepAlive=False):
        self.Verbose()
        self.IsBatchMode()
        return
    

    def GetHistosYMinYMax(self):
        '''
        Loops over all histograms in datasets. Find the minimum y-axis value
        '''
        self.Verbose()

        yMin = +1E20
        yMax = -1E20

        for dataset in self.Datasets:
            h      = dataset.histo
            tmpMin =  h.THisto.GetMinimum()
            tmpMax =  h.THisto.GetMaximum()

            if tmpMin < yMin:
                yMin = h.yMin

            if tmpMax > yMax:
                yMax = h.yMax

        return yMin, yMax

    
    def _SetLogAxes(self, twoPads=False):
        self.Verbose()
        self._SetLogY()
        self._SetLogX()
        self._SetLogZ()
        if twoPads:
            self._SetLogXRatio()
            self._SetLogYRatio()
        return

    
    def _SetGridAxes(self, twoPads=False):
        self.Verbose()
        if twoPads:
            self.TPadPlot.SetGridx(self.THDumbie.gridX)
            self.TPadPlot.SetGridy(self.THDumbie.gridY)
            self.TPadRatio.SetGridx(self.THDumbie.gridXRatio)
            self.TPadRatio.SetGridy(self.THDumbie.gridYRatio)
        else:
            self.TCanvas.SetGridx(self.THDumbie.gridX)
            self.TCanvas.SetGridy(self.THDumbie.gridY)
        return


    def _SetLogX(self):
        self.Verbose()

        if self.THDumbie.logX==False:
            return    
        if self.THDumbie.THisto.GetXaxis().GetXmin() > 0:
            self.TCanvas.SetLogx(True)
            if hasattr(self, 'TPadPlot'):
                self.TPadPlot.SetLogx(True)
        else:
            raise Exception("Request for TCanvas::SetLogx(True) rejected. The minimum x-value is '%s'." % (self.THDumbie.xMin))
        return


    def _SetLogY(self):
        self.Verbose()

        if self.THDumbie.logY==False:
            return
        if self.THDumbie.THisto.GetMinimum() > 0:
            self.TCanvas.SetLogy(True)
            if hasattr(self, 'TPadPlot'):
                self.TPadPlot.SetLogy(True)
        else:
            raise Exception("Request for TCanvas::SetLogy(True) rejected. The minimum y-value is '%s'." % (self.THDumbie.yMin))
        return


    def _SetLogZ(self):
        '''
        Determine whether to set log for z-axis.
        '''
        self.Verbose()

        if isinstance(self.THDumbie.THisto, ROOT.TH1):
            return
        if self.THDumbie.logZ==False:
            return
        if self.THDumbie.THisto.GetZaxis().GetXmin() > 0:
            self.TCanvas.SetLogz(True)
        else:
            raise Exception("Request for TCanvas::SetLogz(True) rejected. The minimum z-value is '%s'." % (self.THDumbie.zMin))
        return
    

    def _SetLogXRatio(self):
        self.Verbose()

        if not hasattr(self, 'TPadRatio'):
            return

        if not self.THRatio.logXRatio:
            return

        if self.THRatio.THisto.GetXaxis().GetXmin() > 0:
            self.TPadRatio.SetLogx(True)
        else:
            raise Exception("Request for TCanvas::SetLogx(True) rejected. The minimum x-value is '%s'." % (self.THRatio.xMin))
        return


    def _SetLogYRatio(self):
        self.Verbose()

        if not hasattr(self, 'TPadRatio'):
            return

        if not self.THRatio.logYRatio:
            return

        if self.THRatio.THisto.GetMinimum()>0:
            self.TPadRatio.SetLogy(True)
        else:
            raise Exception("Request for TCanvas::SetLogx(True) rejected. The minimum x-value is '%s'." % (self.THRatio.yMin))
        return


    def _CreateTPadPlot(self):
        '''
        Creates a plot pad to draw the histogram stack.
        '''
        self.Verbose()

        self.TPadPlot  = self.TCanvas.cd(1)
        self.TPadPlot.SetName("TPadPlot")
        (xlow, ylow, xup, yup) = [ROOT.Double(x) for x in [0.0]*4]
        self.TPadPlot.GetPadPar(xlow, ylow, xup, yup)
        self.TPadPlot.SetPad(xlow, self.padDivisionPoint, xup, yup)
        self.TPadPlot.Draw()
        return


    def _CreateTPadRatio(self):
        '''
        Creates a ratio pad to draw the histogram ratio stack.
        '''
        self.Verbose()
        
        canvasHeightCorr = 0.022

        self.TPadRatio = self.TCanvas.cd(2)
        self.TPadRatio.SetName("TPadRatio")
        (xlow, ylow, xup, yup) = [ROOT.Double(x) for x in [0.0]*4]
        self.TPadRatio.GetPadPar(xlow, ylow, xup, yup)
        self.TPadRatio.SetPad(xlow, ylow, xup, self.padDivisionPoint + ROOT.gStyle.GetPadBottomMargin() - ROOT.gStyle.GetPadTopMargin() + canvasHeightCorr)
        self.TPadRatio.SetFillStyle(4000)
        self.TPadRatio.SetTopMargin(0.0)
        self.TPadRatio.SetBottomMargin(self.TPadRatio.GetBottomMargin()+0.20) #was: 0.16
        self.TPadRatio.Draw()
        return


    def _CreateTPadCover(self, xMin=0.08, yMin=0.285, xMax=0.16, yMax=0.32):
        '''
        Creates a cover pad to cover the overlap of the y-axis divisions between the TPadPlot and the TPadRatio.
        '''
        self.Verbose()

        if not hasattr(self, 'TPadRatio'):
            raise Exception("Cannot create a cover-TPad. First you need to create a ratio-TPad!")
        
        self.TCanvas.cd()
        self.PadCover = ROOT.TPad("PadCover", "PadCover", xMin, yMin, xMax, yMax)
        self.PadCover.SetName("PadCover")
        self.PadCover.SetBorderMode(0)
        self.PadCover.SetFillStyle(1001)
        self.PadCover.SetFillColor(ROOT.kWhite) #ROOT.kRed
        self.PadCover.Draw()
        self.TPadRatio.Draw() # Re-draw TPadRatio to put back the covered y-axis numbers
        return

    
    def _CreateLegend(self):
        '''
        Create a TLegend, customise it and append it to the drawList
        '''
        self.Verbose()
        
        if hasattr(self, 'TLegend'):
            return

        histo = self.THDumbie
        self.TLegend = ROOT.TLegend(histo.xLegMin, histo.yLegMin, histo.xLegMax, histo.yLegMax, "", "brNDC")
        self._CustomiseLegend(self.TLegend)
        self.ExtendDrawLists(self.TLegend, addToRatio=False)
        return


    def _CustomiseLegend(self, legend):
        self.Verbose()
        legend.SetName("TLegend:" + self.TCanvas.GetName())
        legend.SetFillStyle(0)
        legend.SetLineColor(ROOT.kBlack)
        legend.SetLineWidth(1)
        legend.SetBorderSize(0)
        legend.SetShadowColor(ROOT.kWhite)
        legend.SetTextSize(0.03)
        legend.SetTextFont(62)
        return

    
    def IsDrawObject(self, drawObject):
        self.Verbose()
        if isinstance(drawObject, histos.DrawObject):
            return True
        else:
            return False


    def IsHisto(self, rootFile, hObject):
        self.Verbose()

        hPath = hObject.GetAttribute("fullPath")
        if not isinstance(rootFile, ROOT.TFile):
            return False

        h = rootFile.Get(hPath)
        if isinstance(h, ROOT.TH1) or isinstance(h, ROOT.TH2) or isinstance(h, ROOT.TH3):
            return True
        else:
            return False

        
    def _GetTLine(self, xMin, xMax, yMin, yMax, colour=ROOT.kBlack, width=3, style=ROOT.kDashed):
        self.Verbose()
        line = ROOT.TLine(xMin, yMin, xMax, yMax)
        self._CustomiseTLine(line, colour, width, style)
        return line


    def CreateCutLines(self):
        self.Verbose("Creating all TLine objects")

        if hasattr(self, "CutLinesCreated"):
            return
        
        self._CreateTLinesX()
        self._CreateTLinesY()
        self.ExtendDrawLists(self.TLineListX, addToRatio=True)
        self.ExtendDrawLists(self.TLineListY, addToRatio=True)
        self.CutLinesCreated = True
        return


    def _CreateTLinesX(self):
        self.Verbose()

        if not hasattr(self.THDumbie, "xCutLines"):
            return

        if not hasattr(self, "TLineListX"):
            self.TLineListX = []
            
        for value in self.THDumbie.xCutLines:
            if not hasattr(self, "TPadRatio"):
                line = self._GetTLine(value, value, self.THDumbie.THisto.GetMinimum(), self.THDumbie.THisto.GetMaximum())
            else:
                line = self._GetTLine(value, value, self.THRatio.THisto.GetMinimum(), self.THDumbie.THisto.GetMaximum())
            self._CustomiseTLine(line, ROOT.kBlack, 2, ROOT.kDashed)
            self.TLineListX.append(line)
            self.ExtendLegend(line, "x = %s" % (value), "L" )
        return
                
    
    def _CreateTLinesY(self):
        self.Verbose()

        if not hasattr(self.THDumbie, "yCutLines"):
            return

        if not hasattr(self, "TLineListY"):
            self.TLineListY = []
            
        for value in self.THDumbie.yCutLines:
            line = self._GetTLine(self.THDumbie.xMin, self.THDumbie.xMax, value, value)
            self._CustomiseTLine(line, ROOT.kBlack, 2, ROOT.kDashDotted)
            self.TLineListY.append(line)
            self.ExtendLegend(line, "y = %s" % (value), "L" )
        return


    def _GetTBox(self, xMin, xMax, yMin, yMax, fillColour, fillStyle):
        self.Verbose()

        cutBox = ROOT.TBox( xMin, yMin, xMax, yMax)
        cutBox.SetFillStyle(fillStyle)
        cutBox.SetFillColor(fillColour)
        cutBox.SetLineColor(fillColour)
        return cutBox


    def CreateCutBoxes(self):
        self.Verbose("Creating all TBox objects")

        if hasattr(self, "CutBoxesCreated"):
            return
        self._CreateTBoxesX()
        self._CreateTBoxesY()
        self.ExtendDrawLists(self.TBoxListX, addToRatio=True)
        self.ExtendDrawLists(self.TBoxListY, addToRatio=True)
        self.CutBoxesCreated = True
        return


    def _CreateTBoxesX(self, fillStyle=3004):
        self.Verbose()

        if not hasattr(self.THDumbie, "xCutBoxes"):
            return
        if not hasattr(self, "TBoxListX"):
            self.TBoxListX = []
        if not hasattr(self, "TLineListX"):
            self.TLineListX = []
        if not hasattr(self, "TLineListY"):
            self.TLineListY = []
            
        for v in self.THDumbie.xCutBoxes:
            xMin   = v[0]
            xMax   = v[1]
            yMin   = self.THDumbie.THisto.GetMinimum()
            yMax   = self.THDumbie.THisto.GetMaximum()
            colour = v[2]
            cutBox = self._GetTBox(xMin , xMax, yMin, yMax, colour, fillStyle)
            cline1 = self._GetTLine(xMin, xMin, yMin, yMax, colour, 1, ROOT.kSolid)
            cline2 = self._GetTLine(xMax, xMax, yMin, yMax, colour, 1, ROOT.kSolid)
            self.TBoxListX.append(cutBox)
            self.TLineListX.append(cline1)
            self.TLineListY.append(cline2)
            self.ExtendLegend(cutBox, "x = [%s, %s]" % (xMin, xMax), "F" )
        return


    def _CreateTBoxesY(self, fillStyle=3005):
        self.Verbose()

        if not hasattr(self.THDumbie, "yCutBoxes"):
            return
        if not hasattr(self, "TLineListX"):
            self.TLineListX = []
        if not hasattr(self, "TBoxListY"):
            self.TBoxListY = []
        if not hasattr(self, "TLineListY"):
            self.TLineListY = []

        for v in self.THDumbie.yCutBoxes:
            xMin    = self.THDumbie.xMin
            xMax    = self.THDumbie.xMax
            yMin    = v[0]
            yMax    = v[1]
            colour  = v[2]
            cutBox  = self._GetTBox(xMin , xMax, yMin, yMax, colour, fillStyle)
            cline1  = self._GetTLine(xMin, xMax, yMin, yMin, colour, 1, ROOT.kSolid)
            cline2  = self._GetTLine(xMin, xMax, yMax, yMax, colour, 1, ROOT.kSolid)
            self.TBoxListX.append(cutBox)
            self.TBoxListX.append(cutBox)
            self.TLineListX.append(cline1)
            self.TLineListY.append(cline2)
            self.ExtendLegend(cutBox, "y = [%s, %s]" % (xMin, xMax), "F" )
        return


    def _DrawItemsInDrawList(self):
        self.Verbose("Drawing items in draw list")

        self.CreateCutBoxes()
        self.CreateCutLines()

        if hasattr(self, "TPadPlot"):
            self.TPadPlot.cd()
            
        for o in self.drawList:
            if isinstance(o, histos.DrawObject):
                o.Draw("9same" + drawOptions)
            else:
                o.Draw("9same")

        if hasattr(self, "TPadRatio"):
            self._DrawItemsInDrawListRatio()
        self.UpdateCanvas()
        return


    def _DrawItemsInDrawListRatio(self):
        self.Verbose("Drawing items in draw list (ratio)")

        if not hasattr(self, "TPadRatio"):
            raise Exception("Cannot draw items in draw list (ratio). The TPadRatio has not been created")

        self.TPadRatio.cd()
        for o in self.drawListRatio:
            if isinstance(o, ROOT.TLegend):
                continue
            elif isinstance(o, histos.DrawObject):
                o.Draw("9same" + drawOptions)

            if isinstance(o, ROOT.TLine):
                if o.GetX1() == o.GetX2():
                    o.SetY1( self.THRatio.THisto.GetMinimum() )
                    o.SetY2( self.THRatio.THisto.GetMaximum() )
            if isinstance(o, ROOT.TBox):
                if o.GetY1() == self.THDumbie.THisto.GetMaximum():
                    o.SetY1( self.THRatio.THisto.GetMinimum() )
                if o.GetY2() == self.THDumbie.THisto.GetMaximum():
                    o.SetY2( self.THRatio.THisto.GetMaximum() )
            o.Draw("9same")
                
        return


    def UpdateCanvas(self):
        self.Verbose()

        if not hasattr(self, "TCanvas"):
            raise Exception("Cannot update TCanvas because it has not been created yet.")
            
        if hasattr(self, "TPadRatio"):
            self.TPadPlot.Update()
            self.TPadPlot.Modified()
            self.TPadPlot.RedrawAxis()
            #
            self.TPadRatio.Update()
            self.TPadRatio.Modified()
            self.TPadRatio.RedrawAxis()
        else:
            self.TCanvas.Modified()
            self.TCanvas.Update()
            self.TCanvas.RedrawAxis()
        #ROOT.gPad.RedrawAxis() #the histo fill area may hide the axis tick marks. Force a redraw of the axis over all the histograms.
        return
       

    def CreateDumbieHisto(self, newName):
        '''
        Create a dumbie histogram that will be the first to be drawn on canvas. 
        This should have zero entries but have exactly the same attribues  (binning, axes titles etc..) as the ones to be drawn.
        '''
        self.Verbose()

        # Determine global yMin and yMax
        yMin, yMax = self.GetHistosYMinYMax()

        # Copy first histo in datasets list. Reset its Integral, Contents, Errors and Statistics (not Minimum and Maximum)
        emptyHisto = copy.deepcopy(self.Datasets[0].histo)
        # emptyHisto.SetName(newName)
        emptyHisto.THisto.SetName(newName)
        emptyHisto.THisto.Reset("ICES")    
        emptyHisto.THisto.GetYaxis().SetRangeUser(yMin, yMax)
        emptyHisto.THisto.GetYaxis().SetTitleOffset(1.4)
        emptyHisto.THisto.SetLineColor(ROOT.kBlack)
        emptyHisto.THisto.SetLineWidth(0)

        # Increase right pad margin to accomodate z-axis scale and title
        if isinstance(emptyHisto.THisto, ROOT.TH2):
            ROOT.gStyle.SetPadRightMargin(0.15)
        return emptyHisto

    
    def ExtendDrawLists(self, drawObjects, addToRatio=True, addToPlot=True):
        '''
        Append a drawable object of any type (TCanvas, TLegend, TLine, TBox, etc..) to a list.
        This list will be used later on to draw all objects on a single canvas with 1 or 2 drawing pads.
        '''
        self.Verbose()

        if isinstance(drawObjects, list):
            drawList = drawObjects
        else:
            drawList = [drawObjects]

        if addToRatio:
            self.drawListRatio.extend(copy.deepcopy(drawList))

        if addToPlot:
            self.drawList.extend(drawList)
        return 

    
    def ExtendLegend(self, drawObject, label="label", opts="L"):
        '''
        Append a drawable object of any type (TCanvas, TLegend, TLine, TBox, etc..) to the TCanvas.
        At the same time increase the TLegend y-size to accomodate this new entry
        '''
        self.Verbose()

        if not hasattr(self, 'TLegend'):
            raise Exception("Cannot add drawObject '%s' to the TLegend, as the latter has not been created yet." % (drawObject) )

        deltaY = self.TLegend.GetY1() - 0.025
        if isinstance(drawObject, histos.DrawObject):
            histo  = drawObject.THisto
            label  = self.GetLegLabel(drawObject)
            self.TLegend.AddEntry(histo, label, opts)            
        elif isinstance(drawObject, (ROOT.TH1, ROOT.TH2, ROOT.TH3, ROOT.TLine, ROOT.TBox) ):
            self.TLegend.AddEntry(drawObject, label, opts)            
        else:
            raise Exception("Cannot add drawObject '%s' (type='%s') to the TLegend. Unsupported type" % (drawObject, type(drawObject) ) )

        self.TLegend.SetY1(deltaY)
        return

        
    def AddTF1(self, myFunction, xMin, xMax, addToRatio, kwargs={}):
        self.Verbose()

        f1 = ROOT.TF1("f1", myFunction, xMin, xMax)        

        # Customise Line Style
        if kwargs.get("fillColour"):
            f1.SetFillColor( kwargs.get("fillColour") )
        if kwargs.get("fillStyle"):
            f1.SetFillStyle( kwargs.get("fillStyle") )
        if kwargs.get("lineColour"):
            f1.SetLineColor( kwargs.get("lineColour") )
        if kwargs.get("lineStyle"):
            f1.SetLineStyle( kwargs.get("lineStyle") )
        if kwargs.get("lineWidth"):
            f1.SetLineWidth( kwargs.get("lineWidth") )

        self.ExtendDrawLists(f1, addToRatio=True)
        return

    
    def _CustomiseTHRatio(self):
        self.Verbose()

        # Customise the x-axis
        self.THRatio.THisto.GetXaxis().SetTitleOffset(3.2) #was: 2.8

        # Customise the y-axis
        self.THRatio.THisto.GetYaxis().SetTitle(self.THRatio.ratioLabel)    
        self.THRatio.yMax = self.THRatio.yMinRatio
        self.THRatio.yMin = self.THRatio.yMaxRatio        
        self.THRatio.THisto.GetYaxis().SetNdivisions(505)
        self.THRatio.THisto.GetYaxis().SetRangeUser(self.THRatio.yMinRatio, self.THRatio.yMaxRatio)
        self.THRatio.THisto.GetYaxis().SetTitleOffset(1.8)
        self.THDumbie.THisto.GetYaxis().SetTitleOffset(1.8)
        return

    
    def _CheckHistoBinning(self, histoObject):
        '''
        Ensure that the histoObject has exactly the same binning as the TH1Dubmie.
        '''
        self.Verbose()

        binWidthX         = self.THDumbie.binWidthX
        binZeroWidth      = self.THDumbie.THisto.GetXaxis().GetBinWidth(0)
        tmpBinWidthX      = histoObject.binWidthX
        tmpBinZeroWidth   = histoObject.THisto.GetXaxis().GetBinWidth(0)

        if (tmpBinWidthX != binWidthX or tmpBinZeroWidth!=binZeroWidth):
            raise Exception("At least one of the histogram in the plotting queue has a different x-axis binning! Please make sure all your histogram bins are identical.")
        return 

    
    def _CheckHistosBinning(self):
        '''
        Ensure that all histoObjects have exactly the same binning as the TH1Dubmie.
        '''
        self.Verbose()

        binWidthX    = self.THDumbie.binWidthX
        binZeroWidth = self.THDumbie.THisto.GetXaxis().GetBinWidth(0)    
        for dataset in self.Datasets:
            self._CheckHistoBinning(dataset.histo)
        return 
    
    
    def GetDatasetObjectHistoCopy(self, datasetObject):
        '''
        Takes as input a Dataset (or DatasetMerged) object. Return a deep-copy 
        of the associated histogram (histograms).
        '''
        self.Verbose()

        if isinstance(datasetObject, Dataset):
            histo = copy.deepcopy(datasetObject.histo.THisto)
            return histo
        elif isinstance(datasetObject, DatasetMerged):
            histo = None
            for d in datasetObject.GetDatasets():
                if histo == None:
                    histo = copy.deepcopy(d.histo.THisto)
                else:
                    histo.Add(d.histo.THisto)
            return histo


    def GetDatasetObjectDrawObject(self, datasetObject):
        '''
        Takes as input a Dataset (or DatasetMerged) object. Return the 
        drawObject of (one of) the datsets.
        '''
        self.Verbose()

        if isinstance(datasetObject, Dataset):
            drawObject = copy.deepcopy(datasetObject.histo)
            return drawObject
        elif isinstance(datasetObject, DatasetMerged):
            for d in datasetObject.GetDatasets():
                drawObject = copy.deepcopy(d.histo)
                return drawObject
        

    def _CreateDataHistoStack(self):
        '''
        Add all Data histograms to a THStack. For each histogram add a TLegend entry
        and automatically extend the size of the TLegend to accomodate the next entry.
        '''
        self.Verbose()

        histo      = None
        ignoreList = []

        # For loop: All DatasetMerged objects
        for dm in self.GetMergedDatasets():
            if dm.GetIsMC():
                continue
            else:
                histo   = self.GetDatasetObjectHistoCopy(dm)
                drawObj = self.GetDatasetObjectDrawObject(dm)
                self.THStackData.Add(histo)
                self.Verbose("Adding dataset \"%s\" to the MC THStack" % (dm.GetName() ))
                self.ExtendLegend(histo, dm.GetName(), "LP")
                for d in dm.GetDatasets():
                    ignoreList.append( d.GetName() )

        # For loop: All Dataset objects
        for d in self.GetDataDatasets():
            if d.GetName() in ignoreList:
                continue
            else:
                histo   = self.GetDatasetObjectHistoCopy(d)
                drawObj = self.GetDatasetObjectDrawObject(d)
                self.THStackData.Add(histo)
                self.Verbose("Adding dataset \"%s\" to the MC THStack" % (d.GetName() ))
                self.ExtendLegend(histo, self.GetLegLabel(drawObj), "LP")
        return


    def _CreateMcHistoStack(self):
        '''
        Add all MC histograms to a THStack. For each histogram add a TLegend entry
        and automatically extend the size of the TLegend to accomodate the next entry.
        '''
        self.Verbose()

        histo      = None
        ignoreList = []
        
        # For loop: All DatasetMerged objects
        for dm in self.GetMergedDatasets():
            if dm.GetIsData():
                continue
            else:
                histo   = self.GetDatasetObjectHistoCopy(dm)
                drawObj = self.GetDatasetObjectDrawObject(dm)
                self.THStackMC.Add(histo)
                self.Verbose("Adding dataset \"%s\" to the MC THStack" % (dm.GetName() ))
                self.ExtendLegend(histo, dm.GetName(), self.GetLegOptions())
                for d in dm.GetDatasets():
                    ignoreList.append( d.GetName() )

        # For loop: All Dataset objects
        for d in self.GetMcDatasets():
            if d.GetName() in ignoreList:
                continue
            else:
                histo   = self.GetDatasetObjectHistoCopy(d)
                drawObj = self.GetDatasetObjectDrawObject(d)
                self.THStackMC.Add(histo)
                self.Verbose("Adding dataset \"%s\" to the MC THStack" % (d.GetName() ))
                self.ExtendLegend(histo, self.GetLegLabel(drawObj), self.GetLegOptions())
        return


    
    def _CreateRatioHistoStack(self, ratioStackOpts, refDataset):
        self.Verbose()

        # The reference histogram is the numerator histogram
        (hNumerator, colour) = self._GetRatioReferenceHisto(refDataset)

        if hNumerator==None:
            raise Exception("Cannot find reference dataset \"%s\". Are you sure it exists? Available datasets are: \n\t %s" % (refDataset, "\n\t ".join(self.GetDatasetNames())))
        
        if "nostack" in ratioStackOpts:
            hRatioList = self._GetRatioHistoList(hNumerator, refDataset)
            for hRatio in hRatioList:
                self.THStackRatio.Add(hRatio)
        elif "stack" in ratioStackOpts:
            hRatio = self._GetRatioHisto(hNumerator, refDataset)
            self.THStackRatio.Add(hRatio)
        else: 
            raise Exception("Missing option \"stack\" or \"nostack\". Make sure of of them exists.")

        # Add a line at y=1
        line = self._GetTLine(self.THDumbie.xMin, self.THDumbie.xMax, 1.0, 1.0, colour, 2, ROOT.kSolid)
        self.ExtendDrawLists(line, addToRatio=True, addToPlot=False)            
        return


    def _GetRatioHistoList(self, hNumerator, refDataset):
        '''
        '''
        self.Verbose()

        hList    = []
        datasets = []
            
        if refDataset.lower() == "data":
            datasets = self.GetMcDatasets()
        else:
            datasets = self.GetDatasets()

        for dm in datasets:
            if dm.GetName() == refDataset:
                continue
            else:
                hDenominator = self.GetDatasetObjectHistoCopy(dm)
                hRatio       = self.GetDatasetObjectHistoCopy(dm)
                hRatio.Reset("ICES")            
                hRatio.Divide(hNumerator, hDenominator, 1.0, 1.0, "B")
                hList.append(hRatio)
        return hList


    def _GetRatioHisto(self, hNumerator, refDataset):
        '''
        '''
        self.Verbose()


        if refDataset.lower() == "data":
            datasets = self.GetMcDatasets()
        else:
            datasets = self.GetDatasets()

        hDenominator = copy.deepcopy(hNumerator)
        hRatio       = copy.deepcopy(hNumerator)
        hRatio.Reset()
        hDenominator.Reset()
        for dm in datasets:
            if dm.GetName() == refDataset:
                continue
            else:
                h = self.GetDatasetObjectHistoCopy(dm)
                hDenominator.Add(h)
        hRatio.Divide(hNumerator, hDenominator, 1.0, 1.0, "B")
        return hRatio
    

    def SetHistosFillStyle(self, style):
        self.Print("FIXME")
        sys.exit()
        for dataset in self.Datasets:
            dataset.histo.THisto.SetFillStyle(style)
        return


    def SetHistoLabelsOption(self, option):
        '''
        Set option(s) to draw axis with labels option:
        "a" sort by alphabetic order 
        ">" sort by decreasing values 
        "<" sort by increasing values 
        "h" draw labels horizonthal 
        "v" draw labels vertical 
        "u" draw labels up (end of label right adjusted) 
        "d" draw labels down (start of label left adjusted)

        Link: https://root.cern.ch/doc/master/classTAxis.html#a05dd3c5b4c3a1e32213544e35a33597c
        '''        
        self.Verbose()

        opts = ["a", ">", "<", "h", "v", "u", "d"]

        if option not in opts:
            raise Exception("Invalid label option '%s' selected. Please select one of the following: '%s'" % (option, opts) )

        if not hasattr(self, "TPadPlot")  and hasattr(self, "TCanvas"):
            self.THDumbie.THisto.GetXaxis().LabelsOption(option)
        elif hasattr(self, "TPadRatio"):
            self.THRatio.THisto.GetXaxis().LabelsOption(option)
        else:
            raise Exception("Cannot set histo label option '%s'. No THisto or THRatio histograms available!" % (option))
        return



    def SetHistoAxisOffsetX(self, newValue):
        '''
        '''        
        self.Verbose()

        if not hasattr(self, "TPadPlot")  and hasattr(self, "TCanvas"):
            self.THDumbie.THisto.GetXaxis().SetLabelOffset(newValue)
        elif hasattr(self, "TPadRatio"):
            self.THRatio.THisto.GetXaxis().SetLabelOffset(newValue)
        else:
            raise Exception("Cannot set histo x-axis offset to '%s'. No THisto or THRatio histograms available!" % (newValue))
        return


    def SetHistoLabelsSizeX(self, relSize):
        '''
        https://root.cern.ch/doc/master/classTAxis.html#a05dd3c5b4c3a1e32213544e35a33597c
        '''        
        self.Verbose()


        if not hasattr(self, "TPadPlot") and hasattr(self, "TCanvas"):
            self.THDumbie.THisto.GetXaxis().SetLabelSize(self.THDumbie.THisto.GetLabelSize()*relSize)
        elif hasattr(self, "TPadRatio"):
            self.THRatio.THisto.GetXaxis().SetLabelSize(self.THRatio.THisto.GetLabelSize()*relSize)
        else:
            raise Exception("Cannot set histo label option '%s'. No THisto or THRatio histograms available!" % (option))
        return
    

    def AddDrawObject(self, drawObjects):
        self.Verbose()
        
        if type(drawObjects) == list:
            self.Verbose("Copying '%s' drawObjects to all datasets: %s" % (len(drawObjects), "\"" + "\", \"".join(h.GetName() for h in drawObjects) + "\"") )
            sys.exit()
            for d in drawObjects:
                self._CopyToDatasets(d)
        else:
            self.Verbose("Copying '1' drawObjects to all datasets: %s" % ("\"" + drawObjects.GetAttribute("name") + "\"") )
            self._CopyToDatasets(drawObjects)
        return
    

    def _CopyToDatasets(self, drawObject):
        '''
        Takes as input parameter a drawObject and copies its attribues to all datasets.
        '''
        self.Verbose()
        
        if not hasattr(self, 'Datasets'):
            raise Exception("Cannot add copy drawObject as no datasets exist. Check that you have added some datasets")

        self.IsDrawObject(drawObject)

        for d in self.Datasets:
            if not self.IsHisto(d.rootFile, drawObject):
                raise Exception( "The object '%s'(type='%s') in '%s' is neither TH1, nor a TH2, nor a TH3. " % (drawObject, type(drawObject), d.rootFile.GetName()) )
            d.histo     = copy.deepcopy(drawObject)
            drawObject = d.histo
            drawObject.THisto  = self.GetHistoFromFile(d.rootFile, d.histo)
            drawObject.dataset = d
        return
    

    def _SaveDrawOpts(self, drawOpts):
        self.Verbose()

        myOpts = ["", "A", "P", "L", "HIST", "9", "nostack", "stack", "nostackb"]
        for o in drawOpts.split(","):
            if o not in myOpts:
                raise Exception( "Invalid drawing option '%s'. Please select one of the following: %s" % (o, myOpts) )

        self.drawOpts = drawOpts
        return


    def _SaveRatioDrawOpts(self, drawOpts):
        self.Verbose()

        myOpts = ["", "A", "P", "L", "HIST", "9", "nostack", "stack"]
        for o in drawOpts.split(","):
            if o not in myOpts:
                raise Exception( "Invalid THStackRatio drawing option '%s'. Please select one of the following: %s" % (o, myOpts) )

        self.drawOptsRatio = drawOpts
        return


    def GetDrawOpts(self):
        return self.drawOpts


    def GetDrawOptsRatio(self):
        return self.drawOptsRatio

    
    def Draw(self, drawOpts="", ratioDrawOpts=None, refDataset=None):
        self.Verbose()
            
        if ratioDrawOpts==None:
            self._SaveDrawOpts(drawOpts)
            self._Draw(drawOpts)
        else:
            if refDataset == None:
                raise Exception( "Cannot draw ratio pad without a reference datasets. Please provide the name of a dataset as argument")
            else:
                self._SaveDrawOpts(drawOpts)
                self._SaveRatioDrawOpts(ratioDrawOpts)
                self._DrawRatio(drawOpts, ratioDrawOpts, refDataset)
        return


    def _Draw(self, stackOpts="", ratioStackOpts=None, refDataset=None):
        self.Verbose()

        self._CreateCanvas()
        self._CheckHistosBinning()
        self._CreateDataHistoStack()
        self._CreateMcHistoStack()
        self._DrawHistos(stackOpts)
        self._DrawItemsInDrawList()
        self._RedrawSelectedObjects()
        return

    
    def _DrawRatio(self, stackOpts, ratioStackOpts, refDataset):
        self.Verbose()
    
        self._CreateCanvas(True)
        self._CheckHistosBinning()
        self._CreateDataHistoStack()
        self._CreateMcHistoStack()
        self._CreateRatioHistoStack(ratioStackOpts, refDataset)
        self._DrawHistos(stackOpts)
        self._DrawHistosRatio(ratioStackOpts)
        self._DrawItemsInDrawList()
        self._RedrawSelectedObjects()
        self._RedrawSelectedObjectsRatio(ratioStackOpts)
        return

    

    def _RedrawSelectedObjects(self):
        self.Verbose("Re-drawing Legend and Histo dumbies")

        if hasattr(self, "TPadPlot"):
            self.TPadPlot.cd()
            
        self.TLegend.Draw("same")
        self.THDumbie.THisto.Draw("same")
        self.UpdateCanvas()
        return


    def _RedrawSelectedObjectsRatio(self, stackOpts):
        self.Verbose("Re-drawing Legend and Histo dumbies")
        
        if not hasattr(self, "TPadRatio"):
            raise Exception("Cannot redraw objects on ratio pad.A dedicaded TPad was not created.")

        self.TPadRatio.cd()            
        self.THRatio.THisto.Draw("same")
        self.THStackRatio.Draw(stackOpts + ",9same")
        # self._DrawItemsInDrawListRatio()
        for c in self.TBoxListX:
            c.Draw("same")
        for c in self.TBoxListY:
            c.Draw("same")
        self.UpdateCanvas()
        return
    

    def IsBatchMode(self):
        '''
        Forces user to press 'q' before exiting ROOT from batch mode.

        NOTE: 
        When you are NOT in batch mode (self.batchMode = False), a canvas creation generates a window.        
        '''
        self.Verbose()
    
        if not self.batchMode:
            key = ""
            while key == "":
                key = raw_input("\r=== draw_template.py:\n\t Press 'q' to quit, any other key to continue: ")
                if key == "q":
                    sys.exit()
                else:
                    return
        return


    def GetTHStackMC(self):
        self.Verbose()
        return self.THStackMC


    def GetTHStackData(self):
        self.Verbose()
        return self.THStackData

    
    def GetTHStackRatio(self):
        self.Verbose()
        return self.THStackRatio


    def GetTHDumbie(self):
        self.Verbose()
        return self.THDumbie

    
    def _CustomiseTLine(self, line, colour=ROOT.kBlack, width=3, style=ROOT.kSolid):
        self.Verbose()
        line.SetLineColor(colour)
        line.SetLineWidth(width)
        line.SetLineStyle(style)    
        return



    def GetBinNumberFromBinLabel(self, histo, binLabel):
        '''
        Return bin number for bin in histogram "histo" with label "binLabel"
        '''    
        self.Verbose()

        if not isinstance(histo, ROOT.TH1):
            self.Print("ERROR! The histo parameter provided (%s) is not an instance ROOT.TH1. The bin number of bin '%s' cannot be found. EXIT" % (histo, binLabel))
            sys.exit()

        binNumber = None
        nBinsX    = histo.GetNbinsX()+1
        for i in range(nBinsX):
            label = histo.GetXaxis().GetBinLabel(i)
            if label == binLabel:
                binNumber =  i
                break
        if binNumber == None:
            raise Exception("Could not find bin labelled '%s' in histogram with name '%s'" % (binLabel, histo.GetName()) )
        return binNumber
