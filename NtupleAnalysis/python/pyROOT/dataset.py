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
import StringIO

import ROOT

from UCYHiggsAnalysis.NtupleAnalysis.pyROOT.crossSection import xSections
import UCYHiggsAnalysis.NtupleAnalysis.pyROOT.multicrab as multicrab
import UCYHiggsAnalysis.NtupleAnalysis.pyROOT.aux as myAux


#================================================================================================
# Global variables
#================================================================================================
latexNamesDict = {}
latexNamesDict["ST_s_channel_4f_leptonDecays"]         = "t, s-channel"
latexNamesDict["ST_t_channel_antitop_4f_leptonDecays"] = "#bar{t}, t-channel"
latexNamesDict["ST_t_channel_top_4f_leptonDecays"]     = "t, t-channel"
latexNamesDict["ST_tW_antitop_5f_inclusiveDecays"]     = "#bar{t}W"
latexNamesDict["ST_tW_top_5f_inclusiveDecays"]         = "tW"
latexNamesDict["ttHJetToNonbb_M125"]                   = "ttH"
latexNamesDict["TTJets"]                               = "t#bar{t}+jets"
latexNamesDict["DYJetsToLL_M_10to50"]                  = "DY"
latexNamesDict["DYJetsToLL_M_50"]                      = "Z+jets"
latexNamesDict["WJetsToLNu"]                           = "W+jets" #"W^{#pm} #rightarrow l #nu_{l}"
latexNamesDict["WW"]                                   = "WW"
latexNamesDict["WZ"]                                   = "WZ"
latexNamesDict["ZZ"]                                   = "ZZ"
latexNamesDict["MuonEG_Run2015C_25ns_05Oct2015_v1_246908_260426_25ns_Silver"] = "MuonEG (2015C)"
latexNamesDict["MuonEG_Run2015D_PromptReco_v4_246908_260426_25ns_Silver"]     = "MuonEG (2015D-PR))"
latexNamesDict["MuonEG_Run2015D_05Oct2015_v2_246908_260426_25ns_Silver"]      = "MuonEG (2015D)"
# merged
latexNamesDict["Data"]      = "Data"
latexNamesDict["Bkg"]       = "Bkg"
latexNamesDict["Single t"]  = "Single top"

_debugNAllEvents = False

def TruncateString(myString, maxChars):
    tString = (myString[:maxChars-2] + "..") if len(myString) > maxChars else myString
    return tString


#================================================================================================
# Class Definition
#================================================================================================
class Dataset(object):
    def __init__(self, baseDir, name, analysisName, rootFile, verbose = False, **args):
        self.verbose            = verbose
        self.auxObject          = myAux.AuxClass(verbose)
        self.name               = name
        self.analysisName       = analysisName
        self.baseDir            = baseDir
        self.latexName          = latexNamesDict[name]
        self.rootFile           = rootFile
        self.drawObject         = None
        self.lumi               = None
        self.args               = args
        self.dataVersion        = self._GetDataVersion()
        self.codeVersion        = self._GetCodeVersion()
        self.pSet               = self._GetParameterSet()
        self.isData             = self._IsData()
        self.isPseudo           = self._IsPseudo()
        self.isMC               = self._IsMC()        
        self.info               = self._GetInfo()
        self.energy             = self._GetEnergy()
        self.xsection           = self._GetXSection()
        self.allEvents          = None
        self.unweightedEvents   = None
        self.weightedEvents     = None
        self.weightsApplied     = False
        self.isPileupReweighted = self._IsPileUpReweighted()
        self.isTopPtReweighted  = self._IsTopPtReweighted()
        self.pileupWeight       = self._GetPileupWeight()
        self.topPtWeight        = self._GetTopPtWeight()
        self._ReadCounters()
        self._UpdateWeightedEvents()
        self.normFactor         = self._GetNormFactor()    
        self.lumi               = self._GetLuminosity()
        self.intLumi            = None # set by dataset manager
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
        if message=="":
            return
        else:
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
    

    def ForEach(self, function):
        '''
        '''
        self.Verbose()
        return [function(self)]

    
    def _GetDataVersion(self):
        '''
        '''
        self.Verbose()
        dataVersion = self.auxObject.Get(self.rootFile, "configInfo/dataVersion")
        name        = dataVersion.GetName()
        title       = dataVersion.GetTitle()
        return title


    def _GetCodeVersion(self):
        '''
        '''
        self.Verbose()
        codeVersion = self.auxObject.Get(self.rootFile, "configInfo/codeVersionAnalysis")
        name        = codeVersion.GetName()
        title       = codeVersion.GetTitle()
        return codeVersion.GetTitle()


    def _GetParameterSet(self):
        '''
        '''
        self.Verbose()
        pSet  = self.auxObject.Get(self.rootFile, self.analysisName + "/config")
        name  = pSet.GetName()
        title = pSet.GetTitle()
        return title

    
    def GetParameterSet(self):
        '''
        '''
        self.Verbose()
        return self.pSet
    

    def _GetInfo(self):
        '''
        '''
        self.Verbose()
        configInfo = self.auxObject.Get(self.rootFile, "configInfo")
        if configInfo == None:
            self.Print("ERROR! configInfo directory is missing from file %s. EXIT" % self.rootFile.GetName())
            sys.exit()
            
        info = self.auxObject.Get(configInfo, "configinfo")
        return info

    
    def _GetXSection(self):
        '''
        '''
        self.Verbose()
        if not self.isMC:
            return None
        xsection = xSections.crossSection(self.name, "%0.0f" % (self.energy))
        self.Verbose("Setting cross-section of dataset '%s' to '%s'" % (self.name, xsection))
        return xsection
        

    def GetUnweightedEvents(self):
        '''
        '''        
        self.Verbose()
        return self.unweightedEvents
    

    def _UpdateWeightedEvents(self):
        '''
        '''        
        self.Verbose()
        if not self.GetIsMC():
            return

        # Variables
        ratio     = 1.0
        maxChars  = 30
        txtAlign  = "{:<34} {:<20} {:<20} {:<20} {:<20} {:<20}"
        header    = txtAlign.format("\t Dataset",  "Pileup Reweight", "Top-Pt Weight", "Events", "w-Events", "% Change")
        hLine     = "="*len(header)
        table     = []
        shortName = "\t " + TruncateString(self.GetName(), maxChars)

        # Create info table 
        table.append("\t " + hLine)
        table.append(header)
        table.append("\t " + hLine)
        unweightedEvents = self.weightedEvents

        if self.isPileupReweighted:
            delta = (self.pileupWeight - self.unweightedEvents) / self.unweightedEvents
            ratio = ratio * self.pileupWeight / self.unweightedEvents
            
        if self.isTopPtReweighted:
            delta = (self.topPtWeight - self.unweightedEvents) / self.unweightedEvents
            ratio = ratio * self.topPtWeight / self.unweightedEvents

        # Save weighed events
        self.weightedEvents = ratio * self.unweightedEvents
        self.allEvents      = ratio * self.unweightedEvents
        self.weightsApplied = True

        # Append info to table
        row = txtAlign.format(shortName , self.pileupWeight, self.topPtWeight, unweightedEvents, self.weightedEvents, str(delta*100.0) )
        table.append(row)

        if not self.verbose:
            return
        self.Print()
        for r in table:
                print r
        return 


    def GetWeightedEvents(self):
        '''
        '''        
        self.Verbose()
        return self.weightedEvents

    
    def GetAllEvents(self):
        if not hasattr(self, "allEvents"):
            raise Exception("Number of all events is not set for dataset %s! The counter directory was not given, and SetAllEvents() was not called." % self.name)
        return self.allEvents


    def SetAllEvents(self, allEvents):
        '''
        Set the number of all events (for normalization).
        
        This allows both overriding the value read from the event
        counter, or creating a dataset without event counter at all.
        '''
        self.allEvents = allEvents
        return
    

    def SetNormFactor(self, normFactor):
        self.normFactor = normFactor
        return
    

    def GetNormFactor(self):
        '''
        Get the cross section normalization factor.
        
        The normalization factor is defined as:
              normFactor = crossSection/N(allevents)
        so by multiplying the number of MC events with the factor one gets the corresponding cross section.
        '''
        self.Verbose()
        if not self.isMC:
            return None
        
        # Sanity checkk
        if not self.weightsApplied:
            raise Exception("Trying to get the normalisation factor but the necessary MC weights have not been applied!")

        allEvents = self.GetAllEvents()
        causes    = "\n\t1) Counters are weighted"
        causes   += "\n\t2) Analysis job input was a skim"
        causes   += "\n\t3) The method UpdateNAllEventsToPUWeighted() has not been called"
        if allEvents == 0:
            msg = "Number of all events is '%s' for dataset '%s'! Probable causes:" % (allEvents, self.name)
            raise Exception(msg + causes)

        return self.GetXSection() / allEvents


    def _GetLuminosity(self):
        '''
        Get the luminosity corresponding to the generated events
        '''
        self.Verbose()
        if not self.isMC:
            return None
        return self.allEvents / self.GetXSection()


    def GetLuminosity(self):
        self.Verbose()
        return self.lumi

    
    def _GetEnergy(self):
        '''
        '''
        energy  = -1
        control = -1
        nBinsX  = self.info.GetNbinsX()
        for i in range(0, nBinsX):
            if (self.info.GetXaxis().GetBinLabel(i) == "energy"):
                energyVal = self.info.GetBinContent(i)
            if (self.info.GetXaxis().GetBinLabel(i) == "control"):
                controlVal = self.info.GetBinContent(i)

        energy = energyVal/controlVal
        return energy

    
    def _IsPileUpReweighted(self):
        '''
        '''
        self.Verbose()

        binLabel  = "isPileupReweighted"
        binNumber = self._GetBinNumberFromBinLabel(self.info, binLabel)
        weight    = self.info.GetBinContent(binNumber)
        if isinstance(weight, float):
            return True
        else:
            raise Exception("The weight '%s' for dataset '%s' is not an instance of float." % (binLabel, self.name) )
        return False


    def _GetPileupWeight(self):
        '''
        '''
        self.Verbose()
        if self.GetIsData():
            return None

        binLabel = "isPileupReweighted"
        if not self.isPileupReweighted:
            raise Exception("Cannot determine weight '%s' for dataset '%s' because it was not found to be weighted." % (binLabel, self.name) )
        
        binNumber = self._GetBinNumberFromBinLabel(self.info, binLabel)
        weight    = self.info.GetBinContent(binNumber)
        if isinstance(weight, float):
            return weight
        else:
            raise Exception("The weight '%s' for dataset '%s' is not an instance of float." % (binLabel, self.name) )
        return None

    
    def GetPileupWeight(self):
        '''
        '''
        self.Verbose()
        return self.pileupWeight
        
        
    def _IsTopPtReweighted(self):
        '''
        '''
        self.Verbose()

        binLabel  = "isTopPtReweighted"    
        binNumber = self._GetBinNumberFromBinLabel(self.info, binLabel)
        weight    = self.info.GetBinContent(binNumber)
        if isinstance(weight, float):
            if weight > 0.0:
                return True
            else:
                return False
        else:
            raise Exception("The weight '%s' for dataset '%s' is not an instance of float." % (binLabel, self.name) )
        return False

    
    def _GetTopPtWeight(self):
        '''
        '''
        self.Verbose()
        if self.GetIsData():
            return None

        binLabel  = "isTopPtReweighted"
        if not self.isPileupReweighted:
            raise Exception("Cannot determine weight '%s' for dataset '%s' because it was not found to be weighted." % (binLabel, self.name) )
        
        binNumber = self._GetBinNumberFromBinLabel(self.info, binLabel)
        weight    = self.info.GetBinContent(binNumber)
        if isinstance(weight, float):
            return weight
        else:
            raise Exception("The weight '%s' for dataset '%s' is not an instance of float." % (binLabel, self.name) )
        return None
    

    def GetTopPtWeight(self):
        '''
        '''
        self.Verbose()
        return self.topPtWeight

    
    def GetIsPileupReweighted(self):
        '''
        '''
        self.Verbose()
        return self.isPileupReweighted


    def GetIsTopPtReweighted(self):
        '''
        '''
        self.Verbose()
        return self.isTopPtReweighted

    
    def GetDataVersion(self):
        '''
        '''
        self.Verbose()
        return self.dataVersion


    def GetCodeVersion(self):
        '''
        '''
        self.Verbose()
        return self.codeVersion
    

    def _IsData(self):
        '''
        '''
        self.Verbose()

        isData = "data" in self.dataVersion
        return isData


    def GetIsData(self):
        '''
        '''
        self.Verbose()
        return self.isData
    

    def _IsMC(self):
        '''
        '''
        self.Verbose()

        isData    = "data" in self.dataVersion
        isPseudo  = "pseudo" in self.dataVersion
        isMC      = not (isData or isPseudo)
        return isMC


    def GetIsMC(self):
        '''
        '''
        self.Verbose()
        return self.isMC

    
    def _IsPseudo(self):
        '''
        '''
        self.Verbose()

        isPseudo = "pseudo" in self.dataVersion
        return isPseudo

    
    def GetIsPseudo(self):
        '''
        '''
        self.Verbose()
        return self.isPseudo


    def GetDataType(self):
        '''
        Self explanatory
        '''
        if self._IsData():
            return "data"
        if self._IsMC():
            return "MC"
        
        if self._IsPseudo():
            return "pseudo"
        raise Exception("I don't know what I am, sorry.")


    def SetEnergy(self, energy):
        self.Verbose()
        self.energy   = energy
        self.xsection = xSections.crossSection(self.name, energy)
        return

    
    def GetEnergy(self):
        self.Verbose()
        return self.energy

    
    def GetEnergyString(self):
        self.Verbose()
        energy =  "(%0.0f TeV)" % (self.energy)
        return energy


    def GetIntLumiString(self, units = "fb"):
        self.Verbose()

        unitsFactor = 0
        if units == "fb":
            units       = "fb^{-1}"
            unitsFactor = float(1.0/1000.0)
        elif units == "pb":
            units       = "pb^{-1}"
            unitsFactor = float(1.0)
        else:
            self.Print("Unsupported units options '%s' for luminosity string. Select either 'fb' or 'pb'. EXIT" % (units) )
            sys.exit()

        intLumi = "%0.2f" % (self.intLumi * unitsFactor)
        return intLumi + " " + units

    
    def SetLuminosity(self, lumi):
        self.Verbose()
        if self.GetIsMC():
            return
        self.lumi = lumi
        return

    def SetIntegratedLuminosity(self, intLumi):
        self.Verbose()
        self.intLumi = intLumi
        return


    def GetLuminosity(self):
        self.Verbose()
        return self.lumi
        return


    def GetIntLuminosity(self):
        self.Verbose()
        return self.intLumi
        return


    def SetXSection(self, xSection):
        self.Verbose()
        self.xsection = xSection
        return


    def GetLatexName(self):
        self.Verbose()
        return self.latexName

    
    def GetName(self):    
        self.Verbose()
        return self.name


    def SetName(self, name):
        self.Verbose()
        self.name = name
    

    def GetXSection(self):    
        self.Verbose()
        return self.xsection


    def SetDrawObject(self, drawObject):
        self.Verbose()
        self.drawObject = drawObject
        return


    def GetDrawObject(self):    
        self.Verbose()
        return self.drawObject
    
    
    def GetBaseDir(self):
        self.Verbose()
        return self.baseDir

    
    def GetRootFile(self):
        self.Verbose()
        return self.rootFile


    def GetRootHisto(self, name, **kwargs):
        '''
        Get ROOT histogram

        \param name    Path of the ROOT histogram relative to the analysis root directory

        \param kwargs  Keyword arguments, forwarded to GetRootObjects()

        \return pair (\a histogram, \a realName)                                                
    
        If name starts with slash ('/'), it is interpreted as a absolute  
        path within the ROOT file. If dataset consists of multiple files, the histograms are added with the ROOT.TH1.Add() method.
        
        If dataset.TreeDraw object is given (or actually anything with
        draw() method), the draw() method is called by giving the Dataset object as parameters. The draw() method is expected to
        return a TH1 which is then returned.
         '''
        self.Verbose()
        
        (histos, realName) = self.GetRootObjects(name, **kwargs)
        if len(histos) == 1:
            h = histos[0]
        else:
            h = histos[0]
            h = auxObject.Clone(h, h.GetName() + "_cloned")
            for h2 in histos[1:]:
                h.Add(h2)
        return (h, realName)

    
    def GetRootObject(self, name, **kwargs):
        '''
        Get arbitrary ROOT object from the file
        \param name    Path of the ROOT object relative to the analysis root directory           
        
        \param kwargs  Keyword arguments, forwarded to getRootObjects()
        
        \return pair (\a object, \a realName)
        
        If name starts with slash ('/'), it is interpreted as a absolute path within the ROOT file.
        
        If the dataset consists of multiple files, raise an Exception.
        
        User should use GetRootObjects() method instead.
        '''
        self.Verbose()
        
        (lst, realName) = self.getRootObjects(name, **kwargs)
        return (lst[0], realName)


    def GetRootObjects(self, name, **kwargs):
        '''
        Get list of arbitrary ROOT objects from the file
        \param name    Path of the ROOT object relative to the analysis root directory           

        \param kwargs  Keyword arguments, forwarded to _translateName()

        \return pair (\a list, \a realName), where \a list is the list of ROOT objects, one per file, 
        and \a realName is the physical name of the objects

        If name starts with slash ('/'), it is interpreted as a absolute path within the ROOT file
        '''
        self.Verbose()

        ret      = []        
        realName = self._TranslateName(name, **kwargs)
        o        = self.auxObject.Get(self.rootFile, realName)
        
        # Important to use '==' instead of 'is', because null TObject == None, but is not None
        if o == None:
            self.Print("Unable to find object '%s' (requested '%s') from file '%s'" % (realName, name, self.rootFile.GetName()) )
        ret.append(o)
        return (ret, realName)
    
    
    def _TranslateName(self, name, analysisPostfix=""):
        '''
        '''
        self.Verbose("Translating name '%s' with analysisPostFix '%s'" % (name, analysisPostfix))

        ret = ""        
        if len(name) > 0 and name[0] == '/':
            ret = name[1:]
            return ret
        else:
            #ret = self._analysisDirectoryName
            if analysisPostfix != "":
                ret = ret.replace("/", analysisPostfix+"/")
            
            ret += name
            
            if ret[-1] == "/":
                return ret[0:-1]
            return ret
           

    def _GetNormFactor(self):
        self.Verbose()

        if not self.isMC:
            return None

        if not isinstance(self.xsection, float) or not hasattr(self, "xsection"):
            print "self.xsection = ", self.xsection 
            raise Exception("Cross-section is undefined for dataset %s" % self.name)
        if not isinstance(self.allEvents, float) or not hasattr(self, "allEvents"):
            raise Exception("All events is undefined for dataset %s" % self.name)
        
        if self.allEvents > 0:
            return self.xsection / self.allEvents
        else:
            #raise Exception("Cannot determine the normalisation factor for dataset %s. Division by zero (allEvents=%s) " % (self.name, self.allEvents) )
            return 0.0


    def _GetBinNumberFromBinLabel(self, histo, binLabel):
        '''
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
                    
    
    def _ReadUnweightedCounters(self):
        '''
        TDirectory name containing the counters, relative to the analysis directory (default: analysisDirectory+'/counters')")
          
        Reads unweighted counters, saves values & performs sanity checks
        '''
        self.Verbose()

        counterPath         = self.analysisName + "/counters/counter"
        (counter, realName) = self.GetRootHisto(counterPath)
        self._CheckCounter(counterPath)
        
        # Convert the counter histogram (TH1) to a list of (name, count) pairs. 0 is first bin, NOT underflow bin
        countObject = self.auxObject.ConvertHistoToCounter(counter, self.verbose)

        # First counter (index 0), second element (index 1) of the tuple [NOTE: First counter is the underflow bin)
        self.unweightedEvents = countObject[0][1].value()
        self.allEvents        = self.unweightedEvents

        allEventsBin = self._GetBinNumberFromBinLabel(histo=counter, binLabel="Base::AllEvents")

        self.Verbose("Successfully read counters in '%s'. Number of events is '%s'" % (counterPath, self.unweightedEvents))
        return

    
    def _ReadWeightedCounters(self):
        '''
        Reads weighted counters, saves values & performs sanity checks
        '''
        self.Verbose()

        wCounterPath         = self.analysisName + "/counters/weighted/counter"
        (wCounter, realName) = self.GetRootHisto(wCounterPath)
        # self._CheckCounter(counterPath) # not needed & likely to fail because of weights
        
        # Convert the counter histogram (TH1) to a list of (name, count) pairs. 0 is first bin, NOT underflow bin
        wCountObject = self.auxObject.ConvertHistoToCounter(wCounter, self.verbose)

        # First counter (index 0), second element (index 1) of the tuple [NOTE: First counter is the underflow bin)
        self.weightedEvents = wCountObject[0][1].value()
        self.allEvents      = self.weightedEvents

        # NB: At this point self.weightedEvents = self.unweightedEvents, but once weights are applied it changes!
        self.Verbose("Successfully read counters in '%s'. Number of events is '%s'" % (wCounterPath, self.weightedEvents))
        return


    def _CheckCounter(self, counterPath):
        '''
        Check normalization from weighted counters
        '''
        self.Verbose("Checking counter '%s'" % (counterPath) )
        
        normalisationIsOk   = True
        (counter, realName) = self.GetRootHisto(counterPath)

        # Convert the counter histogram (TH1) to a list of (name, count) pairs
        countObject  = self.auxObject.ConvertHistoToCounter(counter, self.verbose)
        allEventsBin = self._GetBinNumberFromBinLabel(histo=counter, binLabel="Base::AllEvents")

        allEvts      = counter.GetBinContent(allEventsBin)
        afterAllEvts = counter.GetBinContent(allEventsBin+1)
        if allEvts < afterAllEvts:
            normalisationIsOk = False

        if not normalisationIsOk:
            #raise Exception("Error: dset=%s: Unweighted skimcounter (%s) is smaller than all events counter of analysis (%s)!" % (self.name, allEvts, afterAllEvts) )
            print "=== dataset.py:\n\t Normalisation is NOT ok for dataset \"%s\" (%s). allEvts = %s, afterAllEvts = %s"  % (self.GetName(), counterPath, allEvts, afterAllEvts)
        return
    

    def _ReadCounters(self):
        '''
        TDirectory name containing the counters, relative to the analysis directory (default: analysisDirectory+'/counters')")
          
        # Read unweighted counters
        # The unweighted counters are allowed to not exist unless  weightedCounters are also enabled

        '''
        self._ReadUnweightedCounters()
        self._ReadWeightedCounters()
        return


    def PrintProperties(self):
        '''
        Prints the object's most important properties
        '''
        self.Print()
        txtAlign = "{:<30} {:<40}"
        msgs     = []
        msgs.append( txtAlign.format("Name "                , ": " + self.GetName() + " (" + self.GetLatexName() + ")" ) )
        msgs.append( txtAlign.format("Data Version"         , ": " + str(self.GetDataVersion()) ) ) 
        msgs.append( txtAlign.format("Cross-Section (pb)"   , ": " + str(self.GetXSection()) ) ) 
        msgs.append( txtAlign.format("Energy (TeV)"         , ": " + str(self.GetEnergy()) ) )
        msgs.append( txtAlign.format("Luminosity (1/pb)"    , ": " + str(self.GetLuminosity()) ) )
        # msgs.append( txtAlign.format("Parameter Set"        , ": " + str(self._GetParameterSet()) ) )
        # msgs.append( txtAlign.format("Info"                 , ": " + str(self._GetInfo()) ) )
        msgs.append( txtAlign.format("Norm Factor"          , ": " + str(self._GetNormFactor()) ) )
        msgs.append( txtAlign.format("Lumi (1/pb) "         , ": " + str(self._GetLuminosity()) ) ) 
        msgs.append( txtAlign.format("MC-Lumi (1/pb)"       , ": " + str(self._GetMCLuminosity()) ) ) 
        msgs.append( txtAlign.format("Int-Lumi (1/pb)"      , ": " + str(self._GetIntLuminosity()) ) ) 
        msgs.append( txtAlign.format("Is MC"                , ": " + str(self.GetIsMC()) ) ) 
        msgs.append( txtAlign.format("Is Data"              , ": " + str(self.GetIsData()) ) ) 
        msgs.append( txtAlign.format("Is Pseudo"            , ": " + str(self.GetIsPseudo()) ) )
        msgs.append( txtAlign.format("Is PU Reweighted"     , ": " + str(self.GetIsPileupReweighted()) ) )
        msgs.append( txtAlign.format("Is TopPt Reweighted"  , ": " + str(self.GetIsTopPtReweighted()) ) )
        msgs.append( txtAlign.format("Is PU Reweighted"     , ": " + str(self.GetIsPileupReweighted())  + " (" + str(self.GetPileupWeight()) + ")" ) )
        msgs.append( txtAlign.format("Is TopPt Reweighted"  , ": " + str(self.GetIsTopPtReweighted())   + " (" + str(self.GetTopPtWeight()) + ")" ) )
        msgs.append( txtAlign.format("Base Directory"       , ": " + self.GetBaseDir() ) )
        msgs.append( txtAlign.format("ROOT"                 , ": " + self.GetRootFile().GetName() ) ) 
        msgs.append( txtAlign.format("Code Version"         , ": " + str(self._GetCodeVersion()) ) )

        if hasattr(self, 'THisto'):
            msgs.append( "\n\t {:<20} {:<20}".format("Histo Name"     , ": " + self.THisto.GetName() ) )
        for r in msgs:
            print "\t ", r
        return


    def Close(self):
        '''
        Close the files
        Can be useful when opening very many files in order to reduce
        the memory footprint and not hit the limit of number of open
        files
        '''
        #for f in self.rootFiles:
        #    f.Close("R")
        #    f.Delete()

        self.rootFile.Close("R")
        self.rootFile.Delete()
        self.rootFile = "" #[]
        return


#================================================================================================ 
# Class Definition
#================================================================================================ 
class DatasetMerged(object):
    '''
    Dataset class for histogram access for a dataset merged from Dataset objects.
    The merged datasets are required to be either MC, data, or pseudo
    '''
    def __init__(self, name, datasets, verbose=False):
        '''
        Constructor.
        
        \param name      Name of the merged dataset

        \param datasets  List of dataset.Dataset objects to merge
        
        Calculates the total cross section (luminosity) for MC (data or pseudo)
        datasets.
        '''
        self.verbose  = verbose
        self.name     = name
        self.datasets = datasets
        self._SanityCheck()
        self.info             = {}
        self.auxObject        = myAux.AuxClass(verbose)
        self.energy           = self._GetEnergy()
        self.xsection         = self._GetXSection()
        self.lumi             = self._GetLuminosity()
        self.dataVersion      = self._GetDataVersion()
        self.unweightedEvents = self._GetUnweightedEvents()
        self.weightedEvents   = self._GetWeightedEvents()
        self.latexname        = latexNamesDict[name]
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
        else:
            return
        return


    def _SanityCheck(self):
        self.Verbose()

        if len(self.datasets) == 0:
            raise Exception("=== dataset.py:\n\t Can't create a DatasetMerged from 0 datasets")
        return


    def _GetLuminosity(self):
        '''
        If all merged datasets are Data return their luminosity sum. Otherwise return None.
        '''
        self.Verbose()

        if self.datasets[0].GetIsMC():
            return None

        refType = self.datasets[0].GetDataType()
        lumiSum = 0.0
        for d in self.datasets:
            lumiSum += d.GetLuminosity()
            dType = d.GetDataType()
            if refType != dType:
                msg = "Can't merge non-%s datasets %s with %s datasets, it is %s" % (reft, d.GetName(), t)
                raise Exception("=== dataset.py:\n\t ", msg)
        self.info["luminosity"] = lumiSum
        return lumiSum


    def _GetXSection(self):
        '''
        If all merged datasets are MC return their cross-section sum. Otherwise return None
        '''
        self.Verbose()

        if not self.datasets[0].GetIsMC():
            return None

        xSectionSum = 0.0
        for d in self.datasets:
            if not d.GetIsMC():
                msg =  "Can't merge non-MC dataset %s with MC datasets, it is %s" % (d.getName(), d.getDataType())
                raise Exception("=== dataset.py:\n\t ", msg)
            else:
                xSectionSum += d.GetXSection()
        self.info["crossSection"] = xSectionSum
        return xSectionSum


    def _GetDataVersion(self):
        '''
        If all merged datasets are of same type return their dataVersion.
        '''
        self.Verbose()

        dataVersion    = self.datasets[0].GetDataVersion()
        for d in self.datasets:
            dVer = d.GetDataVersion()
            if dataVersion != dVer:
                msg = "Can't merge datasets with different dataVersions (%s: %s, %s: %s)" % (self.datasets[0].GetName(), dataVersion, d.GetName(), dVer)
                raise Exception("=== dataset.py:\n\t ", msg)
            else:
                pass

        #self.info["dataVersion"] = dataVersion
        return dataVersion

  
    def GetDataVersion(self):
        self.Verbose()
        
        return self.dataVersion

    
    def GetDatasets(self):
        self.Verbose()
        return self.datasets


    def _GetEnergy(self):
        '''
        Ensure that all merged datasets have the same energy. Return COM energy.
        '''
        self.Verbose()

        energy = self.datasets[0].GetEnergy()
        for d in self.datasets[1:]:
            if energy != d.GetEnergy():
                msg = "Can't merge datasets with different COM energies (%s: %d TeV, %s: %d TeV)" % (self.datasets[0].GetName(), energy, d.GetName(), d.GetEnergy())
                raise Exception("=== dataset.py:\n\t ", msg)
        return energy


    def _GetUnweightedEvents(self):
        '''
        Get sum of all unweighted events from the individual merge datasets
        '''
        self.Verbose()

        unweightedEvents = 0
        for d in self.datasets:
            unweightedEvents += d.GetUnweightedEvents()
        return unweightedEvents


    def GetUnweightedEvents(self):
        self.Verbose()
        return self.unweightedEvents


    def _GetWeightedEvents(self):
        '''
        Get sum of all weighted events from the individual merge datasets
        '''
        self.Verbose()

        weightedEvents = 0
        for d in self.datasets:
            weightedEvents += d.GetWeightedEvents()
        return weightedEvents


    def GetWeightedEvents(self):
        self.Verbose()
        return self.weightedEvents


    def Close(self):
        ''' 
        Close TFiles in the contained dataset.Dataset objects
        '''
        self.Verbose()

        # For-loop: All datasets
        for d in self.datasets:
            print "=== dataset.py:\n\t Closing dataset '%s'" % (d)
            d.Close()
        return

            
    def DeepCopy(self):
        '''
        Make a deep copy of a DatasetMerged object.
        
        Nothing is shared between the returned copy and this object.
        
        \see dataset.Dataset.deepCopy()
        '''
        self.Verbose()

        dm = DatasetMerged(self.name, [d.DeepCopy() for d in self.datasets])
        dm.info.update(self.info)
        return dm


    def SetDirectoryPostfix(self, postfix):
        self.Verbose()

        for d in self.datasets:
            d.SetDirectoryPostfix(postfix)
        return


    def GetName(self):
        self.Verbose()
        return self.name


    def SetName(self, name):
        self.Verbose()
        self.name = name
        return


    def GetLatexName(self):
        self.Verbose()
        return self.latexname


    def SetLatexName(self, name):
        self.Verbose()
        self.latexname = name
        return


    def ForEach(self, function):
        self.Verbose()

        ret = []
        for d in self.datasets:
            ret.extend(d.ForEach(function))
        return ret


    def SetEnergy(self, energy):
        self.Verbose()

        for d in self.datasets:
            d.SetEnergy(energy)
        return


    def GetEnergy(self):
        self.Verbose()
        return self.datasets[0].GetEnergy()


    def SetXSection(self, value):
        self.Verbose()
        if not self.GetIsMC():
            raise Exception("=== dataset.py:\n\t Should not set cross section for non-MC dataset %s (has luminosity)" % self.name)
        raise Exception("=== dataset.py:\n\t Setting cross section for merged dataset is meaningless (it has no real effect, and hence is misleading")


    def GetXSection(self):
        '''
        Get cross section of MC dataset (in pb).
        '''
        self.Verbose()

        if not self.GetIsMC():
            #raise Exception("=== dataset.py:\n\t Dataset %s is not MC, no cross section available" % self.name)
            return None
        return self.info["crossSection"]


    def SetLuminosity(self, value):
        self.Verbose()

        if self.GetIsMC():
            raise Exception("=== dataset.py:\n\t Should not set luminosity for MC dataset %s (has crossSection)" % self.name)
        raise Exception("=== dataset.py:\n\t Setting luminosity for merged dataset is meaningless (it has no real effect, and hence is misleading)")


    def GetLuminosity(self):
        '''
        Get the integrated luminosity of data dataset (in pb^-1).
        '''
        self.Verbose()

        if self.GetIsMC():
            #raise Exception("=== dataset.py:\n\t Dataset %s is MC, no luminosity available" % self.name)
            return None
        return self.info["luminosity"]


    def SetProperty(self, key, value):
        self.Verbose()
        self.info[key] = value
        return


    def GetProperty(self, key):
        self.Verbose()
        return self.info[key]


    def GetIsData(self):
        self.Verbose()
        return self.datasets[0].GetIsData()


    def GetIsPseudo(self):
        self.Verbose()
        return self.datasets[0].GetIsPseudo()


    def GetIsMC(self):
        self.Verbose()
        return self.datasets[0].GetIsMC()


    def GetCounterDirectory(self):
        self.Verbose()

        countDir = self.datasets[0].GetCounterDirectory()
        for d in self.datasets[1:]:
            if countDir != d.GetCounterDirectory():
                raise Exception("=== dataset.py:\n\t Error: merged datasets have different counter directories")
        return countDir


    def GetNormFactor(self):
        self.Verbose()
        return None


    def HasRootHisto(self, name):
        '''
        Check if a ROOT histogram exists in this dataset
        
        \param name  Name (path) of the ROOT histogram
        
        The ROOT histogram is expected to exist in all underlying
        dataset.Dataset objects.
        '''
        self.Verbose()

        has = True
        for d in self.datasets:
            has = has and d.hasRootHisto(name)
        return has


    def GetDatasetRootHisto(self, name, **kwargs):
        '''
        Get the DatasetRootHistoMergedMC/DatasetRootHistoMergedData object for a named histogram.
        
        \param name   Path of the histogram in the ROOT file

        \param kwargs Keyword arguments, forwarder to get
        getDatasetRootHisto() of the contained Dataset objects
        
        DatasetRootHistoMergedData works also for pseudo
        '''
        self.Verbose()

        wrappers = [d.GetDatasetRootHisto(name, **kwargs) for d in self.datasets]
        if self.isMC():
            return DatasetRootHistoMergedMC(wrappers, self)
        elif self.isData():
            return DatasetRootHistoMergedData(wrappers, self)
        elif self.isPseudo():
            return DatasetRootHistoMergedPseudo(wrappers, self)
        else:
            raise Exception("=== dataset.py:\n\t Internal error (unknown dataset type)")
        return


    def GetFirstRootHisto(self, name, **kwargs):
        '''
        Get ROOT histogram
        
        \param name    Path of the ROOT histogram relative to the analysis
        root directory

        \param kwargs  Keyword arguments, forwarded to getRootObjects()
        
        \return pair (\a first histogram, \a realName)
        
        If name starts with slash ('/'), it is interpreted as a absolute
        path within the ROOT file.
        
        If dataset.TreeDraw object is given (or actually anything with
        draw() method), the draw() method is called by giving the
        Dataset object as parameters. The draw() method is expected to
        return a TH1 which is then returned.
        '''
        self.Verbose()

        if hasattr(self.datasets[0], "getFirstRootHisto"):
            content = self.datasets[0].GetFirstRootHisto(name, **kwargs)
        else:
            content = self.datasets[0].GetRootHisto(name, **kwargs)
        return content


    def GetDirectoryContent(self, directory, predicate=lambda x: True):
        '''
        Get the directory content of a given directory in the ROOT file.
        
        \param directory   Path of the directory in the ROOT file

        \param predicate   Append the directory name to the return list only if
                           predicate returns true for the name. Predicate
                           should be a function taking a string as an
                           argument and returning a boolean.
        
        Returns a list of names in the directory. The contents of the
        directories of the merged datasets are required to be identical.
        '''
        content = self.datasets[0].GetDirectoryContent(directory, predicate)
        for d in self.datasets[1:]:
            if content != dGgetDirectoryContent(directory, predicate):
                raise Exception("=== dataset.py:\n\t Error: merged datasets have different contents in directory '%s'" % directory)
        return content


    def FormatDatasetTree(self, indent):
        self.Verbose()

        ret = '%sDatasetMerged("%s", [\n' % (indent, self.getName())
        for dataset in self.datasets:
            ret += dataset.FormatDatasetTree(indent+"  ")
        ret += "%s]),\n" % indent
        return ret


    def GetDataVersion(self):
        self.Verbose()
        return self.dataVersion


    def PrintProperties(self):
        '''
        Prints the object's most important properties
        '''
        self.Verbose()
        
        msg  = "{:<20} {:<20}".format("Name "                   , ": " + self.GetName() + " (" + self.GetLatexName() + ")" )
        msg += "\n\t{:<20} {:<20}".format("Cross-Section (pb)"  , ": " + str(self.GetXSection()) )
        msg += "\n\t{:<20} {:<20}".format("Energy (TeV)"        , ": " + str(self.GetEnergy()) )
        msg += "\n\t{:<20} {:<20}".format("Luminosity (1/pb)"   , ": " + str(self.GetLuminosity()) )
        msg += "\n\t{:<20} {:<20}".format("Data Version"        , ": " + str(self.GetDataVersion()) )
        msg += "\n\t{:<20} {:<20}".format("Is MC"               , ": " + str(self.GetIsMC()) )
        msg += "\n\t{:<20} {:<20}".format("Is Data"             , ": " + str(self.GetIsData()) )
        msg += "\n\t{:<20} {:<20}".format("Is Pseudo"           , ": " + str(self.GetIsPseudo()) )
        self.Print(msg)
        return



#================================================================================================ 
# Class Definition
#================================================================================================ 
class DatasetManager(object):
    '''
    Collection of Dataset objects which are managed together.
    
    Holds both an ordered list of Dataset objects, and a name->object
    map for convenient access by dataset name.
    
    '''
    def __init__(self, baseDir, analysisName, verbose=False):
        '''
        The parameter "baseDir" is the (multicrab) directory (absolute or relative to the cwd) 
        where the luminosity JSON file is located (see self.LoadLuminosities())
        
        DatasetManager is constructed as empty
        '''
        self.verbose      = []
        self.intLumi      = 0
        self.datasets     = []
        self.datasetMap   = {}
        self.mcrab        = multicrab.Multicrab(verbose)
        self.analysisName = analysisName
        self._SetBaseDirectory(baseDir)
        self._AppendDatasets(baseDir)
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
        if message=="":
            return
        else:
            print "\t", message
        return

    
    def PrintList(self, messageList=[""]):
        '''
        Custome made print system. Will print all messages in the messageList even if the verbosity boolean is set to false.
        '''
        print "=== %s:" % (self.__class__.__name__ + "." + sys._getframe(1).f_code.co_name + "()")
        for counter, message in enumerate(messageList):
            if counter == 0:
                print "\t", message
            else:
                print "\t", message
        return


    def SetVerbose(self, verbose):
        '''
        Manually enable/disable verbosity.
        '''
        self.verbose = verbose
        return


    def _PopulateMap(self):
        '''
        Populate the datasetMap member from the datasets list.
        
        Intended only for internal use.
        '''
        self.Verbose()
        
        self.datasetMap = {}
        for d in self.datasets:
            self.datasetMap[d.GetName()] = d
        return

    
    def _SetBaseDirectory(self, baseDir):
        '''
        '''
        self.Verbose()
        
        for d in self.datasets:
            d._setBaseDirectory(baseDir)
        return
    

    def _AppendDatasets(self, baseDir):
        '''
        '''
        self.Verbose()
        
        datasetNames = self.mcrab.GetDatasetsFromMulticrabDir(baseDir)    
        datasetNames.sort(key=lambda x: x.lower())
        self.Verbose("Appending %s (alphabetically sorted) datasets to the dataset manager: %s" % (len(datasetNames), datasetNames))
        
        for dName in datasetNames:
            rootFile      = self.mcrab.GetDatasetRootFile(baseDir, dName)
            datasetObject = Dataset(baseDir, dName, self.analysisName, rootFile, self.verbose)            
            self.Append(datasetObject)
            
        return

        
    def Close(self):
        '''
        Close all TFiles of the contained dataset.Dataset objects
        
        \see dataset.Dataset.close()
        '''
        self.Verbose()
        
        for d in self.datasets:
            d.Close()
        return

    
    def Append(self, dataset):
        '''
        Append a Dataset object to the set.
        
        \param dataset    Dataset object
        
        The new Dataset must have a different name than the already existing ones.
        '''
        self.Verbose()
        
        if dataset.GetName() in self.datasetMap:
            raise Exception("=== dataset.py:\n\tDataset '%s' already exists in this DatasetManager" % dataset.GetName())

        self.datasets.append(dataset)
        self.datasetMap[dataset.GetName()] = dataset
        return

    
    def Extend(self, datasetmgr):
        '''
        Extend the set of Datasets from another DatasetManager object.
        
        \param datasetmgr   DatasetManager object
        
        Note that the dataset.Dataset objects of datasetmgr are appended to
        self by reference, i.e. the Dataset objects will be shared
        between them.
        '''
        self.Verbose()
        
        for d in datasetmgr.datasets:
            self.append(d)
        return

    
    def ShallowCopy(self):
        '''
        Make a shallow copy of the DatasetManager object.
        
        The dataset.Dataset objects are shared between the DatasetManagers.
        
        Useful e.g. if you want to have a subset of the dataset.Dataset objects
        '''
        self.Verbose()
        
        copy = DatasetManager()
        copy.extend(self)
        return copy

    
    def DeepCopy(self):
        '''
        Make a deep copy of the DatasetManager object.
        
        Nothing is shared between the DatasetManagers.
        
        Useful e.g. if you want to have two sets of same datasets, but
        others are somehow modified (e.g. cross section)
        '''
        self.Verbose()
        
        copy = DatasetManager()
        for d in self.datasets:
            copy.append(d.deepCopy())
        return copy

    
    def SetEnergy(self, energy):
        '''
        Set the centre-of-mass energy for all datasets
        '''
        self.Verbose()
        
        for d in self.datasets:
            d.SetEnergy(energy)
        return
    

    def GetEnergies(self):
        '''
        Get a list of centre-of-mass energies of the datasets
        '''
        self.Verbose()
        
        tmp = {}
        for d in self.datasets:
            tmp[d.getEnergy()] = 1
        energies = tmp.keys()
        energies.sort()
        return energies

    
    def HasDataset(self, name):
        self.Verbose()        
        return name in self.datasetMap

    
    def GetDataset(self, name):
        '''
        '''
        self.Verbose()
        
        if name in self.datasetMap:
            return self.datasetMap[name]
        else:
            raise Exception("Dataset '%s' could not be found in dataset map!" % (name))        

    
    def GetAllDatasets(self):
        '''
        Get a list of all dataset.Dataset objects.
        '''
        self.Verbose()
        return self.datasets
                

    def GetMCDatasets(self):
        '''
        Get a list of MC dataset.Dataset objects.
        \todo Implementation would be simpler with filter() method
        '''
        self.Verbose()
        
        ret = []
        for d in self.datasets:
            if d.GetIsMC():
                ret.append(d)
        return ret

    
    def GetDataDatasets(self):
        '''
        Get a list of data dataset.Dataset objects.
        
        '''
        self.Verbose()
        
        ret = []
        for d in self.datasets:
            if d.GetIsData():
                ret.append(d)
        return ret

    
    def GetPseudoDatasets(self):
        '''
        Get a list of pseudo dataset.Dataset objects.
        '''
        self.Verbose()
        return filter(lambda d: d.GetIsPseudo(), self.datasets)

    
    def GetAllDatasetNames(self):
        '''
        Get a list of names of all dataset.Dataset objects.
        '''
        self.Verbose()
        return [x.GetName() for x in self.GetAllDatasets()]

    
    def GetMCDatasetNames(self):
        '''
        Get a list of names of MC dataset.Dataset objects."""
        '''
        self.Verbose()
        return [x.GetName() for x in self.GetMCDatasets()]

    
    def GetDataDatasetNames(self):
        '''
        Get a list of names of data dataset.Dataset objects.
        '''
        self.Verbose()
        return [x.GetName() for x in self.GetDataDatasets()]

    
    def GetPseudoDatasetNames(self):
        '''
        Get a list of names of pseudo dataset.Dataset objects.
        '''
        self.Verbose()
        return [x.GetName() for x in self.GetPseudoDatasets()]

    
    def SelectAndReorder(self, nameList):
        '''
        Select and reorder Datasets.
        
        \param nameList   Ordered list of Dataset names to select
        
        This method can be used to either select a set of
        dataset.Dataset objects. reorder them, or both.
        '''
        self.Verbose()
        selected = []
        for name in nameList:
            try:
                selected.append(self.datasetMap[name])
            except KeyError:
                print >> sys.stderr, "=== dataset.py:\n\tWARNING! Dataset selectAndReorder: dataset %s doesn't exist" % name

        self.datasets = selected
        self._PopulateMap()
        return

    
    def Remove(self, nameList, close=True):
        '''
        Remove dataset.Dataset objects
        
        \param nameList    List of dataset.Dataset names to remove

        \param close       If true, close the removed dataset.Dataset objects
        '''
        self.Verbose()
        if isinstance(nameList, basestring):
            nameList = [nameList]

        selected = []
        for d in self.datasets:
            if not d.GetName() in nameList:
                selected.append(d)
            elif close:
                d.Close()
        self.datasets = selected
        self._PopulateMap()
        return

    
    def Rename(self, oldName, newName):
        '''
        Rename a Dataset.
        
        \param oldName   The current name of a dataset.Dataset

        \param newName   The new name of a dataset.Dataset
        '''
        self.Verbose()

        if oldName == newName:
            return

        if newName in self.datasetMap:
            raise Exception("Trying to rename datasets '%s' to '%s', but a dataset with the new name already exists!" % (oldName, newName))
        self.datasetMap[oldName].SetName(newName)
        self._PopulateMap()
        return

    
    def RenameMany(self, nameMap, silent=False):
        '''
        Rename many dataset.Dataset objects
        
        \param nameMap   Dictionary containing oldName->newName mapping

        \param silent    If true, don't raise Exception if source dataset doesn't exist
        
        \see rename()
        '''
        self.Verbose()
        
        # For-loop
        for oldName, newName in nameMap.iteritems():
            if oldName == newName:
                continue

            if newName in self.datasetMap:
                raise Exception("=== dataset.py:\n\tTrying to rename datasets '%s' to '%s', but a dataset with the new name already exists!" % (oldName, newName))

            try:
                self.datasetMap[oldName].SetName(newName)
            except KeyError, e:
                if not silent:
                    raise Exception("=== dataset.py:\n\tTrying to rename dataset '%s' to '%s', but '%s' doesn't exist!" % (oldName, newName, oldName))
        self._PopulateMap()
        return

    
    def MergeData(self, *args, **kwargs):
        '''
        Merge all data dataset.Dataset objects to one with a name 'Data'.
        
        \param args    Positional arguments (forwarded to merge())
        
        \param kwargs  Keyword arguments (forwarded to merge())
        '''
        self.Verbose()

        self.Merge("Data", self.GetDataDatasetNames(), *args, **kwargs)
        return

    
    def MergeMC(self, *args, **kwargs):
        '''
        Merge all MC dataset.Datasetobjects to one with a name 'MC'.
        
        \param args    Positional arguments (forwarded to merge())
         
        \param kwargs  Keyword arguments (forwarded to merge())
        '''
        self.Verbose()
        self.Merge("MC", self.GetMCDatasetNames(), *args, **kwargs)
        return

    
    def MergeMany(self, mapping, *args, **kwargs):
        '''
        Merge datasets according to the mapping.
        
        \param mapping Dictionary of oldName->mergedName mapping. The
                       dataset.Dataset objects having the same mergedName are merged

        \param args    Positional arguments (forwarded to merge())

        \param kwargs  Keyword arguments (forwarded to merge())
        '''
        self.Verbose()
        toMerge = {}

        # For-loop: All datasets
        for d in self.datasets:
            if d.GetName() in mapping:
                newName = mapping[d.GetName()]
                if newName in toMerge:
                    toMerge[newName].append(d.GetName())
                else:
                    toMerge[newName] = [d.GetName()]

        # For-loop
        for newName, nameList in toMerge.iteritems():
            self.Merge(newName, nameList, *args, **kwargs)
        return
    
            
    def Merge(self, newName, nameList, keepSources=False, addition=False, silent=True, allowMissingDatasets=False):
        '''
        Merge dataset.Dataset objects.
        
        \param newName      Name of the merged dataset.DatasetMerged
        
        \param nameList     List of dataset.Dataset names to merge

        \param keepSources  If true, keep the original dataset.Dataset
                            objects in the list of datasets. Otherwise
                            they are removed, as they are now contained
                            in the dataset.DatasetMerged object

        \param addition     Creates DatasetAddedMC instead of DatasetMerged

        \param allowMissingDatasets  If True, ignore error from missing dataset (warning is nevertheless printed)
        
        If nameList translates to only one dataset.Dataset, the
        dataset.Daataset object is renamed (i.e. dataset.DatasetMerged object is not created)
        '''
        print "=== %s: " % (self.__class__.__name__ + "." + sys._getframe(1).f_code.co_name + "()")
        
        (selected, notSelected, firstIndex) = _MergeStackHelper(self.datasets, nameList, "merge", allowMissingDatasets)

        if len(selected) == 0:
            message = "\tNo datasets '" + ", ".join(nameList) + "' found, not doing anything"
            if allowMissingDatasets:
                if not silent:
                    print >> sys.stderr, message
            else:
                raise Exception(message)
            return
        elif len(selected) == 1 and not keepSources:
            message = "\tOne dataset '" + selected[0].GetName() + "' found from list '" + ", ".join(nameList)+"', renaming it to '%s'" % newName            
            if not silent:
                print >> sys.stderr, message
            self.Rename(selected[0].GetName(), newName)
            print "\t\"%s\" successfully created by merging %s datasets:\n\t %s" % (newName, len(nameList), ", ".join(nameList) )
            return

        if not keepSources:
            self.datasets = notSelected
        if addition:
            newDataset = dataset.DatasetAddedMC(newName, selected)
            print "FIXME! Port DatasetAddedMC from tools.dataset to this file. EXIT"
            sys.exit()
        else:
            newDataset = DatasetMerged(newName, selected)

        self.datasets.insert(firstIndex, newDataset)
        self._PopulateMap()
        print "\t\"%s\" successfully created by merging %s datasets:\n\t %s" % (newName, len(nameList), ", ".join(nameList) )
        # print "\t\"%s\" successfully created by merging %s datasets:\n\t %s" % (newName, len(nameList), "\n\t ".join(nameList) )
        return
    
        
    def LoadLuminosities(self, fName="lumi.json"):
        '''
        Load integrated luminosities from a JSON file. The parameter "fName" is the 
        path to the lumi.json file. If the directory part of the path is empty, the file is
        looked from the base directory. The JSON file should be formatted like this:
        
        \verbatim
        '{
           "dataset_name": value_in_pb,
           "Mu_135821-144114": 2.863224758
         }'
        \endverbatim

        NOTE: 
        As setting the integrated luminosity for a merged dataset
        will fail (see dataset.DatasetMerged.setLuminosity()), loading
        luminosities must be done before merging the data datasets to
        one.
        '''
        self.Print("Reading Integrated Luminosities from %s" % fName)
        import json
        
        # Print info
        txtAlign  = "{:<60} {:>10} {:>6}"
        lumiUnits = "(1/pb)"

        for d in self.datasets:
            if d.GetIsMC():
                continue
            
            # Ensure the JSON file exists
            jsonName = os.path.join(d.baseDir, fName)
            if not os.path.exists(jsonName):
                msg = "\t Luminosity JSON file '%s' does not exist. Have you run 'hplusLumiCalc.py' in your multicrab directory?" % jsonName
                raise Exception(msg)
            
            # Assign luminosities to correct datasets
            data      = json.load( open(jsonName) )

            # For-loop: All items in JSON file
            for name, value in data.iteritems():
                if self.HasDataset(name):
                    if self.GetDataset(name).GetLuminosity()==None:
                        self.GetDataset(name).SetLuminosity(value)
                        print "\t", txtAlign.format(name, value, lumiUnits)
                        self.intLumi += value
                    else:
                        pass
                else:
                    msg = "\t Dataset-Manager has not dataset with name \"%s\"" % (name)
                    raise Exception(msg)
                
        print "\t", txtAlign.format("Total", self.intLumi, lumiUnits)
        return

                    
    def GetLuminosity(self):
        '''
        '''
        self.Verbose()
        return self.intLumi

    
    def GetEnergyString(self):
        self.Verbose()
        energy =  "(" + self.energy + " TeV)"
        return energy


    def GetIntLumString(self, units = "fb"):
        self.Verbose()

        unitsFactor = 0
        if units == "fb":
            units       = "fb^{-1}"
            unitsFactor = float(1.0/1000.0)
        elif units == "pb":
            units       = "pb^{-1}"
            unitsFactor = float(1.0)
        else:
            self.Print("Unsupported units options '%s' for luminosity string. Select either 'fb' or 'pb'. EXIT" % (units) )
            sys.exit()

        intLumi = "%0.2f" % (self.intLumi * unitsFactor)
        return intLumi + " " + units
    
    
    def UpdateNAllEventsToPUWeighted(self, **kwargs):
        '''
        Update all event counts to the ones taking into account the pile-up reweighting
        
        \param kwargs     Keyword arguments (forwarded to dataset.Dataset.updateAllEventsToWeighted)
        
        Uses the table pileupReweightedAllEvents._weightedAllEvents
        '''
        self.Verbose()
        
        # For-loop: All datasets
        for dataset in self.datasets:
            dataset.UpdateNAllEventsToPUWeighted(**kwargs) 
        #self.printInfo()
        return


    def SetIntegratedLuminosity(self, intLumi=-1):
        '''
        Set luminosity to all MC samples
        '''
        self.Verbose()

        if intLumi<0:
            intLumi = self.intLumi
        self.Verbose("Setting Integrated Luminosity for all MC samples to %s (1/pb)" % (intLumi) )

        # For-loop: All datasets
        for dataset in self.datasets:
            dataset.SetIntegratedLuminosity(intLumi)
        return
    
    
    def FormatSummary(self):
        '''
        Format dataset information
        '''
        self.Verbose()

        rows   = []
        info   = []
        maxCh  = 30
        align  = "{:<30} {:>12} {:>12} {:>15} {:>12} {:>14} {:>12} {:>12} {:>16}"
        header = align.format("Dataset", "Events", "w-Events", "XSection (pb)", "Lumi (1/pb)", "Norm Factor", "w (Pileup)", "w (Top-Pt)", "Int-Lumi (1/pb)")
        hLine  = "="*len(header)
        info.append(hLine)
        info.append(header)
        info.append(hLine)
        for dataset in self.datasets:
            if dataset.GetIsMC():
                continue
            fullName         = dataset.GetName()
            shortName        = TruncateString(fullName, maxCh)
            xsection         = dataset.GetXSection()
            intLumi          = dataset.GetIntLuminosity()
            lumi             = '%.1f' % ( dataset.GetLuminosity() )
            normFactor       = dataset.GetNormFactor()
            dataVersion      = dataset.GetDataVersion()
            energy           = '%.0f' % ( dataset.GetEnergy())
            allEvents        = '%.1f' % ( dataset.GetAllEvents())
            unweightedEvents = '%.1f' % ( dataset.GetUnweightedEvents() )
            weightedEvents   = '%.1f' % ( dataset.GetWeightedEvents() )
            if dataset.GetPileupWeight()!=None:
                pileupWeight     = '%.2f' % (dataset.GetPileupWeight() )
            else:
                 pileupWeight    = dataset.GetPileupWeight()
            if dataset.GetTopPtWeight()!=None:
                topPtWeight      = '%.2f' % (dataset.GetTopPtWeight() ) 
            else:
                topPtWeight      = dataset.GetTopPtWeight()
            info.append(align.format(shortName, unweightedEvents, allEvents, xsection, lumi, normFactor, pileupWeight, topPtWeight, intLumi))

        for dataset in self.datasets:
            if dataset.GetIsData():
                continue
            fullName         = dataset.GetName()
            shortName        = TruncateString(fullName, maxCh)
            xsection         = dataset.GetXSection()
            intLumi          = dataset.GetIntLuminosity()
            lumi             = '%.1f' % ( dataset.GetLuminosity() )
            normFactor       = '%.8f' % ( dataset.GetNormFactor() )
            dataVersion      = dataset.GetDataVersion()
            energy           = '%.0f' % (dataset.GetEnergy())
            allEvents        = '%.1f' % (dataset.GetAllEvents())
            unweightedEvents = '%.1f' % (dataset.GetUnweightedEvents() )
            weightedEvents   = '%.1f' % (dataset.GetWeightedEvents() )
            if dataset.GetPileupWeight()!=None:
                pileupWeight     = '%.2f' % (dataset.GetPileupWeight() )
            else:
                 pileupWeight    = dataset.GetPileupWeight()
            if dataset.GetTopPtWeight()!=None:
                topPtWeight      = '%.2f' % (dataset.GetTopPtWeight() ) 
            else:
                topPtWeight      = dataset.GetTopPtWeight()
            info.append(align.format(shortName, unweightedEvents, allEvents, xsection, lumi, normFactor, pileupWeight, topPtWeight, intLumi))
        info.append(hLine)
        return info

    
    def PrintSummary(self):
        self.Print()
        for row in self.FormatSummary():
            print "\t", row
        return
    
        
    def PrintDatasets(self):
        '''
        Print dataset information.
        '''
        self.Verbose()
        for dataset in self.datasets:
            dataset.PrintProperties()
        return
        

    def PrintSelections(self, datasetName=None):
        '''
        Prints the parameterSet of some Dataset
        
        Absolutely no guarantees of which Dataset the parameterSet is
        from will not be given.
        '''
        self.Verbose()
        if datasetName == None:
            self.Print("Printing PSet for all datasets")
            for dataset in self.datasets:
                print dataset.GetParameterSet()
        else:
            self.Print("Printing PSet for dataset '%s'" % (datasetName))
            print self.GetDataset(datasetName).GetParameterSet()
        return
    
        
    def GetSelections(self):
        self.Verbose()
        
        namePSets = self.datasets[0].ForEach(lambda d: (d.GetName(), d.GetParameterSet()))
        return namePSets[0][1]
    


#================================================================================================
# Helper Functions
#================================================================================================
def _MergeStackHelper(datasetList, nameList, task, allowMissingDatasets=False):
    '''
    Helper function for merging/stacking a set of datasets.
    
    \param datasetList  List of all Dataset objects to consider
    \param nameList     List of the names of Dataset objects to merge/stack
    \param task         String to identify merge/stack task (can be 'stack' or 'merge')
    \param allowMissingDatasets  If True, ignore error from missing dataset (warning is nevertheless printed)
    
    \return a triple of:
    - list of selected Dataset objects
    - list of non-selected Dataset objects
    - index of the first selected Dataset object in the original list
    of all Datasets
    
    The Datasets to merge/stack are selected from the list of all
    Datasets, and it is checked that all of them are either data or MC
    (i.e. merging/stacking of data and MC datasets is forbidden).
    '''
    if not task in ["stack", "merge"]:
        raise Exception("Task can be either 'stack' or 'merge', was '%s'" % task)

    selected = []
    notSelected = []
    firstIndex = None
    dataCount = 0
    mcCount = 0
    pseudoCount = 0

    for i, d in enumerate(datasetList):
        if d.GetName() in nameList:
            selected.append(d)
            if firstIndex == None:
                firstIndex = i
            if d._IsData():
                dataCount += 1
            elif d._IsMC():
                mcCount += 1
            elif hasattr(d, "isPseudo") and d.isPseudo():
                pseudoCount += 1
            else:
                raise Exception("Internal error!")
        else:
            notSelected.append(d)

    if dataCount > 0 and mcCount > 0:
        raise Exception("Can not %s data and MC datasets!" % task)
    if dataCount > 0 and pseudoCount > 0:
        raise Exception("Can not %s data and pseudo datasets!" % task)
    if pseudoCount > 0 and mcCount > 0:
        raise Exception("Can not %s pseudo and MC datasets!" % task)

    if len(selected) != len(nameList):
        dlist = nameList[:]
        for d in selected:
            ind = dlist.index(d.getName())
            del dlist[ind]
        message = "Tried to %s '"%task + ", ".join(dlist) +"' which don't exist"
        if allowMissingDatasets:
            print >> sys.stderr, "WARNING: "+message
        else:
            raise Exception(message)

    return (selected, notSelected, firstIndex)
    
