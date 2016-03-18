#!/usr/bin/env python
'''
This script was used ONCE to change the dataVersion of collision-data ROOT files,
which has accidentally found to be 74Xmc instead of 74Xdata.

Kept in repo for potential future use, but has no frequent-use value.
'''

#================================================================================================
# Import modules
#================================================================================================
import os, re
import sys
import glob
import shutil
import subprocess
from optparse import OptionParser
import tarfile

import ROOT
ROOT.gROOT.SetBatch(True)
ROOT.PyConfig.IgnoreCommandLineOptions = True

import UCYHiggsAnalysis.NtupleAnalysis.tools.multicrab as multicrab

#================================================================================================
# Global Variables
#================================================================================================
re_histos         = []
re_se             = re.compile("newPfn =\s*(?P<url>\S+)")
replace_madhatter = ("srm://madhatter.csc.fi:8443/srm/managerv2?SFN=", "root://madhatter.csc.fi:1094")


#================================================================================================
# Function Definitions
#================================================================================================
def AbortScript(keystroke, msg):
    '''
    Give user last chance to abort the script before its execution
    '''
    message = "=== multicrabEdit.py:\n\t %s\n\t Press \"%s\" to abort, any other key to proceed: " % (msg, keystroke)
    response = raw_input(message)
    if (response!= keystroke):
        return
    else:
        print "=== multicrabEdit.py:\n\t EXIT"
        sys.exit()
    return


def histoToDict(histo):
    '''
    '''
    ret = {}
    
    for bin in xrange(1, histo.GetNbinsX()+1):
        ret[histo.GetXaxis().GetBinLabel(bin)] = histo.GetBinContent(bin)    
    return ret


def GetNumOfLinesInFile(fileName):
    '''
    Self explanatory
    '''
    return sum(1 for line in fileName)    


#================================================================================================
# Class Definition    
#================================================================================================
class SanityCheckException(Exception):
    '''
    Check that configInfo/configinfo control bin matches to number of
    input files, in order to monitor a mysterious bug reported by Lauri
    '''
    def __init__(self, message):
        super(SanityCheckException, self).__init__(message)


def sanityCheck(mergedFile, inputFiles):
    '''
    '''
    tfile = ROOT.TFile.Open(mergedFile)
    configinfo = tfile.Get("configInfo/configinfo")
    if configinfo:
	info = histoToDict(configinfo)
        if int(info["control"]) != len(inputFiles):
            raise SanityCheckException("configInfo/configinfo:control = %d, len(inputFiles) = %d" % (int(info["control"]), len(inputFiles)))
    return


def delete(fname,regexp):
    '''
    '''

    fIN = ROOT.TFile.Open(fname,"UPDATE")
    fIN.cd()
    keys = fIN.GetListOfKeys()
    for i in range(len(keys)):
        if keys.At(i):
            keyName = keys.At(i).GetName()
            dir = fIN.GetDirectory(keyName)
            if dir:
                fIN.cd(keyName)
                delFolder(regexp)
                fIN.cd()
    delFolder(regexp)
    fIN.Close()
    return


def pileup(fname, verbose=False):
    '''
    '''

    if not os.path.exists(fname):
        print "=== multicrabEdit.py:\n\t ERROR! Could not find file %s " % (fname)

    # Open file to update it
    fileMode = "UPDATE"
    if verbose:
        print "\t\t Opening file in %s mode" % (fileMode)
    fOUT = ROOT.TFile.Open(fname, fileMode)
    fOUT.cd()
    
    hPU = None

    dataVersion   = fOUT.Get("configInfo/dataVersion")    
    stringToMatch = "data"
    dv_re         = re.compile(stringToMatch)
    match         = dv_re.search(dataVersion.GetTitle())

    if match:
        if verbose:
            print "\t\t Dataset is of type \"%s\". Will add to it Pile-Up histogram" % (dataVersion.GetTitle())
        puFile = os.path.join(os.path.dirname(fname), "PileUp.root")
        if os.path.exists(puFile):
            if verbose:
                print "\t Opening file %s" % (puFile)
            fIN = ROOT.TFile.Open(puFile)
            hPU = fIN.Get("pileup")
        else:
            print "\t PileUp not found in" ,os.path.dirname(fname),", did you run hplusLumiCalc.py?"
    else:
        if verbose:
            print "\t\t Dataset is of type \"%s\". Skipping Pile-Up histogram" % (dataVersion.GetTitle())

    if not hPU == None:
        folder = "configInfo"
        fOUT.cd(folder)
        if verbose:
            print "\t Writing %s/%s to %s" % (folder, hPU.GetName(), puFile)            
        hPU.Write("", ROOT.TObject.kOverwrite)

    # Close file
    fOUT.Close()
    return


def changeDataVersion(fname, verbose=False):
    '''
    root [1] gDirectory->ls()
    TFile *MuonEG_Run2015C_25ns_05Oct2015_v1_246908_260426_25ns_Silver/results/miniAOD2FlatTree-MuonEG_Run2015C_25ns_05Oct2015_v1_246908_260426_25ns_Silver.root
    KEY: TDirectoryFileconfigInfo; configInfo
    KEY: TTreeEvents;

    root [3] configInfo->cd()
    (Bool_t) true
    root [4] gDirectory->ls()
    TDirectoryFile*configInfoconfigInfo
    KEY: TNameddataVersion;74Xmc
    KEY: TH1Fconfiginfo;
    KEY: TH1FSkimCounter;
    KEY: TH1FtopPtWeightAllEvents;1topPtWeightAllEvents
    root [5] 
    '''

    # Open file to update it
    fileMode = "UPDATE"
    print "\t Opening %s file in %s mode" % (fname, fileMode)
    fOUT = ROOT.TFile.Open(fname, fileMode)
    fOUT.cd()

    dataVersion = fOUT.Get("configInfo/dataVersion")    
    if "mc" in dataVersion.GetTitle():
        print "\t 1) The dataVersion=\"\%s\"" % (dataVersion.GetTitle())
        dataVersion.SetTitle("74Xdata")
        fOUT.cd("configInfo")
        dataVersion.Write("", ROOT.TObject.kOverwrite)
        print "\t 2) The dataVersion=\"\%s\"" % (dataVersion.GetTitle())
        fOUT.Close()
    else:
        return
    return


def delFolder(regexp):
    '''
    '''
    keys = ROOT.gDirectory.GetListOfKeys()
    del_re = re.compile(regexp)
    deleted = False
    for i in reversed(range(len(keys))):
        if keys.At(i):
            keyName = keys.At(i).GetName()
            match = del_re.search(keyName)
            if match:
                if not deleted:
                    deleted = True
                else:
                    cycle = keys.At(i).GetCycle()
                    ROOT.gDirectory.Delete(keyName+";%i"%cycle)
    return


def main(opts, args):
    '''
    '''

    # Declare Variables
    multicrabDir = os.getcwd().split("/")    
    crabdirs     = multicrab.getTaskDirectories(opts)
    exit_re      = re.compile("/results/cmsRun_(?P<exitcode>\d+)\.log\.tar\.gz")
    mergedFiles  = []

    # Append regex expressions
    global re_histos
    re_histos.append(re.compile("^output files:.*?(?P<file>%s)" % opts.input))
    re_histos.append(re.compile("^\s+file\s+=\s+(?P<file>%s)" % opts.input))

    print "=== multicrabEdit.py:"
    # For-loop: All CRAB directories
    for iDir, d in enumerate(crabdirs):
        
        if "MuonEG" not in d:
            print "\t Skipping ", d
            continue

        if iDir >0:
            print
        print "\t %s (%s/%s)" % ( multicrabDir[-1] + "/" + d, iDir+1, len(crabdirs) )
        d           = d.replace("/", "")
        files = glob.glob(os.path.join(d, "results", "miniAOD2FlatTree*.root"))

        # For loop: All files
        for f in files:
            changeDataVersion(f)

    return 0


if __name__ == "__main__":
    parser = OptionParser(usage="Usage: %prog [options]")
    multicrab.addOptions(parser)

    parser.add_option("-i", dest="input", type="string", default="miniAOD2FlatTree_.*?\.root",
                      help="Regex for input root files (note: remember to escape * and ? !) (default: 'miniAOD2FlatTree_.*?\.root')")
    parser.add_option("-o", dest="output", type="string", default="miniAOD2FlatTree-%s.root",
                      help="Pattern for merged output root files (use '%s' for crab directory name) (default: 'histograms-%s.root')")

    (opts, args) = parser.parse_args()
    sys.exit( main(opts, args) )
