#!/usr/bin/env python
'''
A testing script for running an analysis with registered selector name "TestAnalysis", as
defined under Testing/src/TestAnalysis.cc. 

The required input is a multiCRAB directory with at least one dataset. If successfull the
script execution will create under Testing/work/analysis_YYMMDD_HHMMSS/ a pseudo multiCRAB
directory structure with the results ROOT files with histograms. These can be later
used as input to plotting scripts to get the desired results.

Usage: 
./testAnalysis.py <path-to-multicrab-directory>"

Example:
./testAnalysis.py /afs/cern.ch/user/a/attikis/public/multicrab_CMSSW752_Default_07Jan2016_testNEW/
'''

#================================================================================================ 
# Imports
#================================================================================================ 
import sys
from UCYHiggsAnalysis.NtupleAnalysis.main import Process, PSet, Analyzer

#================================================================================================ 
# Setup the process
#================================================================================================ 
process = Process()


#================================================================================================ 
# Adding a dataset 
#================================================================================================ 
if len(sys.argv) < 2:
    print "=== testAnalysis:\n\t Not enough arguments passed to script execution. Printing docstring & EXIT."
    print __doc__
    sys.exit(0)
else:
    print "=== testAnalysis.py:\n\t Adding all datasets from multiCRAB directory \"%s\"" % (sys.argv[1])
    process.addDatasetsFromMulticrab(sys.argv[1])
    #sys.exit(0)


#================================================================================================ 
# Add Configuration Attributes
#================================================================================================ 
from UCYHiggsAnalysis.NtupleAnalysis.parameters.signalAnalysisParameters import allSelections
allSelections.TauSelection.rtau = 0.0 # Disable rtau
allSelections.__setattr__("jetPtCutMin" ,    20.0 )
allSelections.__setattr__("jetPtCutMax" , 99999.0 )
allSelections.__setattr__("jetEtaCutMin",   -2.5  )
allSelections.__setattr__("jetEtaCutMax",    2.5  )


#================================================================================================ 
# Add Analysis Variations
#================================================================================================ 
# For-loop: All b-tag discriminators
for algo in ["pfCombinedInclusiveSecondaryVertexV2BJetTags"]:
    print "=== testAnalysis.py:\n\t Adding algorithm \"%s\"" % (algo)
    
    # For-loop: All working points
    for wp in ["Loose", "Medium", "Tight"]:
        selections = allSelections.clone()
        selections.BJetSelection.bjetDiscr = algo
        selections.BJetSelection.bjetDiscrWorkingPoint = wp
        suffix = "_%s_%s" % (algo, wp)

        print "=== testAnalysis.py:\n\t Adding analyzer \"%s\" for working point \"%s\"" % (algo, wp)
        process.addAnalyzer("Test" + suffix, Analyzer("TestAnalysis", config=selections, silent=False) )
        #sys.exit()
        

#================================================================================================ 
# Example of adding an analyzer whose configuration depends on dataVersion
#================================================================================================ 
'''
def createAnalyzer(dataVersion):
    a = Analyzer("ExampleAnalysis")
    if dataVersion.isMC():
        a.tauPtCut = 10
    else:
        a.tauPtCut = 20
    return a
process.addAnalyzer("test2", createAnalyzer)
'''


#================================================================================================ 
# Pick events
#================================================================================================ 
#process.addOptions(EventSaver = PSet(enabled = True,pickEvents = True))


#================================================================================================ 
# Run the analysis
#================================================================================================ 
# Run the analysis with PROOF? By default it uses all cores, but you can give proofWorkers=<N> as a parameter
if "proof" in sys.argv:
    process.run(proof=True)
else:
    process.run()
