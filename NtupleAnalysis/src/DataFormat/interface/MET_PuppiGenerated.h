// -*- c++ -*-
// This file has been auto-generated with HiggsAnalysis/NtupleAnalysis/scripts/hplusGenerateDataFormats.py

#ifndef DataFormat_MET_PuppiGenerated_h
#define DataFormat_MET_PuppiGenerated_h

#include "DataFormat/interface/Particle.h"

class MET_PuppiGeneratedCollection: public ParticleCollection<double> {
public:
  explicit MET_PuppiGeneratedCollection(const std::string& prefix="MET_Puppis")
  : ParticleCollection(prefix)
  {

  }
  ~MET_PuppiGeneratedCollection() {}

  void setupBranches(BranchManager& mgr);



protected:

};


template <typename Coll>
class MET_PuppiGenerated: public Particle<Coll> {
public:
  MET_PuppiGenerated() {}
  MET_PuppiGenerated(const Coll* coll, size_t index)
  : Particle<Coll>(coll, index)
  {}
  ~MET_PuppiGenerated() {}





protected:

};

#endif
