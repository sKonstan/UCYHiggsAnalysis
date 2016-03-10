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
        branchName     = cms.untracked.string("PFCHSJets"), 
        debugMode      = cms.untracked.bool(False),
        src            = cms.InputTag("slimmedJets"), #patJetsReapplyJECAK4CHS # made from ak4PFJetsCHS
        jecPayload     = JECpayloadAK4PFchs.payload,
        discriminators = cms.vstring(
            "combinedSecondaryVertexBJetTags",
            "pfJetBProbabilityBJetTags",
            "pfJetProbabilityBJetTags", 
            "pfTrackCountingHighPurBJetTags",
            "pfTrackCountingHighEffBJetTags",
            "pfSimpleSecondaryVertexHighEffBJetTags", 
            "pfSimpleSecondaryVertexHighPurBJetTags", 
            "pfCombinedSecondaryVertexV2BJetTags",
            "pfCombinedInclusiveSecondaryVertexV2BJetTags",
            "pfCombinedSecondaryVertexSoftLeptonBJetTags", #empty?
            "pfCombinedMVABJetTags",
            ),
        userFloats = cms.vstring(
            "pileupJetId:fullDiscriminant"
            ),
        ),

    #ms.PSet(
    #   branchName     = cms.untracked.string("PuppiJets"),
    #   debugMode      = cms.untracked.bool(False),
    #   src            = cms.InputTag("slimmedJetsPuppi"), #patJetsReapplyJECPuppi # made from ak4PFJets
    #   jecPayload     = JECpayloadAK4PFPuppi.payload,
    #   discriminators = cms.vstring(
    #       "combinedSecondaryVertexBJetTags",
    #       "pfJetBProbabilityBJetTags",
    #       "pfJetProbabilityBJetTags", 
    #       "pfTrackCountingHighPurBJetTags",
    #       "pfTrackCountingHighEffBJetTags",
    #       "pfSimpleSecondaryVertexHighEffBJetTags", 
    #       "pfSimpleSecondaryVertexHighPurBJetTags", 
    #       "pfCombinedSecondaryVertexV2BJetTags",
    #       "pfCombinedInclusiveSecondaryVertexV2BJetTags",
    #       "pfCombinedSecondaryVertexSoftLeptonBJetTags", #empty?
    #       "pfCombinedMVABJetTags",
    #       ),
    #   userFloats = cms.vstring(
    #       "pileupJetId:fullDiscriminant"
    #       ),
    #   )

    )
