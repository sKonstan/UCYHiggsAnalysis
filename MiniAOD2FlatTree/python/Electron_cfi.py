import FWCore.ParameterSet.Config as cms

Electrons = cms.VPSet(
    cms.PSet(
        branchName     = cms.untracked.string("Electrons"),
        src            = cms.InputTag("slimmedElectrons"),
        rhoSource      = cms.InputTag("fixedGridRhoFastjetAll"), # for PU mitigation in isolation
        IDprefix       = cms.string("egmGsfElectronIDs"),
        debugMode      = cms.untracked.bool(False),
        discriminators = cms.vstring(
            "mvaEleID-PHYS14-PU20bx25-nonTrig-V1-wp80",
            "mvaEleID-PHYS14-PU20bx25-nonTrig-V1-wp90")
        )
    )
