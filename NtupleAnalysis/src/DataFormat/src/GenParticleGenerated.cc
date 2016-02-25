
// -*- c++ -*-
// This file has been auto-generated with HiggsAnalysis/NtupleAnalysis/scripts/hplusGenerateDataFormats.py

#include "DataFormat/interface/GenParticleGenerated.h"

#include "Framework/interface/BranchManager.h"

void GenParticleGeneratedCollection::setupBranches(BranchManager& mgr) {
  ParticleCollection::setupBranches(mgr);

  mgr.book(prefix()+"_mass", &fMass);
  mgr.book(prefix()+"_vertexX", &fVertexX);
  mgr.book(prefix()+"_vertexY", &fVertexY);
  mgr.book(prefix()+"_vertexZ", &fVertexZ);
  mgr.book(prefix()+"_charge", &fCharge);
  mgr.book(prefix()+"_status", &fStatus);
  mgr.book(prefix()+"_daughters", &fDaughters);
  mgr.book(prefix()+"_mothers", &fMothers);
}
