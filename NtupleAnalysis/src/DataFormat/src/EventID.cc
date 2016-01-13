#include "DataFormat/interface/EventID.h"
#include "Framework/interface/BranchManager.h"

EventID::EventID():
  fEvent(nullptr),
  fLumi(nullptr),
  fRun(nullptr),
  fNUP(nullptr),
  fPrescale(nullptr)
{}
EventID::~EventID() {}

void EventID::setupBranches(BranchManager& mgr) {
  mgr.book("EventInfo_event"   , &fEvent);
  mgr.book("EventInfo_lumi"    , &fLumi );
  mgr.book("EventInfo_run"     , &fRun  );
  mgr.book("EventInfo_NUP"     , &fNUP  );
  mgr.book("EventInfo_prescale", &fPrescale);
}

