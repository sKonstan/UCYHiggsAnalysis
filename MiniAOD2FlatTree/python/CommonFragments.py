import FWCore.ParameterSet.Config as cms

''''
Usage Instructions:
1) Import this module
2) Call produceCustomisations just before cms.Path
3) Add process.CustomisationsSequence to the cms.Path

Example:
process.myEDFilter = cms.EDFilter('MyEDFilter')

from HiggsAnalysis.MiniAOD2FlatTree.CommonFragments import produceCustomisations
produceCustomisations(process) 
process.runEDFilter = cms.Path(process.CustomisationsSequence * process.myEDFilter)

'''


def produceCustomisations(process):
    '''
    Module that produces all process customisations:
    1) Reproduces Jet Energy Corrections (JEC)
    2) Reproduces Electron ID
    3) Reproduces MET noise filters
    '''
    print "=== CommonFragments.py:\n\tProducing customisations (JEC, Electron ID, MET Noise Filters)"
    
    process.CustomisationsSequence = cms.Sequence()
    reproduceJEC(process)
    reproduceElectronID(process)
    reproduceMETNoiseFilters(process)
    print "=== CommonFragments.py:\n\tCustomisations done\n"

    return


def reproduceJEC(process):
    '''
    Module that reproduces jet collections with the latest Jet Energy Corrections (JEC). Creates new colletions!
    For more details see https://twiki.cern.ch/twiki/bin/view/CMSPublic/WorkBookJetEnergyCorrections#CorrPatJets
    '''    
    print "=== CommonFragments.py:\n\tReproducing jet collections with latest JEC"
    
    from PhysicsTools.PatAlgos.producersLayer1.jetUpdater_cff import patJetCorrFactorsUpdated
    # PF AK4CHS jets
    if not hasattr(process, "JECpayloadAK4PFchs"):
        raise Exception("Error: Could not access process.JECpayloadAK4PFchs! Please load Jet_cfi.py before calling customizations")
    process.patJetCorrFactorsReapplyJECAK4CHS = patJetCorrFactorsUpdated.clone(
      src = cms.InputTag("slimmedJets"),
      levels = ['L1FastJet', 'L2Relative', 'L3Absolute'],
      payload = process.JECpayloadAK4PFchs.payload,  # Set in Jet_cfi.py
    ) 
    from PhysicsTools.PatAlgos.producersLayer1.jetUpdater_cff import patJetsUpdated
    process.patJetsReapplyJECAK4CHS = patJetsUpdated.clone(
      jetSource = cms.InputTag("slimmedJets"),
      jetCorrFactorsSource = cms.VInputTag(cms.InputTag("patJetCorrFactorsReapplyJECAK4CHS"))
    )

    # PUPPI jets
    if not hasattr(process, "JECpayloadAK4PFPuppi"):
        raise Exception("Error: Could not access process.JECpayloadAK4PFPuppi! Please load Jet_cfi.py before calling customizations")
    process.patJetCorrFactorsReapplyJECPuppi = patJetCorrFactorsUpdated.clone(
      src = cms.InputTag("slimmedJetsPuppi"),
      levels = ['L1FastJet', 'L2Relative', 'L3Absolute'],
      payload = process.JECpayloadAK4PFPuppi.payload,  # Set in Jet_cfi.py
    )
    from PhysicsTools.PatAlgos.producersLayer1.jetUpdater_cff import patJetsUpdated
    process.patJetsReapplyJECPuppi = patJetsUpdated.clone(
      jetSource = cms.InputTag("slimmedJetsPuppi"), 
      jetCorrFactorsSource = cms.VInputTag(cms.InputTag("patJetCorrFactorsReapplyJECPuppi"))
    )

    # Add processes to the sequence 
    process.CustomisationsSequence += process.patJetCorrFactorsReapplyJECAK4CHS
    process.CustomisationsSequence += process.patJetsReapplyJECAK4CHS
    process.CustomisationsSequence += process.patJetCorrFactorsReapplyJECPuppi
    process.CustomisationsSequence += process.patJetsReapplyJECPuppi

    return


from PhysicsTools.SelectorUtils.tools.vid_id_tools import *
def reproduceElectronID(process):
    ''' Module that sets up the electron identification (VID framework). Creates new mva discriminators
    
    For more details see:    
    https://twiki.cern.ch/twiki/bin/view/CMS/MultivariateElectronIdentificationRun2

    For more cut-based electron ID see:    
    https://twiki.cern.ch/twiki/bin/view/CMS/CutBasedElectronIdentificationRun2

    For example see:
    https://github.com/ikrav/EgammaWork/blob/ntupler_and_VID_demos_7.4.12/ElectronNtupler/test/runElectrons_VID_MVA_Spring15_25ns_NonTrig_demo.py
    '''
    print "=== CommonFragments.py:\n\tReproducing electron ID discriminators"

    # Turn on the VID electron ID producer (extra options for PAT and/or MINIAOD)
    switchOnVIDElectronIdProducer(process, DataFormat.MiniAOD)

    # Define which IDs we want to produce
    #my_id_modules = ['RecoEgamma.ElectronIdentification.Identification.mvaElectronID_Spring15_25ns_nonTrig_V1_cff']
    my_id_modules = ['RecoEgamma.ElectronIdentification.Identification.mvaElectronID_PHYS14_PU20bx25_nonTrig_V1_cff']
        
    
    # Add the electron IDs to the VID producer
    for idmod in my_id_modules:
        setupAllVIDIdsInModule(process, idmod, setupVIDElectronSelection)

    process.load("RecoEgamma.ElectronIdentification.ElectronMVAValueMapProducer_cfi") #fixme: needed?
    
    # Add process to the sequence 
    process.CustomisationsSequence += process.egmGsfElectronIDSequence

    return


def reproduceMETNoiseFilters(process):
    '''
    Module sets up the HCAL Barrel (HB) and HCAL Endcap (HE) noise filters. Creates new colletions
    
    For more details see:
    https://twiki.cern.ch/twiki/bin/viewauth/CMS/MissingETOptionalFiltersRun2
    '''
    print "=== CommonFragments.py:\n\tReproducing HBHE noise filter"
    
    process.load('CommonTools.RecoAlgos.HBHENoiseFilterResultProducer_cfi')
    process.HBHENoiseFilterResultProducer.minZeros = cms.int32(99999)
    process.HBHENoiseFilterResultProducer.IgnoreTS4TS5ifJetInLowBVRegion=cms.bool(False)
    process.HBHENoiseFilterResultProducer.defaultDecision = cms.string("HBHENoiseFilterResultRun2Loose")

    # Do not apply EDfilters for HBHE noise, the discriminators for them are saved into the ttree
    # Add process to the sequence 
    process.CustomisationsSequence += process.HBHENoiseFilterResultProducer

    return
