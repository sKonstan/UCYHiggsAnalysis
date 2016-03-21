// -*- c++ -*-
#include "Framework/interface/BaseSelector.h"
#include "Framework/interface/makeTH.h"

#include "EventSelection/interface/CommonPlots.h"
#include "EventSelection/interface/EventSelections.h"

#include "TDirectory.h"

class SignalAnalysis: public BaseSelector {
public:
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
  // Count cFakeTauSFCounter;
  // Count cTauTriggerSFCounter;
  // Count cMetTriggerSFCounter;
  ElectronSelection fElectronSelection;
  MuonSelection fMuonSelection;
  Count cLeptons;
  TauSelection fTauSelection;
  JetSelection fJetSelection;
  BJetSelection fBJetSelection;
  // Count cBTaggingSFCounter;
  METSelection fMETSelection;
  Count cSelected;
    
  // Histograms
  WrappedTH1* hExample;

};

#include "Framework/interface/SelectorFactory.h"
REGISTER_SELECTOR(SignalAnalysis);

SignalAnalysis::SignalAnalysis(const ParameterSet& config)
  : BaseSelector(config),
    fCommonPlots(config.getParameter<ParameterSet>("CommonPlots"), CommonPlots::kSignalAnalysis, fHistoWrapper),
    cAllEvents( fEventCounter.addCounter("All events") ),
    cTrigger( fEventCounter.addCounter("Passed trigger") ),
    fMETFilterSelection( config.getParameter<ParameterSet>("METFilter"), fEventCounter, fHistoWrapper, &fCommonPlots, ""),
    cVertexSelection( fEventCounter.addCounter("PV selection") ),
    // fElectronSelection( config.getParameter<ParameterSet>("ElectronSelection"), fEventCounter, fHistoWrapper, &fCommonPlots, ""), 
    // fMuonSelection( config.getParameter<ParameterSet>("MuonSelection"), fEventCounter, fHistoWrapper, &fCommonPlots, ""),
    fElectronSelection( config.getParameter<ParameterSet>("ElectronSelection"), ""),
    fMuonSelection( config.getParameter<ParameterSet>("MuonSelection"), ""),
    cLeptons( fEventCounter.addCounter("Passed leptons") ),
    fTauSelection( config.getParameter<ParameterSet>("TauSelection"), fEventCounter, fHistoWrapper, &fCommonPlots, ""), 
    fJetSelection( config.getParameter<ParameterSet>("JetSelection"), fEventCounter, fHistoWrapper, &fCommonPlots, ""),
    fBJetSelection( config.getParameter<ParameterSet>("BJetSelection"), fEventCounter, fHistoWrapper, &fCommonPlots, ""),
    fMETSelection( config.getParameter<ParameterSet>("METSelection"), fEventCounter, fHistoWrapper, &fCommonPlots, ""),
    cSelected( fEventCounter.addCounter("Selected events") )
{ }


void SignalAnalysis::book(TDirectory *dir) {
  fCommonPlots.book(dir, isData());
  // Book histograms in event selection classes
  fMETFilterSelection.bookHistograms(dir);
  fElectronSelection.bookHistograms(dir);
  fMuonSelection.bookHistograms(dir);
  fTauSelection.bookHistograms(dir);
  fJetSelection.bookHistograms(dir);
  fBJetSelection.bookHistograms(dir);
  fMETSelection.bookHistograms(dir);

  // Book histograms
  hExample = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "example pT", "example pT", 40, 0, 400);

  return;
}


void SignalAnalysis::setupBranches(BranchManager& branchManager) {
  fEvent.setupBranches(branchManager);

  return;
}


void SignalAnalysis::process(Long64_t entry) {

  //====== Initialize
  fCommonPlots.initialize();
  fCommonPlots.setFactorisationBinForEvent(std::vector<float> {});
  cAllEvents.increment();


  //====== Apply Cut: Trigger
  if ( !(fEvent.passTriggerDecision()) ) return;
  cTrigger.increment();
  int nVertices = fEvent.vertexInfo().value();
  fCommonPlots.setNvertices(nVertices);
  fCommonPlots.fillControlPlotsAfterTrigger(fEvent);


  //====== Apply Cut: MET filters [remove events with spurious sources of fake MET]
  const METFilterSelection::Data metFilterData = fMETFilterSelection.analyze(fEvent);
  if ( !metFilterData.passedSelection() ) return;
  

  //====== GenParticle analysis
  // if ( fEvent.isMC() )
  // {
  // } 


  //====== Apply Cut: Primary Vertex (PV)
  if (nVertices < 1) return;
  cVertexSelection.increment();
  fCommonPlots.fillControlPlotsAtVertexSelection(fEvent);
  
  
  /*
  //====== Apply Cut: Electron selection
  const ElectronSelection::Data eData = fElectronSelection.analyze(fEvent);
  if ( !eData.hasIdentifiedElectrons() ) return;
  fCommonPlots.fillControlPlotsAfterElectronSelection(fEvent, eData);


  //====== Apply Cut: Muon selection
  const MuonSelection::Data muData = fMuonSelection.analyze(fEvent);
  if ( !muData.hasIdentifiedMuons() ) return;
  fCommonPlots.fillControlPlotsAfterMuonSelection(fEvent, muData);
  */


  //====== Apply Cut: Lepton selection
  const ElectronSelection::Data eData = fElectronSelection.analyze(fEvent);
  const MuonSelection::Data muData    = fMuonSelection.analyze(fEvent);
  const size_t nElectrons             = eData.getSelectedElectrons().size();
  const size_t nMuons                 = muData.getSelectedMuons().size();
  const size_t nLeptons               = nElectrons + nMuons;
  if ( nLeptons < 2 ) return;

  fCommonPlots.fillControlPlotsAfterElectronSelection(fEvent, eData);
  fCommonPlots.fillControlPlotsAfterMuonSelection(fEvent, muData);
  cLeptons.increment();


  //====== Apply Cut: Tau selection
  const TauSelection::Data tauData = fTauSelection.analyze(fEvent);
  if ( !tauData.hasIdentifiedTaus() ) return; // FIXME: TEMPORARY
  std::cout << "--> REMOVE taudata!" << std::endl;

  //====== Fake tau SF
  // if ( fEvent.isMC() ){ fEventWeight.multiplyWeight(tauData.getTauMisIDSF()); }}
  //====== Tau trigger SF
  // if ( fEvent.isMC() ){ fEventWeight.multiplyWeight(tauData.getTauTriggerSF()); }

  // fCommonPlots.fillControlPlotsAfterTauSelection(fEvent, tauData); // FIXME: TEMPORARY


  //====== MET trigger SF
  // const METSelection::Data silentMETData = fMETSelection.analyze(fEvent, nVertices);
  // if (fEvent.isMC()) {
  // fEventWeight.multiplyWeight(silentMETData.getMETTriggerSF());
  // }


  //====== Apply Cut: Jets selection
  // const JetSelection::Data jetData = fJetSelection.analyze(fEvent, tauData.getSelectedTau());  // FIXME: TEMPORARY
  const JetSelection::Data jetData = fJetSelection.analyzeWithoutTau(fEvent);  // FIXME: TEMPORARY

  if ( !jetData.passedSelection() ) return;
  fCommonPlots.fillControlPlotsAfterJetSelections(fEvent);


  //====== Apply Cut: b-Jets selection
  const BJetSelection::Data bjetData = fBJetSelection.analyze(fEvent, jetData);
  if ( !bjetData.passedSelection() ) return;
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
