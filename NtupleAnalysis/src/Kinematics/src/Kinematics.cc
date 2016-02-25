// -*- c++ -*-
#include <algorithm>  // std::sort
#include <vector>     // std::vector

#include "TDirectory.h"

#include "Framework/interface/BaseSelector.h"
#include "Framework/interface/makeTH.h"
#include "DataFormat/interface/Event.h"
#include "EventSelection/interface/CommonPlots.h"
#include "EventSelection/interface/EventSelections.h"
#include "Tools/interface/MCTools.h"

//#define DEBUG

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
  const int PT_BINS    = 10;
  const double ETA_MAX = 3.0;
  const int ETA_BINS   = 30;

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
    cAllEvents(fEventCounter.addCounter("All")),
    cElectrons(fEventCounter.addCounter("Electrons")),
    cMuons(fEventCounter.addCounter("Muons")),
    cBjets(fEventCounter.addCounter("Bjets")),
    cTrigger(fEventCounter.addCounter("Trigger"))
{ }

void Kinematics::book(TDirectory *dir) {
#ifdef DEBUG
  std::cout << "=== Kinematics.cc:\n\t Kinematics::book()" << std::endl;
#endif

  // Book histograms in event selection classes
  // fElectronSelection.bookHistograms(dir);
  // fMuonSelection.bookHistograms(dir);
  // fJetSelection.bookHistograms(dir);
  // fBJetSelection.bookHistograms(dir);
  // fMETSelection.bookHistograms(dir);

  // Book non-common histograms
  hPassedElectronsPt  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "PassedElectronsPt" , "PassedElectronsPt:Electron p_{T}, GeVc^{-1}:Event", PT_BINS, 0, PT_MAX );
  hPassedElectronsEta = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "PassedElectronsEta", "PassedElectronsEta:Electron #eta:Events"  , ETA_BINS, -ETA_MAX, ETA_MAX);
  hPassedMuonsPt      = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "PassedMuonsPt"     , "PassedMuonsPt:Muon p_{T}, GeVc^{-1}:Event", PT_BINS , 0       , PT_MAX );
  hPassedMuonsEta     = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "PassedMuonsEta"    , "PassedMuonsEta:Muon #eta:Events"          , ETA_BINS, -ETA_MAX, ETA_MAX);
  //
  hAllElectronsPt     = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "AllElectronsPt" , "AllElectronsPt:Electron p_{T}, GeVc^{-1}:Event", PT_BINS, 0, PT_MAX );
  hAllElectronsEta    = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "AllElectronsEta", "AllElectronsEta:Electron #eta:Events"  , ETA_BINS, -ETA_MAX, ETA_MAX);
  hAllMuonsPt         = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "AllMuonsPt"     , "AllMuonsPt:Muon p_{T}, GeVc^{-1}:Event", PT_BINS , 0       , PT_MAX );
  hAllMuonsEta        = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "AllMuonsEta"    , "AllMuonsEta:Muon #eta:Events"          , ETA_BINS, -ETA_MAX, ETA_MAX);


  hAllGenElectronsPt     = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "AllGenElectronsPt"    , "AllGenElectronsPt:Jet p_{T}, GeVc^{-1}:N_{jets}", PT_BINS, 0, PT_MAX);
  hAllGenMuonsPt         = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "AllGenMuonsPt"        , "AllGenMuonsPt:Jet p_{T}, GeVc^{-1}:N_{jets}"    , PT_BINS, 0, PT_MAX);
  hAllGenBjetsPt         = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "AllGenBjetsPt"        , "AllGenBjetsPt:Jet p_{T}, GeVc^{-1}:N_{jets}"    , PT_BINS, 0, PT_MAX);
  hAllGenElectronsEta    = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "AllGenElectronsEta"   , "AllGenElectronsEta:Jet #eta:N_{jets}", ETA_BINS, -ETA_MAX, ETA_MAX);
  hAllGenMuonsEta        = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "AllGenMuonsEta"       , "AllGenMuonsEta:Jet #eta:N_{jets}"    , ETA_BINS, -ETA_MAX, ETA_MAX);
  hAllGenBjetsEta        = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "AllGenBjetsEta"       , "AllGenBjetsEta:Jet #eta:N_{jets}"    , ETA_BINS, -ETA_MAX, ETA_MAX);
  //
  hPassedGenElectronsPt  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "PassedGenElectronsPt" , "PassedGenElectronsPt:Jet p_{T}, GeVc^{-1}:N_{jets}", PT_BINS, 0, PT_MAX);
  hPassedGenMuonsPt      = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "PassedGenMuonsPt"     , "PassedGenMuonsPt:Jet p_{T}, GeVc^{-1}:N_{jets}"    , PT_BINS, 0, PT_MAX);
  hPassedGenBjetsPt      = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "PassedGenBjetsPt"     , "PassedGenBjetsPt:Jet p_{T}, GeVc^{-1}:N_{jets}"    , PT_BINS, 0, PT_MAX);
  hPassedGenElectronsEta = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "PassedGenElectronsEta", "PassedGenElectronsEta:Jet #eta:N_{jets}", ETA_BINS, -ETA_MAX, ETA_MAX);
  hPassedGenMuonsEta     = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "PassedGenMuonsEta"    , "PassedGenMuonsEta:Jet #eta:N_{jets}"    , ETA_BINS, -ETA_MAX, ETA_MAX);
  hPassedGenBjetsEta     = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "PassedGenBjetsEta"    , "PassedGenBjetsEta:Jet #eta:N_{jets}"    , ETA_BINS, -ETA_MAX, ETA_MAX);

  return;
}


void Kinematics::setupBranches(BranchManager& branchManager) {
#ifdef DEBUG
  std::cout << "=== Kinematics.cc:\n\t Kinematics::setupBranches()" << std::endl;
#endif
  fEvent.setupBranches(branchManager);

  return;
}


void Kinematics::process(Long64_t entry) {
#ifdef DEBUG
  std::cout << "=== Kinematics.cc:\n\t Kinematics::process()" << std::endl;
#endif


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


  //  /* attikis
  if( !fEvent.isMC() ) return;

  // Variable declarations
  // static double firstEvt = fEvent.eventID().event(); // static = only be executed once
  // double evtNum          = fEvent.eventID().event();
  int genP_Index         = -1;
  size_t nGenMuons       = 0;
  size_t nGenElectrons   = 0;
  size_t nGenBjets       = 0;
  bool bPassTrg          = true;
  std::vector<double> v_leptonPt;
  MCTools mcTools(fEvent);  

  // For-loop: GenParticles
  //  for(GenParticle genP: fEvent.genparticles()) {
  for(auto genP: fEvent.genparticles()) {

    genP_Index++;

    // Get loop variables
    int genP_PdgId     = genP.pdgId();
    double genP_Pt     = genP.pt();
    double genP_Eta    = genP.eta();
    double genP_Status = genP.status(); // PYTHIA8: http://home.thep.lu.se/~torbjorn/pythia81html/ParticleProperties.html

    // if (genP_Index==0) mcTools.PrintGenParticle(genP_Index, true);
    // else
    //   {
    // 	cout << "\n" << endl;
    // 	mcTools.PrintGenParticle(genP_Index, false);
    //   }
    
    // Electrons
    if(std::abs(genP_PdgId) == 11 && genP_Status < 10){

      // Fill histos
      hAllGenElectronsPt ->Fill(genP_Pt);
      hAllGenElectronsEta->Fill(genP_Eta);
      // Acceptance cuts
      if(genP_Pt >= cfg_ElePtCutMin && std::abs(genP_Eta) < cfg_EleEtaCutMax) {

	nGenElectrons++;
	v_leptonPt.push_back(genP_Pt);

	// Fill histos
	hPassedGenElectronsPt ->Fill(genP_Pt);
	hPassedGenElectronsEta->Fill(genP_Eta);	
      }
    }// Electrons
    if(nGenElectrons == 0) continue;

    // Muons
    if(std::abs(genP_PdgId) == 13 && genP_Status < 10){

      // Fill histos
      hAllGenMuonsPt ->Fill(genP_Pt);
      hAllGenMuonsEta->Fill(genP_Eta);

      // Acceptance cuts
      if(genP_Pt >= cfg_MuPtCutMin && std::abs(genP_Eta) < cfg_MuEtaCutMax){

	nGenMuons++;
	v_leptonPt.push_back(genP_Pt);

	// Fill histos
	hPassedGenMuonsPt ->Fill(genP_Pt);
	hPassedGenMuonsEta->Fill(genP_Eta);
      }
    }// Muons
    if(nGenMuons == 0) continue;
    
    // b-jets
    if(std::abs(genP_PdgId) == 5){

      // Fill histos
      hAllGenBjetsPt ->Fill(genP_Pt);
      hAllGenBjetsEta->Fill(genP_Eta);
      
      // Acceptance cuts
      if(genP_Pt >= cfg_BjetPtCutMin && std::abs(genP_Eta) < cfg_BjetEtaCutMax){
	nGenBjets++;
	
	// Fill histos
	hPassedGenBjetsPt ->Fill(genP_Pt);
	hPassedGenBjetsEta->Fill(genP_Eta);       
      }
    }// b-jets
    if(nGenBjets == 0) continue;
    
  }// GenParticles
  
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
  }

  // Increment Counters    
  cAllEvents.increment();
  if (nGenElectrons > 0) cElectrons.increment();
  if (nGenMuons > 0) cMuons.increment();
  if (nGenBjets > 0) cBjets.increment();
  if (bPassTrg) cTrigger.increment();
  // attikis */ 

  return;
}
