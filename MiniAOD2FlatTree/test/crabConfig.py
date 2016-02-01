'''
Links:
https://twiki.cern.ch/twiki/bin/view/CMSPublic/CRAB3ConfigurationFile
https://twiki.cern.ch/twiki/bin/view/CMSPublic/WorkBookCRAB3Tutorial#Setup_the_environment
'''

#================================================================================================
# Import Modules
#================================================================================================
from WMCore.Configuration import Configuration
# See https://github.com/dmwm/CRABClient/blob/master/src/python/CRABClient/ClientUtilities.py
from CRABClient.UserUtilities import getUsernameFromSiteDB
#from CRABClient.UserUtilities import getWorkArea


#================================================================================================
# General Section: The user specifies generic parameters about the request (e.g. request name).
#================================================================================================
config = Configuration()

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
config.Data.inputDBS      = 'global'    # 'phys03'
config.Data.splitting     = 'LumiBased' # EventBased, FileBased, LumiBased (1 lumi ~= 300 events)
config.Data.unitsPerJob   = 5
config.Data.publication   = False
config.Data.outLFNDirBase = '/store/user/%s/' % (getUsernameFromSiteDB())
config.Data.totalUnits    = -1
### MC: How many files (when Data.splitting='FileBased'), lumi sections (when Data.splitting='LumiBased') or events (when Data.splitting='EventAwareLumiBased') to analyze
#config.Data.splitting     = "EventAwareLumiBased"  # Used with "config.Data.totalUnits"
#config.Data.totalUnits    = 100000                 # Used with "config.Data.splitting"
#config.Data.unitsPerJob   = 5000

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
