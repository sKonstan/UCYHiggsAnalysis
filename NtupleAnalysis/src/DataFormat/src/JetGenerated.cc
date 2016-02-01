
// -*- c++ -*-
// This file has been auto-generated with HiggsAnalysis/NtupleAnalysis/scripts/hplusGenerateDataFormats.py

#include "DataFormat/interface/JetGenerated.h"

#include "Framework/interface/BranchManager.h"

void JetGeneratedCollection::setupBranches(BranchManager& mgr) {
  ParticleCollection::setupBranches(mgr);
  fMCjet.setupBranches(mgr);

  mgr.book(prefix()+"_IDloose", &fIDloose);
  mgr.book(prefix()+"_IDtight", &fIDtight);
  mgr.book(prefix()+"_IDtightLeptonVeto", &fIDtightLeptonVeto);
  mgr.book(prefix()+"_PUIDloose", &fPUIDloose);
  mgr.book(prefix()+"_PUIDmedium", &fPUIDmedium);
  mgr.book(prefix()+"_PUIDtight", &fPUIDtight);
  mgr.book(prefix()+"_pileupJetIdfullDiscriminant", &fPileupJetIdfullDiscriminant);
  mgr.book(prefix()+"_pfCombinedInclusiveSecondaryVertexV2BJetTags", &fPfCombinedInclusiveSecondaryVertexV2BJetTags);
  mgr.book(prefix()+"_pfCombinedMVABJetTags", &fPfCombinedMVABJetTags);
  mgr.book(prefix()+"_pfJetBProbabilityBJetTags", &fPfJetBProbabilityBJetTags);
  mgr.book(prefix()+"_pfJetProbabilityBJetTags", &fPfJetProbabilityBJetTags);
  mgr.book(prefix()+"_hadronFlavour", &fHadronFlavour);
  mgr.book(prefix()+"_partonFlavour", &fPartonFlavour);
  mgr.book(prefix()+"_combinedSecondaryVertexBJetTags"            , &fCombinedSecondaryVertexBJetTags);
  mgr.book(prefix()+"_pfTrackCountingHighPurBJetTags"             , &fPfTrackCountingHighPurBJetTags);
  mgr.book(prefix()+"_pfTrackCountingHighEffBJetTags"             , &fPfTrackCountingHighEffBJetTags);
  mgr.book(prefix()+"_pfSimpleSecondaryVertexHighEffBJetTags"     , &fPfSimpleSecondaryVertexHighEffBJetTags);
  mgr.book(prefix()+"_pfSimpleSecondaryVertexHighPurBJetTags"     , &fPfSimpleSecondaryVertexHighPurBJetTags);
  mgr.book(prefix()+"_pfCombinedSecondaryVertexV2BJetTags"        , &fPfCombinedSecondaryVertexV2BJetTags);
  mgr.book(prefix()+"_pfCombinedSecondaryVertexSoftLeptonBJetTags", &fPfCombinedSecondaryVertexSoftLeptonBJetTags);
  mgr.book(prefix()+"_isBasicJet", &fIsBasicJet);
  mgr.book(prefix()+"_isCaloJet" , &fIsCaloJet);
  mgr.book(prefix()+"_isJPTJet"  , &fIsJPTJet);
  mgr.book(prefix()+"_isPFJet"   , &fIsPFJet);
  mgr.book(prefix()+"_neutralHadronEnergyFraction" , &fNeutralHadronEnergyFraction);
  mgr.book(prefix()+"_neutralEmEnergyFraction"     , &fNeutralEmEnergyFraction);
  mgr.book(prefix()+"_nConstituents"               , &fNConstituents);
  mgr.book(prefix()+"_chargedHadronMultiplicity"   , &fChargedHadronMultiplicity);
  mgr.book(prefix()+"_pt_JESup"   , &fPt_JESup);
  mgr.book(prefix()+"_eta_JESup"  , &fEta_JESup);
  mgr.book(prefix()+"_phi_JESup"  , &fPhi_JESup);
  mgr.book(prefix()+"_e_JESup"    , &fE_JESup);
  mgr.book(prefix()+"_pt_JESdown" , &fPt_JESdown);
  mgr.book(prefix()+"_eta_JESdown", &fEta_JESdown);
  mgr.book(prefix()+"_phi_JESdown", &fPhi_JESdown);
  mgr.book(prefix()+"_e_JESdown"  , &fE_JESdown);
  mgr.book(prefix()+"_pt_JERup"   , &fPt_JERup);
  mgr.book(prefix()+"_eta_JERup"  , &fEta_JERup);
  mgr.book(prefix()+"_phi_JERup"  , &fPhi_JERup);
  mgr.book(prefix()+"_e_JERup"    , &fE_JERup);
  mgr.book(prefix()+"_pt_JERdown" , &fPt_JERdown);
  mgr.book(prefix()+"_eta_JERdown", &fEta_JERdown);
  mgr.book(prefix()+"_phi_JERdown", &fPhi_JERdown);
  mgr.book(prefix()+"_e_JERdown"  , &fE_JERdown);

  
}


