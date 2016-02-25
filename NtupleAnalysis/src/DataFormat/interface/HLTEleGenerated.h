// -*- c++ -*-
// This file has been auto-generated with HiggsAnalysis/NtupleAnalysis/scripts/hplusGenerateDataFormats.py

#ifndef DataFormat_HLTEleGenerated_h
#define DataFormat_HLTEleGenerated_h

#include "DataFormat/interface/Particle.h"

class HLTEleGeneratedCollection: public ParticleCollection<double> {
public:
  explicit HLTEleGeneratedCollection(const std::string& prefix="HLTEles")
  : ParticleCollection(prefix)
  {

  }
  ~HLTEleGeneratedCollection() {}

  void setupBranches(BranchManager& mgr);



protected:

};


template <typename Coll>
class HLTEleGenerated: public Particle<Coll> {
public:
  HLTEleGenerated() {}
  HLTEleGenerated(const Coll* coll, size_t index)
  : Particle<Coll>(coll, index)
  {}
  ~HLTEleGenerated() {}





protected:

};

#endif
