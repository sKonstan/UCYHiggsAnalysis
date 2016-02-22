// -*- c++ -*-                                
#ifndef Framework_MCTools_h
#define Framework_MCTools_h

#include "DataFormat/interface/Event.h"

#include <cmath>
#include <iomanip>
#include <string>
#include <vector>

#include "TLorentzVector.h"
#include "Math/VectorUtil.h"

using namespace std;
typedef Particle<ParticleCollection<double>> genParticle;

class MCTools {
  
public:
  MCTools(Event &fEvt);
  ~MCTools();
  genParticle GetGenP(const unsigned int genP_Index);
  bool RecursivelyLookForMotherId(const unsigned int genP_Index, 
				  int momId, 
				  const bool posn);
  TLorentzVector GetP4(const int genP_Index);
  bool LookForMotherId(const unsigned int genP_Index, 
		       int momId, 
		       const bool takeAbsId);
  TLorentzVector GetVisibleP4(const unsigned int genP_Index);
  TLorentzVector GetVisibleP4(const std::vector<short int>& daughters);
  bool IsNeutrino(const int pdgId);
  int GetPosOfMotherId(const unsigned int genP_Index,
		       int momId, 
		       const bool takeAbsId);
  int GetLdgDaughter(const int genP_Index, 
		     bool bOnlyChargedDaughters);

  double GetHadronicTauMaxSignalCone(const int genP_Index, 
				     bool bOnlyChargedDaughters, 
				     double minPt);

  void GetHadronicTauFinalDaughters(const int genP_Index,
				    std::vector<short int>& finalDaughters);

  void GetHadronicTauChargedPions(const int genP_Index, 
				  std::vector<short int> &chargedPions);

  void GetHadronicTauNeutralPions(const int genP_Index,
				  std::vector<short int> &neutralPions);

  bool IsFinalStateTau(const int genP_Index);

  bool IsFinalStateHadronicTau(const int genP_Index);

  int GetTauDecayMode(const int genP_Index);

  void PrintDaughters(const int genP_Index, bool bPrintHeaders=true);

  void PrintGenParticle(const int genP_Index, bool bPrintHeaders=true);


private:
  Event *fEvent;

  void _GetHadronicTauChargedOrNeutralPions(int tauIndex, 
					    bool charged,
					    std::vector<short int> &pions);


  
};

#endif

