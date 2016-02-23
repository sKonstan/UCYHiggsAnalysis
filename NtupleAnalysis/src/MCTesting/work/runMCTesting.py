#!/usr/bin/env python
'''
A testing script for running an analysis with registered selector name "MCTesting", as
defined under Testing/src/TestAnalysis.cc. 

The required input is a multiCRAB directory with at least one dataset. If successfull the
script execution will create under Testing/work/analysis_YYMMDD_HHMMSS/ a pseudo multiCRAB
directory structure with the results ROOT files with histograms. These can be later
used as input to plotting scripts to get the desired results.

PROOF:
Enable only if your analysis is CPU-limited (e.g. limit calculation)
Wwith one analyzer at a time most probably you are I/O -limited. 
The limit is how much memory one process is using. Lauri has run optimization runs with
 full systematic (~225 modules simultaneously, which takes 3GB of RAM)
i.e. not possible to use PROOF

The combination of the histograms between the PROOF workers seems to be quite slow
 and I suspect that there is something not quite right with the memory release/garbage
 collection there (i.e. done much more slowly than reasonable). I recommend to test and see what happens
and keep looking out if your machine starts swapping like crazy.

In the call to PROOF, you can specify the number of workers if the default all-in approach is too much:
process.run(proof=True, proofWorkers=3)
where proofWorkes is equivalent to the cores used.

Usage: 
./runMCTesting.py <path-to-multicrab-directory>"

Example:
./runMCTesting.py -m /afs/cern.ch/user/a/attikis/public/multicrab_CMSSW752_Default_07Jan2016/

or

./runMCTesting.py -m /afs/cern.ch/user/a/attikis/public/multicrab_CMSSW752_Default_07Jan2016/ -j 16

The available ROOT options for the Error-Ignore-Level are (const Int_t):
        kUnset    =  -1
        kPrint    =   0
        kInfo     =   1000
        kWarning  =   2000
        kError    =   3000
        kBreak    =   4000
        kSysError =   5000
        kFatal    =   6000

ROOT.gErrorIgnoreLevel = 4000 suppresses "Error in <TCling::RegisterModule>: cannot find dictionary module FrameworkDict_rdict.pcm"
'''
#================================================================================================ 
# Imports
#================================================================================================ 
import sys
from optparse import OptionParser
import ROOT
from UCYHiggsAnalysis.NtupleAnalysis.main import Process, PSet, Analyzer


#================================================================================================ 
# Options
#================================================================================================ 
bVerbose  = False       # Default is "False"
bSilent   = True        # Default is "True"
prefix    = "analysis"  # Default is "analysis"
postfix   = ""          # Default is ""
maxEvts   = -1          # Default is -1
ROOT.gErrorIgnoreLevel = 4000

#================================================================================================ 
# Setup the main function
#================================================================================================ 
def main():
    
    # Setup the process
    process = Process(outputPrefix=prefix, outputPostfix=postfix, maxEvents=maxEvts, verbose=bVerbose)


    # Adding a dataset 
    if len(sys.argv) < 2:
        print "=== runMCTesting:\n\t Not enough arguments passed to script execution. Printing docstring & EXIT."
        print __doc__
        sys.exit(0)

    if bVerbose:
        print "=== runMCTesting.py:\n\t Adding all datasets from multiCRAB directory \"%s\"" % (opts.mcrab)

    if (opts.includeOnlyTasks):
        process.addDatasetsFromMulticrab(opts.mcrab, includeOnlyTasks=opts.includeOnlyTasks)
    elif (opts.excludeTasks):
        process.addDatasetsFromMulticrab(opts.mcrab, excludeTasks=opts.excludeTasks)
    else: #all datasets
        process.addDatasetsFromMulticrab(opts.mcrab)


    # Add Configuration Attributes
    print "=== runMCTesting.py:\n\t Loading & Customising cfg parameters from \".kinematicsParameters\""
    from UCYHiggsAnalysis.NtupleAnalysis.parameters.kinematicsParameters import allSelections
    allSelections.__setattr__("ElePtCutMin" ,  7.0)
    allSelections.__setattr__("EleEtaCutMax",  2.5) 
    allSelections.__setattr__("MuPtCutMin"  ,  5.0)
    allSelections.__setattr__("MuEtaCutMax" ,  2.4)
    allSelections.__setattr__("BjetPtCutMin", 25.0)
    allSelections.__setattr__("BjetPtCutMax",  2.5)
    allSelections.__setattr__("LeptonTriggerPtCutMin", [20, 10])

    # Add Analysis Variations
    selections = allSelections.clone()
    process.addAnalyzer("MCTesting", Analyzer("MCTesting", config=selections, silent=bSilent) )
        
    # Pick events
    # process.addOptions(EventSaver = PSet(enabled = True,pickEvents = True))

    # Run the analysis with PROOF? By default it uses all cores, but you can give proofWorkers=<N> as a parameter
    if opts.jCores:
        print "=== runMCTesting:\n\t Running process with PROOF (proofWorkes=%s)" % ( str(opts.jCores) )
        process.run(proof=True, proofWorkers=opts.jCores)  # process.run(proof=True)
    else:
        print "=== runMCTesting:\n\t Running process (no PROOF)"
        process.run()

#================================================================================================
if __name__ == "__main__":
    
    parser = OptionParser(usage="Usage: %prog [options]" , add_help_option=False,conflict_handler="resolve")
    parser.add_option("-m", "--mcrab"   , dest="mcrab"   , action="store", help="Path to the multicrab directory for input")
    parser.add_option("-j", "--jCores"  , dest="jCores"  , action="store", type=int, help="Number of CPU cores (PROOF workes) to use. Default is all available.")
    parser.add_option("-i", "--includeOnlyTasks", dest="includeOnlyTasks", action="store", help="List of datasets in mcrab to include")
    parser.add_option("-e", "--excludeTasks", dest="excludeTasks", action="store", help="List of datasets in mcrab to exclude")
    (opts, args) = parser.parse_args()

    if opts.mcrab == None:
        raise Exception("Please provide input multicrab directory with -m")

    main()
#================================================================================================    
