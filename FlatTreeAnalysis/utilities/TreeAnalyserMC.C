#ifndef TreeAnalyserMC_cxx
#define TreeAnalyserMC_cxx

#define USING_MC

#define TREEDEFINITIONGENP TreeDefinitionGenP
#define TREEDEFINITIONRECO TreeDefinitionReco

#include <typeinfo>

#include "TreeAnalyserMC.h"
#include "L1Tracks.C"
#include "TrackingParticles.C"

void TreeAnalyserMC::InitSelector()
{
  s  = new L1Tracks(this);
  tp = new TrackingParticles(this);
}

#endif //TreeAnalyserMC_cxx
 
