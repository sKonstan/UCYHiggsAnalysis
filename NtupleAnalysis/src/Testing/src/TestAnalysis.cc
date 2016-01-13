// -*- c++ -*-
#include "Framework/interface/BaseSelector.h"
#include "Framework/interface/makeTH.h"

#include "DataFormat/interface/Event.h"
#include "EventSelection/interface/CommonPlots.h"
#include "EventSelection/interface/EventSelections.h"

#include "TDirectory.h"

class TestAnalysis: public BaseSelector {
public:
  enum BTagPartonType {
    kBTagB,
    kBTagC,
    kBtagG,
    kBtagLight,
  };
  explicit TestAnalysis(const ParameterSet& config);
  virtual ~TestAnalysis() {}

  /// Books histograms
  virtual void book(TDirectory *dir) override;
  /// Sets up branches for reading the TTree
  virtual void setupBranches(BranchManager& branchManager) override;
  /// Called for each event
  virtual void process(Long64_t entry) override;

private:
  // Input parameters
  const double cfg_fJetPtCutMin;
  const double cfg_fJetPtCutMax;
  const double cfg_fJetEtaCutMin;
  const double cfg_fJetEtaCutMax;

  // Event selection classes and event counters (in same order like they are applied)
  Count cAllEvents;
  Count cTrigger;
  METFilterSelection fMETFilterSelection;
  Count cVertexSelection;
  TauSelection fTauSelection;
  Count cFakeTauSFCounter;
  Count cTauTriggerSFCounter;
  Count cMetTriggerSFCounter;
  ElectronSelection fElectronSelection;
  MuonSelection fMuonSelection;
  JetSelection fJetSelection;
  AngularCutsCollinear fAngularCutsCollinear;
  BJetSelection fBJetSelection;
  METSelection fMETSelection;
  Count cSelected;
    
  // Non-common histograms
  WrappedTH1* hAllBjets;
  WrappedTH1* hAllCjets;
  WrappedTH1* hAllGjets;
  WrappedTH1* hAllLightjets;
  WrappedTH1* hPassedBjets;
  WrappedTH1* hPassedCjets;
  WrappedTH1* hPassedGjets;
  WrappedTH1* hPassedLightjets;
};

#include "Framework/interface/SelectorFactory.h"
REGISTER_SELECTOR(TestAnalysis);

TestAnalysis::TestAnalysis(const ParameterSet& config)
  : BaseSelector(config),
    cfg_fJetPtCutMin(config.getParameter<double>("jetPtCutMin")),
    cfg_fJetPtCutMax(config.getParameter<double>("jetPtCutMax")),
    cfg_fJetEtaCutMin(config.getParameter<double>("jetEtaCutMin")),
    cfg_fJetEtaCutMax(config.getParameter<double>("jetEtaCutMax")),
    cAllEvents(fEventCounter.addCounter("All events")),
    cTrigger(fEventCounter.addCounter("Passed trigger")),
    fMETFilterSelection(config.getParameter<ParameterSet>("METFilter"),
			fEventCounter, fHistoWrapper, nullptr, ""),
    cVertexSelection(fEventCounter.addCounter("Primary vertex selection")),
    fTauSelection(config.getParameter<ParameterSet>("TauSelection"),
		  fEventCounter, fHistoWrapper, nullptr, ""),
    cFakeTauSFCounter(fEventCounter.addCounter("Fake tau SF")),
    cTauTriggerSFCounter(fEventCounter.addCounter("Tau trigger SF")),
    cMetTriggerSFCounter(fEventCounter.addCounter("Met trigger SF")),
    fElectronSelection(config.getParameter<ParameterSet>("ElectronSelection"),
		       fEventCounter, fHistoWrapper, nullptr, "Veto"),
    fMuonSelection(config.getParameter<ParameterSet>("MuonSelection"),
		   fEventCounter, fHistoWrapper, nullptr, "Veto"),
    fJetSelection(config.getParameter<ParameterSet>("JetSelection"),
		  fEventCounter, fHistoWrapper, nullptr, ""),
    fAngularCutsCollinear(config.getParameter<ParameterSet>("AngularCutsCollinear"),
			  fEventCounter, fHistoWrapper, nullptr, ""),
    fBJetSelection(config.getParameter<ParameterSet>("BJetSelection"),
		   fEventCounter, fHistoWrapper, nullptr, ""),
    fMETSelection(config.getParameter<ParameterSet>("METSelection"),
		  fEventCounter, fHistoWrapper, nullptr, ""),
    cSelected(fEventCounter.addCounter("Selected events"))
{ }

void TestAnalysis::book(TDirectory *dir) {
  // std::cout << "=== TestAnalysis.cc:\n\t TestAnalysis::book()" << std::endl;

  // Book histograms in event selection classes
  fTauSelection.bookHistograms(dir);
  fElectronSelection.bookHistograms(dir);
  fMuonSelection.bookHistograms(dir);
  fJetSelection.bookHistograms(dir);
  fAngularCutsCollinear.bookHistograms(dir);
  fBJetSelection.bookHistograms(dir);
  fMETSelection.bookHistograms(dir);

  // Book non-common histograms
  hAllBjets        = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "AllBjets"         , "allBjets:Jet p_{T}, GeV:N_{jets}"         , 50, 0, 500);
  hAllCjets        = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "AllCjets"         , "allCjets:Jet p_{T}, GeV:N_{jets}"         , 50, 0, 500);
  hAllGjets        = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "AllGjets"         , "allGjets:Jet p_{T}, GeV:N_{jets}"         , 50, 0, 500);
  hAllLightjets    = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "AllLightjets"     , "allLightjets:Jet p_{T}, GeV:N_{jets}"     , 50, 0, 500);
  hPassedBjets     = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "SelectedBjets"    , "SelectedBjets:Jet p_{T}, GeV:N_{jets}"    , 50, 0, 500);
  hPassedCjets     = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "SelectedCjets"    , "SelectedCjets:Jet p_{T}, GeV:N_{jets}"    , 50, 0, 500);
  hPassedGjets     = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "SelectedGjets"    , "SelectedGjets:Jet p_{T}, GeV:N_{jets}"    , 50, 0, 500);
  hPassedLightjets = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "SelectedLightjets", "SelectedLightjets:Jet p_{T}, GeV:N_{jets}", 50, 0, 500);

  return;
}


void TestAnalysis::setupBranches(BranchManager& branchManager) {
  // std::cout << "=== TestAnalysis.cc:\n\t TestAnalysis::setupBranches()" << std::endl;
  fEvent.setupBranches(branchManager);

  return;
}


void TestAnalysis::process(Long64_t entry) {
  // std::cout << "=== TestAnalysis.cc:\n\t TestAnalysis::process()" << std::endl;

  //====== Initialize
  cAllEvents.increment();

  //====== Apply trigger
  if ( !(fEvent.passTriggerDecision()) ) return;
  cTrigger.increment();

  //====== MET filters to remove events with spurious sources of fake MET
  const METFilterSelection::Data metFilterData = fMETFilterSelection.analyze(fEvent);
  if ( !metFilterData.passedSelection() ) return;
  
  //====== GenParticle analysis
  // if needed

  //====== Check that primary vertex exists
  int nVertices = fEvent.vertexInfo().value();
  if (nVertices < 1) return;
  cVertexSelection.increment();
  
  //====== Tau selection
  const TauSelection::Data tauData = fTauSelection.analyze(fEvent);
  if ( !tauData.hasIdentifiedTaus() ) return;
  if ( fEvent.isMC() ) {
    fEventWeight.multiplyWeight(tauData.getTauMisIDSF());
    fEventWeight.multiplyWeight(tauData.getTauTriggerSF());
  }
  
  //====== Fake tau SF
  if ( fEvent.isMC() ) {
    fEventWeight.multiplyWeight(tauData.getTauMisIDSF());
    cFakeTauSFCounter.increment();
  }

  //====== Tau trigger SF
  if ( fEvent.isMC() ) {
    fEventWeight.multiplyWeight(tauData.getTauTriggerSF());
    cTauTriggerSFCounter.increment();
  }

  //====== MET trigger SF
  const METSelection::Data silentMETData = fMETSelection.silentAnalyze(fEvent, nVertices);
  if ( fEvent.isMC() ) {
    fEventWeight.multiplyWeight(silentMETData.getMETTriggerSF());
  }
  cMetTriggerSFCounter.increment();

  //====== Electron veto
  const ElectronSelection::Data eData = fElectronSelection.analyze(fEvent);
  if ( eData.hasIdentifiedElectrons() ) return;

  //====== Muon veto
  const MuonSelection::Data muData = fMuonSelection.analyze(fEvent);
  if ( muData.hasIdentifiedMuons() ) return;

  //====== Jet selection
  const JetSelection::Data jetData = fJetSelection.analyze(fEvent, tauData.getSelectedTau());
  if ( !jetData.passedSelection() ) return;
  
  //====== Point of standard selections
  // For-loop: Selected jets
  for (auto& p: jetData.getSelectedJets()) {
    // Filter by jet pt and eta
    if (p.pt()  < cfg_fJetPtCutMin ) continue;
    if (p.pt()  > cfg_fJetPtCutMax ) continue;
    if (p.eta() < cfg_fJetEtaCutMin) continue;
    if (p.eta() > cfg_fJetEtaCutMax) continue;

    // Look for parton flavour
    int id = std::abs(p.pdgId()); // FIXME switch to partonFlavour
    if (id == 5)       hAllBjets->Fill(p.pt());
    else if (id == 4)  hAllCjets->Fill(p.pt());
    else if (id == 21) hAllGjets->Fill(p.pt());
    else if (id == 1 || id == 2 || id == 3) hAllLightjets->Fill(p.pt());

  }//for (auto& p: jetData.getSelectedJets()) {

  const BJetSelection::Data bjetData = fBJetSelection.silentAnalyze(fEvent, jetData);
  // For-loop: Selected b jets
  for (auto& p: bjetData.getSelectedBJets()) {
    // Filter by jet pt and eta
    if (p.pt()  < cfg_fJetPtCutMin ) continue;
    if (p.pt()  > cfg_fJetPtCutMax ) continue;
    if (p.eta() < cfg_fJetEtaCutMin) continue;
    if (p.eta() > cfg_fJetEtaCutMax) continue;

    // Look for parton flavour
    int id = std::abs(p.pdgId()); // FIXME switch to partonFlavour
    if (id == 5)       hPassedBjets->Fill(p.pt());
    else if (id == 4)  hPassedCjets->Fill(p.pt());
    else if (id == 21) hPassedGjets->Fill(p.pt());
    else if (id == 1 || id == 2 || id == 3) hPassedLightjets->Fill(p.pt());

  }// for (auto& p: bjetData.getSelectedBJets()) {

  //====== All cuts passed
  cSelected.increment();

  //====== All Final plots

}
