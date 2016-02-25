// -*- c++ -*-
// This file has been auto-generated with HiggsAnalysis/NtupleAnalysis/scripts/hplusGenerateDataFormats.py

#ifndef DataFormat_CaloMETGenerated_h
#define DataFormat_CaloMETGenerated_h

#include "DataFormat/interface/Particle.h"

class CaloMETGeneratedCollection: public ParticleCollection<double> {
public:
  explicit CaloMETGeneratedCollection(const std::string& prefix="CaloMETs")
  : ParticleCollection(prefix)
  {

  }
  ~CaloMETGeneratedCollection() {}

  void setupBranches(BranchManager& mgr);



protected:

};


template <typename Coll>
class CaloMETGenerated: public Particle<Coll> {
public:
  CaloMETGenerated() {}
  CaloMETGenerated(const Coll* coll, size_t index)
  : Particle<Coll>(coll, index)
  {}
  ~CaloMETGenerated() {}





protected:

};

#endif
