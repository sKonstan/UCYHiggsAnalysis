// -*- c++ -*-
// This file has been auto-generated with HiggsAnalysis/NtupleAnalysis/scripts/hplusGenerateDataFormats.py

#ifndef DataFormat_PFcandidateGenerated_h
#define DataFormat_PFcandidateGenerated_h

#include "DataFormat/interface/Particle.h"

class PFcandidateGeneratedCollection: public ParticleCollection<double> {
public:
  explicit PFcandidateGeneratedCollection(const std::string& prefix="PFcandidates")
  : ParticleCollection(prefix)
  {

  }
  ~PFcandidateGeneratedCollection() {}

  void setupBranches(BranchManager& mgr);



protected:
  const Branch<std::vector<float>> *fIPTSignificance;
  const Branch<std::vector<float>> *fIPTwrtPV;
  const Branch<std::vector<float>> *fIPzSignificance;
  const Branch<std::vector<float>> *fIPzwrtPV;
  const Branch<std::vector<short>> *fNumOfHits;
  const Branch<std::vector<short>> *fNumOfPixHits;
  const Branch<std::vector<float>> *fIPTwrtPVError;
  const Branch<std::vector<float>> *fIPzwrtPVError;


};


template <typename Coll>
class PFcandidateGenerated: public Particle<Coll> {
public:
  PFcandidateGenerated() {}
  PFcandidateGenerated(const Coll* coll, size_t index)
  : Particle<Coll>(coll, index)
  {}
  ~PFcandidateGenerated() {}



  short NumOfHits() const { return this->fCollection->fNumOfHits->value()[this->index()]; }
  short NumOfPixHits() const { return this->fCollection->fNumOfPixHits->value()[this->index()]; }
  float IPTwrtPV() const { return this->fCollection->fIPTwrtPV->value()[this->index()]; }
  float IPTwrtPVError() const { return this->fCollection->fIPTwrtPVError->value()[this->index()]; }
  float IPzwrtPV() const { return this->fCollection->fIPzwrtPV->value()[this->index()]; }
  float IPzwrtPVError() const { return this->fCollection->fIPzwrtPVError->value()[this->index()]; }
  float IPTSignificance() const { return this->fCollection->fIPTSignificance->value()[this->index()]; }
  float IPzSignificance() const { return this->fCollection->fIPzSignificance->value()[this->index()]; }


protected:

};

#endif
