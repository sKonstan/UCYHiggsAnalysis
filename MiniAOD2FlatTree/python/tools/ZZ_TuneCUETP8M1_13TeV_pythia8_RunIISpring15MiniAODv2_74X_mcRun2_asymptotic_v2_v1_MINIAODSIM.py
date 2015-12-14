import FWCore.ParameterSet.Config as cms

readFiles = cms.untracked.vstring()
secFiles = cms.untracked.vstring() 
readFiles.extend( [
       '/store/mc/RunIISpring15MiniAODv2/ZZ_TuneCUETP8M1_13TeV-pythia8/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/10000/28E57E8A-4071-E511-B930-0025905C42B6.root',
       '/store/mc/RunIISpring15MiniAODv2/ZZ_TuneCUETP8M1_13TeV-pythia8/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/10000/2AF00951-3771-E511-AB96-0025905A60E4.root',
       '/store/mc/RunIISpring15MiniAODv2/ZZ_TuneCUETP8M1_13TeV-pythia8/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/10000/32363EBB-4071-E511-A1E7-0025905C3D6A.root',
       '/store/mc/RunIISpring15MiniAODv2/ZZ_TuneCUETP8M1_13TeV-pythia8/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/10000/32576851-3771-E511-966B-0025905B8598.root',
       '/store/mc/RunIISpring15MiniAODv2/ZZ_TuneCUETP8M1_13TeV-pythia8/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/10000/4248E1BE-4071-E511-967D-0025905C94D0.root',
       '/store/mc/RunIISpring15MiniAODv2/ZZ_TuneCUETP8M1_13TeV-pythia8/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/10000/A0DE7685-4071-E511-A205-0025904C66A4.root',
       '/store/mc/RunIISpring15MiniAODv2/ZZ_TuneCUETP8M1_13TeV-pythia8/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/10000/A22AC48A-4071-E511-A1D0-0025904C6214.root',
       '/store/mc/RunIISpring15MiniAODv2/ZZ_TuneCUETP8M1_13TeV-pythia8/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/10000/AEE78E88-4071-E511-9DAA-0025904C6624.root',
       '/store/mc/RunIISpring15MiniAODv2/ZZ_TuneCUETP8M1_13TeV-pythia8/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/60000/002CA8FD-4074-E511-BE05-6C3BE5B594A0.root',
       '/store/mc/RunIISpring15MiniAODv2/ZZ_TuneCUETP8M1_13TeV-pythia8/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/60000/0CF88DF1-3271-E511-B39A-002354EF3BE1.root',
       '/store/mc/RunIISpring15MiniAODv2/ZZ_TuneCUETP8M1_13TeV-pythia8/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/60000/2006AF18-3271-E511-804E-0025905B8592.root',
       '/store/mc/RunIISpring15MiniAODv2/ZZ_TuneCUETP8M1_13TeV-pythia8/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/60000/228C3F14-3271-E511-BF24-00261894388F.root',
       '/store/mc/RunIISpring15MiniAODv2/ZZ_TuneCUETP8M1_13TeV-pythia8/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/60000/266D4546-A572-E511-B921-0025904C66A4.root',
       '/store/mc/RunIISpring15MiniAODv2/ZZ_TuneCUETP8M1_13TeV-pythia8/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/60000/36024F47-A572-E511-A451-0025905C3E38.root',
       '/store/mc/RunIISpring15MiniAODv2/ZZ_TuneCUETP8M1_13TeV-pythia8/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/60000/449AA91A-3271-E511-B1D4-0025905A6132.root',
       '/store/mc/RunIISpring15MiniAODv2/ZZ_TuneCUETP8M1_13TeV-pythia8/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/60000/44F5DBF0-3271-E511-B8E7-00261894380D.root',
       '/store/mc/RunIISpring15MiniAODv2/ZZ_TuneCUETP8M1_13TeV-pythia8/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/60000/6413C8D0-3271-E511-A956-0025905A612C.root',
       '/store/mc/RunIISpring15MiniAODv2/ZZ_TuneCUETP8M1_13TeV-pythia8/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/60000/A2D2C845-A572-E511-B430-0025905C94D0.root',
       '/store/mc/RunIISpring15MiniAODv2/ZZ_TuneCUETP8M1_13TeV-pythia8/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/60000/A8834648-A572-E511-8492-0025904C6378.root',
       '/store/mc/RunIISpring15MiniAODv2/ZZ_TuneCUETP8M1_13TeV-pythia8/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/60000/AC56E31B-3271-E511-AA32-00259059642E.root',
       '/store/mc/RunIISpring15MiniAODv2/ZZ_TuneCUETP8M1_13TeV-pythia8/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/60000/C62DFEF5-3271-E511-B041-0025905A612A.root',
       '/store/mc/RunIISpring15MiniAODv2/ZZ_TuneCUETP8M1_13TeV-pythia8/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/60000/DA9527F6-3271-E511-9E31-00259059642E.root',
       '/store/mc/RunIISpring15MiniAODv2/ZZ_TuneCUETP8M1_13TeV-pythia8/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/60000/DAAE7116-3271-E511-B799-002618943923.root',
       '/store/mc/RunIISpring15MiniAODv2/ZZ_TuneCUETP8M1_13TeV-pythia8/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/60000/E42E1BF1-3271-E511-84FC-002354EF3BE2.root',
       '/store/mc/RunIISpring15MiniAODv2/ZZ_TuneCUETP8M1_13TeV-pythia8/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/60000/F0017BF3-3271-E511-A3F9-00261894392B.root',
       '/store/mc/RunIISpring15MiniAODv2/ZZ_TuneCUETP8M1_13TeV-pythia8/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/60000/F24D9126-3271-E511-9070-00261894388F.root' ] );


secFiles.extend( [
               ] )
