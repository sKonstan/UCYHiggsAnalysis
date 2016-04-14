// -*- c++ -*-
#include "Framework/interface/BaseSelector.h"
#include "Framework/interface/makeTH.h"

#include "EventSelection/interface/CommonPlots.h"
#include "EventSelection/interface/EventSelections.h"

#include "TDirectory.h"
#include <algorithm>
#include <TLorentzVector.h>
#include "Tools/interface/MCTools.h"
#include <cmath>
class SignalAnalysis: public BaseSelector {
public:
  explicit SignalAnalysis(const ParameterSet& config);
  virtual ~SignalAnalysis() {}

  struct particles{
    std::vector<double> Energy;
    std::vector<double> Phi;
    std::vector<double> Eta;
    std::vector<double> Pt;
    std::vector<int> Id;
    std::vector<int> Index;
    std::vector<int> Mo1;
    std::vector<int> Mo2;
  };

  /// Books histograms
  virtual void book(TDirectory *dir) override;
  /// Sets up branches for reading the TTree
  virtual void setupBranches(BranchManager& branchManager) override;
  /// Called for each event
  virtual void process(Long64_t entry) override;
  std::vector <double> DVectorSorting (std::vector <double> myvector);
  int MLepMode (std::vector <int> vector1,std::vector <int> vector2);
 
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
  const double PT_MAX  = 500.0;
  const int PT_BINS    =  100;  //50                                                                           
  const double ETA_MAX =   3.0;
  const int ETA_BINS   =  30;
  int count=0;
   
  // Histograms
  WrappedTH1* hExample;
  WrappedTH1* hAllMLepPt_op;
  WrappedTH1* hAllMLepNJets_op;
  WrappedTH1* hAllMLepJpt_op;
  WrappedTH1* hPassedMLepNJets_op;
  WrappedTH1* hAllMLepEta_op;
  WrappedTH1* hAllMLepJEta_op;
  WrappedTH2* histo;
  WrappedTH1* hAllMET;
  WrappedTH1* hMLepMET;
  WrappedTH1* hAllMLepPt_same;
  WrappedTH1* hAllMLepNJets_same;
  WrappedTH1* hAllMLepJpt_same;
  WrappedTH1* hPassedMLepNJets_same;
  WrappedTH1* hAllMLepEta_same;
  WrappedTH1* hAllMLepJEta_same;
  WrappedTH1* hNMultiLep;
  WrappedTH1* hNMultiLepOp;
  WrappedTH1* hNMultiLepOpPassed;
  WrappedTH1* hPassedMLepJpt_op;
  WrappedTH1* hPassedMLepJpt_same;
  WrappedTH1* hAllMLepleadLepPt_same;
  WrappedTH1* hAllMLepsubleadLepPt_same;
  WrappedTH1* hAllMLepleadLepPt_op;
  WrappedTH1* hAllMLepsubleadLepPt_op;
  WrappedTH1* hAllMLepNLep_op;
  WrappedTH1* hAllMLepNLep_same;
  WrappedTH1* hgoodlep;
  WrappedTH1* hnumlep;
  WrappedTH1* hBotPt;
  WrappedTH1* hAllMLepNBotToLep_op;
  WrappedTH1* hAllMLepNBotToLep_same;
  WrappedTH1* hWJ62Pt;
  WrappedTH1* hPassedMLepNLep_op;
  WrappedTH1* hPassedMLepNLep_same;
  WrappedTH1* hPassedMLepPt_op;
  WrappedTH1* hPassedMLepPt_same;

  WrappedTH1* hJets_DEne;
  WrappedTH1* hJets_DR;
  WrappedTH1* hJets_DPhi;
  WrappedTH1* hJets_DEta;
  
  WrappedTH1* hGenJ_Pt;
  WrappedTH1* hLepImpPar;
  WrappedTH1* hJets_DEne_lt10;
  WrappedTH1* hJets_DEne_10_25;
  WrappedTH1* hJets_DEne_25_40;
  WrappedTH1* hJets_DEne_40_55;
  WrappedTH1* hJets_DEne_55_70;
  WrappedTH1* hJets_DEne_70_85;
  WrappedTH1* hJets_DEne_85_100;
  WrappedTH1* hJets_DEne_gt100;

  WrappedTH1* hMETcut;
  WrappedTH1* hNJets_cut;
  WrappedTH1* hLep1Pt_cut;
  WrappedTH1* hLep2Pt_cut;
  WrappedTH1* hPassedEvents;
  WrappedTH2* hLepMode;

  WrappedTH1* hMVA_EleFromW;
  WrappedTH1* hMVA_EleFromBot;
  WrappedTH1* hMVA_EleFake;
  WrappedTH1* hLeadLepPt;
  WrappedTH1* hSubleadLepPt;
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
  hAllMLepPt_op = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "AllMLepPt_op" , "All NLep>2 - opposite sign Pt p_{T}, GeVc^{-1}:N_{jets}", PT_BINS, 0, PT_MAX);
  hAllMLepNJets_op = fHistoWrapper.makeTH<TH1I>(HistoLevel::kVital, dir, "AllMLepNJets_op" , "All NLep>2 - opposite sign Numb of jets", 50, 0, 50);
  hAllMLepJpt_op = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "AllMLepJPt_op" , "All NLep>2 - opposite sign Jets_pt Pt p_{T}, GeVc^{-1}:N_{jets}", PT_BINS, 0, PT_MAX);
  hPassedMLepNJets_op = fHistoWrapper.makeTH<TH1I>(HistoLevel::kVital, dir, "PassedMLepNJets_op" , "Passed NMep>2 Numb of jets", 20, 0, 20);
  hAllMLepEta_op= fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "AllMLepEta_op"    , "All Nlep>2 - opposite sign:Lep #eta:N_{jets}"    , ETA_BINS, -ETA_MAX, ETA_MAX);

  hAllMLepJEta_op = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "AllMLepJEta_op"    , "All Nlep>2 - opposite sign:Jet #eta:N_{jets}"    , ETA_BINS, -ETA_MAX, ETA_MAX);

  histo   = fHistoWrapper.makeTH<TH2F>(HistoLevel::kVital, dir, "MuEl" , "MuEl", 4, -2, 2, 4,-2,2);
  hAllMET     = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "AllMET" , "AllMET:Jet p_{T}, GeV:N_{jets}", PT_BINS*3, 0, PT_MAX*3);
  hMLepMET     = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "MLepMET" , "MLepMET:Jet p_{T}, GeV:N_{jets}", PT_BINS*3, 0, PT_MAX*3);

  hAllMLepPt_same = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "AllMLepPt_same" , "All NLep>2 - same sign Pt p_{T}, GeVc^{-1}:N_{jets}", PT_BINS, 0, PT_MAX);
  hAllMLepNJets_same = fHistoWrapper.makeTH<TH1I>(HistoLevel::kVital, dir, "AllMLepNJets_same" , "All NLep>2 - same sign Numb of jets", 50, 0, 50);
  hAllMLepJpt_same = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "AllMLepJPt_same" , "All NLep>2 - same sign Jets_pt Pt p_{T}, GeVc^{-1}:N_{jets}", PT_BINS, 0, PT_MAX);
  hPassedMLepNJets_same = fHistoWrapper.makeTH<TH1I>(HistoLevel::kVital, dir, "PassedMLepNJets_same" , "Passed NMep>2 Numb of jets", 20, 0, 20);
  hAllMLepEta_same= fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "AllMLepEta_same"    , "All Nlep>2 - same sign:Lep #eta:N_{jets}"    , ETA_BINS, -ETA_MAX, ETA_MAX);

  hAllMLepJEta_same = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "AllMLepJEta_same"    , "All Nlep>2 - same sign:Jet #eta:N_{jets}"    , ETA_BINS, -ETA_MAX, ETA_MAX);

  hNMultiLep= fHistoWrapper.makeTH<TH1I>(HistoLevel::kVital, dir, "NMultiLep" , "NMep>2 Numb of Events", 2, 0.5, 2.5);
  hgoodlep=fHistoWrapper.makeTH<TH1I>(HistoLevel::kVital, dir, "goodlep" , "NMep>2 lPt>10,5 Numb of Events", 2, 0.5, 2.5);
  hNMultiLepOp= fHistoWrapper.makeTH<TH1I>(HistoLevel::kVital, dir, "NMultiLepOp" , "NMep>2 Numb of Events opp sign", 2, 0.5, 2.5);
  hNMultiLepOpPassed = fHistoWrapper.makeTH<TH1I>(HistoLevel::kVital, dir, "NMultiLepOpPassed" , "NMep>2 Numb of Events opp sign - Passed", 2, 0.5, 2.5);
  hPassedMLepJpt_op= fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "PassedMLepJPt_op" , "Passed NLep>2 - opposite sign Jets_pt Pt p_{T}, GeVc^{-1}:N_{jets}", PT_BINS, 0, PT_MAX);
  hPassedMLepJpt_same= fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "PassedMLepJPt_same" , "Passed NLep>2 - same sign Jets_pt Pt p_{T}, GeVc^{-1}:N_{jets}", PT_BINS, 0, PT_MAX);
  hAllMLepleadLepPt_same= fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "AllMLepleadLepPt_same" , "All NLep>2 - same sign leading lep  Pt p_{T}, GeVc^{-1}:N_{jets}", PT_BINS, 0, PT_MAX);
  hAllMLepsubleadLepPt_same= fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "AllMLepsubleadLepPt_same" , "All NLep>2 - same sign subl lep Pt p_{T}, GeVc^{-1}:N_{jets}", PT_BINS, 0, PT_MAX);
  hAllMLepleadLepPt_op= fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "AllMLepleadLepPt_op" , "All NLep>2 - opposite sign leading lep  Pt p_{T}, GeVc^{-1}:N_{jets}", PT_BINS, 0, PT_MAX);
  hAllMLepsubleadLepPt_op= fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "AllMLepsubleadLepPt_opposite" , "All NLep>2 - opposite sign subl lep Pt p_{T}, GeVc^{-1}:N_{jets}", PT_BINS, 0, PT_MAX);
  hAllMLepNLep_op= fHistoWrapper.makeTH<TH1I>(HistoLevel::kVital, dir, "AllMLepNLep_op" , "All NMep>2 Numb of leptons op. sign", 10, 0, 10);
  hAllMLepNLep_same = fHistoWrapper.makeTH<TH1I>(HistoLevel::kVital, dir, "AllMLepNLep_same" , "All NMep>2 Numb of leptons same sign", 10, 0, 10);
  hnumlep = fHistoWrapper.makeTH<TH1I>(HistoLevel::kVital, dir, "numlep" , "All Nlep", 11, -0.5, 10.5);
  //                                                                                                                                                                                                                     
  hBotPt=fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "AllBotPt" , "All Bot Pt p_{T}, GeVc^{-1}:N_{jets}", PT_BINS, 0, PT_MAX);
  hAllMLepNBotToLep_op=fHistoWrapper.makeTH<TH1I>(HistoLevel::kVital, dir, "AllMLepNBotToLep_op" , "All NMep>2 Numb of bot toleptons op. sign", 10, 0, 10);
  hAllMLepNBotToLep_same=fHistoWrapper.makeTH<TH1I>(HistoLevel::kVital, dir, "AllMLepNBotToLep_same" , "All NMep>2 Numb of bot toleptons same sign", 10, 0, 10);
  hWJ62Pt= fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "W62Pt" , "W status=62 Pt p_{T}, GeVc^{-1}:N_{jets}", PT_BINS, 0, PT_MAX);

  hPassedMLepNLep_op= fHistoWrapper.makeTH<TH1I>(HistoLevel::kVital, dir, "PassedMLepNLep_op" , "Passed NMep>2 Numb of leptons op. sign", 10, 0, 10);
  hPassedMLepNLep_same= fHistoWrapper.makeTH<TH1I>(HistoLevel::kVital, dir, "PassedMLepNLep_same" , "Passed NMep>2 Numb of leptons same sign", 10, 0, 10);
  hPassedMLepPt_op = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "PassedMLepPt_op" , "Passed NLep>2 - opposite sign Pt p_{T}, GeVc^{-1}:N_{jets}", PT_BINS, 0, PT_MAX);
  hPassedMLepPt_same = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "PassedMLepPt_same" , "Passed NLep>2 - same sign Pt p_{T}, GeVc^{-1}:N_{jets}", PT_BINS, 0, PT_MAX);

  hJets_DEne= fHistoWrapper.makeTH<TH1I>(HistoLevel::kVital, dir, "Jets_DEne", "Jets_DEne", 100,-50,50);
  hJets_DEta= fHistoWrapper.makeTH<TH1I>(HistoLevel::kVital, dir, "Jets_DEta", "Jets_DEta",20,-0.1,0.1);
  hJets_DPhi= fHistoWrapper.makeTH<TH1I>(HistoLevel::kVital, dir, "Jets_DPhi", "Jets_DPhi",20,-0.1, 0.1);
  hJets_DR= fHistoWrapper.makeTH<TH1I>(HistoLevel::kVital, dir, "Jets_DR", "Jets_DR",10,0, 0.1);

  hGenJ_Pt = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "GenJ_Pt" , "GenJ Pt p_{T}, GeVc^{-1}:N_{jets}", PT_BINS, 0, PT_MAX);
  hLepImpPar = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "LepImpPar", "LepImpPar",50,0,0.2);
  hJets_DEne_lt10= fHistoWrapper.makeTH<TH1I>(HistoLevel::kVital, dir, "Jets_DEne_lt10", "Jets_DEne_lt10", 100,-50,50);
  hJets_DEne_10_25= fHistoWrapper.makeTH<TH1I>(HistoLevel::kVital, dir, "Jets_DEne_10_25", "Jets_DEne_10_25", 100,-50,50);
  hJets_DEne_25_40= fHistoWrapper.makeTH<TH1I>(HistoLevel::kVital, dir, "Jets_DEne_25_40", "Jets_DEne_25_40", 100,-50,50);
  hJets_DEne_40_55= fHistoWrapper.makeTH<TH1I>(HistoLevel::kVital, dir, "Jets_DEne_40_55", "Jets_DEne_40_55", 100,-50,50);
  hJets_DEne_55_70= fHistoWrapper.makeTH<TH1I>(HistoLevel::kVital, dir, "Jets_DEne_55_70", "Jets_DEne_55_70", 100,-50,50);
  hJets_DEne_70_85= fHistoWrapper.makeTH<TH1I>(HistoLevel::kVital, dir, "Jets_DEne_70_85", "Jets_DEne_70_85", 100,-50,50);
  hJets_DEne_85_100= fHistoWrapper.makeTH<TH1I>(HistoLevel::kVital, dir, "Jets_DEne_85_100", "Jets_DEne_85_100", 100,-50,50);
  hJets_DEne_gt100= fHistoWrapper.makeTH<TH1I>(HistoLevel::kVital, dir, "Jets_DEne_gt100", "Jets_DEne_gt100", 100,-50,50);
  
  hMETcut=fHistoWrapper.makeTH<TH1D>(HistoLevel::kVital, dir, "METcut", "METcut", 100,0,100);
  hNJets_cut=fHistoWrapper.makeTH<TH1I>(HistoLevel::kVital, dir, "NJets_cut", "NJets_cut",11,2,13);
  hLep1Pt_cut=fHistoWrapper.makeTH<TH1D>(HistoLevel::kVital, dir, "Lep1Pt_cut", "Lep1Pt_cut",60,0,60);
  hLep2Pt_cut=fHistoWrapper.makeTH<TH1D>(HistoLevel::kVital, dir, "Lep2Pt_cut", "Lep2Pt_cut",60,0,60);
  hPassedEvents = fHistoWrapper.makeTH<TH1I>(HistoLevel::kVital, dir, "PassedEvents", "PassedEvents", 5,0,5);
  hLepMode= fHistoWrapper.makeTH<TH2I>(HistoLevel::kVital, dir, "LepMode","LepMode", 4,0,4,4,0,4);

  hMVA_EleFromW=fHistoWrapper.makeTH<TH1D>(HistoLevel::kVital, dir, "MVA_EleFromW", "MVA_EleFromW", 2,-0.5,1.5);
  hMVA_EleFromBot=fHistoWrapper.makeTH<TH1D>(HistoLevel::kVital, dir, "MVA_EleFromBot", "MVA_EleFromBot", 2,-0.5,1.5);
  hMVA_EleFake=fHistoWrapper.makeTH<TH1D>(HistoLevel::kVital, dir, "MVA_EleFake", "MVA_EleFake", 2,-0.5,1.5);
  hLeadLepPt= fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "AllMLepLeadLepPt" , "All NLep>2 - leading lep  Pt p_{T}, GeVc^{-1}:N_{jets}", PT_BINS, 0, PT_MAX);
  hSubleadLepPt= fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "AllMLepSubleadLepPt" , "All NLep>2 - subleading lep  Pt p_{T}, GeVc^{-1}:N_{jets}", PT_BINS, 0, PT_MAX);
  return;
}


void SignalAnalysis::setupBranches(BranchManager& branchManager) {
  fEvent.setupBranches(branchManager);

  return;
}

//___________________Vector Sorting______________________________//                                            
std::vector <double> SignalAnalysis:: DVectorSorting (std::vector <double> myvector)
{
  Int_t n=myvector.size();
  for (Int_t m=0; m<(n-1); m++){
    for (Int_t k=m+1; k<n;k++){
      if (myvector.at(m)>myvector.at(k)){
        Double_t temp=myvector.at(m);
        myvector.at(m)=myvector.at(k);
        myvector.at(k)=temp;
      }
    }
  }
  return myvector;
}

//_____________________MLepMode_______________________________                                                 
int SignalAnalysis:: MLepMode (std::vector <int> vector1,std::vector <int> vector2)
{
  bool qcheck=true;
  int nsize=vector2.size();
  int res;
  for (int i=0; i<nsize; i++){
    if (vector1.at(0)*vector2.at(i)/(std::abs(vector1.at(0)*vector2.at(i))) < 0){
      qcheck=false;
      res=vector2.at(i)/std::abs(vector2.at(i));
      continue;
    }
  }
  if (qcheck) res=vector2.at(0)/std::abs(vector2.at(0));
  return res;
}


void SignalAnalysis::process(Long64_t entry) {
  //std::cout<<"=================================="<<std::endl;
  //====== Initialize
  cAllEvents.increment();
  int nBotToLep=0;
  if( !fEvent.isMC() ) return;

  //std::cout<<count<<std::endl;
  count++;
  int nmlep=0;
  TLorentzVector MET;
  particles Electrons;
  particles Muons;
  particles GJets, Jets;
  particles BotToLep;
  particles Leptons;
  //  MET.Clear();
  // Variable declaration
  Size_t nGenParticles = 0;
  size_t nGenMuons     = 0; 
  //size_t nGenElectrons = 0; 
  int nElectrons=0; 
  //int genP_Index=-1;                                                                                                                                                                                                 
  MCTools mcTools(fEvent);
  TLorentzVector Wp4;
  Wp4.Clear();
  for( auto gen : fEvent.genparticles() ){

    // genP_Index++; 
    // if (genP_Index == 0) {
    //   mcTools.PrintGenParticle(genP_Index, true);                                           
    // } 
    // else{ 
    //   mcTools.PrintGenParticle(genP_Index, false);                                                                                                                                
    // }
    
    // /////////                                                                                                                                                         
    nGenParticles++;
    int genP_PdgId       = gen.pdgId();
    double genP_Pt       = gen.pt();
    double genP_Eta      = gen.eta();
    double genP_Status   = gen.status(); // PYTHIA8: http://home.thep.lu.se/~torbjorn/pythia81html/ParticleProperties.html         
    int index            = gen.index();
    double genP_E        = gen.e();
    double genP_Phi      =gen.phi();
    
   
    if (((std::abs(genP_PdgId)==12)||(std::abs(genP_PdgId)==14)||(std::abs(genP_PdgId)==16)) && genP_Status==1) {
      TLorentzVector p4;
      p4.SetPtEtaPhiE(genP_Pt,genP_Eta,genP_Phi,genP_E);
      MET+=p4;
    }
    
    if (std::abs(genP_PdgId)==24 && genP_Status==62) Wp4=mcTools.GetP4(index);
    // Electrons                                                                                                                                                                                                     
    
    if(std::abs(genP_PdgId) == 11 && genP_Status==1){                                                                                                                                                           
      int motherPos=mcTools.LepMotherPosition(index);
      
      if (motherPos!=-1){ 

	int imom;
	double d0;
	//	for (int i=0; i<nLeptons; i++){
	int iLep=index;
	GenParticle lepton=mcTools.GetGenP(iLep);
	imom=mcTools.ImmediateMoPosition(iLep);
	GenParticle mo=mcTools.GetGenP(imom);
	// Find d0 
	double VprX=mo.vertexX();
	double VprY=mo.vertexY();
	double VsecX=lepton.vertexX();
	double VsecY=lepton.vertexY();
	double Lxy=sqrt((VsecX-VprX)*(VsecX-VprX)+(VsecY-VprY)*(VsecY-VprY));
	double dPhi=lepton.phi()-mo.phi();	
	d0=Lxy*abs(sin(dPhi));
	hLepImpPar->Fill(d0);
	//hLepImpPar->Fill(d0);
	if (d0<0.1){
	  nElectrons++;
	  Electrons.Energy.push_back(genP_E);
	  Electrons.Phi.push_back(genP_Phi);
	  Electrons.Eta.push_back(genP_Eta);
	  Electrons.Pt.push_back(genP_Pt);
	  Electrons.Id.push_back(genP_PdgId);
	  Electrons.Index.push_back(index);

	  Leptons.Energy.push_back(genP_E);
	  Leptons.Phi.push_back(genP_Phi);
	  Leptons.Eta.push_back(genP_Eta);
	  Leptons.Pt.push_back(genP_Pt);
	  Leptons.Id.push_back(genP_PdgId);
	  Leptons.Index.push_back(index);
	}                                                                                                           
      }
    }
  
    if(std::abs(genP_PdgId) == 13 && genP_Status==1){
      int motherPos=mcTools.LepMotherPosition(index);
      if (motherPos!=-1){
        //if (motherPos!=4) std::cout<<motherPos<<endl;                                                                                                                                                                 
        nGenMuons++;

	int imom;
	double d0;
	//	for (int i=0; i<nLeptons; i++){
	int iLep=index;
	GenParticle lepton=mcTools.GetGenP(iLep);
	imom=mcTools.ImmediateMoPosition(iLep);
	GenParticle mo=mcTools.GetGenP(imom);
	// Find d0 
	double VprX=mo.vertexX();
	double VprY=mo.vertexY();
	
	double VsecX=lepton.vertexX();
	double VsecY=lepton.vertexY();
	
	double Lxy=sqrt((VsecX-VprX)*(VsecX-VprX)+(VsecY-VprY)*(VsecY-VprY));
	double dPhi=lepton.phi()-mo.phi();
	
	d0=Lxy*abs(sin(dPhi));
	hLepImpPar->Fill(d0);
	
	//hLepImpPar->Fill(d0);
	if (d0<0.1){
	  
	  Muons.Energy.push_back(genP_E);
	  Muons.Phi.push_back(genP_Phi);
	  Muons.Eta.push_back(genP_Eta);
	  Muons.Pt.push_back(genP_Pt);
	  Muons.Id.push_back(genP_PdgId);
	  Muons.Index.push_back(index);
	  
	  Leptons.Energy.push_back(genP_E);
	  Leptons.Phi.push_back(genP_Phi);
	  Leptons.Eta.push_back(genP_Eta);
	  Leptons.Pt.push_back(genP_Pt);
	  Leptons.Id.push_back(genP_PdgId);
	  Leptons.Index.push_back(index);
	}
      }
    }
    
    if  (((std::abs(genP_PdgId)==11) || (std::abs(genP_PdgId)==13)) && genP_Status==1) {
      bool qBotToLep=mcTools.LookForMotherId(index,5,false);       //  bool qBotToLep=mcTools.RecursivelyLookForMotherId(index,5,false);                                                                                
      if ((!qBotToLep)&&(mcTools.LookForMotherId(index,4,false))){
        int iCharm=mcTools.GetPosOfMotherId(index,4,false);
        if ((iCharm!=-1)&&(mcTools.LookForMotherId(iCharm,5,false))) qBotToLep=true;
      }
  
      if (qBotToLep){
	int imom;
	double d0;
	//	for (int i=0; i<nLeptons; i++){
	int iLep=index;
	GenParticle lepton=mcTools.GetGenP(iLep);
	imom=mcTools.ImmediateMoPosition(iLep);
	GenParticle mo=mcTools.GetGenP(imom);
	// Find d0 
	double VprX=mo.vertexX();
	double VprY=mo.vertexY();
	
	double VsecX=lepton.vertexX();
	double VsecY=lepton.vertexY();
	
	double Lxy=sqrt((VsecX-VprX)*(VsecX-VprX)+(VsecY-VprY)*(VsecY-VprY));
	double dPhi=lepton.phi()-mo.phi();
	
	d0=Lxy*abs(sin(dPhi));
	hLepImpPar->Fill(d0);
	
	//hLepImpPar->Fill(d0);
	if (d0<0.1){
	  
	  
	  nBotToLep++;
	  BotToLep.Energy.push_back(genP_E);
	  BotToLep.Phi.push_back(genP_Phi);
	  BotToLep.Eta.push_back(genP_Eta);
	  BotToLep.Pt.push_back(genP_Pt);
	  BotToLep.Id.push_back(genP_PdgId);
	  BotToLep.Index.push_back(index);
	}
      }
    }
  
  }// for( auto& gen : fEvent.genparticles().getAllGenpCollection() ){                                                                                                                                                 
  hAllMET->Fill(MET.Et());                             
  ///Jets                                   
  int iGJets=0;
  for(GenJet genj : fEvent.genjets()){
    double genJ_Pt=genj.pt();
    double genJ_Eta=genj.eta();
    double genJ_E=genj.e();
    double genJ_Phi=genj.phi();
    
    hGenJ_Pt->Fill(genJ_Pt);
    GJets.Pt.push_back(genJ_Pt);
    GJets.Eta.push_back(genJ_Eta);
    GJets.Phi.push_back(genj.phi());
    if (genJ_Pt > 25 && std::abs(genJ_Eta) < 2.5) iGJets++;
    for(Jet jet : fEvent.jets_pfchs()){
      //double Jet_Pt=jet.pt();                                                                                                                                                                                         
      double Jet_Eta=jet.eta();
      double Jet_E=jet.e();
      double Jet_Phi=jet.phi();

      double DPhiJ=(genJ_Phi-Jet_Phi);
      double DEtaJ=(genJ_Eta-Jet_Eta);
      double DEneJ=(genJ_E-Jet_E);
      double DRJ=sqrt(DPhiJ*DPhiJ+DEtaJ*DEtaJ);
      if (DRJ<0.1){
        hJets_DPhi->Fill(DPhiJ);
        hJets_DEta->Fill(DEtaJ);
        hJets_DR->Fill(DRJ);
        hJets_DEne->Fill(DEneJ);
	if (genJ_Pt<10) hJets_DEne_lt10->Fill(DEneJ);
	else if (genJ_Pt<25) hJets_DEne_10_25->Fill(DEneJ);
	else if (genJ_Pt<40) hJets_DEne_25_40->Fill(DEneJ);
	else if (genJ_Pt<55) hJets_DEne_40_55->Fill(DEneJ);
	else if (genJ_Pt<70) hJets_DEne_55_70->Fill(DEneJ);
	else if (genJ_Pt<85) hJets_DEne_70_85->Fill(DEneJ);
	else if (genJ_Pt<100) hJets_DEne_85_100->Fill(DEneJ);
	else hJets_DEne_gt100->Fill(DEneJ);
      }
    }
  }



   int nLeptons=Leptons.Pt.size();
   
   //--------------------------------------------------------------------------------------------------------//
   //.............................................Multilep Events............................................//                                                                                                              
   
   int sign=0;
   int nGJets=GJets.Pt.size();
   nLeptons=Leptons.Pt.size();
   hnumlep->Fill(nLeptons);
   std::vector <int> PosLep, NegLep, GoodOpLeptons, GoodSameLeptons_pos, GoodSameLeptons_neg;
   PosLep.clear();
   NegLep.clear();
   GoodOpLeptons.clear();
   GoodSameLeptons_pos.clear();
   GoodSameLeptons_neg.clear();

 
   //..........................................Problem WJets Events.........................................//
   /*bool first=true;
   for( auto gen : fEvent.genparticles() ){
     if ((nLeptons)>=2){
       bool problem=false;
       int ndaughters   =  gen.daughters().size();                               
       for (int k=0; k<ndaughters; k++){
	 int idau=gen.daughters().at(k);
	 GenParticle dau=mcTools.GetGenP(idau);
	 if ((std::abs(gen.pdgId())==12)||(std::abs(gen.pdgId())==14)||(std::abs(gen.pdgId())==16)) {
	   if (dau.pdgId() == gen.pdgId() && std::abs(dau.e()-gen.e())>10 ) std::cout<< cAllEvents.value() << std::endl; //problem=true;
	 }
       }
       
       genP_Index++;
       long int numEvent=cAllEvents.value();
       if ( numEvent==12395 ){   
	 if (genP_Index == 0) { 
	   if (first) {
	     std::cout<<" "<<endl;
	     std::cout<<"Event "<<cAllEvents.value()<<std::endl;
	     first =false;
	   }
	   mcTools.PrintEvent(genP_Index, true);
	 }
	 else{ 
	   cout << "\n " << endl; 
	   mcTools.PrintEvent(genP_Index, false);
	 }
       }
       
     }
     }  */

   
   
   bool qGoodLep=false;     
   if ((nLeptons)>=2){
     nmlep++;
   
     hNMultiLep->Fill(1);
   
     hMLepMET->Fill(MET.Et());  
     vector <double> tempP4;
     tempP4.clear();

     //..........................................Find the sign of the Leptons...................................//                                                                 
     for (int i=0; i<nLeptons; i++){
       tempP4.push_back(Leptons.Pt.at(i));
       sign+=Leptons.Id.at(i)/std::abs(Leptons.Id.at(i));
       if ( Leptons.Id.at(i)/std::abs(Leptons.Id.at(i)) > 0 ){
        PosLep.push_back(i);
       }
       else {
	 NegLep.push_back(i);
       }
     }
     tempP4=DVectorSorting(tempP4);
     
     bool qSameSign=false, qOpSign=false;  //Only same/opposite sign leptons       
     
     if (std::abs(sign)==(nLeptons)) qSameSign=true;
     
     int nPos=PosLep.size();
     int nNeg=NegLep.size();
     std:: vector <int> SameSLep;
     
     SameSLep.clear();
     if (PosLep.size()>1){
       for (int i=0; i<nPos; i++){
	 SameSLep.push_back(PosLep.at(i));
       }
     }
     if (NegLep.size()>1){
       for (int i=0; i<nNeg; i++){
	 SameSLep.push_back(NegLep.at(i));
       }
     }
     int nSameSLep=SameSLep.size();
     if (nSameSLep<2) qOpSign=true;
     
     vector <double> tempOpP4;
     tempOpP4.clear();
     vector <double> tempSameP4;
     tempSameP4.clear();
     //......................................................................................................//  
     double METcut=0;
     for (int j=0; j<100; j++){
       if (MET.Et() > METcut) hMETcut->Fill(METcut);
       METcut=METcut+1.;
     }
     int NJets_cut=2;
     for (int j=2; j<13; j++){
       if (iGJets > NJets_cut) hNJets_cut->Fill(NJets_cut);
       NJets_cut=NJets_cut+1;
     }

     double Lep1Pt_cut=0;
     double Lep2Pt_cut=0;
       
     for (int j=0; j<60; j++){
       if (tempP4.at(nLeptons-1) > Lep1Pt_cut) hLep1Pt_cut->Fill(Lep1Pt_cut);
       if (tempP4.at(nLeptons-2) > Lep2Pt_cut) hLep2Pt_cut->Fill(Lep2Pt_cut);
       Lep1Pt_cut++;
       Lep2Pt_cut++;
     }     
     hLeadLepPt->Fill(tempP4.at(nLeptons-1));
     hSubleadLepPt->Fill(tempP4.at(nLeptons-2));
  
     
     //======================================Opposite sign leptons ==========================================//                                                                                                                                                                                          
     if (!qSameSign) {
       hAllMLepNLep_op->Fill(nLeptons);
       hNMultiLepOp->Fill(1);
       hAllMLepNJets_op->Fill(iGJets);  //Number of All jets                                                                                                                                                            
       
       
       for (int k=0; k<nLeptons; k++){
	 tempOpP4.push_back(Leptons.Pt.at(k));
	 hAllMLepPt_op->Fill(Leptons.Pt.at(k));
	 hAllMLepEta_op->Fill(Leptons.Eta.at(k));
       }
       
       tempOpP4=DVectorSorting(tempOpP4);
       
       int ngoodLep=0;
       if (tempOpP4.at(nLeptons-1) > 10 && tempOpP4.at(nLeptons-2) > 7){
	 for (int k=0;k<nLeptons; k++){
	   if (std::abs(Leptons.Eta.at(k)) < 2.4) {
	     ngoodLep++;
	   
	     GoodOpLeptons.push_back(k);
	   }
	 }
	 if (ngoodLep>=2) {
	   hPassedMLepNLep_op->Fill(ngoodLep);
	   qGoodLep=true;
	 }
       }
       
     }
     //___________________________________________________________________________________________________//    
     //===================================Same sign leptons===============================================//                                                                                                                                                                                                 
     if (!qOpSign) {
       if (PosLep.size()>1) hAllMLepNLep_same->Fill(PosLep.size());
       if (NegLep.size()>1) hAllMLepNLep_same->Fill(NegLep.size());
       hAllMLepNJets_same->Fill(iGJets);  //Number of All jets                                                                                                                                                          
       
       for (int k=0; k<nSameSLep; k++){
	 tempSameP4.push_back(Leptons.Pt.at(SameSLep.at(k)));
	 hAllMLepPt_same->Fill(Leptons.Pt.at(SameSLep.at(k)));
	 hAllMLepEta_same->Fill(Leptons.Eta.at(SameSLep.at(k)));
       }
       tempSameP4=DVectorSorting(tempSameP4);
       
       int ngoodLep=0;
       if (tempSameP4.at(nSameSLep-1) > 10 && tempSameP4.at(nSameSLep-2) > 7 ){
	 for (int k=0;k<nSameSLep; k++){
	   if (std::abs(Leptons.Eta.at(SameSLep.at(k))) < 2.4) {
	     ngoodLep++;
	     if (Leptons.Id.at(SameSLep.at(k))< 0) GoodSameLeptons_pos.push_back(SameSLep.at(k));
	     if (Leptons.Id.at(SameSLep.at(k))> 0) GoodSameLeptons_neg.push_back(SameSLep.at(k));
	   }
	 }
	 int nGoodSameLeptons_pos=GoodSameLeptons_pos.size();
	 int nGoodSameLeptons_neg=GoodSameLeptons_neg.size();
	 if (nGoodSameLeptons_pos >=2 ) {
	   hPassedMLepNLep_same->Fill(nGoodSameLeptons_pos);
	   qGoodLep=true;
	 }
	 if (nGoodSameLeptons_neg >=2 ) {
	   hPassedMLepNLep_same->Fill(nGoodSameLeptons_neg);
	   qGoodLep=true;
	 }
       }
     }

     //.....................................JETS........................................          
     //int iGJets=0;
     for (int k=0; k<nGJets; k++){
       //if ((GJets.Pt.at(k)>25)&&(std::abs(GJets.Eta.at(k))<2.4)) iGJets++;
       if (!qSameSign){
	 hAllMLepJpt_op->Fill(GJets.Pt.at(k));
	 hAllMLepJEta_op->Fill(GJets.Eta.at(k));
       }
       if (!qOpSign){
	 hAllMLepJpt_same->Fill(GJets.Pt.at(k));
	 hAllMLepJEta_same->Fill(GJets.Eta.at(k));
       }
     }
     if (!qOpSign){
       //hPassedMLepNGJets_same->Fill(iGJets);
       hAllMLepleadLepPt_same->Fill(tempSameP4.at(nSameSLep-1));
       hAllMLepsubleadLepPt_same->Fill(tempSameP4.at(nSameSLep-2));
       hAllMLepNBotToLep_same->Fill(nBotToLep);
     }
     if (!qSameSign){
       //hPassedMLepNGJets_op->Fill(iGJets);
       hAllMLepleadLepPt_op->Fill(tempOpP4.at(nLeptons-1));
       hAllMLepsubleadLepPt_op->Fill(tempOpP4.at(nLeptons-2));
       hAllMLepNBotToLep_op->Fill(nBotToLep);
     }
     
     const char *x[7] = {"mu+"," ","e+"," ","e-"," ","mu-"};
     hLepMode->Fill(x[0],x[0],0);
     hLepMode->Fill(x[2],x[2],0);
     hLepMode->Fill(x[4],x[4],0);

     for (int j=0; j<nLeptons-1; j++){
       for (int i=j+1; i<nLeptons; i++){
	 int id1=Leptons.Id.at(j);
	 int id2=Leptons.Id.at(i);
	 id1=id1*(abs(id1)-10)/abs(id1);
	 id2=id2*(abs(id2)-10)/abs(id2);
	 if (id1!=id2){
	   int mini=min(id1,id2);
	   int maxi=max(id1,id2);
	   id1=mini;
	   id2=maxi;
	 }
	 
	 hLepMode->Fill(x[3+id1],x[3+id2],1);
       }
     }
     
     for(Electron elec : fEvent.electrons()){
       double Ele_phi=elec.phi();
       double Ele_eta=elec.eta();
       bool notfound=true;	        
       for (int i=0; i<nElectrons; i++){
	 double genEle_phi=Electrons.Phi.at(i);
	 double genEle_eta=Electrons.Eta.at(i);
	 double genEle_index=Electrons.Index.at(i);
	 double Dphi=(Ele_phi-genEle_phi);
	 double Deta=(Ele_eta-genEle_eta);
	 double dr=sqrt(Dphi*Dphi+Deta*Deta);

	 if (dr<0.1) { //identify the electron
	   notfound=false;
	   if (mcTools.RecursivelyLookForMotherId(genEle_index, 24, false)) {
	     hMVA_EleFromW->Fill(elec.mvaEleID_PHYS14_PU20bx25_nonTrig_V1_wp90());
	     //notfound=false;
	   }
	   if (mcTools.RecursivelyLookForMotherId(genEle_index, 5, false)) {
	     hMVA_EleFromBot->Fill(elec.mvaEleID_PHYS14_PU20bx25_nonTrig_V1_wp90());
	     //notfound=false;
	   }
	  
	 }
	 
       }
       if (notfound) hMVA_EleFake->Fill(elec.mvaEleID_PHYS14_PU20bx25_nonTrig_V1_wp90());
     }
   }
   
   // for(Jet jet : fEvent.jets_pfchs())                                                                                                                                                                                 
   hPassedEvents->Fill("AllEvts",1);
   if (nLeptons>=2) {
     hPassedEvents->Fill("NLep>2",1);
     if (qGoodLep) {
       hPassedEvents->Fill("LepPtEta_cut",1);
       if (iGJets>6) {
	 hPassedEvents->Fill("nJets>4",1);
	 if (MET.Et()>40) hPassedEvents->Fill("MET>40",1);
       }
     }
   }


   
   return;
} //End

     
     
