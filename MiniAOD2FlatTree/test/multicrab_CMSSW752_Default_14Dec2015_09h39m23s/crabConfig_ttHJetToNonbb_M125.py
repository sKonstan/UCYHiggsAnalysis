from WMCore.Configuration import Configuration
from CRABClient.UserUtilities import getUsernameFromSiteDB

config = Configuration()

config.section_("General")
config.General.requestName = 'ttHJetToNonbb_M125'
config.General.workArea = 'multicrab_CMSSW752_Default_14Dec2015_09h39m23s'
config.General.transferOutputs = True
config.General.transferLogs    = True

config.section_("JobType")
config.JobType.pluginName  = 'Analysis'
config.JobType.psetName = 'runMiniAOD2FlatTree_DefaultSkim_cfg.py'
config.JobType.pyCfgParams = ['dataVersion=74Xmc']
config.JobType.outputFiles = ['miniAOD2FlatTree.root']

config.section_("Data")
config.Data.inputDataset = '/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM'
config.Data.inputDBS = 'global'
config.Data.splitting     = 'FileBased'
config.Data.unitsPerJob   = 5
config.Data.publication   = False
config.Data.outLFNDirBase = '/store/user/%s/' % (getUsernameFromSiteDB())
config.Data.totalUnits    = 100000                # equivalnet to <Events> when "EventAwareLumiBased" is used
config.Data.splitting     = "EventAwareLumiBased" # testing. please comment this and "config.Data.totalUnits" out

config.section_("Site")
config.Site.storageSite   = 'T2_CH_CERN' 


