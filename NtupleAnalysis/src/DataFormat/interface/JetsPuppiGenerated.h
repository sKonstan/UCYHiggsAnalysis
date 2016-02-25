// -*- c++ -*-
// This file has been auto-generated with HiggsAnalysis/NtupleAnalysis/scripts/hplusGenerateDataFormats.py

#ifndef DataFormat_JetsPuppiGenerated_h
#define DataFormat_JetsPuppiGenerated_h

#include "DataFormat/interface/Particle.h"
#include <string>
#include <vector>
#include <functional>

class JetsPuppiGeneratedCollection: public ParticleCollection<double> {
public:
  explicit JetsPuppiGeneratedCollection(const std::string& prefix="JetsPuppis")
  : ParticleCollection(prefix)
  {

  }
  ~JetsPuppiGeneratedCollection() {}

  void setupBranches(BranchManager& mgr);

  std::vector<std::string> getBJetTagsDiscriminatorNames() const {
    static std::vector<std::string> n = { std::string("")};
    return n;
  }
  std::vector<std::string> getPUIDDiscriminatorNames() const {
    static std::vector<std::string> n = { std::string("")};
    return n;
  }
  std::vector<std::string> getJetIDDiscriminatorNames() const {
    static std::vector<std::string> n = { std::string("")};
    return n;
  }


protected:

};


template <typename Coll>
class JetsPuppiGenerated: public Particle<Coll> {
public:
  JetsPuppiGenerated() {}
  JetsPuppiGenerated(const Coll* coll, size_t index)
  : Particle<Coll>(coll, index)
  {}
  ~JetsPuppiGenerated() {}

  std::vector<std::function<bool()>> getBJetTagsDiscriminatorValues() const {
    static std::vector<std::function<bool()>> values = {
    };
    return values;
  }
  std::vector<std::function<bool()>> getPUIDDiscriminatorValues() const {
    static std::vector<std::function<bool()>> values = {
    };
    return values;
  }
  std::vector<std::function<bool()>> getJetIDDiscriminatorValues() const {
    static std::vector<std::function<bool()>> values = {
    };
    return values;
  }




protected:

};

#endif
