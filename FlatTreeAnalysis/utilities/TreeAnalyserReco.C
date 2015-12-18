#ifndef TreeAnalyserReco_cxx
#define TreeAnalyserReco_cxx

#include <typeinfo>

#define TREEDEFINITIONRECO TreeDefinitionReco

#include "TreeAnalyserReco.h"
#include "L1Tracks.C"
#include "L1PixelTrackFit.C"

void TreeAnalyserReco::InitSelector()
{
  s = new L1Tracks(this);
  f  = new L1PixelTrackFit(this);
}

#endif // TreeAnalyserReco_cxx
