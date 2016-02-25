// -*- c++ -*-
// This file has been auto-generated with HiggsAnalysis/NtupleAnalysis/scripts/hplusGenerateDataFormats.py

#ifndef DataFormat_METGenerated_h
#define DataFormat_METGenerated_h

#include "DataFormat/interface/Particle.h"

class METGeneratedCollection: public ParticleCollection<double> {
public:
  explicit METGeneratedCollection(const std::string& prefix="METs")
  : ParticleCollection(prefix)
  {

  }
  ~METGeneratedCollection() {}

  void setupBranches(BranchManager& mgr);



protected:

};


template <typename Coll>
class METGenerated: public Particle<Coll> {
public:
  METGenerated() {}
  METGenerated(const Coll* coll, size_t index)
  : Particle<Coll>(coll, index)
  {}
  ~METGenerated() {}





protected:

};

#endif
