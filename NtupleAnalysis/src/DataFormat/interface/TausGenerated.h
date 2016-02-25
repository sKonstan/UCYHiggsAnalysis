// -*- c++ -*-
// This file has been auto-generated with HiggsAnalysis/NtupleAnalysis/scripts/hplusGenerateDataFormats.py

#ifndef DataFormat_TausGenerated_h
#define DataFormat_TausGenerated_h

#include "DataFormat/interface/Particle.h"
#include <string>
#include <vector>
#include <functional>

class TausGeneratedCollection: public ParticleCollection<double> {
public:
  explicit TausGeneratedCollection(const std::string& prefix="Tauss")
  : ParticleCollection(prefix)
  {

  }
  ~TausGeneratedCollection() {}

  void setupBranches(BranchManager& mgr);

  std::vector<std::string> getIsolationDiscriminatorNames() const {
    static std::vector<std::string> n = { std::string("")};
    return n;
  }
  std::vector<std::string> getAgainstMuonDiscriminatorNames() const {
    static std::vector<std::string> n = { std::string("")};
    return n;
  }
  std::vector<std::string> getAgainstElectronDiscriminatorNames() const {
    static std::vector<std::string> n = { std::string("")};
    return n;
  }


protected:

};


template <typename Coll>
class TausGenerated: public Particle<Coll> {
public:
  TausGenerated() {}
  TausGenerated(const Coll* coll, size_t index)
  : Particle<Coll>(coll, index)
  {}
  ~TausGenerated() {}

  std::vector<std::function<bool()>> getIsolationDiscriminatorValues() const {
    static std::vector<std::function<bool()>> values = {
    };
    return values;
  }
  std::vector<std::function<bool()>> getAgainstMuonDiscriminatorValues() const {
    static std::vector<std::function<bool()>> values = {
    };
    return values;
  }
  std::vector<std::function<bool()>> getAgainstElectronDiscriminatorValues() const {
    static std::vector<std::function<bool()>> values = {
    };
    return values;
  }




protected:

};

#endif
