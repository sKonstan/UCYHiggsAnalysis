// -*- c++ -*-
// This file has been auto-generated with HiggsAnalysis/NtupleAnalysis/scripts/hplusGenerateDataFormats.py

#ifndef DataFormat_PFcandidatesGenerated_h
#define DataFormat_PFcandidatesGenerated_h

#include "DataFormat/interface/Particle.h"

class PFcandidatesGeneratedCollection: public ParticleCollection<double> {
public:
  explicit PFcandidatesGeneratedCollection(const std::string& prefix="PFcandidatess")
  : ParticleCollection(prefix)
  {

  }
  ~PFcandidatesGeneratedCollection() {}

  void setupBranches(BranchManager& mgr);



protected:

};


template <typename Coll>
class PFcandidatesGenerated: public Particle<Coll> {
public:
  PFcandidatesGenerated() {}
  PFcandidatesGenerated(const Coll* coll, size_t index)
  : Particle<Coll>(coll, index)
  {}
  ~PFcandidatesGenerated() {}





protected:

};

#endif
