#!/usr/bin/env python

from UCYHiggsAnalysis.NtupleAnalysis.main import Process, PSet, Analyzer

# Example of adding an analyzer whose configuration depends on dataVersion
def createAnalyzer(dataVersion):
    a = Analyzer("ExampleAnalysis")
    if dataVersion.isMC():
        a.tauPtCut = 10
    else:
        a.tauPtCut = 20
    return a

process = Process()

# Example of adding a dataset which has its files defined in data/<dataset_name>.txt file
#process.addDatasets(["DoubleMuon"])
#process.addDatasets(["TTbar_HBWB_HToTauNu_M_160_13TeV_pythia6"])

# Example of adding datasets from a multicrab directory
import sys
if len(sys.argv) != 2:
    print "Usage: ./exampleAnalysis.py <path-to-multicrab-directory>"
    sys.exit(0)
process.addDatasetsFromMulticrab(sys.argv[1])

# Example of adding an analyzer
#process.addAnalyzer("test", 
#                    Analyzer("ExampleAnalysis", tauPtCut = 10)
#                    )

#process.addAnalyzer("test", createAnalyzer)
process.addAnalyzer("ExampleAnalysis", createAnalyzer)

# Run the analysis
process.run()

# Run the analysis with PROOF
# By default it uses all cores, but you can give proofWorkers=<N> as a parameter
#process.run(proof=True)
