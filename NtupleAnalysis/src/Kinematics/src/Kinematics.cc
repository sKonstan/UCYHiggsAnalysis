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
  Count cTrigger;
  // ElectronSelection fElectronSelection;
  // Count cSelected;
    
  // Non-common histograms
  WrappedTH1* hAllElectronsPt;
  WrappedTH1* hAllElectronsEta;
  WrappedTH1* hAllMuonsPt;
  WrappedTH1* hAllMuonsEta;
  WrappedTH1* hAllBjetsPt;
  WrappedTH1* hAllBjetsEta;
  WrappedTH1* hPassedElectronsPt;
  WrappedTH1* hPassedElectronsEta;
  WrappedTH1* hPassedMuonsPt;
  WrappedTH1* hPassedMuonsEta;
  WrappedTH1* hPassedBjetsPt;
  WrappedTH1* hPassedBjetsEta;

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
    cAllEvents(fEventCounter.addCounter("All events")),
    cTrigger(fEventCounter.addCounter("Passed trigger"))
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
  hAllElectronsPt     = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "AllElectronsPt" , "AllElectronsPt:Jet p_{T}, GeVc^{-1}:N_{jets}", PT_BINS, 0, PT_MAX);
  hAllMuonsPt         = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "AllMuonsPt"     , "AllMuonsPt:Jet p_{T}, GeVc^{-1}:N_{jets}"    , PT_BINS, 0, PT_MAX);
  hAllBjetsPt         = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "AllBjetsPt"     , "AllBjetsPt:Jet p_{T}, GeVc^{-1}:N_{jets}"    , PT_BINS, 0, PT_MAX);
  hAllElectronsEta    = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "AllElectronsEta", "AllElectronsEta:Jet #eta:N_{jets}", ETA_BINS, -ETA_MAX, ETA_MAX);
  hAllMuonsEta        = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "AllMuonsEta"    , "AllMuonsEta:Jet #eta:N_{jets}"    , ETA_BINS, -ETA_MAX, ETA_MAX);
  hAllBjetsEta        = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "AllBjetsEta"    , "AllBjetsEta:Jet #eta:N_{jets}"    , ETA_BINS, -ETA_MAX, ETA_MAX);
  hPassedElectronsPt  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "PassedElectronsPt" , "PassedElectronsPt:Jet p_{T}, GeVc^{-1}:N_{jets}", PT_BINS, 0, PT_MAX);
  hPassedMuonsPt      = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "PassedMuonsPt"     , "PassedMuonsPt:Jet p_{T}, GeVc^{-1}:N_{jets}"    , PT_BINS, 0, PT_MAX);
  hPassedBjetsPt      = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "PassedBjetsPt"     , "PassedBjetsPt:Jet p_{T}, GeVc^{-1}:N_{jets}"    , PT_BINS, 0, PT_MAX);
  hPassedElectronsEta = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "PassedElectronsEta", "PassedElectronsEta:Jet #eta:N_{jets}", ETA_BINS, -ETA_MAX, ETA_MAX);
  hPassedMuonsEta     = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "PassedMuonsEta"    , "PassedMuonsEta:Jet #eta:N_{jets}"    , ETA_BINS, -ETA_MAX, ETA_MAX);
  hPassedBjetsEta     = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "PassedBjetsEta"    , "PassedBjetsEta:Jet #eta:N_{jets}"    , ETA_BINS, -ETA_MAX, ETA_MAX);

  return;
}


void Kinematics::setupBranches(BranchManager& branchManager) {
  // std::cout << "=== Kinematics.cc:\n\t Kinematics::setupBranches()" << std::endl;
  fEvent.setupBranches(branchManager);

  return;
}


void Kinematics::process(Long64_t entry) {
  // std::cout << "=== Kinematics.cc:\n\t Kinematics::process()" << std::endl;

  //====== Initialize
  cAllEvents.increment();

  if( !fEvent.isMC() ) return;

  // Variable declarations
  Size_t nGenParticles = 0;
  size_t nGenMuons     = 0;
  size_t nGenElectrons = 0;
  size_t nGenBjets     = 0;
  std::vector<double> v_leptonPt;

  // For-loop: All GenParticles
  for( auto& gen : fEvent.genparticles().getAllGenpCollection() ){
    nGenParticles++;
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

    // Electrons
    if(std::abs(genP_PdgId) == 11 && genP_Status < 10){

      hAllElectronsPt ->Fill(genP_Pt);
      hAllElectronsEta->Fill(genP_Eta);

      if(genP_Pt >= cfg_ElePtCutMin && std::abs(genP_Eta) < cfg_EleEtaCutMax) {
	// std::cout << "electron: Pt = " << genP_Pt << ", Eta = " << genP_Eta << ", Status = " << genP_Status << std::endl;
	nGenElectrons++;
	v_leptonPt.push_back(genP_Pt);
	hPassedElectronsPt ->Fill(genP_Pt);
	hPassedElectronsEta->Fill(genP_Eta);	
      }
    }
    if(nGenElectrons == 0) continue;


    // Muons
    if(std::abs(genP_PdgId) == 13 && genP_Status < 10){

      hAllMuonsPt ->Fill(genP_Pt);
      hAllMuonsEta->Fill(genP_Eta);

      if(genP_Pt >= cfg_MuPtCutMin && std::abs(genP_Eta) < cfg_MuEtaCutMax){
	// std::cout << "muon: Pt = " << genP_Pt << ", Eta = " << genP_Eta << ", Status = " << genP_Status << std::endl;
	nGenMuons++;
	v_leptonPt.push_back(genP_Pt);
	hPassedMuonsPt ->Fill(genP_Pt);
	hPassedMuonsEta->Fill(genP_Eta);
      }
    }
    if(nGenMuons == 0) continue;


    // Bjets
    if(std::abs(genP_PdgId) == 5){
      
      hAllBjetsPt ->Fill(genP_Pt);
      hAllBjetsEta->Fill(genP_Eta);
      
      if(genP_Pt >= cfg_BjetPtCutMin && std::abs(genP_Eta) < cfg_BjetEtaCutMax){
	
	hPassedBjetsPt ->Fill(genP_Pt);
	hPassedBjetsEta->Fill(genP_Eta);
	
	// std::cout << "bquark: Pt = " << genP_Pt << ", Eta = " << genP_Eta << ", Status = " << genP_Status << std::endl;
	nGenBjets++;
      }
    }
    if(nGenBjets == 0) continue;


    // Trigger
    std::sort( v_leptonPt.begin(), v_leptonPt.end(), DescendingOrder() );
    bool bPassTrg = true;
    if (v_leptonPt.size() < 2) 
      {
	std::cout << "=== Kinematics.cc:\n\t " << nGenMuons <<  " Muons + " << nGenElectrons << " Electrons = " << v_leptonPt.size() << " Leptons. Break" << std::endl;
	bPassTrg = false;
	break;
      }
    else{
      for(Size_t i=0; i < cfg_LeptonTriggerPtCutMin.size(); i++){
	
	if (v_leptonPt.at(i) < cfg_LeptonTriggerPtCutMin.at(i) ) 
	  {
	    bPassTrg = false;
	    break;
	  }
      }// for(Size_t i=0; i < cfg_LeptonTriggerPtCutMin.size(); i++){
    }// else{
    if (!bPassTrg) continue;

    cTrigger.increment();
    
  }// for( auto& gen : fEvent.genparticles().getAllGenpCollection() ){
  // std::cout << "GenParticle Collection Size = " << nGenParticles << std::endl;

  // size_t nelectrons = 0;
  // for(Electron electron: fEvent.electrons()) {
  //   std::cout << "electron.pdgId() = " << electron.pdgId() << std::endl;
  //   if(electron.pt() > 15 && std::abs(electron.eta()) < 2.4)
  //     ++nelectrons;
  // }
  // if(nelectrons > 0) return;


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
  */

}
