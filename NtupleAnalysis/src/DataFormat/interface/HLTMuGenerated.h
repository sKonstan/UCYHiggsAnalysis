// -*- c++ -*-
// This file has been auto-generated with HiggsAnalysis/NtupleAnalysis/scripts/hplusGenerateDataFormats.py

#ifndef DataFormat_HLTMuGenerated_h
#define DataFormat_HLTMuGenerated_h

#include "DataFormat/interface/Particle.h"

class HLTMuGeneratedCollection: public ParticleCollection<double> {
public:
  explicit HLTMuGeneratedCollection(const std::string& prefix="HLTMus")
  : ParticleCollection(prefix)
  {

  }
  ~HLTMuGeneratedCollection() {}

  void setupBranches(BranchManager& mgr);



protected:

};


template <typename Coll>
class HLTMuGenerated: public Particle<Coll> {
public:
  HLTMuGenerated() {}
  HLTMuGenerated(const Coll* coll, size_t index)
  : Particle<Coll>(coll, index)
  {}
  ~HLTMuGenerated() {}





protected:

};

#endif
