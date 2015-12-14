import FWCore.ParameterSet.Config as cms

readFiles = cms.untracked.vstring()
secFiles = cms.untracked.vstring() 
readFiles.extend( [
       '/store/mc/RunIISpring15MiniAODv2/WZ_TuneCUETP8M1_13TeV-pythia8/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/30000/06181A51-9072-E511-88C0-3306CB18721E.root',
       '/store/mc/RunIISpring15MiniAODv2/WZ_TuneCUETP8M1_13TeV-pythia8/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/30000/08475733-9072-E511-A614-002618943940.root',
       '/store/mc/RunIISpring15MiniAODv2/WZ_TuneCUETP8M1_13TeV-pythia8/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/30000/0897873A-9072-E511-84BC-002590AB3A70.root',
       '/store/mc/RunIISpring15MiniAODv2/WZ_TuneCUETP8M1_13TeV-pythia8/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/30000/0AECFA51-9072-E511-8CBB-E73DA8D27AAC.root',
       '/store/mc/RunIISpring15MiniAODv2/WZ_TuneCUETP8M1_13TeV-pythia8/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/30000/0C152859-9072-E511-AFBD-AD998D63ED84.root',
       '/store/mc/RunIISpring15MiniAODv2/WZ_TuneCUETP8M1_13TeV-pythia8/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/30000/0EE94C4A-9072-E511-94F1-35D3DE6D921E.root',
       '/store/mc/RunIISpring15MiniAODv2/WZ_TuneCUETP8M1_13TeV-pythia8/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/30000/14F69057-9072-E511-8AB5-C9B8EB2BE848.root',
       '/store/mc/RunIISpring15MiniAODv2/WZ_TuneCUETP8M1_13TeV-pythia8/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/30000/1CC17A4A-9072-E511-B749-194D46C77A10.root',
       '/store/mc/RunIISpring15MiniAODv2/WZ_TuneCUETP8M1_13TeV-pythia8/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/30000/247F69D1-4572-E511-8318-0CC47A4D99D6.root',
       '/store/mc/RunIISpring15MiniAODv2/WZ_TuneCUETP8M1_13TeV-pythia8/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/30000/2EE856D1-8F72-E511-8B67-90B11CBCFF75.root',
       '/store/mc/RunIISpring15MiniAODv2/WZ_TuneCUETP8M1_13TeV-pythia8/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/30000/56286064-9072-E511-B74E-E35D8D25FB81.root',
       '/store/mc/RunIISpring15MiniAODv2/WZ_TuneCUETP8M1_13TeV-pythia8/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/30000/586DE362-9072-E511-B883-DFAC82931378.root',
       '/store/mc/RunIISpring15MiniAODv2/WZ_TuneCUETP8M1_13TeV-pythia8/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/30000/5CF16C7E-9072-E511-8616-D39631F858F8.root',
       '/store/mc/RunIISpring15MiniAODv2/WZ_TuneCUETP8M1_13TeV-pythia8/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/30000/72F59EB2-6572-E511-88FB-002590D60194.root',
       '/store/mc/RunIISpring15MiniAODv2/WZ_TuneCUETP8M1_13TeV-pythia8/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/30000/8A4916E7-4872-E511-ABDF-782BCB161F1B.root',
       '/store/mc/RunIISpring15MiniAODv2/WZ_TuneCUETP8M1_13TeV-pythia8/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/30000/8C401B15-9072-E511-AF8E-C56AFF7FC67F.root',
       '/store/mc/RunIISpring15MiniAODv2/WZ_TuneCUETP8M1_13TeV-pythia8/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/30000/8E75A148-9072-E511-8CE6-112EDC9B6124.root',
       '/store/mc/RunIISpring15MiniAODv2/WZ_TuneCUETP8M1_13TeV-pythia8/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/30000/92F88255-5272-E511-87E6-001EC9ADCD52.root',
       '/store/mc/RunIISpring15MiniAODv2/WZ_TuneCUETP8M1_13TeV-pythia8/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/30000/947E3159-9072-E511-B6D7-41FD034DA343.root',
       '/store/mc/RunIISpring15MiniAODv2/WZ_TuneCUETP8M1_13TeV-pythia8/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/30000/96EDDA52-9072-E511-AAA2-D7A8B273C9A0.root',
       '/store/mc/RunIISpring15MiniAODv2/WZ_TuneCUETP8M1_13TeV-pythia8/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/30000/A2AA3E53-9072-E511-A6E4-6DDB9B71C636.root',
       '/store/mc/RunIISpring15MiniAODv2/WZ_TuneCUETP8M1_13TeV-pythia8/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/30000/A809424A-9072-E511-9DAE-F7A6B1C233CD.root',
       '/store/mc/RunIISpring15MiniAODv2/WZ_TuneCUETP8M1_13TeV-pythia8/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/30000/B2540357-9072-E511-892C-C1F43BB44447.root',
       '/store/mc/RunIISpring15MiniAODv2/WZ_TuneCUETP8M1_13TeV-pythia8/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/30000/B80CED45-9072-E511-BE7E-FD52C2416123.root',
       '/store/mc/RunIISpring15MiniAODv2/WZ_TuneCUETP8M1_13TeV-pythia8/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/30000/C2B378DC-8F72-E511-8D52-001E6739AC71.root',
       '/store/mc/RunIISpring15MiniAODv2/WZ_TuneCUETP8M1_13TeV-pythia8/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/30000/C407905F-9072-E511-B5B9-CB1E3B284CD1.root',
       '/store/mc/RunIISpring15MiniAODv2/WZ_TuneCUETP8M1_13TeV-pythia8/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/30000/C4A1CFE6-4872-E511-B659-0CC47A01CB76.root',
       '/store/mc/RunIISpring15MiniAODv2/WZ_TuneCUETP8M1_13TeV-pythia8/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/30000/CCE81B59-9072-E511-BC19-B5863A132260.root',
       '/store/mc/RunIISpring15MiniAODv2/WZ_TuneCUETP8M1_13TeV-pythia8/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/30000/F2EBFF9B-9072-E511-9BF7-BF7E3A861FDE.root' ] );


secFiles.extend( [
               ] )
