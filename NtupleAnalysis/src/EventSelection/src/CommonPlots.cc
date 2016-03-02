#include "EventSelection/interface/CommonPlots.h"
#include "EventSelection/interface/TransverseMass.h"
#include "EventSelection/interface/PUDependencyPlots.h"
#include "DataFormat/interface/Event.h"

CommonPlots::CommonPlots(const ParameterSet& config, const AnalysisType type, HistoWrapper& histoWrapper)
: fAnalysisType(type),
  fHistoWrapper(histoWrapper),
  fHistoSplitter(config, histoWrapper),
  cfg_NVerticesBinSettings(config.getParameter<ParameterSet>("NVerticesBins")),
  cfg_PtBinSettings(config.getParameter<ParameterSet>("PtBins")),
  cfg_EtaBinSettings(config.getParameter<ParameterSet>("EtaBins")),
  cfg_PhiBinSettings(config.getParameter<ParameterSet>("PhiBins")),
  cfg_RtauBinSettings(config.getParameter<ParameterSet>("RtauBins")),
  cfg_NJetsBinSettings(config.getParameter<ParameterSet>("NJetsBins")),
  cfg_MetBinSettings(config.getParameter<ParameterSet>("MetBins")),
  cfg_BJetDiscriminatorBinSettings(config.getParameter<ParameterSet>("BjetDiscrBins"))
{ 
  // Create CommonPlotsBase objects
  fPUDependencyPlots = new PUDependencyPlots(histoWrapper, config.getParameter<bool>("enablePUDependencyPlots"), cfg_NVerticesBinSettings);
  fBaseObjects.push_back(fPUDependencyPlots);
}


CommonPlots::~CommonPlots() { }


void CommonPlots::book(TDirectory *dir, bool isData) { 
  fHistoSplitter.bookHistograms(dir);

  // Create directories for data driven control plots
  std::string myLabelA = "CommonPlots";
  std::string myLabelB = "CommonPlots_FakeTaus";
  std::string myLabelC = "CommonPlots_EWKGenuineTaus";

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

  //====== At Jet selection
  fHistoSplitter.createShapeHistogramTriplet<TH1F>(true, HistoLevel::kVital, myDirs, hCtrlNjets, 
    "Njets_AtJetSelection", ";Number of selected jets;N_{events}", 
    cfg_NJetsBinSettings.bins(), cfg_NJetsBinSettings.min(), cfg_NJetsBinSettings.max());

  //====== After Jet selection   
  fHistoSplitter.createShapeHistogramTriplet<TH1F>(true, HistoLevel::kVital, myDirs, hCtrlNVerticesAfterJetSelections, 
    "NVertices_AfterJetSelections", ";N_{vertices};N_{events}",
    cfg_NVerticesBinSettings.bins(), cfg_NVerticesBinSettings.min(), cfg_NVerticesBinSettings.max());

  fHistoSplitter.createShapeHistogramTriplet<TH1F>(true, HistoLevel::kVital, myDirs, hCtrlSelectedTauPtAfterJetSelections, 
    "SelectedTau_pT_AfterJetSelections", ";#tau p_{T}, GeV/c;N_{events}",
    cfg_PtBinSettings.bins(), cfg_PtBinSettings.min(), cfg_PtBinSettings.max());

  fHistoSplitter.createShapeHistogramTriplet<TH1F>(true, HistoLevel::kVital, myDirs, hCtrlSelectedTauEtaAfterJetSelections, 
    "SelectedTau_eta_AfterJetSelections", ";#tau #eta;N_{events}",
    cfg_EtaBinSettings.bins(), cfg_EtaBinSettings.min(), cfg_EtaBinSettings.max());

  fHistoSplitter.createShapeHistogramTriplet<TH1F>(true, HistoLevel::kVital, myDirs, hCtrlSelectedTauPhiAfterJetSelections, 
    "SelectedTau_phi_AfterJetSelections", ";#tau #phi;N_{events}",
    cfg_PhiBinSettings.bins(), cfg_PhiBinSettings.min(), cfg_PhiBinSettings.max());

  fHistoSplitter.createShapeHistogramTriplet<TH2F>(true, HistoLevel::kInformative, myDirs, hCtrlSelectedTauEtaPhiAfterJetSelections, 
    "SelectedTau_etaphi_AfterJetSelections", ";#tau #eta;#tau #phi;",
    cfg_EtaBinSettings.bins(), cfg_EtaBinSettings.min(), cfg_EtaBinSettings.max(),
    cfg_PhiBinSettings.bins(), cfg_PhiBinSettings.min(), cfg_PhiBinSettings.max());

  fHistoSplitter.createShapeHistogramTriplet<TH1F>(true, HistoLevel::kVital, myDirs, hCtrlSelectedTauLdgTrkPtAfterJetSelections, 
    "SelectedTau_ldgTrkPt_AfterJetSelections", ";#tau ldg. trk p_{T}, GeV/c;N_{events}",
    cfg_PtBinSettings.bins(), cfg_PtBinSettings.min(), cfg_PtBinSettings.max());

  fHistoSplitter.createShapeHistogramTriplet<TH1F>(true, HistoLevel::kVital, myDirs, hCtrlSelectedTauDecayModeAfterJetSelections, 
    "SelectedTau_DecayMode_AfterJetSelections", ";#tau decay mode;N_{events}",
    20, 0, 20);

  fHistoSplitter.createShapeHistogramTriplet<TH1F>(true, HistoLevel::kVital, myDirs, hCtrlSelectedTauNProngsAfterJetSelections, 
    "SelectedTau_Nprongs_AfterJetSelections", ";N_{prongs};N_{events}",
    10, 0, 10);

  fHistoSplitter.createShapeHistogramTriplet<TH1F>(true, HistoLevel::kVital, myDirs, hCtrlSelectedTauRtauAfterJetSelections, 
    "SelectedTau_Rtau_AfterJetSelections", ";R_{#tau};N_{events}",
    cfg_RtauBinSettings.bins(), cfg_RtauBinSettings.min(), cfg_RtauBinSettings.max());

  fHistoSplitter.createShapeHistogramTriplet<TH1F>(true, HistoLevel::kVital, myDirs, hCtrlSelectedTauSourceAfterJetSelections, 
    "SelectedTau_source_AfterJetSelections", ";;N_{events}",
    fHelper.getTauSourceBinCount(), 0, fHelper.getTauSourceBinCount());

  for (int i = 0; i < fHelper.getTauSourceBinCount(); ++i) 
    {
      fHistoSplitter.SetBinLabel(hCtrlSelectedTauSourceAfterJetSelections, i+1, fHelper.getTauSourceBinLabel(i));
    }
  
  fHistoSplitter.createShapeHistogramTriplet<TH1F>(true, HistoLevel::kVital, myDirs, hCtrlNJetsAfterJetSelections, 
    "Njets_AfterJetSelections", ";Number of selected jets;N_{events}",
    cfg_NJetsBinSettings.bins(), cfg_NJetsBinSettings.min(), cfg_NJetsBinSettings.max());

  fHistoSplitter.createShapeHistogramTriplet<TH1F>(true, HistoLevel::kVital, myDirs, hCtrlJetPtAfterJetSelections, 
    "JetPt_AfterJetSelections", ";Selected jets p_{T}, GeV/c;N_{events}",
    cfg_PtBinSettings.bins(), cfg_PtBinSettings.min(), cfg_PtBinSettings.max());

  fHistoSplitter.createShapeHistogramTriplet<TH1F>(true, HistoLevel::kVital, myDirs, hCtrlJetEtaAfterJetSelections, 
    "JetEta_AfterJetSelections", ";Selected jets #eta;N_{events}",
    cfg_EtaBinSettings.bins(), cfg_EtaBinSettings.min(), cfg_EtaBinSettings.max());

  fHistoSplitter.createShapeHistogramTriplet<TH2F>(true, HistoLevel::kInformative, myDirs, hCtrlJetEtaPhiAfterJetSelections, 
    "JetEtaPhi_AfterJetSelections", ";Selected jets #eta;Selected jets #phi",
    cfg_EtaBinSettings.bins(), cfg_EtaBinSettings.min(), cfg_EtaBinSettings.max(),
    cfg_PhiBinSettings.bins(), cfg_PhiBinSettings.min(), cfg_PhiBinSettings.max());


  //====== AT MET Selection
  fHistoSplitter.createShapeHistogramTriplet<TH1F>(true, HistoLevel::kVital, myDirs, hCtrlMET, 
    "MET_AtMETSelection", ";MET, GeV;N_{events}", cfg_MetBinSettings.bins(), cfg_MetBinSettings.min(), cfg_MetBinSettings.max());

  fHistoSplitter.createShapeHistogramTriplet<TH1F>(true, HistoLevel::kVital, myDirs, hCtrlMETPhi, 
    "METPhi_AtMETSelection", ";MET #phi;N_{events}", cfg_PhiBinSettings.bins(), cfg_PhiBinSettings.min(), cfg_PhiBinSettings.max());

  
  //====== At b-tagging
  fHistoSplitter.createShapeHistogramTriplet<TH1F>(true, HistoLevel::kVital, myDirs, hCtrlNBJets, 
    "NBjets_AtBtagging", ";Number of selected b jets;N_{events}",
    cfg_NJetsBinSettings.bins(), cfg_NJetsBinSettings.min(), cfg_NJetsBinSettings.max());
  
  fHistoSplitter.createShapeHistogramTriplet<TH1F>(true, HistoLevel::kVital, myDirs, hCtrlBJetPt, 
    "BJetPt_AtBtagging", ";Selected b jets p_{T}, GeV/c;N_{events}", cfg_PtBinSettings.bins(), cfg_PtBinSettings.min(), cfg_PtBinSettings.max());

  fHistoSplitter.createShapeHistogramTriplet<TH1F>(true, HistoLevel::kVital, myDirs, hCtrlBJetEta, 
    "BJetEta_AtBtagging", ";Selected b jets #eta;N_{events}", cfg_EtaBinSettings.bins(), cfg_EtaBinSettings.min(), cfg_EtaBinSettings.max());

  fHistoSplitter.createShapeHistogramTriplet<TH1F>(true, HistoLevel::kVital, myDirs, hCtrlBDiscriminator, 
    "BtagDiscriminator_AtBtagging", ";b tag discriminator;N_{events}",
    cfg_BJetDiscriminatorBinSettings.bins(), cfg_BJetDiscriminatorBinSettings.min(), cfg_BJetDiscriminatorBinSettings.max());
  

  //====== All selections
  fHistoSplitter.createShapeHistogramTriplet<TH1F>(true, HistoLevel::kVital, myDirs, hCtrlNVerticesAfterAllSelections, 
    "NVertices_AfterAllSelections", ";N_{vertices};N_{events}",
    cfg_NVerticesBinSettings.bins(), cfg_NVerticesBinSettings.min(), cfg_NVerticesBinSettings.max());

  fHistoSplitter.createShapeHistogramTriplet<TH1F>(true, HistoLevel::kVital, myDirs, hCtrlSelectedTauPtAfterAllSelections, 
    "SelectedTau_pT_AfterAllSelections", ";#tau p_{T}, GeV/c;N_{events}",
    cfg_PtBinSettings.bins(), cfg_PtBinSettings.min(), cfg_PtBinSettings.max());

  fHistoSplitter.createShapeHistogramTriplet<TH1F>(true, HistoLevel::kVital, myDirs, hCtrlSelectedTauEtaAfterAllSelections, 
    "SelectedTau_eta_AfterAllSelections", ";#tau #eta;N_{events}",
    cfg_EtaBinSettings.bins(), cfg_EtaBinSettings.min(), cfg_EtaBinSettings.max());

  fHistoSplitter.createShapeHistogramTriplet<TH1F>(true, HistoLevel::kVital, myDirs, hCtrlSelectedTauPhiAfterAllSelections, 
    "SelectedTau_phi_AfterAllSelections", ";#tau #phi;N_{events}",
    cfg_PhiBinSettings.bins(), cfg_PhiBinSettings.min(), cfg_PhiBinSettings.max());

  fHistoSplitter.createShapeHistogramTriplet<TH2F>(true, HistoLevel::kInformative, myDirs, hCtrlSelectedTauEtaPhiAfterAllSelections, 
    "SelectedTau_etaphi_AfterAllSelections", ";#tau #eta;#tau #phi;",
    cfg_EtaBinSettings.bins(), cfg_EtaBinSettings.min(), cfg_EtaBinSettings.max(),
    cfg_PhiBinSettings.bins(), cfg_PhiBinSettings.min(), cfg_PhiBinSettings.max());

  fHistoSplitter.createShapeHistogramTriplet<TH1F>(true, HistoLevel::kVital, myDirs, hCtrlSelectedTauLdgTrkPtAfterAllSelections, 
    "SelectedTau_ldgTrkPt_AfterAllSelections", ";#tau ldg. trk p_{T}, GeV/c;N_{events}",
    cfg_PtBinSettings.bins(), cfg_PtBinSettings.min(), cfg_PtBinSettings.max());

  fHistoSplitter.createShapeHistogramTriplet<TH1F>(true, HistoLevel::kVital, myDirs, hCtrlSelectedTauDecayModeAfterAllSelections, 
    "SelectedTau_DecayMode_AfterAllSelections", ";#tau decay mode;N_{events}",
    20, 0, 20);

  fHistoSplitter.createShapeHistogramTriplet<TH1F>(true, HistoLevel::kVital, myDirs, hCtrlSelectedTauNProngsAfterAllSelections, 
    "SelectedTau_Nprongs_AfterAllSelections", ";N_{prongs};N_{events}",
    10, 0, 10);

  fHistoSplitter.createShapeHistogramTriplet<TH1F>(true, HistoLevel::kVital, myDirs, hCtrlSelectedTauRtauAfterAllSelections, 
    "SelectedTau_Rtau_AfterAllSelections", ";R_{#tau};N_{events}",
    cfg_RtauBinSettings.bins(), cfg_RtauBinSettings.min(), cfg_RtauBinSettings.max());

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
    cfg_NJetsBinSettings.bins(), cfg_NJetsBinSettings.min(), cfg_NJetsBinSettings.max());

  fHistoSplitter.createShapeHistogramTriplet<TH1F>(true, HistoLevel::kVital, myDirs, hCtrlJetPtAfterAllSelections, 
    "JetPt_AfterAllSelections", ";Selected jets p_{T}, GeV/c;N_{events}",
    cfg_PtBinSettings.bins(), cfg_PtBinSettings.min(), cfg_PtBinSettings.max());

  fHistoSplitter.createShapeHistogramTriplet<TH1F>(true, HistoLevel::kVital, myDirs, hCtrlJetEtaAfterAllSelections, 
    "JetEta_AfterAllSelections", ";Selected jets #eta;N_{events}",
    cfg_EtaBinSettings.bins(), cfg_EtaBinSettings.min(), cfg_EtaBinSettings.max());

  fHistoSplitter.createShapeHistogramTriplet<TH2F>(true, HistoLevel::kInformative, myDirs, hCtrlJetEtaPhiAfterAllSelections, 
    "JetEtaPhi_AfterAllSelections", ";Selected jets #eta;Selected jets #phi",
    cfg_EtaBinSettings.bins(), cfg_EtaBinSettings.min(), cfg_EtaBinSettings.max(),
    cfg_PhiBinSettings.bins(), cfg_PhiBinSettings.min(), cfg_PhiBinSettings.max());

  fHistoSplitter.createShapeHistogramTriplet<TH1F>(true, HistoLevel::kVital, myDirs, hCtrlMETAfterAllSelections, 
    "MET_AfterAllSelections", ";MET, GeV;N_{events}", 
    cfg_MetBinSettings.bins(), cfg_MetBinSettings.min(), cfg_MetBinSettings.max());

  fHistoSplitter.createShapeHistogramTriplet<TH1F>(true, HistoLevel::kVital, myDirs, hCtrlMETPhiAfterAllSelections,
    "METPhi_AfterAllSelections", ";MET #phi;N_{events}", 
    cfg_PhiBinSettings.bins(), cfg_PhiBinSettings.min(), cfg_PhiBinSettings.max());

  fHistoSplitter.createShapeHistogramTriplet<TH1F>(true, HistoLevel::kVital, myDirs, hCtrlNBJetsAfterAllSelections,
    "NBjets_AfterAllSelections", ";Number of selected b jets;N_{events}",
    cfg_NJetsBinSettings.bins(), cfg_NJetsBinSettings.min(), cfg_NJetsBinSettings.max());

  fHistoSplitter.createShapeHistogramTriplet<TH1F>(true, HistoLevel::kVital, myDirs, hCtrlBJetPtAfterAllSelections,
    "BJetPt_AfterAllSelections", ";Selected b jets p_{T}, GeV/c;N_{events}",
    cfg_PtBinSettings.bins(), cfg_PtBinSettings.min(), cfg_PtBinSettings.max());

  fHistoSplitter.createShapeHistogramTriplet<TH1F>(true, HistoLevel::kVital, myDirs, hCtrlBJetEtaAfterAllSelections,
    "BJetEta_AfterAllSelections", ";Selected b jets #eta;N_{events}",
    cfg_EtaBinSettings.bins(), cfg_EtaBinSettings.min(), cfg_EtaBinSettings.max());

  fHistoSplitter.createShapeHistogramTriplet<TH1F>(true, HistoLevel::kVital, myDirs, hCtrlBDiscriminatorAfterAllSelections, 
    "BtagDiscriminator_AfterAllSelections", ";b tag discriminator;N_{events}",
    cfg_BJetDiscriminatorBinSettings.bins(), cfg_BJetDiscriminatorBinSettings.min(), cfg_BJetDiscriminatorBinSettings.max());
  
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



void CommonPlots::fillControlPlotsAtTauSelection(const Event& event, const TauSelection::Data& data) {
  fTauData = data;
  for (auto& p: fBaseObjects) { p->fillControlPlotsAtTauSelection(event, data); }

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


void CommonPlots::fillControlPlotsAfterElectronSelection(const Event& event, const ElectronSelection::Data& data) {

  for (auto& p: fBaseObjects) { p->fillControlPlotsAfterElectronSelection(event, data); }
  fElectronData = data;

  if (event.isData()) {}
  
  return;
}


void CommonPlots::fillControlPlotsAfterMuonSelection(const Event& event, const MuonSelection::Data& data) {

  for (auto& p: fBaseObjects) { p->fillControlPlotsAfterMuonSelection(event, data); }
  fMuonData = data;

  if (event.isData()) {}
  
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
  fHistoSplitter.fillShapeHistogramTriplet(hCtrlNVerticesAfterJetSelections, !bIsFakeTau, iVertices);

  if (isQCDMeasurement()) {
    fHistoSplitter.fillShapeHistogramTriplet(hCtrlSelectedTauPtAfterJetSelections, !bIsFakeTau, fTauData.getAntiIsolatedTau().pt());
    fHistoSplitter.fillShapeHistogramTriplet(hCtrlSelectedTauEtaAfterJetSelections, !bIsFakeTau, fTauData.getAntiIsolatedTau().eta());
    fHistoSplitter.fillShapeHistogramTriplet(hCtrlSelectedTauPhiAfterJetSelections, !bIsFakeTau, fTauData.getAntiIsolatedTau().phi());
    fHistoSplitter.fillShapeHistogramTriplet(hCtrlSelectedTauEtaPhiAfterJetSelections, !bIsFakeTau, fTauData.getAntiIsolatedTau().eta(), fTauData.getAntiIsolatedTau().phi());
    fHistoSplitter.fillShapeHistogramTriplet(hCtrlSelectedTauLdgTrkPtAfterJetSelections, !bIsFakeTau, fTauData.getAntiIsolatedTau().lChTrkPt());
    fHistoSplitter.fillShapeHistogramTriplet(hCtrlSelectedTauDecayModeAfterJetSelections, !bIsFakeTau, fTauData.getAntiIsolatedTau().decayMode());
    fHistoSplitter.fillShapeHistogramTriplet(hCtrlSelectedTauNProngsAfterJetSelections, !bIsFakeTau, fTauData.getAntiIsolatedTau().nProngs());
    fHistoSplitter.fillShapeHistogramTriplet(hCtrlSelectedTauRtauAfterJetSelections, !bIsFakeTau, fTauData.getRtauOfAntiIsolatedTau());
    for (auto& p: fHelper.getTauSourceData(!event.isMC(), fTauData.getAntiIsolatedTau())) {
      fHistoSplitter.fillShapeHistogramTriplet(hCtrlSelectedTauSourceAfterJetSelections, !bIsFakeTau, p);
    }
  } else {
    fHistoSplitter.fillShapeHistogramTriplet(hCtrlSelectedTauPtAfterJetSelections, !bIsFakeTau, fTauData.getSelectedTau().pt());
    fHistoSplitter.fillShapeHistogramTriplet(hCtrlSelectedTauEtaAfterJetSelections, !bIsFakeTau, fTauData.getSelectedTau().eta());
    fHistoSplitter.fillShapeHistogramTriplet(hCtrlSelectedTauPhiAfterJetSelections, !bIsFakeTau, fTauData.getSelectedTau().phi());
    fHistoSplitter.fillShapeHistogramTriplet(hCtrlSelectedTauEtaPhiAfterJetSelections, !bIsFakeTau, fTauData.getSelectedTau().eta(), fTauData.getSelectedTau().phi());
    fHistoSplitter.fillShapeHistogramTriplet(hCtrlSelectedTauLdgTrkPtAfterJetSelections, !bIsFakeTau, fTauData.getSelectedTau().lChTrkPt());
    fHistoSplitter.fillShapeHistogramTriplet(hCtrlSelectedTauDecayModeAfterJetSelections, !bIsFakeTau, fTauData.getSelectedTau().decayMode());
    fHistoSplitter.fillShapeHistogramTriplet(hCtrlSelectedTauNProngsAfterJetSelections, !bIsFakeTau, fTauData.getSelectedTau().nProngs());
    fHistoSplitter.fillShapeHistogramTriplet(hCtrlSelectedTauRtauAfterJetSelections, !bIsFakeTau, fTauData.getRtauOfSelectedTau());
    for (auto& p: fHelper.getTauSourceData(!event.isMC(), fTauData.getSelectedTau())) {
      fHistoSplitter.fillShapeHistogramTriplet(hCtrlSelectedTauSourceAfterJetSelections, !bIsFakeTau, p);
    }
  }
  fHistoSplitter.fillShapeHistogramTriplet(hCtrlNJetsAfterJetSelections, !bIsFakeTau, fJetData.getNumberOfSelectedJets());

  for (auto& p: fJetData.getSelectedJets()) 
    {
      fHistoSplitter.fillShapeHistogramTriplet(hCtrlJetPtAfterJetSelections    , !bIsFakeTau, p.pt()  );
      fHistoSplitter.fillShapeHistogramTriplet(hCtrlJetEtaAfterJetSelections   , !bIsFakeTau, p.eta() );
      fHistoSplitter.fillShapeHistogramTriplet(hCtrlJetEtaPhiAfterJetSelections, !bIsFakeTau, p.eta(), p.phi());
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
