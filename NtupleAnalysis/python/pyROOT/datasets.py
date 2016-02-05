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

#import UCYHiggsAnalysis.NtupleAnalysis.pyROOT.multicrab as m_multicrab


#================================================================================================
# Class Definition
#================================================================================================
class Dataset(object):
    def __init__(self, name, rootFile, verbose = False, **args):
        self.bVerbose    = verbose
        self.name        = name
        self.rootFile    = rootFile
        self.args        = args
        self.Verbose()
        return


    def Verbose(self, messageList=None):
        '''
        Custome made verbose system. Will print all messages in the messageList
        only if the verbosity boolean is set to true.
        '''
        if self.bVerbose == True:
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


    def _SetDefaults(self, dataset, CMSSW, PileUp, Events, Geometry, TaskDir, TaskSubDir, **kwargs):
        '''
        '''
        self.Verbose()

        ### Remove upper-case dependence
        dataset = dataset.lower()

        self.DatasetToPileUpMap[dataset]   = PileUp
        self.DatasetToGeometryMap[dataset] = Geometry
        if self.MulticrabDirPath !=None:
            self.DatasetToTaskDirMap[dataset]  = self.MulticrabDirPath + TaskDir
            self.DatasetToFileMap[dataset]     = self.MulticrabDirPath + TaskDir + TaskSubDir + "output-" + TaskDir + ".root"
        self.DatasetToEventsMap[dataset]   = Events
        self.DatasetToCmsswMap[dataset]    = CMSSW

        ### Set all arguments and their values
        for argument, value in kwargs.iteritems():
            setattr(self, name + "_" + argument, value)
        return


    def GetDatasetList(self):
        '''
        Return a list with the dataset names found under the multicrab directory self.mcrab
        '''
        return self.datasetList

    
#    def GetPileUp(self, dataset):
#        '''
#        '''
#        self.Verbose()
#
#        ### Remove upper-case dependence
#        dataset = dataset.lower()
#        return self.DatasetToPileUpMap[dataset]
