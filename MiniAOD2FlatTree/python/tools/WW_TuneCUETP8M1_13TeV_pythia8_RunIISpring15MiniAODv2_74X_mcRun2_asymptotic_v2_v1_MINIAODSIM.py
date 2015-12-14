import FWCore.ParameterSet.Config as cms

readFiles = cms.untracked.vstring()
secFiles = cms.untracked.vstring() 
readFiles.extend( [
       '/store/mc/RunIISpring15MiniAODv2/WW_TuneCUETP8M1_13TeV-pythia8/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/10000/CC5DF8C0-E374-E511-B05C-90E6BA5CB1D4.root',
       '/store/mc/RunIISpring15MiniAODv2/WW_TuneCUETP8M1_13TeV-pythia8/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/60000/00D5DA18-3476-E511-95F5-90E6BA5CBB3C.root',
       '/store/mc/RunIISpring15MiniAODv2/WW_TuneCUETP8M1_13TeV-pythia8/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/60000/04C1A83D-3376-E511-844B-6C626DAA87C9.root',
       '/store/mc/RunIISpring15MiniAODv2/WW_TuneCUETP8M1_13TeV-pythia8/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/60000/0CC54526-CE71-E511-A88C-B083FED04276.root',
       '/store/mc/RunIISpring15MiniAODv2/WW_TuneCUETP8M1_13TeV-pythia8/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/60000/108B5CED-3576-E511-9EFD-50E549336049.root',
       '/store/mc/RunIISpring15MiniAODv2/WW_TuneCUETP8M1_13TeV-pythia8/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/60000/2870BE97-3176-E511-80A1-00241DB7C4B4.root',
       '/store/mc/RunIISpring15MiniAODv2/WW_TuneCUETP8M1_13TeV-pythia8/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/60000/289D2371-3476-E511-9C79-90E6BA5CAE1C.root',
       '/store/mc/RunIISpring15MiniAODv2/WW_TuneCUETP8M1_13TeV-pythia8/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/60000/3642FDCD-3176-E511-851A-001F2908BEFA.root',
       '/store/mc/RunIISpring15MiniAODv2/WW_TuneCUETP8M1_13TeV-pythia8/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/60000/4261E0E8-3576-E511-87B4-6C626DAA87C9.root',
       '/store/mc/RunIISpring15MiniAODv2/WW_TuneCUETP8M1_13TeV-pythia8/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/60000/4A482E36-8D71-E511-8BB7-02163E0151BE.root',
       '/store/mc/RunIISpring15MiniAODv2/WW_TuneCUETP8M1_13TeV-pythia8/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/60000/50FAAA47-3376-E511-A8F3-90E6BA5CBB3C.root',
       '/store/mc/RunIISpring15MiniAODv2/WW_TuneCUETP8M1_13TeV-pythia8/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/60000/6282216D-AB72-E511-BE19-001EC9B21556.root',
       '/store/mc/RunIISpring15MiniAODv2/WW_TuneCUETP8M1_13TeV-pythia8/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/60000/6299A9FE-3076-E511-9130-44A842CFC9CC.root',
       '/store/mc/RunIISpring15MiniAODv2/WW_TuneCUETP8M1_13TeV-pythia8/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/60000/6EAA296E-2174-E511-AE8D-002590207984.root',
       '/store/mc/RunIISpring15MiniAODv2/WW_TuneCUETP8M1_13TeV-pythia8/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/60000/7C33E90A-3176-E511-B76D-B499BAAC3786.root',
       '/store/mc/RunIISpring15MiniAODv2/WW_TuneCUETP8M1_13TeV-pythia8/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/60000/8089DCEF-3576-E511-86C3-40618699A07E.root',
       '/store/mc/RunIISpring15MiniAODv2/WW_TuneCUETP8M1_13TeV-pythia8/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/60000/96D2E1F5-3476-E511-B1FA-001A4D4FBE7B.root',
       '/store/mc/RunIISpring15MiniAODv2/WW_TuneCUETP8M1_13TeV-pythia8/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/60000/98525C3C-3376-E511-9A27-90E6BA5CB960.root',
       '/store/mc/RunIISpring15MiniAODv2/WW_TuneCUETP8M1_13TeV-pythia8/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/60000/A6B1D01F-DC71-E511-A42C-28924A35059A.root',
       '/store/mc/RunIISpring15MiniAODv2/WW_TuneCUETP8M1_13TeV-pythia8/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/60000/AAE0DDF4-3576-E511-AAEC-90E6BA5CBB68.root',
       '/store/mc/RunIISpring15MiniAODv2/WW_TuneCUETP8M1_13TeV-pythia8/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/60000/ACF1FD1B-3176-E511-887E-B499BAAC0414.root',
       '/store/mc/RunIISpring15MiniAODv2/WW_TuneCUETP8M1_13TeV-pythia8/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/60000/B6F8D360-3276-E511-AE0C-90E6BA5CB930.root',
       '/store/mc/RunIISpring15MiniAODv2/WW_TuneCUETP8M1_13TeV-pythia8/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/60000/BE71C5E6-3476-E511-872E-50E549336064.root',
       '/store/mc/RunIISpring15MiniAODv2/WW_TuneCUETP8M1_13TeV-pythia8/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/60000/D216A00B-3176-E511-8FF8-001E0BECB5C0.root',
       '/store/mc/RunIISpring15MiniAODv2/WW_TuneCUETP8M1_13TeV-pythia8/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/60000/D450ADF4-3076-E511-ADC7-001F29084160.root',
       '/store/mc/RunIISpring15MiniAODv2/WW_TuneCUETP8M1_13TeV-pythia8/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/60000/DC012B45-3176-E511-9D59-6C3BE5B5F218.root',
       '/store/mc/RunIISpring15MiniAODv2/WW_TuneCUETP8M1_13TeV-pythia8/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/60000/E6F6C65E-3176-E511-8059-6C3BE5B52368.root',
       '/store/mc/RunIISpring15MiniAODv2/WW_TuneCUETP8M1_13TeV-pythia8/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/60000/F0AB3941-3176-E511-8043-B499BAAC0626.root',
       '/store/mc/RunIISpring15MiniAODv2/WW_TuneCUETP8M1_13TeV-pythia8/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/60000/F6425923-3376-E511-AEEC-6C626DAA87C9.root' ] );


secFiles.extend( [
               ] )
