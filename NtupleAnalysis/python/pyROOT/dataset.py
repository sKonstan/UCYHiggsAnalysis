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
import UCYHiggsAnalysis.NtupleAnalysis.pyROOT.multicrab as multicrab


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
    def __init__(self, baseDir, name, energy, rootFile, intLumi, verbose = False, **args):
        self.verbose     = verbose
        self.name        = name
        self.baseDir     = baseDir
        self.latexName   = latexNamesDict[name]
        self.rootFile    = rootFile
        self.histo       = None
        self.lumi        = intLumi
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


    def SetLuminosity(self, lumi):
        self.Verbose()
        self.lumi = lumi
        return
    
        
    def SetXSection(self, xSection):
        self.Verbose()
        self.xsection = xSection
        return


    def GetLatexName(self):
        return self.latexName

    
    def GetName(self):
        return self.name

    
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


#================================================================================================ 
# Class Definition
#================================================================================================ 
class DatasetManager:
    '''
    Collection of Dataset objects which are managed together.
    
    Holds both an ordered list of Dataset objects, and a name->object
    map for convenient access by dataset name.
    
    '''
    def __init__(self, baseDir, energy, intLumi, verbose=False):
        '''
        The parameter "baseDir" is the (multicrab) directory (absolute or relative to the cwd) 
        where the luminosity JSON file is located (see loadLuminosities())
        
        DatasetManager is constructed as empty
        '''
        self.verbose    = []
        self.intLumi    = -1
        self.datasets   = []
        self.datasetMap = {}
        self.mcrab      = multicrab.Multicrab(verbose)
        self._SetBaseDirectory(baseDir)
        self._AppendDatasets(baseDir, energy, intLumi)
        return
    
        
    def Verbose(self, message=""):
        '''
        Custome made verbose system. Will print all messages in the messageList
        only if the verbosity boolean is set to true.
        '''
        if not self.verbose:
            return
        
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
    

    def _AppendDatasets(self, baseDir, energy, intLumi):
        '''
        '''
        self.Verbose()
        
        datasetNames   = self.mcrab.GetDatasetsFromMulticrabDir(baseDir)
        for dName in datasetNames:
            rootFile       = self.mcrab.GetDatasetRootFile(baseDir, dName)
            datasetObject = Dataset(baseDir, dName, energy, rootFile, self.verbose)
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
            raise Exception("=== dataset.py:\n\t Dataset '%s' already exists in this DatasetManager" % dataset.GetName())

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
        self.Verbose()
        return self.datasetMap[name]

    
    def GetDatasetRootHistos(self, histoName, **kwargs):
        '''
        Get a list of dataset.DatasetRootHisto objects for a given name.
        
        \param histoName   Path to the histogram in each ROOT file.

        \param kwargs      Keyword arguments, forwarder to get
        getDatasetRootHisto() of the contained Dataset objects
    
        \see dataset.Dataset.getDatasetRootHisto()
        '''
        self.Verbose()
        return [d.getDatasetRootHisto(histoName, **kwargs) for d in self.datasets]

    
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
            if d.isMC():
                ret.append(d)
        return ret

    
    def GetDataDatasets(self):
        '''
        Get a list of data dataset.Dataset objects.
        
        \todo Implementation would be simpler with filter() method
        '''
        self.Verbose()
        
        ret = []
        for d in self.datasets:
            if d.isData():
                ret.append(d)
        return ret

    
    def GetPseudoDatasets(self):
        '''
        Get a list of pseudo dataset.Dataset objects.
        '''
        self.Verbose()
        return filter(lambda d: d.isPseudo(), self.datasets)

    
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
                print >> sys.stderr, "=== dataset.py:\n\t WARNING: Dataset selectAndReorder: dataset %s doesn't exist" % name

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
                raise Exception("=== dataset.py:\n\t Trying to rename datasets '%s' to '%s', but a dataset with the new name already exists!" % (oldName, newName))

            try:
                self.datasetMap[oldName].setName(newName)
            except KeyError, e:
                if not silent:
                    raise Exception("=== dataset.py:\n\t Trying to rename dataset '%s' to '%s', but '%s' doesn't exist!" % (oldName, newName, oldName))
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
            message = "=== dataset.py:\n\t Dataset merge: no datasets '" +", ".join(nameList) + "' found, not doing anything"
            if allowMissingDatasets:
                if not silent:
                    print >> sys.stderr, message
            else:
                raise Exception(message)
            return
        elif len(selected) == 1 and not keepSources:
            if not silent:
                print >> sys.stderr, "=== dataset.py:\n\t Dataset merge: one dataset '" + selected[0].GetName() + "' found from list '" + ", ".join(nameList)+"', renaming it to '%s'" % newName
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

        self.Print("Loading luminosities from %s" % (fName) )

        # For-loop: All datasets
        for d in self.datasets:
            jsonName = os.path.join(d.baseDir, fName)
            if not os.path.exists(jsonName):
                msg = "=== dataset.py:\n\t Luminosity JSON file '%s' does not exist. Have you run 'hplusLumiCalc.py' in your multicrab directory?" % jsonname
                raise Exception(msg)
            else:
                data = json.load(open(jsonName))
                for name, value in data.iteritems():
                    if self.HasDataset(name):
                        self.GetDataset(name).SetLuminosity(value)
                        self.intLumi = value

        self.Print("Luminosity is %s pb" % (self.intLumi) )
        return self.intLumi


                    
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
            dataset.updateNAllEventsToPUWeighted(**kwargs)
        #self.printInfo()
        return

    
    def FormatInfo(self):
        '''
        Format dataset information
        '''
        self.Verbose()
        out = StringIO.StringIO()
        col1hdr = "Dataset"
        col2hdr = "Cross section (pb)"
        col3hdr = "Norm. factor"
        col4hdr = "Int. lumi (pb^-1)" 

        maxlen = max([len(x.GetName()) for x in self.datasets]+[len(col1hdr)])
        c1fmt = "%%-%ds" % (maxlen+2)
        c2fmt = "%%%d.4g" % (len(col2hdr)+2)
        c3fmt = "%%%d.4g" % (len(col3hdr)+2)
        c4fmt = "%%%d.10g" % (len(col4hdr)+2)

        c2skip = " "*(len(col2hdr)+2)
        c3skip = " "*(len(col3hdr)+2)
        c4skip = " "*(len(col4hdr)+2)

        out.write((c1fmt%col1hdr)+"  "+col2hdr+"  "+col3hdr+"  "+col4hdr+"\n")

        # For-loop: All datasets
        for dataset in self.datasets:
            line = (c1fmt % dataset.GetName())
            if dataset.isMC():
                line += c2fmt % dataset.getCrossSection()
                normFactor = dataset.getNormFactor()
                if normFactor != None:
                    line += c3fmt % normFactor
                else:
                    line += c3skip
            else:
                line += c2skip+c3skip + c4fmt%dataset.getLuminosity()
            out.write(line)
            out.write("\n")

        ret = out.getvalue()
        out.close()
        return ret

    
    def PrintInfo(self):
        '''
        Print dataset information.
        '''
        self.Verbose()
        print self.formatInfo()
        return

    
    def FormatDatasetTree(self):
        '''
        '''
        self.Verbose()

        ret = "DatasetManager.datasets = [\n"
        for dataset in self.datasets:
            ret += dataset.formatDatasetTree(indent="  ")
        ret += "]"
        return ret

    
    def PrintDatasetTree(self):
        self.Verbose()
        print self.formatDatasetTree()

        
    def PrintSelections(self):
        '''
        Prints the parameterSet of some Dataset
        
        Absolutely no guarantees of which Dataset the parameterSet is
        from will not be given.
        '''
        self.Verbose()
        
        namePSets = self.datasets[0].forEach(lambda d: (d.GetName(), d.getParameterSet()))
        print "=== dataset.py:\n\t ParameterSet for dataset", namePSets[0][0]
        print namePSets[0][1]
        return
    
        
    def GetSelections(self):
        self.Verbose()
        
        namePSets = self.datasets[0].forEach(lambda d: (d.GetName(), d.getParameterSet()))
        #print "ParameterSet for dataset", namePSets[0][0]
        return namePSets[0][1]
    
