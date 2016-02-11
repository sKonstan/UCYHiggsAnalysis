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
import UCYHiggsAnalysis.NtupleAnalysis.pyROOT.aux as aux


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
    def __init__(self, baseDir, name, analysisName, rootFile, verbose = False, **args):
        self.verbose            = verbose
        self.auxObject          = aux.AuxClass(verbose)
        self.name               = name
        self.analysisName       = analysisName
        self.baseDir            = baseDir
        self.latexName          = latexNamesDict[name]
        self.rootFile           = rootFile
        self.drawObject         = None
        self.lumi               = None
        self.normFactor         = None
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
        self.unweightedEvents   = None #self._GetUnweightedEvents() #xenios
        self.weightedEvents     = None #self._GetWeightedEvents() #xenios
        self.isPileupReweighted = self._IsPileUpReweighted()
        self.isTopPtReweighted  = self._IsTopPtReweighted()
        self.pileupWeight       = self._GetPileupWeight()
        self.topPtWeight        = self._GetTopPtWeight()
        self._ReadCounters()
        self.normFactor         = self._GetNormFactor()
        self.Verbose()
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
        

    def _GetUnweightedEvents(self): #xenios
        '''
        '''        
        self.Verbose()
        return -1


    def GetUnweightedEvents(self):
        '''
        '''        
        self.Verbose()
        return self.unweightedEvents
    

    def _GetWeightedEvents(self): #xenios
        '''
        '''        
        self.Verbose()    
        if not self.isMC():
            return

        ratio = 1.0
    
        if self.isPileupReweighted:
            delta = (self.pileupWeight - self.unweightedEvents) / self.unweightedEvents
            ratio = ratio * self.pileupWeight / self.unweightedEvents
            self.Print("Dataset (%s): Updated NAllEvents to pileUpReweighted NAllEvents, change: %0.6f %%" % (self.getName(), delta*100.0) )

        if self.isTopPtReweighted:
            delta = (self.topPtReweighted - self.unweightedEvents) / self.unweightedEvents
            self.Print("Dataset (%s): Updated NAllEvents to isTopPtReweighted NAllEvents, change: %0.6f %%"%(self.getName(), delta*100.0) )
            ratio = ratio * self.topPtWeight / self.unweightedEvents
        weightedEvents = ratio * self.unweightedEvents
        return weightedEvents    


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
        allEvents = self.GetAllEvents()
        causes    = "\n\t1) Counters are weighted"
        causes   += "\n\t2) Analysis job input was a skim"
        causes   += "\n\t3) The method updateNAllEventsToPUWeighted() has not been called"
        if allEvents == 0:
            msg = "Number of all events is '%s' for dataset '%s'! Probable causes:" % (allEvents, self.name)
            raise Exception(msg + causes)
        return self.GetXSection() / allEvents

    

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
            return True
        else:
            raise Exception("The weight '%s' for dataset '%s' is not an instance of float." % (binLabel, self.name) )
        return False

    
    def _GetTopPtWeight(self):
        '''
        '''
        self.Verbose()

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

    
    def SetEnergy(self, energy):
        self.Verbose()
        self.energy   = energy
        self.xsection = xSections.crossSection(self.name, energy)
        return

    def GetEnergy(self):
        self.Verbose()
        return self.energy
        return
    

    def SetLuminosity(self, lumi):
        self.Verbose()
        self.lumi = lumi
        return


    def GetLuminosity(self):
        self.Verbose()
        return self.lumi
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
        
        # Convert the counter histogram (TH1) to a list of (name, count) pairs
        countObject = self.auxObject.ConvertHistoToCounter(counter, self.verbose)

        # Second counter (index 1), second element (index 1) of the tuple [NOTE: First counter is usually zero - underflow bin)
        self.unweightedEvents = countObject[1][1].value()
        self.allEvents        = self.unweightedEvents

        self.Verbose("Successfully read counters in '%s'. Number of events is '%s'" % (counterPath, self.unweightedEvents))
        return

    
    def _ReadWeightedCounters(self):
        '''
        Reads weighted counters, saves values & performs sanity checks
        '''
        self.Verbose()

        counterPath         = self.analysisName + "/counters/weighted/counter"
        (counter, realName) = self.GetRootHisto(counterPath)
        self._CheckCounter(counterPath)
        
        # Convert the counter histogram (TH1) to a list of (name, count) pairs
        countObject = self.auxObject.ConvertHistoToCounter(counter, self.verbose)

        # Second counter (index 1), second element (index 1) of the tuple [NOTE: First counter is usually zero - underflow bin)
        self.weightedEvents = countObject[1][1].value()
        self.allEvents      = self.weightedEvents

        self.Verbose("Successfully read counters in '%s'. Number of events is '%s'" % (counterPath, self.unweightedEvents))
        return


    def _CheckCounter(self, counterPath):
        '''
        Check normalization from weighted counters
        '''
        self.Verbose("Checking couter '%s'" % (counterPath) )
        
        normalisationIsOk   = True
        (counter, realName) = self.GetRootHisto(counterPath)

        # Convert the counter histogram (TH1) to a list of (name, count) pairs
        countObject  = self.auxObject.ConvertHistoToCounter(counter, self.verbose)
        allEventsBin = self._GetBinNumberFromBinLabel(histo=counter, binLabel="Base::AllEvents")

        if counter.GetBinContent(allEventsBin) < counter.GetBinContent(allEventsBin+1):
            normalisationIsOk = False

        if not normalisationIsOk:
            raise Exception("Error: dset=%s: Unweighted skimcounter is smaller than all events counter of analysis!" % self.name)
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
        self.Verbose()
        msg  = "{:<20} {:<20}".format("Name "                   , ": " + self.GetName() + " (" + self.GetLatexName() + ")" )
        msg += "\n\t{:<20} {:<20}".format("Base Directory"      , ": " + self.GetBaseDir() )
        msg += "\n\t{:<20} {:<20}".format("ROOT"                , ": " + self.GetRootFile().GetName() )
        msg += "\n\t{:<20} {:<20}".format("Cross-Section (pb)"  , ": " + str(self.GetXSection()) )
        msg += "\n\t{:<20} {:<20}".format("Energy (TeV)"        , ": " + str(self.GetEnergy()) )
        msg += "\n\t{:<20} {:<20}".format("Luminosity (1/pb)"   , ": " + str(self.GetLuminosity()) )
        msg += "\n\t{:<20} {:<20}".format("Data Version"        , ": " + str(self.GetDataVersion()) )
        msg += "\n\t{:<20} {:<20}".format("Is MC"               , ": " + str(self.GetIsMC()) )
        msg += "\n\t{:<20} {:<20}".format("Is Data"             , ": " + str(self.GetIsData()) )
        msg += "\n\t{:<20} {:<20}".format("Is Pseudo"           , ": " + str(self.GetIsPseudo()) )
        msg += "\n\t{:<20} {:<20}".format("Is PU Reweighted"    , ": " + str(self.GetIsPileupReweighted()) )
        msg += "\n\t{:<20} {:<20}".format("Is TopPt Reweighted" , ": " + str(self.GetIsTopPtReweighted()) )
        msg += "\n\t{:<20} {:<20}".format("Is PU Reweighted"    , ": " + str(self.GetIsPileupReweighted())  + " (" + str(self.GetPileupWeight()) + ")" )
        msg += "\n\t{:<20} {:<20}".format("Is TopPt Reweighted" , ": " + str(self.GetIsTopPtReweighted())   + " (" + str(self.GetTopPtWeight()) + ")" )
    
        if self.GetHisto() != None:
            msg += "\n\t {:<20} {:<20}".format("Histo Name"     , ": " + self.GetHisto().GetName() )
        self.Print(msg)
        return


#================================================================================================ 
# Class Definition
#================================================================================================ 
class DatasetManager:
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
        #self.Print("Appending %s datasets found under directory %s" % (len(datasetNames), baseDir))
        self.Print("Appending %s datasets to the dataset manager:\n\t%s" % (len(datasetNames), datasetNames))
                
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
            d.close()
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
        self._populateMap()
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
                d.close()
        self.datasets = selected
        self._populateMap()
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
        self.datasetMap[oldName].setName(newName)
        self._populateMap()
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
                self.datasetMap[oldName].setName(newName)
            except KeyError, e:
                if not silent:
                    raise Exception("=== dataset.py:\n\tTrying to rename dataset '%s' to '%s', but '%s' doesn't exist!" % (oldName, newName, oldName))
        self._populateMap()
        return

    
    def MergeData(self, *args, **kwargs):
        '''
        Merge all data dataset.Dataset objects to one with a name 'Data'.
        
        \param args    Positional arguments (forwarded to merge())
        
        \param kwargs  Keyword arguments (forwarded to merge())
        '''
        self.Verbose()
        self.merge("Data", self.GetDataDatasetNames(), *args, **kwargs)
        return

    
    def MergeMC(self, *args, **kwargs):
        '''
        Merge all MC dataset.Datasetobjects to one with a name 'MC'.
        
        \param args    Positional arguments (forwarded to merge())
         
        \param kwargs  Keyword arguments (forwarded to merge())
        '''
        self.Verbose()
        self.merge("MC", self.GetMCDatasetNames(), *args, **kwargs)
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
            self.merge(newName, nameList, *args, **kwargs)
        return
    
            
    def Merge(self, newName, nameList, keepSources=False, addition=False, silent=False, allowMissingDatasets=False):
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
        self.Verbose()
        
        (selected, notSelected, firstIndex) = _mergeStackHelper(self.datasets, nameList, "merge", allowMissingDatasets)
        if len(selected) == 0:
            message = "=== dataset.py:\n\tDataset merge: no datasets '" +", ".join(nameList) + "' found, not doing anything"
            if allowMissingDatasets:
                if not silent:
                    print >> sys.stderr, message
            else:
                raise Exception(message)
            return
        elif len(selected) == 1 and not keepSources:
            if not silent:
                print >> sys.stderr, "=== dataset.py:\n\tDataset merge: one dataset '" + selected[0].GetName() + "' found from list '" + ", ".join(nameList)+"', renaming it to '%s'" % newName
            self.rename(selected[0].GetName(), newName)
            return

        if not keepSources:
            self.datasets = notSelected
        if addition:
            newDataset = DatasetAddedMC(newName, selected)
        else:
            newDataset = DatasetMerged(newName, selected)

        self.datasets.insert(firstIndex, newDataset)
        self._populateMap()
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
        self.Verbose()
        import json

        # For-loop: All datasets
        for d in self.datasets:
            jsonName = os.path.join(d.baseDir, fName)
            if not os.path.exists(jsonName):
                msg = "=== dataset.py:\n\tLuminosity JSON file '%s' does not exist. Have you run 'hplusLumiCalc.py' in your multicrab directory?" % jsonname
                raise Exception(msg)
            else:
                data = json.load(open(jsonName))
                for name, value in data.iteritems():
                    if self.HasDataset(name):
                        self.GetDataset(name).SetLuminosity(value)
                        self.intLumi = value

        self.Print("Luminosity is %s (1/pb) (read from %s)" % (self.intLumi, os.path.join(d.baseDir, fName)) )
        return


                    
    def GetLuminosity(self):
        '''
        '''
        self.Verbose()
        return self.intLumi

    
    def GetLuminosityString(self, units = "fb"):
        '''
        '''
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
        #self.printInfo() #xenios
        return


    def SetLuminosityForMC(self, intLumi=-1):
        '''
        Set luminosity to all MC samples
        '''
        self.Verbose()

        if intLumi < 0:
            intLumi = self.intLumi
        self.Print("Setting Luminosity for all MC samples to %s (1/pb)" % (intLumi) )
                   
        # For-loop: All datasets
        for dataset in self.datasets:
            if not dataset.GetIsMC():
                continue
            dataset.SetLuminosity(intLumi)
        return
    
    
    def FormatSummary(self):
        '''
        Format dataset information
        '''
        self.Verbose()

        rows   = []
        info   = []
        align  = "{:^35} {:^10} {:^10} {:^15} {:^15} {:^20} {:>15} {:>15} {:>15}"
        header = align.format("Dataset", "Version", "E (TeV)", "XSection (pb)", "Lumi (1/pb)", "Norm Factor", "Events", "Unweighted", "Weighted")
        hLine  = "="*len(header)
        info.append(hLine)
        info.append(header)
        info.append(hLine)
        for dataset in self.datasets:
            name             = dataset.GetName()
            xsec             = dataset.GetXSection()
            lumi             = dataset.GetLuminosity()
            norm             = dataset.GetNormFactor()
            dataVersion      = dataset.GetDataVersion()
            energy           = dataset.GetEnergy()
            allEvents        = dataset.GetAllEvents()
            unweightedEvents = dataset.GetUnweightedEvents()
            weightedEvents   = dataset.GetWeightedEvents()
            alldEvents       = dataset.GetAllEvents()
            #pileupWeight     = dataset.GetPileupWeight()
            #topPtWeight      = dataset.GetTopPtWeight()
            align  = "{:<35} {:^10} {:^10} {:>15} {:>15} {:>20} {:>15} {:>15} {:>15}"
            line = align.format(name, dataVersion, energy, xsec, lumi, norm, allEvents, unweightedEvents, weightedEvents)
            info.append(line)
        info.append(hLine)
        return info

    
    def PrintSummary(self):
        '''
        Print dataset information.
        '''
        self.Verbose()
        self.PrintList(self.FormatSummary())
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
    
