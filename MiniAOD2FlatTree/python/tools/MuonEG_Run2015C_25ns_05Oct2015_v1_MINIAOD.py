import FWCore.ParameterSet.Config as cms

maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )
readFiles = cms.untracked.vstring()
secFiles = cms.untracked.vstring() 
source = cms.Source ("PoolSource",fileNames = readFiles, secondaryFileNames = secFiles)
readFiles.extend( [
       '/store/data/Run2015C_25ns/MuonEG/MINIAOD/05Oct2015-v1/40000/20021F19-0E74-E511-AD11-0025905A60B0.root',
       '/store/data/Run2015C_25ns/MuonEG/MINIAOD/05Oct2015-v1/40000/5E4C8F2F-0E74-E511-B69E-0025905A4964.root',
       '/store/data/Run2015C_25ns/MuonEG/MINIAOD/05Oct2015-v1/40000/D8A17218-0E74-E511-9257-00261894390B.root' ] );


secFiles.extend( [
               ] )
