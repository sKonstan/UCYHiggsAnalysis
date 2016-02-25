// -*- c++ -*-
// This file has been auto-generated with HiggsAnalysis/NtupleAnalysis/scripts/hplusGenerateDataFormats.py

#ifndef DataFormat_GenJetsGenerated_h
#define DataFormat_GenJetsGenerated_h

#include "DataFormat/interface/Particle.h"

class GenJetsGeneratedCollection: public ParticleCollection<double> {
public:
  explicit GenJetsGeneratedCollection(const std::string& prefix="GenJetss")
  : ParticleCollection(prefix)
  {

  }
  ~GenJetsGeneratedCollection() {}

  void setupBranches(BranchManager& mgr);



protected:

};


template <typename Coll>
class GenJetsGenerated: public Particle<Coll> {
public:
  GenJetsGenerated() {}
  GenJetsGenerated(const Coll* coll, size_t index)
  : Particle<Coll>(coll, index)
  {}
  ~GenJetsGenerated() {}





protected:

};

#endif
