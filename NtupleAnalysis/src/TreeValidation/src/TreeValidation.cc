// -*- c++ -*-
#include <iomanip> 
#include "Framework/interface/BaseSelector.h"
#include "Framework/interface/makeTH.h"

#include "DataFormat/interface/Event.h"
#include "EventSelection/interface/CommonPlots.h"
#include "EventSelection/interface/EventSelections.h"

#include "TDirectory.h"

using namespace std;

class TreeValidation: public BaseSelector {
public:
  enum BTagPartonType {
    kBTagB,
    kBTagC,
    kBtagG,
    kBtagLight,
  };
  explicit TreeValidation(const ParameterSet& config);
  virtual ~TreeValidation() {}

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
  // AngularCutsCollinear fAngularCutsCollinear;
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
REGISTER_SELECTOR(TreeValidation);

TreeValidation::TreeValidation(const ParameterSet& config)
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
    // fAngularCutsCollinear(config.getParameter<ParameterSet>("AngularCutsCollinear"),
    // 			  fEventCounter, fHistoWrapper, nullptr, ""),
    fBJetSelection(config.getParameter<ParameterSet>("BJetSelection"),
		   fEventCounter, fHistoWrapper, nullptr, ""),
    fMETSelection(config.getParameter<ParameterSet>("METSelection"),
		  fEventCounter, fHistoWrapper, nullptr, ""),
    cSelected(fEventCounter.addCounter("Selected events"))
{ }

void TreeValidation::book(TDirectory *dir) {
  // std::cout << "=== TreeValidation.cc:\n\t TreeValidation::book()" << std::endl;

  // Book histograms in event selection classes
  fTauSelection.bookHistograms(dir);
  fElectronSelection.bookHistograms(dir);
  fMuonSelection.bookHistograms(dir);
  fJetSelection.bookHistograms(dir);
  // fAngularCutsCollinear.bookHistograms(dir);
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


void TreeValidation::setupBranches(BranchManager& branchManager) {
  // std::cout << "=== TreeValidation.cc:\n\t TreeValidation::setupBranches()" << std::endl;
  fEvent.setupBranches(branchManager);

  return;
}


void TreeValidation::process(Long64_t entry) {
  // std::cout << "=== TreeValidation.cc:\n\t TreeValidation::process()" << std::endl;


  // EventID Evt = fEvent.eventID();  // not allowed
  //  std::cout << std::setw(10);
  cout << "\n\n EventInfo_event                  "<<"\tevent()\t                   "<< fEvent.eventID().event() << endl;
  cout << " EventInfo_run\t                      "<<"\trun()\t                     "<< fEvent.eventID().run() << endl;
  cout << " EventInfo_lumi\t                     "<<"\tlumi()\t                    "<< fEvent.eventID().lumi() << endl;
  cout << " EventInfo_prescale                   "<<"\ttrgPrescale()\t             "<< fEvent.eventID().trgPrescale() << endl;
  cout << " EventInfo_nPUvertices\t              "<<"\tnPUvertices()\t             "<< fEvent.eventID().nPUvertices() << endl;
  cout << " EventInfo_NUP\t                      "<<"\tNUP()\t                     "<< fEvent.eventID().NUP() << endl;
  cout << " EventInfo_nGoodOfflineVertices\t     "<<"\tnGoodOfflineVertices()\t    "<< fEvent.eventID().nGoodOfflineVertices() << endl;
  cout << " EventInfo_pvX\t                      "<<"\tpvX()\t                     "<< fEvent.eventID().pvX() << endl;
  cout << " EventInfo_pvY\t                      "<<"\tpvY()\t                     "<< fEvent.eventID().pvY() << endl;
  cout << " EventInfo_pvZ\t                      "<<"\tpvZ()\t                     "<< fEvent.eventID().pvZ() << endl;
  cout << " EventInfo_pvDistanceToNextVertex     "<<"\tpvDistanceToNextVertex()    "<< fEvent.eventID().pvDistanceToNextVertex() << endl;
  cout << " EventInfo_pvDistanceToClosestVertex  "<<"\tpvDistanceToClosestVertex() "<< fEvent.eventID().pvDistanceToClosestVertex() << endl;
  cout << string(100, '=') << endl;
  
  METFilter metfl = fEvent.metFilter();
  cout << "\n" << endl;
  cout << " METFilter_Flag_HBHENoiseFilter\t  " << "\tpassFlag_HBHENoiseFilter()\t     " << metfl.passFlag_HBHENoiseFilter() << endl;
  cout << " METFilter_Flag_HBHENoiseIsoFilter " << "\tpassFlag_HBHENoiseIsoFilter()\t  " << metfl.passFlag_HBHENoiseIsoFilter() << endl;
  cout << " METFilter_Flag_CSCTightHaloFilter " << "\tpassFlag_CSCTightHaloFilter()\t  " << metfl.passFlag_CSCTightHaloFilter() << endl;
  cout << " METFilter_Flag_goodVertices\t     " << "\tpassFlag_goodVertices()\t        " << metfl.passFlag_goodVertices() << endl;
  cout << " METFilter_Flag_eeBadScFilter\t    " << "\tpassFlag_eeBadScFilter()\t       " << metfl.passFlag_eeBadScFilter() << endl;
  cout << " METFilter_hbheNoiseTokenRun2Loose " << "\tpasshbheNoiseTokenRun2Loose()\t  " << metfl.passHbheNoiseTokenRun2Loose() << endl;
  cout << " METFilter_hbheNoiseTokenRun2Tight " << "\tpasshbheNoiseTokenRun2Tight()\t  " << metfl.passHbheNoiseTokenRun2Tight() << endl;
  cout << " METFilter_hbheIsoNoiseToken\t     " << "\tpasshbheIsoNoiseToken()\t        " << metfl.passHbheIsoNoiseToken() << endl;
  cout << string(100, '=') << "\n" << endl;

  Size_t iTau=0;
  for(Tau tau: fEvent.taus()){
      
    if(iTau==0)
      {
	cout<< " Taus_pt                                           "      <<"\tpt()\t                                        "<<tau.pt() << endl;
	cout<< " Taus_eta                                          "      <<"\teta()\t                                        "<<tau.eta() << endl;
	cout<< " Taus_phi                                          "      <<"\tphi()\t                                        "<<tau.phi() << endl;
	cout<< " Taus_e\t                                            "    <<"\te()\t                                        "<<tau.e() << endl;

	if(fEvent.isMC())
	  {
	    cout<< " Taus_pdgId                                        "  <<"\tMCVisibleTau()->pdgId()\t                        "<<tau.MCVisibleTau()->pdgId() << endl;
	    cout<< " Taus_pdgOrigin\t                                    "<<"\tpdgOrigin()\t                                "<<tau.pdgOrigin() << endl;
	    cout<< " Taus_mcNProngs\t                                    "<<"\tmcNProngs()\t                                "<<tau.mcNProngs() << endl;
	    cout<< " Taus_mcNPizero\t                                    "<<"\tmcNPizero()\t                                "<<tau.mcNPizero() << endl;
	  }
	cout<< " Taus_lChTrkPt\t                                     "    <<"\tlChTrkPt()\t                                "<<tau.lChTrkPt() << endl;
	cout<< " Taus_lChTrkEta\t                                    "    <<"\tlChTrkEta()\t                                "<<tau.lChTrkEta() << endl;
	cout<< " Taus_lNeutrTrkPt                                  "      <<"\tlNeutrTrkPt()\t                                "<<tau.lNeutrTrkPt() << endl;
	cout<< " Taus_lNeutrTrkEta                                 "      <<"\tlNeutrTrkEta()\t                                "<<tau.lNeutrTrkEta() << endl;
	cout<< " Taus_decayMode\t                                    "    <<"\tdecayMode()\t                                "<<tau.decayMode() << endl;
	cout<< " Taus_IPxy                                         "      <<"\tIPxy()\t                                        "<<tau.IPxy() << endl;
	cout<< " Taus_IPxySignif                                   "      <<"\tIPxySignif()\t                                "<<tau.IPxySignif() << endl;
	cout<< " Taus_nProngs\t                                      "    <<"\tnProngs()\t                                "<<tau.nProngs() << endl;

	if(fEvent.isMC())
	  {
	    cout<< " Taus_pt_MCVisibleTau\t                              "<<"\tMCVisibleTau()->pt()\t                        "<<tau.MCVisibleTau()->pt() << endl;
	    cout<< " Taus_eta_MCVisibleTau\t                             "<<"\tMCVisibleTau()->eta()\t                        "<<tau.MCVisibleTau()->eta() << endl;
	    cout<< " Taus_phi_MCVisibleTau\t                             "<<"\tMCVisibleTau()->phi()\t                        "<<tau.MCVisibleTau()->phi() << endl;
	    cout<< " Taus_e_MCVisibleTau\t                               "<<"\tMCVisibleTau()->e()\t                        "<<tau.MCVisibleTau()->e() << endl;
	  }
	cout<< " Taus_pt_matchingJet\t                               "    <<"\tmatchingJet()->pt()\t                        "<<tau.matchingJet()->pt() << endl;
	cout<< " Taus_eta_matchingJet\t                              "    <<"\tmatchingJet()->eta()\t                        "<<tau.matchingJet()->eta() << endl;
	cout<< " Taus_phi_matchingJet\t                              "    <<"\tmatchingJet()->phi()\t                        "<<tau.matchingJet()->phi() << endl;
	cout<< " Taus_e_matchingJet                                "      <<"\tmatchingJet()->e()\t                        "<<tau.matchingJet()->e() << endl;
	  
	cout<< " Taus_againstElectronLooseMVA5\t                     "    <<"\tagainstElectronLooseMVA5()\t                "<<tau.againstElectronLooseMVA5() << endl;
	cout<< " Taus_againstElectronMVA5category                  "      <<"\tagainstElectronMVA5category()\t                "<<tau.againstElectronMVA5category() << endl;
	cout<< " Taus_againstElectronMVA5raw\t                       "    <<"\tagainstElectronMVA5raw()\t                "<<tau.againstElectronMVA5raw() << endl;
	cout<< " Taus_againstElectronMediumMVA5\t                    "    <<"\tagainstElectronMediumMVA5()\t                "<<tau.againstElectronMediumMVA5() << endl;
	cout<< " Taus_againstElectronTightMVA5\t                     "    <<"\tagainstElectronTightMVA5()\t                "<<tau.againstElectronTightMVA5() << endl;
	cout<< " Taus_againstElectronVLooseMVA5\t                    "    <<"\tagainstElectronVLooseMVA5()\t                "<<tau.againstElectronVLooseMVA5() << endl;
	cout<< " Taus_againstElectronVTightMVA5\t                    "    <<"\tagainstElectronVTightMVA5()\t                "<<tau.againstElectronVTightMVA5() << endl;
	cout<< " Taus_againstMuonLoose3\t                            "    <<"\tagainstMuonLoose3()\t                        "<<tau.againstMuonLoose3() << endl;
	cout<< " Taus_againstMuonTight3\t                            "    <<"\tagainstMuonTight3()\t                        "<<tau.againstMuonTight3() << endl;
	cout<< " Taus_byCombinedIsolationDeltaBetaCorrRaw3Hits\t     "    <<"\tbyCombinedIsolationDeltaBetaCorrRaw3Hits()\t"<<tau.byCombinedIsolationDeltaBetaCorrRaw3Hits() << endl;
	cout<< " Taus_byIsolationMVA3newDMwLTraw                   "      <<"\tbyIsolationMVA3newDMwLTraw()\t                "<<tau.byIsolationMVA3newDMwLTraw() << endl;
	cout<< " Taus_byIsolationMVA3oldDMwLTraw                   "      <<"\tbyIsolationMVA3oldDMwLTraw()\t                "<<tau.byIsolationMVA3oldDMwLTraw() << endl;
	cout<< " Taus_byLooseCombinedIsolationDeltaBetaCorr3Hits   "      <<"\tbyLooseCombinedIsolationDeltaBetaCorr3Hits()\t"<<tau.byLooseCombinedIsolationDeltaBetaCorr3Hits() << endl;
	cout<< " Taus_byLooseIsolationMVA3newDMwLT                 "      <<"\tbyLooseIsolationMVA3newDMwLT()\t                "<<tau.byLooseIsolationMVA3newDMwLT() << endl;
	cout<< " Taus_byLooseIsolationMVA3oldDMwLT                 "      <<"\tbyLooseIsolationMVA3oldDMwLT()\t                "<<tau.byLooseIsolationMVA3oldDMwLT() << endl;
	cout<< " Taus_byLoosePileupWeightedIsolation3Hits          "      <<"\tbyLoosePileupWeightedIsolation3Hits()\t        "<<tau.byLoosePileupWeightedIsolation3Hits() << endl;
	cout<< " Taus_byMediumCombinedIsolationDeltaBetaCorr3Hits  "      <<"\tbyMediumCombinedIsolationDeltaBetaCorr3Hits()\t"<<tau.byMediumCombinedIsolationDeltaBetaCorr3Hits() << endl;
	cout<< " Taus_byMediumIsolationMVA3newDMwLT                "      <<"\tbyMediumIsolationMVA3newDMwLT()\t                "<<tau.byMediumIsolationMVA3newDMwLT() << endl;
	cout<< " Taus_byMediumIsolationMVA3oldDMwLT                "      <<"\tbyMediumIsolationMVA3oldDMwLT()\t                "<<tau.byMediumIsolationMVA3oldDMwLT() << endl;
	cout<< " Taus_byMediumPileupWeightedIsolation3Hits         "      <<"\tbyMediumPileupWeightedIsolation3Hits()\t        "<<tau.byMediumPileupWeightedIsolation3Hits() << endl;
	cout<< " Taus_byPhotonPtSumOutsideSignalCone\t               "    <<"\tbyPhotonPtSumOutsideSignalCone()\t        "<<tau.byPhotonPtSumOutsideSignalCone() << endl;
	cout<< " Taus_byPileupWeightedIsolationRaw3Hits\t            "    <<"\tbyPileupWeightedIsolationRaw3Hits()\t        "<<tau.byPileupWeightedIsolationRaw3Hits() << endl;
	cout<< " Taus_byTightCombinedIsolationDeltaBetaCorr3Hits   "      <<"\tbyTightCombinedIsolationDeltaBetaCorr3Hits()\t"<<tau.byTightCombinedIsolationDeltaBetaCorr3Hits() << endl;
	cout<< " Taus_byTightIsolationMVA3newDMwLT                 "     <<"\tbyTightIsolationMVA3newDMwLT()\t                "<<tau.byTightIsolationMVA3newDMwLT() << endl;
	cout<< " Taus_byTightIsolationMVA3oldDMwLT                 "     <<"\tbyTightIsolationMVA3oldDMwLT()\t                "<<tau.byTightIsolationMVA3oldDMwLT() << endl;
	cout<< " Taus_byTightPileupWeightedIsolation3Hits          "     <<"\tbyTightPileupWeightedIsolation3Hits()\t        "<<tau.byTightPileupWeightedIsolation3Hits() << endl;
	cout<< " Taus_byVLooseIsolationMVA3newDMwLT                "     <<"\tbyVLooseIsolationMVA3newDMwLT()\t                "<<tau.byVLooseIsolationMVA3newDMwLT() << endl;
	cout<< " Taus_byVLooseIsolationMVA3oldDMwLT                "     <<"\tbyVLooseIsolationMVA3oldDMwLT()\t                "<<tau.byVLooseIsolationMVA3oldDMwLT() << endl;
	cout<< " Taus_byVTightIsolationMVA3newDMwLT                "     <<"\tbyVTightIsolationMVA3newDMwLT()\t                "<<tau.byVTightIsolationMVA3newDMwLT() << endl;
	cout<< " Taus_byVTightIsolationMVA3oldDMwLT                "     <<"\tbyVTightIsolationMVA3oldDMwLT()\t                "<<tau.byVTightIsolationMVA3oldDMwLT() << endl;
	cout<< " Taus_byVVTightIsolationMVA3newDMwLT\t               "   <<"\tbyVVTightIsolationMVA3newDMwLT()\t        "<<tau.byVVTightIsolationMVA3newDMwLT() << endl;
	cout<< " Taus_byVVTightIsolationMVA3oldDMwLT\t               "   <<"\tbyVVTightIsolationMVA3oldDMwLT()\t        "<<tau.byVVTightIsolationMVA3oldDMwLT() << endl;
	cout<< " Taus_chargedIsoPtSum\t                              "   <<"\tchargedIsoPtSum()\t                        "<<tau.chargedIsoPtSum() << endl;
	cout<< " Taus_decayModeFinding\t                             "   <<"\tdecayModeFinding()\t                        "<<tau.decayModeFinding() << endl;
	cout<< " Taus_decayModeFindingNewDMs\t                       "   <<"\tdecayModeFindingNewDMs()\t                "<<tau.decayModeFindingNewDMs() << endl;
	cout<< " Taus_footprintCorrection                          "     <<"\tfootprintCorrection()\t                        "<<tau.footprintCorrection() << endl;
	cout<< " Taus_neutralIsoPtSum\t                              "   <<"\tneutralIsoPtSum()\t                        "<<tau.neutralIsoPtSum() << endl;
	cout<< " Taus_neutralIsoPtSumWeight                        "     <<"\tneutralIsoPtSumWeight()\t                        "<<tau.neutralIsoPtSumWeight() << endl;
	cout<< " Taus_photonPtSumOutsideSignalCone                 "     <<"\tphotonPtSumOutsideSignalCone()\t                "<<tau.photonPtSumOutsideSignalCone() << endl;
	cout<< " Taus_puCorrPtSum                                  "     <<"\tpuCorrPtSum()\t                                "<<tau.puCorrPtSum() << endl;

 	if(fEvent.isMC()) {
	  // cout << " Taus_pt_TESup\t                                     " <<"\tTESupPt()\t                                "<<tau.pt_TESup() << endl;
	  //cout<< " Taus_eta_TESup\t                                    " <<"\tTESupEta()\t                                "<<tau.TESupEta() << endl;
	  //cout<< " Taus_phi_TESup\t                                    " <<"\tTESupPhi()\t                                "<<tau.TESupPhi() << endl;
	  //cout<< " Taus_e_TESup\t                                      " <<"\tTESupE()\t                                "<<tau.TESupE() << endl;
	  //  
	  //cout<< " Taus_pt_TESdown                                   "   <<"\tTESdownPt()\t                                "<<tau.TESdownPt() << endl;
	  //cout<< " Taus_eta_TESdown                                  "   <<"\tTESdownEta()\t                                "<<tau.TESdownEta() << endl;
	  //cout<< " Taus_phi_TESdown                                  "   <<"\tTESdownPhi()\t                                "<<tau.TESdownPhi() << endl;
	  //cout<< " Taus_e_TESdown\t                                    " <<"\tTESdownE()\t                                "<<tau.TESdownE() << endl;
	  //  
	  //cout<< " Taus_pt_TESextremeUp\t                              " <<"\tTESexupPt()\t                                "<<tau.TESexupPt() << endl;
	  //cout<< " Taus_eta_TESextremeUp\t                             " <<"\tTESexupEta()\t                                "<<tau.TESexupEta() << endl;
	  //cout<< " Taus_phi_TESextremeUp\t                             " <<"\tTESexupPhi()\t                                "<<tau.TESexupPhi() << endl;
	  //cout<< " Taus_e_TESextremeUp\t                               " <<"\tTESexupE()\t                                "<<tau.TESexupE() << endl;
	  //  
	  //cout<< " Taus_pt_TESextremeDown\t                            " <<"\tTESexdownPt()\t                                "<<tau.TESexdownPt() << endl;
	  //cout<< " Taus_eta_TESextremeDown                           "   <<"\tTESexdownEta()\t                                "<<tau.TESexdownEta() << endl;
	  //cout<< " Taus_phi_TESextremeDown                           "   <<"\tTESexdownPhi()\t                                "<<tau.TESexdownPhi() << endl;
	  //cout<< " Taus_e_TESextremeDown\t                             " <<"\tTESexdownE()\t                                "<<tau.TESexdownE() << endl;	
	}

      }
    iTau++;
  }
  cout<<"Tau Collection size    "<<iTau << endl;
  cout<<"_____________________________________________________________________________________________________________________________\n\n";

  Size_t iElec=0;
  for(Electron elec : fEvent.electrons())
    {
      if(iElec==0)
  	{
  	  cout<< " Electrons_pt                                      "    <<"\tpt()                                          "<<elec.pt() << endl;
  	  cout<< " Electrons_eta                                     "    <<"\teta()                                         "<<elec.eta() << endl;
  	  cout<< " Electrons_phi                                     "    <<"\tphi()                                         "<<elec.phi() << endl;
  	  cout<< " Electrons_e                                       "    <<"\te()                                           "<<elec.e() << endl;
  	  cout<< " Electrons_relIsoDeltaBeta                         "    <<"\trelIsoDeltaBeta()                             "<<elec.relIsoDeltaBeta() << endl;
  	  cout<< " Electrons_isPF                                    "    <<"\tisPF()                                        "<<elec.isPF() << endl;
  	  cout<< " Electrons_ecalIso                                 "    <<"\tecalIso()                                     "<<elec.ecalIso() << endl;
  	  cout<< " Electrons_hcalIso                                 "    <<"\thcalIso()                                     "<<elec.hcalIso() << endl;
  	  cout<< " Electrons_caloIso                                 "    <<"\tcaloIso()                                     "<<elec.caloIso() << endl;
  	  cout<< " Electrons_trackIso                                "    <<"\ttrackIso()                                    "<<elec.trackIso() << endl;
  	  if(fEvent.isMC())
  	    {
  	      cout<< " Electrons_pt_MCelectron                           "<<"\tMCelectron()->pt()                            "<<elec.MCelectron()->pt() << endl;
  	      cout<< " Electrons_eta_MCelectron                          "<<"\tMCelectron()->eta()                           "<<elec.MCelectron()->eta() << endl;
  	      cout<< " Electrons_phi_MCelectron                          "<<"\tMCelectron()->phi()                           "<<elec.MCelectron()->phi() << endl;
  	      cout<< " Electrons_e_MCelectron                            "<<"\tMCelectron()->e()                             "<<elec.MCelectron()->e() << endl;
  	    }
  	  cout<< " Electrons_mvaEleID_PHYS14_PU20bx25_nonTrig_V1_wp80"    <<"\tmvaEleID_PHYS14_PU20bx25_nonTrig_V1_wp80()    "<<elec.mvaEleID_PHYS14_PU20bx25_nonTrig_V1_wp80() << endl;
  	  cout<< " Electrons_mvaEleID_PHYS14_PU20bx25_nonTrig_V1_wp90"    <<"\tmvaEleID_PHYS14_PU20bx25_nonTrig_V1_wp90()    "<<elec.mvaEleID_PHYS14_PU20bx25_nonTrig_V1_wp90() << endl;
  	}
      iElec++;
    }
  cout<<"Electron Collection size    "<<iElec << endl;
  cout<<"_____________________________________________________________________________________________________________________________\n\n";
  
  Size_t iMuon=0;
  for(Muon mu : fEvent.muons())
    {
      if(iMuon == 0)
  	{ 
  	  cout<< " Muons_pt             "<<"\tpt()               "<<mu.pt() << endl;
  	  cout<< " Muons_eta            "<<"\teta()              "<<mu.eta() << endl;
  	  cout<< " Muons_phi            "<<"\tphi()              "<<mu.phi() << endl;
  	  cout<< " Muons_e              "<<"\te()                "<<mu.e() << endl;
  	  cout<< " Muons_isGlobalMuon   "<<"\tisGlobalMuon()     "<<mu.isGlobalMuon() << endl;
  	  cout<< " Muons_muIDLoose      "<<"\tmuIDLoose()        "<<mu.muIDLoose() << endl;
  	  cout<< " Muons_muIDMedium     "<<"\tmuIDMedium()       "<<mu.muIDMedium() << endl;
  	  cout<< " Muons_muIDTight      "<<"\tmuIDTight()        "<<mu.muIDTight() << endl;
  	  cout<< " Muons_ecalIso        "<<"\tecalIso()          "<<mu.ecalIso() << endl;
  	  cout<< " Muons_hcalIso        "<<"\thcalIso()          "<<mu.hcalIso() << endl;
  	  cout<< " Muons_caloIso        "<<"\tcaloIso()          "<<mu.caloIso() << endl;
  	  cout<< " Muons_relIsoDeltaBeta"<<"\trelIsoDeltaBeta()  "<<mu.relIsoDeltaBeta() << endl;
  	  if(fEvent.isMC())
  	    {
  	      cout<< " Muons_pt_MCmuon      "<<"\tMCmuon()->pt()     "<<mu.MCmuon()->pt() << endl;
  	      cout<< " Muons_eta_MCmuon     "<<"\tMCmuon()->eta()    "<<mu.MCmuon()->eta() << endl;
  	      cout<< " Muons_phi_MCmuon     "<<"\tMCmuon()->phi()    "<<mu.MCmuon()->phi() << endl;
  	      cout<< " Muons_e_MCmuon       "<<"\tMCmuon()->e()      "<<mu.MCmuon()->e() << endl;
  	    }
  	}
      iMuon++;
    } // loop on muons
  cout<<"Muon Collection size    "<<iMuon << endl;
  cout<<"_____________________________________________________________________________________________________________________________\n\n";

  Size_t iJet=0;
  for(Jet jet : fEvent.jets_pfchs())
    {
      if(iJet==0)
  	{
	  
  	  cout<< " Jets_pt                                            "<<"\tpt()                                            "<<jet.pt() << endl;
  	  cout<< " Jets_eta                                           "<<"\teta()                                           "<<jet.eta() << endl;
  	  cout<< " Jets_phi                                           "<<"\tphi()                                           "<<jet.phi() << endl;
  	  cout<< " Jets_e                                             "<<"\te()                                             "<<jet.e() << endl;
	  
  	  cout<< " Jets_pdgId                                         "<<"\tMCjet()->pdgId()                                "<<jet.MCjet()->pdgId() << endl;
  	  cout<< " Jets_hadronFlavour                                 "<<"\thadronFlavour()                                 "<<jet.hadronFlavour() << endl;
  	  cout<< " Jets_partonFlavour                                 "<<"\tpartonFlavour()                                 "<<jet.partonFlavour() << endl;
	  
  	  cout<< " Jets_combinedSecondaryVertexBJetTags               "<<"\tcombinedSecondaryVertexBJetTags()               "<<jet.combinedSecondaryVertexBJetTags() << endl;
  	  cout<< " Jets_pfJetBProbabilityBJetTags                     "<<"\tpfJetBProbabilityBJetTags()                     "<<jet.pfJetBProbabilityBJetTags() << endl;
  	  cout<< " Jets_pfJetProbabilityBJetTags                      "<<"\tpfJetProbabilityBJetTags()                      "<<jet.pfJetProbabilityBJetTags() << endl;
  	  cout<< " Jets_pfTrackCountingHighPurBJetTags                "<<"\tpfTrackCountingHighPurBJetTags()                "<<jet.pfTrackCountingHighPurBJetTags() << endl;
  	  cout<< " Jets_pfTrackCountingHighEffBJetTags                "<<"\tpfTrackCountingHighEffBJetTags()                "<<jet.pfTrackCountingHighEffBJetTags() << endl;
  	  cout<< " Jets_pfSimpleSecondaryVertexHighEffBJetTags        "<<"\tpfSimpleSecondaryVertexHighEffBJetTags()        "<<jet.pfSimpleSecondaryVertexHighEffBJetTags() << endl;
  	  cout<< " Jets_pfSimpleSecondaryVertexHighPurBJetTags        "<<"\tpfSimpleSecondaryVertexHighPurBJetTags()        "<<jet.pfSimpleSecondaryVertexHighPurBJetTags() << endl;
  	  cout<< " Jets_pfCombinedSecondaryVertexV2BJetTags           "<<"\tpfCombinedSecondaryVertexV2BJetTags()           "<<jet.pfCombinedSecondaryVertexV2BJetTags() << endl;
  	  cout<< " Jets_pfCombinedInclusiveSecondaryVertexV2BJetTags  "<<"\tpfCombinedInclusiveSecondaryVertexV2BJetTags()  "<<jet.pfCombinedInclusiveSecondaryVertexV2BJetTags() << endl;
  	  cout<< " Jets_pfCombinedSecondaryVertexSoftLeptonBJetTags   "<<"\tpfCombinedSecondaryVertexSoftLeptonBJetTags()   "<<jet.pfCombinedSecondaryVertexSoftLeptonBJetTags() << endl;
  	  cout<< " Jets_pfCombinedMVABJetTags                         "<<"\tpfCombinedMVABJetTags()                         "<<jet.pfCombinedMVABJetTags() << endl;
  	  cout<< " Jets_pileupJetIdfullDiscriminant                   "<<"\tpileupJetIdfullDiscriminant()                   "<<jet.pileupJetIdfullDiscriminant() << endl;
  	  cout<< " Jets_IDloose                                       "<<"\tIDloose()                                       "<<jet.IDloose() << endl;
  	  cout<< " Jets_IDtight                                       "<<"\tIDtight()                                       "<<jet.IDtight() << endl;
  	  cout<< " Jets_IDtightLeptonVeto                             "<<"\tIDtightLeptonVeto()                             "<<jet.IDtightLeptonVeto() << endl;
  	  cout<< " Jets_PUIDloose                                     "<<"\tPUIDloose()                                     "<<jet.PUIDloose() << endl;
  	  cout<< " Jets_PUIDmedium                                    "<<"\tPUIDmedium()                                    "<<jet.PUIDmedium() << endl;
  	  cout<< " Jets_PUIDtight                                     "<<"\tPUIDtight()                                     "<<jet.PUIDtight() << endl;
  	  cout<< " Jets_isBasicJet                                    "<<"\tisBasicJet()                                    "<<jet.isBasicJet() << endl;
  	  cout<< " Jets_isCaloJet                                     "<<"\tisCaloJet()                                     "<<jet.isCaloJet() << endl;
  	  cout<< " Jets_isJPTJet                                      "<<"\tisJPTJet()                                      "<<jet.isJPTJet() << endl;
  	  cout<< " Jets_isPFJet                                       "<<"\tisPFJet()                                       "<<jet.isPFJet() << endl;
  	  cout<< " Jets_neutralHadronEnergyFraction                   "<<"\tneutralHadronEnergyFraction()                   "<<jet.neutralHadronEnergyFraction() << endl;
  	  cout<< " Jets_neutralEmEnergyFraction                       "<<"\tneutralEmEnergyFraction()                       "<<jet.neutralEmEnergyFraction() << endl;
  	  cout<< " Jets_nConstituents                                 "<<"\tnConstituents()                                 "<<jet.nConstituents() << endl;
  	  cout<< " Jets_chargedHadronMultiplicity                     "<<"\tchargedHadronMultiplicity()                     "<<jet.chargedHadronMultiplicity() << endl;
	  
  	  cout<< " Jets_pt_MCjet                                      "<<"\tMCjet()->pt()                                   "<<jet.MCjet()->pt() << endl;
  	  cout<< " Jets_eta_MCjet                                     "<<"\tMCjet()->eta()                                  "<<jet.MCjet()->eta() << endl;
  	  cout<< " Jets_phi_MCjet                                     "<<"\tMCjet()->phi()                                  "<<jet.MCjet()->phi() << endl;
  	  cout<< " Jets_e_MCjet                                       "<<"\tMCjet()->e()                                    "<<jet.MCjet()->e() << endl;
	  
  	  if(fEvent.isMC())
  	    {
  	      // cout<< " Jets_pt_JESup                                      "<<"\tJESup_pt()                                     "<<jet.JESup_pt() << endl;
  	      // cout<< " Jets_eta_JESup                                     "<<"\tJESup_eta()                                    "<<jet.JESup_eta() << endl;
  	      // cout<< " Jets_phi_JESup                                     "<<"\tJESup_phi()                                    "<<jet.JESup_phi() << endl;
  	      // cout<< " Jets_e_JESup                                       "<<"\tJESup_e()                                      "<<jet.JESup_e() << endl;
	      
  	      // cout<< " Jets_pt_JESdown                                    "<<"\tJESdown_pt()                                    "<<jet.JESdown_pt() << endl;
  	      // cout<< " Jets_eta_JESdown                                   "<<"\tJESdown_eta()                                   "<<jet.JESdown_eta() << endl;
  	      // cout<< " Jets_phi_JESdown                                   "<<"\tJESdown_phi()                                   "<<jet.JESdown_phi() << endl;
  	      // cout<< " Jets_e_JESdown                                     "<<"\tJESdown_e()                                     "<<jet.JESdown_e() << endl;
	      
  	      // cout<< " Jets_pt_JERup                                      "<<"\tJERup_pt()                                      "<<"Not Included" << endl;//jet.JERup_pt() << endl;
  	      // cout<< " Jets_eta_JERup                                     "<<"\tJERup_eta()                                     "<<"Not Included" << endl;//jet.JERup_eta() << endl;
  	      // cout<< " Jets_phi_JERup                                     "<<"\tJERup_phi()                                     "<<"Not Included" << endl;//jet.JERup_phi() << endl;
  	      // cout<< " Jets_e_JERup                                       "<<"\tJERup_e()                                       "<<"Not Included" << endl;//jet.JERup_e() << endl;
	      
  	      // cout<< " Jets_pt_JERdown                                    "<<"\tJERdown_pt()                                    "<<"Not Included" << endl;//jet.JERdown_pt() << endl;
  	      // cout<< " Jets_eta_JERdown                                   "<<"\tJERdown_eta()                                   "<<"Not Included" << endl;//jet.JERdown_eta() << endl;
  	      // cout<< " Jets_phi_JERdown                                   "<<"\tJERdown_phi()                                   "<<"Not Included" << endl;//jet.JERdown_phi() << endl;
  	      // cout<< " Jets_e_JERdown                                     "<<"\tJERdown_e()                                     "<<"Not Included" << endl;//jet.JERdown_e() << endl;
  	    }
  	}// if jet =0
      iJet++;
    }// loop on jet
  cout<<"Jet Collection size    "<<iJet << endl;
  cout<<"_____________________________________________________________________________________________________________________________\n\n";


  Size_t iJetPuppi=0;
  for(Jet jet : fEvent.jets_puppi())
    {
      if(iJetPuppi==0)
  	{
	  
  	  cout<< " PuppiJets_pt                                            "<<"\tpt()                                            "<<jet.pt() << endl;
  	  cout<< " PuppiJets_eta                                           "<<"\teta()                                           "<<jet.eta() << endl;
  	  cout<< " PuppiJets_phi                                           "<<"\tphi()                                           "<<jet.phi() << endl;
  	  cout<< " PuppiJets_e                                             "<<"\te()                                             "<<jet.e() << endl;
	  
  	  cout<< " PuppiJets_pdgId                                         "<<"\tMCjet()->pdgId()                                "<<jet.MCjet()->pdgId() << endl;
  	  cout<< " PuppiJets_hadronFlavour                                 "<<"\thadronFlavour()                                 "<<jet.hadronFlavour() << endl;
  	  cout<< " PuppiJets_partonFlavour                                 "<<"\tpartonFlavour()                                 "<<jet.partonFlavour() << endl;
	  
  	  cout<< " PuppiJets_combinedSecondaryVertexBJetTags               "<<"\tcombinedSecondaryVertexBJetTags()               "<<jet.combinedSecondaryVertexBJetTags() << endl;
  	  cout<< " PuppiJets_pfJetBProbabilityBJetTags                     "<<"\tpfJetBProbabilityBJetTags()                     "<<jet.pfJetBProbabilityBJetTags() << endl;
  	  cout<< " PuppiJets_pfJetProbabilityBJetTags                      "<<"\tpfJetProbabilityBJetTags()                      "<<jet.pfJetProbabilityBJetTags() << endl;
  	  cout<< " PuppiJets_pfTrackCountingHighPurBJetTags                "<<"\tpfTrackCountingHighPurBJetTags()                "<<jet.pfTrackCountingHighPurBJetTags() << endl;
  	  cout<< " PuppiJets_pfTrackCountingHighEffBJetTags                "<<"\tpfTrackCountingHighEffBJetTags()                "<<jet.pfTrackCountingHighEffBJetTags() << endl;
  	  cout<< " PuppiJets_pfSimpleSecondaryVertexHighEffBJetTags        "<<"\tpfSimpleSecondaryVertexHighEffBJetTags()        "<<jet.pfSimpleSecondaryVertexHighEffBJetTags() << endl;
  	  cout<< " PuppiJets_pfSimpleSecondaryVertexHighPurBJetTags        "<<"\tpfSimpleSecondaryVertexHighPurBJetTags()        "<<jet.pfSimpleSecondaryVertexHighPurBJetTags() << endl;
  	  cout<< " PuppiJets_pfCombinedSecondaryVertexV2BJetTags           "<<"\tpfCombinedSecondaryVertexV2BJetTags()           "<<jet.pfCombinedSecondaryVertexV2BJetTags() << endl;
  	  cout<< " PuppiJets_pfCombinedInclusiveSecondaryVertexV2BJetTags  "<<"\tpfCombinedInclusiveSecondaryVertexV2BJetTags()  "<<jet.pfCombinedInclusiveSecondaryVertexV2BJetTags() << endl;
  	  cout<< " PuppiJets_pfCombinedSecondaryVertexSoftLeptonBJetTags   "<<"\tpfCombinedSecondaryVertexSoftLeptonBJetTags()   "<<jet.pfCombinedSecondaryVertexSoftLeptonBJetTags() << endl;
  	  cout<< " PuppiJets_pfCombinedMVABJetTags                         "<<"\tpfCombinedMVABJetTags()                         "<<jet.pfCombinedMVABJetTags() << endl;
  	  cout<< " PuppiJets_pileupJetIdfullDiscriminant                   "<<"\tpileupJetIdfullDiscriminant()                   "<<jet.pileupJetIdfullDiscriminant() << endl;
  	  cout<< " PuppiJets_IDloose                                       "<<"\tIDloose()                                       "<<jet.IDloose() << endl;
  	  cout<< " PuppiJets_IDtight                                       "<<"\tIDtight()                                       "<<jet.IDtight() << endl;
  	  cout<< " PuppiJets_IDtightLeptonVeto                             "<<"\tIDtightLeptonVeto()                             "<<jet.IDtightLeptonVeto() << endl;
  	  cout<< " PuppiJets_PUIDloose                                     "<<"\tPUIDloose()                                     "<<jet.PUIDloose() << endl;
  	  cout<< " PuppiJets_PUIDmedium                                    "<<"\tPUIDmedium()                                    "<<jet.PUIDmedium() << endl;
  	  cout<< " PuppiJets_PUIDtight                                     "<<"\tPUIDtight()                                     "<<jet.PUIDtight() << endl;
  	  cout<< " PuppiJets_isBasicJet                                    "<<"\tisBasicJet()                                    "<<jet.isBasicJet() << endl;
  	  cout<< " PuppiJets_isCaloJet                                     "<<"\tisCaloJet()                                     "<<jet.isCaloJet() << endl;
  	  cout<< " PuppiJets_isJPTJet                                      "<<"\tisJPTJet()                                      "<<jet.isJPTJet() << endl;
  	  cout<< " PuppiJets_isPFJet                                       "<<"\tisPFJet()                                       "<<jet.isPFJet() << endl;
  	  cout<< " PuppiJets_neutralHadronEnergyFraction                   "<<"\tneutralHadronEnergyFraction()                   "<<jet.neutralHadronEnergyFraction() << endl;
  	  cout<< " PuppiJets_neutralEmEnergyFraction                       "<<"\tneutralEmEnergyFraction()                       "<<jet.neutralEmEnergyFraction() << endl;
  	  cout<< " PuppiJets_nConstituents                                 "<<"\tnConstituents()                                 "<<jet.nConstituents() << endl;
  	  cout<< " PuppiJets_chargedHadronMultiplicity                     "<<"\tchargedHadronMultiplicity()                     "<<jet.chargedHadronMultiplicity() << endl;
	  
  	  cout<< " PuppiJets_pt_MCjet                                      "<<"\tMCjet()->pt()                                   "<<jet.MCjet()->pt() << endl;
  	  cout<< " PuppiJets_eta_MCjet                                     "<<"\tMCjet()->eta()                                  "<<jet.MCjet()->eta() << endl;
  	  cout<< " PuppiJets_phi_MCjet                                     "<<"\tMCjet()->phi()                                  "<<jet.MCjet()->phi() << endl;
  	  cout<< " PuppiJets_e_MCjet                                       "<<"\tMCjet()->e()                                    "<<jet.MCjet()->e() << endl;
	  
	  // cout<< " PuppiJets_pt_JESup                                      "<<"\tJESup_pt()                                     "<<jet.JESup_pt() << endl;
	  // cout<< " PuppiJets_eta_JESup                                     "<<"\tJESup_eta()                                    "<<jet.JESup_eta() << endl;
	  // cout<< " PuppiJets_phi_JESup                                     "<<"\tJESup_phi()                                    "<<jet.JESup_phi() << endl;
	  // cout<< " PuppiJets_e_JESup                                       "<<"\tJESup_e()                                      "<<jet.JESup_e() << endl;
	  
	  // cout<< " PuppiJets_pt_JESdown                                    "<<"\tJESdown_pt()                                    "<<jet.JESdown_pt() << endl;
	  // cout<< " PuppiJets_eta_JESdown                                   "<<"\tJESdown_eta()                                   "<<jet.JESdown_eta() << endl;
	  // cout<< " PuppiJets_phi_JESdown                                   "<<"\tJESdown_phi()                                   "<<jet.JESdown_phi() << endl;
	  // cout<< " PuppiJets_e_JESdown                                     "<<"\tJESdown_e()                                     "<<jet.JESdown_e() << endl;
	  
	  // cout<< " PuppiJets_pt_JERup                                      "<<"\tJERup_pt()                                      "<<jet.JERup_pt() << endl;
	  // cout<< " PuppiJets_eta_JERup                                     "<<"\tJERup_eta()                                     "<<jet.JERup_eta() << endl;
	  // cout<< " PuppiJets_phi_JERup                                     "<<"\tJERup_phi()                                     "<<jet.JERup_phi() << endl;
	  // cout<< " PuppiJets_e_JERup                                       "<<"\tJERup_e()                                       "<<jet.JERup_e() << endl;
	  
	  // cout<< " PuppiJets_pt_JERdown                                    "<<"\tJERdown_pt()                                    "<<jet.JERdown_pt() << endl;
	  // cout<< " PuppiJets_eta_JERdown                                   "<<"\tJERdown_eta()                                   "<<jet.JERdown_eta() << endl;
	  // cout<< " PuppiJets_phi_JERdown                                   "<<"\tJERdown_phi()                                   "<<jet.JERdown_phi() << endl;
	  // cout<< " PuppiJets_e_JERdown                                     "<<"\tJERdown_e()                                     "<<jet.JERdown_e() << endl;
	
  	}// if jet =0
      iJetPuppi++;
    }// loop on jet
  cout<<"JetPuppi Collection size    "<<iJetPuppi << endl;
  cout<<"_____________________________________________________________________________________________________________________________\n\n";



  cout << " MET_Type1                  " << "\tet()                " << fEvent.met_Type1().et() << endl;
  cout << " MET_Type1_x                " << "\tx()                  " << fEvent.met_Type1().x() << endl;
  cout << " MET_Type1_y                " << "\ty()                  " << fEvent.met_Type1().y() << endl;
  cout << " MET_Type1_phi              " << "\tphi()                " << fEvent.met_Type1().phi() << endl;
  cout << " MET_Type1_significance     " << "\tsignificance()       " << fEvent.met_Type1().significance() << endl;

  cout << " MET_Type1_NoHF_et               " << "\tet()                 " << fEvent.met_Type1_NoHF().et() << endl;
  cout << " MET_Type1_NoHF_x                " << "\tx()                  " << fEvent.met_Type1_NoHF().x() << endl;
  cout << " MET_Type1_NoHF_y                " << "\ty()                  " << fEvent.met_Type1_NoHF().y() << endl;
  cout << " MET_Type1_NoHF_phi              " << "\tphi()                " << fEvent.met_Type1_NoHF().phi() << endl;
  cout << " MET_Type1_NoHF_significance     " << "\tsignificance()       " << fEvent.met_Type1_NoHF().significance() << endl;

  cout<< " MET_Puppi_et               " << "\tet()                 " << fEvent.met_Puppi().et() << endl;
  cout<< " MET_Puppi_x                " << "\tx()                  " << fEvent.met_Puppi().x() << endl;
  cout<< " MET_Puppi_y                " << "\ty()                  " << fEvent.met_Puppi().y() << endl;
  cout<< " MET_Puppi_phi              " << "\tphi()                " << fEvent.met_Puppi().phi() << endl;
  cout<< " MET_Puppi_significance     " << "\tsignificance()       " << fEvent.met_Puppi().significance() << endl;

  cout<< " CaloMET_et                " << "\tet()                 " << fEvent.calomet().et() << endl;
  cout<< " CaloMET_x                 " << "\tx()                  " << fEvent.calomet().x() << endl;
  cout<< " CaloMET_y                 " << "\ty()                  " << fEvent.calomet().y() << endl;
  
  if ( fEvent.isMC() )
    {
      cout<< " GenMET_et                   " << "\tet()                   " << fEvent.genMET().et() << endl;
      cout<< " GenMET_x                    " << "\tx()                    " << fEvent.genMET().x() << endl;
      cout<< " GenMET_y                    " << "\ty()                    " << fEvent.genMET().y() << endl;
      cout<< " GenMET_phi                  " << "\tphi()                  " << fEvent.genMET().phi() << endl;
    }

  cout << endl;

  if ( fEvent.isMC() )
    {
      Size_t iPFcand=0;
      for(PFCands pfcand : fEvent.pfCandidates())
	{
	  if(iPFcand == 0)
	    {
	      cout<< " PFcandidates_pt                "<<"\tpt()               "<<pfcand.pt() << endl;
	      cout<< " PFcandidates_eta               "<<"\teta()              "<<pfcand.eta() << endl;
	      cout<< " PFcandidates_phi               "<<"\tphi()              "<<pfcand.phi() << endl;
	      cout<< " PFcandidates_e                 "<<"\te()                "<<pfcand.e() << endl;
	      cout<< " PFcandidates_pdgId             "<<"\tpdgId()            "<<pfcand.pdgId() << endl;
	      cout<< " PFcandidates_NumOfHits         "<<"\tNumOfHits()        "<<pfcand.NumOfHits() << endl;
	      cout<< " PFcandidates_NumOfPixHits      "<<"\tNumOfPixHits()     "<<pfcand.NumOfPixHits() << endl;
	      cout<< " PFcandidates_IPTwrtPV          "<<"\tIPTwrtPV()         "<<pfcand.IPTwrtPV() << endl;
	      cout<< " PFcandidates_IPTwrtPVError     "<<"\tIPTwrtPVError()    "<<pfcand.IPTwrtPVError() << endl;
	      cout<< " PFcandidates_IPzwrtPV          "<<"\tIPzwrtPV()         "<<pfcand.IPzwrtPV() << endl;
	      cout<< " PFcandidates_IPzwrtPVError     "<<"\tIPzwrtPVError()    "<<pfcand.IPzwrtPVError() << endl;
	      cout<< " PFcandidates_IPTSignificance   "<<"\tIPTSignificance()  "<<pfcand.IPTSignificance() << endl;
	      cout<< " PFcandidates_IPzSignificance   "<<"\tIPzSignificance()  "<<pfcand.IPzSignificance() << endl;
	    }
	  iPFcand++;
	}
      cout<<"PF Cand Collection size    "<<iPFcand << endl;
      cout<<"_____________________________________________________________________________________________________________________________\n\n";
    }
  
  if(fEvent.isMC())
    {
      GenWeight genWt = fEvent.genWeight();
      cout<< " GenWeight                "<<"\tweight()               "<<genWt.weight() << endl;
      cout<<"_____________________________________________________________________________________________________________________________\n\n";
    }


  if(fEvent.isMC())
    {
      Size_t iGenp=0;
      for(auto gen : fEvent.genparticles())
      	{
      	  if(iGenp ==0)
      	    {
      	      cout<< " GenParticles_pt          "<<"\tpt()                "<<gen.pt() << endl;
      	      cout<< " GenParticles_eta         "<<"\teta()               "<<gen.eta() << endl;
      	      cout<< " GenParticles_phi         "<<"\tphi()               "<<gen.phi() << endl;
      	      cout<< " GenParticles_e           "<<"\te()                 "<<gen.e() << endl;
      	      cout<< " GenParticles_pdgId       "<<"\tpdgId()             "<<gen.pdgId() << endl;
      	      cout<< " GenParticles_mass        "<<"\tmass()              "<<gen.mass() << endl;
      	      cout<< " GenParticles_vertexX     "<<"\tvertexX()           "<<gen.vertexX() << endl;
      	      cout<< " GenParticles_vertexY     "<<"\tvertexY()           "<<gen.vertexY() << endl;
      	      cout<< " GenParticles_vertexZ     "<<"\tvertexZ()           "<<gen.vertexX() << endl;
      	      cout<< " GenParticles_charge      "<<"\tcharge()            "<<gen.charge() << endl;
      	      cout<< " GenParticles_status      "<<"\tstatus()            "<<gen.status() << endl;
      	      cout<< " GenParticles_mothers     "<<"\tmothers()           "<<gen.mothers().size()<<"\t {mothers() return a vector}" << endl;
      	      cout<< " GenParticles_daughters   "<<"\tdaughters()         "<<gen.daughters().size()<<"\t {daughters() return a vector}" << endl;
      	    }
	  iGenp++;
	}// end loop on genp
      cout<<"GenParticle Collection size    "<<iGenp << endl;
      cout<<"_____________________________________________________________________________________________________________________________\n\n";
	    
    }// if MC


  if(fEvent.isMC())
    {
      Size_t iGenJ=0;
      for(GenJet genj : fEvent.genjets())
	{

	  if(iGenJ == 0)
	    {
	      cout<< " GenJets_pt                "<<"\tpt()                "<<genj.pt() << endl;
      	      cout<< " GenJets_eta               "<<"\teta()               "<<genj.eta() << endl;
      	      cout<< " GenJets_phi               "<<"\tphi()               "<<genj.phi() << endl;
      	      cout<< " GenJets_e                 "<<"\te()                 "<<genj.e() << endl;
	      cout<< " GenJets_charge            "<<"\tcharge()            "<<genj.charge() << endl;
	      cout<< " GenJets_emEnergy          "<<"\temEnergy()          "<<genj.emEnergy() << endl;
	      cout<< " GenJets_hadEnergy         "<<"\thadEnergy()         "<<genj.hadEnergy() << endl;
	      cout<< " GenJets_auxEnergy         "<<"\tauxEnergy()         "<<genj.auxEnergy() << endl;
	      cout<< " GenJets_invisEnergy       "<<"\tinvisEnergy()       "<<genj.invisEnergy() << endl;
	      cout<< " GenJets_nGenConstituents  "<<"\tnGenConstituents()  "<<genj.nGenConstituents() << endl;
	      
	    }
	  iGenJ++;
	}
      cout<<"GenJet Collection size    "<<iGenJ << endl;
      cout<<"_____________________________________________________________________________________________________________________________\n\n";

    }// if MC
  
  
  cout<< " L1MET_l1extra_et               " << "\tet()                 " << fEvent.L1extramet().et() << endl;
  cout<< " L1MET_l1extra_x                " << "\tx()                  " << fEvent.L1extramet().x() << endl;
  cout<< " L1MET_l1extra_y                " << "\ty()                  " << fEvent.L1extramet().y() << endl;
  cout<< " L1MET_l1extra_phi              " << "\tphi()                " << fEvent.L1extramet().phi() << endl;

  cout<< " L1MET_et                       " << "\tet()                 " << fEvent.L1met().et() << endl;
  cout<< " L1MET_x                        " << "\tx()                  " << fEvent.L1met().x() << endl;
  cout<< " L1MET_y                        " << "\ty()                  " << fEvent.L1met().y() << endl;
  cout<< " L1MET_phi                      " << "\tphi()                " << fEvent.L1met().phi() << endl;

  cout<< " HLTMET_et                      " << "\tet()                 " << fEvent.HLTmet().et() << endl;
  cout<< " HLTMET_x                       " << "\tx()                  " << fEvent.HLTmet().x() << endl;
  cout<< " HLTMET_y                       " << "\ty()                  " << fEvent.HLTmet().y() << endl;
  cout<< " HLTMET_phi                     " << "\tphi()                " << fEvent.HLTmet().phi() << endl;


  Size_t iHLTTau=0;
  for(HLTTau hltTau : fEvent.triggerTaus())
    {
      if(iHLTTau == 0)
	{
	  cout<< " HLTTau_pt                    "<<"\tpt()                 "<<hltTau.pt() << endl;
	  cout<< " HLTTau_eta                   "<<"\teta()                "<<hltTau.eta() << endl;
	  cout<< " HLTTau_phi                   "<<"\tphi()                "<<hltTau.phi() << endl;
	  cout<< " HLTTau_e                     "<<"\te()                  "<<hltTau.e() << endl;
	}
      iHLTTau++;
    }
  cout<<"HLT Tau Collection size    "<<iHLTTau << endl;
  cout<<"_____________________________________________________________________________________________________________________________\n\n";

  cout<< " HLTTau_pt           "<<"\tfEvent.configurableTriggerDecision()                 "<<fEvent.configurableTriggerDecision()<<"   {Or Decision of TRG list in .py}" << endl;


}//end process












/*      
	for (size_t i = 0; i < fEvent.genparticles().getAllGenpCollection().size(); ++i) 
       	{
	auto& gen = fEvent.genparticles().getAllGenpCollection();
	if(iGenp < 5)
	{
	cout<<"\nLL          "<<gen.pdgId()[i]//<< gen.pdgId()[i]<<"   "<<gen.pt()[i]<<"   "<<gen.eta()[i]<<"   "<<gen.phi()[i]<<"   "<<gen.e()[i]<<"   " << endl;//<<gen.mass() << endl;
	// 	      //     cout<<"\nLL          "<< gen.mass()<<"   "<<gen.vertexX()<<"   "<<gen.vertexY()<<"   "<<gen.vertexZ()<<"   "<<gen.status() << endl;
	}
	iGenp++;
  	}
*/
