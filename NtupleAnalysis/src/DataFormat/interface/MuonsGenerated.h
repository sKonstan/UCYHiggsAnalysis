// -*- c++ -*-
// This file has been auto-generated with HiggsAnalysis/NtupleAnalysis/scripts/hplusGenerateDataFormats.py

#ifndef DataFormat_MuonsGenerated_h
#define DataFormat_MuonsGenerated_h

#include "DataFormat/interface/Particle.h"
#include <string>
#include <vector>
#include <functional>

class MuonsGeneratedCollection: public ParticleCollection<double> {
public:
  explicit MuonsGeneratedCollection(const std::string& prefix="Muonss")
  : ParticleCollection(prefix)
  {

  }
  ~MuonsGeneratedCollection() {}

  void setupBranches(BranchManager& mgr);

  std::vector<std::string> getIDDiscriminatorNames() const {
    static std::vector<std::string> n = { std::string("")};
    return n;
  }


protected:

};


template <typename Coll>
class MuonsGenerated: public Particle<Coll> {
public:
  MuonsGenerated() {}
  MuonsGenerated(const Coll* coll, size_t index)
  : Particle<Coll>(coll, index)
  {}
  ~MuonsGenerated() {}

  std::vector<std::function<bool()>> getIDDiscriminatorValues() const {
    static std::vector<std::function<bool()>> values = {
    };
    return values;
  }




protected:

};

#endif
