// -*- c++ -*-                                
#ifndef Framework_MCTools_h
#define Framework_MCTools_h

#include "DataFormat/interface/Event.h"

#include <cmath>
#include <iomanip>
#include <TLorentzVector.h>
#include <string>
#include <cmath>
#include <vector>

using namespace std;
typedef Particle<ParticleCollection<double>> genParticle;

class MCTools {
  
public:
  MCTools(Event &fEvt);
  ~MCTools();
  genParticle GetGenP(int genP_Index);
  bool RecursivelyLookForMotherId(int genP_Index, int momId, const bool posn);
  int PosOfMotherId(int genP_Index, int momId, const bool takeAbsId);
  TLorentzVector GetP4(const int genP_Index);
  bool LookForMotherId(int genP_Index, int momId, const bool takeAbsId);
  TLorentzVector GetVisibleP4(const std::vector<unsigned short>& daughters);
  
private:
  Event *fEvent;
  
};

#endif

