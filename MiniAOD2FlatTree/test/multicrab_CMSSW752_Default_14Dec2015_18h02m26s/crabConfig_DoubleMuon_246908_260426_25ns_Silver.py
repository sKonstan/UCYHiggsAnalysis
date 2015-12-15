from WMCore.Configuration import Configuration
from CRABClient.UserUtilities import getUsernameFromSiteDB

config = Configuration()

config.section_("General")
config.General.requestName = 'DoubleMuon_246908_260426_25ns_Silver'
config.General.workArea = 'multicrab_CMSSW752_Default_14Dec2015_18h02m26s'
config.General.transferOutputs = True
config.General.transferLogs    = True

config.section_("JobType")
config.JobType.pluginName  = 'Analysis'
config.JobType.psetName = 'runMiniAOD2FlatTree_DefaultSkim_cfg.py'
config.JobType.pyCfgParams = ['dataVersion=74Xdata']
config.JobType.outputFiles = ['miniAOD2FlatTree.root']

config.section_("Data")
config.Data.inputDataset = '/DoubleMuon/Run2015D-PromptReco-v4/MINIAOD'
config.Data.inputDBS = 'global'
config.Data.splitting = 'LumiBased'
config.Data.lumiMask = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions15/13TeV/Cert_246908-260426_13TeV_PromptReco_Collisions15_25ns_JSON_Silver.txt'
config.Data.unitsPerJob = 100
config.Data.publication   = False
config.Data.outLFNDirBase = '/store/user/%s/' % (getUsernameFromSiteDB())
config.Data.totalUnits    = 100000                # equivalnet to <Events> when "EventAwareLumiBased" is used
config.Data.splitting = 'LumiBased'
config.Data.lumiMask = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions15/13TeV/Cert_246908-260426_13TeV_PromptReco_Collisions15_25ns_JSON_Silver.txt'

config.section_("Site")
config.Site.storageSite   = 'T2_CH_CERN' 


