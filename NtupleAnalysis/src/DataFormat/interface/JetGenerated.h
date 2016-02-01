// -*- c++ -*-
// This file has been auto-generated with HiggsAnalysis/NtupleAnalysis/scripts/hplusGenerateDataFormats.py

#ifndef DataFormat_JetGenerated_h
#define DataFormat_JetGenerated_h

#include "DataFormat/interface/Particle.h"
#include <string>
#include <vector>
#include <functional>

class JetGeneratedCollection: public ParticleCollection<double> {
public:
  explicit JetGeneratedCollection(const std::string& prefix="Jets")
  : ParticleCollection(prefix),
    fMCjet(prefix)
  {
    fMCjet.setEnergySystematicsVariation("_MCjet");
  }
  ~JetGeneratedCollection() {}

  void setupBranches(BranchManager& mgr);

  std::vector<std::string> getBJetTagsDiscriminatorNames() const {
    static std::vector<std::string> n = { std::string("pfCombinedInclusiveSecondaryVertexV2BJetTags"), std::string("pfJetBProbabilityBJetTags"), std::string("pfJetProbabilityBJetTags")};
    return n;
  }
  std::vector<std::string> getPUIDDiscriminatorNames() const {
    static std::vector<std::string> n = { std::string("PUIDloose"), std::string("PUIDmedium"), std::string("PUIDtight")};
    return n;
  }
  std::vector<std::string> getJetIDDiscriminatorNames() const {
    static std::vector<std::string> n = { std::string("IDloose"), std::string("IDtight"), std::string("IDtightLeptonVeto")};
    return n;
  }

  const ParticleCollection<double>* getMCjetCollection() const { return &fMCjet; }
protected:
  ParticleCollection<double> fMCjet;

protected:
  const Branch<std::vector<bool>> *fIDloose;
  const Branch<std::vector<bool>> *fIDtight;
  const Branch<std::vector<bool>> *fIDtightLeptonVeto;
  const Branch<std::vector<bool>> *fPUIDloose;
  const Branch<std::vector<bool>> *fPUIDmedium;
  const Branch<std::vector<bool>> *fPUIDtight;
  const Branch<std::vector<double>> *fPileupJetIdfullDiscriminant;
  const Branch<std::vector<float>> *fPfCombinedInclusiveSecondaryVertexV2BJetTags;
  const Branch<std::vector<float>> *fPfCombinedMVABJetTags;
  const Branch<std::vector<float>> *fPfJetBProbabilityBJetTags;
  const Branch<std::vector<float>> *fPfJetProbabilityBJetTags;
  const Branch<std::vector<int>> *fHadronFlavour;
  const Branch<std::vector<int>> *fPartonFlavour;

  const Branch<std::vector<int>>     *fPdgId;
  const Branch<std::vector<float>>   *fCombinedSecondaryVertexBJetTags;
  const Branch<std::vector<float>>   *fPfTrackCountingHighPurBJetTags;
  const Branch<std::vector<float>>   *fPfTrackCountingHighEffBJetTags;
  const Branch<std::vector<float>>   *fPfSimpleSecondaryVertexHighEffBJetTags;
  const Branch<std::vector<float>>   *fPfSimpleSecondaryVertexHighPurBJetTags;
  const Branch<std::vector<float>>   *fPfCombinedSecondaryVertexV2BJetTags;
  const Branch<std::vector<float>>   *fPfCombinedSecondaryVertexSoftLeptonBJetTags;

  const Branch<std::vector<bool>>    *fIsBasicJet;
  const Branch<std::vector<bool>>    *fIsCaloJet;
  const Branch<std::vector<bool>>    *fIsJPTJet;
  const Branch<std::vector<bool>>    *fIsPFJet;

  const Branch<std::vector<double>>  *fNeutralHadronEnergyFraction;
  const Branch<std::vector<double>>  *fNeutralEmEnergyFraction;
  const Branch<std::vector<short>>   *fNConstituents;
  const Branch<std::vector<short>>   *fChargedHadronMultiplicity;

  // const Branch<std::vector<double>>  *fPt_MCjet;
  // const Branch<std::vector<double>>  *fEta_MCjet;
  // const Branch<std::vector<double>>  *fPhi_MCjet;
  // const Branch<std::vector<double>>  *fE_MCjet;

  const Branch<std::vector<double>>  *fPt_JESup;
  const Branch<std::vector<double>>  *fEta_JESup;
  const Branch<std::vector<double>>  *fPhi_JESup;
  const Branch<std::vector<double>>  *fE_JESup;

  const Branch<std::vector<double>>  *fPt_JESdown;
  const Branch<std::vector<double>>  *fEta_JESdown;
  const Branch<std::vector<double>>  *fPhi_JESdown;
  const Branch<std::vector<double>>  *fE_JESdown;

  const Branch<std::vector<double>>  *fPt_JERup;
  const Branch<std::vector<double>>  *fEta_JERup;
  const Branch<std::vector<double>>  *fPhi_JERup;
  const Branch<std::vector<double>>  *fE_JERup;

  const Branch<std::vector<double>>  *fPt_JERdown;
  const Branch<std::vector<double>>  *fEta_JERdown;
  const Branch<std::vector<double>>  *fPhi_JERdown;
  const Branch<std::vector<double>>  *fE_JERdown;


};


template <typename Coll>
class JetGenerated: public Particle<Coll> {
public:
  JetGenerated() {}
  JetGenerated(const Coll* coll, size_t index)
  : Particle<Coll>(coll, index),
    fMCjet(coll->getMCjetCollection(), index)
  {}
  ~JetGenerated() {}

  std::vector<std::function<bool()>> getBJetTagsDiscriminatorValues() const {
    static std::vector<std::function<bool()>> values = {
      [&](){ return this->pfCombinedInclusiveSecondaryVertexV2BJetTags(); },
      [&](){ return this->pfJetBProbabilityBJetTags(); },
      [&](){ return this->pfJetProbabilityBJetTags(); }
    };
    return values;
  }
  std::vector<std::function<bool()>> getPUIDDiscriminatorValues() const {
    static std::vector<std::function<bool()>> values = {
      [&](){ return this->PUIDloose(); },
      [&](){ return this->PUIDmedium(); },
      [&](){ return this->PUIDtight(); }
    };
    return values;
  }
  std::vector<std::function<bool()>> getJetIDDiscriminatorValues() const {
    static std::vector<std::function<bool()>> values = {
      [&](){ return this->IDloose(); },
      [&](){ return this->IDtight(); },
      [&](){ return this->IDtightLeptonVeto(); }
    };
    return values;
  }

  const Particle<ParticleCollection<double>>* MCjet() const { return &fMCjet; }

  bool IDloose() const { return this->fCollection->fIDloose->value()[this->index()]; }
  bool IDtight() const { return this->fCollection->fIDtight->value()[this->index()]; }
  bool IDtightLeptonVeto() const { return this->fCollection->fIDtightLeptonVeto->value()[this->index()]; }
  bool PUIDloose() const { return this->fCollection->fPUIDloose->value()[this->index()]; }
  bool PUIDmedium() const { return this->fCollection->fPUIDmedium->value()[this->index()]; }
  bool PUIDtight() const { return this->fCollection->fPUIDtight->value()[this->index()]; }
  double pileupJetIdfullDiscriminant() const { return this->fCollection->fPileupJetIdfullDiscriminant->value()[this->index()]; }
  float pfCombinedInclusiveSecondaryVertexV2BJetTags() const { return this->fCollection->fPfCombinedInclusiveSecondaryVertexV2BJetTags->value()[this->index()]; }
  float pfCombinedMVABJetTags() const { return this->fCollection->fPfCombinedMVABJetTags->value()[this->index()]; }
  float pfJetBProbabilityBJetTags() const { return this->fCollection->fPfJetBProbabilityBJetTags->value()[this->index()]; }
  float pfJetProbabilityBJetTags() const { return this->fCollection->fPfJetProbabilityBJetTags->value()[this->index()]; }
  int hadronFlavour() const { return this->fCollection->fHadronFlavour->value()[this->index()]; }
  int partonFlavour() const { return this->fCollection->fPartonFlavour->value()[this->index()]; }


  //  int pdgId() const { return this->fCollection->fPdgId->value()[this->index()]; }
  float combinedSecondaryVertexBJetTags() const { return this->fCollection->fCombinedSecondaryVertexBJetTags->value()[this->index()]; }
  float pfTrackCountingHighPurBJetTags() const { return this->fCollection->fPfTrackCountingHighPurBJetTags->value()[this->index()]; }
  float pfTrackCountingHighEffBJetTags() const { return this->fCollection->fPfTrackCountingHighEffBJetTags->value()[this->index()]; }
  float pfSimpleSecondaryVertexHighEffBJetTags() const { return this->fCollection->fPfSimpleSecondaryVertexHighEffBJetTags->value()[this->index()]; }
  float pfSimpleSecondaryVertexHighPurBJetTags() const { return this->fCollection->fPfSimpleSecondaryVertexHighPurBJetTags->value()[this->index()]; }
  float pfCombinedSecondaryVertexV2BJetTags() const { return this->fCollection->fPfCombinedSecondaryVertexV2BJetTags->value()[this->index()]; }
  float pfCombinedSecondaryVertexSoftLeptonBJetTags() const { return this->fCollection->fPfCombinedSecondaryVertexSoftLeptonBJetTags->value()[this->index()]; }

  bool isBasicJet() const { return this->fCollection->fIsBasicJet->value()[this->index()]; }
  bool isCaloJet() const { return this->fCollection->fIsCaloJet->value()[this->index()]; }
  bool isJPTJet() const { return this->fCollection->fIsJPTJet->value()[this->index()]; }
  bool isPFJet() const { return this->fCollection->fIsPFJet->value()[this->index()]; }

  double neutralHadronEnergyFraction() const { return this->fCollection->fNeutralHadronEnergyFraction->value()[this->index()]; }
  double neutralEmEnergyFraction() const { return this->fCollection->fNeutralEmEnergyFraction->value()[this->index()]; }
  short nConstituents() const { return this->fCollection->fNConstituents->value()[this->index()]; }
  short chargedHadronMultiplicity() const { return this->fCollection->fChargedHadronMultiplicity->value()[this->index()]; }

  // double mcPt() const { return this->fCollection->fPt_MCjet->value()[this->index()]; }
  // double mcEat() const { return this->fCollection->fEta_MCjet->value()[this->index()]; }
  // double mcPhi() const { return this->fCollection->fPhi_MCjet->value()[this->index()]; }
  // double mcE() const { return this->fCollection->fE_MCjet->value()[this->index()]; }

  double JESup_pt() const { return this->fCollection->fPt_JESup->value()[this->index()]; }
  double JESup_eta() const { return this->fCollection->fEta_JESup->value()[this->index()]; }
  double JESup_phi() const { return this->fCollection->fPhi_JESup->value()[this->index()]; }
  double JESup_e() const { return this->fCollection->fE_JESup->value()[this->index()]; }

  double JESdown_pt() const { return this->fCollection->fPt_JESdown->value()[this->index()]; }
  double JESdown_eta() const { return this->fCollection->fEta_JESdown->value()[this->index()]; }
  double JESdown_phi() const { return this->fCollection->fPhi_JESdown->value()[this->index()]; }
  double JESdown_e() const { return this->fCollection->fE_JESdown->value()[this->index()]; }

  double JERup_pt() const { return this->fCollection->fPt_JERup->value()[this->index()]; }
  double JERup_eta() const { return this->fCollection->fEta_JERup->value()[this->index()]; }
  double JERup_phi() const { return this->fCollection->fPhi_JERup->value()[this->index()]; }
  double JERup_e() const { return this->fCollection->fE_JERup->value()[this->index()]; }

  double JERdown_pt() const { return this->fCollection->fPt_JERdown->value()[this->index()]; }
  double JERdown_eta() const { return this->fCollection->fEta_JERdown->value()[this->index()]; }
  double JERdown_phi() const { return this->fCollection->fPhi_JERdown->value()[this->index()]; }
  double JERdown_e() const { return this->fCollection->fE_JERdown->value()[this->index()]; }


protected:
  Particle<ParticleCollection<double>> fMCjet;

};

#endif
