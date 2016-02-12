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
        self.batchMode         = batchMode
        self.styleObject       = styles.StyleClass(verbose)
        self.textObject        = text.TextClass(verbose)
        self.auxObject         = aux.AuxClass(verbose)
        self.canvasFactor      = 1.25
        #
        self.DatasetInLegend   = False
        self.isTH2             = False
        self.TBoxList          = []
        self.THDumbie          = None
        self.THRatio           = None
        self.THStack           = ROOT.THStack("THStack", "Stack for PadPlot Histograms")
        self.THStackHistoList  = [] #needed because looping over self.THSTack.GetHists() crashes!
        self.THStackRatio      = ROOT.THStack("THStackRatio", "Stack for PadRatio Histograms")
        self.TLegend           = None
        self.TMultigraph       = ROOT.TMultiGraph("TMultigraph", "ROOT.TMultiGraph holding various ROOT.TGraphs")
        #
        self.drawObjectList    = []
        self.drawObjectListR   = []
        self.includeStack      = False
        self.invPadRatio       = False
        self.padRatio          = False
        self.xTLineList        = []
        self.yTLineList        = []
        print
        return

    
    def GetSelfName(self):
        return self.__class__.__name__


    def GetFunctionName(self):
        return sys._getframe(1).f_code.co_name + "()"
    
    
    def Verbose(self, message=""):
        '''
        Custome made verbose system. Will print all messages in the messageList
        only if the verbosity boolean is set to true.
        '''
        if self.verbose:
            print "=== %s:" % ( self.GetSelfName() + "." + self.GetFunctionName() )
            if message!="":
                print "\t", message
        return


    def Print(self, message=""):
        '''
        Custome made print system. Will print the message even if the verbosity boolean is set to false.
        '''
        print "=== %s:" % ( self.GetSelfName() + "." + self.GetFunctionName() )
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


    def PrintWarning(self, msg, keystroke):
        '''                                                                                                                                                          
        Print a warning and make sure user sees it by requiring a keystroke
        '''
        self.Print()
        
        response = raw_input("\t" + msg + ". Press \"%s\" to quit, any other key to proceed: " % (keystroke))
        if response== "q":
            sys.exit()
        else:
            return
        return
    
            
    def _CreateCanvas(self):
        '''
        Create a name for a TCanvas and then create it. 
        This name will later on be used to save the canvas under a user specific format ("png", "pdf", "eps", etc..)
        '''                    
        self.Verbose()

        if hasattr(self, 'TCanvas'):
            return

        canvasName   = self.THDumbie.GetName()
        self.TCanvas = ROOT.TCanvas( canvasName, canvasName, 1)
        self._SetLogAxes()
        self.TCanvas.cd()
        return


    def _Create2PadCanvas(self):
        '''
        Create a 2-pad TCanvas to accomodate a ratio plot and customise it.
        '''                    
        self.Verbose()

        if not hasattr(self, 'TCanvas'):
            raise Exception("The Class Object '%s' already has a 'TCanvas' attribute." % self.GetSelfName())

        # Normal assignment operations (a = b) will simply point the new variable towards the existing object.
        self.THRatio = self.GetDumbieHisto("THRatio")
        
        # Create TCanvas and divide it into two pads: one for plot pad, one for ratio pad
        canvasName   = self.THDumbie.GetAttribute("name")
        self.TCanvas = ROOT.TCanvas( canvasName, canvasName, ROOT.gStyle.GetCanvasDefW(), int(ROOT.gStyle.GetCanvasDefH()*self.canvasFactor))
        self.TCanvas.Divide(1,2)
        
        # Remove x-axis title and labels from the THDumbie to avoid overlap with those THRatio
        self.THDumbie.RemoveBinLabelsX()
        self.THDumbie.RemoveTitleX()

        # Create plot, ratio and cover pads
        self._CreatePads()
        self._SetLogAxes2PadCanvas()
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

    
    def _CreatePadCover(self, xMin=0.08, yMin=0.285, xMax=0.16, yMax=0.32):
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
        self.PadPlot.SetPad(xlow, 1-1/self.canvasFactor, xup, yup)
        self.PadPlot.Draw()
        self.TCanvas.Update()
        return


    def _CreatePadRatio(self):
        '''
        Creates a ratio pad to draw the histogram ratio stack.
        '''
        self.Verbose()
        
        canvasHeightCorr = 0.022

        self.PadRatio = self.TCanvas.cd(2)
        self.PadRatio.SetName("PadRatio")
        (xlow, ylow, xup, yup) = [ROOT.Double(x) for x in [0.0]*4]
        self.PadRatio.GetPadPar(xlow, ylow, xup, yup)
        self.PadRatio.SetPad(xlow, ylow, xup, 1-1/self.canvasFactor + ROOT.gStyle.GetPadBottomMargin() - ROOT.gStyle.GetPadTopMargin() + canvasHeightCorr)
        self.PadRatio.SetFillStyle(4000)
        self.PadRatio.SetTopMargin(0.0)
        self.PadRatio.SetBottomMargin(self.PadRatio.GetBottomMargin()+0.20) #was: 0.16
        self.PadRatio.Draw()
        self.TCanvas.Update()
        return


    def _SetLogXRatio(self):
        self.Verbose()

        if self.THRatio.logXRatio==False:
            return
        if self.THRatio.THisto.GetXaxis().GetXmin() > 0:
            self.PadRatio.SetLogx(True)
        else:
            raise Exception("Request for TCanvas::SetLogx(True) rejected. The minimum x-value is '%s'." % (self.THRatio.xMin))
        return


    def _SetLogYRatio(self):
        self.Verbose()

        if self.THRatio.logYRatio==False:
            return
        if self.THRatio.THisto.GetMinimum()>0:
            self.PadRatio.SetLogy(True)
        else:
            raise Exception("Request for TCanvas::SetLogx(True) rejected. The minimum x-value is '%s'." % (self.THRatio.yMin))
        return
    

    def _SetLogAxes2PadCanvas(self):
        '''
        Apply customisations to a 2-pad TCanvas.
        '''
        self.Verbose()

        # Determine whether to set log for y- and x- axis.
        self._SetLogY()
        self._SetLogX()
        self._SetLogZ()
        self._SetLogXRatio()
        self._SetLogYRatio()
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

    

    def AddDrawObject(self, histos):
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
            self.Print("Adding '1' histogram to the histogram queue: %s" % ("\"" + histos.GetAttribute("name") + "\"") )
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
                self.TLegend.AddEntry( h.THisto, self.GetLegLabel(h), h.legOptions)
                self.TLegend.SetY1( self.TLegend.GetY1() - 0.02)
            else:
                pass
        return


    def _AddHistoToQueue(self, histoObject):
        '''
        '''
        self.Verbose()
        
        if not hasattr(self, 'Datasets'):
            raise Exception("Cannot add histogram to queue as no datasets exist. Check that you have added some datasets")

        # Ensure that the pass argument is a valid histo object
        self.IsDrawObject(histoObject)

        # For-loop: All datasets
        for i, dataset in enumerate(self.Datasets):

            # Ensure that histogram exists in the file
            self.IsHisto(dataset.rootFile, histoObject)

            ### Map histo to dataset  
            self.Datasets[i].histo = copy.deepcopy(histoObject)
            
            # Assign user-defined attributes to histo object
            histoObject = self.Datasets[i].histo
            self._AssignHistoObjectAttributes(dataset.rootFile, dataset, histoObject)

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

        # Assign global values
        self.padRatio      = h.ratio
        self.invPadRatio   = h.invRatio
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


    def IsDrawObject(self, drawObject):
        self.Verbose()
        if isinstance(drawObject, histos.DrawObject):
            return
        else:
            raise Exception("The argument passed is not an instance of histos.DrawObject.")
        return



    def IsHisto(self, rootFile, hObject):
        self.Verbose()

        prefix = hObject.GetAttribute("path") + "/"
        if prefix != "/":
            hPath  = prefix + hObject.GetAttribute("name")
        else:
            hPath = hObject.GetAttribute("name")

        h = rootFile.Get(hPath)
        if isinstance(h, ROOT.TH1) or isinstance(h, ROOT.TH2) or isinstance(h, ROOT.TH3):
            return
        else:
            raise Exception( "The object '%s' in '%s' is neither TH1, nor a TH2, nor a TH3." % (hPath, rootFile.GetName()) )
        return


    def GetDumbieHisto(self, newName):
        '''
        Create a dumbie histogram that will be the first to be drawn on canvas. 
        This should have zero entries but have exactly the same attribues  (binning, axes titles etc..) as the ones to be drawn.
        '''
        self.Verbose()

        # Determine global yMin and yMax
        yMin, yMax = self.GetHistosYMinYMax()

        # Copy first histo in datasets list. Reset its Integral, Contents, Errors and Statistics (not Minimum and Maximum)
        emptyHisto = copy.deepcopy(self.Datasets[0].histo)
        #emptyHisto.SetName(newName)
        emptyHisto.THisto.SetName(newName)
        emptyHisto.THisto.Reset("ICES")    
        emptyHisto.THisto.GetYaxis().SetRangeUser(yMin, yMax)

        # Set Number of divisions
        if isinstance(emptyHisto.THisto, ROOT.TH2):
            emptyHisto.THisto.GetXaxis().SetNdivisions(510) 
        elif isinstance(emptyHisto.THisto, ROOT.TH1):
            emptyHisto.THisto.GetXaxis().SetNdivisions(510) #505
        else:
            raise Exception("Cannot call SetNdivisions for '%s'. Currently ony ROOT.TH1 and ROOT.TH2 supported." % (emptyHisto) )
            
        # Set Line Colour and Width
        emptyHisto.THisto.SetLineColor(ROOT.kBlack)
        emptyHisto.THisto.SetLineWidth(1)

        # Increase right pad margin to accomodate z-axis scale and title
        if isinstance(emptyHisto.THisto, ROOT.TH2) == True:
            ROOT.gStyle.SetPadRightMargin(0.15)
        return emptyHisto
                

    def AppendToDrawObjectList(self, objectToBeDrawn):
        '''
        Append a drawable object of any type (TCanvas, TLegend, TLine, TBox, etc..) to a list.
        This list will be used later on to draw all objects.
        '''
        self.Verbose()

        self.drawObjectList.append(objectToBeDrawn)
        self.drawObjectListR.append(copy.deepcopy(objectToBeDrawn))
        return 
        

    def Draw(self, THStackDrawOpt="nostack", includeStack=False, bAddReferenceHisto=True):
        '''
        Draw all necessary histograms for all datasets.
        '''
        self.Verbose()
        self.includeStack = includeStack
        self._CreateCanvasAndLegendAndDumbie()
        
        if hasattr(self, 'normOption'):
            if self.normOption == "toOne" and THStackDrawOpt=="stack" and len(self.Datasets)>1:
                msg = "WARNING! Drawing '%s' stacked samples with normalisation option '%s'" % (len(self.Datasets), self.normOption)
                self.PrintWarning(msg, "q")

        if THStackDrawOpt=="nostack":
            for dataset in self.Datasets:
                dataset.histo.THisto.SetFillStyle(3003)
                
        self._CheckHistogramBinning()
        self._AddHistogramsToStack()
        self._DrawHistograms(THStackDrawOpt)

        self._DrawRatioHistograms(bAddReferenceHisto)
        self._DrawNonHistoObjects()
        self._CustomiseStack()
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
            self.IsDrawObject(h)
            h.ApplyStyles(self.styleObject)
            h.THisto.Draw(h.drawOptions + ",9same,")
            self.TLegend.AddEntry( h.THisto, h.legLabel, h.GetAttribute("legOptions") )
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
            self.TLegend.AddEntry( histo.THisto, self.GetLegLabel(histo), histo.GetAttribute("legOptions"))
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

        self.THDumbie = self.GetDumbieHisto("THDumbie")

        if self.padRatio or self.invPadRatio:
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
        hDenominator = copy.copy( self.THStackHistoList[0] ) 
        self.Print("Using histogram '%s' as denominator for ratio plots! " % (hDenominator.GetName()))
        
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
                #hRatio.Divide(UnityTH1, hRatio)
                self.Print("Not supported yet")
                sys.exit()

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
        self.THRatio.THisto.GetXaxis().SetTitleOffset(3.2) #was: 2.8
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

        binWidthX    = self.THDumbie.binWidthX
        binZeroWidth = self.THDumbie.THisto.GetXaxis().GetBinWidth(0)    
        for dataset in self.Datasets:
            self._CheckHistoBinning(dataset.histo)
        return 
    
        
    def DatasetAsLegend(self, flag):
        self.Verbose()
        self.DatasetInLegend = flag
        self.EnableColourPalette(not flag)
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
    def EnableColourPalette(self, bEnable=False):
        '''
        Changes colour for each histogram within a given dataset only if 1 dataset is present.
        '''
        self.Verbose()
        self.styleObject.EnableColourPalette(bEnable)
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
        self.PadCover

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
        self.Print("Customising all histograms")
        
        if not hasattr(self, 'histosNormed'):
            raise Exception("Cannot customise histograms. Need to call first NormaliseHistos() and then CustomiseHistos()")

        for d in self.Datasets:
            d.histo.ApplyStyles(self.styleObject)
        return

    
    def NormaliseHistos(self, normOption):
        self.Print("Normalising all histograms '%s'" % (normOption) )
    
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
            dataset.histo.NormaliseToFactor(dataset.GetNormFactor())
        elif normOpt == "toLuminosity":
            dataset.histo.NormaliseToFactor(dataset.GetLuminosity())
        else:
            raise Exception("Unknown histoObject normalisation option '%s'.!" % (dataset.histo.normalise))
        return


    def GetLegLabel(self, hObject):
        '''
        '''
        self.Verbose()
        
        if self.DatasetInLegend:
            return hObject.GetAttribute("dataset").GetLatexName()
        else:
            return hObject.GetAttribute("legLabel")


    def AddDataset(self, dataset):
        '''
        Add a new dataset and associate it to a root file.
        '''
        self.Verbose()

        if not hasattr(self, 'Datasets'):
            self.Datasets = []
        
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


    def DrawCmsText(self, energy, lumi, prelim=True):
        '''
        Add the default CMS text on the canvas. Several defaults are available. 
        For available options see the class TextClass(object) under tools/text.py.
        '''
        self.Print("Drawing 'CMS Preliminary', '%s TeV' and '%s' text" % (energy, lumi) )        
        
        if hasattr(self, 'PadPlot'):
            self.PadPlot.cd()

        if prelim:
            self.textObject.AddDefaultText("preliminary", "")
        else:
            self.textObject.AddDefaultText("publication", "")
        self.textObject.AddDefaultText("lumi", lumi)
        self.textObject.AddDefaultText("energy", "(" + energy + " TeV)")
        self.textObject.DrawTextList()
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



    def GetAttribute(self, attr):
        self.Verbose()
        if hasattr(self, attr):
            return getattr(self, attr)
        else:
            raise Exception("Class object '%s' does not have attribute '%s'" % (self.GetSelfName(), attr))
        return

    
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

    
    def _SetLogAxes(self):
        '''
        Apply axes customisations to a TCanvas.
        '''
        self.Verbose()
        self._SetLogY()
        self._SetLogX()
        self._SetLogZ()
        return


    def _SetLogX(self):
        self.Verbose()

        if self.THDumbie.logX==False:
            return    
        if self.THDumbie.THisto.GetXaxis().GetXmin() > 0:
            self.TCanvas.SetLogx(True)
            if hasattr(self, 'PadPlot'):
                self.PadPlot.SetLogx(True)
        else:
            raise Exception("Request for TCanvas::SetLogx(True) rejected. The minimum x-value is '%s'." % (self.THDumbie.xMin))
        return


    def _SetLogY(self):
        self.Verbose()

        if self.THDumbie.logY==False:
            return
        if self.THDumbie.THisto.GetMinimum() > 0:
            self.TCanvas.SetLogy(True)
            if hasattr(self, 'PadPlot'):
                self.PadPlot.SetLogy(True)
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
    
