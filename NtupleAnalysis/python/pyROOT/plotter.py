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
import UCYHiggsAnalysis.NtupleAnalysis.pyROOT.styles as styles
import UCYHiggsAnalysis.NtupleAnalysis.pyROOT.histos as histos
import UCYHiggsAnalysis.NtupleAnalysis.pyROOT.tdrstyle as tdrstyle


#================================================================================================
# Define class
#================================================================================================
class Plotter(object): 
    def __init__(self, verbose=False, batchMode=True):
        self.verbose           = verbose
        self.DatasetInLegend   = False
        self.Datasets          = []
        self.isTH1             = False
        self.isTH2             = False
        self.PadCover          = None
        self.PadPlot           = None
        self.PadRatio          = None
        #
        self.TBoxList          = []
        self.THDumbie          = None
        self.THRatio           = None
        self.THStack           = ROOT.THStack("THStack", "Stack for PadPlot Histograms")
        self.THStackHistoList  = [] #needed because looping over self.THSTack.GetHists() crashes!
        self.THStackRatio      = ROOT.THStack("THStackRatio", "Stack for PadRatio Histograms")
        self.TLegend           = None
        self.TMultigraph       = ROOT.TMultiGraph("TMultigraph", "ROOT.TMultiGraph holding various ROOT.TGraphs")
        #
        self.auxObject         = aux.AuxClass(verbose)
        self.batchMode         = batchMode
        self.canvasFactor      = 1.25
        self.divisionPoint     = 1-1/self.canvasFactor
        self.drawObjectList    = []
        self.drawObjectListR   = []
        self.includeStack      = False
        self.invPadRatio       = False
        self.padRatio          = False
        self.styleObject       = styles.StyleClass(verbose)
        self.textObject        = text.TextClass(verbose)
        self.xTLineList        = []
        self.yTLineList        = []
        print
        return

    
    def Verbose(self, message=""):
        '''
        Custome made verbose system. Will print all messages in the messageList
        only if the verbosity boolean is set to true.
        '''
        if not self.verbose:
            return
        
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


    def SetVerbose(self, verbose):
        '''
        Manually enable/disable verbosity.
        '''
        self.verbose = verbose
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
        '''
        self.Verbose()
        if hasattr(self, 'rootIsSet'):
            return

        self.Print("Resetting ROOT, setting TDR style, and setting:")

        info   = []
        align  = "{:<15} {:<10}"
        info.append( align.format("OptStat"        , ": " + str( optStat) ) )
        info.append( align.format("MaxDigits"      , ": " + str( maxDigits) ) ) 
        info.append( align.format("NumberContours" , ": " + str( nContours) ) )
        info.append( align.format("gerrIgnoreLevel", ": " + str( errIgnoreLevel) ) )

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
    
        Example: gStyle->SetOptStat(11);
        print only name of histogram and number of entries.
        '''
        self.Verbose()
        self.PadCover

        # Beautifications/Styling
        ROOT.gStyle.SetStatBorderSize(0)
        ROOT.gStyle.SetStatColor(ROOT.kWhite)
        ROOT.gStyle.SetStatStyle(3001)
        ROOT.gStyle.SetStatTextColor(ROOT.kBlack)
        ROOT.gStyle.SetStatFontSize(15)
        
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
    

    def AddDataset(self, dataset):
        '''
        Add a new dataset and associate it to a root file.
        '''
        self.Verbose()
        if self.verbose:
            dataset.PrintProperties()
        self.Datasets.append(dataset)
        return


    def AddDatasets(self, datasetObjects):
        '''
        Add all datasets in the datasetObjects list to the plotter
        '''
        self.Print("Adding '%s' datasets to the plotter object" % (len(datasetObjects) ) )
        
        for d in datasetObjects:
            self.Verbose("Adding dataset %s from file %s." % (d.name, d.rootFile.GetName()))
            self.AddDataset(d)
        return
            

    def _CreateCanvas(self):
        '''
        Create a name for a TCanvas and then create it. 
        This name will later on be used to save the canvas under a user specific format ("png", "pdf", "eps", etc..)
        '''                    
        self.Verbose()

        if hasattr(self, 'TCanvas'):
            return
            
        # Normal assignment operations (a = b) will simply point the new variable towards the existing object.
        histo = self.THDumbie 

        # Create a name for the TCanvas
        canvasName = histo.GetName()

        self.TCanvas = ROOT.TCanvas( canvasName, canvasName, 1)

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
        self.THRatio.THisto.SetName("THRatio")

        # Create TCanvas name that included the dataset name
        canvasName = histo.name

        # Create TCanvas and divide it into two pads: one for plot pad, one for ratio pad
        self.Verbose("Creating canvas with name '%s'" % ( canvasName))
        self.TCanvas = ROOT.TCanvas( canvasName, canvasName, ROOT.gStyle.GetCanvasDefW(), int(ROOT.gStyle.GetCanvasDefH()*self.canvasFactor))
        self.TCanvas.Divide(1,2)

        # Remove x-axis title and labels from the THDumbie to avoid overlap with those THRatio
        self._RemoveXaxisBinLabels(histo.THisto)
        self._RemoveXaxisTitle(histo.THisto)

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
        self.PadPlot.SetPad(xlow, self.divisionPoint, xup, yup)
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
        self.PadRatio.SetPad(xlow, ylow, xup, self.divisionPoint + ROOT.gStyle.GetPadBottomMargin() - ROOT.gStyle.GetPadTopMargin() + CanvasHeightCorr)
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
            histo.xMin = histo.THisto.GetXaxis().GetXmin()

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
            histo.yMin = histo.THisto.GetMinimum()

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

        if histo.logZ==False or isinstance(histo.THisto, ROOT.TH2) == False:
            return

        # Set log-scale for z-axis 
        if histo.zMin == None:
            histo.zMin = histo.THisto.GetZaxis().GetXmin()

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
                histo.yMin = histo.THisto.GetMinimum()
            
            if histo.yMin > 0:
                PadOrCancas.SetLogy(True)
            else:
                raise Exception("Request for TCanvas::SetLogy(True) rejected. The '%s' minimum y-value is '%s'." % (histo.name, histo.yMin))

        # Set log-scale for x-axis 
        if histo.logXRatio==True:
            if histo.xMin == None:
                histo.xMin = histo.THisto.GetXaxis().GetXmin()

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
            self.TLegend = ROOT.TLegend(histo.xLegMin, histo.yLegMin, histo.xLegMax, histo.yLegMax, "", "brNDC")
            self._CustomiseLegend()
            self.drawObjectList.append( self.TLegend )
        return
        

    def _CustomiseLegend(self):
        '''
        Customise a TLegend.
        '''
        self.Verbose()
        
        self.TLegend.SetName(self.GetCanvasName())
        self.TLegend.SetFillStyle(0)
        self.TLegend.SetLineColor(ROOT.kBlack)
        self.TLegend.SetLineWidth(1)
        self.TLegend.SetBorderSize(0)
        self.TLegend.SetShadowColor(ROOT.kWhite)
        self.TLegend.SetTextSize(0.03)
        self.TLegend.SetTextFont(62)
        return

    

    def AddHisto(self, histos):
        '''
        '''
        self.Verbose()
        
        if type(histos) == list:
            self.Print("Adding '%s' histograms to the histogram queue: %s" % (len(histos), "\"" + "\", \"".join(h.GetName() for h in histos) + "\"") )
            for h in histos:
                self._AddHistoToQueue(h)
            #self.Print("FIXME! EXIT")
            #sys.exit()
        else:
            self.Print("Adding '1' histogram to the histogram queue: %s" % ("\"" + histos.GetName() + "\"") )
            self._AddHistoToQueue(histos)

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

        # For-loop: All Datasets
        for dataset in self.Datasets:
            h = dataset.histo
            
            self.Verbose( ["Creating Profile%s for histogram '%s'  and adding to THStack." % ( ProfileAxis.upper(), h.name)] )
            if ProfileAxis == "x":
                hProfileX_Name = h.name +"_ProfileX"
                hProfileX      = h.THisto.ProfileX(hProfileX_Name, firstBin, LastBin)
                self.THStack.Add( hProfileX )
            else:
                self.Print("WARNING! Although this works, some validation would have to be carried out with a simple a well undestood 2D histo")
                hProfileY_Name = h.name +"_ProfileY"
                hProfileY      = h.THisto.ProfileY(hProfileY_Name, firstBin, LastBin)
                self.THStack.Add( hProfileY )
                
            # Add legend entries for THStack?
            if bAddLegendEntries == True:
                self.TLegend.AddEntry( h.THisto, self._GetLegEntryLabel(h), h.legOptions)
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
            self.Print("ERROR! No datasets found. EXIT")
            sys.exit()

        # Ensure that the pass argument is a valid histo object
        self.IsValidHistoObject(histoObject)

        # For-loop: All datasets
        for i, dataset in enumerate(self.Datasets):

            # Ensure that histogram exists in the file
            self.CheckHistoExists(dataset.rootFile, histoObject)

            ### Map histo to dataset  
            self.Datasets[i].histo = copy.deepcopy(histoObject)
            
            # Assign user-defined attributes to histo object
            histoObject = self.Datasets[i].histo
            self._AssignHistoObjectAttributes(dataset.rootFile, dataset, histoObject)

            # Print extensive histogram information
            self.PrintHistoInfo(histoObject, False)

        return

    
    def _AssignHistoObjectAttributes(self, rootFile, dataset, histoObject):
        '''
        '''
        self.Verbose()
        
        # Declare shorter name references
        h = histoObject
        f = rootFile

        # Assign attributes
        h.THisto      = self.GetHistoFromFile(f, h)
        h.dataset       = dataset

        # Determine the histogram integral
        if self.isTH2:
            #self.TDRStyleObject.setWide(True)
            self._CheckNoTH2WithMoreThanOneDatasets(h)
            h.integral  = h.THisto.Integral(0, h.THisto.GetNbinsX()+1, 0, h.THisto.GetNbinsY()+1)
        else:
            h.integral  = h.THisto.Integral(0, h.THisto.GetNbinsX()+1)
            
        # Assign global values
        self.padRatio      = h.ratio
        self.invPadRatio   = h.invRatio
            
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

        msg  = "{:<15} {:<20}".format("Dataset"            , ": " + histo.dataset.name)
        msg += "\n\t{:<15} {:<20}".format("HistoPath"      , ": " + histo.path)
        msg += "\n\t{:<15} {:<20}".format("HistoName"      , ": " + histo.name)
        msg += "\n\t{:<15} {:<20}".format("Integral()"     , ": " + str(histo.GetIntegral()))
        msg += "\n\t{:<15} {:<20}".format("normalise"      , ": " + histo.normalise)

        if histo.THisto.Integral() == 0 or verbose:
            self.Print(msg)
            
        self.Verbose(msg)
        return


    def ConvertToOneMinusCumulativeHistos(self):
        '''
        This method converts all histograms into a (1-cumulative integral) histograms.
        '''
        self.Verbose()
        
        # For-loop: All datasets
        for dataset in self.Datasets:
            self._ConvertToOneMinusCumulativeHisto(dataset.histo)
        return

    
    def DrawEfficiency(self, cutDirection=">", errType="binomial"):
        '''
        '''
        self.Verbose()
        
        self._CustomiseHistograms()

        # Change some histoObject attributes
        self.Print("FIXME")
        histo     =  self.GetHistos()[0]
        saveName  = histo.saveName
        kwargs    = histo.kwargs
        binWidthX = histo.binWidthX
        if histo.binWidthX == None:
            binWidthX = histo.THisto.GetBinWidth(0)
        
        kwargs["yUnits"]      = ""
        kwargs["logX"]        = False
        kwargs["logY"]        = False
        kwargs["yMin"]        = 0.0
        kwargs["yMax"]        = 1.15
        kwargs["normalise"]   = ""
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
        
        # For-loop: All Datasets
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
        nBinsX  = histo.THisto.GetNbinsX()+1
        for b in range(0, nBinsX+1):

            binWidth   = histo.THisto.GetBinWidth(b)
            binCenter  = histo.THisto.GetBinCenter(b)
            binLowEdge = histo.THisto.GetBinLowEdge(b)
            binUpEdge  = binCenter + binWidth/2

            nPass      = histo.THisto.Integral(b+1, nBinsX) #events that pass the up-edge of the bin
            nTotal     = histo.THisto.Integral( 0, nBinsX )
            eff        = -1.0

            # Calculate the efficiency and its error
            eff, err = self.auxObject.Efficiency(nPass, nTotal, errType)
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
        histo.THisto.SetMaximum(1.0)
        self.AddTGraphErrors(histo, xVals, xUp, xLow, effVals, effUp, effLow, None, None, None, False, **kwargs)
        return


    def _CheckNoTH2WithMoreThanOneDatasets(self, histoObject):
        ''''
        Ensure that no TH2 is drawn where more than 1 dataset is created. Very difficult to distinguish so we need to take care.
        '''
        self.Verbose()
        
        hType = type(histoObject.THisto)
        
        if len(self.Datasets)>1 and "TH2" in str(hType):
            raise Exception("Cannot draw a TH2 while more than 1 datasets are present.")
        else:
            return


    def IsValidHistoObject(self, histoObject):
        ''''
        Ensure that the histoObject is of valid type (histos.TH1 or histos.TH2). Raise an exception otherwise.
        '''
        self.Verbose()

        if isinstance(histoObject, histos.DrawObject):
            return
        else:
            self.Print("ERROR!", "Unknown histo type. Please make sure the histo object '%s' (type = '%s') is either a TH1 or a TH2" % (histoObject, type(histoObject)), "EXIT")
            sys.exit()            


    def CheckHistoExists(self, rootFile, hObject):
        '''
        Ensure that the histogram you are trying to get from a TFile really exists.
        '''
        self.Verbose()
        
        hPath = ""
        if (hObject.path == "") or (hObject.path == None):
            hPath = hObject.name
        else:
            hPath = hObject.path + "/" + hObject.name

        self.isTH1 = isinstance( rootFile.Get(hPath), ROOT.TH1F) or isinstance( rootFile.Get(hPath), ROOT.TH1D)
        self.isTH2 = isinstance( rootFile.Get(hPath), ROOT.TH2F) or isinstance( rootFile.Get(hPath), ROOT.TH2D)
        if  not self.isTH1 and not self.isTH2:
            raise Exception( "Could not find histo object '%s' in TFile '%s' under folder '%s'." % (hObject.name, rootFile.GetName(), hObject.path) )

        return


    def CreateDumbie(self, THDumbie=None):
        '''
        Create a dumbie histogram that will be the first to be drawn on each canvas. 
        This should have zero entries but have exactly the same attribues  (binning, axes titles etc..) as the ones to be drawn.
        '''
        self.Verbose()

        myMax = -1E10
        myMin = +1E10
        # For-loop: All datasets
        for dataset in self.Datasets:
            h      = dataset.histo
            tmpMax =  h.THisto.GetMaximum()
            if tmpMax > myMax:
                myMax = h.yMax
                myMin = h.yMin
                self.THDumbie = copy.deepcopy(h)
                self.THDumbie.THisto.SetName("THDumbie")
            else:
                continue

        # Reset only Integral, Contents, Errors and Statistics (not Minimum and Maximum)
        self.THDumbie.THisto.Reset("ICES")

        # Set custom range for x- and y- axis and pad margins            
        self.THDumbie.THisto.GetYaxis().SetRangeUser(myMin, myMax)
        self.THDumbie.THisto.GetXaxis().SetRangeUser(h.xMin, h.xMax) #does nothing if xMax > max x-value when histogram was created

        # Set Number of divisions! 
        if (self.isTH2):
            self.THDumbie.THisto.GetXaxis().SetNdivisions(510) 
        else:
            #self.THDumbie.THisto.GetXaxis().SetNdivisions(510) #default
            self.THDumbie.THisto.GetXaxis().SetNdivisions(505)

        # Set Line Colour and Width
        self.THDumbie.THisto.SetLineColor(ROOT.kBlack)
        self.THDumbie.THisto.SetLineWidth(1)

        # Increase right pad margin to accomodate z-axis scale and title
        if isinstance(self.THDumbie.THisto, ROOT.TH2) == True:
            ROOT.gStyle.SetPadRightMargin(0.15)
            #ROOT.gStyle.SetPadRightMargin(0.15)
        return
                

    def AppendToDrawObjectList(self, objectToBeDrawn):
        '''
        Append a drawable object of any type (TCanvas, TLegend, TLine, TBox, etc..) to a list.
        This list will be used later on to draw all objects.
        '''
        self.Verbose()

        self.drawObjectList.append(objectToBeDrawn)
        self.drawObjectListR.append(copy.deepcopy(objectToBeDrawn))
        return 

        
    def EnableColourPalette(self, bEnable=False):
        '''
        Changes colour for each histogram within a given dataset only if 1 dataset is present.
        '''
        self.Verbose()
        
        self.styleObject.EnableColourPalette(bEnable)
        return


    def _CustomiseHistograms(self):
        '''
        Customise all histograms
        '''
        self.Verbose()
        
        # For-loop: All datasets
        for d in self.Datasets:
            d.histo.ApplyStyles(self.styleObject)
        return

    
    def _NormaliseHistograms(self):
        '''
        Normalise all histograms
        '''
        self.Verbose()
        
        for dataset in self.Datasets:
            self._NormaliseHisto(dataset)
        return


    def _NormaliseHisto(self, dataset):
        '''
        Normalise the histoObject passed to this function according to user-specified criteria. 
        '''
        self.Verbose()

        options = ["", "toOne", "byXSection", "toLuminosity"]
        norm    = dataset.histo.normalise
    
        if norm not in options:
            raise Exception("Unsupported normalisation option '%s'. Please choose one of the following options:\n\t \"%s\"" % (norm, "\", \"".join(opt for opt in options) ) )

        if norm == "":
            self.PrintHistoInfo(dataset.histo, True)
            return
        elif norm == "toOne":
            dataset.histo.NormaliseToOne()
            return
        elif norm == "byXSection":
            dataset.histo.NormaliseToFactor(dataset.GetNormFactor())
        elif norm == "toLuminosity":
            dataset.histo.NormaliseToFactor(dataset.GetLuminosity())
        else:
            raise Exception("Unknown histoObject normalisation option '%s'.!" % (dataset.histo.normalise))

        self.PrintHistoInfo(dataset.histo, False)
        return


    def Draw(self, THStackDrawOpt="nostack", includeStack=False, bAddReferenceHisto=True):
        '''
        Draw all necessary histograms for all datasets.
        '''
        self.Verbose()

        self.includeStack = includeStack
        self._NormaliseHistograms()
        self._CustomiseHistograms()
        self._CreateCanvasAndLegendAndDumbie()

        if self.THDumbie.normalise == "toOne" and THStackDrawOpt=="stack" and len(self.Datasets)>1:
            self.Print("WARNING! Drawing '%s' stacked samples with normalisation option '%s'" % (len(self.Datasets), self.THDumbie.normalise) )

        if THStackDrawOpt=="nostack":
            for dataset in self.Datasets:
                dataset.histo.THisto.SetFillStyle(3003)
                
        self._CheckHistogramBinning()
        self._AddHistogramsToStack()
        self._DrawHistograms(THStackDrawOpt)
        self._DrawRatioHistograms(bAddReferenceHisto)
        self._DrawNonHistoObjects()
        self._CustomiseStack()
        #self.THStack.Draw("same")             #new: needed when drawing cut-boxes
        #self.TLegend.Draw("same")             #new: needed when drawing cut-boxes
        self.THDumbie.THisto.Draw("same")
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
        '''
        self.Verbose()

        
        for h in HistoObjectList:
            self.IsValidHistoObject(h)
            h.ApplyStyles(self.styleObject)
            h.THisto.Draw(h.drawOptions + ",9same,")
            self.TLegend.AddEntry( h.THisto, h.legTitle, self._GetLegEntryOptions(h) )
            self.TLegend.SetY1( self.TLegend.GetY1() - 0.02)

        self.TLegend.SetHeader(TLegendHeader)
        self.THDumbie.THisto.Draw("same")
        return


    def Draw2DProfile(self, THStackDrawOpt="nostack", includeStack=False, ProfileAxis=None, firstBin=1, lastBin=-1):
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
            raise Exception("Invalid ProfileAxis option selected ('%s'). You need to speficy the axis of the Profile (x or y)" % (ProfileAxis) )

        self.includeStack = includestack
        self.EnableColourPalette(True)
        self._NormaliseHistograms()
        self._CustomiseHistograms()
        self._CreateCanvasAndLegendAndDumbie()
        self._CheckHistogramBinning()
        self._AddHistogramsToStack2D(ProfileAxis, firstBin, lastBin)
        self._DrawHistograms(THStackDrawOpt)
        self._DrawRatioHistograms()
        self._DrawNonHistoObjects()
        self._CustomiseStack()
        self.THDumbie.THisto.Draw("same")
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

        # For-loop: All histos
        for histo in self.GetHistos():
            
            self.THStack.Add(histo.THisto)
            self.THStackHistoList.append(histo.THisto) #xenios
            self.TLegend.AddEntry( histo.THisto, self._GetLegEntryLabel(histo), self._GetLegEntryOptions(histo) ) #xenios
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
        if self.padRatio == True or self.invPadRatio == True:
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

        # Extend the DrawObjectList with the TLineList
        self.drawObjectList.extend(self.xTLineList)
        self.drawObjectList.extend(self.yTLineList)

        self.drawObjectListR.extend( copy.deepcopy(self.xTLineList) )
        if (self.THDumbie.yCutLinesRatioPad == True):
            self.drawObjectListR.extend( copy.deepcopy(self.yTLineList) )
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
            self._CustomiseTLine(line, lineColour=ROOT.kBlack, lineWidth=3, lineStyle=ROOT.kDashed) #ROOT.kDashDotted
            self.TLegend.SetY1( self.TLegend.GetY1() - 0.02)
            self.AppendToTLineList( line, axis)

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
        self.drawObjectList.extend(self.xTLineList)
        self.drawObjectList.extend(self.yTLineList)
        self.drawObjectList.extend(self.TBoxList)

        self.drawObjectListR.extend(copy.deepcopy(self.xTLineList))
        if (self.THDumbie.yCutLinesRatioPad == True):
            self.drawObjectListR.extend(copy.deepcopy(self.yTLineList))
            self.drawObjectListR.extend(copy.deepcopy(self.TBoxList))
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

        self.THDumbie.THisto.Draw(self.THDumbie.drawOptions)
        self.DrawStackInclusive()
        self.THStack.Draw(THStackDrawOpt + "," + self.THDumbie.drawOptions + "," +  "9same") #"PADS"
        ROOT.gPad.RedrawAxis() #the histo fill area may hide the axis tick marks. Force a redraw of the axis over all the histograms.
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

        if self.padRatio == False and self.invPadRatio == False:
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
            hRatio.Divide(hNumerator, hDenominator, 1.0, 1.0, "B") #"B" = Binomial

            # Inverts ratio histogram if requested (i.e. each bin has content 1/bin)
            if self.invPadRatio == True:
                hRatio.Divide(UnityTH1, hRatio) 

            # Finally, add this ratio histogram to the THStackRatio
            self.THStackRatio.Add(hRatio)

        # Customise axes and titles
        self.CustomiseTHRatio()

        # Draw the Ratio Stack with "nostack" option
        self.THRatio.THisto.Draw()
        self.THStackRatio.Draw("nostack9sameAP")
        
        # Switch back to the PadPlot (necessary)
        self.PadPlot.cd()
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
        self.THRatio.THisto.GetXaxis().SetTitleOffset(2.8)
        if self.THRatio.ratioLabel == None:
            if self.invPadRatio == False:
                self.THRatio.ratioLabel = "Ratio"
            else:
                self.THRatio.ratioLabel = "1/Ratio"
        self.THRatio.THisto.GetYaxis().SetTitle(self.THRatio.ratioLabel)

        # Customise the y-axis
        self.THRatio.yMax = self.THRatio.yMinRatio
        self.THRatio.yMin = self.THRatio.yMaxRatio
        self.THRatio.THisto.GetYaxis().SetNdivisions(505)
        self.THRatio.THisto.GetYaxis().SetRangeUser(self.THRatio.yMinRatio, self.THRatio.yMaxRatio)
        self.THRatio.THisto.GetYaxis().SetTitleOffset(1.8) 
        self.THDumbie.THisto.GetYaxis().SetTitleOffset(1.8)
        
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
        if self.includeStack==False:
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
            h.THisto.GetYaxis().SetRangeUser(h.yMin, h.yMax)        
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

        if self.DatasetInLegend: #xenios
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
        #if self.padRatio == False and  self.invPadRatio == False:
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
        Draw all drawable objects found in self.drawObjectList.
        '''
        self.Verbose()                

        if (self.padRatio == True or self.invPadRatio == True):
            self._DrawNonHistoObjectsWithPadRatio()
        else:
            self._DrawNonHistoObjectsNoPadRatio()        
        return


    def _DrawNonHistoObjectsNoPadRatio(self):
        '''
        Draw all drawable objects found in self.drawObjectList.
        '''
        self.Verbose()                

        # First create the draw objects (TLines, TBoxes etc..)
        self.CreateCutBoxes()
        self.CreateCutLines()
        
        # Draw all objects on the PadPlot
        for o in self.drawObjectList:
            o.Draw("same")
        return


    def _DrawNonHistoObjectsWithPadRatio(self):
        '''
        Draw all drawable objects found in self.drawObjectList.
        '''
        self.Verbose()                

        # First create the draw objects (TLines, TBoxes etc..)
        self.CreateCutBoxes()
        self.CreateCutLines()
        
        # Draw all objects on the PadPlot
        self.PadPlot.cd()
        for o in self.drawObjectList:
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
        for o in self.drawObjectListR:
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
        binZeroWidth      = self.THDumbie.THisto.GetXaxis().GetBinWidth(0)
        tmpBinWidthX      = histoObject.binWidthX
        tmpBinZeroWidth   = histoObject.THisto.GetXaxis().GetBinWidth(0)
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
        binZeroWidth = self.THDumbie.THisto.GetXaxis().GetBinWidth(0)
        
        # For-loop: All datasets
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
        self.textObject.AddEnergyText(energy)
        self.textObject.AddPreliminary()
        self.textObject.AddLumiText(lumi)
        self.TCanvas.Update()
        return
        
    
    def _IsValidSavePath(self, savePath):
        '''
        Make sure that the full path below which files will be saved exists and has the correct format
        '''
        if not isinstance(savePath, str):
            raise Exception("The save path '%s' is not valid! Please make sure the path provided is a string." % (savePath) )
        
        if savePath!="":
            if not savePath.endswith("/"):
                savePath += "/" 
            if not os.path.exists(savePath):
                raise Exception("The path '%s' does not exist! Please make sure the provided path is correct." % (savePath) )
        return
                   

    def GetUnityTH1(self):
        '''
        Returns a TH1 with identical attributes to those of self.TH1Dubmie. But, all its bins
        are filled with 1. So you have a flat distribution histogram at y=1, over the entire x-axis range.
        '''
        self.Verbose()
        hUnity = copy.deepcopy(self.THRatio)
        hUnity.THisto.Reset()
        hUnity.THisto.SetName("hUnity")
        hUnity.name = "hUnity"

        nBins = hUnity.THisto.GetNbinsX()
        for i in range (0, nBins+1):
            #hUnity.THisto.Fill(i, 1) # error bars are quite large. need to investigate if they are correct.
            # In the meantime, set the bin-error to zero. I think this is the correct way to do it
            hUnity.THisto.SetBinContent(i, 1)
            hUnity.THisto.SetBinError(i, 0)
            
        return hUnity.THisto

        
    def DatasetAsLegend(self, flag):
        '''
        '''
        self.Verbose()
        
        self.DatasetInLegend = flag
        self.EnableColourPalette(not flag)
        return


    def PrintElapsedTime(self, units = "seconds"):
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
            
        self.Print("Elapsed time: '%s' %s" % (deltaT, units))
        return


    def GetTHStackHistoList(self):
        self.Verbose()
        return self.THStackHistoList


    def GetTHStack(self):
        self.Verbose()
        return self.THStack


    def GetTHDumbie(self):
        self.Verbose()
        return self.THDumbie


    #================================================================================================
    def GetDatasets(self):
        self.Verbose()
        return self.Datasets


    def GetLegend(self):
        self.Verbose()
        return self.TLegend


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
    

    def SetCanvasName(self, name):
        self.Verbose()
        self.TCanvas.SetName(name)
        return


    def GetCanvasName(self):
        self.Verbose()
        return self.TCanvas.GetName()

    
    def _SaveAs(self, saveName, saveFormats):
        '''
        Loop over all formats and save the canvas to 
        '''
        self.Verbose()

        self.SetCanvasName(saveName)
        self.TCanvas.Update()

        for ext in saveFormats:
            name = self.GetCanvasName() + "." + ext
            self.TCanvas.SaveAs(name)
            print "\t%s" % name
        return

    
    def SaveAs(self, savePath=os.getcwd() + "/", saveName="", savePostfix="", saveFormats=["png", "C", "eps", "pdf"]):
        '''
        Save canvas to a specified path and with the desirable format.
        '''
        self.Print()
            
        self._IsValidSavePath(savePath)
        self._SaveAs(saveName, saveFormats)
        return


    def Save(self, savePath=os.getcwd() + "/", saveFormats=["png", "eps", "pdf"]):
        '''
        Save canvas with the default canvas (histogram) name to the current working directory
        '''
        self.Print()

        self._IsValidSavePath(savePath)
        saveName = savePath + self.GetCanvasName()
        self._SaveAs(saveName, saveFormats)
        return
