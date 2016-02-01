
// -*- c++ -*-
// This file has been auto-generated with HiggsAnalysis/NtupleAnalysis/scripts/hplusGenerateDataFormats.py

#include "DataFormat/interface/ElectronGenerated.h"

#include "Framework/interface/BranchManager.h"

void ElectronGeneratedCollection::setupBranches(BranchManager& mgr) {
  ParticleCollection::setupBranches(mgr);
  fMCelectron.setupBranches(mgr);

  mgr.book(prefix()+"_mvaEleID_PHYS14_PU20bx25_nonTrig_V1_wp80", &fMvaEleID_PHYS14_PU20bx25_nonTrig_V1_wp80);
  mgr.book(prefix()+"_mvaEleID_PHYS14_PU20bx25_nonTrig_V1_wp90", &fMvaEleID_PHYS14_PU20bx25_nonTrig_V1_wp90);
  mgr.book(prefix()+"_relIsoDeltaBeta", &fRelIsoDeltaBeta);

  mgr.book(prefix()+"_isPF", &fIsPF);
  mgr.book(prefix()+"_ecalIso", &fEcalIso);
  mgr.book(prefix()+"_hcalIso", &fHcalIso);
  mgr.book(prefix()+"_caloIso", &fCaloIso);
  mgr.book(prefix()+"_trackIso", &fTrackIso);
  // mgr.book(prefix()+"_pt_MCelectron", &fPt_MCelectron);
  // mgr.book(prefix()+"_eta_MCelectron", &fEta_MCelectron);
  // mgr.book(prefix()+"_phi_MCelectron", &fPhi_MCelectron);
  // mgr.book(prefix()+"_e_MCelectron", &fE_MCelectron);

}
