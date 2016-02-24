
// -*- c++ -*-
// This file has been auto-generated with HiggsAnalysis/NtupleAnalysis/scripts/hplusGenerateDataFormats.py

#include "DataFormat/interface/MuonGenerated.h"

#include "Framework/interface/BranchManager.h"

void MuonGeneratedCollection::setupBranches(BranchManager& mgr) {
  ParticleCollection::setupBranches(mgr);
  fMCmuon.setupBranches(mgr);

  mgr.book(prefix()+"_TrgMatch_HLT_DiMu9_Ele9_CaloIdL_TrackIdL_vx", &fTrgMatch_HLT_DiMu9_Ele9_CaloIdL_TrackIdL_vx);
  mgr.book(prefix()+"_TrgMatch_HLT_IsoMu20_vx", &fTrgMatch_HLT_IsoMu20_vx);
  mgr.book(prefix()+"_TrgMatch_HLT_IsoTkMu20_vx", &fTrgMatch_HLT_IsoTkMu20_vx);
  mgr.book(prefix()+"_TrgMatch_HLT_Mu17_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_vx", &fTrgMatch_HLT_Mu17_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_vx);
  mgr.book(prefix()+"_TrgMatch_HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_vx", &fTrgMatch_HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_vx);
  mgr.book(prefix()+"_TrgMatch_HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ_vx", &fTrgMatch_HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ_vx);
  mgr.book(prefix()+"_TrgMatch_HLT_Mu8_DiEle12_CaloIdL_TrackIdL_vx", &fTrgMatch_HLT_Mu8_DiEle12_CaloIdL_TrackIdL_vx);
  mgr.book(prefix()+"_TrgMatch_HLT_Mu8_TrkIsoVVL_Ele17_CaloIdL_TrackIdL_IsoVL_vx", &fTrgMatch_HLT_Mu8_TrkIsoVVL_Ele17_CaloIdL_TrackIdL_IsoVL_vx);
  mgr.book(prefix()+"_TrgMatch_HLT_TripleMu_12_10_5_vx", &fTrgMatch_HLT_TripleMu_12_10_5_vx);
  mgr.book(prefix()+"_isGlobalMuon", &fIsGlobalMuon);
  mgr.book(prefix()+"_muIDLoose", &fMuIDLoose);
  mgr.book(prefix()+"_muIDMedium", &fMuIDMedium);
  mgr.book(prefix()+"_muIDTight", &fMuIDTight);
  mgr.book(prefix()+"_caloIso", &fCaloIso);
  mgr.book(prefix()+"_ecalIso", &fEcalIso);
  mgr.book(prefix()+"_hcalIso", &fHcalIso);
  mgr.book(prefix()+"_relIsoDeltaBeta", &fRelIsoDeltaBeta);
}
