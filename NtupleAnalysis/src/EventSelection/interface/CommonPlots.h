// -*- c++ -*-
#ifndef EventSelection_CommonPlots_h
#define EventSelection_CommonPlots_h

#include "EventSelection/interface/EventSelections.h"
#include "EventSelection/interface/CommonPlotsHelper.h"
#include "EventSelection/interface/CommonPlotsBase.h"
#include "EventSelection/interface/PUDependencyPlots.h"
#include "Framework/interface/ParameterSet.h"
#include "Framework/interface/HistogramSettings.h"
#include "Framework/interface/HistoSplitter.h"
#include "Framework/interface/HistoWrapper.h"

#include "TDirectory.h"

#include <vector>

class CommonPlots {
public:
  enum AnalysisType {
    kSignalAnalysis = 0,
    kEmbedding,
    kQCDMeasurement,
  };

  CommonPlots(const ParameterSet& config, const CommonPlots::AnalysisType type, HistoWrapper& histoWrapper);
  ~CommonPlots();
  
  void book(TDirectory* dir, bool isData);
  
  /// Initialize (call this at the beginning of each event; prevents double-counting of events)
  void initialize();

  /// Sets factorisation bin (call this for each event before filling the first histogram!)
  void setFactorisationBinForEvent(const std::vector<float>& values=std::vector<float>{}) { fHistoSplitter.setFactorisationBinForEvent(values); }
  
  /// Return the histogram splitter objects
  HistoSplitter& getHistoSplitter() { return fHistoSplitter; }
  const HistogramSettings& getPtBinSettings() const { return fPtBinSettings; }
  
  //===== unique filling methods (to be called inside the event selection routine only, i.e. (before a passing decision is done))
  void fillControlPlotsAtVertexSelection(const Event& event);
  void fillControlPlotsAtElectronSelection(const Event& event, const ElectronSelection::Data& data);
  void fillControlPlotsAtMuonSelection(const Event& event, const MuonSelection::Data& data);
  void fillControlPlotsAtJetSelection(const Event& event, const JetSelection::Data& data);
  void fillControlPlotsAtMETSelection(const Event& event, const METSelection::Data& data);
  void fillControlPlotsAtBtagging(const Event& event, const BJetSelection::Data& data);
  
  //===== unique filling methods (to be called AFTER return statement from analysis routine)
  void setNvertices(int vtx) { iVertices = vtx; fPUDependencyPlots->setNvtx(vtx); }
  void fillControlPlotsAfterTrigger(const Event& event);
  void fillControlPlotsAfterElectronSelection(const Event& event, const ElectronSelection::Data& data);
  void fillControlPlotsAfterMuonSelection(const Event& event, const ElectronSelection::Data& data);
  void fillControlPlotsAfterTauSelection(const Event& event, const TauSelection::Data& data);
  void fillControlPlotsAfterJetSelections(const Event& event);
  void fillControlPlotsAfterAllSelections(const Event& event);

  /// Getter for all vertices
  int nVertices() const { return iVertices; }

private:
  /// Returns true if common plots is created by QCD measurement
  const bool isQCDMeasurement() const { return fAnalysisType == kQCDMeasurement; }
  
private:
  ///===== Analysis type
  const AnalysisType fAnalysisType;

  ///===== HistoWrapper;
  HistoWrapper fHistoWrapper;
  
  ///===== Histogram splitter
  HistoSplitter fHistoSplitter;

  ///===== Settings for histogram binning
  const HistogramSettings fNVerticesBinSettings;
  const HistogramSettings fPtBinSettings;
  const HistogramSettings fEtaBinSettings;
  const HistogramSettings fPhiBinSettings;
  const HistogramSettings fRtauBinSettings;
  const HistogramSettings fNjetsBinSettings;
  const HistogramSettings fMetBinSettings;
  const HistogramSettings fBJetDiscriminatorBinSettings;

  ///===== Histograms
  // NOTE: think before adding a histogram - they do slow down the analysis a lot
  // NOTE: the histograms with the prefix hCtrl are used as data driven control plots
  // NOTE: the histograms with the prefix hShape are used as shape histograms
  // NOTE: histogram triplets contain the inclusive and events with fake tau histograms
  
  // vertex

  // tau selection

  // tau trigger SF

  // veto tau selection
  
  // electron veto
  
  // muon veto
 
  // jet selection
  HistoSplitter::SplittedTripletTH1s hCtrlNjets;
  
  // MET trigger SF
  HistoSplitter::SplittedTripletTH1s hCtrlNjetsAfterJetSelectionAndMETSF;
  
  // this is the point of "standard selections"
  HistoSplitter::SplittedTripletTH1s hCtrlNVerticesAfterStdSelections;
  
  HistoSplitter::SplittedTripletTH1s hCtrlSelectedTauPtAfterStdSelections;
  HistoSplitter::SplittedTripletTH1s hCtrlSelectedTauEtaAfterStdSelections;
  HistoSplitter::SplittedTripletTH1s hCtrlSelectedTauPhiAfterStdSelections;
  HistoSplitter::SplittedTripletTH2s hCtrlSelectedTauEtaPhiAfterStdSelections;
  HistoSplitter::SplittedTripletTH1s hCtrlSelectedTauLdgTrkPtAfterStdSelections;
  HistoSplitter::SplittedTripletTH1s hCtrlSelectedTauDecayModeAfterStdSelections;
  HistoSplitter::SplittedTripletTH1s hCtrlSelectedTauNProngsAfterStdSelections;
  HistoSplitter::SplittedTripletTH1s hCtrlSelectedTauRtauAfterStdSelections;
  HistoSplitter::SplittedTripletTH1s hCtrlSelectedTauSourceAfterStdSelections;
  
  HistoSplitter::SplittedTripletTH1s hCtrlNJetsAfterStdSelections;
  HistoSplitter::SplittedTripletTH1s hCtrlJetPtAfterStdSelections;
  HistoSplitter::SplittedTripletTH1s hCtrlJetEtaAfterStdSelections;
  HistoSplitter::SplittedTripletTH2s hCtrlJetEtaPhiAfterStdSelections;
  
  // MET
  HistoSplitter::SplittedTripletTH1s hCtrlMET;
  HistoSplitter::SplittedTripletTH1s hCtrlMETPhi;
  
  // b tagging
  HistoSplitter::SplittedTripletTH1s hCtrlNBJets;
  HistoSplitter::SplittedTripletTH1s hCtrlBJetPt;
  HistoSplitter::SplittedTripletTH1s hCtrlBJetEta;
  HistoSplitter::SplittedTripletTH1s hCtrlBDiscriminator;
  
  // control plots after all selections
  HistoSplitter::SplittedTripletTH1s hCtrlNVerticesAfterAllSelections;
  
  HistoSplitter::SplittedTripletTH1s hCtrlSelectedTauPtAfterAllSelections;
  HistoSplitter::SplittedTripletTH1s hCtrlSelectedTauEtaAfterAllSelections;
  HistoSplitter::SplittedTripletTH1s hCtrlSelectedTauPhiAfterAllSelections;
  HistoSplitter::SplittedTripletTH2s hCtrlSelectedTauEtaPhiAfterAllSelections;
  HistoSplitter::SplittedTripletTH1s hCtrlSelectedTauLdgTrkPtAfterAllSelections;
  HistoSplitter::SplittedTripletTH1s hCtrlSelectedTauDecayModeAfterAllSelections;
  HistoSplitter::SplittedTripletTH1s hCtrlSelectedTauNProngsAfterAllSelections;
  HistoSplitter::SplittedTripletTH1s hCtrlSelectedTauRtauAfterAllSelections;
  HistoSplitter::SplittedTripletTH1s hCtrlSelectedTauSourceAfterAllSelections;
  HistoSplitter::SplittedTripletTH1s hCtrlSelectedTauIPxyAfterAllSelections;

  HistoSplitter::SplittedTripletTH1s hCtrlNJetsAfterAllSelections;
  HistoSplitter::SplittedTripletTH1s hCtrlJetPtAfterAllSelections;
  HistoSplitter::SplittedTripletTH1s hCtrlJetEtaAfterAllSelections;
  HistoSplitter::SplittedTripletTH2s hCtrlJetEtaPhiAfterAllSelections;

  HistoSplitter::SplittedTripletTH1s hCtrlMETAfterAllSelections;
  HistoSplitter::SplittedTripletTH1s hCtrlMETPhiAfterAllSelections;
  
  HistoSplitter::SplittedTripletTH1s hCtrlNBJetsAfterAllSelections;
  HistoSplitter::SplittedTripletTH1s hCtrlBJetPtAfterAllSelections;
  HistoSplitter::SplittedTripletTH1s hCtrlBJetEtaAfterAllSelections;
  HistoSplitter::SplittedTripletTH1s hCtrlBDiscriminatorAfterAllSelections;
  

  // Other plots
  WrappedTH1* hNSelectedVsRunNumber; // For data only
  
  //====== Plots from base class
  std::vector<CommonPlotsBase*> fBaseObjects;
  PUDependencyPlots* fPUDependencyPlots;
  
  //====== Data cache: Cached data objects from silent analyze
  // VertexSelection::Data fVertexData;
  int iVertices;
  TauSelection::Data fTauData;
  bool bIsFakeTau; // FIXME: a boolean used at the moment
  ElectronSelection::Data fElectronData;
  MuonSelection::Data fMuonData;
  JetSelection::Data fJetData;
  BJetSelection::Data fBJetData;
  METSelection::Data fMETData;

  /// Helper
  CommonPlotsHelper fHelper;
};

#endif
