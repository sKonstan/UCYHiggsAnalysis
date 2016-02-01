// -*- c++ -*-
// This file has been auto-generated with HiggsAnalysis/NtupleAnalysis/scripts/hplusGenerateDataFormats.py

#ifndef DataFormat_GenJetGenerated_h
#define DataFormat_GenJetGenerated_h

#include "DataFormat/interface/Particle.h"

class GenJetGeneratedCollection: public ParticleCollection<double> {
public:
  explicit GenJetGeneratedCollection(const std::string& prefix="GenJets")
  : ParticleCollection(prefix)
  {

  }
  ~GenJetGeneratedCollection() {}

  void setupBranches(BranchManager& mgr);

protected:

  const Branch<std::vector<double> >  *fEmEnergy;
  const Branch<std::vector<double> >  *fHadEnergy;
  const Branch<std::vector<double> >  *fAuxEnergy;
  const Branch<std::vector<double> >  *fInvisEnergy;
  const Branch<std::vector<short> >   *fNGenConstituents;



};


template <typename Coll>
class GenJetGenerated: public Particle<Coll> {
public:
  GenJetGenerated() {}
  GenJetGenerated(const Coll* coll, size_t index)
  : Particle<Coll>(coll, index)
  {}
  ~GenJetGenerated() {}

  
  double emEnergy() const { return this->fCollection->fEmEnergy->value()[this->index()]; }
  double hadEnergy() const { return this->fCollection->fHadEnergy->value()[this->index()]; }
  double auxEnergy() const { return this->fCollection->fAuxEnergy->value()[this->index()]; }
  double invisEnergy() const { return this->fCollection->fInvisEnergy->value()[this->index()]; }
  short nGenConstituents() const { return this->fCollection->fNGenConstituents->value()[this->index()]; }




protected:

};

#endif
