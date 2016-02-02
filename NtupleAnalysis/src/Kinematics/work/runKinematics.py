#!/usr/bin/env python
'''
A testing script for running an analysis with registered selector name "Kinematics", as
defined under Testing/src/TestAnalysis.cc. 

The required input is a multiCRAB directory with at least one dataset. If successfull the
script execution will create under Testing/work/analysis_YYMMDD_HHMMSS/ a pseudo multiCRAB
directory structure with the results ROOT files with histograms. These can be later
used as input to plotting scripts to get the desired results.

Usage: 
./runKinematics.py <path-to-multicrab-directory>"

Example:
./runKinematics.py /afs/cern.ch/user/a/attikis/public/multicrab_CMSSW752_Default_07Jan2016/
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
    print "=== runKinematics:\n\t Not enough arguments passed to script execution. Printing docstring & EXIT."
    print __doc__
    sys.exit(0)
else:
    if bVerbose:
        print "=== runKinematics.py:\n\t Adding all datasets from multiCRAB directory \"%s\"" % (sys.argv[1])
    process.addDatasetsFromMulticrab(sys.argv[1])


#================================================================================================ 
# Add Configuration Attributes
#================================================================================================ 
print "=== runKinematics.py:\n\t Loading & Customising cfg parameters from \".kinematicsParameters\""
from UCYHiggsAnalysis.NtupleAnalysis.parameters.kinematicsParameters import allSelections
allSelections.__setattr__("ElePtCutMin" ,  7.0)
allSelections.__setattr__("EleEtaCutMax",  2.5) 
allSelections.__setattr__("MuPtCutMin"  ,  5.0)
allSelections.__setattr__("MuEtaCutMax" ,  2.4)
allSelections.__setattr__("BjetPtCutMin", 25.0)
allSelections.__setattr__("BjetPtCutMax",  2.5)
allSelections.__setattr__("LeptonTriggerPtCutMin", [20, 10])


#================================================================================================ 
# Add Analysis Variations
#================================================================================================ 
selections = allSelections.clone()
process.addAnalyzer("Kinematics", Analyzer("Kinematics", config=selections, silent=bSilent) )
        

#================================================================================================ 
# Pick events
#================================================================================================ 
# process.addOptions(EventSaver = PSet(enabled = True,pickEvents = True))


#================================================================================================ 
# Run the analysis
#================================================================================================ 
# Run the analysis with PROOF? By default it uses all cores, but you can give proofWorkers=<N> as a parameter
if bVerbose:
        print "=== runKinematics:\n\t Running the process ..." 
if "proof" in sys.argv:
    process.run(proof=True)
else:
    process.run()

#print "=== runKinematics:\n\t DONE"
