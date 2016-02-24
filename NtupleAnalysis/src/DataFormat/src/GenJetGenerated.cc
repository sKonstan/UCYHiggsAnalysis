
// -*- c++ -*-
// This file has been auto-generated with HiggsAnalysis/NtupleAnalysis/scripts/hplusGenerateDataFormats.py

#include "DataFormat/interface/GenJetGenerated.h"

#include "Framework/interface/BranchManager.h"

void GenJetGeneratedCollection::setupBranches(BranchManager& mgr) {
  ParticleCollection::setupBranches(mgr);

  mgr.book(prefix()+"_auxEnergy", &fAuxEnergy);
  mgr.book(prefix()+"_emEnergy", &fEmEnergy);
  mgr.book(prefix()+"_hadEnergy", &fHadEnergy);
  mgr.book(prefix()+"_invisEnergy", &fInvisEnergy);
  mgr.book(prefix()+"_charge", &fCharge);
  mgr.book(prefix()+"_nGenConstituents", &fNGenConstituents);
}
