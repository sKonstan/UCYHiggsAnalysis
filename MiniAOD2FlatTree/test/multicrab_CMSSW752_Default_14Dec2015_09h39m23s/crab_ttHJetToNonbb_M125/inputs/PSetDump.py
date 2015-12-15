import FWCore.ParameterSet.Config as cms

process = cms.Process("MiniAOD2FlatTree")

process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring( ('/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/10000/084C88C7-CA6D-E511-92EC-0025900EB530.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/10000/0CD68CD5-CA6D-E511-B8F0-0022195E660C.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/10000/14939DBE-CA6D-E511-AEDA-0CC47A124334.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/10000/30AF04DE-CA6D-E511-8DA6-002590C14B42.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/10000/388584C6-CA6D-E511-8C88-001EC9ADD74F.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/10000/40F170D9-CA6D-E511-9B6B-001EC9ADE118.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/10000/44D205C4-CA6D-E511-A4FB-001EC9ADDD7B.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/10000/46688DBD-CA6D-E511-96B4-0025904C540E.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/10000/503761CA-CA6D-E511-B972-0CC47A124458.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/10000/504F54D8-CA6D-E511-82F8-001EC9ADE40B.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/10000/667943BD-CA6D-E511-B6EC-0025905C3D3E.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/10000/66966582-CB6D-E511-99A5-001EC9ADDBCD.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/10000/68BE26CF-CA6D-E511-949D-002590E50602.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/10000/6AA0D7C1-CA6D-E511-A00B-001EC9ADC343.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/10000/7AC6FE81-CB6D-E511-B136-001EC9ADDBCD.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/10000/82342CBC-CA6D-E511-ABCA-0025905C42B8.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/10000/84073CC3-CA6D-E511-80F9-001EC9ADDBB9.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/10000/90BA5E86-CB6D-E511-887A-001EC9ADDBFF.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/10000/922799D8-CA6D-E511-A650-001EC9ADE55F.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/10000/923ADDBD-CA6D-E511-9492-0025905C96EA.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/10000/969FA5D7-CA6D-E511-AB12-001EC9ADC5E1.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/10000/A20704C4-CA6D-E511-9FF6-001EC9ADDBCD.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/10000/A801A7EE-CA6D-E511-A0E2-0022195E688C.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/10000/BE592ABC-CA6D-E511-A007-0025905C3E36.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/10000/C6FF98D6-CA6D-E511-BDD6-0022195D9EE0.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/10000/C80B41BC-CA6D-E511-8577-0025905C95F8.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/10000/D0CA9BC2-CA6D-E511-A3E7-001EC9ADC9B5.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/10000/DC8BA9CE-CA6D-E511-9CE5-0025900EB504.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/10000/E0B6D7C1-CA6D-E511-84BC-001EC9ADC343.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/10000/EE7148C4-CA6D-E511-8010-001EC9ADCC80.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/30000/0A9E2A36-D46D-E511-8CD8-001EC9ADE5DC.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/30000/2AF1DA30-D46D-E511-A473-0025900EB19A.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/30000/44AC3B32-D46D-E511-AA01-001EC9ADE40B.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/30000/4C853B38-D46D-E511-BB66-0CC47A124224.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/30000/6099EB3C-D46D-E511-87BA-0022195D9EE0.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/30000/8698CE43-D46D-E511-9256-001EC9ADDA06.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/30000/8E6FFD30-D46D-E511-B4AC-001EC9ADC0B4.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/30000/9EF1944D-D46D-E511-BA81-001EC9ADDBF0.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/30000/A24F6133-D46D-E511-9321-001EC9ADDE57.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/30000/C4D9F3B3-D36D-E511-A24A-0025905C96A6.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/30000/C88442B6-D36D-E511-80DE-0CC47A1240B0.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/30000/D8967AB6-D36D-E511-85E8-0025905C3DD0.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/30000/DA378436-D46D-E511-B6D5-001EC9ADDBCD.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/30000/DCE63D35-D46D-E511-8187-001EC9ADCE83.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/30000/E8B25234-D46D-E511-858E-001EC9ADE258.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/30000/EE9D3533-D46D-E511-9AEA-001EC9ADDBF5.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/30000/F2C602B7-D36D-E511-A394-002590C14CD2.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/40000/00EFC145-D76D-E511-A360-001EC9ADE177.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/40000/04E8019B-D66D-E511-BC9B-0025905C2CA4.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/40000/12173198-D66D-E511-B6B7-002590E505FE.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/40000/12A88A3E-D76D-E511-A3D7-001EC9ADDE5C.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/40000/16467F99-D66D-E511-A701-0025905C42F4.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/40000/18C23FA1-D66D-E511-A73D-001EC9ADC0B4.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/40000/2CF07998-D66D-E511-8D0B-0025905C94D2.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/40000/325BE93E-D76D-E511-A757-001EC9ADDBFF.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/40000/367FA7B3-D66D-E511-A8DA-0CC47A124224.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/40000/4070ABE5-D76D-E511-8AC8-001EC9ADE690.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/40000/42B82F40-D76D-E511-ADEC-002590E50B28.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/40000/441A6E99-D66D-E511-8AA2-0025905C4264.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/40000/4A2257A2-D66D-E511-A0B9-001EC9ADC343.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/40000/4E08D599-D66D-E511-9B98-0025905C94D2.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/40000/50BDE79D-D66D-E511-9807-001EC9ADE5DC.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/40000/50FDB49A-D66D-E511-A950-0025905C975E.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/40000/5219073E-D76D-E511-AC5A-0025900EB234.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/40000/54EC1E98-D66D-E511-A231-0025905BA734.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/40000/5657C4ED-D76D-E511-A1CA-0025900EB52A.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/40000/585CF338-D96D-E511-836B-001EC9ADE690.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/40000/5ABA239C-D66D-E511-AC27-001EC9ADDBCD.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/40000/605EEBAC-D66D-E511-BD02-001EC9ADCE83.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/40000/6079A398-D66D-E511-94FD-0025905C2CB8.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/40000/60CA9C43-D76D-E511-BD63-0025900EB52C.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/40000/60F21198-D66D-E511-B354-0025905C96EA.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/40000/66B0D244-D76D-E511-8C04-001EC9ADDB0F.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/40000/74C8723D-D76D-E511-AD7E-001EC9ADE5DC.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/40000/786F9598-D66D-E511-B2B6-0025905C3D6A.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/40000/7A349346-D76D-E511-97B8-002590E5037C.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/40000/7C196E99-D66D-E511-B61E-0025905C4264.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/40000/7E79A398-D66D-E511-8DD5-0025905C2CB8.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/40000/84BE2C46-D76D-E511-919F-001EC9ADE690.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/40000/860E6A99-D66D-E511-8544-0025905C975E.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/40000/8C8A99EB-D76D-E511-A801-0CC47A124334.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/40000/8C8E099C-D66D-E511-AE0E-001EC9ADC9B5.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/40000/925C359C-D66D-E511-AA0F-001EC9ADDE57.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/40000/965CCE29-D96D-E511-A5A7-001EC9ADDDDF.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/40000/9C480B3E-D76D-E511-9CC5-001D0970C37A.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/40000/9CEA639E-D66D-E511-911E-001EC9ADE794.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/40000/9E3D973D-D76D-E511-BD22-002590C18A26.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/40000/9E9A3542-D76D-E511-AD9A-001EC9ADC343.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/40000/9EEA073E-D76D-E511-8284-001D0970C37A.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/40000/AA14A7A5-D66D-E511-9DF2-001EC9ADE744.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/40000/AED6A29D-D66D-E511-A4DF-001EC9ADDBF5.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/40000/B0387F99-D66D-E511-8A65-0025905C3DF6.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/40000/B04F0A3D-D76D-E511-96D1-001EC9ADE258.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/40000/B2DB95E6-D76D-E511-B5BD-001EC9ADE177.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/40000/B45BBE3C-D76D-E511-AD46-001EC9ADDB5A.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/40000/B641EEA7-D66D-E511-BD02-001EC9ADDA06.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/40000/BA7A239F-D66D-E511-8E84-002590C18A26.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/40000/BA7FFFE9-D76D-E511-9087-001EC9ADDBCD.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/40000/BC27779C-D66D-E511-A7BD-001EC9ADE9A6.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/40000/BC9F339A-D66D-E511-B721-002590AC4C6C.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/40000/BCEECF3F-D76D-E511-B07B-001EC9ADDDDF.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/40000/C43B1D99-D66D-E511-9DF3-0025905C94D0.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/40000/C89ECA9D-D66D-E511-8198-002219558002.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/40000/CA74019E-D66D-E511-A321-001EC9ADE40B.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/40000/CAF7A698-D66D-E511-AFA0-0025905C3DF8.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/40000/CCDC5E9A-D66D-E511-A963-0025905C42F2.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/40000/CE58813F-D76D-E511-A1D8-001EC9ADDD58.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/40000/D675A724-D96D-E511-87AC-002590E505FE.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/40000/D84D90AA-D66D-E511-B685-0025900EB19A.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/40000/DA1B589A-D66D-E511-B92F-0025905C2C84.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/40000/DA77A398-D66D-E511-A14F-0025905C2CB8.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/40000/DC30AA9A-D66D-E511-A413-0025905C96EA.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/40000/E63FC09D-D66D-E511-9D25-001EC9ADDBF0.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/40000/F0282CE3-D76D-E511-AF57-002590E50600.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/40000/F060669F-D66D-E511-88BC-001EC9ADDBFF.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/40000/F0885C25-D86D-E511-8C5A-002590E505FE.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/40000/F8897B9A-D66D-E511-AE5A-0025905C2CA6.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/50000/003AB6D6-CA6D-E511-85BF-00266CFAE228.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/50000/06CB2643-CA6D-E511-AAE9-0025905C96EA.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/50000/089D1DF1-C96D-E511-9E4C-00266CFADD94.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/50000/1C596D03-CA6D-E511-A478-001EC9ADDB5A.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/50000/1C65D593-CA6D-E511-934E-0025905C9724.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/50000/22D30AF0-C96D-E511-897F-3417EBE649FF.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/50000/266BC9EF-C96D-E511-8962-3417EBE649FF.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/50000/280416EF-C96D-E511-BD05-002590E505FE.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/50000/2E3525F4-C96D-E511-B544-00266CF9B5D0.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/50000/32C413F0-C96D-E511-AFB4-00266CFAEBA0.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/50000/409B94F3-C96D-E511-A947-00266CF25708.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/50000/461766D6-CA6D-E511-A218-00A0D1EE29B8.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/50000/466394D4-CA6D-E511-9042-3417EBE649FF.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/50000/484F1CD7-CA6D-E511-AA37-00266CFADD94.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/50000/4C0406EF-C96D-E511-B09F-00266CFAE228.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/50000/4C22B503-CA6D-E511-952A-001EC9ADE177.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/50000/4E8CFFE2-CA6D-E511-BAD2-00266CF9C0F0.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/50000/4ED34CD6-CA6D-E511-BF2E-00A0D1EE29B8.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/50000/50221AF0-C96D-E511-97EA-001EC9ADD5B0.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/50000/5A2291EC-C96D-E511-AA72-00266CFABAF0.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/50000/5AC06BEC-C96D-E511-849E-00266CFABAF0.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/50000/682406EF-C96D-E511-8E46-00266CFAE228.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/50000/682E6BEE-C96D-E511-A393-0025905C2D9A.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/50000/68D3FFF0-C96D-E511-B2AF-0025905C96EA.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/50000/70D10EF0-C96D-E511-A970-3417EBE64AFE.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/50000/740473D6-CA6D-E511-9A7B-00266CFAE228.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/50000/76E6BCFE-C96D-E511-A28E-002590A80DEA.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/50000/784D7DEE-C96D-E511-87E9-7845C4FC39B3.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/50000/7C25ED29-CA6D-E511-8C58-0025904CF75A.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/50000/82C04F30-CA6D-E511-8F37-0025905C42F2.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/50000/82C5B3EF-C96D-E511-A10E-3417EBE649FF.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/50000/84C0FCFE-C96D-E511-8EFC-002590A80DF0.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/50000/86A183EA-C96D-E511-A31E-3417EBE644C2.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/50000/880B33F2-C96D-E511-BAC3-00266CF271E8.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/50000/88A664D9-CA6D-E511-94A0-008CFA0020D4.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/50000/8A4523F3-C96D-E511-B07C-001EC9ADEB7C.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/50000/8A7E4CF0-C96D-E511-9053-00266CF9BBE4.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/50000/9040B749-CA6D-E511-836F-0025905C3D3E.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/50000/909ECE06-CA6D-E511-A08E-00266CF9BF5C.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/50000/9AA459F3-C96D-E511-956D-00A0D1EE29B8.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/50000/A89828F5-C96D-E511-8E35-002590DB9286.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/50000/B02C17D8-CA6D-E511-BF2D-00266CF9B5D0.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/50000/B234B6EE-C96D-E511-BA63-0025904C540E.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/50000/B28A37F4-C96D-E511-800E-00A0D1EE29B8.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/50000/B8A149F2-C96D-E511-9445-009C02AAB554.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/50000/BA5AEFF5-C96D-E511-8B70-00266CF9AED8.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/50000/BE8E991B-CC6D-E511-B519-009C02AAB554.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/50000/C2B95BF0-C96D-E511-954B-00266CF9BBE4.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/50000/C8819AF2-C96D-E511-983F-00266CF271E8.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/50000/DC849BF3-C96D-E511-A7D4-00A0D1EE29B8.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/50000/EC6963F5-C96D-E511-91C2-00266CF9AED8.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/50000/FAAB7AF2-C96D-E511-A926-00266CF271E8.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/50000/FEE920F1-C96D-E511-8133-0025904CF102.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/60000/0C672592-CB6D-E511-9212-002590E50AFE.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/60000/3A48499B-CB6D-E511-86BF-001D0970C37A.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/60000/3A8E1494-CB6D-E511-82C7-001EC9ADE794.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/60000/424E5095-CB6D-E511-A38A-0022195E6693.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/60000/52184599-CB6D-E511-8CC3-001EC9ADDBEB.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/60000/7CF17899-CB6D-E511-BDCA-001EC9ADDBEB.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/60000/86C06795-CB6D-E511-BCE0-001EC9ADC5E1.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/60000/AEA98F98-CB6D-E511-945B-001EC9ADE703.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/60000/B6944AA4-CB6D-E511-A789-001EC9ADDFB0.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/60000/C2497392-CB6D-E511-B6CD-002590E50600.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/60000/D61C7095-CB6D-E511-806F-001EC9ADDBF5.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/60000/E6472898-CB6D-E511-BDF2-001EC9ADE67C.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/60000/ECA12E91-CB6D-E511-B2F2-0CC47A124334.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2_ext1-v1/30000/00A87ACA-706F-E511-A664-0025905C445A.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2_ext1-v1/30000/04E18112-716F-E511-A91B-0025905AC960.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2_ext1-v1/30000/06704948-E46D-E511-AF5A-90B11C04FE0C.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2_ext1-v1/30000/1040DC44-E46D-E511-B0C8-0025905C4472.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2_ext1-v1/30000/10E02F69-6B6F-E511-B2DE-0025905C446A.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2_ext1-v1/30000/121C4905-6E6F-E511-88E6-0025905AC806.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2_ext1-v1/30000/1297DE1B-E46D-E511-89B5-0025905AC802.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2_ext1-v1/30000/146F74FB-E46D-E511-9A1E-001E67A3EAB1.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2_ext1-v1/30000/16297CB9-6B6F-E511-8AEC-0025905C22B0.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2_ext1-v1/30000/16C5D0FA-706F-E511-B19A-0025905C2CC2.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2_ext1-v1/30000/1862F528-6B6F-E511-8326-0025905AF57C.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2_ext1-v1/30000/1A3D3760-E46D-E511-B46E-001517EC2B60.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2_ext1-v1/30000/1E41EB25-6B6F-E511-A218-0025905C2CC2.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2_ext1-v1/30000/1E8F13AD-6D6F-E511-B7CE-0025905AC99C.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2_ext1-v1/30000/202D408D-756F-E511-97BD-0025905AC808.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2_ext1-v1/30000/203AABB3-6D6F-E511-80B6-0025905AC99A.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2_ext1-v1/30000/20B21DB0-6D6F-E511-9508-0025905AF57C.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2_ext1-v1/30000/225A6FD9-706F-E511-B96D-0025905AC95E.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2_ext1-v1/30000/241ABFE3-6D6F-E511-92AA-0025905AC982.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2_ext1-v1/30000/26398B45-E46D-E511-91C8-90B11C064AD8.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2_ext1-v1/30000/2A00E6B7-6D6F-E511-9047-0025905AC878.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2_ext1-v1/30000/2CDB7CFB-E46D-E511-85D2-001E67A3E872.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2_ext1-v1/30000/2E882D37-E56D-E511-B02E-001E67A3E872.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2_ext1-v1/30000/322F5299-6B6F-E511-BFD1-0025905AC982.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2_ext1-v1/30000/3260C428-E56D-E511-B9AB-001517FB25E4.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2_ext1-v1/30000/32EE8600-E56D-E511-9443-90B11C06954E.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2_ext1-v1/30000/3403F004-6E6F-E511-8FF4-0025905AC806.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2_ext1-v1/30000/3457502B-6B6F-E511-91D6-0025905AC878.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2_ext1-v1/30000/36040244-E46D-E511-8A89-90B11C08C6BF.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2_ext1-v1/30000/364B51CF-756F-E511-A0E1-0025905AC824.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2_ext1-v1/30000/364EF24A-E46D-E511-8C14-90B11C08CA45.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2_ext1-v1/30000/3668A8C4-756F-E511-AF2E-0025905C2CC2.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2_ext1-v1/30000/36E1DE6A-756F-E511-9B3B-0025905AC822.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2_ext1-v1/30000/36E9254F-E46D-E511-83E6-001E675A69DC.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2_ext1-v1/30000/3AE0FE14-766F-E511-9422-0025905C4326.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2_ext1-v1/30000/3CA2CEA2-6D6F-E511-8797-0025905AC99A.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2_ext1-v1/30000/4071943F-E46D-E511-ABF7-001E67A3E8CC.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2_ext1-v1/30000/40EB5005-6E6F-E511-8BF5-0025905AC806.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2_ext1-v1/30000/462344FF-6A6F-E511-93B7-0025905AC878.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2_ext1-v1/30000/4645004A-E46D-E511-88C8-001517F7F950.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2_ext1-v1/30000/481A210A-716F-E511-80F6-0025905AC806.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2_ext1-v1/30000/4848E0E5-706F-E511-B9A1-0025905C445A.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2_ext1-v1/30000/4AA9F865-6B6F-E511-AA94-0025905C445C.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2_ext1-v1/30000/4C99EFAC-6D6F-E511-8D4E-0025905AC99C.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2_ext1-v1/30000/4E203512-716F-E511-8F0F-0025905AC960.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2_ext1-v1/30000/4E41D1A5-706F-E511-8D53-0025905C22AE.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2_ext1-v1/30000/52FF56FA-E46D-E511-B5AC-001E67A406E0.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2_ext1-v1/30000/5641B5C8-706F-E511-A79C-0025905AC95E.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2_ext1-v1/30000/5ACC6992-6D6F-E511-9802-0025905AC960.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2_ext1-v1/30000/5C42BADF-706F-E511-840B-0025905AC97C.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2_ext1-v1/30000/5CA4F9C1-6A6F-E511-8D6F-0025905C445C.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2_ext1-v1/30000/5E6F62A6-E86D-E511-9334-0026182FD7A9.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2_ext1-v1/30000/5E91B129-6B6F-E511-B6D7-0025905C4472.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2_ext1-v1/30000/5ECD3BFF-6A6F-E511-BE09-0025905AC878.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2_ext1-v1/30000/606FCEAC-6D6F-E511-B740-0025905AC97C.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2_ext1-v1/30000/64E459E1-706F-E511-AAA2-0025905AC806.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2_ext1-v1/30000/66AB0EFF-706F-E511-8B8B-0025905C2CC2.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2_ext1-v1/30000/68515ADE-6B6F-E511-AAB4-0025905AC9AE.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2_ext1-v1/30000/6A1D9FC6-756F-E511-ADF7-0025905C2CC0.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2_ext1-v1/30000/6E8876C6-756F-E511-B86C-0025905C2CC0.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2_ext1-v1/30000/70D364E0-706F-E511-AC15-0025905AC99C.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2_ext1-v1/30000/741ABFE3-6D6F-E511-898F-0025905AC982.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2_ext1-v1/30000/742D7271-E46D-E511-AFF0-001E675A690A.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2_ext1-v1/30000/781387AB-6D6F-E511-A437-0025905C4472.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2_ext1-v1/30000/7A3465FC-E56D-E511-A513-001517FAAB30.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2_ext1-v1/30000/7E333760-E46D-E511-A9AF-001517EC2B60.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2_ext1-v1/30000/7EA83B6E-E46D-E511-A3DC-001517F7F504.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2_ext1-v1/30000/7ECED8E6-6A6F-E511-99A8-0025905AC97C.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2_ext1-v1/30000/804BFE64-6B6F-E511-BCD0-0025905AC960.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2_ext1-v1/30000/82BD8740-E46D-E511-97AA-001E67A3FB91.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2_ext1-v1/30000/84498E47-E46D-E511-A8F0-0025905AC95E.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2_ext1-v1/30000/84BBC4DE-706F-E511-BDDA-0025905AC99A.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2_ext1-v1/30000/84DEA946-E46D-E511-91B6-0025905AC97A.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2_ext1-v1/30000/88BFD3AC-6D6F-E511-BBFC-0025905AC97C.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2_ext1-v1/30000/8C1AAD4A-E46D-E511-BDA0-001517E74088.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2_ext1-v1/30000/9205E312-716F-E511-96E7-0025905AC960.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2_ext1-v1/30000/9452DC25-6B6F-E511-8227-0025905C2CC2.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2_ext1-v1/30000/98580850-E46D-E511-BF2D-001E675A6725.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2_ext1-v1/30000/98BC2B50-E46D-E511-8ED0-0025905AC808.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2_ext1-v1/30000/98EC2697-6B6F-E511-A6D4-0025905AC878.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2_ext1-v1/30000/9EB95FE5-756F-E511-8229-0025905AC982.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2_ext1-v1/30000/A02C4A46-E46D-E511-AB50-0025905C2CC2.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2_ext1-v1/30000/A04A6AFC-706F-E511-80E3-0025905C426E.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2_ext1-v1/30000/A0B5CEF0-706F-E511-B719-0025905AC982.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2_ext1-v1/30000/A0C52E4E-716F-E511-9743-0025905AF57C.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2_ext1-v1/30000/A2360797-6E6F-E511-AA0F-0025905C445A.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2_ext1-v1/30000/A28C2257-E46D-E511-8394-0026182FD7A9.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2_ext1-v1/30000/A63BE446-E46D-E511-8DCC-0025905AC99A.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2_ext1-v1/30000/A6A0CB45-E46D-E511-B9E9-0025905AC984.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2_ext1-v1/30000/A6C96B4A-E46D-E511-B856-90B11C06CD59.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2_ext1-v1/30000/A8E5F580-6D6F-E511-B1BD-0025905AC99C.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2_ext1-v1/30000/AA523850-E46D-E511-B21D-001E67A402C1.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2_ext1-v1/30000/AA91DBFE-E46D-E511-992C-90B11C1453E1.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2_ext1-v1/30000/AAF2E4DE-706F-E511-86A1-0025905AC99A.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2_ext1-v1/30000/AAFB54DE-6B6F-E511-AA75-0025905AC9AE.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2_ext1-v1/30000/ACD1E7BF-E46D-E511-A416-001517FB25E4.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2_ext1-v1/30000/AEA35042-E46D-E511-89F4-001E67A3E8F9.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2_ext1-v1/30000/B0236E52-E46D-E511-8D8E-001517FB1944.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2_ext1-v1/30000/B086BEDE-706F-E511-9422-0025905AC99A.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2_ext1-v1/30000/B09594F5-6A6F-E511-B7D6-0025905AF57E.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2_ext1-v1/30000/B23E3C52-6B6F-E511-BDE2-0025905AC99A.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2_ext1-v1/30000/B4F1D1F8-E46D-E511-A26A-001E67A4069F.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2_ext1-v1/30000/BA3178A7-6B6F-E511-BBDF-0025905AC960.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2_ext1-v1/30000/BA82A5AE-6D6F-E511-832A-0025905C446A.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2_ext1-v1/30000/BCAF4C45-E46D-E511-BC7D-0025905AC802.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2_ext1-v1/30000/BEF30197-6D6F-E511-BDB1-0025905C445C.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2_ext1-v1/30000/C24845C9-716F-E511-8016-0025905C4434.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2_ext1-v1/30000/C2606712-716F-E511-90B7-0025905AC960.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2_ext1-v1/30000/C2774C4A-E46D-E511-9A30-0025905C446E.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2_ext1-v1/30000/C6C31AB0-6D6F-E511-B0D6-0025905AF57C.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2_ext1-v1/30000/CA6F9FE1-756F-E511-B7F4-0025905C2CC2.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2_ext1-v1/30000/CC008C45-E46D-E511-BD7D-0025905AC9AE.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2_ext1-v1/30000/CC063665-6D6F-E511-85B5-0025905AC97C.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2_ext1-v1/30000/CE3E5B45-E46D-E511-BACC-0025905AC982.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2_ext1-v1/30000/D2463C52-6B6F-E511-92FC-0025905AC99A.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2_ext1-v1/30000/D46B7448-6B6F-E511-A37E-0025905AC960.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2_ext1-v1/30000/D4980F05-6E6F-E511-BAE1-0025905AC806.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2_ext1-v1/30000/D64EBD33-6B6F-E511-B237-0025905C4472.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2_ext1-v1/30000/D8775148-E46D-E511-A32C-D4AE529D9537.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2_ext1-v1/30000/D8DF8EFC-E46D-E511-B7B5-90B11C064B50.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2_ext1-v1/30000/DA3364F3-756F-E511-8F93-0025905AC97A.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2_ext1-v1/30000/DCB05A4D-E46D-E511-9856-90B11C04FAC6.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2_ext1-v1/30000/E22686F4-706F-E511-B999-0025905C4472.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2_ext1-v1/30000/E2A2F3C4-756F-E511-B100-0025905C4472.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2_ext1-v1/30000/E4F5C1BA-756F-E511-A5D1-0025905C445C.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2_ext1-v1/30000/E88C9F48-E46D-E511-87CD-90B11C050395.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2_ext1-v1/30000/EC1F16CB-6B6F-E511-8A13-0025905AC808.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2_ext1-v1/30000/EC3BC2F3-756F-E511-BA8A-0025905AC97A.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2_ext1-v1/30000/EE3CE849-E46D-E511-8528-0025905C446E.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2_ext1-v1/30000/F0249346-E46D-E511-BE98-001517FAAB30.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2_ext1-v1/30000/F23DDCB6-6D6F-E511-BF9D-0025905AC804.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2_ext1-v1/30000/F23F6746-E46D-E511-9976-0025905AC804.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2_ext1-v1/30000/F2B9CED1-706F-E511-A85D-0025905AC806.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2_ext1-v1/30000/F874E4C3-756F-E511-AC88-0025905AC99A.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2_ext1-v1/30000/F8FDB5C1-6D6F-E511-AC20-0025905AC984.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2_ext1-v1/30000/FAF3F2E8-706F-E511-9D2B-0025905C426E.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2_ext1-v1/30000/FC5142B0-6D6F-E511-84A3-0025905C2CC0.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2_ext1-v1/40000/040FE2FF-DD6D-E511-B427-0025905AC982.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2_ext1-v1/40000/064F8D03-DE6D-E511-97E5-0025905AC99A.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2_ext1-v1/40000/06CF0D03-DE6D-E511-BAB3-0025905C4432.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2_ext1-v1/40000/0C04BBA9-E06D-E511-908E-0025905AC97A.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2_ext1-v1/40000/0CA84DB6-DE6D-E511-A6D6-0025905AC804.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2_ext1-v1/40000/0CE30203-DE6D-E511-AB10-0025905C4434.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2_ext1-v1/40000/0E90E9D8-E06D-E511-83B1-0025905AF57E.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2_ext1-v1/40000/103EBC1C-DE6D-E511-9A40-001E67A401B3.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2_ext1-v1/40000/12C2FFEB-E06D-E511-AE46-0025905AC806.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2_ext1-v1/40000/1AA002F9-E06D-E511-96C3-0025905AF57C.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2_ext1-v1/40000/1C5AF7D9-E06D-E511-8442-0025905AC804.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2_ext1-v1/40000/1E7B2509-DE6D-E511-BEE6-001E675A68BF.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2_ext1-v1/40000/1ECF2104-DE6D-E511-AA52-0025905AC97A.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2_ext1-v1/40000/220BF202-DE6D-E511-86DE-0025905AC878.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2_ext1-v1/40000/225E53EC-E06D-E511-8FF9-0025905AF57C.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2_ext1-v1/40000/245B2BBD-DE6D-E511-AE22-0025905AF57E.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2_ext1-v1/40000/28A5E7B2-DE6D-E511-AFFA-0025905AC97A.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2_ext1-v1/40000/2A1AA605-DE6D-E511-A057-001517FB2458.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2_ext1-v1/40000/2A6CCE03-DE6D-E511-92F1-0025905AC808.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2_ext1-v1/40000/2C6019EA-DE6D-E511-9284-0025905AC878.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2_ext1-v1/40000/3407B5B3-DE6D-E511-935A-0025905C445A.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2_ext1-v1/40000/36564000-DE6D-E511-A37F-0025905C22AE.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2_ext1-v1/40000/3AA0FDD8-E06D-E511-AD5B-0025905AC960.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2_ext1-v1/40000/3E3FDEEB-E06D-E511-A88D-0025905AC95E.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2_ext1-v1/40000/40F8E607-DE6D-E511-9C4E-90B11C12E856.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2_ext1-v1/40000/426DDBB2-E06D-E511-B6F2-0025905AC99A.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2_ext1-v1/40000/429B78EC-E06D-E511-8698-0025905C2CC2.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2_ext1-v1/40000/42A399B6-DE6D-E511-8439-0025905AC878.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2_ext1-v1/40000/4A450BB4-DE6D-E511-940C-0025905C22B0.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2_ext1-v1/40000/4A906F00-DE6D-E511-B01B-0025905C22AE.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2_ext1-v1/40000/4AABE703-DE6D-E511-A21C-0025905C4474.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2_ext1-v1/40000/4E855F03-DE6D-E511-B392-0025905AC99A.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2_ext1-v1/40000/4EBB5D0B-DE6D-E511-B113-001E675A6725.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2_ext1-v1/40000/5245B0EB-E06D-E511-8AC0-0025905AC982.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2_ext1-v1/40000/56CFCD01-DE6D-E511-9E4F-0025905AF57C.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2_ext1-v1/40000/5AA1B9B2-DE6D-E511-A9F4-0025905AF57C.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2_ext1-v1/40000/5C6170EC-E06D-E511-B22F-0025905AC99C.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2_ext1-v1/40000/5CE896B7-E06D-E511-866E-0025905AC99A.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2_ext1-v1/40000/600680B3-DE6D-E511-A305-0025905AC960.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2_ext1-v1/40000/60CA0DEC-E06D-E511-8458-0025905AF57C.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2_ext1-v1/40000/6675AA0A-DE6D-E511-8416-001517FB228C.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2_ext1-v1/40000/66830100-DE6D-E511-8E5E-001E67A3EC00.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2_ext1-v1/40000/689C9A00-DE6D-E511-A158-0025905AC95E.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2_ext1-v1/40000/68E7CA02-DE6D-E511-84F9-0025905AC822.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2_ext1-v1/40000/6A35FAC6-E06D-E511-B592-0025905AC960.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2_ext1-v1/40000/6AB97600-DE6D-E511-998B-001E67A40514.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2_ext1-v1/40000/72043DB4-DE6D-E511-B53F-0025905AC982.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2_ext1-v1/40000/727DA50F-DE6D-E511-A85F-001E675A6C2A.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2_ext1-v1/40000/72FF0C03-DE6D-E511-9B25-001E67A3EA11.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2_ext1-v1/40000/784B5004-DE6D-E511-BA06-0025905AC804.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2_ext1-v1/40000/7AE6B600-DE6D-E511-8396-0025905AC95E.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2_ext1-v1/40000/7AE76BED-E06D-E511-B7BC-0025905C445A.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2_ext1-v1/40000/7C4A0803-DE6D-E511-82A0-0025905AC876.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2_ext1-v1/40000/84316E03-DE6D-E511-9AAB-0025905AC97C.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2_ext1-v1/40000/886263B5-DE6D-E511-AFB8-0025905AC824.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2_ext1-v1/40000/8C1B8BB2-DE6D-E511-8591-0025905AF57C.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2_ext1-v1/40000/944FD5ED-E06D-E511-B256-0025905C22B0.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2_ext1-v1/40000/949A9B02-DE6D-E511-860A-0025905C445A.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2_ext1-v1/40000/98099A04-DE6D-E511-9954-E0DB550BA718.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2_ext1-v1/40000/9C5C09B6-DE6D-E511-822C-0025905AC808.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2_ext1-v1/40000/9EDA80B4-DE6D-E511-A4C5-0025905AC824.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2_ext1-v1/40000/A2C81600-DE6D-E511-B5A4-0025905C446E.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2_ext1-v1/40000/A6493502-DE6D-E511-B58E-0025905C445A.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2_ext1-v1/40000/AA286102-DE6D-E511-A2A2-0025905AC982.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2_ext1-v1/40000/AC5F2CC4-E06D-E511-A579-0025905AC878.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2_ext1-v1/40000/AEE413F9-DD6D-E511-807D-001E67A4069F.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2_ext1-v1/40000/B0E3C1B2-DE6D-E511-AC66-0025905AC960.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2_ext1-v1/40000/B27697EB-E06D-E511-BF0C-0025905C445C.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2_ext1-v1/40000/B44A10B3-DE6D-E511-B5C3-0025905C2CC2.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2_ext1-v1/40000/B828C404-DE6D-E511-B7CD-001517FB21BC.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2_ext1-v1/40000/BA85F07F-E16D-E511-927D-0025905AF57C.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2_ext1-v1/40000/C8FE1900-DE6D-E511-A735-001E67A3EC05.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2_ext1-v1/40000/CCE8A6B6-DE6D-E511-AAFF-0025905C42D2.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2_ext1-v1/40000/CED278EC-E06D-E511-92E5-0025905AC824.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2_ext1-v1/40000/D00F59FD-DD6D-E511-B5F4-001E67A40523.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2_ext1-v1/40000/D22DE4B5-DE6D-E511-AB41-0025905C446A.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2_ext1-v1/40000/D235DDB4-DE6D-E511-96D9-0025905AC99A.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2_ext1-v1/40000/D26F69B2-DE6D-E511-8245-0025905C4472.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2_ext1-v1/40000/D4D4C2B5-DE6D-E511-95CF-0025905AC808.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2_ext1-v1/40000/D62C6EB5-DE6D-E511-BB45-0025905AC95E.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2_ext1-v1/40000/DAFA6BED-E06D-E511-AF38-0025905C446E.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2_ext1-v1/40000/DAFE2E33-DE6D-E511-9AB2-001517FB20EC.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2_ext1-v1/40000/DC3229AB-E06D-E511-A8B3-0025905AC960.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2_ext1-v1/40000/DE4905B3-DE6D-E511-9C2D-0025905AF57C.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2_ext1-v1/40000/DE534BFF-DD6D-E511-82D8-0025905AF57C.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2_ext1-v1/40000/E24B2DEC-E06D-E511-A348-0025905AC9AE.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2_ext1-v1/40000/E2CC93BE-E06D-E511-BE14-0025905AC808.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2_ext1-v1/40000/E4A3BDB3-DE6D-E511-A69E-0025905AC960.root', 
        '/store/mc/RunIISpring15MiniAODv2/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/MINIAODSIM/74X_mcRun2_asymptotic_v2_ext1-v1/40000/E4DB15B5-DE6D-E511-9422-0025905AC99A.root' ) )
)
process.HBHENoiseFilterResultProducer = cms.EDProducer("HBHENoiseFilterResultProducer",
    IgnoreTS4TS5ifJetInLowBVRegion = cms.bool(False),
    defaultDecision = cms.string('HBHENoiseFilterResultRun2Loose'),
    minHPDHits = cms.int32(17),
    minHPDNoOtherHits = cms.int32(10),
    minIsolatedNoiseSumE = cms.double(50.0),
    minIsolatedNoiseSumEt = cms.double(25.0),
    minNumIsolatedNoiseChannels = cms.int32(10),
    minZeros = cms.int32(99999),
    noiselabel = cms.InputTag("hcalnoise")
)


process.egmGsfElectronIDs = cms.EDProducer("VersionedGsfElectronIdProducer",
    physicsObjectIDs = cms.VPSet(cms.PSet(
        idDefinition = cms.PSet(
            cutFlow = cms.VPSet(cms.PSet(
                cutName = cms.string('GsfEleMVACut'),
                isIgnored = cms.bool(False),
                mvaCategoriesMapName = cms.InputTag("electronMVAValueMapProducer","ElectronMVAEstimatorRun2Phys14NonTrigCategories"),
                mvaCuts = cms.vdouble(-0.253, 0.081, -0.081, 0.965, 0.917, 
                    0.683),
                mvaValueMapName = cms.InputTag("electronMVAValueMapProducer","ElectronMVAEstimatorRun2Phys14NonTrigValues"),
                needsAdditionalProducts = cms.bool(True)
            )),
            idName = cms.string('mvaEleID-PHYS14-PU20bx25-nonTrig-V1-wp80')
        ),
        idMD5 = cms.string('8b587a6315d6808df7af9d3471d22a20'),
        isPOGApproved = cms.untracked.bool(True)
    ), 
        cms.PSet(
            idDefinition = cms.PSet(
                cutFlow = cms.VPSet(cms.PSet(
                    cutName = cms.string('GsfEleMVACut'),
                    isIgnored = cms.bool(False),
                    mvaCategoriesMapName = cms.InputTag("electronMVAValueMapProducer","ElectronMVAEstimatorRun2Phys14NonTrigCategories"),
                    mvaCuts = cms.vdouble(-0.483, -0.267, -0.323, 0.933, 0.825, 
                        0.337),
                    mvaValueMapName = cms.InputTag("electronMVAValueMapProducer","ElectronMVAEstimatorRun2Phys14NonTrigValues"),
                    needsAdditionalProducts = cms.bool(True)
                )),
                idName = cms.string('mvaEleID-PHYS14-PU20bx25-nonTrig-V1-wp90')
            ),
            idMD5 = cms.string('a01428d36d3d0e6b1f89ab772aa606a1'),
            isPOGApproved = cms.untracked.bool(True)
        )),
    physicsObjectSrc = cms.InputTag("slimmedElectrons")
)


process.electronMVAValueMapProducer = cms.EDProducer("ElectronMVAValueMapProducer",
    mvaConfigurations = cms.VPSet(cms.PSet(
        mvaName = cms.string('ElectronMVAEstimatorRun2Phys14NonTrig'),
        weightFileNames = cms.vstring('RecoEgamma/ElectronIdentification/data/PHYS14/EIDmva_EB1_5_oldscenario2phys14_BDT.weights.xml', 
            'RecoEgamma/ElectronIdentification/data/PHYS14/EIDmva_EB2_5_oldscenario2phys14_BDT.weights.xml', 
            'RecoEgamma/ElectronIdentification/data/PHYS14/EIDmva_EE_5_oldscenario2phys14_BDT.weights.xml', 
            'RecoEgamma/ElectronIdentification/data/PHYS14/EIDmva_EB1_10_oldscenario2phys14_BDT.weights.xml', 
            'RecoEgamma/ElectronIdentification/data/PHYS14/EIDmva_EB2_10_oldscenario2phys14_BDT.weights.xml', 
            'RecoEgamma/ElectronIdentification/data/PHYS14/EIDmva_EE_10_oldscenario2phys14_BDT.weights.xml')
    )),
    src = cms.InputTag("gedGsfElectrons"),
    srcMiniAOD = cms.InputTag("slimmedElectrons","","@skipCurrentProcess")
)


process.patJetCorrFactorsReapplyJECAK4CHS = cms.EDProducer("JetCorrFactorsProducer",
    emf = cms.bool(False),
    extraJPTOffset = cms.string('L1FastJet'),
    flavorType = cms.string('J'),
    levels = cms.vstring('L1FastJet', 
        'L2Relative', 
        'L3Absolute'),
    payload = cms.string('AK4PFchs'),
    primaryVertices = cms.InputTag("offlineSlimmedPrimaryVertices"),
    rho = cms.InputTag("fixedGridRhoFastjetAll"),
    src = cms.InputTag("slimmedJets"),
    useNPV = cms.bool(True),
    useRho = cms.bool(True)
)


process.patJetCorrFactorsReapplyJECPuppi = cms.EDProducer("JetCorrFactorsProducer",
    emf = cms.bool(False),
    extraJPTOffset = cms.string('L1FastJet'),
    flavorType = cms.string('J'),
    levels = cms.vstring('L1FastJet', 
        'L2Relative', 
        'L3Absolute'),
    payload = cms.string('AK4PFPuppi'),
    primaryVertices = cms.InputTag("offlineSlimmedPrimaryVertices"),
    rho = cms.InputTag("fixedGridRhoFastjetAll"),
    src = cms.InputTag("slimmedJetsPuppi"),
    useNPV = cms.bool(True),
    useRho = cms.bool(True)
)


process.patJetsReapplyJECAK4CHS = cms.EDProducer("PATJetUpdater",
    addJetCorrFactors = cms.bool(True),
    jetCorrFactorsSource = cms.VInputTag(cms.InputTag("patJetCorrFactorsReapplyJECAK4CHS")),
    jetSource = cms.InputTag("slimmedJets"),
    userData = cms.PSet(
        userCands = cms.PSet(
            src = cms.VInputTag("")
        ),
        userClasses = cms.PSet(
            src = cms.VInputTag("")
        ),
        userFloats = cms.PSet(
            src = cms.VInputTag("")
        ),
        userFunctionLabels = cms.vstring(),
        userFunctions = cms.vstring(),
        userInts = cms.PSet(
            src = cms.VInputTag("")
        )
    )
)


process.patJetsReapplyJECPuppi = cms.EDProducer("PATJetUpdater",
    addJetCorrFactors = cms.bool(True),
    jetCorrFactorsSource = cms.VInputTag(cms.InputTag("patJetCorrFactorsReapplyJECPuppi")),
    jetSource = cms.InputTag("slimmedJetsPuppi"),
    userData = cms.PSet(
        userCands = cms.PSet(
            src = cms.VInputTag("")
        ),
        userClasses = cms.PSet(
            src = cms.VInputTag("")
        ),
        userFloats = cms.PSet(
            src = cms.VInputTag("")
        ),
        userFunctionLabels = cms.vstring(),
        userFunctions = cms.vstring(),
        userInts = cms.PSet(
            src = cms.VInputTag("")
        )
    )
)


process.skimCounterAll = cms.EDProducer("EventCountProducer")


process.skimCounterPassed = cms.EDProducer("EventCountProducer")


process.dump = cms.EDFilter("MiniAOD2FlatTreeFilter",
    CMEnergy = cms.int32(13),
    CodeVersion = cms.string('9fb56c92654cfdb57399fd4b2bc8fcaae70de574'),
    DataVersion = cms.string('74Xmc'),
    Electrons = cms.VPSet(cms.PSet(
        IDprefix = cms.string('egmGsfElectronIDs'),
        branchName = cms.untracked.string('Electrons'),
        debugMode = cms.untracked.bool(False),
        discriminators = cms.vstring('mvaEleID-PHYS14-PU20bx25-nonTrig-V1-wp80', 
            'mvaEleID-PHYS14-PU20bx25-nonTrig-V1-wp90'),
        rhoSource = cms.InputTag("fixedGridRhoFastjetAll"),
        src = cms.InputTag("slimmedElectrons")
    )),
    EventInfo = cms.PSet(
        LHESrc = cms.untracked.InputTag("externalLHEProducer"),
        OfflinePrimaryVertexSrc = cms.InputTag("offlineSlimmedPrimaryVertices"),
        PileupSummaryInfoSrc = cms.InputTag("slimmedAddPileupInfo"),
        branchName = cms.untracked.string('EventInfo'),
        debugMode = cms.untracked.bool(False)
    ),
    GenJets = cms.VPSet(cms.PSet(
        branchName = cms.untracked.string('GenJets'),
        debugMode = cms.untracked.bool(False),
        saveGenJetConstituents = cms.untracked.bool(False),
        src = cms.InputTag("slimmedGenJets")
    )),
    GenParticles = cms.VPSet(cms.PSet(
        branchName = cms.untracked.string('GenParticles'),
        debugMode = cms.untracked.bool(False),
        saveAllGenParticles = cms.untracked.bool(True),
        saveGenElectrons = cms.untracked.bool(False),
        saveGenMuons = cms.untracked.bool(False),
        saveGenNeutrinos = cms.untracked.bool(False),
        saveGenTaus = cms.untracked.bool(False),
        src = cms.InputTag("prunedGenParticles")
    )),
    GenWeights = cms.VPSet(cms.PSet(
        branchName = cms.untracked.string('GenWeights'),
        debugMode = cms.untracked.bool(False),
        filter = cms.untracked.bool(False),
        src = cms.InputTag("generator")
    )),
    Jets = cms.VPSet(cms.PSet(
        branchName = cms.untracked.string('Jets'),
        debugMode = cms.untracked.bool(False),
        discriminators = cms.vstring('pfJetBProbabilityBJetTags', 
            'pfJetProbabilityBJetTags', 
            'pfCombinedSecondaryVertexBJetTags', 
            'pfCombinedInclusiveSecondaryVertexBJetTags', 
            'pfCombinedInclusiveSecondaryVertexV2BJetTags', 
            'pfCombinedMVABJetTags'),
        jecPayload = cms.string('AK4PFchs'),
        src = cms.InputTag("slimmedJets"),
        userFloats = cms.vstring('pileupJetId:fullDiscriminant')
    ), 
        cms.PSet(
            branchName = cms.untracked.string('JetsPuppi'),
            debugMode = cms.untracked.bool(False),
            discriminators = cms.vstring('pfJetBProbabilityBJetTags', 
                'pfJetProbabilityBJetTags', 
                'pfCombinedSecondaryVertexBJetTags', 
                'pfCombinedInclusiveSecondaryVertexBJetTags', 
                'pfCombinedInclusiveSecondaryVertexV2BJetTags', 
                'pfCombinedMVABJetTags'),
            jecPayload = cms.string('AK4PFPuppi'),
            src = cms.InputTag("slimmedJetsPuppi"),
            userFloats = cms.vstring('pileupJetId:fullDiscriminant')
        )),
    METNoiseFilter = cms.PSet(
        debugMode = cms.untracked.bool(False),
        filtersFromTriggerResults = cms.vstring('Flag_CSCTightHaloFilter', 
            'Flag_goodVertices', 
            'Flag_eeBadScFilter'),
        hbheIsoNoiseTokenSource = cms.InputTag("HBHENoiseFilterResultProducer","HBHEIsoNoiseFilterResult"),
        hbheNoiseTokenRun2LooseSource = cms.InputTag("HBHENoiseFilterResultProducer","HBHENoiseFilterResultRun2Loose"),
        hbheNoiseTokenRun2TightSource = cms.InputTag("HBHENoiseFilterResultProducer","HBHENoiseFilterResultRun2Tight"),
        printTriggerResultsList = cms.untracked.bool(True),
        triggerResults = cms.InputTag("TriggerResults","","PAT")
    ),
    METs = cms.VPSet(cms.PSet(
        branchName = cms.untracked.string('MET_Type1'),
        debugMode = cms.untracked.bool(False),
        src = cms.InputTag("slimmedMETs")
    ), 
        cms.PSet(
            branchName = cms.untracked.string('MET_Type1_NoHF'),
            debugMode = cms.untracked.bool(False),
            src = cms.InputTag("slimmedMETsNoHF")
        ), 
        cms.PSet(
            branchName = cms.untracked.string('MET_Puppi'),
            debugMode = cms.untracked.bool(False),
            src = cms.InputTag("slimmedMETsPuppi")
        )),
    Muons = cms.VPSet(cms.PSet(
        branchName = cms.untracked.string('Muons'),
        debugMode = cms.untracked.bool(False),
        discriminators = cms.vstring(),
        src = cms.InputTag("slimmedMuons")
    )),
    OutputFileName = cms.string('miniAOD2FlatTree.root'),
    PUInfoInputFileName = cms.string('PileUp.root'),
    Skim = cms.PSet(
        Counters = cms.VInputTag("skimCounterAll", "skimCounterPassed")
    ),
    Taus = cms.VPSet(cms.PSet(
        TESvariation = cms.untracked.double(0.03),
        TESvariationExtreme = cms.untracked.double(0.1),
        branchName = cms.untracked.string('Taus'),
        debugMode = cms.untracked.bool(False),
        discriminators = cms.vstring('againstElectronLooseMVA5', 
            'againstElectronMVA5category', 
            'againstElectronMVA5raw', 
            'againstElectronMediumMVA5', 
            'againstElectronTightMVA5', 
            'againstElectronVLooseMVA5', 
            'againstElectronVTightMVA5', 
            'againstMuonLoose3', 
            'againstMuonTight3', 
            'byCombinedIsolationDeltaBetaCorrRaw3Hits', 
            'byIsolationMVA3newDMwLTraw', 
            'byIsolationMVA3oldDMwLTraw', 
            'byLooseCombinedIsolationDeltaBetaCorr3Hits', 
            'byLooseIsolationMVA3newDMwLT', 
            'byLooseIsolationMVA3oldDMwLT', 
            'byLoosePileupWeightedIsolation3Hits', 
            'byMediumCombinedIsolationDeltaBetaCorr3Hits', 
            'byMediumIsolationMVA3newDMwLT', 
            'byMediumIsolationMVA3oldDMwLT', 
            'byMediumPileupWeightedIsolation3Hits', 
            'byPhotonPtSumOutsideSignalCone', 
            'byPileupWeightedIsolationRaw3Hits', 
            'byTightCombinedIsolationDeltaBetaCorr3Hits', 
            'byTightIsolationMVA3newDMwLT', 
            'byTightIsolationMVA3oldDMwLT', 
            'byTightPileupWeightedIsolation3Hits', 
            'byVLooseIsolationMVA3newDMwLT', 
            'byVLooseIsolationMVA3oldDMwLT', 
            'byVTightIsolationMVA3newDMwLT', 
            'byVTightIsolationMVA3oldDMwLT', 
            'byVVTightIsolationMVA3newDMwLT', 
            'byVVTightIsolationMVA3oldDMwLT', 
            'chargedIsoPtSum', 
            'decayModeFinding', 
            'decayModeFindingNewDMs', 
            'footprintCorrection', 
            'neutralIsoPtSum', 
            'neutralIsoPtSumWeight', 
            'photonPtSumOutsideSignalCone', 
            'puCorrPtSum'),
        filter = cms.untracked.bool(False),
        jetSrc = cms.InputTag("slimmedJets"),
        src = cms.InputTag("slimmedTaus")
    )),
    Tracks = cms.VPSet(cms.PSet(
        IPvsPVz = cms.untracked.double(5),
        OfflinePrimaryVertexSrc = cms.InputTag("offlineSlimmedPrimaryVertices"),
        branchName = cms.untracked.string('PFcandidates'),
        debugMode = cms.untracked.bool(False),
        etaCut = cms.untracked.double(2.5),
        ptCut = cms.untracked.double(0.0),
        saveOnlyChargedParticles = cms.untracked.bool(True),
        src = cms.InputTag("packedPFCandidates")
    )),
    Trigger = cms.PSet(
        L1Extra = cms.InputTag("l1extraParticles","MET"),
        TriggerBits = cms.vstring('HLT_Ele22_eta2p1_WPTight_Gsf_v', 
            'HLT_Ele22_eta2p1_WP75_Gsf_v', 
            'HLT_Ele22_eta2p1_WPLoose_Gsf_v', 
            'HLT_IsoMu17_eta2p1_v', 
            'HLT_IsoMu18_v', 
            'HLT_IsoMu20_v', 
            'HLT_IsoMu20_eta2p1_v', 
            'HLT_Mu8_v', 
            'HLT_Mu17_v', 
            'HLT_Mu24_v', 
            'HLT_Mu34_v', 
            'HLT_Dimuon13_PsiPrime_v', 
            'HLT_Dimuon13_Upsilon_v', 
            'HLT_Dimuon20_Jpsi_v', 
            'HLT_Dimuon16_Jpsi_v', 
            'HLT_Dimuon10_Jpsi_Barrel_v', 
            'HLT_Dimuon8_PsiPrime_Barrel_v', 
            'HLT_Dimuon8_Upsilon_Barrel_v', 
            'HLT_Dimuon0_Phi_Barrel_v'),
        TriggerMatch = cms.untracked.vstring('LooseIsoPFTau50_Trk30_eta2p1'),
        TriggerObjects = cms.InputTag("selectedPatTrigger"),
        TriggerResults = cms.InputTag("TriggerResults","","HLT"),
        debugMode = cms.untracked.bool(False),
        filter = cms.untracked.bool(False)
    )
)


process.skim = cms.EDFilter("AnalysisSkim",
    HLTPaths = cms.vstring('HLT_LooseIsoPFTau50_Trk30_eta2p1_MET80_JetIdCleaned_v', 
        'HLT_Mu8_v', 
        'HLT_Mu17_v'),
    JetCollection = cms.InputTag("slimmedJets"),
    JetEtCut = cms.double(20),
    JetEtaCut = cms.double(2.4),
    JetUserFloats = cms.vstring('pileupJetId:fullDiscriminant'),
    NJets = cms.int32(3),
    TriggerResults = cms.InputTag("TriggerResults","","HLT"),
    debugMode = cms.bool(False)
)


process.PUInfo = cms.EDAnalyzer("PUInfo",
    OutputFileName = cms.string('PileUp.root'),
    PileupSummaryInfoSrc = cms.InputTag("slimmedAddPileupInfo"),
    debugMode = cms.untracked.bool(False)
)


process.egmGsfElectronIDSequence = cms.Sequence(process.electronMVAValueMapProducer+process.egmGsfElectronIDs)


process.CustomisationsSequence = cms.Sequence(process.patJetCorrFactorsReapplyJECAK4CHS+process.patJetsReapplyJECAK4CHS+process.patJetCorrFactorsReapplyJECPuppi+process.patJetsReapplyJECPuppi+process.egmGsfElectronIDSequence+process.HBHENoiseFilterResultProducer)


process.runEDFilter = cms.Path(process.CustomisationsSequence+process.dump)


process.MessageLogger = cms.Service("MessageLogger",
    FrameworkJobReport = cms.untracked.PSet(
        FwkJob = cms.untracked.PSet(
            limit = cms.untracked.int32(10000000),
            optionalPSet = cms.untracked.bool(True)
        ),
        default = cms.untracked.PSet(
            limit = cms.untracked.int32(0)
        ),
        optionalPSet = cms.untracked.bool(True)
    ),
    categories = cms.untracked.vstring('FwkJob', 
        'FwkReport', 
        'FwkSummary', 
        'Root_NoDictionary'),
    cerr = cms.untracked.PSet(
        FwkJob = cms.untracked.PSet(
            limit = cms.untracked.int32(0),
            optionalPSet = cms.untracked.bool(True)
        ),
        FwkReport = cms.untracked.PSet(
            limit = cms.untracked.int32(10000000),
            optionalPSet = cms.untracked.bool(True),
            reportEvery = cms.untracked.int32(10)
        ),
        FwkSummary = cms.untracked.PSet(
            limit = cms.untracked.int32(10000000),
            optionalPSet = cms.untracked.bool(True),
            reportEvery = cms.untracked.int32(1)
        ),
        INFO = cms.untracked.PSet(
            limit = cms.untracked.int32(0)
        ),
        Root_NoDictionary = cms.untracked.PSet(
            limit = cms.untracked.int32(0),
            optionalPSet = cms.untracked.bool(True)
        ),
        default = cms.untracked.PSet(
            limit = cms.untracked.int32(10000000)
        ),
        noTimeStamps = cms.untracked.bool(False),
        optionalPSet = cms.untracked.bool(True),
        threshold = cms.untracked.string('INFO')
    ),
    cerr_stats = cms.untracked.PSet(
        optionalPSet = cms.untracked.bool(True),
        output = cms.untracked.string('cerr'),
        threshold = cms.untracked.string('WARNING')
    ),
    cout = cms.untracked.PSet(
        placeholder = cms.untracked.bool(True)
    ),
    debugModules = cms.untracked.vstring(),
    debugs = cms.untracked.PSet(
        placeholder = cms.untracked.bool(True)
    ),
    default = cms.untracked.PSet(

    ),
    destinations = cms.untracked.vstring('warnings', 
        'errors', 
        'infos', 
        'debugs', 
        'cout', 
        'cerr'),
    errors = cms.untracked.PSet(
        placeholder = cms.untracked.bool(True)
    ),
    fwkJobReports = cms.untracked.vstring('FrameworkJobReport'),
    infos = cms.untracked.PSet(
        Root_NoDictionary = cms.untracked.PSet(
            limit = cms.untracked.int32(0),
            optionalPSet = cms.untracked.bool(True)
        ),
        optionalPSet = cms.untracked.bool(True),
        placeholder = cms.untracked.bool(True)
    ),
    statistics = cms.untracked.vstring('cerr_stats'),
    suppressDebug = cms.untracked.vstring(),
    suppressInfo = cms.untracked.vstring(),
    suppressWarning = cms.untracked.vstring(),
    warnings = cms.untracked.PSet(
        placeholder = cms.untracked.bool(True)
    )
)


process.CastorDbProducer = cms.ESProducer("CastorDbProducer")


process.EcalLaserCorrectionService = cms.ESProducer("EcalLaserCorrectionService")


process.SiStripRecHitMatcherESProducer = cms.ESProducer("SiStripRecHitMatcherESProducer",
    ComponentName = cms.string('StandardMatcher'),
    NSigmaInside = cms.double(3.0),
    PreFilter = cms.bool(False)
)


process.StripCPEfromTrackAngleESProducer = cms.ESProducer("StripCPEESProducer",
    ComponentName = cms.string('StripCPEfromTrackAngle'),
    ComponentType = cms.string('StripCPEfromTrackAngle'),
    parameters = cms.PSet(
        mLC_P0 = cms.double(-0.326),
        mLC_P1 = cms.double(0.618),
        mLC_P2 = cms.double(0.3),
        mTEC_P0 = cms.double(-1.885),
        mTEC_P1 = cms.double(0.471),
        mTIB_P0 = cms.double(-0.742),
        mTIB_P1 = cms.double(0.202),
        mTID_P0 = cms.double(-1.427),
        mTID_P1 = cms.double(0.433),
        mTOB_P0 = cms.double(-1.026),
        mTOB_P1 = cms.double(0.253),
        maxChgOneMIP = cms.double(6000.0),
        useLegacyError = cms.bool(False)
    )
)


process.hcal_db_producer = cms.ESProducer("HcalDbProducer",
    dump = cms.untracked.vstring(''),
    file = cms.untracked.string('')
)


process.siPixelQualityESProducer = cms.ESProducer("SiPixelQualityESProducer",
    ListOfRecordToMerge = cms.VPSet(cms.PSet(
        record = cms.string('SiPixelQualityFromDbRcd'),
        tag = cms.string('')
    ), 
        cms.PSet(
            record = cms.string('SiPixelDetVOffRcd'),
            tag = cms.string('')
        ))
)


process.siStripBackPlaneCorrectionDepESProducer = cms.ESProducer("SiStripBackPlaneCorrectionDepESProducer",
    BackPlaneCorrectionDeconvMode = cms.PSet(
        label = cms.untracked.string('deconvolution'),
        record = cms.string('SiStripBackPlaneCorrectionRcd')
    ),
    BackPlaneCorrectionPeakMode = cms.PSet(
        label = cms.untracked.string('peak'),
        record = cms.string('SiStripBackPlaneCorrectionRcd')
    ),
    LatencyRecord = cms.PSet(
        label = cms.untracked.string(''),
        record = cms.string('SiStripLatencyRcd')
    )
)


process.siStripGainESProducer = cms.ESProducer("SiStripGainESProducer",
    APVGain = cms.VPSet(cms.PSet(
        Label = cms.untracked.string(''),
        NormalizationFactor = cms.untracked.double(1.0),
        Record = cms.string('SiStripApvGainRcd')
    ), 
        cms.PSet(
            Label = cms.untracked.string(''),
            NormalizationFactor = cms.untracked.double(1.0),
            Record = cms.string('SiStripApvGain2Rcd')
        )),
    AutomaticNormalization = cms.bool(False),
    appendToDataLabel = cms.string(''),
    printDebug = cms.untracked.bool(False)
)


process.siStripLorentzAngleDepESProducer = cms.ESProducer("SiStripLorentzAngleDepESProducer",
    LatencyRecord = cms.PSet(
        label = cms.untracked.string(''),
        record = cms.string('SiStripLatencyRcd')
    ),
    LorentzAngleDeconvMode = cms.PSet(
        label = cms.untracked.string('deconvolution'),
        record = cms.string('SiStripLorentzAngleRcd')
    ),
    LorentzAnglePeakMode = cms.PSet(
        label = cms.untracked.string('peak'),
        record = cms.string('SiStripLorentzAngleRcd')
    )
)


process.siStripQualityESProducer = cms.ESProducer("SiStripQualityESProducer",
    ListOfRecordToMerge = cms.VPSet(cms.PSet(
        record = cms.string('SiStripDetVOffRcd'),
        tag = cms.string('')
    ), 
        cms.PSet(
            record = cms.string('SiStripDetCablingRcd'),
            tag = cms.string('')
        ), 
        cms.PSet(
            record = cms.string('RunInfoRcd'),
            tag = cms.string('')
        ), 
        cms.PSet(
            record = cms.string('SiStripBadChannelRcd'),
            tag = cms.string('')
        ), 
        cms.PSet(
            record = cms.string('SiStripBadFiberRcd'),
            tag = cms.string('')
        ), 
        cms.PSet(
            record = cms.string('SiStripBadModuleRcd'),
            tag = cms.string('')
        ), 
        cms.PSet(
            record = cms.string('SiStripBadStripRcd'),
            tag = cms.string('')
        )),
    PrintDebugOutput = cms.bool(False),
    ReduceGranularity = cms.bool(False),
    ThresholdForReducedGranularity = cms.double(0.3),
    UseEmptyRunInfo = cms.bool(False),
    appendToDataLabel = cms.string('')
)


process.sistripconn = cms.ESProducer("SiStripConnectivity")


process.stripCPEESProducer = cms.ESProducer("StripCPEESProducer",
    ComponentName = cms.string('stripCPE'),
    ComponentType = cms.string('SimpleStripCPE'),
    parameters = cms.PSet(

    )
)


process.GlobalTag = cms.ESSource("PoolDBESSource",
    DBParameters = cms.PSet(
        authenticationPath = cms.untracked.string(''),
        authenticationSystem = cms.untracked.int32(0),
        connectionRetrialPeriod = cms.untracked.int32(10),
        connectionRetrialTimeOut = cms.untracked.int32(60),
        connectionTimeOut = cms.untracked.int32(60),
        enableConnectionSharing = cms.untracked.bool(True),
        enablePoolAutomaticCleanUp = cms.untracked.bool(False),
        enableReadOnlySessionOnUpdateConnection = cms.untracked.bool(False),
        idleConnectionCleanupPeriod = cms.untracked.int32(10),
        messageLevel = cms.untracked.int32(0)
    ),
    connect = cms.string('frontier://FrontierProd/CMS_CONDITIONS'),
    globaltag = cms.string('74X_mcRun2_asymptotic_v4'),
    toGet = cms.VPSet()
)


process.es_hardcode = cms.ESSource("HcalHardcodeCalibrations",
    GainWidthsForTrigPrims = cms.bool(False),
    HERecalibration = cms.bool(False),
    HEreCalibCutoff = cms.double(20.0),
    HFRecalibration = cms.bool(False),
    HcalReLabel = cms.PSet(
        RelabelHits = cms.untracked.bool(False),
        RelabelRules = cms.untracked.PSet(
            CorrectPhi = cms.untracked.bool(False),
            Eta1 = cms.untracked.vint32(1, 2, 2, 2, 3, 
                3, 3, 3, 3, 3, 
                3, 3, 3, 3, 3, 
                3, 3, 3, 3),
            Eta16 = cms.untracked.vint32(1, 1, 2, 2, 2, 
                2, 2, 2, 2, 3, 
                3, 3, 3, 3, 3, 
                3, 3, 3, 3),
            Eta17 = cms.untracked.vint32(1, 1, 2, 2, 3, 
                3, 3, 4, 4, 4, 
                4, 4, 5, 5, 5, 
                5, 5, 5, 5)
        )
    ),
    hcalTopologyConstants = cms.PSet(
        maxDepthHB = cms.int32(2),
        maxDepthHE = cms.int32(3),
        mode = cms.string('HcalTopologyMode::LHC')
    ),
    iLumi = cms.double(-1.0),
    toGet = cms.untracked.vstring('GainWidths')
)


process.prefer("es_hardcode")

process.CondDBSetup = cms.PSet(
    DBParameters = cms.PSet(
        authenticationPath = cms.untracked.string(''),
        authenticationSystem = cms.untracked.int32(0),
        connectionRetrialPeriod = cms.untracked.int32(10),
        connectionRetrialTimeOut = cms.untracked.int32(60),
        connectionTimeOut = cms.untracked.int32(60),
        enableConnectionSharing = cms.untracked.bool(True),
        enablePoolAutomaticCleanUp = cms.untracked.bool(False),
        enableReadOnlySessionOnUpdateConnection = cms.untracked.bool(False),
        idleConnectionCleanupPeriod = cms.untracked.int32(10),
        messageLevel = cms.untracked.int32(0)
    )
)

process.HcalReLabel = cms.PSet(
    RelabelHits = cms.untracked.bool(False),
    RelabelRules = cms.untracked.PSet(
        CorrectPhi = cms.untracked.bool(False),
        Eta1 = cms.untracked.vint32(1, 2, 2, 2, 3, 
            3, 3, 3, 3, 3, 
            3, 3, 3, 3, 3, 
            3, 3, 3, 3),
        Eta16 = cms.untracked.vint32(1, 1, 2, 2, 2, 
            2, 2, 2, 2, 3, 
            3, 3, 3, 3, 3, 
            3, 3, 3, 3),
        Eta17 = cms.untracked.vint32(1, 1, 2, 2, 3, 
            3, 3, 4, 4, 4, 
            4, 4, 5, 5, 5, 
            5, 5, 5, 5)
    )
)

process.JECpayloadAK4PFPuppi = cms.PSet(
    payload = cms.string('AK4PFPuppi')
)

process.JECpayloadAK4PFchs = cms.PSet(
    payload = cms.string('AK4PFchs')
)

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(100)
)

process.mvaEleID_PHYS14_PU20bx25_nonTrig_V1_producer_config = cms.PSet(
    mvaName = cms.string('ElectronMVAEstimatorRun2Phys14NonTrig'),
    weightFileNames = cms.vstring('RecoEgamma/ElectronIdentification/data/PHYS14/EIDmva_EB1_5_oldscenario2phys14_BDT.weights.xml', 
        'RecoEgamma/ElectronIdentification/data/PHYS14/EIDmva_EB2_5_oldscenario2phys14_BDT.weights.xml', 
        'RecoEgamma/ElectronIdentification/data/PHYS14/EIDmva_EE_5_oldscenario2phys14_BDT.weights.xml', 
        'RecoEgamma/ElectronIdentification/data/PHYS14/EIDmva_EB1_10_oldscenario2phys14_BDT.weights.xml', 
        'RecoEgamma/ElectronIdentification/data/PHYS14/EIDmva_EB2_10_oldscenario2phys14_BDT.weights.xml', 
        'RecoEgamma/ElectronIdentification/data/PHYS14/EIDmva_EE_10_oldscenario2phys14_BDT.weights.xml')
)

process.mvaEleID_PHYS14_PU20bx25_nonTrig_V1_wp80 = cms.PSet(
    cutFlow = cms.VPSet(cms.PSet(
        cutName = cms.string('GsfEleMVACut'),
        isIgnored = cms.bool(False),
        mvaCategoriesMapName = cms.InputTag("electronMVAValueMapProducer","ElectronMVAEstimatorRun2Phys14NonTrigCategories"),
        mvaCuts = cms.vdouble(-0.253, 0.081, -0.081, 0.965, 0.917, 
            0.683),
        mvaValueMapName = cms.InputTag("electronMVAValueMapProducer","ElectronMVAEstimatorRun2Phys14NonTrigValues"),
        needsAdditionalProducts = cms.bool(True)
    )),
    idName = cms.string('mvaEleID-PHYS14-PU20bx25-nonTrig-V1-wp80')
)

process.mvaEleID_PHYS14_PU20bx25_nonTrig_V1_wp90 = cms.PSet(
    cutFlow = cms.VPSet(cms.PSet(
        cutName = cms.string('GsfEleMVACut'),
        isIgnored = cms.bool(False),
        mvaCategoriesMapName = cms.InputTag("electronMVAValueMapProducer","ElectronMVAEstimatorRun2Phys14NonTrigCategories"),
        mvaCuts = cms.vdouble(-0.483, -0.267, -0.323, 0.933, 0.825, 
            0.337),
        mvaValueMapName = cms.InputTag("electronMVAValueMapProducer","ElectronMVAEstimatorRun2Phys14NonTrigValues"),
        needsAdditionalProducts = cms.bool(True)
    )),
    idName = cms.string('mvaEleID-PHYS14-PU20bx25-nonTrig-V1-wp90')
)

process.options = cms.untracked.PSet(
    SkipEvent = cms.untracked.vstring('ProductNotFound'),
    printDependencies = cms.untracked.bool(False),
    wantSummary = cms.untracked.bool(False)
)

process.Electrons = cms.VPSet(cms.PSet(
    IDprefix = cms.string('egmGsfElectronIDs'),
    branchName = cms.untracked.string('Electrons'),
    debugMode = cms.untracked.bool(False),
    discriminators = cms.vstring('mvaEleID-PHYS14-PU20bx25-nonTrig-V1-wp80', 
        'mvaEleID-PHYS14-PU20bx25-nonTrig-V1-wp90'),
    rhoSource = cms.InputTag("fixedGridRhoFastjetAll"),
    src = cms.InputTag("slimmedElectrons")
))

process.Jets = cms.VPSet(cms.PSet(
    branchName = cms.untracked.string('Jets'),
    debugMode = cms.untracked.bool(False),
    discriminators = cms.vstring('pfJetBProbabilityBJetTags', 
        'pfJetProbabilityBJetTags', 
        'pfCombinedSecondaryVertexBJetTags', 
        'pfCombinedInclusiveSecondaryVertexBJetTags', 
        'pfCombinedInclusiveSecondaryVertexV2BJetTags', 
        'pfCombinedMVABJetTags'),
    jecPayload = cms.string('AK4PFchs'),
    src = cms.InputTag("slimmedJets"),
    userFloats = cms.vstring('pileupJetId:fullDiscriminant')
), 
    cms.PSet(
        branchName = cms.untracked.string('JetsPuppi'),
        debugMode = cms.untracked.bool(False),
        discriminators = cms.vstring('pfJetBProbabilityBJetTags', 
            'pfJetProbabilityBJetTags', 
            'pfCombinedSecondaryVertexBJetTags', 
            'pfCombinedInclusiveSecondaryVertexBJetTags', 
            'pfCombinedInclusiveSecondaryVertexV2BJetTags', 
            'pfCombinedMVABJetTags'),
        jecPayload = cms.string('AK4PFPuppi'),
        src = cms.InputTag("slimmedJetsPuppi"),
        userFloats = cms.vstring('pileupJetId:fullDiscriminant')
    ))

process.METs = cms.VPSet(cms.PSet(
    branchName = cms.untracked.string('MET_Type1'),
    debugMode = cms.untracked.bool(False),
    src = cms.InputTag("slimmedMETs")
), 
    cms.PSet(
        branchName = cms.untracked.string('MET_Type1_NoHF'),
        debugMode = cms.untracked.bool(False),
        src = cms.InputTag("slimmedMETsNoHF")
    ), 
    cms.PSet(
        branchName = cms.untracked.string('MET_Puppi'),
        debugMode = cms.untracked.bool(False),
        src = cms.InputTag("slimmedMETsPuppi")
    ))

process.Muons = cms.VPSet(cms.PSet(
    branchName = cms.untracked.string('Muons'),
    debugMode = cms.untracked.bool(False),
    discriminators = cms.vstring(),
    src = cms.InputTag("slimmedMuons")
))

process.Taus = cms.VPSet(cms.PSet(
    TESvariation = cms.untracked.double(0.03),
    TESvariationExtreme = cms.untracked.double(0.1),
    branchName = cms.untracked.string('Taus'),
    debugMode = cms.untracked.bool(False),
    discriminators = cms.vstring('againstElectronLooseMVA5', 
        'againstElectronMVA5category', 
        'againstElectronMVA5raw', 
        'againstElectronMediumMVA5', 
        'againstElectronTightMVA5', 
        'againstElectronVLooseMVA5', 
        'againstElectronVTightMVA5', 
        'againstMuonLoose3', 
        'againstMuonTight3', 
        'byCombinedIsolationDeltaBetaCorrRaw3Hits', 
        'byIsolationMVA3newDMwLTraw', 
        'byIsolationMVA3oldDMwLTraw', 
        'byLooseCombinedIsolationDeltaBetaCorr3Hits', 
        'byLooseIsolationMVA3newDMwLT', 
        'byLooseIsolationMVA3oldDMwLT', 
        'byLoosePileupWeightedIsolation3Hits', 
        'byMediumCombinedIsolationDeltaBetaCorr3Hits', 
        'byMediumIsolationMVA3newDMwLT', 
        'byMediumIsolationMVA3oldDMwLT', 
        'byMediumPileupWeightedIsolation3Hits', 
        'byPhotonPtSumOutsideSignalCone', 
        'byPileupWeightedIsolationRaw3Hits', 
        'byTightCombinedIsolationDeltaBetaCorr3Hits', 
        'byTightIsolationMVA3newDMwLT', 
        'byTightIsolationMVA3oldDMwLT', 
        'byTightPileupWeightedIsolation3Hits', 
        'byVLooseIsolationMVA3newDMwLT', 
        'byVLooseIsolationMVA3oldDMwLT', 
        'byVTightIsolationMVA3newDMwLT', 
        'byVTightIsolationMVA3oldDMwLT', 
        'byVVTightIsolationMVA3newDMwLT', 
        'byVVTightIsolationMVA3oldDMwLT', 
        'chargedIsoPtSum', 
        'decayModeFinding', 
        'decayModeFindingNewDMs', 
        'footprintCorrection', 
        'neutralIsoPtSum', 
        'neutralIsoPtSumWeight', 
        'photonPtSumOutsideSignalCone', 
        'puCorrPtSum'),
    filter = cms.untracked.bool(False),
    jetSrc = cms.InputTag("slimmedJets"),
    src = cms.InputTag("slimmedTaus")
))

process.mvaConfigsForEleProducer = cms.VPSet(cms.PSet(
    mvaName = cms.string('ElectronMVAEstimatorRun2Phys14NonTrig'),
    weightFileNames = cms.vstring('RecoEgamma/ElectronIdentification/data/PHYS14/EIDmva_EB1_5_oldscenario2phys14_BDT.weights.xml', 
        'RecoEgamma/ElectronIdentification/data/PHYS14/EIDmva_EB2_5_oldscenario2phys14_BDT.weights.xml', 
        'RecoEgamma/ElectronIdentification/data/PHYS14/EIDmva_EE_5_oldscenario2phys14_BDT.weights.xml', 
        'RecoEgamma/ElectronIdentification/data/PHYS14/EIDmva_EB1_10_oldscenario2phys14_BDT.weights.xml', 
        'RecoEgamma/ElectronIdentification/data/PHYS14/EIDmva_EB2_10_oldscenario2phys14_BDT.weights.xml', 
        'RecoEgamma/ElectronIdentification/data/PHYS14/EIDmva_EE_10_oldscenario2phys14_BDT.weights.xml')
))

