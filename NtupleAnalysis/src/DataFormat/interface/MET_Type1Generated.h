// -*- c++ -*-
// This file has been auto-generated with HiggsAnalysis/NtupleAnalysis/scripts/hplusGenerateDataFormats.py

#ifndef DataFormat_MET_Type1Generated_h
#define DataFormat_MET_Type1Generated_h

#include "DataFormat/interface/Particle.h"

class MET_Type1GeneratedCollection: public ParticleCollection<double> {
public:
  explicit MET_Type1GeneratedCollection(const std::string& prefix="MET_Type1s")
  : ParticleCollection(prefix)
  {

  }
  ~MET_Type1GeneratedCollection() {}

  void setupBranches(BranchManager& mgr);



protected:

};


template <typename Coll>
class MET_Type1Generated: public Particle<Coll> {
public:
  MET_Type1Generated() {}
  MET_Type1Generated(const Coll* coll, size_t index)
  : Particle<Coll>(coll, index)
  {}
  ~MET_Type1Generated() {}





protected:

};

#endif
