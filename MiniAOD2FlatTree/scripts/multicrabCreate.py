#!/usr/bin/env python
'''
Usage: 
multicrabcreate.py [multicrab-dir-to-be-resubmitted]

Description:
This script is used to launch multicrab jobs, with certain customisable options.
The file datasets.py is used an an auxiliary file to determine the samples to be processesed.

Launching the command with a multicrab-dir as a parameter:
[username@lxp lus0036:test]$ multicrabCreate.py <multicrab_dir>
resubmits some crab tasks within the multicrab dir. 

Links:
https://twiki.cern.ch/twiki/bin/view/CMSPublic/CRAB3ConfigurationFile
https://twiki.cern.ch/twiki/bin/view/CMSPublic/WorkBookCRAB3Tutorial#Setup_the_environment
'''

#================================================================================================
# Import modules
#================================================================================================
import os
import re
import sys
import time
from optparse import OptionParser
import UCYHiggsAnalysis.MiniAOD2FlatTree.tools.git as git

#from datasets import *
from UCYHiggsAnalysis.MiniAOD2FlatTree.tools.datasets import *


#================================================================================================
# Function Definitions
#================================================================================================
def GetCmsswVersion(verbose=False):
    '''
    Get a command-line-friendly format of the CMSSW version currently use.
    https://docs.python.org/2/howto/regex.html
    '''
    
    if verbose:
        print "=== multicrabCreate.py:\n\t GetCmsswVersion()"

    # Get the current working directory
    pwd = os.getcwd()

    # Create a compiled regular expression object 
    cmssw_re = re.compile("/CMSSW_(?P<version>\S+?)/")

    # Scan through the string 'pwd' & look for any location where the compiled RE 'cmssw_re' matches
    match = cmssw_re.search(pwd)
    
    version = ""
    if match:
        # Return the string matched by the RE. Convert to desirable format
        version = match.group("version")
        version = version.replace("_","")
        version = version.replace("pre","p")
        version = version.replace("patch","p")        
    return version
        
    
def GetSkimType(PSet, verbose=False):
    '''
    Get the skim type according to the name of the PSET file used.
    This will be used to setup the multicrab job accordingly.
    '''
    if verbose:
        print "=== multicrabCreate.py:\n\t GetSkimType()"

    # Create a compiled regular expression object 
    skim_re = re.compile("runMiniAOD2FlatTree_(?P<skimType>\S+)Skim_cfg.py")
    
    # Scan through the string 'PSet' & look for any location where the compiled RE 'skim_re' matches 
    match = skim_re.search(PSet)

    skimType = ""
    if match:
        skimType = match.group("skimType")
    else:
        print "=== multicrabCreate.py:\n\t Could not determine the skim type for PSet \"%s\". EXIT." % (PSet)
        sys.exit()

    return skimType


def GetDatasetList(skimType, verbose=False):
    '''
    Get the list of datasets to be processed according to the skim type (and hance PSET file used).
    This will be used to setup the multicrab job accordingly.
    '''
    if verbose:
        print "=== multicrabCreate.py:\n\t GetDatasetList()"

    datasetList = []
    myDatasets  = Datasets(False)

    if skimType == "Default":        
        datasetList  = myDatasets.GetDatasetObjects(miniAODversion="RunIISpring15MiniAODv2", datasetType = opts.datasetType)
    else:
        print "=== multicrabCreate.py:\n\t Unknown skim type '%s'." % (skimType), ". EXIT"
        sys.exit()

    return datasetList

    
def GetTaskDirName(datasetList, skimType, version, verbose=False):
    '''
    Get the name of the CRAB task directory to be created. For the user's benefit this
    will include the CMSSW uversion, the skim type and possibly important information from
    the dataset used, such as the bunch-crossing time.
    '''
    if verbose:
        print "=== multicrabCreate.py:\n\t GetTaskDirName()"

    # Constuct basic task directory name
    taskDirName  = "multicrab"
    taskDirName += "_CMSSW" + version
    taskDirName += "_"  + skimType

    # Add dataset-specific info, like bunch-crossing 
    bx_re = re.compile("\S+(?P<bx>\d\dns)_\S+")
    match = bx_re.search(datasetList[0].DAS)
    if match:
        taskDirName+= "_" + match.group("bx")

    # Append the creation time to the task directory name
    taskDirName+= "_" + time.strftime("%d%b%Y_%Hh%Mm%Ss")

    # Overwrite task dir name by user input? Check script execution command
    if len(sys.argv) == 2 and os.path.exists(sys.argv[1]) and os.path.isdir(sys.argv[1]):
        taskDirName = sys.argv[1]
    else:
        taskDirName = taskDirName
    
    return taskDirName


def CreateCrabTask(taskDirName, verbose=False):
    '''
    Creates a directory which will be used as the CRAB task directory.
    Also copies all available information from git regarding the current status of the code, 
    including the unique "commit id", "git diff" and "git status".   
    '''
    if verbose:
        print "=== multicrabCreate.py:\n\t CreateCrabTask()"

    # If the task directory does not exist create it
    if not os.path.exists(taskDirName):
        os.mkdir(taskDirName)
    else:
        if verbose:
            print "=== multicrabCreate.py:\n\t Created CRAB task directory \"%s\"" % (taskDirName)

    if verbose:
        print "=== multicrabCreate.py:\n\t Created CRAB task directory \"%s\"" % (taskDirName)
    else:
        return
        
        
    # Copy file to be used (and others to be tracked) to the task directory
    cmd = "cp %s %s" %(PSET, taskDirName)
    os.system(cmd)

    # Write the commit id, "git status", "git diff" command output the directory created for the multicrab task.
    gitFileList = git.writeCodeGitInfo(taskDirName, False)

    if verbose:
        print "=== multicrabCreate.py:\n\t Copied %s to '%s'." % ("'" + "', '".join(gitFileList) + "'", taskDirName)
    return


def GetRequestName(dataset):
    '''
    Return the file name and path to an (empty) crabConfig_*.py file where "*" 
    contains the dataset name and other information such as tune, COM, Run number etc..
    of the Data or MC sample used.
    '''

    # Create compiled regular expression objects
    tune_re        = re.compile("(?P<name>\S+)_Tune")
    tev_re         = re.compile("(?P<name>\S+)_13TeV")
    runRange_re    = re.compile("Cert_(?P<RunRange>\d+-\d+)_13TeV_PromptReco_Collisions15(?P<BunchSpacing>\S*)_JSON(?P<Silver>(_\S+|))\.")
    datadataset_re = re.compile("^/(?P<name>\S+?)/(?P<run>Run\S+?)/")
    mcdataset_re   = re.compile("^/(?P<name>\S+?)/")
    
    # Scan through the string 'dataset.DAS' & look for any location where the compiled RE 'mcdataset_re' matches
    match = mcdataset_re.search(dataset.DAS)
    if dataset.isData():
	match = datadataset_re.search(dataset.DAS)
    if match:
        # Append the dataset name
        requestName = match.group("name")

        # Append the Run number (for Data samples only)
        if dataset.isData():
            requestName += "_"
            requestName += match.group("run")

        # Append the MC-tune (for MC samples only)
        #requestName = match.group("name")
        tune_match  = tune_re.search(requestName)
        if tune_match:
	    requestName = tune_match.group("name")

        # Append the COM Energy (for MC samples only)
        tev_match = tev_re.search(requestName)
        if tev_match:
            requestName = tev_match.group("name")

        # Append the Run Range (for Data samples only)
        if dataset.isData():
            runRangeMatch = runRange_re.search(dataset.lumiMask)
	    if runRangeMatch:
	        runRange           = runRangeMatch.group("RunRange")
	        runRange           = runRange.replace("-","_")
	        bunchSpacing       = runRangeMatch.group("BunchSpacing")
	        requestName += "_"+ runRange + bunchSpacing
                Ag                 = runRangeMatch.group("Silver") #Ag is symbol for chemical element of silver
                if Ag == "_Silver":
                    requestName += Ag
    else:
        raise Exception("=== multicrabCreate.py:\n\t Unexpected error for dataset '%s'. It must either be data or MC" %dataset)

    # Finally, replace dashes with underscores 
    requestName = requestName.replace("-","_")
    return requestName


def EnsurePathDoesNotExit(taskDirName, requestName):
    '''
    Ensures that file does not already exist
    '''
    filePath = os.path.join(taskDirName, requestName)
    
    if not os.path.exists(filePath):
        return
    else:
        raise Exception("=== multicrabCreate.py:\n\t File '%s' already exists!" % (filePath) )

    return


def CreateCfgFile(dataset, taskDirName, requestName, infilePath = "crabConfig.py", verbose=False):
    '''
    Creates a CRAB-specific configuration file which will be used in the submission
    of a job. The function uses as input a generic cfg file which is then customised
    based on the dataset type used.
    '''
    if verbose:
        print "=== multicrabCreate.py:\n\t CreateCfgFile()"

    outfilePath = os.path.join(taskDirName, "crabConfig_" + requestName + ".py")

    # Check that file does not already exist
    EnsurePathDoesNotExit(taskDirName, outfilePath)
    
    # Open input file (read mode) and output file (write mode)
    fileIN  = open(infilePath , "r")
    fileOUT = open(outfilePath, "w")
    
    # For each CRAB cfg-file field create a compiled regular expression object 
    crab_requestName_re = re.compile( "config.General.requestName" )
    crab_workArea_re    = re.compile( "config.General.workArea"    )
    crab_pset_re        = re.compile( "config.JobType.psetName"    )
    crab_psetParams_re  = re.compile( "config.JobType.pyCfgParams" )
    crab_dataset_re     = re.compile( "config.Data.inputDataset"   )
    crab_split_re       = re.compile( "config.Data.splitting"      )
    crab_splitunits_re  = re.compile( "config.Data.unitsPerJob"    )
    crab_dbs_re         = re.compile( "config.Data.inputDBS"       )

    # For-loop: All line of input fine
    for line in fileIN:

        # Skip lines whicha are commented out
        if line[0] == "#":
            continue

        # Set the "inputDataset" field which specifies the name of the dataset. Can be official CMS dataset or a dataset produced by a user.
        match = crab_dataset_re.search(line)
        if match:
            line = "config.Data.inputDataset = '" + dataset.DAS + "'\n"

        # Set the "requestName" field which specifies the request/task name. Used by CRAB to create a project directory (named crab_<requestName>)
        match = crab_requestName_re.search(line)
        if match:
            line = "config.General.requestName = '" + requestName + "'\n"

        # Set the "workArea" field which specifies the (full or relative path) where to create the CRAB project directory. 
        match = crab_workArea_re.search(line)
        if match:
            line = "config.General.workArea = '" + taskDirName + "'\n"

        # Set the "psetName" field which specifies the name of the CMSSW pset_cfg.py file that will be run via cmsRun.
        match = crab_pset_re.search(line)
        if match:
            line = "config.JobType.psetName = '" + PSET + "'\n"

        # Set the "pyCfgParams" field which contains list of parameters to pass to the pset_cfg.py file.
        match = crab_psetParams_re.search(line)
        if match:
            line = "config.JobType.pyCfgParams = ['dataVersion=" + dataset.dataVersion + "']\n"

        # Set the "inputDBS" field which specifies the URL of the DBS reader instance where the input dataset is published
        match = crab_dbs_re.search(line)
        if match:
            line = "config.Data.inputDBS = '"+dataset.DBS+"'\n"

        # Only if dataset is real data
        if dataset.isData():
    
            # Set the "splitting" field which specifies the mode to use to split the task in jobs ('FileBased', 'LumiBased', or 'EventAwareLumiBased')
            match = crab_split_re.search(line)
            if match:
                line  = "config.Data.splitting = 'LumiBased'\n"
                line += "config.Data.lumiMask = '" + dataset.lumiMask + "'\n"
            
            # Set the "unitsPerJob" field which suggests (but not impose) how many files, lumi sections or events to include in each job.
            match = crab_splitunits_re.search(line) 
            if match:
                line = "config.Data.unitsPerJob = 100\n"
        else:
            pass

        # Write line to the output file
        fileOUT.write(line)
            
    # Close input and output files
    fileOUT.close()
    fileIN.close()

    if verbose:
        print "=== multicrabCreate.py:\n\t Created CRAB cfg file \"%s\"" % (fileOUT.name)
    return


def SubmitCrabTask(taskDirName, requestName, verbose=False):
    '''
    Submit a given CRAB task using the specific cfg file.
    '''
    if verbose:
        print "=== multicrabCreate.py:\n\t SubmitCrabTask()"

    outfilePath = os.path.join(taskDirName, "crabConfig_" + requestName + ".py")

    # Submit the CRAB task
    cmd_submit = "crab submit " + outfilePath
    if verbose:
        print "=== multicrabCreate.py:\n\t ", cmd_submit
    os.system(cmd_submit)

    # Rename the CRAB task directory (remove "crab_" from its name)
    cmd_mv = "mv " + os.path.join(taskDirName, "crab_" + requestName) + " " + os.path.join(taskDirName, requestName)
    if verbose:
        print "=== multicrabCreate.py:\n\t ", cmd_mv
    os.system(cmd_mv)

    # Call 'crab status' command for taskDirNme/requestName 
    #import time
    #time.sleep(1)
    #cmd_status = "crab status --dir=" + os.path.join(taskDirName, requestName)
    #print "=== multicrabCreate.py:\n\t ", cmd_status
    #os.system(cmd_status)
    return


def AbortCrabTask(keystroke):
    '''
    Give user last chance to abort CRAB task creation.
    '''
    message  =  "=== multicrabCreate.py:\n\t Press \"%s\" to abort, any other key to proceed: " % (keystroke)

    response = raw_input(message)
    if (response!= keystroke):
        return
    else:
        print "=== multicrabCreate.py:\n\t EXIT"
        sys.exit()
    return


def AskToContinue(datasetList, verbose=False):
    '''
    '''
    if verbose:
        print "=== multicrabCreate.py:\n\t AskToContinue()"

    msg  = "\n\t Creating CRAB task with PSet:\n\t\t %s" % (PSET)
    msg += "\n\t The following datasets will be used:\n\t\t%s" % ("\n\t\t".join(str(d.DAS) for d in datasetList))
    print "=== multicrabCreate.py:%s" % (msg)
    AbortCrabTask(keystroke="q")
    return


#================================================================================================
# Options & Declaration
#================================================================================================
PSET     = "runMiniAOD2FlatTree_DefaultSkim_cfg.py"


#================================================================================================
# Main Program
#================================================================================================
def main(opts, args):
    
    # Get the CMSSW version
    version = GetCmsswVersion(opts.verbose)
    
    # Get the Skim type
    skimType = GetSkimType(PSET, opts.verbose)

    # Get the datasets
    datasetList = GetDatasetList(skimType, opts.verbose)

    # Give user last chance to abort
    AskToContinue(datasetList, opts.verbose)

    # Get the task directory name
    if opts.taskDirName=="":
        taskDirName = GetTaskDirName(datasetList, skimType, version, opts.verbose)
    else:
        taskDirName = opts.taskDirName

    # Create CRAB task diractory
    CreateCrabTask(taskDirName)

    # For-loop: All datasets
    for dataset in datasetList:

        if opts.verbose:
            print "=== multicrabCreate.py:\n\t Getting request name, creating cfg file && submitting CRAB task for dataset \"%s\"" % (dataset)

        # Create CRAB configuration file for each dataset
        requestName = GetRequestName(dataset)
    
        # Create a CRAB cfg file for each dataset
        CreateCfgFile(dataset, taskDirName, requestName, "crabConfig.py", opts.verbose)

        # Sumbit job for CRAB cfg file            
        SubmitCrabTask(taskDirName, requestName, opts.verbose)

    return 0


if __name__ == "__main__":
    '''
    https://docs.python.org/3/library/argparse.html

    name or flags...: Either a name or a list of option strings, e.g. foo or -f, --foo.
    action..........: The basic type of action to be taken when this argument is encountered at the command line.
    nargs...........: The number of command-line arguments that should be consumed.
    const...........: A constant value required by some action and nargs selections.
    default.........: The value produced if the argument is absent from the command line.
    type............: The type to which the command-line argument should be converted.
    choices.........: A container of the allowable values for the argument.
    required........: Whether or not the command-line option may be omitted (optionals only).
    help............: A brief description of what the argument does.
    metavar.........: A name for the argument in usage messages.
    dest............: The name of the attribute to be added to the object returned by parse_args().
    '''

    parser = OptionParser(usage="Usage: %prog [options]")
    parser.add_option("-v", "--verbose", dest="verbose"    , default=False, action="store_true", help="Verbose mode")

    parser.add_option("-d", "--dir", dest="taskDirName", type="string", default="", help="Custom name for multiCRAB directory name")

    parser.add_option("-t", "--datasetType", dest="datasetType", type="string", default="", help="The type/group of datasets to run on. Currently the available types/groups are: \"All\", \"Data\", \"MC\".")

    (opts, args) = parser.parse_args()

    if opts.datasetType == "":
        print "=== multicrabCreate.py:\n\t ERROR! The script was executed without definining the dataset type/group to use. Retry using the following syntax:"
        print "\t\t multicrabCreate.py --datasetType=\"SelectedMC\" [or any other supported datasetType]" 
        print "\t For help execute the script with the \"help\" option:"
        print "\t\t multicrabCreate.py --help"
        sys.exit()

    sys.exit( main(opts, args) )
