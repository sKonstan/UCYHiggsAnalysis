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
    '''
    Colours: https://root.cern.ch/doc/master/classTColor.html
    root [0] TColorWheel *w = new TColorWheel();
    root [1] w->Draw();

    Markers: https://root.cern.ch/doc/v606/classTAttMarker.html
    '''
    def __init__(self, verbose = False):
        self.verbose                = verbose
        self.TextObject             = text.TextClass(verbose=self.verbose)
        self.datasetList            = ["DoubleMuon", "DoubleEG", "MuonEG", "SingleMuon", "SingleElectron"]
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
        self._SetDefaults("ST_s_channel_4f_leptonDecays", colour=ROOT.kYellow-7, mStyle=ROOT.kCircle, lWidth=2, lStyle=ROOT.kSolid , fStyle=1001, mSize = 1.0, drawOpts="HIST", legOpts="F")            
        self._SetDefaults("ST_t_channel_top_4f_leptonDecays", colour=ROOT.kYellow-9, mStyle=ROOT.kCircle, lWidth=2, lStyle=ROOT.kSolid , fStyle=1001, mSize = 1.0, drawOpts="HIST", legOpts="F")
        self._SetDefaults("ST_t_channel_antitop_4f_leptonDecays", colour=ROOT.kYellow-5, mStyle=ROOT.kCircle, lWidth=2, lStyle=ROOT.kSolid , fStyle=1001, mSize = 1.0, drawOpts="HIST", legOpts="F")
        self._SetDefaults("ST_tW_antitop_5f_inclusiveDecays", colour=ROOT.kGray+1, mStyle=ROOT.kCircle, lWidth=2, lStyle=ROOT.kSolid , fStyle=1001, mSize = 1.0, drawOpts="HIST", legOpts="F")
        self._SetDefaults("ST_tW_top_5f_inclusiveDecays", colour=ROOT.kGray+2, mStyle=ROOT.kCircle, lWidth=2, lStyle=ROOT.kSolid , fStyle=1001, mSize = 1.0, drawOpts="HIST", legOpts="F")
        self._SetDefaults("ttHJetToNonbb_M125" , colour=ROOT.kOrange+10, mStyle=ROOT.kOpenCircle      , lWidth=2, lStyle=ROOT.kSolid, fStyle=1001, mSize = 1.0, drawOpts="HIST", legOpts="F")
        self._SetDefaults("TTJets"             , colour=ROOT.kGray     , mStyle=ROOT.kCircle          , lWidth=2, lStyle=ROOT.kSolid , fStyle=1001, mSize = 1.0, drawOpts="HIST", legOpts="F")
        self._SetDefaults("DYJetsToLL_M_10to50", colour=ROOT.kGreen-9  , mStyle=ROOT.kOpenTriangleUp  , lWidth=2, lStyle=ROOT.kSolid , fStyle=1001, mSize = 1.0, drawOpts="HIST", legOpts="F")
        self._SetDefaults("DYJetsToLL_M_50", colour=ROOT.kGreen+3  , mStyle=ROOT.kOpenTriangleUp  , lWidth=2, lStyle=ROOT.kSolid , fStyle=1001, mSize = 1.0, drawOpts="HIST", legOpts="F")
        self._SetDefaults("WJetsToLNu"         , colour=ROOT.kMagenta-7, mStyle=ROOT.kOpenTriangleDown, lWidth=2, lStyle=ROOT.kSolid , fStyle=1001, mSize = 1.0, drawOpts="HIST", legOpts="F")
        self._SetDefaults("WW"                 , colour=ROOT.kBlue-4   , mStyle=ROOT.kMultiply        , lWidth=2, lStyle=ROOT.kSolid , fStyle=1001, mSize = 1.0, drawOpts="HIST", legOpts="F")
        self._SetDefaults("WZ"                 , colour=ROOT.kCyan-7   , mStyle=ROOT.kOpenSquare      , lWidth=2, lStyle=ROOT.kSolid , fStyle=1001, mSize = 1.0, drawOpts="HIST", legOpts="F")
        self._SetDefaults("ZZ"                 , colour=ROOT.kAzure+5, mStyle=ROOT.kOpenTriangleUp  , lWidth=2, lStyle=ROOT.kSolid , fStyle=1001, mSize = 1.0, drawOpts="HIST", legOpts="F")
        self._SetDefaults("Data"               , colour=ROOT.kBlack    , mStyle=ROOT.kFullCircle      , lWidth=2, lStyle=ROOT.kSolid, fStyle=1001, mSize = 1.0, drawOpts="P", legOpts="LP")
        self._SetSpecials("random", colour = cycle(self.colourPaletteList).next(), mStyle=ROOT.kFullCircle, lWidth=3, lStyle=0, fStyle=3001, drawOpts="HIST", legOpts="F")
        self.Verbose()
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
            # print "'%s': '%s' =  '%s'" % (name, argument , value)
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


    def _GetTH1Values(self, styleType):
        '''
        '''
        self.Verbose()
        
        fillColour  = getattr(self, styleType + "_colour" ) # + self.colourShade[styleType].next()
        markerStyle = getattr(self, styleType + "_mStyle"  )

        self.Verbose(["StyleType '%s', FillColour = '%s'" % (styleType, fillColour)])        
        lineColour  = fillColour
        markerSize  = getattr(self, styleType + "_mSize"    )
        lineWidth   = getattr(self, styleType + "_lWidth"   )
        lineStyle   = getattr(self, styleType + "_lStyle"   )
        fillStyle   = getattr(self, styleType + "_fStyle"   )
        drawOptions = getattr(self, styleType + "_drawOpts" )
        legOptions  = getattr(self, styleType + "_legOpts"  )
        return (fillColour, lineColour, markerStyle, markerSize, lineWidth, lineStyle, fillStyle, drawOptions, legOptions)


    def _GetTGraphValues(self, styleType):
        self.Verbose()
        
        fillColour  = getattr(self, styleType + "_colour" ) # + self.colourShade[styleType].next()
        markerStyle = getattr(self, styleType + "_mStyle"  )

        self.Verbose(["StyleType '%s', FillColour = '%s'" % (styleType, fillColour)])
        lineColour  = fillColour
        markerSize  = getattr(self, styleType + "_mSize"    )
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
        
        fillColour  = getattr(self, styleType + "_colour" ) + self.colourShade[styleType].next()
        markerStyle = self.markerStyleCounter[styleType].next()
        lineColour  = fillColour
        markerSize  = getattr(self, styleType + "_mSize"     )
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
        
        fillColour  = getattr(self, styleType + "_colour" ) + self.colourShade[styleType].next()
        markerStyle = self.markerStyleCounter[styleType].next()
        lineColour  = fillColour
        markerSize  = getattr(self, styleType + "_mSize"    )
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
        
        if histoObject.styleType != None:
            styleType = histoObject.styleType.lower()
        else:
            styleType = histoObject.dataset.name.lower()

        dName = histoObject.dataset.name
        if styleType in self.styleTypeList:
            return self._GetTH1Values(styleType)
        elif styleType in self.styleTypeSpecialList:
            return self._GetTH1SpecialValues(styleType)
        elif dName.split("_")[0] in self.datasetList: #in case data datasets are not merged
            return self._GetTH1Values("Data".lower())
        else:
            raise Exception("Could not determine style for dataset with name '%s'" % (dName))
        return
    

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
