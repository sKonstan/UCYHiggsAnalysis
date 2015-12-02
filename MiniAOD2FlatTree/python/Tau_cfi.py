import FWCore.ParameterSet.Config as cms
Taus = cms.VPSet(
    cms.PSet(
        branchName     = cms.untracked.string("Taus"),
        src            = cms.InputTag("slimmedTaus"),
        debugMode      = cms.untracked.bool(True),
        discriminators = cms.vstring(
            'againstElectronLooseMVA5',
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
            "puCorrPtSum"
            ),
        filter              = cms.untracked.bool(False), 
        jetSrc              = cms.InputTag("slimmedJets"), # made from ak4PFJetsCHS
        TESvariation        = cms.untracked.double(0.03),  # Tau Energy Scale Variation (Up/Down)
        TESvariationExtreme = cms.untracked.double(0.10)   # Extreme Tau Energy Scale Variation (Up/Down)
        )
    )

