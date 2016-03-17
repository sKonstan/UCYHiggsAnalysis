#================================================================================================
# All imported modules
#================================================================================================
import os, sys
import array
import math
import copy
import inspect
from optparse import OptionParser

import ROOT

import UCYHiggsAnalysis.NtupleAnalysis.pyROOT.styles as styles

#================================================================================================
# Class definition
#================================================================================================
class DrawObject:
    def __init__(self, path, name, legLabel, **kwargs):
        self.verbose    = kwargs.get("verbose", False)
        self.path       = path
        self.name       = name
        self.fullPath   = self._GetFullPath()
        self.THisto     = None
        self.legLabel   = self._GetLegendLabel(legLabel)
        self.xUnits     = kwargs.get("xUnits", "")
        self.yUnits     = kwargs.get("yUnits", "")
        self.zUnits     = kwargs.get("zUnits", "")
        self.xLabel     = self._GetLabelX(**kwargs)
        self.yLabel     = self._GetLabelY(**kwargs)
        self.zLabel     = self._GetLabelZ(**kwargs)
        self.xMin       = kwargs.get("xMin", None)
        self.xMax       = kwargs.get("xMax", None)
        self.yMin       = kwargs.get("yMin", None)
        self.yMax       = kwargs.get("yMax", None)
        self.yMinRatio  = kwargs.get("yMinRatio", 0.0)
        self.yMaxRatio  = kwargs.get("yMaxRatio", 2.2)
        self.zMin       = kwargs.get("zMin", None)
        self.zMax       = kwargs.get("zMax", None)
        self.xLegMin    = kwargs.get("xLegMin", 0.70)
        self.xLegMax    = kwargs.get("xLegMax", 0.95)
        self.yLegMin    = kwargs.get("yLegMin", 0.78)
        self.yLegMax    = kwargs.get("yLegMax", 0.93)
        self.xCutLines  = kwargs.get("xCutLines", [])
        self.xCutBoxes  = kwargs.get("xCutBoxes", [])
        self.yCutLines  = kwargs.get("yCutLines", [])
        self.yCutBoxes  = kwargs.get("yCutBoxes", [])
        self.logX       = kwargs.get("logX", False)
        self.logY       = kwargs.get("logY", False)
        self.logZ       = kwargs.get("logZ", False)
        self.logXRatio  = kwargs.get("logXRatio", False)
        self.logYRatio  = kwargs.get("logYRatio", False)
        self.gridX      = kwargs.get("gridX", False)
        self.gridY      = kwargs.get("gridY", False)
        self.gridXRatio = kwargs.get("gridXRatio", False)
        self.gridYRatio = kwargs.get("gridYRatio", False)
        self.binWidthX  = kwargs.get("binWidthX", None)
        self.binWidthY  = kwargs.get("binWidthY", None)
        self.ratioLabel = kwargs.get("ratioLabel", None)
        self.styleType  = kwargs.get("styleType", None)
        self.kwargs     = kwargs
        self.Verbose()
        #self.PrintAttributes()
        return            

    
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
        
        response = raw_input("\t" + msg + ". Press \"%s\" to quit, any other key to proceed: " % (keystroke))
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

        # Alternative way
        # attrs = vars(self)
        # print ', '.join("%s: %s" % item for item in attrs.items())
        return


    def SetAttribute(self, attr, value):
        self.Verbose()
        return setattr(self, attr, value)

    
    def GetAttribute(self, attr):
        self.Verbose()
        if hasattr(self, attr):
            return getattr(self, attr)
        else:
            raise Exception("Class object '%s' does not have attribute '%s'" % (self.GetSelfName(), attr))
        

    def _GetLegendLabel(self, legLabel):    
        self.Verbose()
        if not isinstance(legLabel, str):
            raise Exception("The legend label is not an instance of string, but of type '%s'." % ( type(legLabel) ) )
        else:
            return legLabel

        
    def _GetLabelX(self, **args):
        '''
        '''
        self.Verbose()


        if hasattr(self, 'xUnits') and self.xUnits != "":
            postfix = " [" + self.xUnits + "]"
        else:
            postfix = ""
        return args.get("xLabel", "") + postfix


    def _GetLabelY(self, **args):
        '''
        '''
        self.Verbose()


        if hasattr(self, 'yUnits') and self.yUnits != "":
            postfix = " [" + self.yUnits + "]"
        else:
            postfix = ""
        return args.get("yLabel", "") + postfix


    def _GetLabelZ(self, **args):
        '''
        '''
        self.Verbose()


        if hasattr(self, 'zUnits') and self.zUnits != "":
            postfix = " [" + self.zUnits + "]"
        else:
            postfix = ""
        return args.get("zLabel", "") + postfix


    def ApplyStyles(self):
        '''
        Takes a style object as input to customise the histogram (self). First the rebinning is done
        to the user-defined x-axis bin width. Then the fill/line/marker styles are applied. Then 
        the default axes styles are also configured.
        '''
        self.Verbose()

        self._RebinXToWidth()
        self._RebinYToWidth()
        self._SetFillLineMarkerStyles()
        self._SetAxisStyle()
        return
    

    def _SetAxisStyle(self):
        '''
        Sets the x- and y-axis defaults, like offset, label size, label font and yMax.
        '''
        self.Verbose()

        ### Set histogram axis labels
        self.THisto.SetTitle("")
        self.binWidthX = self.THisto.GetXaxis().GetBinWidth(0)

        if "%" not in self.yLabel:
            self.Print("WARNING! No provision for y-units provided for '%s' in yLabel(='%s'). " % (self.THisto.GetName(), self.yLabel) )

        if isinstance(self.THisto, ROOT.TH1):
            self.THisto.GetXaxis().SetTitle( self.xLabel )
            self.THisto.GetYaxis().SetTitle( self.yLabel % (self.binWidthX) + " " + self.xUnits )
        elif isinstance(self.THisto, ROOT.TH2):
            self.yLabel = self.yLabel# + " " + self.yUnits
            if "%" not in self.xLabel:
                self.Print("WARNING! No provision for x-units provided in xLabel(='%s'). " % (self.xLabel) )
            self.binWidthY = self.THisto.GetYaxis().GetBinWidth(0)
            self.THisto.GetXaxis().SetTitle( self.xLabel % (self.binWidthX) )
            self.THisto.GetYaxis().SetTitle( self.yLabel % (self.binWidthY) )
        elif isinstance(self.THisto, ROOT.TH3):
            raise Exception("Unsupported histogram object '%s'" % (self.THisto))
        else:
            raise Exception("Unknown histogram object '%s'" % (self.THisto))

    
        ### Customise x- and y-axis title font, size, offset
        self.THisto.GetXaxis().SetTitleSize(ROOT.gStyle.GetTitleSize("Z"))
        self.THisto.GetXaxis().SetTitleFont(ROOT.gStyle.GetTitleFont("Z"))
        self.THisto.GetXaxis().SetTitleOffset(1.0)
        
        self.THisto.GetYaxis().SetTitleSize(ROOT.gStyle.GetTitleSize("Z"))
        self.THisto.GetYaxis().SetTitleFont(ROOT.gStyle.GetTitleFont("Z"))
        self.THisto.GetYaxis().SetTitleOffset(1.40)

        ### Customise x- and y-axis label font, size, offset
        self.THisto.GetXaxis().SetLabelSize(ROOT.gStyle.GetLabelSize("Z"))
        self.THisto.GetXaxis().SetLabelFont(ROOT.gStyle.GetLabelFont("Z"))
        self.THisto.GetXaxis().SetLabelOffset(ROOT.gStyle.GetLabelOffset("Z"))
        #
        self.THisto.GetYaxis().SetLabelSize(ROOT.gStyle.GetLabelSize("Z"))
        self.THisto.GetYaxis().SetLabelFont(ROOT.gStyle.GetLabelFont("Z"))
        self.THisto.GetYaxis().SetLabelOffset(ROOT.gStyle.GetLabelOffset("Z"))
        
        ### Customise x- and y-axis label font, size, offset
        self.THisto.GetXaxis().SetLabelSize(ROOT.gStyle.GetLabelSize("Z"))
        self.THisto.GetXaxis().SetLabelFont(ROOT.gStyle.GetLabelFont("Z"))
        self.THisto.GetXaxis().SetLabelOffset(ROOT.gStyle.GetLabelOffset("Z"))
        #
        self.THisto.GetYaxis().SetLabelSize(ROOT.gStyle.GetLabelSize("Z"))
        self.THisto.GetYaxis().SetLabelFont(ROOT.gStyle.GetLabelFont("Z"))
        self.THisto.GetYaxis().SetLabelOffset(ROOT.gStyle.GetLabelOffset("Z"))
        
        xMin = None
        xMax = None
        yMin = None
        yMax = None

        ### Now for the range of the axes
        if (self.xMin != None):
            xMin = self.xMin
        else:
            self.xMin = self.THisto.GetXaxis().GetXmin()
            
        if (self.xMax != None):
            xMax = self.xMax
        else:
            self.xMax = self.THisto.GetXaxis().GetXmax()

        if (self.yMin != None):
            yMin = self.yMin 
        else:
            if isinstance(self.THisto, ROOT.TH1):
                self.yMin = self.THisto.GetMinimum()
            else:
                self.yMin = self.THisto.GetYaxis().GetXmin()
                
        if (self.yMax != None):
            yMax = self.yMax
        else:
            if isinstance(self.THisto, ROOT.TH1):
                self.yMax = self.THisto.GetMaximum()*self.GetYMaxFactor(self.logY)
            else:
                self.yMax = self.THisto.GetYaxis().GetXmax()

        self.THisto.GetYaxis().SetRangeUser(self.yMin, self.yMax)
        self.THisto.GetXaxis().SetRangeUser(self.xMin, self.xMax) #Only works if xMin (xMax) is greater (smaller) at the histogram creation time
        
        ### Take care of z-axis range (only applicable for ROOT.TH2's)
        if isinstance(self.THisto, ROOT.TH2):
            self.THisto.GetZaxis().SetTitle( self.zLabel )
            #self.THisto.GetZaxis().SetTitleSize( self.THisto.GetZaxis().GetTitleSize()*0.8 )
            self.THisto.GetZaxis().SetTitleOffset(1.30)
            if (self.zMax != None):
                zMax = self.zMax
                self.THisto.GetZaxis().SetRangeUser(self.zMin, self.zMax) 
            else:
                pass
        else:
            return


        return


    def GetYMaxFactor(self, bLogY):
        '''
        Returns a factor with which we multiply the y-axis max to extend it.
        '''
        self.Verbose()

        yMaxFactor = None
        if bLogY == False:
            yMaxFactor = 1.4 #1.25
        else:
            yMaxFactor = 100.0 #50.0
        return yMaxFactor


    def GetYMinFactor(self, bLogY):
        '''
        Returns a factor with which we multiply the y-axis min to extend it.
        '''
        self.Verbose()

        return 1.0/self.GetYMaxFactor(bLogY)


    def _SetFillLineMarkerStyles(self):
        '''
        This function customises all the histogram-related styles (fill, marker, line). It uses a style object as input to determine all these according to 
        either the dataset name (if "styleType": None) or the actual user-defined styleType.
        '''
        self.Verbose(["For help see: 'http://root.cern.ch/root/html/TAttMarker.html' and 'http://root.cern.ch/root/html/TAttLine.html'."])

        s = styles.StyleClass(self.verbose)
        
        if isinstance(self.THisto, ROOT.TH1):
            (fillColour, lineColour, markerStyle, markerSize, lineWidth, lineStyle, fillStyle) = s.GetTH1Styles(self)
        elif isinstance(self.THisto, ROOT.TH2):
            (fillColour, lineColour, markerStyle, markerSize, lineWidth, lineStyle, fillStyle) = s.GetTH2Styles(self)
        elif isinstance(self.THisto, ROOT.TH3):
            raise Exception("Usupported histogram object '%s'" % (self.THisto))
        else:
            raise Exception("Unknown histogram object '%s'" % (self.THisto))

        ### Apply colours/styles
        self.THisto.SetFillColor(fillColour)
        self.THisto.SetFillStyle(fillStyle)

        self.THisto.SetLineColor(lineColour)
        self.THisto.SetLineStyle(lineStyle)
        self.THisto.SetLineWidth(lineWidth)
        
        self.THisto.SetMarkerColor(fillColour)
        self.THisto.SetMarkerStyle(markerStyle)
        self.THisto.SetMarkerSize(markerSize)
        return


    def _RebinXToWidth(self):
        '''
        Rebin a histogram x-axis according to the user-defined bin width. 
        '''
        self.Verbose()

        if self.binWidthX==None:
            return

        hName             = self.THisto.GetName()
        originalBinWidthX = self.THisto.GetXaxis().GetBinWidth(0)
        originalNBinsX    = self.THisto.GetNbinsX()

        ### Exact float comparison is tricky in python
        if ( abs(originalBinWidthX - self.binWidthX) < 1e-10): 
            self.Verbose(["Requested binWidthX '%f' is same as original bin-width size ('%f'). Doing nothing." % ( self.binWidthX, originalBinWidthX )])
            return

        self.Verbose(["Rebinning histogram '%s' of original bin size '%s'." % ( hName, originalBinWidthX )])
        ### Calculate the number of bins that correspond to the new bin width. Convert number to an integer
        xMin     = self.THisto.GetXaxis().GetXmin()
        xMax     = self.THisto.GetXaxis().GetXmax()
        nBinsX   = (xMax-xMin)/self.binWidthX
        intBinsX = int(nBinsX+0.5)

        ### Check that the user-requested binning makes sense
        if intBinsX !=0:
            remainderX = self.THisto.GetNbinsX() % intBinsX
        else:
            self.Print("Cannot achieve requested binning. Integer modulo by zero (intBinsX = %s). Skipping this histo." % (intBinsX))
            return
            
        self.Verbose(["remainderX = %s %s %s = %s" % (self.THisto.GetNbinsX(), "%", intBinsX, remainderX)])
        
        if remainderX != 0:
            self.Print("WARNING! Trying to rebin histogram '%s' of x-axis bin-width '%s' to new bin-width of '%s'. The xMin is '%g' and xMax '%g' => number of bins would be '%g', which is not divisor of the number of bins '%d', remainder is '%d'. Will do nothing." % (hName, originalBinWidthX, self.binWidthX, xMin, xMax, nBinsX, originalNBinsX, remainderX))
            return
            
        rebinNBinsToOne = self.THisto.GetNbinsX()/intBinsX

        if isinstance(self.THisto, ROOT.TH1):
            self.THisto.Rebin(rebinNBinsToOne)
        elif isinstance(self.THisto, ROOT.TH2):
            self.THisto.RebinX(rebinNBinsToOne)
        elif isinstance(self.THisto, ROOT.TH3):
            raise Exception("Usupported histogram object '%s'" % (self.THisto))
        else:
            raise Exception("Unknown histogram object '%s'" % (self.THisto))

        ### Send a warning message if the user-defined binWidthX could not be achieved exactly.
        if self.THisto.GetXaxis().GetBinWidth(0) != self.binWidthX:
            self.Print("WARNING! Could not achieve bin-width of '%f' for x-axis of hist '%s'. Actual bin-width is '%f'" % ( self.binWidthX,  self.name, self.THisto.GetXaxis().GetBinWidth(0)))

        return


    def _RebinYToWidth(self):
        '''
        Rebin a histogram y-axis according to the user-defined bin width. 
        '''
        self.Verbose()
        
        if isinstance(self.THisto, ROOT.TH1):
            return
            
        hName             = self.THisto.GetName()
        originalBinWidthY = self.THisto.GetYaxis().GetBinWidth(0)
        originalNBinsY    = self.THisto.GetNbinsY()

        if self.binWidthY==None:
            return
        else:
            self.Verbose(["Rebinning histogram '%s' of original bin size '%s'." % ( hName, originalBinWidthY )])

        ### Calculate the number of bins that correspond to the new bin width. Convert number to an integer
        yMin     = self.THisto.GetYaxis().GetXmin()
        yMax     = self.THisto.GetYaxis().GetXmax()
        nBinsY   = (yMax-yMin)/self.binWidthY
        intBinsY = int(nBinsY+0.5)

        ### Check that the user-requested binning makes sense
        remainderY = self.THisto.GetNbinsY() % intBinsY

        self.Verbose(["remainderX = %s %s %s = %s" % (self.THisto.GetNbinsY(), "%", intBinsY, remainderY)])
        
        if remainderY != 0:
            self.Print("WARNING! Trying to rebin histogram '%s' of y-axis bin-width '%s' to new bin-width of '%s'. The yMin is '%g' and yMax '%g' => number of bins would be '%g', which is not divisor of the number of bins '%d', remainder is '%d'. Will do nothing." % (hName, originalBinWidthY, self.binWidthY, yMin, yMax, nBinsY, originalNBinsY, remainderY))
            return
        else:    
            rebinNBinsToOne = self.THisto.GetNbinsY()/intBinsY
            self.THisto.RebinY(rebinNBinsToOne)
        ### Send a warning message if the user-defined binWidthX could not be achieved exactly.
        if self.THisto.GetYaxis().GetBinWidth(0)!=self.binWidthY:
            self.Print("WARNING! Could not exactly achieve a new bin-width of '%s' for y-axis. The new bin-width will instead be '%s'." % ( self.binWidthY, self.THisto.GetYaxis().GetBinWidth(0) ))

        return


    def NormaliseToOne(self):
        '''
        Normalize TH1/TH2/TH3 to unit area.
        
        \param h   RootHistoWithUncertainties object, or TH1/TH2/TH3 histogram
        
        \return Normalized histogram (same as the argument object, i.e. no copy is made).
        '''
        self.Verbose()
        
        integral = self.GetIntegral()
        if integral == 0:
            return
        else:
            self.NormaliseToFactor(1.0/integral)
            return

    
    def NormaliseToFactor(self, scaleFactor):
        '''
        Scale TH1 with a given factor.
    
        \param h   TH1 histogram
        \param f   Scale factor
    
        TH1.Sumw2() is called before the TH1.Scale() in order to scale the histogram errors correctly.
        '''
        self.Verbose()
        if not isinstance(scaleFactor, float):
            self.Print("WARNING! The scaleFactor variable passed as argument is an instance of float, but '%s' instead" % (type(scaleFactor) ) )
        
        errorIgnoreLevel       = ROOT.gErrorIgnoreLevel
        ROOT.gErrorIgnoreLevel = ROOT.kError

        self.THisto.Sumw2() # errors are also scaled after this call 
        self.THisto.Scale(scaleFactor)

        ROOT.gErrorIgnoreLevel = errorIgnoreLevel
        return

    #================================================================================================
    def SetName(self, name):
        self.Verbose()
        self.name = name
        return


    def GetAttribute(self, attr):
        self.Verbose()
        if hasattr(self, attr):
            return getattr(self, attr)
        else:
            raise Exception("Class object '%s' does not have attribute '%s'" % (self.GetSelfName(), attr))
        return
        

    def GetIntegral(self):
        self.Verbose()

        if isinstance(self.THisto, ROOT.TH1):
            integral = self.THisto.Integral(0, self.THisto.GetNbinsX()+1)
        elif isinstance(self.THisto, ROOT.TH2):
            integral = self.THisto.Integral(0, self.THisto.GetNbinsX()+1, 0, self.THisto.GetNbinsY()+1)
        elif isinstance(self.THisto, ROOT.TH3):
            integral = self.THisto.Integral(0, self.THisto.GetNbinsX()+1, 0, self.THisto.GetNbinsY()+1, 0, self.THisto.GetNbinsZ()+1)
        else:
            raise Exception("Unknown histogram object '%s'" % (self.THisto))
        return integral
    

    def RemoveBinLabelsX(self):
        '''
        Removes all the x-axis labels from the histogram pass as argument.
        '''
        self.Verbose()

        nBinsX = self.THisto.GetNbinsX()
        for i in range(1, nBinsX+1):
            self.THisto.GetXaxis().SetBinLabel(i, "")
        return


    def RemoveTitleX(self):
        '''
        Removes the x-axis title from the histogram passed as argument.
        '''
        self.Verbose()
        self.THisto.GetXaxis().SetTitleSize(0)
        return


    def _GetFullPath(self):
        self.Verbose()

        prefix = self.GetAttribute("path") + "/"
        if prefix == "/":
            return self.GetAttribute("name")
        else:
            return prefix + self.GetAttribute("name")    
        raise Exception("This should never be reached")
        

    def SetName(self, name):
        self.Verbose()
        self.name = name
        return

    
    def GetName(self):
        self.Verbose()
        return self.name

    
        
