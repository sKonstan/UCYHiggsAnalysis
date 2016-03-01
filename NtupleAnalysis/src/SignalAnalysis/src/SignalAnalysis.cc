// -*- c++ -*-
#include "Framework/interface/BaseSelector.h"
#include "Framework/interface/makeTH.h"

#include "EventSelection/interface/CommonPlots.h"
#include "EventSelection/interface/EventSelections.h"

#include "TDirectory.h"

class SignalAnalysis: public BaseSelector {
public:
  // explicit SignalAnalysis(const ParameterSet& config, const TH1* skimCounters);
  explicit SignalAnalysis(const ParameterSet& config);
  virtual ~SignalAnalysis() {}

  /// Books histograms
  virtual void book(TDirectory *dir) override;
  /// Sets up branches for reading the TTree
  virtual void setupBranches(BranchManager& branchManager) override;
  /// Called for each event
  virtual void process(Long64_t entry) override;

private:
  // Input parameters

  /// Common plots
  CommonPlots fCommonPlots;
  // Event selection classes and event counters (in same order like they are applied)
  Count cAllEvents;
  Count cTrigger;
  METFilterSelection fMETFilterSelection;
  Count cVertexSelection;
  ElectronSelection fElectronSelection;
  MuonSelection fMuonSelection;
  TauSelection fTauSelection;
  JetSelection fJetSelection;
  BJetSelection fBJetSelection;
  METSelection fMETSelection;
  Count cSelected;
    
  // Non-common histograms
  WrappedTH1* hExample;

};

#include "Framework/interface/SelectorFactory.h"
REGISTER_SELECTOR(SignalAnalysis);

SignalAnalysis::SignalAnalysis(const ParameterSet& config)
  : BaseSelector(config),
    fCommonPlots(config.getParameter<ParameterSet>("CommonPlots"), CommonPlots::kSignalAnalysis, fHistoWrapper),
    cAllEvents(fEventCounter.addCounter("All events")),
    cTrigger(fEventCounter.addCounter("Passed trigger")),
    fMETFilterSelection(config.getParameter<ParameterSet>("METFilter"), fEventCounter, fHistoWrapper, &fCommonPlots, ""),
    cVertexSelection(fEventCounter.addCounter("Primary vertex selection")),
    fElectronSelection(config.getParameter<ParameterSet>("ElectronSelection"), fEventCounter, fHistoWrapper, &fCommonPlots, ""),
    fMuonSelection(config.getParameter<ParameterSet>("MuonSelection"), fEventCounter, fHistoWrapper, &fCommonPlots, ""),
    fTauSelection(config.getParameter<ParameterSet>("TauSelection"), fEventCounter, fHistoWrapper, &fCommonPlots, ""), 
    fJetSelection(config.getParameter<ParameterSet>("JetSelection"), fEventCounter, fHistoWrapper, &fCommonPlots, ""),
    fBJetSelection(config.getParameter<ParameterSet>("BJetSelection"), fEventCounter, fHistoWrapper, &fCommonPlots, ""),
    fMETSelection(config.getParameter<ParameterSet>("METSelection"), fEventCounter, fHistoWrapper, &fCommonPlots, ""),
    cSelected(fEventCounter.addCounter("Selected events"))
{ }


void SignalAnalysis::book(TDirectory *dir) {
  fCommonPlots.book(dir, isData());
  fMETFilterSelection.bookHistograms(dir);
  fElectronSelection.bookHistograms(dir);
  fMuonSelection.bookHistograms(dir);
  fTauSelection.bookHistograms(dir);
  fJetSelection.bookHistograms(dir);
  fBJetSelection.bookHistograms(dir);
  fMETSelection.bookHistograms(dir);

  // Book non-common histograms
  hExample =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "example pT", "example pT", 40, 0, 400);
}


void SignalAnalysis::setupBranches(BranchManager& branchManager) {
  fEvent.setupBranches(branchManager);
}


void SignalAnalysis::process(Long64_t entry) {

  //====== Initialize
  fCommonPlots.initialize();
  fCommonPlots.setFactorisationBinForEvent(std::vector<float> {});
  cAllEvents.increment();


  //====== Apply trigger
  if ( !(fEvent.passTriggerDecision()) ) return;
  cTrigger.increment();
  int nVertices = fEvent.vertexInfo().value();
  fCommonPlots.setNvertices(nVertices);
  fCommonPlots.fillControlPlotsAfterTrigger(fEvent);


  //====== MET filters to remove events with spurious sources of fake MET
  const METFilterSelection::Data metFilterData = fMETFilterSelection.analyze(fEvent);
  if ( !metFilterData.passedSelection() ) return;
  

  //====== GenParticle analysis
  // if needed
  

  //====== Check that primary vertex exists
  if (nVertices < 1) return;
  cVertexSelection.increment();
  fCommonPlots.fillControlPlotsAtVertexSelection(fEvent);
  

  //====== Electron selection
  const ElectronSelection::Data eData = fElectronSelection.analyze(fEvent);
  if ( eData.hasIdentifiedElectrons() ) return; //fixme
  // fCommonPlots.fillControlPlotsAfterElectronSelection(fEvent); //fixme


  //====== Muon veto
  const MuonSelection::Data muData = fMuonSelection.analyze(fEvent);
  if ( muData.hasIdentifiedMuons() ) return; //fixme
  // fCommonPlots.fillControlPlotsAfterMuonSelection(fEvent); //fixme 


  //====== Tau selection
  const TauSelection::Data tauData = fTauSelection.analyze(fEvent);
  if ( !tauData.hasIdentifiedTaus() ) return;
  //====== Fake tau SF
  // if ( fEvent.isMC() ){ fEventWeight.multiplyWeight(tauData.getTauMisIDSF()); }}
  //====== Tau trigger SF
  // if ( fEvent.isMC() ){ fEventWeight.multiplyWeight(tauData.getTauTriggerSF()); }
  // fCommonPlots.fillControlPlotsAfterTauSelection(fEvent); //fixme


  //====== MET trigger SF
  // const METSelection::Data silentMETData = fMETSelection.analyze(fEvent, nVertices);
  // if (fEvent.isMC()) {
  // fEventWeight.multiplyWeight(silentMETData.getMETTriggerSF());
  // }


  //====== Jet selection
  const JetSelection::Data jetData = fJetSelection.analyze(fEvent, tauData.getSelectedTau());
  if ( !jetData.passedSelection() ) return;
  fCommonPlots.fillControlPlotsAfterJetSelections(fEvent);


  //====== b-jet selection
  const BJetSelection::Data bjetData = fBJetSelection.analyze(fEvent, jetData);
  if (!bjetData.passedSelection() ) return;
  //====== b tag SF
  // if ( fEvent.isMC() ) { fEventWeight.multiplyWeight(bjetData.getBTaggingScaleFactorEventWeight()); }


  //====== MET selection
  const METSelection::Data METData = fMETSelection.analyze(fEvent, nVertices);
  if ( !METData.passedSelection() ) return;
  

  //====== All cuts passed
  cSelected.increment();


  // Fill final plots
  fCommonPlots.fillControlPlotsAfterAllSelections(fEvent);

  
  //====== Finalize
  fEventSaver.save();
}
