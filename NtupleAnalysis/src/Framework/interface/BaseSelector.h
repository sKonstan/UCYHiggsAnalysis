// -*- c++ -*-
#ifndef Framework_BaseSelector_h
#define Framework_BaseSelector_h

#include "Framework/interface/ParameterSet.h"
#include "Framework/interface/EventWeight.h"
#include "Framework/interface/EventCounter.h"
#include "Framework/interface/HistoWrapper.h"
#include "Framework/interface/EventSaver.h"

#include "DataFormat/interface/Event.h"

#include "Tools/interface/PileupWeight.h"

#include "Rtypes.h"
#include "TBranch.h"
#include "TTree.h"

#include <string>
#include <vector>
#include <algorithm>

class TTree;
class TDirectory;
class TH1;

class BranchManager;

/// Selector base class
class BaseSelector {
public:
  explicit BaseSelector(const ParameterSet& config);
  virtual ~BaseSelector();

  void setEventSaver(EventSaver *saver) { fEventSaver.setSaver(saver); }

  void setOutput(TDirectory *dir) {
    fEventCounter.setOutput(dir);
    bookInternal(dir);
    book(dir);
  }

  /// Processes internally event before process method is called
  void processInternal(Long64_t entry);

  void setPileUpWeights(TH1* hPUdata, TH1* hPUmc){
    fPileupWeight.calculateWeights(hPUdata,hPUmc);
  }
  
  void setIsttbar(bool status) { bIsttbar = status; }

  /// Book internal histograms
  void bookInternal(TDirectory *dir);
   
  // Implement these
  virtual void book(TDirectory *dir) = 0;
  virtual void setupBranches(BranchManager& branchManager) = 0;
  virtual void process(Long64_t entry) = 0;

protected:
  bool isMC() const { return fIsMC; }
  bool isData() const { return !isMC(); }
  bool isttbar() const { return bIsttbar; }

  Event fEvent;
  EventWeight fEventWeight;
  EventCounter fEventCounter;
  HistoWrapper fHistoWrapper;
  EventSaverClient fEventSaver;
  PileupWeight fPileupWeight;

private:
  Count cBaseAllEvents;
  Count cPileupWeighted;
  Count cPrescaled;
  Count cTopPtReweighted;
  Count cExclusiveSamplesWeighted;

  const bool fIsMC;
  bool bIsttbar;
  int iTopPtVariation;
  
  // Internal histograms
  WrappedTH1* hNvtxBeforeVtxReweighting;
  WrappedTH1* hNvtxAfterVtxReweighting;
  
  
  
};

#endif