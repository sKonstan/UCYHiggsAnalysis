import FWCore.ParameterSet.Config as cms

# Workaround: use PSets because this module is loaded
JECpayloadAK4PFchs = cms.PSet(
    payload = cms.string("AK4PFchs")
    )

JECpayloadAK4PFPuppi = cms.PSet(
    payload = cms.string("AK4PFPuppi")
    )

Jets = cms.VPSet(
    cms.PSet(
        branchName     = cms.untracked.string("Jets"),
        debugMode      = cms.untracked.bool(False),
        src            = cms.InputTag("slimmedJets"), #patJetsReapplyJECAK4CHS # made from ak4PFJetsCHS
        jecPayload     = JECpayloadAK4PFchs.payload,
        discriminators = cms.vstring(
            "pfJetBProbabilityBJetTags",
            "pfJetProbabilityBJetTags",
            "pfCombinedSecondaryVertexBJetTags",
            "pfCombinedInclusiveSecondaryVertexBJetTags",
            #"combinedInclusiveSecondaryVertexV2BJetTags", # for 72x
            "pfCombinedInclusiveSecondaryVertexV2BJetTags", # for 74x
            "pfCombinedMVABJetTags",
            ),
        userFloats = cms.vstring(
            "pileupJetId:fullDiscriminant"
            ),
        ),

    cms.PSet(
        branchName     = cms.untracked.string("JetsPuppi"),
        debugMode      = cms.untracked.bool(False),
        src            = cms.InputTag("slimmedJetsPuppi"), #patJetsReapplyJECPuppi # made from ak4PFJets
        jecPayload     = JECpayloadAK4PFPuppi.payload,
        discriminators = cms.vstring(
            "pfJetBProbabilityBJetTags",
            "pfJetProbabilityBJetTags",
            "pfCombinedSecondaryVertexBJetTags",
            "pfCombinedInclusiveSecondaryVertexBJetTags",
            #"combinedInclusiveSecondaryVertexV2BJetTags", # for 72x
            "pfCombinedInclusiveSecondaryVertexV2BJetTags", # for 74x
            "pfCombinedMVABJetTags",
            ),
        userFloats = cms.vstring(
            "pileupJetId:fullDiscriminant"
            ),
        )
    )
