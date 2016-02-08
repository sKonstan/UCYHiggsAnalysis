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

import ROOT

from UCYHiggsAnalysis.NtupleAnalysis.pyROOT.crossSection import xSections
#import UCYHiggsAnalysis.NtupleAnalysis.pyROOT.multicrab as m_multicrab


#================================================================================================
# Global variables
#================================================================================================
latexNamesDict = {}
latexNamesDict["ttHJetToNonbb_M125"]  = "ttH"               # (m_{H^{0}} = 125 GeV)"
latexNamesDict["TTJets"]              = "t#bar{t} + jets"
latexNamesDict["DYJetsToLL_M_10to50"] = "DY"                # (m_{#ell#ell}=10-50 GeV)"
latexNamesDict["WJetsToLNu"]          = "W^{#pm} #rightarrow l #nu_{l}" #to #ell #nu_{#ell}"
latexNamesDict["WW"]                  = "WW"                # "W^{#pm} W^{#mp}"
latexNamesDict["WZ"]                  = "WZ"                # "W^{#pm} Z^{0}"
latexNamesDict["ZZ"]                  = "ZZ"                # "Z^{0} Z^{0}"
latexNamesDict["MuonEG_246908_260426_25ns_Silver"]= "Data"


#================================================================================================
# Class Definition
#================================================================================================
class Dataset(object):
    def __init__(self, name, energy, rootFile, verbose = False, **args):
        self.verbose     = verbose
        self.name        = name
        self.latexName   = latexNamesDict[name]
        self.rootFile    = rootFile
        self.histo       = None
        self.energy      = energy
        self.xsection    = xSections.crossSection(name, energy)
        self.args        = args
        self.Verbose()
        return


    def Verbose(self, message=""):
        '''
        Custome made verbose system. Will print all messages in the messageList
        only if the verbosity boolean is set to true.
        '''
        if self.verbose:
            print "*** %s:" % (self.__class__.__name__ + "." + sys._getframe(1).f_code.co_name + "()")
            if message!="":
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
        self.Verbose()
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
        self.Verbose()
        self.verbose = verbose
        return


    def SetEnergy(self, energy):
        self.Verbose()
        self.energy   = energy
        self.xsection = xSections.crossSection(self.name, energy)
        return

        
    def SetXSection(self, xSection):
        self.Verbose()
        self.xsection = xSection
        return


    def GetLatexName(self):
        return self.latexName
    
    
    def PrintProperties(self):
        '''
        Prints the object's most important properties
        '''
        self.Verbose()
        msg  = " {:<20} {:<20}".format("Name"                   , ": " + self.name)
        msg += "\n\t {:<20} {:<20}".format("ROOT"              , ": " + self.rootFile.GetName())
        msg += "\n\t {:<20} {:<20}".format("Cross-Section (pb)", ": " + str(self.xsection) )
        msg += "\n\t {:<20} {:<20}".format("Energy (TeV)"      , ": " + self.energy)

        self.Print(msg)
        return
