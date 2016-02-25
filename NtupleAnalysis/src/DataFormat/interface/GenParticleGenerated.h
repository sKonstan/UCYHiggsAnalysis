// -*- c++ -*-
// This file has been auto-generated with HiggsAnalysis/NtupleAnalysis/scripts/hplusGenerateDataFormats.py

#ifndef DataFormat_GenParticleGenerated_h
#define DataFormat_GenParticleGenerated_h

#include "DataFormat/interface/Particle.h"

class GenParticleGeneratedCollection: public ParticleCollection<double> {
public:
  explicit GenParticleGeneratedCollection(const std::string& prefix="GenParticles")
  : ParticleCollection(prefix)
  {

  }
  ~GenParticleGeneratedCollection() {}

  void setupBranches(BranchManager& mgr);



protected:
  const Branch<std::vector<double>> *fMass;
  const Branch<std::vector<double>> *fVertexX;
  const Branch<std::vector<double>> *fVertexY;
  const Branch<std::vector<double>> *fVertexZ;
  const Branch<std::vector<short>> *fCharge;
  const Branch<std::vector<short>> *fStatus;
  const Branch<std::vector<std::vector<unsigned short> >> *fDaughters;
  const Branch<std::vector<std::vector<unsigned short> >> *fMothers;
};


template <typename Coll>
class GenParticleGenerated: public Particle<Coll> {
public:
  GenParticleGenerated() {}
  GenParticleGenerated(const Coll* coll, size_t index)
  : Particle<Coll>(coll, index)
  {}
  ~GenParticleGenerated() {}



  double mass() const { return this->fCollection->fMass->value()[this->index()]; }
  double vertexX() const { return this->fCollection->fVertexX->value()[this->index()]; }
  double vertexY() const { return this->fCollection->fVertexY->value()[this->index()]; }
  double vertexZ() const { return this->fCollection->fVertexZ->value()[this->index()]; }
  short charge() const { return this->fCollection->fCharge->value()[this->index()]; }
  short status() const { return this->fCollection->fStatus->value()[this->index()]; }
  std::vector<unsigned short>  daughters() const { return this->fCollection->fDaughters->value()[this->index()]; }
  std::vector<unsigned short>  mothers() const { return this->fCollection->fMothers->value()[this->index()]; }

protected:

};

#endif
