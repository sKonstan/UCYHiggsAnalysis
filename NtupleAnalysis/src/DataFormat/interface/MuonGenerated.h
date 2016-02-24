// -*- c++ -*-
// This file has been auto-generated with HiggsAnalysis/NtupleAnalysis/scripts/hplusGenerateDataFormats.py

#ifndef DataFormat_MuonGenerated_h
#define DataFormat_MuonGenerated_h

#include "DataFormat/interface/Particle.h"
#include <string>
#include <vector>
#include <functional>

class MuonGeneratedCollection: public ParticleCollection<double> {
public:
  explicit MuonGeneratedCollection(const std::string& prefix="Muons")
  : ParticleCollection(prefix),
    fMCmuon(prefix)
  {
    fMCmuon.setEnergySystematicsVariation("_MCmuon");
  }
  ~MuonGeneratedCollection() {}

  void setupBranches(BranchManager& mgr);

  std::vector<std::string> getIDDiscriminatorNames() const {
    static std::vector<std::string> n = { std::string("muIDLoose"), std::string("muIDMedium"), std::string("muIDTight")};
    return n;
  }

  const ParticleCollection<double>* getMCmuonCollection() const { return &fMCmuon; }
protected:
  ParticleCollection<double> fMCmuon;

protected:
  const Branch<std::vector<bool>> *fTrgMatch_HLT_DiMu9_Ele9_CaloIdL_TrackIdL_vx;
  const Branch<std::vector<bool>> *fTrgMatch_HLT_IsoMu20_vx;
  const Branch<std::vector<bool>> *fTrgMatch_HLT_IsoTkMu20_vx;
  const Branch<std::vector<bool>> *fTrgMatch_HLT_Mu17_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_vx;
  const Branch<std::vector<bool>> *fTrgMatch_HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_vx;
  const Branch<std::vector<bool>> *fTrgMatch_HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ_vx;
  const Branch<std::vector<bool>> *fTrgMatch_HLT_Mu8_DiEle12_CaloIdL_TrackIdL_vx;
  const Branch<std::vector<bool>> *fTrgMatch_HLT_Mu8_TrkIsoVVL_Ele17_CaloIdL_TrackIdL_IsoVL_vx;
  const Branch<std::vector<bool>> *fTrgMatch_HLT_TripleMu_12_10_5_vx;
  const Branch<std::vector<bool>> *fIsGlobalMuon;
  const Branch<std::vector<bool>> *fMuIDLoose;
  const Branch<std::vector<bool>> *fMuIDMedium;
  const Branch<std::vector<bool>> *fMuIDTight;
  const Branch<std::vector<float>> *fCaloIso;
  const Branch<std::vector<float>> *fEcalIso;
  const Branch<std::vector<float>> *fHcalIso;
  const Branch<std::vector<float>> *fRelIsoDeltaBeta;
};


template <typename Coll>
class MuonGenerated: public Particle<Coll> {
public:
  MuonGenerated() {}
  MuonGenerated(const Coll* coll, size_t index)
  : Particle<Coll>(coll, index),
    fMCmuon(coll->getMCmuonCollection(), index)
  {}
  ~MuonGenerated() {}

  std::vector<std::function<bool()>> getIDDiscriminatorValues() const {
    static std::vector<std::function<bool()>> values = {
      [&](){ return this->muIDLoose(); },
      [&](){ return this->muIDMedium(); },
      [&](){ return this->muIDTight(); }
    };
    return values;
  }

  const Particle<ParticleCollection<double>>* MCmuon() const { return &fMCmuon; }

  bool TrgMatch_HLT_DiMu9_Ele9_CaloIdL_TrackIdL_vx() const { return this->fCollection->fTrgMatch_HLT_DiMu9_Ele9_CaloIdL_TrackIdL_vx->value()[this->index()]; }
  bool TrgMatch_HLT_IsoMu20_vx() const { return this->fCollection->fTrgMatch_HLT_IsoMu20_vx->value()[this->index()]; }
  bool TrgMatch_HLT_IsoTkMu20_vx() const { return this->fCollection->fTrgMatch_HLT_IsoTkMu20_vx->value()[this->index()]; }
  bool TrgMatch_HLT_Mu17_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_vx() const { return this->fCollection->fTrgMatch_HLT_Mu17_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_vx->value()[this->index()]; }
  bool TrgMatch_HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_vx() const { return this->fCollection->fTrgMatch_HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_vx->value()[this->index()]; }
  bool TrgMatch_HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ_vx() const { return this->fCollection->fTrgMatch_HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ_vx->value()[this->index()]; }
  bool TrgMatch_HLT_Mu8_DiEle12_CaloIdL_TrackIdL_vx() const { return this->fCollection->fTrgMatch_HLT_Mu8_DiEle12_CaloIdL_TrackIdL_vx->value()[this->index()]; }
  bool TrgMatch_HLT_Mu8_TrkIsoVVL_Ele17_CaloIdL_TrackIdL_IsoVL_vx() const { return this->fCollection->fTrgMatch_HLT_Mu8_TrkIsoVVL_Ele17_CaloIdL_TrackIdL_IsoVL_vx->value()[this->index()]; }
  bool TrgMatch_HLT_TripleMu_12_10_5_vx() const { return this->fCollection->fTrgMatch_HLT_TripleMu_12_10_5_vx->value()[this->index()]; }
  bool isGlobalMuon() const { return this->fCollection->fIsGlobalMuon->value()[this->index()]; }
  bool muIDLoose() const { return this->fCollection->fMuIDLoose->value()[this->index()]; }
  bool muIDMedium() const { return this->fCollection->fMuIDMedium->value()[this->index()]; }
  bool muIDTight() const { return this->fCollection->fMuIDTight->value()[this->index()]; }
  float caloIso() const { return this->fCollection->fCaloIso->value()[this->index()]; }
  float ecalIso() const { return this->fCollection->fEcalIso->value()[this->index()]; }
  float hcalIso() const { return this->fCollection->fHcalIso->value()[this->index()]; }
  float relIsoDeltaBeta() const { return this->fCollection->fRelIsoDeltaBeta->value()[this->index()]; }

protected:
  Particle<ParticleCollection<double>> fMCmuon;

};

#endif
