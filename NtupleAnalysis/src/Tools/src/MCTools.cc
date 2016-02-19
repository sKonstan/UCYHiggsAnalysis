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


genParticle MCTools::GetGenP(int genP_Index){
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


bool MCTools::RecursivelyLookForMotherId(int genP_Index,
					 int momId,
					 const bool takeAbsId){

  genParticle genP     = GetGenP(genP_Index);
  // int genP_PdgId       = genP.pdgId();
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


int MCTools::PosOfMotherId(int genP_Index,
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
      mom_Index = PosOfMotherId(mom_Index, momId, takeAbsId);
      return mom_Index;
    }
  }// for (unsigned short i = 0; i < nMoms; i++){
  return 65535;
}



bool MCTools::LookForMotherId(int genP_Index,
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

  TLorentzVector p4;
  if (daughters.size() == 0) return p4;

  // For-loop: Daughters
  for (unsigned short i = 0; i< daughters.size(); i++){

    unsigned short dau_Index = daughters.at(i);
    int dau_PdgId                  = abs( dau_Index );

    // Skip invisible daughters (neutrinos)
    if( (dau_PdgId == 12)  || (dau_PdgId == 14)  || (dau_PdgId == 16) ){ continue; }

    genParticle dau  = GetGenP(dau_Index);
    double genP_Pt   = dau.pt();
    double genP_Eta  = dau.eta();
    double genP_Phi  = dau.phi();                                                                                                                                           
    double genP_Mass = dau.mass();

    TLorentzVector tmp;
    tmp.SetPtEtaPhiM(genP_Pt, genP_Eta, genP_Phi, genP_Mass);
    p4 += tmp;

  } // For-loop: Daughters

  return p4;
}



// ================================================================================================================================================

/*
double MCTools::getWeight(const Event& fEvent){
 

  if(h_weight == 0)
    throw hplus::Exception("runtime") << "MCTools enabled, but no MCToolss in multicrab!";

  int NPU = fEvent.vertexInfo().simulatedValue();
  int bin = h_weight->GetXaxis()->FindBin( NPU );
  //std::cout << "***" << NPU << ":" << bin << ":" << h_weight->GetBinContent( bin ) << std::endl;
  return h_weight->GetBinContent( bin );
}

void MCTools::calculateWeights(TH1* h_data, TH1* h_mc){
  if(!h_data or !h_mc)
    throw hplus::Exception("runtime") << "Did not find pileup distributions";

  h_data->Scale(1.0/h_data->Integral());
  h_mc->Scale(1.0/h_mc->Integral());
  //std::cout << h_data->Integral() << ", " << h_mc->Integral() << std::endl;

  h_weight = (TH1*)h_data->Clone("lumiWeights");
  h_weight->Divide(h_mc);
//   for (int i = 1; i < h_weight->GetNbinsX()+1; ++i)
//     std::cout << i << ":" << h_weight->GetBinContent(i) << std::endl;
}
*/
