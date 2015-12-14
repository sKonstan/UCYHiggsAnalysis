#!/usr/bin/env python
###############################################################
### All imported modules
###############################################################
import os
import FWCore.ParameterSet.Config as cms

###############################################################
### Function definition
###############################################################
def GetEosRootFilesForDataset(dataset):
    
    allDatasets = []
    datasets_v2 = [
        "/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM",
        "/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2_ext1-v1/MINIAODSIM",
        "/TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v3/MINIAODSIM",
        "/ST_tW_antitop_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM",
        "/ST_tW_top_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v2/MINIAODSIM",
        "/ST_t-channel_top_4f_leptonDecays_13TeV-powheg-pythia8_TuneCUETP8M1/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM",
        "/ST_t-channel_antitop_4f_leptonDecays_13TeV-powheg-pythia8_TuneCUETP8M1/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM",
        "/ST_s-channel_4f_leptonDecays_13TeV-amcatnlo-pythia8_TuneCUETP8M1/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM",
        "/DYJetsToLL_M-10to50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM",
        "/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM",        
        "/DYJetsToLL_M-50_HT-100to200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM",
        "/DYJetsToLL_M-50_HT-200to400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM",
        "/DYJetsToLL_M-50_HT-400to600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v2/MINIAODSIM",
        "/DYJetsToLL_M-50_HT-600toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM",
        "/WW_TuneCUETP8M1_13TeV-pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM",
        "/WZ_TuneCUETP8M1_13TeV-pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM",
        "/ZZ_TuneCUETP8M1_13TeV-pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM",
        "/WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM",
        "/WJetsToLNu_HT-100To200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM",
        "/WJetsToLNu_HT-200To400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM",
        "/WJetsToLNu_HT-400To600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM",
        "/WJetsToLNu_HT-600To800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM",
        "/WJetsToLNu_HT-800To1200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM",
        "/WJetsToLNu_HT-1200To2500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM",
        "/WJetsToLNu_HT-2500ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM",
        "/DoubleMuon/Run2015D-PromptReco-v4/MINIAOD"
        "/DoubleEG/Run2015D-PromptReco-v4/MINIAOD"
        "/MuonEG/Run2015D-PromptReco-v4/MINIAOD"
        "/SingleMuon/Run2015D-PromptReco-v4/MINIAOD"
        "/SingleElectron/Run2015D-PromptReco-v4/MINIAOD"]
    
    allDatasets.extend(datasets_v2)

    # Ensure that dataset is valid/supported
    if dataset not in allDatasets:
        raise Exception("Unknown dataset '%s'. Please select a valid dataset from this list:\n\t%s" % (dataset, "\n\t".join(allDatasets)) )

    # MC Data
    if dataset == '/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM':
        import UCYHiggsAnalysis.MiniAOD2FlatTree.tools.ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix_RunIISpring15MiniAODv2_74X_mcRun2_asymptotic_v2_v1_MINIAODSIM as dataset_py
        return dataset_py.readFiles

    elif dataset == '/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2_ext1-v1/MINIAODSIM':
        import UCYHiggsAnalysis.MiniAOD2FlatTree.tools.ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix_RunIISpring15MiniAODv2_74X_mcRun2_asymptotic_v2_ext1_v1_MINIAODSIM as dataset_py
        return dataset_py.readFiles

    elif dataset == '/TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v3/MINIAODSIM':
        import UCYHiggsAnalysis.MiniAOD2FlatTree.tools.TTJets_TuneCUETP8M1_13TeV_amcatnloFXFX_pythia8_RunIISpring15MiniAODv2_74X_mcRun2_asymptotic_v2_v3_MINIAODSIM as dataset_py
        return dataset_py.readFiles

    elif dataset == '/DYJetsToLL_M-10to50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM':
        import UCYHiggsAnalysis.MiniAOD2FlatTree.tools. DYJetsToLL_M_10to50_TuneCUETP8M1_13TeV_amcatnloFXFX_pythia8_RunIISpring15MiniAODv2_74X_mcRun2_asymptotic_v2_v1_MINIAODSIM as dataset_py
        return dataset_py.readFiles    

    elif dataset == '/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM':
        import UCYHiggsAnalysis.MiniAOD2FlatTree.tools.DYJetsToLL_M_50_TuneCUETP8M1_13TeV_amcatnloFXFX_pythia8_RunIISpring15MiniAODv2_74X_mcRun2_asymptotic_v2_v1_MINIAODSIM as dataset_py
        return dataset_py.readFiles

    elif dataset == '/DYJetsToLL_M-50_HT-100to200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM':
        import UCYHiggsAnalysis.MiniAOD2FlatTree.tools.DYJetsToLL_M_50_HT_100to200_TuneCUETP8M1_13TeV_madgraphMLM_pythia8_RunIISpring15MiniAODv2_74X_mcRun2_asymptotic_v2_v1_MINIAODSIM as dataset_py
        return dataset_py.readFiles
        
    elif dataset == '/DYJetsToLL_M-50_HT-200to400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM':
        import UCYHiggsAnalysis.MiniAOD2FlatTree.tools.DYJetsToLL_M_50_HT_200to400_TuneCUETP8M1_13TeV_madgraphMLM_pythia8_RunIISpring15MiniAODv2_74X_mcRun2_asymptotic_v2_v1_MINIAODSIM as dataset_py
        return dataset_py.readFiles
    
    elif dataset == '/DYJetsToLL_M-50_HT-400to600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v2/MINIAODSIM':
        import UCYHiggsAnalysis.MiniAOD2FlatTree.tools.DYJetsToLL_M_50_HT_400to600_TuneCUETP8M1_13TeV_madgraphMLM_pythia8_RunIISpring15MiniAODv2_74X_mcRun2_asymptotic_v2_v2_MINIAODSIM as dataset_py
        return dataset_py.readFiles
        
    elif dataset == '/DYJetsToLL_M-50_HT-600toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM':
        import UCYHiggsAnalysis.MiniAOD2FlatTree.tools.DYJetsToLL_M_50_HT_600toInf_TuneCUETP8M1_13TeV_madgraphMLM_pythia8_RunIISpring15MiniAODv2_74X_mcRun2_asymptotic_v2_v1_MINIAODSIM as dataset_py
        return dataset_py.readFiles

    elif dataset == '/WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM':
        import UCYHiggsAnalysis.MiniAOD2FlatTree.tools.WJetsToLNu_TuneCUETP8M1_13TeV_amcatnloFXFX_pythia8_RunIISpring15MiniAODv2_74X_mcRun2_asymptotic_v2_v1_MINIAODSIM as dataset_py
        return dataset_py.readFiles

    elif dataset == '/WJetsToLNu_HT-100To200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM':
        import UCYHiggsAnalysis.MiniAOD2FlatTree.tools.WJetsToLNu_HT_100To200_TuneCUETP8M1_13TeV_madgraphMLM_pythia8_RunIISpring15MiniAODv2_74X_mcRun2_asymptotic_v2_v1_MINIAODSIM as dataset_py
        return dataset_py.readFiles

    elif dataset == '/WJetsToLNu_HT-200To400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM':
        import UCYHiggsAnalysis.MiniAOD2FlatTree.tools.WJetsToLNu_HT_200To400_TuneCUETP8M1_13TeV_madgraphMLM_pythia8_RunIISpring15MiniAODv2_74X_mcRun2_asymptotic_v2_v1_MINIAODSIM as dataset_py
        return dataset_py.readFiles

    elif dataset == '/WJetsToLNu_HT-400To600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM':
        import UCYHiggsAnalysis.MiniAOD2FlatTree.tools.WJetsToLNu_HT_400To600_TuneCUETP8M1_13TeV_madgraphMLM_pythia8_RunIISpring15MiniAODv2_74X_mcRun2_asymptotic_v2_v1_MINIAODSIM as dataset_py
        return dataset_py.readFiles

    elif dataset == '/WJetsToLNu_HT-600To800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM':
        import UCYHiggsAnalysis.MiniAOD2FlatTree.tools.WJetsToLNu_HT_600To800_TuneCUETP8M1_13TeV_madgraphMLM_pythia8_RunIISpring15MiniAODv2_74X_mcRun2_asymptotic_v2_v1_MINIAODSIM as dataset_py
        return dataset_py.readFiles

    elif dataset == '/WJetsToLNu_HT-800To1200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM':
        import UCYHiggsAnalysis.MiniAOD2FlatTree.tools.WJetsToLNu_HT_800To1200_TuneCUETP8M1_13TeV_madgraphMLM_pythia8_RunIISpring15MiniAODv2_74X_mcRun2_asymptotic_v2_v1_MINIAODSIM as dataset_py
        return dataset_py.readFiles

    elif dataset == '/WJetsToLNu_HT-1200To2500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM':
        import UCYHiggsAnalysis.MiniAOD2FlatTree.tools.WJetsToLNu_HT_1200To2500_TuneCUETP8M1_13TeV_madgraphMLM_pythia8_RunIISpring15MiniAODv2_74X_mcRun2_asymptotic_v2_v1_MINIAODSIM as dataset_py
        return dataset_py.readFiles

    elif dataset == '/WJetsToLNu_HT-2500ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM':
        import UCYHiggsAnalysis.MiniAOD2FlatTree.tools.WJetsToLNu_HT_2500ToInf_TuneCUETP8M1_13TeV_madgraphMLM_pythia8_RunIISpring15MiniAODv2_74X_mcRun2_asymptotic_v2_v1_MINIAODSIM as dataset_py
        return dataset_py.readFiles

    elif dataset == '/ST_tW_antitop_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM':
        import UCYHiggsAnalysis.MiniAOD2FlatTree.tools.ST_tW_antitop_5f_inclusiveDecays_13TeV_powheg_pythia8_TuneCUETP8M1_RunIISpring15MiniAODv2_74X_mcRun2_asymptotic_v2_v1_MINIAODSIM as dataset_py
        return dataset_py.readFiles
    
    elif dataset == '/ST_tW_top_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v2/MINIAODSIM':
        import UCYHiggsAnalysis.MiniAOD2FlatTree.tools.ST_tW_top_5f_inclusiveDecays_13TeV_powheg_pythia8_TuneCUETP8M1_RunIISpring15MiniAODv2_74X_mcRun2_asymptotic_v2_v2_MINIAODSIM as dataset_py
        return dataset_py.readFiles

    elif dataset == '/ST_t-channel_top_4f_leptonDecays_13TeV-powheg-pythia8_TuneCUETP8M1/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM':
        import UCYHiggsAnalysis.MiniAOD2FlatTree.tools.ST_t_channel_top_4f_leptonDecays_13TeV_powheg_pythia8_TuneCUETP8M1_RunIISpring15MiniAODv2_74X_mcRun2_asymptotic_v2_v1_MINIAODSIM as dataset_py
        return dataset_py.readFiles

    elif dataset == '/ST_t-channel_antitop_4f_leptonDecays_13TeV-powheg-pythia8_TuneCUETP8M1/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM':
        import UCYHiggsAnalysis.MiniAOD2FlatTree.tools.ST_t_channel_antitop_4f_leptonDecays_13TeV_powheg_pythia8_TuneCUETP8M1_RunIISpring15MiniAODv2_74X_mcRun2_asymptotic_v2_v1_MINIAODSIM as dataset_py
        return dataset_py.readFiles

    elif dataset == '/ST_s-channel_4f_leptonDecays_13TeV-amcatnlo-pythia8_TuneCUETP8M1/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM':
        import UCYHiggsAnalysis.MiniAOD2FlatTree.tools.ST_s_channel_4f_leptonDecays_13TeV_amcatnlo_pythia8_TuneCUETP8M1_RunIISpring15MiniAODv2_74X_mcRun2_asymptotic_v2_v1_MINIAODSIM as dataset_py
        return dataset_py.readFiles
 
    elif dataset == '/WW_TuneCUETP8M1_13TeV-pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM':
        import UCYHiggsAnalysis.MiniAOD2FlatTree.tools.WW_TuneCUETP8M1_13TeV_pythia8_RunIISpring15MiniAODv2_74X_mcRun2_asymptotic_v2_v1_MINIAODSIM as dataset_py
        return dataset_py.readFiles

    elif dataset == '/WZ_TuneCUETP8M1_13TeV-pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM':
        import UCYHiggsAnalysis.MiniAOD2FlatTree.tools.WZ_TuneCUETP8M1_13TeV_pythia8_RunIISpring15MiniAODv2_74X_mcRun2_asymptotic_v2_v1_MINIAODSIM as dataset_py
        return dataset_py.readFiles

    elif dataset == '/ZZ_TuneCUETP8M1_13TeV-pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM':
        import UCYHiggsAnalysis.MiniAOD2FlatTree.tools.ZZ_TuneCUETP8M1_13TeV_pythia8_RunIISpring15MiniAODv2_74X_mcRun2_asymptotic_v2_v1_MINIAODSIM as dataset_py
        return dataset_py.readFiles

    # Collision Data
    elif dataset == "/DoubleMuon/Run2015D-PromptReco-v4/MINIAOD":
        import UCYHiggsAnalysis.MiniAOD2FlatTree.tools.DoubleMuon_Run2015D_PromptReco_v4_MINIAOD as dataset_py
        return dataset_py.readFiles

    elif dataset == "/DoubleEG/Run2015D-PromptReco-v4/MINIAOD":
        import UCYHiggsAnalysis.MiniAOD2FlatTree.tools.DoubleEG_Run2015D_PromptReco_v4_MINIAOD as dataset_py
        return dataset_py.readFiles

    elif dataset == "/MuonEG/Run2015D-PromptReco-v4/MINIAOD":
        import UCYHiggsAnalysis.MiniAOD2FlatTree.tools.MuonEG_Run2015D_PromptReco_v4_MINIAOD as dataset_py
        return dataset_py.readFiles

    elif dataset == "/SingleMuon/Run2015D-PromptReco-v4/MINIAOD":
        import UCYHiggsAnalysis.MiniAOD2FlatTree.tools.SingleMuon_Run2015D_PromptReco_v4_MINIAOD as dataset_py
        return dataset_py.readFiles

    elif dataset == "/SingleElectron/Run2015D-PromptReco-v4/MINIAOD":
        import UCYHiggsAnalysis.MiniAOD2FlatTree.tools.SingleElectron_Run2015D_PromptReco_v4_MINIAOD as dataset_py
        return dataset_py.readFiles

    else:
        raise Exception("Unknown dataset '%s'. Please provide a valid dataset." % (dataset) )


