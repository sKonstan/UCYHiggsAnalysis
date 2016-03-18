#================================================================================================ 
# Imports
#================================================================================================ 
import sys
import os
import copy
import glob
import ConfigParser

import ROOT

import UCYHiggsAnalysis.NtupleAnalysis.tools.OrderedDict as OrderedDict
#import UCYHiggsAnalysis.NtupleAnalysis.tools.dataset as dataset
import UCYHiggsAnalysis.NtupleAnalysis.tools.multicrab as multicrab
import UCYHiggsAnalysis.NtupleAnalysis.pyROOT.aux as m_aux

#================================================================================================ 
# Global Definitions
#================================================================================================
_optionDefaults = {
    "input": "histograms-*.root",
    }


#================================================================================================ 
# Class Definition
#================================================================================================ 
class Multicrab(object): 
    '''
    '''
    def __init__(self, verbose=False):
        self.verbose = verbose
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


    def GetDatasetsFromMulticrabDir(self, mcrabDir, **kwargs):
        '''
        '''
        self.Verbose()

        if not isinstance(mcrabDir, str):
            self.Print("Expected argument \"mcrabDir\" as type str, got %s instead. EXIT" % type(mcrabDir))
            sys.exit()

        self.Verbose("Accessing multicrab directory %s" % (mcrabDir))
        if "cfgfile" in kwargs:
            self.Print("This option is still under construction. EXIT")
            sys.exit()
        else:
            return self.GetTaskDirectories(mcrabDir)
        
        return []


    def GetTaskDirectories(self, mcrab):
        '''
        '''
        self.Verbose()

        # Get all items under multicrab directory
        dirsList = glob.glob(os.path.join(mcrab, "*"))

        # Remove from dirs list non-directory items
        dirsList = filter(lambda d: os.path.isdir(d), dirsList)
        
        # Drop the mcrab path from the directories to get the datasets
        datasets = []
        for d in dirsList:
            datasets.append(d.split("/")[-1])

        self.Print("Found %s task directories under %s:\n\t%s" % (len(datasets), mcrab, "\n\t".join(datasets)))
        return datasets


    def GetDatasetRootFile(self, mcrab, dataset, **kwargs):
        '''
        '''
        self.Verbose()

        pathToFile = os.path.join(mcrab, dataset, "res")
        return self.GetRootFile(pathToFile, mode="r")


    def GetRootFile(self, path, mode="r"):
        '''
        Returns a ROOT file object. This is read from the path passed as argument.

        '''
        self.Verbose()

        items    = os.listdir(path)
        rootFile = None
        
        # For-loop: Items under multicrabDir/res (or multicrabDir/results)
        for i in items:

            # Determined if item is a ROOT file
            filePath    = os.path.join(path, i)
            fileName    = filePath.split("/")[-1]
            bIsRootFile = fileName.startswith("histograms-") * fileName.endswith(".root")
            if not bIsRootFile:
                continue
            else:
                rootFile = ROOT.TFile.Open( filePath, mode)            
                self.Verbose("Read ROOT file %s" % filePath)
                break

        self.IsRootFile(rootFile)        
        return rootFile


    def PrintPSet(self, mcrab, dataset, psetPath):
        ''' 
        Print the PSet used when generating a particular ROOT file.
        '''
        self.Verbose()

        rootFile  = self.GetDatasetRootFile(mcrab, dataset)
        named     = rootFile.Get(psetPath)
        psetValue = named.GetTitle()
        msg  = "{:<15} {:<15}".format("Multicrab"     , ": " + mcrab)
        msg += "\n\t{:<15} {:<15}".format("Dataset"   , ": " + dataset)
        msg += "\n\t{:<15} {:<15}".format("PSet Path" , ": " + psetPath)
        msg += "\n\t{:<15} {:<15}".format("PSet Value", ": " + psetValue)
        self.Print(msg)
        return

    
    def PrintKeys(self, mcrab, dataset):
        ''' 
        Prints a the list of keys for the ROOT file passed as argument"
        '''
        self.Verbose()

        rootFile = self.GetDatasetRootFile(mcrab, dataset)
        self.IsRootFile(rootFile)
        self.PrintKeysFromRootFile(rootFile)
        return

    
    def PrintKeysFromRootFile(self, rootFile):
        ''' 
        Prints a the list of keys for the ROOT file passed as argument"
        '''
        self.Verbose()

        self.IsRootFile(rootFile)
        msg   = "Printing list of keys for ROOT file %s" % rootFile.GetName()
        hLine = " "*len(msg)
        self.Print(msg)
        print hLine
        rootFile.GetListOfKeys().Print()
        print hLine
        return

    
    def IsRootFile(self, rootFile):
        '''
        Ensuse that the input file is a ROOT file. 
        '''
        if isinstance(rootFile, ROOT.TFile):
            return
        else:
            msg = "The file %s is not a ROOT file, but of type %s. EXIT" % ( rootFile.GetName(), type(rootFile) ) 
            self.Print(msg)
            sys.exit()
        return
