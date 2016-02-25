// -*- c++ -*-
// This file has been auto-generated with HiggsAnalysis/NtupleAnalysis/scripts/hplusGenerateDataFormats.py

#ifndef DataFormat_PFCHSJetsGenerated_h
#define DataFormat_PFCHSJetsGenerated_h

#include "DataFormat/interface/Particle.h"
#include <string>
#include <vector>
#include <functional>

class PFCHSJetsGeneratedCollection: public ParticleCollection<double> {
public:
  explicit PFCHSJetsGeneratedCollection(const std::string& prefix="PFCHSJetss")
  : ParticleCollection(prefix)
  {

  }
  ~PFCHSJetsGeneratedCollection() {}

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
class PFCHSJetsGenerated: public Particle<Coll> {
public:
  PFCHSJetsGenerated() {}
  PFCHSJetsGenerated(const Coll* coll, size_t index)
  : Particle<Coll>(coll, index)
  {}
  ~PFCHSJetsGenerated() {}

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
