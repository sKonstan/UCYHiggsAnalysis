// -*- c++ -*-
// This file has been auto-generated with HiggsAnalysis/NtupleAnalysis/scripts/hplusGenerateDataFormats.py

#ifndef DataFormat_HLTGenerated_h
#define DataFormat_HLTGenerated_h

#include "DataFormat/interface/Particle.h"

class HLTGeneratedCollection: public ParticleCollection<double> {
public:
  explicit HLTGeneratedCollection(const std::string& prefix="HLTs")
  : ParticleCollection(prefix)
  {

  }
  ~HLTGeneratedCollection() {}

  void setupBranches(BranchManager& mgr);



protected:

};


template <typename Coll>
class HLTGenerated: public Particle<Coll> {
public:
  HLTGenerated() {}
  HLTGenerated(const Coll* coll, size_t index)
  : Particle<Coll>(coll, index)
  {}
  ~HLTGenerated() {}





protected:

};

#endif
