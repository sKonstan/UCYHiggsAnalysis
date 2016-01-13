#include "DataFormat/interface/VertexInfo.h"
#include "Framework/interface/BranchManager.h"

VertexInfo::VertexInfo():
  bBranchesExist(false),
  fNPU(nullptr),
  fSimulatedNPU(nullptr),
  fPVDistanceToClosestVertex(nullptr),
  fPVDistanceToNextVertex(nullptr),
  fPVx(nullptr),
  fPVy(nullptr),
  fPVz(nullptr)
{}
VertexInfo::~VertexInfo() {}

void VertexInfo::setupBranches(BranchManager& mgr) {
  //mgr.book("nPU", &fNPU); // The MC number of PU vertices is not available for data
  mgr.book("EventInfo_nGoodOfflineVertices"     , &fNPU );
  mgr.book("EventInfo_nPUvertices"              , &fSimulatedNPU );
  mgr.book("EventInfo_pvDistanceToClosestVertex", &fPVDistanceToClosestVertex );
  mgr.book("EventInfo_pvDistanceToNextVertex"   , &fPVDistanceToNextVertex );
  mgr.book("EventInfo_pvX"                      , &fPVx );
  mgr.book("EventInfo_pvY"                      , &fPVy );
  mgr.book("EventInfo_pvZ"                      , &fPVz );
  bBranchesExist = true;
}

