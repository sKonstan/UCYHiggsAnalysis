#include "Tools/interface/MCTools.h"
#include "Framework/interface/Exception.h"

#include "TFile.h"
#include "TH1.h"

//#define DEBUG

MCTools::MCTools(Event &fEvt){
  fEvent = &fEvt;
  if( fEvent->isData()==true ) return; 
}


MCTools::~MCTools(){}  

bool MCTools::IsNeutrino(const int pdgId){
  if( ( fabs(pdgId) == 12)  || ( fabs(pdgId) == 14)  || ( fabs(pdgId) == 16) ) return true;
  else return false;
}


genParticle MCTools::GetGenP(const unsigned int genP_Index){
  return fEvent->genparticles().getAllGenpCollection().at(genP_Index);
}


TLorentzVector MCTools::GetP4(const int genP_Index){

  TLorentzVector p4;
  genParticle genP = GetGenP(genP_Index);
  double genP_Pt   = genP.pt();
  double genP_Eta  = genP.eta();
  double genP_Phi  = genP.phi();                                                                                                                                           
  double genP_Mass = genP.mass();
  p4.SetPtEtaPhiM(genP_Pt, genP_Eta, genP_Phi, genP_Mass);
  return p4;
}


bool MCTools::RecursivelyLookForMotherId(const unsigned int genP_Index,
					 int momId,
					 const bool takeAbsId){

  genParticle genP     = GetGenP(genP_Index);
  unsigned short nMoms = genP.mothers().size();
  if (nMoms == 0) return false;

#ifdef DEBUG
  std::cout << "Looking for mother #" << momId << " of genParticle with index (pdgid) "<< genP_Index << "(" << genP_pdgId << ")" << std::endl;
#endif

  int myId;
  // For-loop: All mothers
  for (unsigned short i = 0; i < nMoms; i++){

    unsigned int mom_Index = genP.mothers().at(i);
    genParticle mom        = GetGenP(mom_Index);
    int mom_PdgId          = mom.pdgId();

    // std::cout << "genP_Index = " << genP_Index << ", genP_PdgId = " << genP_PdgId << ", mom_Index = " << mom_Index << ", mom_PdgId = " << mom_PdgId << std::endl;

    if (!takeAbsId) {
      myId  = fabs(mom_PdgId);
      momId = fabs(momId);
    }
    else myId = mom_PdgId;
    if (myId == momId) return true;
    if (RecursivelyLookForMotherId(mom_Index, momId, takeAbsId) ) return true;
  }
  return false;
}


int MCTools::GetPosOfMotherId(const unsigned int genP_Index,
			      int momId,
			      const bool takeAbsId){
  
  genParticle genP     = GetGenP(genP_Index);
  unsigned short nMoms = genP.mothers().size();
  if (nMoms == 0) return 65535;
  int myId;
  int mom_Index;

  // For-loop: All mothers
  for (unsigned short i = 0; i < nMoms; i++){

    mom_Index = genP.mothers().at(i);
    genParticle mom = GetGenP(mom_Index);
    int mom_PdgId   = mom.pdgId();

    if (!takeAbsId) {
      myId = fabs(mom_PdgId);
      momId = fabs(momId);
    }
    else {
      myId = mom_PdgId;
    } 
    int status = mom.status();
    if (myId == momId) {
      if (status == 3) {
	if(mom.daughters().size()>2){
	  mom_Index = mom.daughters().at(2);
	  return mom_Index;
	}
	else return 65535;
      }
      else return mom_Index;
    }
    else {
      mom_Index = GetPosOfMotherId(mom_Index, momId, takeAbsId);
      return mom_Index;
    }
  }// for (unsigned short i = 0; i < nMoms; i++){
  return 65535;
}



bool MCTools::LookForMotherId(const unsigned int genP_Index,
			      int momId,
			      const bool takeAbsId){

  genParticle genP     = GetGenP(genP_Index);
  unsigned short nMoms = genP.mothers().size();

  if (nMoms == 0) return false;
  int myId;

  // For-loop: All mothers
  for (unsigned short i = 0; i < nMoms; i++) {

    unsigned short mom_Index = genP.mothers().at(i);
    genParticle mom          = GetGenP(mom_Index);
    int mom_PdgId            = mom.pdgId();


    if (!takeAbsId) {
      myId  = fabs(mom_PdgId);
      momId = fabs(momId);
    }
    else myId = mom_PdgId;
    if (myId == momId) return true;
  }// for (unsigned short i = 0; i < nMoms; i++) {
  return false;
}


TLorentzVector MCTools::GetVisibleP4(const std::vector<short int>& daughters){

  /*
    Returns the 4-vector sum of all visible daughters. If one would use this
    to calculate the visible eT from a hadronic tau then the eT calculated would 
    correcpond to the vector-sum eT of all decay products (and NOT the scalar eT sum)
    In fact, the eT calculated using this 4-vector would be identical to the eT of 
    the tau itself or that of the intermediate resonance (e.g. rho, alpha_1)
  */

  TLorentzVector p4(0,0,0,0);
  if (daughters.size() == 0) return p4;

  // For-loop: Daughters
  for (unsigned short i = 0; i< daughters.size(); i++){

    int dau_Index   = daughters.at(i);
    genParticle dau = GetGenP(dau_Index);
    int dau_PdgId   = dau.pdgId();
    double dau_Pt   = dau.pt();
    double dau_Eta  = dau.eta();
    double dau_Phi  = dau.phi();                                                                                                                                           
    double dau_Mass = dau.mass();

    // Skip invisible daughters (neutrinos)
    if ( IsNeutrino(dau_PdgId) ) continue;

    TLorentzVector tmp;
    tmp.SetPtEtaPhiM(dau_Pt, dau_Eta, dau_Phi, dau_Mass);
    p4 += tmp;

  } // For-loop: Daughters

  return p4;
}


TLorentzVector MCTools::GetVisibleP4(const unsigned int genP_Index){

  // Overloaded version ofTLorentzVector MCTools::GetVisibleP4() 

  genParticle genP = GetGenP(genP_Index);
  const std::vector<short int> daughters = genP.daughters();

  TLorentzVector p4(0,0,0,0);
  if (daughters.size() == 0) return p4;

  // For-loop: Daughters
  for (unsigned short i = 0; i< daughters.size(); i++){

    int dau_Index   = daughters.at(i);
    genParticle dau = GetGenP(dau_Index);
    int dau_PdgId   = dau.pdgId();
    double dau_Pt   = dau.pt();
    double dau_Eta  = dau.eta();
    double dau_Phi  = dau.phi();                                                                                                                                           
    double dau_Mass = dau.mass();

    // Skip invisible daughters (neutrinos)
    if ( IsNeutrino(dau_PdgId) ) continue;

    TLorentzVector tmp;
    tmp.SetPtEtaPhiM(dau_Pt, dau_Eta, dau_Phi, dau_Mass);
    p4 += tmp;

  } // For-loop: Daughters

  return p4;
}


int MCTools::GetLdgDaughter(const int genP_Index, 
			    bool bOnlyChargedDaughters){


  genParticle genP = GetGenP(genP_Index);
  const std::vector<short int> daughters = genP.daughters();

  // Declarations
  int ldgPtIndex = -1;
  double ldgPt   = -1.0;

  if (daughters.size() == 0) return ldgPtIndex;

  // For-loop: Daughters
  for (size_t i = 0; i< daughters.size(); i++){
    
    int dau_Index   = daughters.at(i);
    genParticle dau = GetGenP(dau_Index);
    int dau_PdgId   = dau.pdgId();

    // Skip invisible daughters (neutrinos)
    if ( IsNeutrino(dau_PdgId) ) continue;

    // Get pt and charge
    double dau_Pt     = dau.pt();
    double dau_Charge = dau.charge();
    
    if(bOnlyChargedDaughters && fabs(dau_Charge) < 1 ) continue;

    // Find leading daughter index
    if (dau_Pt > ldgPt ){
      ldgPt      = dau_Pt;
      ldgPtIndex = dau_Index;
    }
    
  }  // For-loop: Daughters

  return ldgPtIndex;
}


double MCTools::GetHadronicTauMaxSignalCone(const int genP_Index,
					    bool bOnlyChargedDaughters, 
					    double minPt){

  genParticle genP = GetGenP(genP_Index);
  if (fabs(genP.pdgId() != 15) ) {
    std::cout << "=== MCTools::GetHadronicTauMaxSignalCone():\n\t Particle with index " << genP_Index << " is not a tau. Return -1" << std::endl;
    return -1;
  }

  const std::vector<short int> daughters = genP.daughters();
  if (daughters.size() <= 1) return -1;

  // Get Ldg Charged Track properties
  const int ldgChTk_Index   = GetLdgDaughter(genP_Index, true);
  TLorentzVector ldgChTk_P4 = GetP4(ldgChTk_Index);

  double dRMax = -1.0;

  // For-loop: Daughters
  for (size_t i = 0; i< daughters.size(); i++){

    int dau_Index   = daughters.at(i);
    genParticle dau = GetGenP(dau_Index);
    int dau_PdgId   = dau.pdgId();

    // Skip self and neutrinos
    if (dau_Index == ldgChTk_Index) continue;
    if (IsNeutrino(dau_PdgId)) continue;

    // Get Daughter properties
    TLorentzVector dau_P4 = GetP4(dau_Index);
    double dau_Charge     = dau.charge();

    // Consider only charged daughters above minPt
    if (dau_P4.Pt() < minPt) continue;
    if (bOnlyChargedDaughters){ if( fabs(dau_Charge) < 1 ) continue; }

    double dR = ROOT::Math::VectorUtil::DeltaR(ldgChTk_P4, dau_P4);
    if (dR > dRMax) dRMax = dR;
    
  } // For-loop: Daughters

  return dRMax;
}


/*
void MCTools::GetHadronicTauChargedOrNeutralPions(int tauIndex, 
						  int charge,
						  std::vector<unsigned short> &chargedPions){
  
  
  if (GenP_Daughters->at(tauIndex).size() == 0) return;

  // Get the pi+/-,pi0, K+/-, K0,K0L,KOS,eta,omegas and gammas
  std::vector<unsigned short> hTau_Dau;
  GetHadronicTauFinalDaughters(tauIndex, hTau_Dau);
  
  // For-loop: Daughters
  for (unsigned short i = 0; i< hTau_Dau.size(); i++){

    // Get Daughter properties
    int daughter_index     = hTau_Dau.at(i);
    Double_t daughter_charge = GenP_Charge->at(daughter_index);

    // Keep only the pi+/-, K+/-, omegas
    if( fabs(daughter_charge) != charge ) continue;
    
    // Save to container
    chargedPions.push_back(daughter_index);
    
  } // For-loop: Daughters
  
  return;
}
*/