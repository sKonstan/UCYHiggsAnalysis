// -*- c++ -*-
#ifndef DataFormat_MET_h
#define DataFormat_MET_h

#include "Framework/interface/Branch.h"
#include "Framework/interface/BranchManager.h"
#include "DataFormat/interface/Particle.h"

class BranchManager;

class METBase {
public:
  explicit METBase(const std::string& prefix);
  ~METBase();

  // Disable copying, assignment, and moving
  // Mainly because according to the design, there should be no need for them
  
  //METBase(const METBase&) = delete;
  //METBase(METBase&&) = delete;
  //METBase& operator=(const METBase&) = delete;
  //METBase& operator=(METBase&&) = delete;

  void setEnergySystematicsVariation(const std::string& scenario);

protected:
  const std::string& prefix() const { return fPrefix; }
  const std::string& energySystematicsVariation() const { return fEnergySystematicsVariation; }

private:
  std::string fPrefix;
  std::string fEnergySystematicsVariation;
};

template <typename NUMBER>
class MET_T: public METBase {
public:
  using float_type = NUMBER;
  using XYVector = math::XYVectorT<float_type>;
  using Scalar = float_type;

  explicit MET_T(const std::string& prefix):
    METBase(prefix),
    fVal(nullptr),
    fX(nullptr),
    fY(nullptr),
    fSignificance(nullptr),
    fIsCaloMET(nullptr),
    fIsPFMET(nullptr),
    fIsRecoMET(nullptr),
    fSumEt(nullptr),
    fPhi(nullptr),
    fNeutralEMEtFraction(nullptr),
    fNeutralEMEt(nullptr),
    fChargedMEtFraction(nullptr),
    fChargedEMEt(nullptr),
    fNeutralHadEtFraction(nullptr),
    fNeutralHadEt(nullptr),
    fChargedHadEtFraction(nullptr),
    fChargedHadEt(nullptr),
    fMuonEtFraction(nullptr),
    fMuonEt(nullptr)

  {}
  ~MET_T() {}

  void setupBranches(BranchManager& mgr) {
    mgr.book(prefix()+""+energySystematicsVariation(), &fVal);
    mgr.book(prefix()+"_x"+energySystematicsVariation(), &fX);
    mgr.book(prefix()+"_y"+energySystematicsVariation(), &fY);
    mgr.book(prefix()+"_significance"+energySystematicsVariation(), &fSignificance);
    mgr.book(prefix()+"_isCaloMET"+energySystematicsVariation(), &fIsCaloMET);
    mgr.book(prefix()+"_isPFMET"+energySystematicsVariation(), &fIsPFMET);
    mgr.book(prefix()+"_isRecoMET"+energySystematicsVariation(), &fIsRecoMET);
    //for caloMET
    mgr.book(prefix()+"_sumEt"+energySystematicsVariation(), &fSumEt);
    //for genMET
    mgr.book(prefix()+"_phi"+energySystematicsVariation(), &fPhi);
    mgr.book(prefix()+"_NeutralEMEtFraction"+energySystematicsVariation(), &fNeutralEMEtFraction);
    mgr.book(prefix()+"_NeutralEMEt"+energySystematicsVariation(), &fNeutralEMEt);
    mgr.book(prefix()+"_ChargedMEtFraction"+energySystematicsVariation(), &fChargedMEtFraction);
    mgr.book(prefix()+"_ChargedEMEt"+energySystematicsVariation(), &fChargedEMEt);
    mgr.book(prefix()+"_NeutralHadEtFraction"+energySystematicsVariation(), &fNeutralHadEtFraction);
    mgr.book(prefix()+"_NeutralHadEt"+energySystematicsVariation(), &fNeutralHadEt);
    mgr.book(prefix()+"_ChargedHadEtFraction"+energySystematicsVariation(), &fChargedHadEtFraction);
    mgr.book(prefix()+"_ChargedHadEt"+energySystematicsVariation(), &fChargedHadEt);
    mgr.book(prefix()+"_MuonEtFraction"+energySystematicsVariation(), &fMuonEtFraction);
    mgr.book(prefix()+"_MuonEt"+energySystematicsVariation(), &fMuonEt);

  }


  float_type val() const { return fVal->value(); }
  float_type x() const { return fX->value(); }
  float_type y() const { return fY->value(); }
  float_type et() const { return p2().R(); }
  float_type Phi() const { return p2().Phi(); }
  float_type phi() const { return p2().Phi(); }
  float_type significance() const { return fSignificance->value(); }
  bool isCaloMET () const { return fIsCaloMET->value(); }
  bool isPFMET () const { return fIsPFMET->value(); }
  bool isRecoMET () const { return fIsRecoMET->value(); }
  float_type sumEt()  const { return fSumEt->value(); }
  XYVector p2() const {
    return XYVector(x(), y());
  }
  
  float_type phi1()  const { return fPhi->value(); }
  float_type NeutralEMEtFraction()  const { return fNeutralEMEtFraction->value(); }
  float_type NeutralEMEt()  const { return fNeutralEMEt->value(); }
  float_type ChargedMEtFraction()  const { return fChargedMEtFraction->value(); }
  float_type ChargedEMEt()  const { return fChargedEMEt->value(); }
  float_type NeutralHadEtFraction()  const { return fNeutralHadEtFraction->value(); }
  float_type NeutralHadEt()  const { return fNeutralHadEt->value(); }
  float_type ChargedHadEtFraction()  const { return fChargedHadEtFraction->value(); }
  float_type ChargedHadEt()  const { return fChargedHadEt->value(); }
  float_type MuonEtFraction()  const { return fMuonEtFraction->value(); }
  float_type MuonEt()  const { return fMuonEt->value(); }




  

private:
  const Branch<float_type> *fVal;
  const Branch<float_type> *fX;
  const Branch<float_type> *fY;
  const Branch<float_type> *fSignificance;
  const Branch<bool>       *fIsCaloMET;
  const Branch<bool>       *fIsPFMET;
  const Branch<bool>       *fIsRecoMET;
  
  //for CaloMET
  const Branch<float_type> *fSumEt;

  //for GenMET
  const Branch<float_type> *fPhi;
  const Branch<float_type> *fNeutralEMEtFraction;
  const Branch<float_type> *fNeutralEMEt;
  const Branch<float_type> *fChargedMEtFraction;
  const Branch<float_type> *fChargedEMEt;
  const Branch<float_type> *fNeutralHadEtFraction;
  const Branch<float_type> *fNeutralHadEt;
  const Branch<float_type> *fChargedHadEtFraction;
  const Branch<float_type> *fChargedHadEt;
  const Branch<float_type> *fMuonEtFraction;
  const Branch<float_type> *fMuonEt;



};

using MET = MET_T<double>;

#endif
