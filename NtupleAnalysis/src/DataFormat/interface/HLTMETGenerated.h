// -*- c++ -*-
// This file has been auto-generated with HiggsAnalysis/NtupleAnalysis/scripts/hplusGenerateDataFormats.py

#ifndef DataFormat_HLTMETGenerated_h
#define DataFormat_HLTMETGenerated_h

#include "DataFormat/interface/Particle.h"

class HLTMETGeneratedCollection: public ParticleCollection<double> {
public:
  explicit HLTMETGeneratedCollection(const std::string& prefix="HLTMETs")
  : ParticleCollection(prefix)
  {

  }
  ~HLTMETGeneratedCollection() {}

  void setupBranches(BranchManager& mgr);



protected:

};


template <typename Coll>
class HLTMETGenerated: public Particle<Coll> {
public:
  HLTMETGenerated() {}
  HLTMETGenerated(const Coll* coll, size_t index)
  : Particle<Coll>(coll, index)
  {}
  ~HLTMETGenerated() {}





protected:

};

#endif
