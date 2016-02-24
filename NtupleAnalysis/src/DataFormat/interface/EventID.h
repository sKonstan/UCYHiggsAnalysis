// -*- c++ -*-
#ifndef DataFormat_EventID_h
#define DataFormat_EventID_h

#include "Framework/interface/Branch.h"

class BranchManager;

class EventID {
public:
  EventID();
  ~EventID();

  // Disable copying, assignment, and moving
  // Mainly because according to the design, there should be no need for them
  EventID(const EventID&) = delete;
  EventID(EventID&&) = delete;
  EventID& operator=(const EventID&) = delete;
  EventID& operator=(EventID&&) = delete;

  void setupBranches(BranchManager& mgr);

  unsigned long long event() const { return fEvent->value(); }
  unsigned int       lumi()  const { return fLumi->value(); }
  unsigned int       run()   const { return fRun->value(); }
  /// Number of partons generated
  short NUP() const { return fNUP->value(); }
  /// Trigger prescale
  float trgPrescale() const { return fPrescale->value(); }

  short nPUvertices() const { return fNPUvertices->value(); }
  short nGoodOfflineVertices() const { return fNGoodOfflineVertices->value(); }
  float pvX() const { return fPvX->value(); }
  float pvY() const { return fPvY->value(); }
  float pvZ() const { return fPvZ->value(); }
  float pvDistanceToNextVertex() const { return fPvDistanceToNextVertex->value(); }
  float pvDistanceToClosestVertex() const { return fPvDistanceToClosestVertex->value(); }

  
  
private:
  const Branch<unsigned long long> *fEvent;
  const Branch<unsigned int> *fLumi;
  const Branch<unsigned int> *fRun;
  const Branch<short> *fNUP;
  const Branch<float> *fPrescale;
  const Branch<short> *fNPUvertices;
  const Branch<short> *fNGoodOfflineVertices;
  const Branch<float> *fPvX;
  const Branch<float> *fPvY;
  const Branch<float> *fPvZ;
  const Branch<float> *fPvDistanceToNextVertex;
  const Branch<float> *fPvDistanceToClosestVertex;


};

#endif
