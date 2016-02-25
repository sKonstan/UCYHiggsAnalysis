// -*- c++ -*-
// This file has been auto-generated with HiggsAnalysis/NtupleAnalysis/scripts/hplusGenerateDataFormats.py

#ifndef DataFormat_ElectronsGenerated_h
#define DataFormat_ElectronsGenerated_h

#include "DataFormat/interface/Particle.h"
#include <string>
#include <vector>
#include <functional>

class ElectronsGeneratedCollection: public ParticleCollection<double> {
public:
  explicit ElectronsGeneratedCollection(const std::string& prefix="Electronss")
  : ParticleCollection(prefix)
  {

  }
  ~ElectronsGeneratedCollection() {}

  void setupBranches(BranchManager& mgr);

  std::vector<std::string> getIDDiscriminatorNames() const {
    static std::vector<std::string> n = { std::string("")};
    return n;
  }


protected:

};


template <typename Coll>
class ElectronsGenerated: public Particle<Coll> {
public:
  ElectronsGenerated() {}
  ElectronsGenerated(const Coll* coll, size_t index)
  : Particle<Coll>(coll, index)
  {}
  ~ElectronsGenerated() {}

  std::vector<std::function<bool()>> getIDDiscriminatorValues() const {
    static std::vector<std::function<bool()>> values = {
    };
    return values;
  }




protected:

};

#endif
