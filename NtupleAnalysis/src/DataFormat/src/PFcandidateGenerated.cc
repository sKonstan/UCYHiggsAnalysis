
// -*- c++ -*-
// This file has been auto-generated with HiggsAnalysis/NtupleAnalysis/scripts/hplusGenerateDataFormats.py

#include "DataFormat/interface/PFcandidateGenerated.h"

#include "Framework/interface/BranchManager.h"

void PFcandidateGeneratedCollection::setupBranches(BranchManager& mgr) {
  ParticleCollection::setupBranches(mgr);

  mgr.book(prefix()+"_IPTSignificance", &fIPTSignificance);
  mgr.book(prefix()+"_IPTwrtPV", &fIPTwrtPV);
  mgr.book(prefix()+"_IPTwrtPVError", &fIPTwrtPVError);
  mgr.book(prefix()+"_IPzSignificance", &fIPzSignificance);
  mgr.book(prefix()+"_IPzwrtPV", &fIPzwrtPV);
  mgr.book(prefix()+"_IPzwrtPVError", &fIPzwrtPVError);
  mgr.book(prefix()+"_NumOfHits", &fNumOfHits);
  mgr.book(prefix()+"_NumOfPixHits", &fNumOfPixHits);
}
