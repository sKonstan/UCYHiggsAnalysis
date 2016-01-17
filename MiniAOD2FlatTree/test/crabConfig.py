from WMCore.Configuration import Configuration
# See https://github.com/dmwm/CRABClient/blob/master/src/python/CRABClient/ClientUtilities.py
from CRABClient.UserUtilities import getUsernameFromSiteDB
#from CRABClient.UserUtilities import getWorkArea

config = Configuration()

#================================================================================================
# General Section: The user specifies generic parameters about the request (e.g. request name).
#================================================================================================
config.section_("General")
config.General.requestName     = rName
config.General.workArea        = dirName
config.General.transferOutputs = True
config.General.transferLogs    = True
#config.General.failureLimit
#config.General.instance
#config.General.activity

#================================================================================================
# JobType Section: Contains all the parameters of the user job type and related configurables
#================================================================================================
config.section_("JobType")
config.JobType.pluginName  = 'Analysis'
config.JobType.psetName    = 'runMiniAOD2FlatTree_cfg.py'
config.JobType.pyCfgParams = ''
config.JobType.outputFiles = ['miniAOD2FlatTree.root']
# config.JobType.generator
# config.JobType.inputFiles
# config.JobType.disableAutomaticOutputCollection
# config.JobType.eventsPerLumi
# config.JobType.allowUndistributedCMSSW
# config.JobType.maxMemoryMB
# config.JobType.maxJobRuntimeMin
# config.JobType.numCores
# config.JobType.priority
# config.JobType.scriptExe
# config.JobType.scriptArgs
# config.JobType.sendPythonFolde
# config.JobType.externalPluginFile

#================================================================================================
# Data Section: Contains all parameters related to the data to be analyzed (incl. splitting params)
#================================================================================================
config.section_("Data")
config.Data.inputDataset  = dataset
config.Data.inputDBS      = 'global' #'phys03'
config.Data.splitting     = 'FileBased'
config.Data.unitsPerJob   = 5
config.Data.publication   = False
config.Data.outLFNDirBase = '/store/user/%s/' % (getUsernameFromSiteDB())
config.Data.totalUnits    = 100000 #-1
#config.Data.splitting     = "EventAwareLumiBased" # testing. please comment this and "config.Data.totalUnits" out
# config.Data.allowNonValidInputDatase
# config.Data.outputPrimaryDataset
# config.Data.inputDBS
# config.Data.unitsPerJob
# config.Data.useParent
# config.Data.secondaryInputDataset
# config.Data.lumiMask
# config.Data.runRange
# config.Data.outLFNDirBase
# config.Data.publication
# config.Data.publishDBS
# config.Data.outputDatasetTag
# config.Data.publishWithGroupName
# config.Data.ignoreLocality
# config.Data.userInputFiles

#================================================================================================
# Site Section: Contains the Grid site parameters (incl. stage out information)
#================================================================================================
config.section_("Site")
config.Site.storageSite = 'T2_CH_CERN' 
config.Site.blacklist   = ['T2_US_Florida'] #suspicious
# config.Site.whitelist = ['T2_CH_CERN', 'T2_FI_HIP']



#================================================================================================
# Debug Section: For experts use only
#================================================================================================
# config.section_("Debug")
# config.Debug.oneEventMode = True
# config.Debug.ASOURL       = ''
# config.Debug.scheddName   = ''
# config.Debug.extraJDL     = ''
# config.Debug.collector    = ''
