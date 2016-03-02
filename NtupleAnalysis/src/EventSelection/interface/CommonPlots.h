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
  const HistogramSettings& getPtBinSettings() const { return cfg_PtBinSettings; }
  
  //===== unique filling methods (to be called inside the event selection routine only, i.e. (before a passing decision is done))
  // [Called inside the object selection class. e.g. called inside MuonSelection.cc]
  void fillControlPlotsAtVertexSelection(const Event& event);
  void fillControlPlotsAtElectronSelection(const Event& event, const ElectronSelection::Data& data);
  void fillControlPlotsAtMuonSelection(const Event& event, const MuonSelection::Data& data);
  void fillControlPlotsAtTauSelection(const Event& event, const TauSelection::Data& data);
  void fillControlPlotsAtJetSelection(const Event& event, const JetSelection::Data& data);
  void fillControlPlotsAtMETSelection(const Event& event, const METSelection::Data& data);
  void fillControlPlotsAtBtagging(const Event& event, const BJetSelection::Data& data);
  
  //===== unique filling methods (to be called AFTER return statement from analysis routine)
  // [Called inside the generic selection class. e.g. called inside SignalAnalysis.cc]
  void setNvertices(int vtx) { iVertices = vtx; fPUDependencyPlots->setNvtx(vtx); }
  void fillControlPlotsAfterTrigger(const Event& event);
  void fillControlPlotsAfterElectronSelection(const Event& event, const ElectronSelection::Data& data);
  void fillControlPlotsAfterMuonSelection(const Event& event, const MuonSelection::Data& data);
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
  const HistogramSettings cfg_NVerticesBinSettings;
  const HistogramSettings cfg_PtBinSettings;
  const HistogramSettings cfg_EtaBinSettings;
  const HistogramSettings cfg_PhiBinSettings;
  const HistogramSettings cfg_RtauBinSettings;
  const HistogramSettings cfg_NJetsBinSettings;
  const HistogramSettings cfg_MetBinSettings;
  const HistogramSettings cfg_BJetDiscriminatorBinSettings;

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
  //
  HistoSplitter::SplittedTripletTH1s hCtrlNVerticesAfterJetSelections;
  HistoSplitter::SplittedTripletTH1s hCtrlSelectedTauPtAfterJetSelections;
  HistoSplitter::SplittedTripletTH1s hCtrlSelectedTauEtaAfterJetSelections;
  HistoSplitter::SplittedTripletTH1s hCtrlSelectedTauPhiAfterJetSelections;
  HistoSplitter::SplittedTripletTH2s hCtrlSelectedTauEtaPhiAfterJetSelections;
  HistoSplitter::SplittedTripletTH1s hCtrlSelectedTauLdgTrkPtAfterJetSelections;
  HistoSplitter::SplittedTripletTH1s hCtrlSelectedTauDecayModeAfterJetSelections;
  HistoSplitter::SplittedTripletTH1s hCtrlSelectedTauNProngsAfterJetSelections;
  HistoSplitter::SplittedTripletTH1s hCtrlSelectedTauRtauAfterJetSelections;
  HistoSplitter::SplittedTripletTH1s hCtrlSelectedTauSourceAfterJetSelections;
  HistoSplitter::SplittedTripletTH1s hCtrlNJetsAfterJetSelections;
  HistoSplitter::SplittedTripletTH1s hCtrlJetPtAfterJetSelections;
  HistoSplitter::SplittedTripletTH1s hCtrlJetEtaAfterJetSelections;
  HistoSplitter::SplittedTripletTH2s hCtrlJetEtaPhiAfterJetSelections;
  
  // MET trigger SF
  HistoSplitter::SplittedTripletTH1s hCtrlNjetsAfterJetSelectionAndMETSF;
  
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
