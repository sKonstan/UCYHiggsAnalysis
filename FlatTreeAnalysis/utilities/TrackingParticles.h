#ifndef TrackingParticles_h
#define TrackingParticles_h

#include "TreeDefinitionReco.h"

#ifdef USING_MC
#include "TreeDefinitionGenP.h" 
#define TREEANALYSER TreeAnalyserMC
#include "TreeAnalyserMC.h"
#else
#include "TreeDefinitionReco.h"
#define TREEANALYSER TreeAnalyserReco
#include "TreeAnalyserReco.h"
#endif // USING_MC

using namespace std;

class TrackingParticles
{
 public:
  // Constructors/Destructors
  TrackingParticles(TREEANALYSER* t_) { t = t_; };

  // Member Functions
  double GetD0(const int iTrack);

  double GetD0Mag(const int iTrack);

  double GetD0Sign(const int iTrack);

  double GetD0Phi(const int iTrack);
  
  void PrintTPProperties(const int iTrack);

  unsigned int GetNumOfStubs(const int iTrack);

  TLorentzVector GetP4(const vector<int> tks_Index);

  // Variables
  TREEANALYSER* t;

 private:
  // Variables
  MCTools mcTools;
  AuxTools auxTools;

  int GetPixelIndexOfTrack(const int tk_Index);

};

#endif //ObjectSelect_h