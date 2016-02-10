#================================================================================================
# All imported modules
#================================================================================================
import os, sys
import array
import math
import copy
import inspect
import glob
from optparse import OptionParser
from itertools import cycle

import UCYHiggsAnalysis.NtupleAnalysis.pyROOT.text as text
import ROOT

#================================================================================================
# Class Definition 
#================================================================================================
class StyleClass(object):
    def __init__(self, verbose = False):
        self.verbose                = verbose
        self.bEnableColourPalette   = False
        self.TextObject             = text.TextClass(verbose=self.verbose)
        self.styleTypeList          = []
        self.styleTypeSpecialList   = []
        self.colourPaletteList      = [ROOT.kBlack, ROOT.kRed-4, ROOT.kAzure+6, ROOT.kSpring+2, ROOT.kMagenta-2, ROOT.kGray, ROOT.kOrange+5, ROOT.kYellow-4, ROOT.kBlue-4,
                                       ROOT.kGreen-2, ROOT.kViolet-5, ROOT.kPink-8, ROOT.kTeal-1, ROOT.kCyan-7]
        self.markerStyleCounterList = [ROOT.kFullCircle, ROOT.kOpenCircle, ROOT.kOpenSquare, ROOT.kOpenTriangleUp, ROOT.kOpenTriangleDown, ROOT.kOpenCross, ROOT.kFullSquare,
                                       ROOT.kFullTriangleUp, ROOT.kFullTriangleDown, ROOT.kFullCross, ROOT.kFullDiamond, ROOT.kOpenDiamond, ROOT.kFullStar, ROOT.kOpenStar]
        self.fillStyleCounterList   = [3001, 3002, 3003, 3004, 3005, 3006, 3007, 3144, 3244, 3444]
        self.lineStyleCounterList   = [i for i in range(+1, +10, +1)]
        self.colourShadeList        = [i for i in range(-9, +4, +3)]
        self.colourPalette          = {}
        self.markerStyleCounter     = {}
        self.fillStyleCounter       = {}
        self.lineStyleCounter       = {}
        self.colourShade            = {}
        self.MsgCounter             = 0
        self._SetDefaults("ttHJetToNonbb_M125" , colour=ROOT.kRed+1    , mStyle=ROOT.kOpenCircle      , lWidth=2, lStyle=ROOT.kDashed, fStyle=1001, drawOpts="HIST", legOpts="F")
        self._SetDefaults("TTJets"             , colour=ROOT.kMagenta+2, mStyle=ROOT.kFullCircle      , lWidth=2, lStyle=ROOT.kSolid , fStyle=1001, drawOpts="HIST", legOpts="F")
        self._SetDefaults("DYJetsToLL_M_10to50", colour=ROOT.kYellow-7 , mStyle=ROOT.kFullTriangleUp  , lWidth=2, lStyle=ROOT.kSolid , fStyle=1001, drawOpts="HIST", legOpts="F")
        self._SetDefaults("WJetsToLNu"         , colour=ROOT.kBlue+1   , mStyle=ROOT.kFullTriangleDown, lWidth=2, lStyle=ROOT.kSolid , fStyle=1001, drawOpts="HIST", legOpts="F")
        self._SetDefaults("WW"                 , colour=ROOT.kGreen    , mStyle=ROOT.kOpenTriangleUp  , lWidth=2, lStyle=ROOT.kSolid , fStyle=1001, drawOpts="HIST", legOpts="F")
        self._SetDefaults("WZ"                 , colour=ROOT.kGreen+2  , mStyle=ROOT.kOpenTriangleUp  , lWidth=2, lStyle=ROOT.kSolid , fStyle=1001, drawOpts="HIST", legOpts="F")
        self._SetDefaults("ZZ"                 , colour=ROOT.kGreen-2  , mStyle=ROOT.kOpenTriangleUp  , lWidth=2, lStyle=ROOT.kSolid , fStyle=1001, drawOpts="HIST", legOpts="F")
        self._SetDefaults("Data"               , colour=ROOT.kBlack    , mStyle=ROOT.kOpenCircle, lWidth=2, lStyle=ROOT.kDashed, fStyle=1001, drawOpts="HIST", legOpts="F")
        self._SetSpecials("random", colour = cycle(self.colourPaletteList).next(), mStyle=ROOT.kFullCircle, lWidth=3, lStyle=0, fStyle=3001, drawOpts="HIST", legOpts="F")
        self.Verbose()
        return

    
    def Verbose(self, messageList=None):
        '''
        Custome made verbose system. Will print all messages in the messageList
        only if the verbosity boolean is set to true.
        '''
        if self.verbose:
            print "*** %s:" % (self.__class__.__name__ + "." + sys._getframe(1).f_code.co_name + "()")
            if messageList==None:
                return
            else:
                for message in messageList:
                    print "\t", message
        return


    def Print(self, message=""):
        '''
        Custome made print system. Will print the message even if the verbosity boolean is set to false.
        '''
        print "*** %s:" % (self.__class__.__name__ + "." + sys._getframe(1).f_code.co_name + "()")
        if message!="":
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


    def _SetDefaults(self, name, **kwargs):
        '''
        Call this function to initialise some default self values when an object is first created.
        Append the style name to a list so that the object is aware of all available pre-defined defaults.
        '''
        self.Verbose()
        
        # Remove dependence on upper-case characters
        name = name.lower()
        self.colourPalette[name]      = cycle(self.colourPaletteList)
        self.colourShade[name]        = cycle(self.colourShadeList)
        self.lineStyleCounter[name]   = cycle(self.lineStyleCounterList)
        self.fillStyleCounter[name]   = cycle(self.fillStyleCounterList)
        self.markerStyleCounter[name] = cycle(self.markerStyleCounterList)

        ### Set all arguments and their values
        for argument, value in kwargs.iteritems():
            setattr(self, name + "_" + argument, value)
            #self.drawOptions  = kwargs.get("drawOptions", None)
            #print "'%s': '%s' =  '%s'" % (name, argument , value)
        self.styleTypeList.append( name.lower() )
        return


    def _SetSpecials(self, name, **kwargs):
        '''
        Call this function to initialise some special self values when an object is first created.
        Append the style name to a list so that the object is aware of all available pre-defined defaults.
        '''
        self.Verbose()

        self.colourPalette[name]      = cycle(self.colourPaletteList)
        self.colourShade[name]        = cycle(self.colourShadeList)
        self.lineStyleCounter[name]   = cycle(self.lineStyleCounterList)
        self.fillStyleCounter[name]   = cycle(self.fillStyleCounterList)
        self.markerStyleCounter[name] = cycle(self.markerStyleCounterList)

        ### Set all arguments and their values
        for argument, value in kwargs.iteritems():
            setattr(self, name + "_" + argument, value)
            #print "'%s': '%s' =  '%s'" % (name, argument , value)

        self.styleTypeSpecialList.append(name)
        return


    def EnableColourPalette(self, bEnable):
        '''
        This boolean controls whether the fillColour is the same for each dataset (just a shade change)
        or if it is different (full colour change).
        '''
        self.Verbose()
        self.bEnableColourPalette=bEnable
        return


    def _GetTH1Values(self, styleType):
        '''
        '''
        self.Verbose()
        
        if self.bEnableColourPalette==True:
            fillColour  = self.colourPalette[styleType].next()
            markerStyle = self.markerStyleCounter[styleType].next()
        else:
            fillColour  = getattr(self, styleType + "_colour" ) # + self.colourShade[styleType].next()
            markerStyle = getattr(self, styleType + "_mStyle"  )

        self.Verbose(["StyleType '%s', FillColour = '%s'" % (styleType, fillColour)])        
        markerSize  = 1.0
        lineColour  = fillColour
        lineWidth   = getattr(self, styleType + "_lWidth"   )
        lineStyle   = getattr(self, styleType + "_lStyle"   )
        fillStyle   = getattr(self, styleType + "_fStyle"   )
        drawOptions = getattr(self, styleType + "_drawOpts" )
        legOptions  = getattr(self, styleType + "_legOpts"  )
        return (fillColour, lineColour, markerStyle, markerSize, lineWidth, lineStyle, fillStyle, drawOptions, legOptions)


    def _GetTGraphValues(self, styleType):
        self.Verbose()
        
        if self.bEnableColourPalette==True:
            fillColour  = self.colourPalette[styleType].next()
            markerStyle = self.markerStyleCounter[styleType].next()
        else:
            fillColour  = getattr(self, styleType + "_colour" ) # + self.colourShade[styleType].next()
            markerStyle = getattr(self, styleType + "_mStyle"  )

        self.Verbose(["StyleType '%s', FillColour = '%s'" % (styleType, fillColour)])
        markerSize  = 1.0
        lineColour  = fillColour
        lineWidth   = getattr(self, styleType + "_lineWidth" )
        lineStyle   = getattr(self, styleType + "_lineStyle" )
        fillStyle   = 3002 #self.fillStyleCounter[styleType].next()
        drawOptions = getattr(self, styleType + "_drawOptions" )
        legOptions  = getattr(self, styleType + "_legOptions" )
        return (fillColour, lineColour, markerStyle, markerSize, lineWidth, lineStyle, fillStyle, drawOptions, legOptions)


    def _GetTH1SpecialValues(self, styleType):
        '''
        '''
        self.Verbose()
        
        if self.bEnableColourPalette==True:
            fillColour  = self.colourPalette[styleType].next()
        else:
            fillColour  = getattr(self, styleType + "_colour" ) + self.colourShade[styleType].next()

        markerStyle = self.markerStyleCounter[styleType].next()
        markerSize  = 1.0
        lineColour  = fillColour
        lineWidth   = getattr(self, styleType + "_lineWidth" )
        lineStyle   = getattr(self, styleType + "_lineStyle" )
        fillStyle   = getattr(self, styleType + "_fillStyle" )
        drawOptions = getattr(self, styleType + "_drawOptions" )
        legOptions  = getattr(self, styleType + "_legOptions" )
        return (fillColour, lineColour, markerStyle, markerSize, lineWidth, lineStyle, fillStyle, drawOptions, legOptions)


    def _GetTH2Values(self, styleType):
        '''
        '''
        self.Verbose()
        
        if self.bEnableColourPalette==True:
            fillColour  = self.colourPalette[styleType].next()
        else:
            fillColour  = getattr(self, styleType + "_colour" ) + self.colourShade[styleType].next()

        markerStyle = self.markerStyleCounter[styleType].next()
        markerSize  = 1.0

        lineColour  = fillColour
        lineWidth   = getattr(self, styleType + "_lineWidth" )
        lineStyle   = getattr(self, styleType + "_lineStyle" ) # + self.lineStyleCounter[styleType].next()

        fillStyle   = getattr(self, styleType + "_fillStyle" ) # + self.fillStyleCounter[styleType].next()

        drawOptions = "COL"
        legOptions  = getattr(self, styleType + "_legOptions" )
        return (fillColour, lineColour, markerStyle, markerSize, lineWidth, lineStyle, fillStyle, drawOptions, legOptions)


    def PrintAttributes(self):
        '''
        Call this function to print all histogram attributes.
        '''
        self.Verbose(["Attributes: %s" % (self.__dict__)])
        return


    def GetTH1Styles(self, histoObject):
        '''
        Get the style attributes for a ROOT.TH1 histogram, such as colour, markerStyle, markerSize, lineWidth, lineStyle, fillStyle and options.
        '''
        self.Verbose()
        
        styleType = None

        if histoObject.styleType != None:
            styleType = histoObject.styleType.lower()
        else:
            styleType = histoObject.dataset.name.lower()
                    
        self.Verbose(["styleType: %s" % (styleType)])
        if styleType in self.styleTypeList:
            return self._GetTH1Values(styleType)
        elif styleType in self.styleTypeSpecialList:
            return self._GetTH1SpecialValues(styleType)
        else:
            return self._GetTH1Values("random")


    def GetTH2Styles(self, histoObject):
        '''
        Get the style attributes for a ROOT.TH2 histogram, such as colour, markerStyle, markerSize, lineWidth, lineStyle, fillStyle and options.
        '''
        self.Verbose()
        
        styleType = None
        
        if histoObject.styleType != None:
            styleType = histoObject.styleType.lower()
        else:
            styleType = histoObject.dataset.lower()

        if styleType in self.styleTypeList:
            return self._GetTH2Values(styleType)
        else:
            return self._GetTH2Values("random")


    def GetTGraphStyles(self, styleType, dataset = None):
        '''
        Get the style attributes for a ROOT.TH1 histogram, such as colour, markerStyle, markerSize, lineWidth, lineStyle, fillStyle and options.
        '''
        self.Verbose()
        msg  = "ERROR! Could not find the style type '%s' ['%s']."
        msg += "Please select one of the following style names:" % (styleType, type(styleType)), "\n\t".join(self.styleTypeList)
        msg += "EXIT"
        
        if dataset == None:
            if (styleType == None or styleType == "") and dataset == None:            
                self.Print(msg)
                sys.exit()

        styleType = styleType.lower()
        if styleType in self.styleTypeList:
            return self._GetTGraphValues(styleType)
        elif styleType in self.styleTypeSpecialList:
            return self._GetTH1SpecialValues(styleType)
        else:
            return self._GetTH2Values("random")
        
