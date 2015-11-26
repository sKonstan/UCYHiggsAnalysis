import FWCore.ParameterSet.VarParsing as VarParsing
from HiggsAnalysis.MiniAOD2FlatTree.tools.dataVersion import DataVersion
import sys

# Set global variables
bDebug = False 
validSampleValues = [
    "WJets",
    "W1Jets",
    "W2Jets",
    "W3Jets",
    "W4Jets",
    "TTJets",
]


def getOptions(options=None, bDebug=True):
    '''
    Module for returning options that can be passed from the command line as arguments to cmsRun command.

    For more details see:
    https://twiki.cern.ch/twiki/bin/view/CMSPublic/SWGuideAboutPythonConfigFile#Passing_Command_Line_Arguments_T

    cmsRun runMiniAOD2FlatTree_cfg.py \dataVersion=74X_dataRun2_Prompt_v4
    '''
    print "=== dataOptions.py:\n\t Registering predefined default values for options"

    if options == None:
        options = VarParsing.VarParsing()

    # Set default options. These can be overwritten from the command line when launching cmsRun.
    options.register("crossSection",
                     -1.0, # default value
                     options.multiplicity.singleton, # singleton or list
                     options.varType.float,          # string, int, or float
                     "Cross section of the dataset stored to histograms ROOT file (default: \"-1.0\"")

    options.register("luminosity",
                     -1.0, # default value
                     options.multiplicity.singleton, # singleton or list
                     options.varType.float,          # string, int, or float
                     "Integrated luminosity of the dataset stored to histograms ROOT file (default: \"-1.0\"")

    options.register("dataVersion",
                     "",
                     options.multiplicity.singleton, # singleton or list
                     options.varType.string,         # string, int, or float
                     "Data version (default: \"\"")

    options.register("trigger",
                     [],
                     options.multiplicity.list, options.varType.string,
                     "Triggers to use logical OR if multiple given (default: \"[]\"")

    options.register("someList",
                     [],
                     options.multiplicity.list, options.varType.string,
                     "Example list (default: \"[]\"")

    options.register("anotherList",
                     [],
                     options.multiplicity.list, options.varType.string,
                     "Another example list (default: \"[]\"")

    options.register("doHLTMatching",
                     1,
                     options.multiplicity.singleton,
                     options.varType.int,
                     "Do HLT trigger matching? (default: \"1\")")

    options.register("triggerThrow",
                     1,
                     options.multiplicity.singleton,
                     options.varType.int,
                     "Should the TriggerFilter for data throw if trigger path is not found? (default: \"1\")")

    options.register("triggerMC",
                     0,
                     options.multiplicity.singleton,
                     options.varType.int,
                     "Should MC be triggered? (default: \"0\")")

    options.register("runOnCrab",
                     0,
                     options.multiplicity.singleton,
                     options.varType.int,
                     "Set to 1 if job will be run with crab. Typically you don't have to set it by yourself, since it is set in crab.cfg/multicrab.cfg (default: \"0\"")

    options.register("energy",
                     0,
                     options.multiplicity.singleton,
                     options.varType.int, # Use integer for now, if we later need e.g. 12.5 TeV, let's use string then
                     "Centre-of-mass energy in TeV (default: \"0\"")

    options.register("sample",
                     "",
                     options.multiplicity.singleton,
                     options.varType.string,
                     "Sample name for specific weighting schemes. Valid values are: " + ", ".join(validSampleValues) + " (default: \"\")")
    
    if (bDebug):
        print "=== dataOptions.py:\n\t options:\n", options

    # Protection in case sys.argv is missing due to various edm tools
    if not hasattr(sys, "argv"):
        return options

    # Hack to be able to pass multiple arguments from multicrab.cfg
    if len(sys.argv) > 0:
        last = sys.argv.pop()
        sys.argv.extend(last.split(":"))

    # Get and parse the command line arguments
    options.parseArguments()

    if options.sample != "" and options.sample not in validSampleValues:
        raise Exception("Invalid value '%s' of 'sample' command line parameter, valid values are %s" % (options.sample, ", ".join(validSampleValues)))

    return options


def getOptionsDataVersion(dataVersion, options=None, useDefaultSignalTrigger=True):
    '''
    Module returns values for options related to the data version selected. 
    Uses information from the auxiliary file DataVersion.py
    '''
    print "=== dataOptions.py:\n\tSetting values to dataVersion related options"
    
    # First get default options
    options = getOptions(options)

    # Check that dataversion is not the default (empt string) value
    if options.dataVersion != "":
        dataVersion = options.dataVersion

    # Initialise dataVersion object
    dataVersion = DataVersion(dataVersion)

    # Set the trigger depending on the dataset version & type (MC or Data)
    if useDefaultSignalTrigger and len(options.trigger) == 0 and dataVersion.isMC():
        options.trigger = [dataVersion.getDefaultSignalTrigger()]

    return (options, dataVersion)
