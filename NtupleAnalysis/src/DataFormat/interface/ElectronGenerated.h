// -*- c++ -*-
// This file has been auto-generated with HiggsAnalysis/NtupleAnalysis/scripts/hplusGenerateDataFormats.py

#ifndef DataFormat_ElectronGenerated_h
#define DataFormat_ElectronGenerated_h

#include "DataFormat/interface/Particle.h"
#include <string>
#include <vector>
#include <functional>

class ElectronGeneratedCollection: public ParticleCollection<double> {
public:
  explicit ElectronGeneratedCollection(const std::string& prefix="Electrons")
  : ParticleCollection(prefix),
    fMCelectron(prefix)
  {
    fMCelectron.setEnergySystematicsVariation("_MCelectron");
  }
  ~ElectronGeneratedCollection() {}

  void setupBranches(BranchManager& mgr);

  std::vector<std::string> getIDDiscriminatorNames() const {
    static std::vector<std::string> n = { std::string("mvaEleID_PHYS14_PU20bx25_nonTrig_V1_wp80"), std::string("mvaEleID_PHYS14_PU20bx25_nonTrig_V1_wp90")};
    return n;
  }

  const ParticleCollection<double>* getMCelectronCollection() const { return &fMCelectron; }
protected:
  ParticleCollection<double> fMCelectron;

protected:
  const Branch<std::vector<bool>> *fTrgMatch_HLT_Ele16_Ele12_Ele8_CaloIdL_TrackIdL_vx;
  const Branch<std::vector<bool>> *fTrgMatch_HLT_Ele17_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_vx;
  const Branch<std::vector<bool>> *fTrgMatch_HLT_Ele23_WPLoose_Gsf_vx;
  const Branch<std::vector<bool>> *fIsPF;
  const Branch<std::vector<bool>> *fMvaEleID_PHYS14_PU20bx25_nonTrig_V1_wp80;
  const Branch<std::vector<bool>> *fMvaEleID_PHYS14_PU20bx25_nonTrig_V1_wp90;
  const Branch<std::vector<float>> *fCaloIso;
  const Branch<std::vector<float>> *fEcalIso;
  const Branch<std::vector<float>> *fHcalIso;
  const Branch<std::vector<float>> *fRelIsoDeltaBeta;
  const Branch<std::vector<float>> *fTrackIso;
};


template <typename Coll>
class ElectronGenerated: public Particle<Coll> {
public:
  ElectronGenerated() {}
  ElectronGenerated(const Coll* coll, size_t index)
  : Particle<Coll>(coll, index),
    fMCelectron(coll->getMCelectronCollection(), index)
  {}
  ~ElectronGenerated() {}

  std::vector<std::function<bool()>> getIDDiscriminatorValues() const {
    static std::vector<std::function<bool()>> values = {
      [&](){ return this->mvaEleID_PHYS14_PU20bx25_nonTrig_V1_wp80(); },
      [&](){ return this->mvaEleID_PHYS14_PU20bx25_nonTrig_V1_wp90(); }
    };
    return values;
  }

  const Particle<ParticleCollection<double>>* MCelectron() const { return &fMCelectron; }

  bool TrgMatch_HLT_Ele16_Ele12_Ele8_CaloIdL_TrackIdL_vx() const { return this->fCollection->fTrgMatch_HLT_Ele16_Ele12_Ele8_CaloIdL_TrackIdL_vx->value()[this->index()]; }
  bool TrgMatch_HLT_Ele17_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_vx() const { return this->fCollection->fTrgMatch_HLT_Ele17_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_vx->value()[this->index()]; }
  bool TrgMatch_HLT_Ele23_WPLoose_Gsf_vx() const { return this->fCollection->fTrgMatch_HLT_Ele23_WPLoose_Gsf_vx->value()[this->index()]; }
  bool isPF() const { return this->fCollection->fIsPF->value()[this->index()]; }
  bool mvaEleID_PHYS14_PU20bx25_nonTrig_V1_wp80() const { return this->fCollection->fMvaEleID_PHYS14_PU20bx25_nonTrig_V1_wp80->value()[this->index()]; }
  bool mvaEleID_PHYS14_PU20bx25_nonTrig_V1_wp90() const { return this->fCollection->fMvaEleID_PHYS14_PU20bx25_nonTrig_V1_wp90->value()[this->index()]; }
  float caloIso() const { return this->fCollection->fCaloIso->value()[this->index()]; }
  float ecalIso() const { return this->fCollection->fEcalIso->value()[this->index()]; }
  float hcalIso() const { return this->fCollection->fHcalIso->value()[this->index()]; }
  float relIsoDeltaBeta() const { return this->fCollection->fRelIsoDeltaBeta->value()[this->index()]; }
  float trackIso() const { return this->fCollection->fTrackIso->value()[this->index()]; }

protected:
  Particle<ParticleCollection<double>> fMCelectron;

};

#endif
