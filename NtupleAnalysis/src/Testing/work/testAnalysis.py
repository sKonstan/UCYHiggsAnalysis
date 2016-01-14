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
# Options
#================================================================================================ 
bVerbose  = False       # Default is "False"
bSilent   = True        # Default is "True"
prefix    = "analysis"  # Default is "analysis"
postfix   = ""          # Default is ""
maxEvts   = -1          # Default is -1


#================================================================================================ 
# Setup the process
#================================================================================================ 
process = Process(outputPrefix=prefix, outputPostfix=postfix, maxEvents=maxEvts, verbose=bVerbose)


#================================================================================================ 
# Adding a dataset 
#================================================================================================ 
if len(sys.argv) < 2:
    print "=== testAnalysis:\n\t Not enough arguments passed to script execution. Printing docstring & EXIT."
    print __doc__
    sys.exit(0)
else:
    if bVerbose:
        print "=== testAnalysis.py:\n\t Adding all datasets from multiCRAB directory \"%s\"" % (sys.argv[1])
    process.addDatasetsFromMulticrab(sys.argv[1])


#================================================================================================ 
# Add Configuration Attributes
#================================================================================================ 
print "=== testAnalysis.py:\n\t Loading & Customising cfg parameters from \".signalAnalysisParameters\""
from UCYHiggsAnalysis.NtupleAnalysis.parameters.signalAnalysisParameters import allSelections

# Trigger
allSelections.Trigger.triggerOR = ["HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_vx",
                                   "HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ_vx",
                                   "HLT_IsoMu20_vx",
                                   "HLT_IsoTkMu20_vx",
                                   "HLT_Ele17_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_vx",
                                   "HLT_Ele23_WPLoose_Gsf_vx",
                                   "HLT_Ele23_CaloIdL_TrackIdL_IsoVL_vx", #MC
                                   "HLT_Mu17_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_vx",
                                   "HLT_Mu8_TrkIsoVVL_Ele17_CaloIdL_TrackIdL_IsoVL_vx",
                                   "HLT_DiMu9_Ele9_CaloIdL_TrackIdL_vx",
                                   "HLT_Mu8_DiEle12_CaloIdL_TrackIdL_vx",
                                   "HLT_TripleMu_12_10_5_vx",
                                   "HLT_Ele16_Ele12_Ele8_CaloIdL_TrackIdL_vx",
                               ]
allSelections.__setattr__("jetPtCutMin" ,    20.0 )
allSelections.__setattr__("jetPtCutMax" , 99999.0 )
allSelections.__setattr__("jetEtaCutMin",   -2.5  )
allSelections.__setattr__("jetEtaCutMax",    2.5  )


#================================================================================================ 
# Add Analysis Variations
#================================================================================================ 
# For-loop: All b-tag discriminators
print "=== testAnalysis.py:"
for algo in ["pfCombinedInclusiveSecondaryVertexV2BJetTags"]:
    
    # For-loop: All working points
    for wp in ["Loose", "Medium", "Tight"]:
    #for wp in ["Loose"]:
        selections = allSelections.clone()
        selections.BJetSelection.bjetDiscr = algo
        selections.BJetSelection.bjetDiscrWorkingPoint = wp
        suffix = "_%s_%s" % (algo, wp)

        #if bVerbose:
        print "\t Adding algorithm \"%s\" for working point \"%s\"" % (algo, wp)
        process.addAnalyzer("Test" + suffix, Analyzer("TestAnalysis", config=selections, silent=bSilent) )
        

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
# process.addOptions(EventSaver = PSet(enabled = True,pickEvents = True))


#================================================================================================ 
# Run the analysis
#================================================================================================ 
# Run the analysis with PROOF? By default it uses all cores, but you can give proofWorkers=<N> as a parameter
if bVerbose:
        print "=== testAnalysis:\n\t Running the process ..." 
if "proof" in sys.argv:
    process.run(proof=True)
else:
    process.run()

print "=== testAnalysis:\n\t DONE"
