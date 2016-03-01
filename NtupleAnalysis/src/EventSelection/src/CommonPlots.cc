#include "EventSelection/interface/CommonPlots.h"
#include "EventSelection/interface/TransverseMass.h"
#include "EventSelection/interface/PUDependencyPlots.h"
#include "DataFormat/interface/Event.h"

CommonPlots::CommonPlots(const ParameterSet& config, const AnalysisType type, HistoWrapper& histoWrapper)
: fAnalysisType(type),
  fHistoWrapper(histoWrapper),
  fHistoSplitter(config, histoWrapper),
  fNVerticesBinSettings(config.getParameter<ParameterSet>("nVerticesBins")),
  fPtBinSettings(config.getParameter<ParameterSet>("ptBins")),
  fEtaBinSettings(config.getParameter<ParameterSet>("etaBins")),
  fPhiBinSettings(config.getParameter<ParameterSet>("phiBins")),
  fRtauBinSettings(config.getParameter<ParameterSet>("rtauBins")),
  fNjetsBinSettings(config.getParameter<ParameterSet>("njetsBins")),
  fMetBinSettings(config.getParameter<ParameterSet>("metBins")),
  fBJetDiscriminatorBinSettings(config.getParameter<ParameterSet>("bjetDiscrBins"))
{ 
  // Create CommonPlotsBase objects
  fPUDependencyPlots = new PUDependencyPlots(histoWrapper, config.getParameter<bool>("enablePUDependencyPlots"), fNVerticesBinSettings);
  fBaseObjects.push_back(fPUDependencyPlots);
}


CommonPlots::~CommonPlots() { }


void CommonPlots::book(TDirectory *dir, bool isData) { 
  fHistoSplitter.bookHistograms(dir);

  // Create directories for data driven control plots
  std::string myLabelA = "CommonPlotsA";
  std::string myLabelB = "CommonPlotsB";
  std::string myLabelC = "CommonPlotsC";

  TDirectory* myDirA = fHistoWrapper.mkdir(HistoLevel::kInformative, dir, myLabelA);
  TDirectory* myDirB = fHistoWrapper.mkdir(HistoLevel::kInformative, dir, myLabelB);
  TDirectory* myDirC = fHistoWrapper.mkdir(HistoLevel::kInformative, dir, myLabelC);
  std::vector<TDirectory*> _myDirs = {myDirA, myDirB, myDirC};
  std::vector<TDirectory*> myDirs;
  
  for (auto& p: _myDirs) myDirs.push_back(p);
  
    
  //====== Vertex selection

  //====== Electron selection

  //====== Muon selection

  //====== Tau selection

  //====== Jet selection
  fHistoSplitter.createShapeHistogramTriplet<TH1F>(true, HistoLevel::kVital, myDirs, hCtrlNjets, 
    "Njets", ";Number of selected jets;N_{events}", 
    fNjetsBinSettings.bins(), fNjetsBinSettings.min(), fNjetsBinSettings.max());
  
  
  //====== Standard selections
  fHistoSplitter.createShapeHistogramTriplet<TH1F>(true, HistoLevel::kVital, myDirs, hCtrlNVerticesAfterStdSelections, 
    "NVertices_AfterStandardSelections", ";N_{vertices};N_{events}",
    fNVerticesBinSettings.bins(), fNVerticesBinSettings.min(), fNVerticesBinSettings.max());

  fHistoSplitter.createShapeHistogramTriplet<TH1F>(true, HistoLevel::kVital, myDirs, hCtrlSelectedTauPtAfterStdSelections, 
    "SelectedTau_pT_AfterStandardSelections", ";#tau p_{T}, GeV/c;N_{events}",
    fPtBinSettings.bins(), fPtBinSettings.min(), fPtBinSettings.max());

  fHistoSplitter.createShapeHistogramTriplet<TH1F>(true, HistoLevel::kVital, myDirs, hCtrlSelectedTauEtaAfterStdSelections, 
    "SelectedTau_eta_AfterStandardSelections", ";#tau #eta;N_{events}",
    fEtaBinSettings.bins(), fEtaBinSettings.min(), fEtaBinSettings.max());

  fHistoSplitter.createShapeHistogramTriplet<TH1F>(true, HistoLevel::kVital, myDirs, hCtrlSelectedTauPhiAfterStdSelections, 
    "SelectedTau_phi_AfterStandardSelections", ";#tau #phi;N_{events}",
    fPhiBinSettings.bins(), fPhiBinSettings.min(), fPhiBinSettings.max());

  fHistoSplitter.createShapeHistogramTriplet<TH2F>(true, HistoLevel::kInformative, myDirs, hCtrlSelectedTauEtaPhiAfterStdSelections, 
    "SelectedTau_etaphi_AfterStandardSelections", ";#tau #eta;#tau #phi;",
    fEtaBinSettings.bins(), fEtaBinSettings.min(), fEtaBinSettings.max(),
    fPhiBinSettings.bins(), fPhiBinSettings.min(), fPhiBinSettings.max());

  fHistoSplitter.createShapeHistogramTriplet<TH1F>(true, HistoLevel::kVital, myDirs, hCtrlSelectedTauLdgTrkPtAfterStdSelections, 
    "SelectedTau_ldgTrkPt_AfterStandardSelections", ";#tau ldg. trk p_{T}, GeV/c;N_{events}",
    fPtBinSettings.bins(), fPtBinSettings.min(), fPtBinSettings.max());

  fHistoSplitter.createShapeHistogramTriplet<TH1F>(true, HistoLevel::kVital, myDirs, hCtrlSelectedTauDecayModeAfterStdSelections, 
    "SelectedTau_DecayMode_AfterStandardSelections", ";#tau decay mode;N_{events}",
    20, 0, 20);

  fHistoSplitter.createShapeHistogramTriplet<TH1F>(true, HistoLevel::kVital, myDirs, hCtrlSelectedTauNProngsAfterStdSelections, 
    "SelectedTau_Nprongs_AfterStandardSelections", ";N_{prongs};N_{events}",
    10, 0, 10);

  fHistoSplitter.createShapeHistogramTriplet<TH1F>(true, HistoLevel::kVital, myDirs, hCtrlSelectedTauRtauAfterStdSelections, 
    "SelectedTau_Rtau_AfterStandardSelections", ";R_{#tau};N_{events}",
    fRtauBinSettings.bins(), fRtauBinSettings.min(), fRtauBinSettings.max());

  fHistoSplitter.createShapeHistogramTriplet<TH1F>(true, HistoLevel::kVital, myDirs, hCtrlSelectedTauSourceAfterStdSelections, 
    "SelectedTau_source_AfterStandardSelections", ";;N_{events}",
    fHelper.getTauSourceBinCount(), 0, fHelper.getTauSourceBinCount());

  for (int i = 0; i < fHelper.getTauSourceBinCount(); ++i) 
    {
      fHistoSplitter.SetBinLabel(hCtrlSelectedTauSourceAfterStdSelections, i+1, fHelper.getTauSourceBinLabel(i));
    }
  
  fHistoSplitter.createShapeHistogramTriplet<TH1F>(true, HistoLevel::kVital, myDirs, hCtrlNJetsAfterStdSelections, 
    "Njets_AfterStandardSelections", ";Number of selected jets;N_{events}",
    fNjetsBinSettings.bins(), fNjetsBinSettings.min(), fNjetsBinSettings.max());

  fHistoSplitter.createShapeHistogramTriplet<TH1F>(true, HistoLevel::kVital, myDirs, hCtrlJetPtAfterStdSelections, 
    "JetPt_AfterStandardSelections", ";Selected jets p_{T}, GeV/c;N_{events}",
    fPtBinSettings.bins(), fPtBinSettings.min(), fPtBinSettings.max());

  fHistoSplitter.createShapeHistogramTriplet<TH1F>(true, HistoLevel::kVital, myDirs, hCtrlJetEtaAfterStdSelections, 
    "JetEta_AfterStandardSelections", ";Selected jets #eta;N_{events}",
    fEtaBinSettings.bins(), fEtaBinSettings.min(), fEtaBinSettings.max());

  fHistoSplitter.createShapeHistogramTriplet<TH2F>(true, HistoLevel::kInformative, myDirs, hCtrlJetEtaPhiAfterStdSelections, 
    "JetEtaPhi_AfterStandardSelections", ";Selected jets #eta;Selected jets #phi",
    fEtaBinSettings.bins(), fEtaBinSettings.min(), fEtaBinSettings.max(),
    fPhiBinSettings.bins(), fPhiBinSettings.min(), fPhiBinSettings.max());


  //====== MET
  fHistoSplitter.createShapeHistogramTriplet<TH1F>(true, HistoLevel::kVital, myDirs, hCtrlMET, 
    "MET", ";MET, GeV;N_{events}", fMetBinSettings.bins(), fMetBinSettings.min(), fMetBinSettings.max());

  fHistoSplitter.createShapeHistogramTriplet<TH1F>(true, HistoLevel::kVital, myDirs, hCtrlMETPhi, 
    "METPhi", ";MET #phi;N_{events}", fPhiBinSettings.bins(), fPhiBinSettings.min(), fPhiBinSettings.max());

  
  //====== b tagging
  fHistoSplitter.createShapeHistogramTriplet<TH1F>(true, HistoLevel::kVital, myDirs, hCtrlNBJets, 
    "NBjets", ";Number of selected b jets;N_{events}",
    fNjetsBinSettings.bins(), fNjetsBinSettings.min(), fNjetsBinSettings.max());
  
  fHistoSplitter.createShapeHistogramTriplet<TH1F>(true, HistoLevel::kVital, myDirs, hCtrlBJetPt, 
    "BJetPt", ";Selected b jets p_{T}, GeV/c;N_{events}", fPtBinSettings.bins(), fPtBinSettings.min(), fPtBinSettings.max());

  fHistoSplitter.createShapeHistogramTriplet<TH1F>(true, HistoLevel::kVital, myDirs, hCtrlBJetEta, 
    "BJetEta", ";Selected b jets #eta;N_{events}", fEtaBinSettings.bins(), fEtaBinSettings.min(), fEtaBinSettings.max());

  fHistoSplitter.createShapeHistogramTriplet<TH1F>(true, HistoLevel::kVital, myDirs, hCtrlBDiscriminator, 
    "BtagDiscriminator", ";b tag discriminator;N_{events}",
    fBJetDiscriminatorBinSettings.bins(), fBJetDiscriminatorBinSettings.min(), fBJetDiscriminatorBinSettings.max());
  

  //====== All selections
  fHistoSplitter.createShapeHistogramTriplet<TH1F>(true, HistoLevel::kVital, myDirs, hCtrlNVerticesAfterAllSelections, 
    "NVertices_AfterAllSelections", ";N_{vertices};N_{events}",
    fNVerticesBinSettings.bins(), fNVerticesBinSettings.min(), fNVerticesBinSettings.max());

  fHistoSplitter.createShapeHistogramTriplet<TH1F>(true, HistoLevel::kVital, myDirs, hCtrlSelectedTauPtAfterAllSelections, 
    "SelectedTau_pT_AfterAllSelections", ";#tau p_{T}, GeV/c;N_{events}",
    fPtBinSettings.bins(), fPtBinSettings.min(), fPtBinSettings.max());

  fHistoSplitter.createShapeHistogramTriplet<TH1F>(true, HistoLevel::kVital, myDirs, hCtrlSelectedTauEtaAfterAllSelections, 
    "SelectedTau_eta_AfterAllSelections", ";#tau #eta;N_{events}",
    fEtaBinSettings.bins(), fEtaBinSettings.min(), fEtaBinSettings.max());

  fHistoSplitter.createShapeHistogramTriplet<TH1F>(true, HistoLevel::kVital, myDirs, hCtrlSelectedTauPhiAfterAllSelections, 
    "SelectedTau_phi_AfterAllSelections", ";#tau #phi;N_{events}",
    fPhiBinSettings.bins(), fPhiBinSettings.min(), fPhiBinSettings.max());

  fHistoSplitter.createShapeHistogramTriplet<TH2F>(true, HistoLevel::kInformative, myDirs, hCtrlSelectedTauEtaPhiAfterAllSelections, 
    "SelectedTau_etaphi_AfterAllSelections", ";#tau #eta;#tau #phi;",
    fEtaBinSettings.bins(), fEtaBinSettings.min(), fEtaBinSettings.max(),
    fPhiBinSettings.bins(), fPhiBinSettings.min(), fPhiBinSettings.max());

  fHistoSplitter.createShapeHistogramTriplet<TH1F>(true, HistoLevel::kVital, myDirs, hCtrlSelectedTauLdgTrkPtAfterAllSelections, 
    "SelectedTau_ldgTrkPt_AfterAllSelections", ";#tau ldg. trk p_{T}, GeV/c;N_{events}",
    fPtBinSettings.bins(), fPtBinSettings.min(), fPtBinSettings.max());

  fHistoSplitter.createShapeHistogramTriplet<TH1F>(true, HistoLevel::kVital, myDirs, hCtrlSelectedTauDecayModeAfterAllSelections, 
    "SelectedTau_DecayMode_AfterAllSelections", ";#tau decay mode;N_{events}",
    20, 0, 20);

  fHistoSplitter.createShapeHistogramTriplet<TH1F>(true, HistoLevel::kVital, myDirs, hCtrlSelectedTauNProngsAfterAllSelections, 
    "SelectedTau_Nprongs_AfterAllSelections", ";N_{prongs};N_{events}",
    10, 0, 10);

  fHistoSplitter.createShapeHistogramTriplet<TH1F>(true, HistoLevel::kVital, myDirs, hCtrlSelectedTauRtauAfterAllSelections, 
    "SelectedTau_Rtau_AfterAllSelections", ";R_{#tau};N_{events}",
    fRtauBinSettings.bins(), fRtauBinSettings.min(), fRtauBinSettings.max());

  fHistoSplitter.createShapeHistogramTriplet<TH1F>(true, HistoLevel::kVital, myDirs, hCtrlSelectedTauSourceAfterAllSelections, 
    "SelectedTau_source_AfterAllSelections", ";;N_{events}",
    fHelper.getTauSourceBinCount(), 0, fHelper.getTauSourceBinCount());

  for (int i = 0; i < fHelper.getTauSourceBinCount(); ++i) {
    fHistoSplitter.SetBinLabel(hCtrlSelectedTauSourceAfterAllSelections, i+1, fHelper.getTauSourceBinLabel(i));
  }

  fHistoSplitter.createShapeHistogramTriplet<TH1F>(true, HistoLevel::kVital, myDirs, hCtrlSelectedTauIPxyAfterAllSelections, 
    "SelectedTau_IPxy_AfterAllSelections", ";IP_{T} (cm);N_{events}",
    100, 0, 0.2);

  fHistoSplitter.createShapeHistogramTriplet<TH1F>(true, HistoLevel::kVital, myDirs, hCtrlNJetsAfterAllSelections, 
    "Njets_AfterAllSelections", ";Number of selected jets;N_{events}",
    fNjetsBinSettings.bins(), fNjetsBinSettings.min(), fNjetsBinSettings.max());

  fHistoSplitter.createShapeHistogramTriplet<TH1F>(true, HistoLevel::kVital, myDirs, hCtrlJetPtAfterAllSelections, 
    "JetPt_AfterAllSelections", ";Selected jets p_{T}, GeV/c;N_{events}",
    fPtBinSettings.bins(), fPtBinSettings.min(), fPtBinSettings.max());

  fHistoSplitter.createShapeHistogramTriplet<TH1F>(true, HistoLevel::kVital, myDirs, hCtrlJetEtaAfterAllSelections, 
    "JetEta_AfterAllSelections", ";Selected jets #eta;N_{events}",
    fEtaBinSettings.bins(), fEtaBinSettings.min(), fEtaBinSettings.max());

  fHistoSplitter.createShapeHistogramTriplet<TH2F>(true, HistoLevel::kInformative, myDirs, hCtrlJetEtaPhiAfterAllSelections, 
    "JetEtaPhi_AfterAllSelections", ";Selected jets #eta;Selected jets #phi",
    fEtaBinSettings.bins(), fEtaBinSettings.min(), fEtaBinSettings.max(),
    fPhiBinSettings.bins(), fPhiBinSettings.min(), fPhiBinSettings.max());

  fHistoSplitter.createShapeHistogramTriplet<TH1F>(true, HistoLevel::kVital, myDirs, hCtrlMETAfterAllSelections, 
    "MET_AfterAllSelections", ";MET, GeV;N_{events}", 
    fMetBinSettings.bins(), fMetBinSettings.min(), fMetBinSettings.max());

  fHistoSplitter.createShapeHistogramTriplet<TH1F>(true, HistoLevel::kVital, myDirs, hCtrlMETPhiAfterAllSelections,
    "METPhi_AfterAllSelections", ";MET #phi;N_{events}", 
    fPhiBinSettings.bins(), fPhiBinSettings.min(), fPhiBinSettings.max());

  fHistoSplitter.createShapeHistogramTriplet<TH1F>(true, HistoLevel::kVital, myDirs, hCtrlNBJetsAfterAllSelections,
    "NBjets_AfterAllSelections", ";Number of selected b jets;N_{events}",
    fNjetsBinSettings.bins(), fNjetsBinSettings.min(), fNjetsBinSettings.max());

  fHistoSplitter.createShapeHistogramTriplet<TH1F>(true, HistoLevel::kVital, myDirs, hCtrlBJetPtAfterAllSelections,
    "BJetPt_AfterAllSelections", ";Selected b jets p_{T}, GeV/c;N_{events}",
    fPtBinSettings.bins(), fPtBinSettings.min(), fPtBinSettings.max());

  fHistoSplitter.createShapeHistogramTriplet<TH1F>(true, HistoLevel::kVital, myDirs, hCtrlBJetEtaAfterAllSelections,
    "BJetEta_AfterAllSelections", ";Selected b jets #eta;N_{events}",
    fEtaBinSettings.bins(), fEtaBinSettings.min(), fEtaBinSettings.max());

  fHistoSplitter.createShapeHistogramTriplet<TH1F>(true, HistoLevel::kVital, myDirs, hCtrlBDiscriminatorAfterAllSelections, 
    "BtagDiscriminator_AfterAllSelections", ";b tag discriminator;N_{events}",
    fBJetDiscriminatorBinSettings.bins(), fBJetDiscriminatorBinSettings.min(), fBJetDiscriminatorBinSettings.max());
  
  if (isData) 
    {
      hNSelectedVsRunNumber = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, 
      "NSelectedVsRunNumber", "NSelectedVsRunNumber;Run number;N_{events}", 14000, 246000, 260000);
    }
  
  for (auto& p: fBaseObjects) { p->book(dir, isData); }

  return;
}


void CommonPlots::initialize() {
  iVertices     = -1;
  fTauData      = TauSelection::Data();
  bIsFakeTau    = false;
  fElectronData = ElectronSelection::Data();
  fMuonData     = MuonSelection::Data();
  fJetData      = JetSelection::Data();
  fBJetData     = BJetSelection::Data();
  fMETData      = METSelection::Data();
  fHistoSplitter.initialize();
  
  for (auto& p: fBaseObjects) { p->reset(); }

  return;
}


//================================================================================================  
// Unique filling methods (to be called inside the event selection routine only)
//================================================================================================  
void CommonPlots::fillControlPlotsAtVertexSelection(const Event& event) {
  for (auto& p: fBaseObjects) { p->fillControlPlotsAtVertexSelection(event); } 

  return;
}


void CommonPlots::fillControlPlotsAtElectronSelection(const Event& event, const ElectronSelection::Data& data) {
  fElectronData = data;
  for (auto& p: fBaseObjects) { p->fillControlPlotsAtElectronSelection(event, data); }

  return;
}


void CommonPlots::fillControlPlotsAtMuonSelection(const Event& event, const MuonSelection::Data& data) {
  fMuonData = data;
  for (auto& p: fBaseObjects) { p->fillControlPlotsAtMuonSelection(event, data); }

  return;
}


void CommonPlots::fillControlPlotsAtJetSelection(const Event& event, const JetSelection::Data& data) {
  fJetData = data;
  fHistoSplitter.fillShapeHistogramTriplet(hCtrlNjets, !bIsFakeTau, fJetData.getNumberOfSelectedJets());
  for (auto& p: fBaseObjects) { p->fillControlPlotsAtJetSelection(event, data); }

  return;
}


void CommonPlots::fillControlPlotsAtBtagging(const Event& event, const BJetSelection::Data& data) {
  fBJetData = data;
  fHistoSplitter.fillShapeHistogramTriplet(hCtrlNBJets, !bIsFakeTau, fBJetData.getNumberOfSelectedBJets());

  for (auto& p: fJetData.getSelectedJets()) 
    {
      fHistoSplitter.fillShapeHistogramTriplet(hCtrlBDiscriminator, !bIsFakeTau, p.bjetDiscriminator());
    }

  for (auto& p: fBJetData.getSelectedBJets()) 
    {
      fHistoSplitter.fillShapeHistogramTriplet(hCtrlBJetPt, !bIsFakeTau, p.pt());
      fHistoSplitter.fillShapeHistogramTriplet(hCtrlBJetEta, !bIsFakeTau, p.eta());
    }
  for (auto& p: fBaseObjects) { p->fillControlPlotsAtBtagging(event, data); }
  
  return;
}


void CommonPlots::fillControlPlotsAtMETSelection(const Event& event, const METSelection::Data& data) {
  fMETData = data;
  fHistoSplitter.fillShapeHistogramTriplet(hCtrlMET, !bIsFakeTau, fMETData.getMET().R());
  fHistoSplitter.fillShapeHistogramTriplet(hCtrlMETPhi, !bIsFakeTau, fMETData.getMET().phi());
  for (auto& p: fBaseObjects) { p->fillControlPlotsAtMETSelection(event, data); }

  return;
}


//================================================================================================  
// Unique filling methods (to be called AFTER return statement from analysis routine)
//================================================================================================  
void CommonPlots::fillControlPlotsAfterTrigger(const Event& event) {
  for (auto& p: fBaseObjects) { p->fillControlPlotsAfterTrigger(event); } 

  return;
}


void CommonPlots::fillControlPlotsAfterTauSelection(const Event& event, const TauSelection::Data& data) {
  // Code logic: if there is no identified tau (or anti-isolated tau for QCD), the code will for sure crash later
  // This piece of code is called from TauSelection, so there one cannot judge if things go right or not, 
  // that kind of check needs to be done in the analysis code (i.e. cut away event if tau selection is not passed)
  for (auto& p: fBaseObjects) { p->fillControlPlotsAfterTauSelection(event, data); }
  fTauData = data;

  if (event.isData()) 
    {
      bIsFakeTau = false;
      return;
    }

  if (isQCDMeasurement()) {
    if (data.hasAntiIsolatedTaus()) {
      bIsFakeTau = !(data.getAntiIsolatedTauIsGenuineTau());
    }
  } else {
    if (data.hasIdentifiedTaus()) {
      bIsFakeTau = !(data.isGenuineTau());
    }
  }
  
  return;
}


void CommonPlots::fillControlPlotsAfterJetSelections(const Event& event) {
  fHistoSplitter.fillShapeHistogramTriplet(hCtrlNVerticesAfterStdSelections, !bIsFakeTau, iVertices);

  if (isQCDMeasurement()) {
    fHistoSplitter.fillShapeHistogramTriplet(hCtrlSelectedTauPtAfterStdSelections, !bIsFakeTau, fTauData.getAntiIsolatedTau().pt());
    fHistoSplitter.fillShapeHistogramTriplet(hCtrlSelectedTauEtaAfterStdSelections, !bIsFakeTau, fTauData.getAntiIsolatedTau().eta());
    fHistoSplitter.fillShapeHistogramTriplet(hCtrlSelectedTauPhiAfterStdSelections, !bIsFakeTau, fTauData.getAntiIsolatedTau().phi());
    fHistoSplitter.fillShapeHistogramTriplet(hCtrlSelectedTauEtaPhiAfterStdSelections, !bIsFakeTau, fTauData.getAntiIsolatedTau().eta(), fTauData.getAntiIsolatedTau().phi());
    fHistoSplitter.fillShapeHistogramTriplet(hCtrlSelectedTauLdgTrkPtAfterStdSelections, !bIsFakeTau, fTauData.getAntiIsolatedTau().lChTrkPt());
    fHistoSplitter.fillShapeHistogramTriplet(hCtrlSelectedTauDecayModeAfterStdSelections, !bIsFakeTau, fTauData.getAntiIsolatedTau().decayMode());
    fHistoSplitter.fillShapeHistogramTriplet(hCtrlSelectedTauNProngsAfterStdSelections, !bIsFakeTau, fTauData.getAntiIsolatedTau().nProngs());
    fHistoSplitter.fillShapeHistogramTriplet(hCtrlSelectedTauRtauAfterStdSelections, !bIsFakeTau, fTauData.getRtauOfAntiIsolatedTau());
    for (auto& p: fHelper.getTauSourceData(!event.isMC(), fTauData.getAntiIsolatedTau())) {
      fHistoSplitter.fillShapeHistogramTriplet(hCtrlSelectedTauSourceAfterStdSelections, !bIsFakeTau, p);
    }
  } else {
    fHistoSplitter.fillShapeHistogramTriplet(hCtrlSelectedTauPtAfterStdSelections, !bIsFakeTau, fTauData.getSelectedTau().pt());
    fHistoSplitter.fillShapeHistogramTriplet(hCtrlSelectedTauEtaAfterStdSelections, !bIsFakeTau, fTauData.getSelectedTau().eta());
    fHistoSplitter.fillShapeHistogramTriplet(hCtrlSelectedTauPhiAfterStdSelections, !bIsFakeTau, fTauData.getSelectedTau().phi());
    fHistoSplitter.fillShapeHistogramTriplet(hCtrlSelectedTauEtaPhiAfterStdSelections, !bIsFakeTau, fTauData.getSelectedTau().eta(), fTauData.getSelectedTau().phi());
    fHistoSplitter.fillShapeHistogramTriplet(hCtrlSelectedTauLdgTrkPtAfterStdSelections, !bIsFakeTau, fTauData.getSelectedTau().lChTrkPt());
    fHistoSplitter.fillShapeHistogramTriplet(hCtrlSelectedTauDecayModeAfterStdSelections, !bIsFakeTau, fTauData.getSelectedTau().decayMode());
    fHistoSplitter.fillShapeHistogramTriplet(hCtrlSelectedTauNProngsAfterStdSelections, !bIsFakeTau, fTauData.getSelectedTau().nProngs());
    fHistoSplitter.fillShapeHistogramTriplet(hCtrlSelectedTauRtauAfterStdSelections, !bIsFakeTau, fTauData.getRtauOfSelectedTau());
    for (auto& p: fHelper.getTauSourceData(!event.isMC(), fTauData.getSelectedTau())) {
      fHistoSplitter.fillShapeHistogramTriplet(hCtrlSelectedTauSourceAfterStdSelections, !bIsFakeTau, p);
    }
  }
  fHistoSplitter.fillShapeHistogramTriplet(hCtrlNJetsAfterStdSelections, !bIsFakeTau, fJetData.getNumberOfSelectedJets());

  for (auto& p: fJetData.getSelectedJets()) 
    {
      fHistoSplitter.fillShapeHistogramTriplet(hCtrlJetPtAfterStdSelections, !bIsFakeTau, p.pt());
      fHistoSplitter.fillShapeHistogramTriplet(hCtrlJetEtaAfterStdSelections, !bIsFakeTau, p.eta());
      fHistoSplitter.fillShapeHistogramTriplet(hCtrlJetEtaPhiAfterStdSelections, !bIsFakeTau, p.eta(), p.phi());
    }

  return;
}


void CommonPlots::fillControlPlotsAfterAllSelections(const Event& event) {
  fHistoSplitter.fillShapeHistogramTriplet(hCtrlNVerticesAfterAllSelections, !bIsFakeTau, iVertices);

  if (isQCDMeasurement()) {
    fHistoSplitter.fillShapeHistogramTriplet(hCtrlSelectedTauPtAfterAllSelections, !bIsFakeTau, fTauData.getAntiIsolatedTau().pt());
    fHistoSplitter.fillShapeHistogramTriplet(hCtrlSelectedTauEtaAfterAllSelections, !bIsFakeTau, fTauData.getAntiIsolatedTau().eta());
    fHistoSplitter.fillShapeHistogramTriplet(hCtrlSelectedTauPhiAfterAllSelections, !bIsFakeTau, fTauData.getAntiIsolatedTau().phi());
    fHistoSplitter.fillShapeHistogramTriplet(hCtrlSelectedTauEtaPhiAfterAllSelections, !bIsFakeTau, fTauData.getAntiIsolatedTau().eta(), fTauData.getAntiIsolatedTau().phi());
    fHistoSplitter.fillShapeHistogramTriplet(hCtrlSelectedTauLdgTrkPtAfterAllSelections, !bIsFakeTau, fTauData.getAntiIsolatedTau().lChTrkPt());
    fHistoSplitter.fillShapeHistogramTriplet(hCtrlSelectedTauDecayModeAfterAllSelections, !bIsFakeTau, fTauData.getAntiIsolatedTau().decayMode());
    fHistoSplitter.fillShapeHistogramTriplet(hCtrlSelectedTauNProngsAfterAllSelections, !bIsFakeTau, fTauData.getAntiIsolatedTau().nProngs());
    fHistoSplitter.fillShapeHistogramTriplet(hCtrlSelectedTauRtauAfterAllSelections, !bIsFakeTau, fTauData.getRtauOfAntiIsolatedTau());
    for (auto& p: fHelper.getTauSourceData(!event.isMC(), fTauData.getAntiIsolatedTau())) {
      fHistoSplitter.fillShapeHistogramTriplet(hCtrlSelectedTauSourceAfterAllSelections, !bIsFakeTau, p);
    }
    fHistoSplitter.fillShapeHistogramTriplet(hCtrlSelectedTauIPxyAfterAllSelections, !bIsFakeTau, fTauData.getAntiIsolatedTau().IPxy());
  } else {
    fHistoSplitter.fillShapeHistogramTriplet(hCtrlSelectedTauPtAfterAllSelections, !bIsFakeTau, fTauData.getSelectedTau().pt());
    fHistoSplitter.fillShapeHistogramTriplet(hCtrlSelectedTauEtaAfterAllSelections, !bIsFakeTau, fTauData.getSelectedTau().eta());
    fHistoSplitter.fillShapeHistogramTriplet(hCtrlSelectedTauPhiAfterAllSelections, !bIsFakeTau, fTauData.getSelectedTau().phi());
    fHistoSplitter.fillShapeHistogramTriplet(hCtrlSelectedTauEtaPhiAfterAllSelections, !bIsFakeTau, fTauData.getSelectedTau().eta(), fTauData.getSelectedTau().phi());
    fHistoSplitter.fillShapeHistogramTriplet(hCtrlSelectedTauLdgTrkPtAfterAllSelections, !bIsFakeTau, fTauData.getSelectedTau().lChTrkPt());
    fHistoSplitter.fillShapeHistogramTriplet(hCtrlSelectedTauDecayModeAfterAllSelections, !bIsFakeTau, fTauData.getSelectedTau().decayMode());
    fHistoSplitter.fillShapeHistogramTriplet(hCtrlSelectedTauNProngsAfterAllSelections, !bIsFakeTau, fTauData.getSelectedTau().nProngs());
    fHistoSplitter.fillShapeHistogramTriplet(hCtrlSelectedTauRtauAfterAllSelections, !bIsFakeTau, fTauData.getRtauOfSelectedTau());
    for (auto& p: fHelper.getTauSourceData(!event.isMC(), fTauData.getSelectedTau())) {
      fHistoSplitter.fillShapeHistogramTriplet(hCtrlSelectedTauSourceAfterAllSelections, !bIsFakeTau, p);
    }
    fHistoSplitter.fillShapeHistogramTriplet(hCtrlSelectedTauIPxyAfterAllSelections, !bIsFakeTau, fTauData.getSelectedTau().IPxy());
  }
  fHistoSplitter.fillShapeHistogramTriplet(hCtrlNJetsAfterAllSelections, !bIsFakeTau, fJetData.getNumberOfSelectedJets());
  for (auto& p: fJetData.getSelectedJets()) 
    {
      fHistoSplitter.fillShapeHistogramTriplet(hCtrlJetPtAfterAllSelections, !bIsFakeTau, p.pt());
      fHistoSplitter.fillShapeHistogramTriplet(hCtrlJetEtaAfterAllSelections, !bIsFakeTau, p.eta());
      fHistoSplitter.fillShapeHistogramTriplet(hCtrlJetEtaPhiAfterAllSelections, !bIsFakeTau, p.eta(), p.phi());
    }

  fHistoSplitter.fillShapeHistogramTriplet(hCtrlMETAfterAllSelections, !bIsFakeTau, fMETData.getMET().R());
  fHistoSplitter.fillShapeHistogramTriplet(hCtrlMETPhiAfterAllSelections, !bIsFakeTau, fMETData.getMET().phi());
  
  fHistoSplitter.fillShapeHistogramTriplet(hCtrlNBJetsAfterAllSelections, !bIsFakeTau, fBJetData.getNumberOfSelectedBJets());
  for (auto& p: fBJetData.getSelectedBJets()) 
    {
      fHistoSplitter.fillShapeHistogramTriplet(hCtrlBJetPtAfterAllSelections, !bIsFakeTau, p.pt());
      fHistoSplitter.fillShapeHistogramTriplet(hCtrlBJetEtaAfterAllSelections, !bIsFakeTau, p.eta());
      fHistoSplitter.fillShapeHistogramTriplet(hCtrlBDiscriminatorAfterAllSelections, !bIsFakeTau, p.bjetDiscriminator());
    }
    
  if (event.isData()) {
    hNSelectedVsRunNumber->Fill(event.eventID().run());
  }
  for (auto& p: fBaseObjects) {
    p->fillControlPlotsAfterAllSelections(event);
  }

  return;
}
