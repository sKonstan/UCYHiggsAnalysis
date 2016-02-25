// -*- c++ -*-
// This file has been auto-generated with HiggsAnalysis/NtupleAnalysis/scripts/hplusGenerateDataFormats.py

#ifndef DataFormat_GenMETGenerated_h
#define DataFormat_GenMETGenerated_h

#include "DataFormat/interface/Particle.h"

class GenMETGeneratedCollection: public ParticleCollection<double> {
public:
  explicit GenMETGeneratedCollection(const std::string& prefix="GenMETs")
  : ParticleCollection(prefix)
  {

  }
  ~GenMETGeneratedCollection() {}

  void setupBranches(BranchManager& mgr);



protected:

};


template <typename Coll>
class GenMETGenerated: public Particle<Coll> {
public:
  GenMETGenerated() {}
  GenMETGenerated(const Coll* coll, size_t index)
  : Particle<Coll>(coll, index)
  {}
  ~GenMETGenerated() {}





protected:

};

#endif
