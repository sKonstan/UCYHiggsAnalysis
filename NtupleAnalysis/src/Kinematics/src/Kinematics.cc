// -*- c++ -*-
#include "Framework/interface/BaseSelector.h"
#include "Framework/interface/makeTH.h"

#include "DataFormat/interface/Event.h"
#include "EventSelection/interface/CommonPlots.h"
#include "EventSelection/interface/EventSelections.h"

#include "TDirectory.h"

#include <algorithm>  // std::sort
#include <vector>     // std::vector

class Kinematics: public BaseSelector {
public:
  struct AscendingOrder{ bool operator() (double a, double b) const{  return ( a < b ); } };
  struct DescendingOrder{ bool operator() (double a, double b) const{  return ( a > b ); } };
enum BTagPartonType {
    kBTagB,
    kBTagC,
    kBtagG,
    kBtagLight,
  };
  explicit Kinematics(const ParameterSet& config);
  virtual ~Kinematics() {}

  /// Books histograms
  virtual void book(TDirectory *dir) override;
  /// Sets up branches for reading the TTree
  virtual void setupBranches(BranchManager& branchManager) override;
  /// Called for each event
  virtual void process(Long64_t entry) override;

private:
  // Input parameters
  const double cfg_ElePtCutMin;
  const double cfg_EleEtaCutMax;
  const double cfg_MuPtCutMin;
  const double cfg_MuEtaCutMax;
  const double cfg_BjetPtCutMin;
  const double cfg_BjetEtaCutMax;
  const std::vector<double> cfg_LeptonTriggerPtCutMin;
  const double PT_MAX  = 200.0;
  const int PT_BINS    =  10;
  const double ETA_MAX =   3.0;
  const int ETA_BINS   =  30;

  // Event selection classes and event counters (in same order like they are applied)
  Count cAllEvents;
  Count cElectrons;
  Count cMuons;
  Count cBjets;
  Count cTrigger;
  // ElectronSelection fElectronSelection;
  // Count cSelected;
    
  // Non-common histograms
  WrappedTH1* hAllElectronsPt;
  WrappedTH1* hAllElectronsEta;
  WrappedTH1* hPassedElectronsPt;
  WrappedTH1* hPassedElectronsEta;
  WrappedTH1* hAllMuonsPt;
  WrappedTH1* hAllMuonsEta;
  WrappedTH1* hPassedMuonsPt;
  WrappedTH1* hPassedMuonsEta;

  WrappedTH1* hAllGenElectronsPt;
  WrappedTH1* hAllGenElectronsEta;
  WrappedTH1* hAllGenMuonsPt;
  WrappedTH1* hAllGenMuonsEta;
  WrappedTH1* hAllGenBjetsPt;
  WrappedTH1* hAllGenBjetsEta;
  WrappedTH1* hPassedGenElectronsPt;
  WrappedTH1* hPassedGenElectronsEta;
  WrappedTH1* hPassedGenMuonsPt;
  WrappedTH1* hPassedGenMuonsEta;
  WrappedTH1* hPassedGenBjetsPt;
  WrappedTH1* hPassedGenBjetsEta;

};

#include "Framework/interface/SelectorFactory.h"
REGISTER_SELECTOR(Kinematics);

Kinematics::Kinematics(const ParameterSet& config)
  : BaseSelector(config),
    cfg_ElePtCutMin(config.getParameter<double>("ElePtCutMin")),
    cfg_EleEtaCutMax(config.getParameter<double>("EleEtaCutMax")),
    cfg_MuPtCutMin(config.getParameter<double>("MuPtCutMin")),
    cfg_MuEtaCutMax(config.getParameter<double>("MuEtaCutMax")),
    cfg_BjetPtCutMin(config.getParameter<double>("BjetPtCutMin")),
    cfg_BjetEtaCutMax(config.getParameter<double>("BjetPtCutMax")),
    cfg_LeptonTriggerPtCutMin(config.getParameter<std::vector<double> >("LeptonTriggerPtCutMin")),
    cAllEvents(fEventCounter.addCounter("All Events")),
    cElectrons(fEventCounter.addCounter("Passed Electrons")),
    cMuons(fEventCounter.addCounter("Passed Muons")),
    cBjets(fEventCounter.addCounter("Passed Bjets")),
    cTrigger(fEventCounter.addCounter("Passed Trigger"))
    // fElectronSelection(config.getParameter<ParameterSet>("ElectronSelection"),
    // 		       fEventCounter, fHistoWrapper, nullptr, "Veto"),
    //cSelected(fEventCounter.addCounter("Selected events"))
{ }

void Kinematics::book(TDirectory *dir) {
  // std::cout << "=== Kinematics.cc:\n\t Kinematics::book()" << std::endl;

  // Book histograms in event selection classes
  // fElectronSelection.bookHistograms(dir);
  // fMuonSelection.bookHistograms(dir);
  // fJetSelection.bookHistograms(dir);
  // fAngularCutsCollinear.bookHistograms(dir);
  // fBJetSelection.bookHistograms(dir);
  // fMETSelection.bookHistograms(dir);

  // Book non-common histograms
  hPassedElectronsPt  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "PassedElectronsPt" , "PassedElectronsPt:Electron p_{T}, GeVc^{-1}:Event", PT_BINS, 0, PT_MAX);
  hPassedElectronsEta = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "PassedElectronsEta" , "PassedElectronsEta:Electron #eta:Events", ETA_BINS, -ETA_MAX, ETA_MAX);
  hAllElectronsPt     = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "AllElectronsPt" , "AllElectronsPt:Electron p_{T}, GeVc^{-1}:Event", PT_BINS, 0, PT_MAX);
  hAllElectronsEta    = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "AllElectronsEta" , "AllElectronsEta:Electron #eta:Events", ETA_BINS, -ETA_MAX, ETA_MAX);

  hPassedMuonsPt  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "PassedMuonsPt" , "PassedMuonsPt:Muon p_{T}, GeVc^{-1}:Event", PT_BINS, 0, PT_MAX);
  hPassedMuonsEta = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "PassedMuonsEta" , "PassedMuonsEta:Muon #eta:Events", ETA_BINS, -ETA_MAX, ETA_MAX);
  hAllMuonsPt     = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "AllMuonsPt" , "AllMuonsPt:Muon p_{T}, GeVc^{-1}:Event", PT_BINS, 0, PT_MAX);
  hAllMuonsEta    = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "AllMuonsEta" , "AllMuonsEta:Muon #eta:Events", ETA_BINS, -ETA_MAX, ETA_MAX);

  hAllGenElectronsPt     = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "AllGenElectronsPt"    , "AllGenElectronsPt:Jet p_{T}, GeVc^{-1}:N_{jets}", PT_BINS, 0, PT_MAX);
  hAllGenMuonsPt         = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "AllGenMuonsPt"        , "AllGenMuonsPt:Jet p_{T}, GeVc^{-1}:N_{jets}"    , PT_BINS, 0, PT_MAX);
  hAllGenBjetsPt         = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "AllGenBjetsPt"        , "AllGenBjetsPt:Jet p_{T}, GeVc^{-1}:N_{jets}"    , PT_BINS, 0, PT_MAX);
  hAllGenElectronsEta    = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "AllGenElectronsEta"   , "AllGenElectronsEta:Jet #eta:N_{jets}", ETA_BINS, -ETA_MAX, ETA_MAX);
  hAllGenMuonsEta        = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "AllGenMuonsEta"       , "AllGenMuonsEta:Jet #eta:N_{jets}"    , ETA_BINS, -ETA_MAX, ETA_MAX);
  hAllGenBjetsEta        = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "AllGenBjetsEta"       , "AllGenBjetsEta:Jet #eta:N_{jets}"    , ETA_BINS, -ETA_MAX, ETA_MAX);
  hPassedGenElectronsPt  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "PassedGenElectronsPt" , "PassedGenElectronsPt:Jet p_{T}, GeVc^{-1}:N_{jets}", PT_BINS, 0, PT_MAX);
  hPassedGenMuonsPt      = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "PassedGenMuonsPt"     , "PassedGenMuonsPt:Jet p_{T}, GeVc^{-1}:N_{jets}"    , PT_BINS, 0, PT_MAX);
  hPassedGenBjetsPt      = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "PassedGenBjetsPt"     , "PassedGenBjetsPt:Jet p_{T}, GeVc^{-1}:N_{jets}"    , PT_BINS, 0, PT_MAX);
  hPassedGenElectronsEta = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "PassedGenElectronsEta", "PassedGenElectronsEta:Jet #eta:N_{jets}", ETA_BINS, -ETA_MAX, ETA_MAX);
  hPassedGenMuonsEta     = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "PassedGenMuonsEta"    , "PassedGenMuonsEta:Jet #eta:N_{jets}"    , ETA_BINS, -ETA_MAX, ETA_MAX);
  hPassedGenBjetsEta     = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "PassedGenBjetsEta"    , "PassedGenBjetsEta:Jet #eta:N_{jets}"    , ETA_BINS, -ETA_MAX, ETA_MAX);

  return;
}


void Kinematics::setupBranches(BranchManager& branchManager) {
  // std::cout << "=== Kinematics.cc:\n\t Kinematics::setupBranches()" << std::endl;
  fEvent.setupBranches(branchManager);

  return;
}


void Kinematics::process(Long64_t entry) {
  // std::cout << "=== Kinematics.cc:\n\t Kinematics::process()" << std::endl;

  for(Electron elec: fEvent.electrons()) {
    hPassedElectronsPt->Fill(elec.pt());
    hPassedElectronsEta->Fill(elec.eta());
    if(elec.pt() < 15 && std::abs(elec.eta()) > 2.4) continue;
    hAllElectronsPt->Fill(elec.pt());
    hAllElectronsEta->Fill(elec.eta());
  }


  for(Muon mu: fEvent.muons()) {
    hPassedMuonsPt->Fill(mu.pt());
    hPassedMuonsEta->Fill(mu.eta());
    if(mu.pt() < 15 && std::abs(mu.eta()) > 2.4) continue;
    hAllMuonsPt->Fill(mu.pt());
    hAllMuonsEta->Fill(mu.eta());
  }


  if( !fEvent.isMC() ) return;

  // Variable declarations
  Size_t nGenParticles = 0;
  size_t nGenMuons     = 0;
  size_t nGenElectrons = 0;
  size_t nGenBjets     = 0;
  bool bPassTrg        = true;
  std::vector<double> v_leptonPt;

  // For-loop: All GenParticles
  for( auto& gen : fEvent.genparticles().getAllGenpCollection() ){
    nGenParticles++;

    // Get loop variables
    int genP_PdgId       = gen.pdgId();
    double genP_Pt       = gen.pt();
    double genP_Eta      = gen.eta();
    double genP_Status   = gen.status(); // PYTHIA8: http://home.thep.lu.se/~torbjorn/pythia81html/ParticleProperties.html
    // double GenP_Phi      = gen.phi();
    // double GenP_E        = gen.e();
    // double GenP_Mass     = gen.mass();
    // double GenP_VertexX  = gen.vertexX();
    // double GenP_VertexY  = gen.vertexY();
    // double GenP_VertexZ  = gen.vertexX();
    // double GenP_Charge   = gen.charge();
    // double GenP_Mothers  = gen.mothers().size();
    // double GenP_Daughters= gen.daughters().size();

    // std::cout << "fEvent.genparticles().at(1).pt() " = << fEvent.genparticles().at(1).pt() << std::endl;
    
    // Electrons
    if(std::abs(genP_PdgId) == 11 && genP_Status < 10){

      hAllGenElectronsPt ->Fill(genP_Pt);
      hAllGenElectronsEta->Fill(genP_Eta);

      if(genP_Pt >= cfg_ElePtCutMin && std::abs(genP_Eta) < cfg_EleEtaCutMax) {
	// std::cout << "electron: Pt = " << genP_Pt << ", Eta = " << genP_Eta << ", Status = " << genP_Status << std::endl;
	nGenElectrons++;
	v_leptonPt.push_back(genP_Pt);
	hPassedGenElectronsPt ->Fill(genP_Pt);
	hPassedGenElectronsEta->Fill(genP_Eta);	
      }
    }
    if(nGenElectrons == 0) continue;

    // Muons
    if(std::abs(genP_PdgId) == 13 && genP_Status < 10){

      hAllGenMuonsPt ->Fill(genP_Pt);
      hAllGenMuonsEta->Fill(genP_Eta);

      if(genP_Pt >= cfg_MuPtCutMin && std::abs(genP_Eta) < cfg_MuEtaCutMax){
	// std::cout << "muon: Pt = " << genP_Pt << ", Eta = " << genP_Eta << ", Status = " << genP_Status << std::endl;
	nGenMuons++;
	v_leptonPt.push_back(genP_Pt);
	hPassedGenMuonsPt ->Fill(genP_Pt);
	hPassedGenMuonsEta->Fill(genP_Eta);
      }
    }
    if(nGenMuons == 0) continue;
    
    // Bjets
    if(std::abs(genP_PdgId) == 5){
      
      hAllGenBjetsPt ->Fill(genP_Pt);
      hAllGenBjetsEta->Fill(genP_Eta);
      
      if(genP_Pt >= cfg_BjetPtCutMin && std::abs(genP_Eta) < cfg_BjetEtaCutMax){
	
	hPassedGenBjetsPt ->Fill(genP_Pt);
	hPassedGenBjetsEta->Fill(genP_Eta);
	
	// std::cout << "bquark: Pt = " << genP_Pt << ", Eta = " << genP_Eta << ", Status = " << genP_Status << std::endl;
	nGenBjets++;
      }
    }
    if(nGenBjets == 0) continue;
    
  }// for( auto& gen : fEvent.genparticles().getAllGenpCollection() ){
  
  // Trigger
  std::sort( v_leptonPt.begin(), v_leptonPt.end(), DescendingOrder() );
  if (v_leptonPt.size() < 2) bPassTrg = false;
  else{
    for(Size_t i=0; i < cfg_LeptonTriggerPtCutMin.size(); i++){
      if (v_leptonPt.at(i) < cfg_LeptonTriggerPtCutMin.at(i) ){
	bPassTrg = false;
	break;
      }
    }// for(Size_t i=0; i < cfg_LeptonTriggerPtCutMin.size(); i++){
  }// else

  // Increment Counters    
  cAllEvents.increment();
  if (nGenElectrons > 0) cElectrons.increment();
  if (nGenMuons > 0) cMuons.increment();
  if (nGenBjets > 0) cBjets.increment();
  if (bPassTrg) cTrigger.increment();
  
  /*
  // std::cout << "=== Kinematics.cc:\n\t Kinematics::process()" << std::endl;

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
    if (id == 5)       hAllGenBjets->Fill(p.pt());
    else if (id == 4)  hAllGenCjets->Fill(p.pt());
    else if (id == 21) hAllGenGjets->Fill(p.pt());
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
    if (id == 5)       hPassedGenBjets->Fill(p.pt());
    else if (id == 4)  hPassedGenCjets->Fill(p.pt());
    else if (id == 21) hPassedGenGjets->Fill(p.pt());
    else if (id == 1 || id == 2 || id == 3) hPassedGenLightjets->Fill(p.pt());

  }// for (auto& p: bjetData.getSelectedBJets()) {

  //====== All cuts passed
  cSelected.increment();

  //====== All Final plots
  */

}
