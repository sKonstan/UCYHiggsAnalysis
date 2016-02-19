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
    double dau_Pt  = dau.pt();
    int dau_Charge = dau.charge();
    
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
  if ( std::abs(genP.pdgId()) != 15) {
    std::cout << "=== MCTools::GetHadronicTauMaxSignalCone():" << std::endl;
    std::cout << "\t Particle with index " << genP_Index << " is not a tau (pdgId = " << genP.pdgId() << "). Return" << std::endl;
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
    int dau_Charge        = dau.charge();

    // Consider only charged daughters above minPt
    if (dau_P4.Pt() < minPt) continue;
    if (bOnlyChargedDaughters){ if( fabs(dau_Charge) < 1 ) continue; }

    double dR = ROOT::Math::VectorUtil::DeltaR(ldgChTk_P4, dau_P4);
    if (dR > dRMax) dRMax = dR;
    
  } // For-loop: Daughters

  return dRMax;
}


void MCTools::GetHadronicTauFinalDaughters(const int genP_Index,
					   std::vector<short int>& finalDaughters){

  genParticle genP = GetGenP(genP_Index);
  int genP_PdgId   = std::abs(genP.pdgId());
  if (genP_PdgId != 15) {
    // std::cout << "=== MCTools::GetHadronicTauFinalDaughters():" << std::endl;
    // std::cout << "\t Particle with index " << genP_Index << " is not a tau (pdgId = " << genP.pdgId() << "). Return" << std::endl;
    return;
  }

  if (genP.daughters().size() == 0) return;

  // For-loop: Daughters
  for (size_t i = 0; i< genP.daughters().size(); i++){

    int dau_Index   = genP.daughters().at(i);
    genParticle dau = GetGenP(dau_Index);
    int dau_PdgId   = dau.pdgId();

    // Keep only the pi+/-,pi0, K+/-, 
    // K0,K0L,KOS,eta,omegas and gammas from tau->tau+gamma transition
    if ( (dau_PdgId == 111 || dau_PdgId == 211 || dau_PdgId == 321 ||   //pi0,pi+/-,K+/-
          dau_PdgId == 130 || dau_PdgId == 310 || dau_PdgId == 311 ||   //K0L,K0S,K0
	  dau_PdgId == 211 || dau_PdgId == 223)                     //eta and omega
	 || (dau_PdgId == 22 && genP_PdgId==15 && finalDaughters.size()!=0 ) ){  //Avoid leptonic decay
      // Because of the mixing of Generator and Detector simulation particles
      // in the list check if the particle has a parent already in the list
      // If it does then it comes from a hadronic interaction with the
      // detector material and it is not part of the tau decay
      int ifound = 0;

      // For-loop: Daughters
      for (size_t j = 0; j < finalDaughters.size(); j++){

	int jdau_Index   = finalDaughters.at(j);
	genParticle jdau = GetGenP(jdau_Index);
	int jdau_PdgId   = jdau.pdgId();
	if (RecursivelyLookForMotherId(dau_Index, jdau_PdgId, true) ) ifound += 1;

      }// for (short int j=0; j< daughters.size(); j++){

      if (ifound == 0) finalDaughters.push_back(dau_Index);
    
    } // if ( (dau_PdgId == 111 ...

    GetHadronicTauFinalDaughters(dau_Index, finalDaughters);
  }
  return;
}



void MCTools::_GetHadronicTauChargedOrNeutralPions(int genP_Index, 
						   bool charged,
						   std::vector<short int> &pions){

  std::cout << "=== MCTools::_GetHadronicTauChargedOrNeutralPions():\n\t Requires debugging!" << std::endl;  

  genParticle genP = GetGenP(genP_Index);
  if ( std::abs(genP.pdgId()) != 15) {
    std::cout << "=== MCTools::_GetHadronicTauChargedOrNeutralPions():" << std::endl;
    std::cout << "\t Particle with index " << genP_Index << " is not a tau (pdgId = " << genP.pdgId() << "). Return" << std::endl;
    return;
  }

  if (genP.daughters().size() == 0) return;

  // Get the pi+/-,pi0, K+/-, K0, K0L, KOS, Eta, Omegas and Gammas
  std::vector<short int> daughters;
  GetHadronicTauFinalDaughters(genP_Index, daughters);
  
  // For-loop: Daughters
  for (unsigned short i = 0; i< daughters.size(); i++){

    // Get the daughter properties
    int dau_Index   = daughters.at(i);
    genParticle dau = GetGenP(dau_Index);
    int dau_Charge  = dau.charge();

    // Keep only the pi+/-, K+/-, omegas
    if (charged && std::abs(dau_Charge)==0 ) continue;

    // Keep only the p0, K0 etc..
    if (!charged && std::abs(dau_Charge)!=0 ) continue;

    // Save to container
    pions.push_back(dau_Index);
    
  } // For-loop: Daughters
  
  return;
}


void MCTools::GetHadronicTauNeutralPions(int genP_Index, 
					 std::vector<short int> &neutralPions){

  _GetHadronicTauChargedOrNeutralPions(genP_Index, false, neutralPions);
  return;
}


void MCTools::GetHadronicTauChargedPions(int genP_Index, 
					 std::vector<short int> &chargedPions){

  _GetHadronicTauChargedOrNeutralPions(genP_Index, true, chargedPions);
  return;
}

