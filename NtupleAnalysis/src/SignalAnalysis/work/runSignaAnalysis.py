#!/usr/bin/env python
''' 
INSTRUCTIONS:
The required minimum input is a multiCRAB directory with at least one dataset. If successfull 
a pseudo multiCRAB with name "analysis_YYMMDD_HHMMSS/" will be created, inside which each
dataset has its own directory with the results (ROOT files with histograms). These can be later
used as input to plotting scripts to get the desired results.

PROOF:
Enable only if your analysis is CPU-limited (e.g. limit calculation) With one analyzer at
a time most probably you are I/O -limited. The limit is how much memory one process is using. 
                                                                                                                                                                                  
USAGE:
./runKinematics.py -m <path-to-multicrab-directory> -j <numOfCores> -i <DatasetName>

Example:
./runSignalAnalysis.py -m /afs/cern.ch/user/a/attikis/public/multicrab_CMSSW752_Default_07Jan2016/
or                                                                                                                                                                                  
./runKinematics.py -m /afs/cern.ch/user/a/attikis/public/multicrab_CMSSW752_Default_07Jan2016/ -j 16

ROOT:
The available ROOT options for the Error-Ignore-Level are (const Int_t):
        kUnset    =  -1
        kPrint    =   0
        kInfo     =   1000
        kWarning  =   2000
        kError    =   3000
        kBreak    =   4000
'''

#================================================================================================
#Imports
#================================================================================================
import sys
from optparse import OptionParser

from UCYHiggsAnalysis.NtupleAnalysis.main import Process, PSet, Analyzer
from UCYHiggsAnalysis.NtupleAnalysis.parameters.signalAnalysisParameters import allSelections
from UCYHiggsAnalysis.NtupleAnalysis.parameters.ttbarAnalysisParameters import ttbarSelections
from UCYHiggsAnalysis.NtupleAnalysis.AnalysisBuilder import AnalysisBuilder

import ROOT


#================================================================================================
# Options
#================================================================================================
prefix      = "SignalAnalysis"
postfix     = ""
dataEras    = ["2015D"]
searchModes = ["mH125"]
ROOT.gErrorIgnoreLevel = 0


#================================================================================================
# Function Definition
#================================================================================================
def Verbose(msg, printHeader=False):
    if not opts.verbose:
        return

    if printHeader:
        print "=== runSignalAnalysis.py:"

    if msg !="":
        print "\t", msg
    return


def Print(msg, printHeader=True):
    if printHeader:
        print "=== runSignalAnalysis.py:"

    if msg !="":
        print "\t", msg
    return


#================================================================================================
# Setup the main function 
#================================================================================================
def main():


    # Setup the process
    process = Process(prefix, postfix, opts.maxEvts, opts.verbose)

    # Require at least two arguments (script-name, path to multicrab)
    if len(sys.argv) < 2:
        Print("Not enough arguments passed to script execution. Printing docstring & EXIT.")
        print __doc__
        sys.exit(0)

    if (opts.includeOnlyTasks):
        Print("Adding only dataset %s from multiCRAB directory %s" % (opts.includeOnlyTasks, opts.mcrab) )
        process.addDatasetsFromMulticrab(opts.mcrab, includeOnlyTasks=opts.includeOnlyTasks)
    elif (opts.excludeTasks):
        Print("Adding all datasets except %s from multiCRAB directory %s" % (opts.excludeTasks, opts.mcrab) )
        Print("If collision data are present, then vertex reweighting is done according to the chosen data era (era=2015C, 2015D, 2015) etc...")
        process.addDatasetsFromMulticrab(opts.mcrab, excludeTasks=opts.excludeTasks)
    else:
        Print("Adding all datasets from multiCRAB directory %s" % (opts.mcrab) )
        Print("If collision data are present, then vertex reweighting is done according to the chosen data era (era=2015C, 2015D, 2015) etc...")
        process.addDatasetsFromMulticrab(opts.mcrab)

    # ================================================================================================
    # Selection customisations
    # ================================================================================================
    # allSelections.CommonPlots.histogramSplitting = [
    #     PSet(label="tauPt", binLowEdges=[60.0, 70.0, 80.0, 100.0], useAbsoluteValues=False),
    #     ]
    # allSelections.TauSelection.rtau = 0.0
    # allSelections.BJetSelection.numberOfBJetsCutValue = 0
    # allSelections.BJetSelection.numberOfBJetsCutDirection = "=="


    # ================================================================================================
    # Command Line Options
    # ================================================================================================
    # applyAnalysisCommandLineOptions(sys.argv, allSelections)


    # ================================================================================================
    # Build analysis modules
    # ================================================================================================
    builder = AnalysisBuilder("SignalAnalysis", 
                              dataEras,
                              searchModes,
                              usePUreweighting=True,
                              doSystematicVariations=False
                              )


    # ================================================================================================
    # Variations for optimisation
    # ================================================================================================
    # builder.addVariation("METSelection.METCutValue", [100,120,140])
    # builder.addVariation("AngularCutsBackToBack.workingPoint", ["Loose","Medium","Tight"])
    
    # builder.build(process, allSelections)
    builder.build(process, ttbarSelections)

    # ================================================================================================
    # Pick events
    # ================================================================================================
    # process.addOptions(EventSaver = PSet(enabled = True,pickEvents = True))
    

    # ================================================================================================
    # Run the analysis
    # ================================================================================================
    # Run the analysis with PROOF? By default it uses all cores, but you can give proofWorkers=<N> as a parameter
    if opts.jCores:
        Print("Running process with PROOF (proofWorkes=%s)" % ( str(opts.jCores) ) )
        process.run(proof=True, proofWorkers=opts.jCores)
    else:
        Print("Running process (no PROOF)")
        process.run()


#================================================================================================
if __name__ == "__main__":
    parser = OptionParser(usage="Usage: %prog [options]" , add_help_option=False,conflict_handler="resolve")
    parser.add_option("-m", "--mcrab"   , dest="mcrab"   , action="store", help="Path to the multicrab directory for input")
    parser.add_option("-j", "--jCores"  , dest="jCores"  , action="store", type=int, help="Number of CPU cores (PROOF workes) to use. Default is all available.")
    parser.add_option("-i", "--includeOnlyTasks", dest="includeOnlyTasks", action="store", help="List of datasets in mcrab to include")
    parser.add_option("-e", "--excludeTasks"    , dest="excludeTasks"    , action="store", help="List of datasets in mcrab to exclude")
    parser.add_option("-v", "--verbose"         , dest="verbose"         , action="store_true", default = False , help="Enable verbosity (for debugging reasons)")
    parser.add_option("--maxEvts", dest="maxEvts", type=int, default = -1, action="store", help="Maximum number of events to run on") 
    (opts, args) = parser.parse_args()                                                                                                                                              

    if opts.mcrab == None:
        raise Exception("Please provide input multicrab directory with -m")
    main()
#================================================================================================
