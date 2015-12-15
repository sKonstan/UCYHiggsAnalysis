import FWCore.ParameterSet.Config as cms

process = cms.Process("MiniAOD2FlatTree")

process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring('/store/mc/RunIISpring15MiniAODv2/ST_s-channel_4f_leptonDecays_13TeV-amcatnlo-pythia8_TuneCUETP8M1/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/50000/12DCEE99-C56D-E511-AA75-08606E15EABA.root', 
        '/store/mc/RunIISpring15MiniAODv2/ST_s-channel_4f_leptonDecays_13TeV-amcatnlo-pythia8_TuneCUETP8M1/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/50000/249EA2A1-C76D-E511-BBC6-3085A9262DA0.root', 
        '/store/mc/RunIISpring15MiniAODv2/ST_s-channel_4f_leptonDecays_13TeV-amcatnlo-pythia8_TuneCUETP8M1/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/50000/2ABAF8BC-C56D-E511-86C0-08606E17C77E.root', 
        '/store/mc/RunIISpring15MiniAODv2/ST_s-channel_4f_leptonDecays_13TeV-amcatnlo-pythia8_TuneCUETP8M1/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/50000/3037C502-C76D-E511-88A9-7824AFAE696F.root', 
        '/store/mc/RunIISpring15MiniAODv2/ST_s-channel_4f_leptonDecays_13TeV-amcatnlo-pythia8_TuneCUETP8M1/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/50000/34C62EC0-C66D-E511-9DDB-08606E15EABA.root', 
        '/store/mc/RunIISpring15MiniAODv2/ST_s-channel_4f_leptonDecays_13TeV-amcatnlo-pythia8_TuneCUETP8M1/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/50000/4A29A1F2-C66D-E511-BA65-08606E15EABA.root', 
        '/store/mc/RunIISpring15MiniAODv2/ST_s-channel_4f_leptonDecays_13TeV-amcatnlo-pythia8_TuneCUETP8M1/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/50000/5AA8E358-C66D-E511-B0CF-F46D042E833B.root', 
        '/store/mc/RunIISpring15MiniAODv2/ST_s-channel_4f_leptonDecays_13TeV-amcatnlo-pythia8_TuneCUETP8M1/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/50000/5C09A7A4-C76D-E511-BF37-08606E15E9AE.root', 
        '/store/mc/RunIISpring15MiniAODv2/ST_s-channel_4f_leptonDecays_13TeV-amcatnlo-pythia8_TuneCUETP8M1/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/50000/5C43A46A-C56D-E511-A68A-F46D042E833B.root', 
        '/store/mc/RunIISpring15MiniAODv2/ST_s-channel_4f_leptonDecays_13TeV-amcatnlo-pythia8_TuneCUETP8M1/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/50000/780FDDC7-C46D-E511-A152-D8D385FF18C4.root', 
        '/store/mc/RunIISpring15MiniAODv2/ST_s-channel_4f_leptonDecays_13TeV-amcatnlo-pythia8_TuneCUETP8M1/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/50000/84BA46E6-C66D-E511-89FE-002618943BF9.root', 
        '/store/mc/RunIISpring15MiniAODv2/ST_s-channel_4f_leptonDecays_13TeV-amcatnlo-pythia8_TuneCUETP8M1/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/50000/886062C3-C46D-E511-9D57-34E6D7E387A8.root', 
        '/store/mc/RunIISpring15MiniAODv2/ST_s-channel_4f_leptonDecays_13TeV-amcatnlo-pythia8_TuneCUETP8M1/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/50000/8AE4F60B-C66D-E511-9AC6-3085A9262DA0.root', 
        '/store/mc/RunIISpring15MiniAODv2/ST_s-channel_4f_leptonDecays_13TeV-amcatnlo-pythia8_TuneCUETP8M1/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/50000/947A13FA-C56D-E511-A9A5-F46D043B3D41.root', 
        '/store/mc/RunIISpring15MiniAODv2/ST_s-channel_4f_leptonDecays_13TeV-amcatnlo-pythia8_TuneCUETP8M1/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/50000/9C3CB4F9-C46D-E511-AB13-F46D043B3D41.root', 
        '/store/mc/RunIISpring15MiniAODv2/ST_s-channel_4f_leptonDecays_13TeV-amcatnlo-pythia8_TuneCUETP8M1/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/50000/9CFD6044-C66D-E511-86CD-08606E15E9AE.root', 
        '/store/mc/RunIISpring15MiniAODv2/ST_s-channel_4f_leptonDecays_13TeV-amcatnlo-pythia8_TuneCUETP8M1/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/50000/A2BED061-C76D-E511-9AFE-E03F49D6226B.root', 
        '/store/mc/RunIISpring15MiniAODv2/ST_s-channel_4f_leptonDecays_13TeV-amcatnlo-pythia8_TuneCUETP8M1/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/50000/AE542E18-C66D-E511-BAAF-F46D043B3D41.root', 
        '/store/mc/RunIISpring15MiniAODv2/ST_s-channel_4f_leptonDecays_13TeV-amcatnlo-pythia8_TuneCUETP8M1/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/50000/B270BDC9-C46D-E511-95E1-B499BAABCF0E.root', 
        '/store/mc/RunIISpring15MiniAODv2/ST_s-channel_4f_leptonDecays_13TeV-amcatnlo-pythia8_TuneCUETP8M1/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/50000/C4FF999A-C66D-E511-90F4-BCEE7B2FE01D.root', 
        '/store/mc/RunIISpring15MiniAODv2/ST_s-channel_4f_leptonDecays_13TeV-amcatnlo-pythia8_TuneCUETP8M1/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/50000/C8FAEB9D-C76D-E511-8AF1-BCEE7B2FE01D.root', 
        '/store/mc/RunIISpring15MiniAODv2/ST_s-channel_4f_leptonDecays_13TeV-amcatnlo-pythia8_TuneCUETP8M1/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/50000/D2A16942-C76D-E511-BAFB-F46D042E833B.root', 
        '/store/mc/RunIISpring15MiniAODv2/ST_s-channel_4f_leptonDecays_13TeV-amcatnlo-pythia8_TuneCUETP8M1/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/50000/D65E0A4F-C76D-E511-A3E6-08606E17C77E.root')
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
    CodeVersion = cms.string('c79cef45219b1666ade96651e45157260e0c4865'),
    DataVersion = cms.string('74Xdata'),
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
        triggerResults = cms.InputTag("TriggerResults","","RECO")
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
        TriggerBits = cms.vstring('HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_v', 
            'HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ_v', 
            'HLT_IsoMu20_v', 
            'HLT_IsoTkMu20_v', 
            'HLT_Ele17_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_v', 
            'HLT_Ele23_WPLoose_Gsf_v', 
            'HLT_Ele23_CaloIdL_TrackIdL_IsoVL_v', 
            'HLT_Mu17_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_v', 
            'HLT_Mu8_TrkIsoVVL_Ele17_CaloIdL_TrackIdL_IsoVL_v', 
            'HLT_IsoMu20_v', 
            'HLT_IsoTkMu20_v', 
            'HLT_Ele23_WPLoose_Gsf_v', 
            'HLT_Ele23_CaloIdL_TrackIdL_IsoVL_v', 
            'HLT_DiMu9_Ele9_CaloIdL_TrackIdL_v', 
            'HLT_Mu8_DiEle12_CaloIdL_TrackIdL_v', 
            'HLT_TripleMu_12_10_5_v', 
            'HLT_Ele16_Ele12_Ele8_CaloIdL_TrackIdL_v', 
            'HLT_Mu17_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_v', 
            'HLT_Mu8_TrkIsoVVL_Ele17_CaloIdL_TrackIdL_IsoVL_v', 
            'HLT_Ele17_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_v', 
            'HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_v', 
            'HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ_v', 
            'HLT_IsoMu20_v', 
            'HLT_IsoTkMu20_v', 
            'HLT_Ele23_WPLoose_Gsf_v', 
            'HLT_Ele23_CaloIdL_TrackIdL_IsoVL_v'),
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
    globaltag = cms.string('74X_dataRun2_Prompt_v4'),
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
    input = cms.untracked.int32(5000)
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

