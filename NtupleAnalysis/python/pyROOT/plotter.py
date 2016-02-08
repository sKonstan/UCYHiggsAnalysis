'''
Normal assignment operations (a = b) will simply point the new variable towards the existing object.
A deep copy ( copy.deepcopy() ) constructs a new compound object and then, recursively, inserts copies into it of the objects found in the original.
A shallow copy ( copy.copy() ) constructs a new compound object and then (to the extent possible) inserts references into it to the objects found in the original.
'''

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
import time
import numpy
from array import array
import re
import collections

import ROOT
from ROOT import std

import UCYHiggsAnalysis.NtupleAnalysis.pyROOT.text as text
import UCYHiggsAnalysis.NtupleAnalysis.pyROOT.aux as aux
import UCYHiggsAnalysis.NtupleAnalysis.pyROOT.styles as styles
import UCYHiggsAnalysis.NtupleAnalysis.pyROOT.histos as histos
import UCYHiggsAnalysis.NtupleAnalysis.pyROOT.tdrstyle as tdrstyle


#================================================================================================
# Define class
#================================================================================================
class Plotter(object): 
    def __init__(self, verbose=False, batchMode=True):
        self.verbose           = verbose
        self.BatchMode         = batchMode
        self.StyleObject       = styles.StyleClass(verbose)
        self.TextObject        = text.TextClass(verbose)
        self.AuxObject         = aux.AuxClass(verbose)
        self.CanvasFactor      = 1.25
        #self.DatasetToHistoMap = collections.OrderedDict()
        self.Datasets          = []
        self.DivisionPoint     = 1-1/self.CanvasFactor
        self.DrawObjectList    = []
        self.DrawObjectListR   = []
        self.HistoObjectList   = []
        self.TCanvas           = None
        self.TLegend           = None
        self.PadCover          = None
        self.PadPlot           = None
        self.PadRatio          = None        
        self.TBoxList          = []
        self.xTLineList        = []
        self.yTLineList        = []
        self.THRatio           = None
        self.THDumbie          = None
        self.THStack           = ROOT.THStack("THStack" + "@" + str(time.time()), "Stack for PadPlot Histograms")
        self.THStackHistoList  = [] #needed because looping over self.THSTack.GetHists() crashes!
        self.THStackRatio      = ROOT.THStack("THStackRatio" + "@" + str(time.time()), "Stack for PadRatio Histograms")
        self.bInvPadRatio      = False
        self.bPadRatio         = False
        self.RatioErrorType    = None
        self.bStackInclusive   = False
        self.TMultigraph       = ROOT.TMultiGraph("TMultigraph"  + "@" + str(time.time()), "ROOT.TMultiGraph holding various ROOT.TGraphs")
        self.startTime         = time.time()        
        self.MsgCounter        = 0
        self.CutOption         = None
        self.IsTH1             = False
        self.IsTH2             = False
        self.CutLineColour     = ROOT.kBlack
        self.SaveContourPoints = False
        self.MaxDecimals       = None
        self.DatasetInLegend   = False
        self.PileUp            = None
        return

    
    def Verbose(self, message=""):
        '''
        Custome made verbose system. Will print all messages in the messageList
        only if the verbosity boolean is set to true.
        '''
        if not self.verbose:
            return
        
        print "%s:" % (self.__class__.__name__ + "." + sys._getframe(1).f_code.co_name + "()")
        print "\t", message
        return


    def Print(self, message=""):
        '''
        Custome made print system. Will print the message even if the verbosity boolean is set to false.
        '''
        print "*** %s:" % (self.__class__.__name__ + "." + sys._getframe(1).f_code.co_name + "()")
        print "\t", message
        return

    
    def PrintList(self, messageList=[""]):
        '''
        Custome made print system. Will print all messages in the messageList even if the verbosity boolean is set to false.
        '''
        for counter, message in enumerate(messageList):
            if counter == 0:
                self.Print(message)
            else:
                print "\t", message
        return


    def SetVerbose(self, verbose):
        '''
        Manually enable/disable verbosity.
        '''
        self.verbose = verbose
        return


    def SetupROOT(self):

        '''
        Setup ROOT before doing anything else. Reset ROOT settings, disable statistics box,
        apply Techical Design Report (TDR) style.
        '''
        self.Verbose()

        ROOT.gROOT.Reset()
        tdrstyle.TDRStyle()
        ROOT.gStyle.SetOptStat(0)
        ROOT.TGaxis.SetMaxDigits(4)
        ROOT.gROOT.SetBatch(self.BatchMode)
        self.SetupROOTErrorIgnoreLevel(2000)
        ROOT.gStyle.SetNumberContours(999)
        return


    def SetupStatsBox(self, xPos=0.94, yPos=0.84, width=0.20, height=0.12, options = 0):
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
    
        Example: gStyle->SetOptStat(11);
        print only name of histogram and number of entries.
        '''
        self.Verbose()
        #self.PadCover

        # Beautifications/Styling
        ROOT.gStyle.SetStatBorderSize(0)
        ROOT.gStyle.SetStatColor(ROOT.kWhite)
        ROOT.gStyle.SetStatStyle(3001)
        ROOT.gStyle.SetStatTextColor(ROOT.kBlack)
        #ROOT.gStyle.SetStatFont(62)
        ROOT.gStyle.SetStatFontSize(15)
        # ROOT.gStyle.SetStatFormat(const char* format = "6.4g")
        
        # Dimensions
        ROOT.gStyle.SetStatY(yPos)
        ROOT.gStyle.SetStatX(xPos)
        ROOT.gStyle.SetStatW(width)
        ROOT.gStyle.SetStatH(height)
        ROOT.gStyle.SetOptStat(options)

        # Workaround for not being able to not remove it
        if yPos == -1 and xPos == -1 and width==-1 and height==-1:
            ROOT.gStyle.SetStatTextColor(ROOT.kWhite)
            ROOT.gStyle.SetStatFontSize(0)
            ROOT.gStyle.SetStatStyle(0)
            
        return


    def SetupROOTErrorIgnoreLevel(self, level):
        '''
        Available options (const Int_t):
        kUnset    =  -1
        kPrint    =   0
        kInfo     =   1000
        kWarning  =   2000
        kError    =   3000
        kBreak    =   4000
        kSysError =   5000
        kFatal    =   6000
        '''
        self.Verbose()

        ROOT.gErrorIgnoreLevel = level
        return
    

    def AddDataset(self, dataset):
        '''
        Add a new dataset and associate it to a root file.
        '''
        self.Verbose("Adding dataset %s from file %s." % (dataset.name, dataset.rootFile.GetName()))
        self.Print("FIXME")
        
        ## Get the Pile Up
        #self.GetPileUp(dataset)
                
        ## Map dataset to ROOT file, append dataset (name) to datasetlist, append ROOT file (name) to TFile list
        #self.DatasetToRootFileMap[dataset]  = rootFile
        
        ## Map dataset to Latex name
        self.Datasets.append(dataset)
        return


    def AddDatasets(self, datasetObjects):
        '''
        Add all datasets in the datasetObjects list to the plotter
        '''
        self.Verbose()
        
        for d in datasetObjects:
            self.Verbose("Adding dataset %s from file %s." % (d.name, d.rootFile.GetName()))
            self.AddDataset(d)
        return

    
    def GetPileUp(self, dataset):
        '''
        '''
        self.Vertbose()
        if self.PileUp == None:
            self.PileUp = 140
            self.Print("FIXME")
            return
        return
        

    def _CreateCanvas(self):
        '''
        Create a name for a TCanvas and then create it. 
        This name will later on be used to save the canvas under a user specific format ("png", "pdf", "eps", etc..)
        '''                    
        self.Verbose()

        # Normal assignment operations (a = b) will simply point the new variable towards the existing object.
        histo = self.THDumbie 

        # Create a name for the TCanvas
        if histo.saveName == None:
            canvasName = histo.name
        else:
            canvasName = histo.saveName

        # Create TCanvas and activate it
        self.Verbose("Creating canvas with name '%s'" % ( canvasName))

        # Add the time in the canvas name to avoid memory duplicates when handling the same histos. Truncate "@time" when saving canvas
        canvasName =  canvasName + "@" + str(time.time())
        self.TCanvas = ROOT.TCanvas( canvasName, canvasName, 1)
        time.sleep(0.2) #to avoid getting the same time (canvas/histo overwrite)

        self._SetLogAxesCanvas()
        self.TCanvas.cd()
        return


    def _Create2PadCanvas(self):
        '''
        Create a 2-pad TCanvas to accomodate a ratio plot and customise it.
        '''                    
        self.Verbose()

        # Normal assignment operations (a = b) will simply point the new variable towards the existing object.
        histo = self.THDumbie 

        # Create the THRatio histogram (PadRatio equivalent of PadPlot's THDumbie)
        self.THRatio = copy.deepcopy(histo)
        self.THRatio.TH1orTH2.SetName("THRatio")

        # Create TCanvas name that included the dataset name
        if histo.saveName == None:
            canvasName = histo.name
        else:
            canvasName = histo.saveName

        # Create TCanvas and divide it into two pads: one for plot pad, one for ratio pad
        self.Verbose("Creating canvas with name '%s'" % ( canvasName))
        canvasName =  canvasName + "@" + str(time.time())
        self.TCanvas = ROOT.TCanvas( canvasName, canvasName, ROOT.gStyle.GetCanvasDefW(), int(ROOT.gStyle.GetCanvasDefH()*self.CanvasFactor))
        self.TCanvas.Divide(1,2)

        # Remove x-axis title and labels from the THDumbie to avoid overlap with those THRatio
        self._RemoveXaxisBinLabels(histo.TH1orTH2)
        self._RemoveXaxisTitle(histo.TH1orTH2)

        # Create plot, ratio and cover pads
        self._CreatePads()
        
        # Take care of log-axis settings
        self._SetLogAxes2PadCanvas()

        # Update canvas and change back to the PadPlot
        self.TCanvas.Update()
        self.PadPlot.cd()

        return


    def _CreatePads(self):
        '''
        Create the plot, ratio and cover pads.
        '''
        self.Verbose()

        self._CreatePadPlot()
        self._CreatePadRatio()
        self._CreatePadCover()
        return

    
    def _CreatePadCover(self, xMin=0.09, yMin=0.285, xMax=0.16, yMax=0.32):
        '''
        Creates a cover pad to cover the overlap of the y-axis divisions between the PadPlot and the PadRatio.
        '''
        self.Verbose()
        
        self.TCanvas.cd()
        self.PadCover = ROOT.TPad("PadCover", "PadCover", xMin, yMin, xMax, yMax)
        self.PadCover.SetName("PadCover")
        self.PadCover.SetBorderMode(0)
        self.PadCover.SetFillStyle(1001)
        self.PadCover.SetFillColor(ROOT.kWhite) #ROOT.kRed
        self.PadCover.Draw()
        self.PadRatio.Draw() # Re-draw PadRatio to put back the covered y-axis numbers
        self.TCanvas.Update()
        return


    def _CreatePadPlot(self):
        '''
        Creates a plot pad to draw the histogram stack.
        '''
        self.Verbose()

        self.PadPlot  = self.TCanvas.cd(1)
        self.PadPlot.SetName("PadPlot")
        (xlow, ylow, xup, yup) = [ROOT.Double(x) for x in [0.0]*4]
        self.PadPlot.GetPadPar(xlow, ylow, xup, yup)
        self.PadPlot.SetPad(xlow, self.DivisionPoint, xup, yup)
        self.PadPlot.Draw()
        self.TCanvas.Update()
        return


    def _CreatePadRatio(self):
        '''
        Creates a ratio pad to draw the histogram ratio stack.
        '''
        self.Verbose()
        
        CanvasHeightCorr = 0.022

        self.PadRatio = self.TCanvas.cd(2)
        self.PadRatio.SetName("PadRatio")
        (xlow, ylow, xup, yup) = [ROOT.Double(x) for x in [0.0]*4]
        self.PadRatio.GetPadPar(xlow, ylow, xup, yup)
        self.PadRatio.SetPad(xlow, ylow, xup, self.DivisionPoint + ROOT.gStyle.GetPadBottomMargin() - ROOT.gStyle.GetPadTopMargin() + CanvasHeightCorr)
        self.PadRatio.SetFillStyle(4000)
        self.PadRatio.SetTopMargin(0.0)
        self.PadRatio.SetBottomMargin(self.PadRatio.GetBottomMargin()+0.16)
        self.PadRatio.Draw()
        self.TCanvas.Update()
        return


    def _RemoveXaxisBinLabels(self, histo):
        '''
        Removes all the x-axis labels from the histogram pass as argument.
        '''
        self.Verbose()

        bIsTH1 = isinstance(histo, ROOT.TH1)
        if bIsTH1 == False:
            self.Print("The histogram '%s' is not a ROOT.TH1 instance. Doing nothing" % histo.name)
            return
        histo.GetXaxis().SetLabelSize(0)
        return


    def _RemoveXaxisTitle(self, histo):
        '''
        Removes the x-axis title from the histogram passed as argument.
        '''
        self.Verbose()

        bIsTH1 = isinstance(histo, ROOT.TH1)
        if bIsTH1 == False:
            self.Print("The histogram '%s' is not a ROOT.TH1 instance. Doing nothing" % histo.name)
            return
        histo.GetXaxis().SetTitleSize(0)
        return


    def _SetLogAxesCanvas(self):
        '''
        Apply axes customisations to a TCanvas.
        '''
        self.Verbose()

        # Determine whether to set log for y- and x- axis.
        self._SetLogY(self.THDumbie, self.TCanvas)
        self._SetLogX(self.THDumbie, self.TCanvas)
        self._SetLogZ(self.THDumbie, self.TCanvas)
        return


    def _SetLogX(self, histo, PadOrCancas):
        '''
        Determine whether to set log for x-axis.
        '''
        self.Verbose()

        if histo.logX==False:
            return

        # Set log-scale for x-axis 
        if histo.xMin == None:
            histo.xMin = histo.TH1orTH2.GetXaxis().GetXmin()

        if histo.xMin > 0:
            PadOrCancas.SetLogx(True)
        else:
            raise Exception("Request for TCanvas::SetLogx(True) rejected. The '%s' minimum x-value is '%s'." % (histo.name, histo.xMin))
        return


    def _SetLogY(self, histo, PadOrCancas):
        '''
        Determine whether to set log for y-axis.
        '''
        self.Verbose()

        if histo.logY==False:
            return

        if histo.yMin == None:
            histo.yMin = histo.TH1orTH2.GetMinimum()

        if histo.yMin > 0:
            PadOrCancas.SetLogy(True)
        else:
            raise Exception("Request for TCanvas::SetLogy(True) rejected. The '%s' minimum y-value is '%s'." % (histo.name, histo.yMin))
        return


    def _SetLogZ(self, histo, PadOrCancas):
        '''
        Determine whether to set log for z-axis.
        '''
        self.Verbose()

        if histo.logZ==False or isinstance(histo.TH1orTH2, ROOT.TH2) == False:
            return

        # Set log-scale for z-axis 
        if histo.zMin == None:
            histo.zMin = histo.TH1orTH2.GetZaxis().GetXmin()

        if histo.zMin > 0:
            PadOrCancas.SetLogz(True)
        else:
            raise Exception("Request for TCanvas::SetLogz(True) rejected. The '%s' minimum z-value is '%s'." % (histo.name, histo.zMin))
        return


    def _SetLogXYRatio(self, histo, PadOrCancas):
        '''
        Determine whether to set log for x-axis.
        '''
        self.Verbose()

        # Set log-scale for y-axis 
        if histo.logYRatio==True:
            if histo.yMin == None:
                histo.yMin = histo.TH1orTH2.GetMinimum()
            
            if histo.yMin > 0:
                PadOrCancas.SetLogy(True)
            else:
                raise Exception("Request for TCanvas::SetLogy(True) rejected. The '%s' minimum y-value is '%s'." % (histo.name, histo.yMin))

        # Set log-scale for x-axis 
        if histo.logXRatio==True:
            if histo.xMin == None:
                histo.xMin = histo.TH1orTH2.GetXaxis().GetXmin()

            if histo.xMin > 0:
                PadOrCancas.SetLogx(True)
            else:
                raise Exception("Request for TCanvas::SetLogx(True) rejected. The '%s' minimum x-value is '%s'." % (histo.name, histo.xMin))
        return


    def _SetLogAxes2PadCanvas(self):
        '''
        Apply customisations to a 2-pad TCanvas.
        '''
        self.Verbose()

        # Determine whether to set log for y- and x- axis.
        self._SetLogY(self.THDumbie, self.PadPlot)
        self._SetLogX(self.THDumbie, self.PadPlot)
        self._SetLogZ(self.THDumbie, self.PadPlot)
        self._SetLogXYRatio(self.THRatio, self.PadRatio)
        return


    def _CreateLegend(self):
        '''
        Create a TLegend, customise it and return it.
        '''
        self.Verbose()
        
        if isinstance(self.TLegend, ROOT.TLegend) == True:
            return
        else:
            histo = self.THDumbie
            self.TLegend = ROOT.TLegend(histo.xLegMin, histo.yLegMin, histo.xLegMax, histo.yLegMax, self._GetLegendHeader(), "brNDC")
            self._CustomiseLegend()
            self.DrawObjectList.append( self.TLegend )
        return


    def _CustomiseLegend(self):
        '''
        Customise a TLegend.
        '''
        self.Verbose()
        
        self.TLegend.SetName("legend_" + str(time.time()) )
        self.TLegend.SetFillStyle(0)
        self.TLegend.SetLineColor(ROOT.kBlack)
        self.TLegend.SetLineWidth(1)
        self.TLegend.SetBorderSize(0)
        self.TLegend.SetShadowColor(ROOT.kWhite)
        self.TLegend.SetTextSize(0.03)
        self.TLegend.SetTextFont(62)
        return

    

    def AddHisto(self, histoObject):
        '''
        '''
        self.Verbose()
        
        if type(histoObject) == list:
            for h in histoObject:
                self._AddHistoToQueue(h)
        elif isinstance(histoObject, histos.TH1orTH2):
            self._AddHistoToQueue(histoObject)
        else:
            self.Print("ERROR!", "Expected object of type '%s' but got '%s' instead" % ( histos.TH1orTH2, type(histoObject) ), "EXIT")
            sys.exit()
        return
    

    def _AddHistogramsToStack2D(self, ProfileAxis, firstBin, LastBin):
        '''
        Add all histograms (except Dumbie) to a THStack. For each histogram add a TLegend entry
        and automatically extend the size of the TLegend to accomodate the next entry.
        '''
        self.Verbose()

        entryLabel = ""
        if  ProfileAxis =="x" or  ProfileAxis =="y":
            bAddLegendEntries = True
        else:
            bAddLegendEntries = False
        self.TCanvas.SetName( self.TCanvas.GetName() + "_Profile%s" % (ProfileAxis.upper()) )

        # For-loop: Histos
        #for h in self.DatasetToHistoMap.values():
        for dataset in self.Datasets:
            h = dataset.histo
            
            self.Verbose( ["Creating Profile%s for histogram '%s'  and adding to THStack." % ( ProfileAxis.upper(), h.name)] )
            if ProfileAxis == "x":
                hProfileX_Name = h.name +"_ProfileX"
                hProfileX      = h.TH1orTH2.ProfileX(hProfileX_Name, firstBin, LastBin)
                self.THStack.Add( hProfileX )
            else:
                self.Print("WARNING! Although this works, some validation would have to be carried out with a simple a well undestood 2D histo")
                hProfileY_Name = h.name +"_ProfileY"
                hProfileY      = h.TH1orTH2.ProfileY(hProfileY_Name, firstBin, LastBin)
                self.THStack.Add( hProfileY )
                
            # Add legend entries for THStack?
            if bAddLegendEntries == True:
                self.TLegend.AddEntry( h.TH1orTH2, self._GetLegEntryLabel(h), h.legOptions)
                self.TLegend.SetY1( self.TLegend.GetY1() - 0.02)
            else:
                pass
        return


    def _AddHistoToQueue(self, histoObject):
        '''
        '''
        self.Verbose()
        
        # Sanity check. At least one dataset is present 
        if len(self.Datasets)<1:
            self.Print("ERROR!", "No datasets found! Exit")
            sys.exit()

        # Ensure that the pass argument is a valid histo object
        self.IsValidHistoObject(histoObject)

        # Loop over all datasets
        for dataset in self.Datasets:

            # Get the ROOT file for given dataset
            f           = dataset.rootFile

            # Ensure that histogram exists in the file
            self.CheckThatHistoExists(f, histoObject)

            ### Map histo to dataset  
            #mapKey = dataset.name + ":" + histoObject.name
            #self.Verbose(["Mapping '%s' to key '%s'." % ( histoObject.name, mapKey)])
            #self.DatasetToHistoMap[mapKey] = copy.deepcopy(histoObject)
            dataset.histo = copy.deepcopy(histoObject)
            
            # Assign user-defined attributes to histo object
            histoObject = dataset.histo
            self._AssignHistoObjectAttributes( f, dataset, histoObject)

            # Print extensive histogram information
            self.PrintHistoInfo(histoObject, False)

            # Append to histoObject list
            self.HistoObjectList.append(histoObject)

        return

    
    def _AssignHistoObjectAttributes(self, rootFile, dataset, histoObject):
        '''
        '''
        self.Verbose()
        
        # Declare shorter name references
        h = histoObject
        f = rootFile

        # Assign attributes
        h.TH1orTH2      = self.GetHistoFromFile(f, h)
        h.TFileName     = f.GetName()
        h.dataset       = dataset
        h.rangeIntegral = h.TH1orTH2.Integral()

        # Determine the histogram integral
        if self.IsTH2:
            #self.TDRStyleObject.setWide(True)
            self._CheckThatNoTH2WithMoreThanOneDatasets(h)
            h.integral  = h.TH1orTH2.Integral(0, h.TH1orTH2.GetNbinsX()+1, 0, h.TH1orTH2.GetNbinsY()+1)
        else:
            h.integral  = h.TH1orTH2.Integral(0, h.TH1orTH2.GetNbinsX()+1)
            
        # Assign global values
        self.bPadRatio      = h.ratio
        self.bInvPadRatio   = h.invRatio
        self.RatioErrorType = h.ratioErrorType
            
        return
        


    def GetHistoFromFile(self, f, histo):
        '''
        '''
        self.Verbose()
        
        histoPath = ""
        if histo.path == "" or histo.path==None:
            histoPath = histo.name
        else:
            histoPath = histo.path + "/" + histo.name

        return f.Get(histoPath)


    def PrintHistoInfo(self, histo, verbose=False):
        '''
        '''
        self.Verbose()

        msg  = " {:<20} {:<20}".format("File"               , ": " + histo.TFileName)
        msg += "\n\t {:<20} {:<20}".format("Dataset"        , ": " + histo.dataset.name)
        msg += "\n\t {:<20} {:<20}".format("HistoPath"      , ": " + histo.path)
        msg += "\n\t {:<20} {:<20}".format("HistoName"      , ": " + histo.name)
        msg += "\n\t {:<20} {:<20}".format("Integral()"     , ": " + str(histo.rangeIntegral))
        msg += "\n\t {:<20} {:<20}".format("Integral(0, -1)", ": " + str(histo.integral))
        msg += "\n\t {:<20} {:<20}".format("normaliseTo"    , ": " + histo.normaliseTo)

        if histo.TH1orTH2.Integral() == 0:
            self.Print(msg)
            
        self.Verbose(msg)
        return


    def ConvertToOneMinusCumulativeHistos(self):
        '''
        This method converts all histograms into a (1-cumulative integral) histograms.
        '''
        self.Verbose()
        
        # For-loop: All datasets
        #for dataset in self.DatasetToHistoMap.keys():
        #h = self.DatasetToHistoMap[dataset]
        #    self._ConvertToOneMinusCumulativeHisto(h)
        for dataset in self.Datasets:
            self._ConvertToOneMinusCumulativeHisto(dataset.histo)
        return

    
    def DrawEfficiency(self, cutDirection=">", errType="binomial"):
        '''
        '''
        self.Verbose()
        
        self._CustomiseHistograms()

        # Change some histoObject attributes
        histo = self.HistoObjectList[0]
        saveName = histo.saveName
        kwargs   = histo.kwargs
        binWidthX = histo.binWidthX
        if histo.binWidthX == None:
            binWidthX = histo.TH1orTH2.GetBinWidth(0)
        
        kwargs["yUnits"]      = ""
        kwargs["logX"]        = False
        kwargs["logY"]        = False
        kwargs["yMin"]        = 0.0
        kwargs["yMax"]        = 1.15
        kwargs["normaliseTo"] = ""
        yTitleOld             = kwargs["yLabel"].rsplit("/", 1)[0]
        kwargs["yLabel"]      = kwargs["yLabel"].replace(yTitleOld, "Efficiency (" + cutDirection +  ") ")
        kwargs["yLabel"]      = kwargs["yLabel"]  % (binWidthX)  + " " + histo.xUnits
        kwargs["drawOptions"] = "AP" #"ACE3"
        kwargs["legOptions"]  = "LP" #"FL"

        # Change histo saveName according to cut-direction
        if cutDirection == ">":
            saveName = saveName + "_GreaterThan"
        elif cutDirection == "<":
            saveName= saveName + "_LessThan"
        else:
            raise Exception("Invalid cut-direction '%s' selected for efficiency plot. Please select either '<' or '>'." % (cutDirection) )

        self._ConvertToEfficiencyHistos(cutDirection, errType, **kwargs)
        self.DrawMultigraph(saveName, **kwargs)
        return


    def _ConvertToEfficiencyHistos(self, cutDirection, errType="binomial", **kwargs):
        '''
        '''
        self.Verbose()
        
#        for dataset in self.DatasetToHistoMap:
#            h = self.DatasetToHistoMap[dataset]
#            self._ConvertToEfficiencyHisto(h, cutDirection, errType, **kwargs)
        for dataset in self.Datasets:
            h = dataset.histo
            self._ConvertToEfficiencyHisto(h, cutDirection, errType, **kwargs)
        return


    def _ConvertToEfficiencyHisto(self, histo, cutDirection, errType="binomial", **kwargs):
        '''
        Replaces bin content with the efficiency of the given bin. Cut direction can be chosen.
        '''
        self.Verbose()
        
        # Declare lists
        xVals   = []
        xLow    = []
        xUp     = []
        effVals = []
        effLow  = []
        effUp   = []

        # For-loop: Histo Bins
        nBinsX  = histo.TH1orTH2.GetNbinsX()+1
        for b in range(0, nBinsX+1):

            binWidth   = histo.TH1orTH2.GetBinWidth(b)
            binCenter  = histo.TH1orTH2.GetBinCenter(b)
            binLowEdge = histo.TH1orTH2.GetBinLowEdge(b)
            binUpEdge  = binCenter + binWidth/2

            nPass      = histo.TH1orTH2.Integral(b+1, nBinsX) #events that pass the up-edge of the bin
            nTotal     = histo.TH1orTH2.Integral( 0, nBinsX )
            eff        = -1.0

            # Calculate the efficiency and its error
            eff, err = self.AuxObject.Efficiency(nPass, nTotal, errType)
            if (cutDirection == ">"):
                pass
            elif (cutDirection == "<"):
                eff = 1-eff
            else:
                self.Print("ERROR! Illegal logic operator ('%s') for cut-direction. EXIT" % (cutDirection))
                sys.exit()

            self.Verbose("bin = %s, x %s %s,  eff = %s +/- %s" % (b, cutDirection, binUpEdge, eff, err))
            
            # Save into lists
            xVals.append(binUpEdge)
            xUp.append(0.0)
            xLow.append(0.0)

            effVals.append(eff)
            effUp.append(err)
            effLow.append(err)


        # Use values to create a TGraphErrors
        histo.TH1orTH2.SetMaximum(1.0)
        self.AddTGraphErrors(histo, xVals, xUp, xLow, effVals, effUp, effLow, None, None, None, False, **kwargs)
        return


    def _ConvertToOneMinusCumulativeHisto(self, histo):
        '''
        This method convert a given histogram to a (1-cumulative integral) histogram. 
        '''
        self.Verbose()

        # Sanity check: Ensure that no bin-resining has been requested
        if (histo.binWidthX != None):
            self.Print("ERROR! The requested x-axis bin width ('%s') is invalid. Please set both axes bin-widths to 'None'. EXIT" % histo.binWidthX)
            sys.exit()
        elif (histo.binWidthY != None):
            self.Print("ERROR! The requested y-axis bin width ('%s') is invalid. Please set both axes bin-widths to 'None'. EXIT" % histo.binWidthY)
            sys.exit()
        else:
            pass
        
        # Loop over all histogram bins
        h = histo.TH1orTH2
        self.Print( ["Converting histo '%s' into a (1-cumulative integral) histogram" % ( h.GetName() )] )

        if isinstance(h, ROOT.TH1F) == True:
            nBins = h.GetNbinsX()+1
            for b in range(0, nBins+1):
                value = h.Integral(b, nBins) 
                error = math.sqrt(value)
                h.SetBinContent( b, value )
                h.SetBinError  ( b, error )
            return
        elif isinstance(h, ROOT.TH2D) == True:
            nBinsX = h.GetNbinsX()+1
            nBinsY = h.GetNbinsY()+1
            for bX in range(0, nBinsX+1):
                for bY in range(0, nBinsY+1):
                    # Draw only y<= x values
                    if bY >= bX and self.SaveContourPoints == False: 
                        break
                    else: #if you want to calculate thresholds proceed as normal
                        pass
                    value = h.Integral(bX, nBinsX, bY, nBinsY)
                    error = math.sqrt(value)
                    h.SetBinContent( bX, bY, value)
                    h.SetBinError  ( bX, bY, error)
            return
        else:
            raise Exception("Cannot only convert a TH1D or a TH2D into a rate histogram, but instead got an object of type '%s'." % (type(h) ) )
        return


    def _CheckThatNoTH2WithMoreThanOneDatasets(self, histoObject):
        ''''
        Ensure that no TH2 is drawn where more than 1 dataset is created. Very difficult to distinguish so we need to take care.
        '''
        self.Verbose()
        
        hType = type(histoObject.TH1orTH2)
        
        if len(self.Datasets)>1 and "TH2" in str(hType):
            raise Exception("Cannot draw a TH2 while more than 1 datasets are present.")
        else:
            return


    def IsTypeTH2(self, histo):
        '''
        Check if histoObject is of type ROOT.TH2
        '''

        hType = type(histo)

        if "TH2" in str(hType):
            return True
        else:
            return False


    def IsValidHistoObject(self, histoObject):
        ''''
        Ensure that the histoObject is of valid type (histos.TH1 or histos.TH2). Raise an exception otherwise.
        '''
        self.Verbose()

        if isinstance(histoObject, histos.TH1orTH2):
            return
        else:
            self.Print("ERROR!", "Unknown histo type. Please make sure the histo object '%s' (type = '%s') is either a TH1 or a TH2" % (histoObject, type(histoObject)), "EXIT")
            sys.exit()            


    def CheckThatHistoExists(self, rootFile, hObject):
        '''
        Ensure that the histogram you are trying to get from a TFile really exists.
        '''
        self.Verbose()
        
        hPath = ""
        if (hObject.path == "") or (hObject.path == None):
            hPath = hObject.name
        else:
            hPath = hObject.path + "/" + hObject.name

        self.IsTH1 = isinstance( rootFile.Get(hPath), ROOT.TH1F)
        self.IsTH2 = isinstance( rootFile.Get(hPath), ROOT.TH2D)

        if not self.IsTH1 and not self.IsTH2:
            raise Exception( "Could not find histo object '%s' in TFile '%s' under folder '%s'." % (hObject.name, rootFile.GetName(), hObject.path) )
        else:
            msg  = " {:<20} {:<20}".format("File", ": " + rootFile.GetName())
            msg += "\n\t {:<20} {:<20}".format("Histo", ": " + hPath)
            msg += "\n\t {:<20} {:<20}".format("IsTH1", ": " + str( self.IsTH1) )
            msg += "\n\t {:<20} {:<20}".format("IsTH2", ": " + str( self.IsTH2) )
            self.Print(msg)
            return

        return


    def CreateDumbie(self, THDumbie=None):
        '''
        Create a dumbie histogram that will be the first to be drawn on each canvas. 
        This should have zero entries but have exactly the same attribues  (binning, axes titles etc..) as the ones to be drawn.
        '''
        self.Verbose()

        myMax = -1E10
        myMin = +1E10
        # Loop over all TH1's and determine dataset histo with yMax
        #for dataset in self.DatasetToHistoMap.keys():
        for dataset in self.Datasets:
            #h = self.DatasetToHistoMap[dataset]
            h = dataset.histo
            tmpMax =  h.TH1orTH2.GetMaximum()
            if tmpMax > myMax:
                myMax = h.yMax
                myMin = h.yMin
                #self.THDumbie = copy.deepcopy(self.DatasetToHistoMap[dataset])
                self.THDumbie = copy.deepcopy(h)
                self.THDumbie.TH1orTH2.SetName("THDumbie")
            else:
                continue

        # Reset only Integral, Contents, Errors and Statistics (not Minimum and Maximum)
        self.THDumbie.TH1orTH2.Reset("ICES")

        # Set custom range for x- and y- axis and pad margins            
        self.THDumbie.TH1orTH2.GetYaxis().SetRangeUser(myMin, myMax)
        self.THDumbie.TH1orTH2.GetXaxis().SetRangeUser(h.xMin, h.xMax) #does nothing if xMax > max x-value when histogram was created

        # Set Number of divisions! 
        if (self.IsTH2):
            self.THDumbie.TH1orTH2.GetXaxis().SetNdivisions(510) 
        else:
            #self.THDumbie.TH1orTH2.GetXaxis().SetNdivisions(510) #default
            self.THDumbie.TH1orTH2.GetXaxis().SetNdivisions(505)

        # Set Line Colour and Width
        self.THDumbie.TH1orTH2.SetLineColor(ROOT.kBlack)
        self.THDumbie.TH1orTH2.SetLineWidth(1)

        # Increase right pad margin to accomodate z-axis scale and title
        if isinstance(self.THDumbie.TH1orTH2, ROOT.TH2) == True:
            ROOT.gStyle.SetPadRightMargin(0.15)
            #ROOT.gStyle.SetPadRightMargin(0.15)
        return
                

    def AppendToDrawObjectList(self, objectToBeDrawn):
        '''
        Append a drawable object of any type (TCanvas, TLegend, TLine, TBox, etc..) to a list.
        This list will be used later on to draw all objects.
        '''
        self.Verbose()

        self.DrawObjectList.append(objectToBeDrawn)
        self.DrawObjectListR.append(copy.deepcopy(objectToBeDrawn))
        return 

        
    def EnableColourPalette(self, bEnable=False):
        '''
        Changes colour for each histogram within a given dataset only if 1 dataset is present.
        '''
        self.Verbose()
        
        self.StyleObject.EnableColourPalette(bEnable)
        return


    def _CustomiseHistograms(self):
        '''
        Customise all histograms found inside the DatasetToHistoMap.
        '''
        self.Verbose()
        
        # For-loop: All datasets
        for histo in self.HistoObjectList:
            histo.ApplyStyles( self.StyleObject, type(histo.TH1orTH2))
        return

    
    def _NormaliseHistograms(self):
        '''
        Normalise all histograms found inside the DatasetToHistoMap.
        '''
        self.Verbose()
        
        # Loop over all histograms and normalise according to user options
#        for mapKey in self.DatasetToHistoMap:
#            h = self.DatasetToHistoMap[mapKey]
#            self._NormaliseHisto(h)
        for dataset in self.Datasets:
            self._NormaliseHisto(dataset.histo)
        return


    def _NormaliseHisto(self, h):
        '''
        Normalise the histoObject passed to this function according to user-specified criteria. 
        '''
        self.Verbose()
        
        if h.normaliseTo=="":
            return

        scaleFactor = 1
        if h.TH1orTH2.GetEntries() == 0:
            self.Print("WARNING! Cannot normalise histogram.", "HistoName: '%s'" % (h.name), "Entries: '%s'" % (h.TH1orTH2.GetEntries()), "TFile: '%s'" % (h.TFileName))
            return
        
        if h.normaliseTo == "One":
            scaleFactor = h.integral #Note: Using h.rangeIntegral is wrong, as it might depend on histogram binning and maximum of x-axis!
            if scaleFactor!=0:
                h.scaleFactor = 1.0/scaleFactor
                h.TH1orTH2.Scale(h.scaleFactor)
            else:
                self.Print("WARNING! Cannot normalise histogram. Will do nothing.", "HistoName: '%s'" % (h.name), "TFile: '%s'" % (h.TFileName), "ScaleFactor: '%s'" % (scaleFactor))
                return
        elif h.normaliseTo == "MB@40MHz":
            ConvertRateTokHz  = 1.0E-3
            CrossingRate      = 40.0E+6 #Hz
            MCEventsTotal     = 100.0 #self.DatasetObject.GetEvents(h.dataset)
            self.Print("FIXME")
            scaleFactor       = (CrossingRate)/(MCEventsTotal)*ConvertRateTokHz
            h.scaleFactor     = scaleFactor
            h.TH1orTH2.Scale(scaleFactor)
        elif h.normaliseTo == "MB@30MHz":
            ConvertRateTokHz  = 1.0E-3
            CrossingRate      = 30.0E+6 #Hz
            MCEventsTotal     = 100.0 #self.DatasetObject.GetEvents(h.dataset)
            self.Print("FIXME")
            scaleFactor       = (CrossingRate)/(MCEventsTotal)*ConvertRateTokHz
            h.scaleFactor     = scaleFactor
            h.TH1orTH2.Scale(scaleFactor)
        elif type(h.normaliseTo) == float:
            h.scaleFactor     = float(h.normaliseTo)
            h.TH1orTH2.Scale(h.scaleFactor)
        else:
            raise Exception("Unknown histoObject normalisation option '%s'.!" % (h.normaliseTo))
        
        self.Verbose("File: '%s'" % (h.TFileName), "Dataset: '%s'" % (h.dataset), "HistoPath: '%s'" % (h.path), "HistoName: '%s'" % (h.name), 
                      "Integral(): '%s'" % (h.rangeIntegral), "Integral(0, nBins+1): '%s'" % (h.integral), "normaliseTo: '%s'" % (h.normaliseTo))
        return


    def Draw(self, THStackDrawOpt="nostack", bStackInclusive=False, bAddReferenceHisto=True):
        '''
        Draw all necessary histograms for all datasets.
        '''
        self.Verbose()

        self.bStackInclusive = bStackInclusive
        self._NormaliseHistograms()
        self._CustomiseHistograms()
        self._CreateCanvasAndLegendAndDumbie()
        self._CheckHistogramBinning()
        self._AddHistogramsToStack()
        #self.Verbose("Drawing histo '%s'" % (self.THDumbie.name) + "THStackDrawOpt: '%s'" % (THStackDrawOpt), "bStackInclusive: '%s'" % (bStackInclusive))
        
        self._DrawHistograms(THStackDrawOpt)
        self._DrawRatioHistograms(bAddReferenceHisto)
        self._DrawNonHistoObjects()
        self._CustomiseStack()
        #self.THStack.Draw("same")            #new: needed when drawing cut-boxes
        #self.TLegend.Draw("same")            #new: needed when drawing cut-boxes
        #self.AddPreliminaryText()             #new: needed when drawing cut-boxes
        self.THDumbie.TH1orTH2.Draw("same")
        return


    def ConvertHistosToEfficiency(self, cutDirection=">",  errType = "binomial",  **kwargs):
        '''
        Draw all necessary histograms for all datasets.
        '''
        self.Verbose()

        self._ConvertToEfficiencyHistos(cutDirection, errType, **kwargs)
        return


    def DrawSame(self, HistoObjectList, TLegendHeader=""):
        '''
        This was designed to be used  in conjuction with GetHistos(). 
        For example:

        p1 = plotter.Plotter( verbose, bBatchMode )
        for dataset in datasetList:
           p1.AddDataset(dataset, datasetPaths[dataset])
        p1.AddHisto(hList1)
        p1.Draw(THStackDrawOpt="nostack", bStackInclusive = False)
        
        p2 = plotter.Plotter( verbose, bBatchMode )
        for dataset in datasetList:
           p2.AddDataset(dataset, datasetPaths_D[dataset])
        p2.AddHisto(hList2)
        p2.Draw(THStackDrawOpt="nostack", bStackInclusive = False)
        p2.DrawSame(p1.GetHistos())
        p2.SaveHistos(bSavePlots, mySavePath, mySaveFormats)
        '''
        self.Verbose()

        for h in HistoObjectList:
            self.IsValidHistoObject(h)
            h.ApplyStyles( self.StyleObject, type(h.TH1orTH2))
            h.TH1orTH2.Draw(h.drawOptions + ",9same,")
            self.TLegend.AddEntry( h.TH1orTH2, h.legTitle, self._GetLegEntryOptions(h) )
            self.TLegend.SetY1( self.TLegend.GetY1() - 0.02)

        self.TLegend.SetHeader(TLegendHeader)
        self.THDumbie.TH1orTH2.Draw("same")
        return


    def Draw2DProfile(self, THStackDrawOpt="nostack", bStackInclusive=False, ProfileAxis=None, firstBin=1, lastBin=-1):
        '''
        Draw a ProfileX or ProfileY of a TH2D. Basically, this will plot a weighted 2D histo with a single entry replacing 
        all entries in X (or Y axis). The entry that replaces all other entries in the Profile direction is the average.

        Profile histograms are used to display the mean value of Y and its error for each bin in X. The displayed error is by default the
        standard error on the mean (i.e. the standard deviation divided by the sqrt(n) ). Profile histograms are in many cases an elegant 
        replacement of two-dimensional histograms : the inter-relation of two histogram or scatter-plot; its representation on the line-printer 
        is not particularly satisfactory, except for sparse data. If Y is an unknown (but single-valued) approximate function of X, this function
        is displayed by a profile histogram with much better precision than by a scatter-plot.
        See: http://root.cern.ch/root/html/TProfile.html
        '''
        self.Verbose()

        allowedValues = [None, "x", "y"]
        if ProfileAxis not in allowedValues:
            raise Exception("Invalid ProfileAxis option selected ('%s'). You need to speficy the axis of the Profile (x or y). Available options are 'x' and 'y'." % (ProfileAxis) )

        self.bStackInclusive = bStackInclusive
        self.EnableColourPalette(True)
        self._NormaliseHistograms()
        self._CustomiseHistograms()
        self._CreateCanvasAndLegendAndDumbie()
        self._CheckHistogramBinning()
        self._AddHistogramsToStack2D(ProfileAxis, firstBin, lastBin)
        self.Verbose("Drawing histo '%s'" % (self.THDumbie.name), "THStackDrawOpt: '%s'" % (THStackDrawOpt), "bStackInclusive: '%s'" % (bStackInclusive))
        self._DrawHistograms(THStackDrawOpt)
        self._DrawRatioHistograms()
        self._DrawNonHistoObjects()
        self._CustomiseStack()
        self.THDumbie.TH1orTH2.Draw("same")
        return


    def AddTF1(self, myFunction, xMin, xMax, kwargs={}):
        '''
        '''
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

        self.AppendToDrawObjectList(f1)
        return


    def _AddHistogramsToStack(self):
        '''
        Add all histograms (except Dumbie) to a THStack. For each histogram add a TLegend entry
        and automatically extend the size of the TLegend to accomodate the next entry.
        '''
        self.Verbose()

        bAddLegendEntries = "TH1" in str(type(self.THDumbie.TH1orTH2)) and isinstance(self.TLegend, ROOT.TLegend)
        entryLabel = ""
        
        # Loop over all histo objects
        for histo in self.HistoObjectList:
            
            dataset = histo.dataset.name
            #histo   = histo.dself.DatasetToHistoMap[dataset] #self.DatasetToHistoMap[dataset] 

            # Add legend entries for THStack
            self.THStack.Add(histo.TH1orTH2)
            self.THStackHistoList.append(histo.TH1orTH2)
            

            if bAddLegendEntries == False:
                continue

            # Add legend entries only for TH1 type histos        
            if histo.legTitle != None:
                self.TLegend.AddEntry( histo.TH1orTH2, self._GetLegEntryLabel(histo), self._GetLegEntryOptions(histo) )
                self.TLegend.SetY1( self.TLegend.GetY1() - 0.02)
        return


    def _CustomiseStack(self):
        '''
        Customise the THStack. Apply x- and y-axis range. Can also implement the inclusive error bar (if histos stacks) in the future,
        by cloning the stack and drawing only the errors with "E1" option?
        '''
        self.Verbose()
        self.THStack.GetYaxis().SetRangeUser(self.THDumbie.yMin, self.THDumbie.yMax)
        self.THStack.GetXaxis().SetRangeUser(self.THDumbie.xMin, self.THDumbie.xMax)
        return


    def _CreateCanvasAndLegendAndDumbie(self):
        '''
        Create a TCanvas, a TLegend, and a dubmie TH1.
        '''
        self.Verbose()

        self.CreateDumbie()
        if self.bPadRatio == True or self.bInvPadRatio == True:
            self._Create2PadCanvas()
        else:
            self._CreateCanvas()

        self._CreateLegend()
        return

        
    def CreateCutLines(self):
        '''
        Create TLines for each cut-line defined by the user when creating a histo instance. 
        Append them to the DrawObjectList so that they can be drawn later on.
        '''
        self.Verbose("Creating cut-lines.")

        # Create the TLines for each axis
        self._AppendXYCutLinesToTLineList("x")
        self._AppendXYCutLinesToTLineList("y")
        self._DoZCutLines()

        # Extend the DrawObjectList with the TLineList
        self.DrawObjectList.extend(self.xTLineList)
        self.DrawObjectList.extend(self.yTLineList)

        self.DrawObjectListR.extend( copy.deepcopy(self.xTLineList) )
        if (self.THDumbie.yCutLinesRatioPad == True):
            self.DrawObjectListR.extend( copy.deepcopy(self.yTLineList) )
        return


    def _AppendXYCutLinesToTLineList(self, axis):
        '''
        Create, customise and append x- or y-axis cut lines to the TLineList. Also add entry to TLegend and provide extra space for another TLegened entry.
        '''
        self.Verbose()

        bXaxisCut = False
        bYaxisCut = False

        if axis == "x":
            bXaxisCut = True
            cLines = self.THDumbie.xCutLines
        elif axis == "y":
            bYaxisCut = True
            cLines = self.THDumbie.yCutLines
        else:
            raise Exception("The option 'axis' can either be \"x\" or \"y\". Passed option was \"%s\"." % (axis) )

        if cLines == None:
            return
                
        # Loop over all x-axis cut values
        for value in cLines:
            if bXaxisCut == True:
                xMin = value
                xMax = value
            else:
                xMin = self.THDumbie.xMin
                xMax = self.THDumbie.xMax

            if bYaxisCut == True:
                yMin = value
                yMax = value
            else:
                yMin = self.THDumbie.yMin
                yMax = self.THDumbie.yMax

            line = ROOT.TLine(xMin, yMin, xMax, yMax)
            self._CustomiseTLine(line, lineColour=self.CutLineColour, lineWidth=3, lineStyle=ROOT.kDashed) #ROOT.kDashDotted
            self.TLegend.SetY1( self.TLegend.GetY1() - 0.02)
            self.AppendToTLineList( line, axis)

        return


    def _DoZCutLines(self):
        '''
        Create, customise and append z-axis cut lines to the TLineList. Also add entry to TLegend and provide extra space for another TLegened entry.
        "CONT"	 Draw a contour plot (same as CONT0).
        "CONT0"	 Draw a contour plot using surface colors to distinguish contours.
        "CONT1"	 Draw a contour plot using line styles to distinguish contours.
        "CONT2"	 Draw a contour plot using the same line style for all contours.
        "CONT3"	 Draw a contour plot using fill area colors.
        "CONT4"	 Draw a contour plot using surface colors (SURF option at theta = 0).
        "CONT5"	 (TGraph2D only) Draw a contour plot using Delaunay triangles.
        See http://root.cern.ch/root/html/THistPainter.html for contour draw options!
        '''
        self.Verbose()

        zCutLines = self.THDumbie.zCutLines
        if zCutLines == None or len(zCutLines)==0:
            return
        
        # Copy list into a numpy array, otherwise ROOT will complain
        contours = numpy.asarray(self.THDumbie.zCutLines)
        if (self.THDumbie.zCutLinesErrors == True):
            self._DrawZCutLinesWithErrors(zCutLines)
        else:
            self.DrawZCutLines(zCutLines)
        return


    def _DrawZCutLinesWithErrors(self, zCutLines):
        '''
        Draw z-cut lines defined by the user at histogram creation time.
        Add error bands around the nominal contour that correspond to +/- 1 sigma.
        For information regarding the extraction of the contours as TGraphs see:
        http://root.cern.ch/root/html/THistPainter.html
        [ Look for Draw("CONT LIST") option ]
        '''
        # Copy list into a numpy array, otherwise ROOT will complain
        contours = numpy.asarray(self.THDumbie.zCutLines)

        # Set Contour bands
        contourBands   = [1.0, 1.0/self.THDumbie.scaleFactor, 1.0/self.THDumbie.scaleFactor]
        lineStyles     = [ROOT.kSolid, ROOT.kDashDotted, ROOT.kDashDotted] #[ROOT.kSolid, ROOT.kSolid, ROOT.kSolid] #,ROOT.kDashed, ROOT.kDashed]
        lineColours    = [self.CutLineColour, ROOT.kRed-4, ROOT.kAzure+6, ROOT.kSpring+2, ROOT.kMagenta-2, ROOT.kYellow-4, self.CutLineColour, ROOT.kOrange+8, 
                          ROOT.kBlue-4, ROOT.kGreen-2, ROOT.kViolet-5, ROOT.kPink-8, ROOT.kTeal-1, ROOT.kCyan-7, 
                          self.CutLineColour, ROOT.kRed-4, ROOT.kAzure+6, ROOT.kSpring+2, ROOT.kMagenta-2, ROOT.kYellow-4, self.CutLineColour, ROOT.kOrange+8,
                          ROOT.kBlue-4, ROOT.kGreen-2, ROOT.kViolet-5, ROOT.kPink-8, ROOT.kTeal-1, ROOT.kCyan-7]
        lineShades     = [+0, -3, -3]
        lineWidths     = [+3, +1, +1]
        
        # Get Last histogram in the stack and customise it
        hStackList = []
        total = len(zCutLines)*len(contourBands)
        for i in range(0, total ):
            hStackList.append(copy.deepcopy(self.THStack.GetStack()))

        # Declare the arrays where the contours values (nominal, Up, Down) will be saved
        tmpHistoDict = {}

        # for-Loop: Over all histogram types (Nominal, FluctuateUp, FluctuateDown)
        for iBand in range(0, len(contourBands)): 

            # Get the total histogram
            h = hStackList[iBand].Last()

            # Default, Fluctuate up or Fluctuate down
            if iBand == 0:
                histoType = "Nominal"
            elif iBand == 1: # +1sigma
                self.FluctuateHisto(h, contourBands[iBand], True)
                histoType = "FluctuateUp"
            elif iBand == 2: # -1sigma
                self.FluctuateHisto(h, contourBands[iBand], False)
                histoType = "FluctuateDown"
            else:
                pass

            h.SetName(h.GetName() + "_" + histoType )
            tmpHistoList = []

            # for-Loop: Over all z-cuts, for the given iBand(0 = Nominal, 1 = +1sigma, 2 = -1sigma)
            for i in range(0, len(zCutLines)):
                self.Verbose( ["iHistoType: '%s'/'%s' (Nominal, FluctuateUp, FluctuateDown)" % (iBand+1, len(contourBands) ), "zCutNumber: '%s'/'%s'" % (i+1, len(zCutLines)) ] )
                h.SetLineColor( lineColours[i] )
                h.SetFillColor( lineColours[i] + lineShades[iBand] )
                h.SetLineStyle( lineStyles[iBand] )
                h.SetLineWidth( lineWidths[iBand] )
                h.SetContour(i+1, contours) #should start at 1

                # Before drawing, save the histogram to some list
                if self.SaveContourPoints == True:
                    tmpHistoList.append(h)

                # Draw the histogram
                h.Draw("cont3same9")

                if iBand == 0:
                    self.TLegend.AddEntry( h, "%s %s #pm 1#sigma" % (zCutLines[i], self.THDumbie.zUnits), "L" )
                    self.TLegend.SetY1( self.TLegend.GetY1() - 0.02)

            # Save the Nominal, FluctuateUp, FluctuateDown histos for the specific cut value
            tmpHistoDict[ histoType ] = tmpHistoList

        self.SaveContourPointsToFile(tmpHistoDict)
        return


    def DrawZCutLines(self, zCutLines):
        '''
        Draw z-cut lines defined by the user at histogram creation time.
        '''
        # Copy list into a numpy array, otherwise ROOT will complain
        contours = numpy.asarray(self.THDumbie.zCutLines)

        # Set Contour bands
        lineColours    = [ROOT.kWhite, ROOT.kYellow, ROOT.kRed, ROOT.kBlack]
        
        # Get Last histogram in the stack and customise it
        hStackList = []
        total = len(zCutLines)
        for i in range(0, total ):
            hStackList.append(copy.deepcopy(self.THStack.GetStack()))
        
        # Loop over all z-cuts
        for i in range(0, len(zCutLines)):
            # Get the total histogram
            h = hStackList[i].Last()
            h.SetLineColor( lineColours[i] )
            h.SetFillColor( lineColours[i] )
            h.SetLineStyle( ROOT.kSolid )
            h.SetLineWidth( 3 )
            h.SetContour(i+1, contours) #should start at 1
            h.Draw("cont3same9")
            self.TLegend.AddEntry( h, "%s %s" % (zCutLines[i], self.THDumbie.zUnits), "L" )
            self.TLegend.SetY1( self.TLegend.GetY1() - 0.02)
        return



    def FluctuateHisto(self, histo, scaleFactor, bFluctuateUp):
        '''
        Statistical fluctuation of histograms to enable contour error bands.
        '''
        # Reverse scaleFactor
        histo.Scale( scaleFactor )
        zeroEntriesPoissonError = 1.7 #As instructed by Ptochos

        if "TH1" in str(type(histo)):
            # Fluctate with bin content with sqrt(N)
            for x in range(0, histo.GetNbinsX()):
                binContent = histo.GetBinContent(x)
                if (bFluctuateUp == True):
                    if binContent < 1.0:
                        histo.SetBinContent(x, histo.GetBinContent(x) + scaleFactor*zeroEntriesPoissonError )
                    else:
                        histo.SetBinContent(x, histo.GetBinContent(x) + scaleFactor*math.sqrt(histo.GetBinContent(x)) )
                else:
                    if binContent > 0.0:
                        histo.SetBinContent(x, histo.GetBinContent(x ) - scaleFactor*math.sqrt(histo.GetBinContent(x)) )
                    else:
                        histo.SetBinContent(x, binContent) # do nothing
        elif "TH2" in str(type(histo)):
            # Fluctate with bin content with sqrt(N)
            for x in range(0, histo.GetNbinsX()):
                for y in range(0, histo.GetNbinsY()):
                    binContent = histo.GetBinContent(x, y)
                    if (bFluctuateUp == True):
                        if binContent < 1.0:
                            histo.SetBinContent(x, y, histo.GetBinContent(x, y) + scaleFactor*zeroEntriesPoissonError )
                        else:
                            histo.SetBinContent(x, y, histo.GetBinContent(x, y) + scaleFactor*math.sqrt(histo.GetBinContent(x, y)) )
                    elif (bFluctuateUp == False):
                        if binContent > 0.0:
                            histo.SetBinContent(x, y, histo.GetBinContent(x, y) - scaleFactor*math.sqrt(histo.GetBinContent(x, y)) )
                        else:
                            histo.SetBinContent(x, y, binContent) # do nothing
        else:
            raise Exception("Unsupported histo type '%s'. Cannot proceed." % (type(histo) ) )

        # Scale back to normal
        histo.Scale( 1.0/scaleFactor )
        return
        

    def CreateCutBoxes(self):
        '''
        Create TBoxes with associated TLines (custom colour) for each list of cut-range defined by the user when creating a histo instance. 
        Append them to the DrawObjectList so that they can be drawn later on.
        '''
        self.Verbose()
        
        # Loop over list of xMin-xMax-colour pairs (also a list)
        self._AppendXYCutBoxesToTBoxList("x")
        self._AppendXYCutBoxesToTBoxList("y")

        # Extend the DrawObjectList with the TLineList and TBoxList
        self.DrawObjectList.extend(self.xTLineList)
        self.DrawObjectList.extend(self.yTLineList)
        self.DrawObjectList.extend(self.TBoxList)

        self.DrawObjectListR.extend(copy.deepcopy(self.xTLineList))
        if (self.THDumbie.yCutLinesRatioPad == True):
            self.DrawObjectListR.extend(copy.deepcopy(self.yTLineList))
            self.DrawObjectListR.extend(copy.deepcopy(self.TBoxList))
        return


    def _AppendXYCutBoxesToTBoxList(self, axis):
        '''
        Create, customise and append x- or y-axis cut boxes to the TBoxList. Also add entry to TLegend and provide extra space for another TLegened entry.
        '''
        self.Verbose()


        bXaxisCut = False
        bYaxisCut = False
        if axis == "x":
            bXaxisCut = True
            cBoxes = self.THDumbie.xCutBoxes
        elif axis == "y":
            bYaxisCut = True
            cBoxes = self.THDumbie.yCutBoxes
        else:
            raise Exception("The option 'axis' can either be \"x\" or \"y\". Passed option was \"%s\"." % (axis) )

        if cBoxes == None:
            return

        for v in cBoxes:
            if bXaxisCut == True:
                xMin = v[0]
                xMax = v[1]
            else:
                xMin = self.THDumbie.xMin
                xMax = self.THDumbie.xMax

            if bYaxisCut == True:
                yMin = v[0]
                yMax = v[1]
            else:
                yMin = self.THDumbie.yMin
                yMax = self.THDumbie.yMax

            cutBox  = ROOT.TBox( xMin, yMin, xMax, yMax)
            if bXaxisCut == True:
                cLine1  = ROOT.TLine(xMin, yMin, xMin, yMax)
                cLine2  = ROOT.TLine(xMax, yMin, xMax, yMax)
            else:
                cLine1  = ROOT.TLine(xMin, yMin, xMax, yMin)
                cLine2  = ROOT.TLine(xMin, yMax, xMax, yMax)
            cLine1.SetLineColor(v[2])
            cLine2.SetLineColor(v[2])
            cLine1.SetLineWidth(1)
            cLine2.SetLineWidth(1)
            self.TLegend.SetY1( self.TLegend.GetY1() - 0.02)
            self.AppendToTLineList( cLine1, axis)
            self.AppendToTLineList( cLine2, axis )
            self.AppendToTBoxList(cutBox, boxColour= v[2] )
        return


    def _DrawHistograms(self, THStackDrawOpt):
        '''
        Draw the THDumbie. Draw the THStack . Create the CutBoxes and CutLines. 
        Re-draw the TH1Dubmie to unhide the hidden tickmards (true when drawing histograms 
        will fill style 1001. Draw all objects in the DrawObjectList.
        For drawing options (TH1, TH2, THStack etc..) see:
        http://root.cern.ch/root/html/THistPainter.html
        '''
        self.Verbose()

        self.THDumbie.TH1orTH2.Draw(self.THDumbie.drawOptions)
        self.DrawStackInclusive()
        self.THStack.Draw(THStackDrawOpt + "," + self.THDumbie.drawOptions + "," +  "9same") #"PADS"
        ROOT.gPad.RedrawAxis() #the histo fill area may hide the axis tick marks. Force a redraw of the axis over all the histograms.
        # self.AddPreliminaryText()
        self.TCanvas.Update()
        self.TCanvas.SetGridx(self.THDumbie.gridX)
        self.TCanvas.SetGridy(self.THDumbie.gridY)
        return


    def _DrawRatioHistograms(self, bAddReferenceHisto=True):
        '''
        Draw all plots on the PadRatio (if applicable).
        For efficiencies and errors see:
        http://steve.cooleysekula.net/goingupalleys/2011/08/09/python-and-root-tricks-efficiency-graphs/
        '''
        self.Verbose()

        if self.bPadRatio == False and self.bInvPadRatio == False:
            return

        self.PadRatio.cd()        

        # Create the histogram that will divide all other histograms in the THStackRatio (Normalisation histogram)
        UnityTH1 = self.GetUnityTH1()
        hDenominator = copy.deepcopy( self.THStackHistoList[0] ) 
        self.Verbose("Using histogram '%s' as denominator for ratio plots! " % (hDenominator.GetName()))

        # Add the reference ratio plot (to enable the identification of the histogram used for the normalisation)
        # Note: Do not add the hReference histogram  before calling the function self.CustomiseTHRatio(). 
        if bAddReferenceHisto:
            hReference = copy.deepcopy(hDenominator)
            hReference.Divide(hReference)
            hReference.SetMarkerSize(0)
            hReference.SetLineStyle(ROOT.kSolid)            
            for iBin in range (1, hReference.GetNbinsX()+1):
                hReference.SetBinError(iBin, 0.00000000001)
            self.THStackRatio.Add(hReference)

        # Loop over all histograms in the THStack and create the THStackRatio.
        for h in self.THStackHistoList:
            if h == self.THStackHistoList[0]:                
                continue

            # Copy Active histogram
            hRatio     = copy.deepcopy(h)
            hNumerator = copy.deepcopy(h)
            
            # Divide the active histogram with the normalisation histogram
            hRatio.Divide(hNumerator, hDenominator, 1.0, 1.0, self.RatioErrorType)

            # Inverts ratio histogram if requested (i.e. each bin has content 1/bin)
            if self.bInvPadRatio == True:
                hRatio.Divide(UnityTH1, hRatio) 

            # Save histogram values to a txt file (for later processing if needed)
            #self.SaveHistoAsTxtFile(hRatio)

            # Finally, add this ratio histogram to the THStackRatio
            self.THStackRatio.Add(hRatio)

        # Customise axes and titles
        self.CustomiseTHRatio()

        # Draw the Ratio Stack with "nostack" option
        self.THRatio.TH1orTH2.Draw()
        self.THStackRatio.Draw("nostack9sameAP")
        
#        # Finally add the reference ratio plot (to enable the identification of the histogram used for the normalisation)
#        # Note: Do not add the hReference histogram  before calling the function self.CustomiseTHRatio(). 
#        if bAddReferenceHisto:
#            hReference = copy.deepcopy(hDenominator)
#            hReference.Divide(hReference)
#            hReference.SetMarkerSize(0)
#            hReference.SetLineStyle(ROOT.kSolid)            
#            for iBin in range (1, hReference.GetNbinsX()+1):
#                hReference.SetBinError(iBin, 0.00000000001)
#            self.THStackRatio.Add(hReference)

        # Switch back to the PadPlot (necessary)
        self.PadPlot.cd()
        return

    
    def SaveHistoAsTxtFile(self, h):
        '''
        '''
        self.Verbose()
        print "Fix me. Saving as .txt not needed anymore. EXIT"
        sys.exit()

        xVals     = []
        xErrDown  = []
        xErrUp    = []
        yVals     = []
        yErrDown  = []
        yErrUp    = []

        # Loop over all histogram bins (except under/over bins)
        binZeroWidth = h.GetXaxis().GetBinWidth(0)
        for iBin in range (1, h.GetNbinsX()+1):

            xVals.append( h.GetBinCenter(iBin) ) #h.GetBinCenter(iBin)
            xErrUp.append( binZeroWidth/2.0 )
            xErrDown.append( binZeroWidth/2.0 )

            yVals.append( h.GetBinContent(iBin) )
            yErrUp.append( h.GetBinErrorUp(iBin) )
            yErrDown.append( h.GetBinErrorLow(iBin) )
        self.SaveTGraphArraysDataToFile( h.GetName() + ".txt", xVals, xErrUp, xErrDown, yVals, yErrUp, yErrDown, 3)
        return



    def CustomiseTHRatio(self):
        '''
        Apply all necessary customisations to self.THRatio histogram.
        '''

        # Customise axes and titles
        if self.THRatio.yMinRatio == None:
            self.THRatio.yMinRatio = self.THStackRatio.GetMinimum("nostack")*self.THRatio.GetYMinFactor(self.THRatio.logYRatio)
        if self.THRatio.yMaxRatio == None:
            self.THRatio.yMaxRatio = self.THStackRatio.GetMaximum("nostack")*self.THRatio.GetYMaxFactor(self.THRatio.logYRatio)

        # Customise the title
        self.THRatio.TH1orTH2.GetXaxis().SetTitleOffset(2.8)
        if self.THRatio.ratioLabel == None:
            if self.bInvPadRatio == False:
                self.THRatio.ratioLabel = "Ratio"
            else:
                self.THRatio.ratioLabel = "1/Ratio"
        self.THRatio.TH1orTH2.GetYaxis().SetTitle(self.THRatio.ratioLabel)

        # Customise the y-axis
        self.THRatio.yMax = self.THRatio.yMinRatio
        self.THRatio.yMin = self.THRatio.yMaxRatio
        self.THRatio.TH1orTH2.GetYaxis().SetNdivisions(505)
        self.THRatio.TH1orTH2.GetYaxis().SetRangeUser(self.THRatio.yMinRatio, self.THRatio.yMaxRatio)
        self.THRatio.TH1orTH2.GetYaxis().SetTitleOffset(1.8) 
        self.THDumbie.TH1orTH2.GetYaxis().SetTitleOffset(1.8)
        
        # Enable grid to easy readout of histo
        self.PadRatio.SetGridx(self.THDumbie.gridX)
        self.PadRatio.SetGridy(self.THDumbie.gridY)
        return


    def DrawStackInclusive(self):
        '''
        The GetStack function returns a TObjArray* of TH1* where the TH1 at index i is the sum of histograms 0->i.
        TObjArray::Last() returns the last TH1 in the list, hence the sum of all TH1.
        For help see: http://root.cern.ch/phpBB3/viewtopic.php?f=3&t=12138
        '''
        self.Verbose()
        if self.bStackInclusive==False:
            return

        inclusive = self.THStack.GetStack().Last()
        inclusive.SetFillStyle(0)
        inclusive.SetFillColor(ROOT.kGray)
        inclusive.SetLineColor(ROOT.kGray)
        inclusive.SetLineStyle(ROOT.kSolid)
        inclusive.SetLineWidth(3)

        if self.THDumbie.yMax < inclusive.GetMaximum():
            yMaxNew = inclusive.GetMaximum()
            h       = self.THDumbie
            h.yMax  = yMaxNew*h.GetYMaxFactor(self.THDumbie.logY)
            h.TH1orTH2.GetYaxis().SetRangeUser(h.yMin, h.yMax)        
        else:
            pass
        inclusive.Draw("HISTsame9")
        
        # Add histogram entry to the legend
        self.TLegend.AddEntry( inclusive, "inclusive", "L" )
        self.TLegend.SetY1( self.TLegend.GetY1() - 0.02)

        return


    def _GetLegEntryLabel(self, histoObject):
        '''
        Determine and return the TLegenend entry label for this instance of histogram object.
        '''
        self.Verbose()
        
        entryLabel = "empty"
        if histoObject.legTitle == None:            
            return  entryLabel

        if self.DatasetInLegend:
            entryLabel = histoObject.dataset.GetLatexName()
        else:
            entryLabel = histoObject.legTitle

        if isinstance(entryLabel, str) == True:
            self.Verbose("The TLegend entry name is '%s'." % (entryLabel))
            return entryLabel
        else:
            raise Exception("The TLegend entry label cannot be returned as it is not of type string but instead of type '%s'." % ( type(entryLabel) ) )


    def _GetLegEntryOptions(self, histoObject):
        '''
        Determine the draw options for all histograms in the THStack by examining the TLegend entry styles:
        "L": draw line associated with TAttLine if obj inherits from TAttLine
        "P": draw polymarker associated with TAttMarker if obj inherits from TAttMarker
        "F": draw a box with fill associated wit TAttFill if obj inherits TAttFill
        "E": draw vertical error bar
        '''
        self.Verbose()
        
        options = histoObject.legOptions
        #if self.bPadRatio == False and  self.bInvPadRatio == False:
        #    options = histoObject.legOptions
        #else:
        #    options = histoObject.legOptions + "P"
        return options


    def AppendToTLineList(self, line, axis):
        '''
        Append a TLine to the TLineList. 
        '''
        self.Verbose()

        if axis == "x":
            self.xTLineList.append(line)
        elif axis == "y":
            self.yTLineList.append(line)
        else:
            raise Exception("The option 'axis' can either be \"x\" or \"y\". Passed option was \"%s\"." % (axis) )

        return


    def _CustomiseTLine(self, line, lineColour=ROOT.kBlack, lineWidth=3, lineStyle=ROOT.kSolid):
        '''
        '''
        self.Verbose()

        line.SetLineWidth(lineWidth)
        line.SetLineStyle(lineStyle)
        line.SetLineColor(lineColour)
        line.Draw()
        return


    def AppendToTBoxList(self, box, boxColour=18):
        '''
        Append a TBox to the TBoxList. 
        '''
        self.Verbose()
        box.SetFillStyle(3003) #3003
        box.SetFillColor(boxColour)
        self.TBoxList.append(box)
        return


    def _DrawNonHistoObjects(self):
        '''
        Draw all drawable objects found in self.DrawObjectList.
        '''
        self.Verbose()                

        if (self.bPadRatio == True or self.bInvPadRatio == True):
            self._DrawNonHistoObjectsWithPadRatio()
        else:
            self._DrawNonHistoObjectsNoPadRatio()        
        return


    def _DrawNonHistoObjectsNoPadRatio(self):
        '''
        Draw all drawable objects found in self.DrawObjectList.
        '''
        self.Verbose()                

        # First create the draw objects (TLines, TBoxes etc..)
        self.CreateCutBoxes()
        self.CreateCutLines()
        
        # Draw all objects on the PadPlot
        for o in self.DrawObjectList:
            o.Draw("same")
        return


    def _DrawNonHistoObjectsWithPadRatio(self):
        '''
        Draw all drawable objects found in self.DrawObjectList.
        '''
        self.Verbose()                

        # First create the draw objects (TLines, TBoxes etc..)
        self.CreateCutBoxes()
        self.CreateCutLines()
        
        # Draw all objects on the PadPlot
        self.PadPlot.cd()
        for o in self.DrawObjectList:
            o.Draw("same")

        # Update modified canvas and re-draw the PadPlot axes
        self.PadPlot.Modified()
        self.PadPlot.RedrawAxis()
        self.PadPlot.SetGridx(self.THDumbie.gridX)
        self.PadPlot.SetGridy(self.THDumbie.gridY)

        self.PadRatio.Modified()
        self.PadRatio.RedrawAxis()


        # Draw all objects on the PadRatio
        self.PadRatio.cd()
        for o in self.DrawObjectListR:
            if isinstance(o, ROOT.TLegend) == True:
                continue

            if ( ( o.GetY1() != o.GetY2() ) and (o.GetX1() == self.THRatio.xMin ) and ( self.THRatio.xMax == o.GetX2() ) ):
                continue
            elif ( (o.GetX1() == self.THRatio.xMin ) and ( self.THRatio.xMax == o.GetX2() ) ):
                continue               
            elif( o.GetX1() == o.GetX2() ):
                o.SetY1(self.THDumbie.yMinRatio)
                o.SetY2(self.THDumbie.yMaxRatio)
            else:
                #print "o.GetX1() = %s, o.GetX2() = %s, o.GetY1() = %s, o.GetY2() = %s" % ( o.GetX1(), o.GetX2(),o.GetY1(), o.GetY2())
                o.SetY1(self.THDumbie.yMinRatio)
                o.SetY2(self.THDumbie.yMaxRatio)
            o.Draw("same")

        # Update modified canvas and re-draw the PadPlot axes
        self.PadRatio.Modified()
        self.PadRatio.RedrawAxis()
        
        self.PadPlot.cd()
        return

    
    def _CheckHistoBinning(self, histoObject):
        '''
        Ensure that the histoObject has exactly the same binning as the TH1Dubmie.
        '''
        self.Verbose()

        binningIsOk       = False
        binWidthX         = self.THDumbie.binWidthX
        binZeroWidth      = self.THDumbie.TH1orTH2.GetXaxis().GetBinWidth(0)
        tmpBinWidthX      = histoObject.binWidthX
        tmpBinZeroWidth   = histoObject.TH1orTH2.GetXaxis().GetBinWidth(0)
        if (tmpBinWidthX != binWidthX or tmpBinZeroWidth!=binZeroWidth):
            raise Exception("At least one of the histogram in the plotting queue has a different x-axis binning! Please make sure all your histogram bins are identical.")
        return 


    def _CheckHistogramBinning(self):
        '''
        Ensure that all histoObjects have exactly the same binning as the TH1Dubmie.
        '''
        self.Verbose()

        binningIsOk  = False
        binWidthX    = self.THDumbie.binWidthX
        binZeroWidth = self.THDumbie.TH1orTH2.GetXaxis().GetBinWidth(0)
        
        # Check that the x-axis bin is same for all histograms
#        for dataset in self.DatasetToHistoMap.keys():
#            h = self.DatasetToHistoMap[dataset]
#            self._CheckHistoBinning(h)
        for dataset in self.Datasets:
            self._CheckHistoBinning(dataset.histo)
        return 


    def AddPreliminaryText(self, energy, lumi):
        '''
        Add the default CMS text on the canvas. Several defaults are available. 
        For available options see the class TextClass(object) under tools/text.py.
        '''
        self.Verbose()
        
        self.TCanvas.cd()
        self.TextObject.AddEnergyText(energy)
        self.TextObject.AddPreliminary()
        self.TextObject.AddLumiText(lumi)
        self.TCanvas.Update()
        return
    

    def SaveHistos(self, bSave=False, savePath=os.getcwd() + "/", saveFormats=[".png", ".C", ".eps", ".pdf"], saveExtension=""):
        '''
        Save all canvases to specified path and with the desirable format.
        '''
        self.Verbose()
        
        if bSave == False:
            return
            
        # Sanity checks
        if savePath == "" or savePath == None:
            savePath = os.getcwd() + "/"            
        if os.path.exists(savePath) == False: 
            raise Exception("The path '%s' does not exist! Please make sure the provided path is correct." % (savePath) )

        # Define path and save
        saveName = savePath + self.TCanvas.GetName().rsplit('@', 1)[0] + saveExtension
        #creationTime =  self.TCanvas.GetName().rsplit('@', 1)[1]
                                                              

        msg  = "{:<20} {:<20}".format("SaveName" , ": " + saveName)
        msg += "{:<20} {:<20}".format("Format(s)", ": " + ", ".join(saveFormats) )
        self.Print(msg)
        for ext in saveFormats:
            self.TCanvas.Update()
            self.TCanvas.SaveAs( saveName + "." + ext )

        #ROOT.gDirectory.ls()
        return


    def GetCanvasName(self):
        '''
        Return canvas name upon which the plotter objects histograms will be saved on.
        '''
        self.Verbose()
        
        return self.TCanvas.GetName()


    def SetCanvasName(self, canvasName):
        '''
        '''
        self.Verbose()
        
        self.TCanvas.SetName(canvasName)
        return


    def AppendToCanvasName(self, canvasNameExt):
        '''
        '''
        self.Verbose()
        
        self.TCanvas.SetName( self.TCanvas.GetName() + canvasNameExt)
        return


    def GetUnityTH1(self):
        '''
        Returns a TH1 with identical attributes to those of self.TH1Dubmie. But, all its bins
        are filled with 1. So you have a flat distribution histogram at y=1, over the entire x-axis range.
        '''
        self.Verbose()
        hUnity = copy.deepcopy(self.THRatio)
        hUnity.TH1orTH2.Reset()
        hUnity.TH1orTH2.SetName("hUnity")
        hUnity.name = "hUnity"

        nBins = hUnity.TH1orTH2.GetNbinsX()
        for i in range (0, nBins+1):
            #hUnity.TH1orTH2.Fill(i, 1) # error bars are quite large. need to investigate if they are correct.
            # In the meantime, set the bin-error to zero. I think this is the correct way to do it
            hUnity.TH1orTH2.SetBinContent(i, 1)
            hUnity.TH1orTH2.SetBinError(i, 0)
            
        return hUnity.TH1orTH2

        
    def DatasetAsLegend(self, flag):
        '''
        '''
        self.Verbose()
        
        self.DatasetInLegend = flag
        self.EnableColourPalette(not flag)
        return


    def PrintElapsedTime(self, units = "seconds", marker = ""):
        '''
        Print the time elapses since the creation of the plotter object.
        
        '''
        self.Verbose()
        
        deltaT = time.time() - self.startTime
        if units == "seconds":
            pass
        elif units == "minutes":
            deltaT = deltaT/60.0
        elif units == "hours":
            deltaT = deltaT/(60.0*60)
        else:
            raise Exception("Unsupported units of time. Please choose from 'seconds', 'minutes' and 'hours'.")
            
        self.Print("Elapsed time%s: '%s' %s" % (marker, deltaT, units))
        return


    def FindFirstBinBelowValue(self, histo, targetValue, axis=1):
        '''
        FindLastBinAbove(targetValue, axis=1): 
        find last bin with content > threshold for axis (1=x, 2=y, 3=z)
        if no bins with content > threshold is found the function returns -1.
        '''
        self.Verbose()

        iBin = histo.FindLastBinAbove(targetValue, axis)
        if iBin == -1:
            self.Verbose("WARNING! Could not find target value '%s'." % (targetValue))
        binCenter      = histo.GetBinCenter ( iBin   )
        binCenterUp    = histo.GetBinCenter ( iBin+1 )
        binCenterDown  = histo.GetBinCenter ( iBin-1 )
        binContent     = histo.GetBinContent( iBin   )
        binContentUp   = histo.GetBinContent( iBin+1 )
        binContentDown = histo.GetBinContent( iBin-1 )
        binError       = histo.GetBinError( iBin )

        # Sanity check
        if binContent != 0:
            percentageOffset = ((binContent - targetValue)/binContent )*100
        else:
            percentageOffset = 99999.9

        if abs(percentageOffset) > 50:
            self.Verbose( ["Target: '%s'" % (targetValue) , "BinContent: '%s'" % (binContent), "BinContent (+1): '%s'" % (binContentUp), "BinContent (-1): '%s'" % (binContentDown), 
                         "BinCenter: '%s'" % (binCenter), "BinCenter (+1): '%s'" % (binCenterUp), "BinCenter (-1): '%s'" % (binCenterDown), "Rate Offset (%%): '%f'" % (percentageOffset)] )
        return iBin, binCenter, binContent, binError


    def FindFirstBinAboveValue(self, histo, targetValue):
        '''
        '''
        self.Verbose()
        
        iBin = histo.FindFirstBinAbove(targetValue)
        if iBin == -1:
            raise Exception("Could not find target value '%s'!" % (targetValue))

        # Get actual values
        binCenter  = histo.GetBinCenter(  iBin )
        binContent = histo.GetBinContent( iBin)

        # Sanity check
        if binContent != 0:
            percentageOffset = ((binContent - targetValue)/binContent )*100
        else:
            percentageOffset = 99999.9

        if abs(percentageOffset) > 50:
            self.Verbose( ["Target: '%s'" % (targetValue) , "BinContent: '%s'" % (binContent), "BinCenter: '%s'" % (binCenter), "Offset (%%): '%f'" % (percentageOffset)] )
        return iBin, binCenter, binContent


    def _GetLegendHeader(self):
        '''
        Create a TLegend header and return it.
        '''
        self.Verbose()
        legHeader = self.THDumbie.legTitle
        return legHeader


    def GetHistos(self):
        '''
        '''
        self.Verbose()
        return self.HistoObjectList


    def GetTLegend(self):
        '''
        '''
        self.Verbose()
        return self.TLegend



    def SetTLegendHeader(self, text):
        '''
        '''
        self.Verbose()
        
        self.TLegend.SetHeader(text)
        return


    def GetTHStackHistoList(self):
        '''
        '''
        self.Verbose()
        return self.THStackHistoList


    def GetTHStack(self):
        '''
        '''
        self.Verbose()
        return self.THStack


    def GetTHDumbie(self):
        '''
        '''
        self.Verbose()
        return self.THDumbie


    def GetDatasetList(self):
        '''
        '''
        self.Verbose()
        datasetList = []
        for d in self.Datasets:
            datasetList.append(d.name)
        return datasetList
