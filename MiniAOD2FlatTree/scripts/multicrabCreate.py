#!/usr/bin/env python
'''
Usage: 
multicrabcreate.py [multicrab-dir-to-be-resubmitted]

Description:
This script is used to launch multicrab jobs, with certain customisable options.
The file datasets.py is used an an auxiliary file to determine the samples to be processesed.

Launching the command with a multicrab-dir as a parameter:
[username@lxplus0036:test]$ multicrabCreate.py <multicrab_dir>
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
import UCYHiggsAnalysis.MiniAOD2FlatTree.tools.git as git

#from datasets import *
from UCYHiggsAnalysis.MiniAOD2FlatTree.tools.datasets import *


#================================================================================================
# Function Definitions
#================================================================================================
def GetCmsswVersion():
    '''
    Get a command-line-friendly format of the CMSSW version currently use.
    https://docs.python.org/2/howto/regex.html
    '''

    # Get the current working directory
    pwd = os.getcwd()

    # Create a compiled regular expression object 
    cmssw_re = re.compile("/CMSSW_(?P<version>\S+?)/")

    # Scan through the string 'pwd' & look for any location where the compiled RE 'cmssw_re' matches
    match = cmssw_re.search(pwd)
    
    version = ""
    if match:
        # Return the string matched by the RE
        version = match.group("version")

        # Convert to desirable format
        version = version.replace("_","")
        version = version.replace("pre","p")
        version = version.replace("patch","p")
        
    return version
        
    
def GetSkimType(PSet):
    '''
    Get the skim type according to the name of the PSET file used.
    This will be used to setup the multicrab job accordingly.
    '''

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

    print "=== multicrabCreate.py:\n\t Will create CRAB task using PSet \"%s\"." % (PSet)
    return skimType


def GetDatasetList(skimType):
    '''
    Get the list of datasets to be processed according to the skim type (and hance PSET file used).
    This will be used to setup the multicrab job accordingly.
    '''
    datasetList = []
    myDatasets  = Datasets(False)
    
    if skimType == "Default":        
        datasetList  = myDatasets.GetDatasetObjects(miniAODversion="RunIISpring15MiniAODv2", datasetType = "CollisionData")
        #datasetList.append(myDatasets.GetDatasetObject("/MuonEG/Run2015D-PromptReco-v4/MINIAOD"))
        #datasetList = [myDatasets.GetDatasetObject("/DoubleMuon/Run2015D-PromptReco-v4/MINIAOD")]
        #datasetList.append(myDatasets.GetDatasetObject('/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM'))
        #datasetList.append(myDatasets.GetDatasetObject('/TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v3/MINIAODSIM'))
        #datasetList.append(myDatasets.GetDatasetObject('/WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM'))

        #datasetList = myDatasets.GetDatasetObjects(miniAODversion="RunIISpring15MiniAODv2")        

        # testing
#        dataList = ['/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM',
#                    '/TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v3/MINIAODSIM',
#                    #'/ST_tW_top_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v2/MINIAODSIM',
#                    #'/ST_t-channel_top_4f_leptonDecays_13TeV-powheg-pythia8_TuneCUETP8M1/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM',
#                    #'/ST_s-channel_4f_leptonDecays_13TeV-amcatnlo-pythia8_TuneCUETP8M1/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM',
#                    '/DYJetsToLL_M-10to50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM',
#                    '/WW_TuneCUETP8M1_13TeV-pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM',
#                    '/WZ_TuneCUETP8M1_13TeV-pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM',
#                    '/ZZ_TuneCUETP8M1_13TeV-pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM',
#                    '/WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM',
#                    ]
#        datasetList = []
#        for d in dataList: 
#            datasetList.append(myDatasets.GetDatasetObject(d))
    else:
        print "=== multicrabCreate.py:\n\t Unknown skim type '%s'." % (skimType), ". EXIT"
        sys.exit()

    print "=== multicrabCreate.py:\n\t Creating CRAB Tasks for the following datasets:\n\t\t", "\n\t\t".join(str(d.DAS) for d in datasetList)
    return datasetList

    
def GetTaskDirName(datasetList, skimType, version):
    '''
    Get the name of the CRAB task directory to be created. For the user's benefit this
    will include the CMSSW uversion, the skim type and possibly important information from
    the dataset used, such as the bunch-crossing time.
    '''

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


def CreateCrabTask(taskDirName):
    '''
    Creates a directory which will be used as the CRAB task directory.
    Also copies all available information from git regarding the current status of the code, 
    including the unique "commit id", "git diff" and "git status".   
    '''
    # If the task directory does not exist create it
    if not os.path.exists(taskDirName):
        os.mkdir(taskDirName)
    print "=== multicrabCreate.py:\n\t Created CRAB task directory \"%s\"" % (taskDirName)
        
    # Copy file to be used (and others to be tracked) to the task directory
    cmd = "cp %s %s" %(PSET, taskDirName)
    os.system(cmd)

    # Write the commit id, "git status", "git diff" command output the directory created for the multicrab task.
    gitFileList = git.writeCodeGitInfo(taskDirName, False)
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
        requestName = match.group("name")
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


def CreateCfgFile(dataset, taskDirName, requestName, infilePath = "crabConfig.py"):
    '''
    Creates a CRAB-specific configuration file which will be used in the submission
    of a job. The function uses as input a generic cfg file which is then customised
    based on the dataset type used.
    '''
    
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
        print "dataset.dataVersion = ", dataset.dataVersion
        import sys
        sys.exit()

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
    print "=== multicrabCreate.py:\n\t Created CRAB cfg file \"%s\"" % (fileOUT.name)

    return


def SubmitCrabTask(taskDirName, requestName):
    '''
    Submit a given CRAB task using the specific cfg file.
    '''
    outfilePath = os.path.join(taskDirName, "crabConfig_" + requestName + ".py")

    # Submit the CRAB task
    cmd_submit = "crab submit " + outfilePath
    print "=== multicrabCreate.py:\n\t ", cmd_submit
    os.system(cmd_submit)

    # Rename the CRAB task directory (remove "crab_" from its name)
    cmd_mv = "mv " + os.path.join(taskDirName, "crab_" + requestName) + " " + os.path.join(taskDirName, requestName)
    print "=== multicrabCreate.py:\n\t ", cmd_mv
    os.system(cmd_mv)

    # Small hack. By calling 'crab status' for all tasks prevents it from crashing when calling 'crab status' once the
    # jobs are submitted. This is caused because I RENAME the CRAB tasks with the previous command "os.system(cmd_mv)". 
    import time
    time.sleep(1)
    cmd_status = "crab status --dir=" + os.path.join(taskDirName, requestName)
    print "=== multicrabCreate.py:\n\t ", cmd_status
    os.system(cmd_status)

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


#================================================================================================
# Options & Declaration
#================================================================================================
PSET     = "runMiniAOD2FlatTree_DefaultSkim_cfg.py"
skimType = "Default"

# Get the CMSSW Version
version = GetCmsswVersion()
 
# Get the Skim type
skimType = GetSkimType(PSET)

# Get the datasets
datasetList = GetDatasetList(skimType)

# Give user last chance to abort
AbortCrabTask(keystroke="q")

# Get the task directory name
taskDirName = GetTaskDirName(datasetList, skimType, version)

# Create CRAB task diractory
CreateCrabTask(taskDirName)

# For-loop: All datasets
for dataset in datasetList:

    # Create CRAB configuration file for each dataset
    requestName = GetRequestName(dataset)
    
    # Create a CRAB cfg file for each dataset
    CreateCfgFile(dataset, taskDirName, requestName)

    # Sumbit job for CRAB cfg file            
    SubmitCrabTask(taskDirName, requestName)
