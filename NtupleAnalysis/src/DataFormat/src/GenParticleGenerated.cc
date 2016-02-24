
// -*- c++ -*-
// This file has been auto-generated with HiggsAnalysis/NtupleAnalysis/scripts/hplusGenerateDataFormats.py

#include "DataFormat/interface/GenParticleGenerated.h"

#include "Framework/interface/BranchManager.h"

void GenParticleGeneratedCollection::setupBranches(BranchManager& mgr) {

  mgr.book("GenParticles_e", &fE);
  mgr.book("GenParticles_eta", &fEta);
  mgr.book("GenParticles_mass", &fMass);
  mgr.book("GenParticles_phi", &fPhi);
  mgr.book("GenParticles_pt", &fPt);
  mgr.book("GenParticles_vertexX", &fVertexX);
  mgr.book("GenParticles_vertexY", &fVertexY);
  mgr.book("GenParticles_vertexZ", &fVertexZ);
  mgr.book("GenParticles_pdgId", &fPdgId);
  mgr.book("GenParticles_charge", &fCharge);
  mgr.book("GenParticles_status", &fStatus);
  mgr.book("GenParticles_daughters", &fDaughters);
  mgr.book("GenParticles_mothers", &fMothers);
}


// Added by hand
const std::vector<Particle<ParticleCollection<double>>> GenParticleGeneratedCollection::getAllGenpCollection() const {
  std::vector<Particle<ParticleCollection<float_type>>> v;
for (size_t i = 0; i < fAllGenp.size(); ++i)
  v.push_back(Particle<ParticleCollection<float_type>>(&fAllGenp, i));
return v;
}

