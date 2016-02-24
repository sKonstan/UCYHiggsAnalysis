// -*- c++ -*-
// This file has been auto-generated with HiggsAnalysis/NtupleAnalysis/scripts/hplusGenerateDataFormats.py

#ifndef DataFormat_GenParticleGenerated_h
#define DataFormat_GenParticleGenerated_h

#include "DataFormat/interface/Particle.h"
#include <vector>

class GenParticleGeneratedCollection {
public:
  using float_type = double;
  explicit GenParticleGeneratedCollection(const std::string& prefix="GenParticles")
    : //added by hand
    fAllGenp(prefix) // add by hand
  {
    fAllGenp.setEnergySystematicsVariation(""); // added by hand
  }
  ~GenParticleGeneratedCollection() {}

  void setupBranches(BranchManager& mgr);

  const std::vector<Particle<ParticleCollection<float_type>>> getAllGenpCollection() const; //added by hand

public:
  const std::vector<double> getE() const { return fE->value(); }
  const std::vector<double> getEta() const { return fEta->value(); }
  const std::vector<double> getMass() const { return fMass->value(); }
  const std::vector<double> getPhi() const { return fPhi->value(); }
  const std::vector<double> getPt() const { return fPt->value(); }
  const std::vector<double> getVertexX() const { return fVertexX->value(); }
  const std::vector<double> getVertexY() const { return fVertexY->value(); }
  const std::vector<double> getVertexZ() const { return fVertexZ->value(); }
  const std::vector<int> getPdgId() const { return fPdgId->value(); }
  const std::vector<short> getCharge() const { return fCharge->value(); }
  const std::vector<short> getStatus() const { return fStatus->value(); }
  const std::vector<std::vector<unsigned short> > getDaughters() const { return fDaughters->value(); } // for the second std::vector, std:: added by hand
  const std::vector<std::vector<unsigned short> > getMothers() const { return fMothers->value(); }     // for the second std::vector, std:: added by hand

protected:
  const Branch<std::vector<double>> *fE;
  const Branch<std::vector<double>> *fEta;
  const Branch<std::vector<double>> *fMass;
  const Branch<std::vector<double>> *fPhi;
  const Branch<std::vector<double>> *fPt;
  const Branch<std::vector<double>> *fVertexX;
  const Branch<std::vector<double>> *fVertexY;
  const Branch<std::vector<double>> *fVertexZ;
  const Branch<std::vector<int>> *fPdgId;
  const Branch<std::vector<short>> *fCharge;
  const Branch<std::vector<short>> *fStatus;
  const Branch<std::vector<std::vector<unsigned short> >> *fDaughters; // for the second std::vector, std:: added by hand
  const Branch<std::vector<std::vector<unsigned short> >> *fMothers;   // for the second std::vector, std:: added by hand
  ParticleCollection<float_type> fAllGenp;
};

#endif
