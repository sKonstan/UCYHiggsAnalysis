// -*- c++ -*-
// This file has been auto-generated with HiggsAnalysis/NtupleAnalysis/scripts/hplusGenerateDataFormats.py

#ifndef DataFormat_EventInfoGenerated_h
#define DataFormat_EventInfoGenerated_h

#include "DataFormat/interface/Particle.h"

class EventInfoGeneratedCollection: public ParticleCollection<double> {
public:
  explicit EventInfoGeneratedCollection(const std::string& prefix="EventInfos")
  : ParticleCollection(prefix)
  {

  }
  ~EventInfoGeneratedCollection() {}

  void setupBranches(BranchManager& mgr);



protected:

};


template <typename Coll>
class EventInfoGenerated: public Particle<Coll> {
public:
  EventInfoGenerated() {}
  EventInfoGenerated(const Coll* coll, size_t index)
  : Particle<Coll>(coll, index)
  {}
  ~EventInfoGenerated() {}





protected:

};

#endif
