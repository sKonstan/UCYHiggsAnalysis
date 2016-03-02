// -*- c++ -*-
#include "EventSelection/interface/JetSelection.h"

#include "Framework/interface/ParameterSet.h"
#include "EventSelection/interface/CommonPlots.h"
#include "DataFormat/interface/Event.h"
#include "Framework/interface/HistoWrapper.h"
#include "Framework/interface/Exception.h"
//#include "Framework/interface/makeTH.h"

#include "Math/VectorUtil.h"

JetSelection::Data::Data()
  : bPassedSelection(false),
    fJetMatchedToTau(0),
    fHT(-1.0)
{ }

JetSelection::Data::~Data() { }


const Jet& JetSelection::Data::getJetMatchedToTau() const { 
  if (!jetMatchedToTauFound())
    throw hplus::Exception("Assert") << "You forgot to check if the jet matched to tau exists (jetMatchedToTauFound()), this message occurs when none exists!";
  return fJetMatchedToTau[0];
}


JetSelection::JetSelection(const ParameterSet& config, EventCounter& eventCounter, HistoWrapper& histoWrapper, CommonPlots* commonPlots, const std::string& postfix)
  : BaseSelection(eventCounter, histoWrapper, commonPlots, postfix),
    cfg_PtCut(          config.getParameter<float>("PtCut")          ),
    cfg_EtaCut(         config.getParameter<float>("EtaCut")         ),
    cfg_TauMatchDeltaR( config.getParameter<float>("TauMatchDeltaR") ),
    cfg_NJetsCut(config, "NJetsCut"),
    // Event counter for passing selection
    cPassedJetSelection( fEventCounter.addCounter("passed jet selection (" + postfix + ")") ),
    // Event sub-counters for passing selection
    cSubAll(                fEventCounter.addSubCounter("jet selection (" + postfix + ")", "All events")            ),
    cSubPassedJetID(        fEventCounter.addSubCounter("jet selection (" + postfix + ")", "Passed jet ID")         ),
    cSubPassedJetPUID(      fEventCounter.addSubCounter("jet selection (" + postfix + ")", "Passed PU ID")          ),
    cSubPassedMatchWithTau( fEventCounter.addSubCounter("jet selection (" + postfix + ")", "Passed tau match")      ),
    cSubPassedPt(           fEventCounter.addSubCounter("jet selection (" + postfix + ")", "Passed pt cut")         ),
    cSubPassedEta(          fEventCounter.addSubCounter("jet selection (" + postfix + ")", "Passed eta cut")        ),
    cSubPassedJetCount(     fEventCounter.addSubCounter("jet selection (" + postfix + ")", "Passed jet number cut") )
{ 
  initialize(config);
}


JetSelection::JetSelection(const ParameterSet& config)
  : BaseSelection(),
    cfg_PtCut(          config.getParameter<float>("PtCut") ),
    cfg_EtaCut(         config.getParameter<float>("EtaCut") ),
    cfg_TauMatchDeltaR( config.getParameter<float>("TauMatchDeltaR") ),
    cfg_NJetsCut(       config, "NJetsCut"),
    // Event counter for passing selection
    cPassedJetSelection(fEventCounter.addCounter("passed jet selection")),
    // Event sub-counters for passing selection
    cSubAll(                fEventCounter.addSubCounter("jet selection", "All events")            ),
    cSubPassedJetID(        fEventCounter.addSubCounter("jet selection", "Passed jet ID")         ),
    cSubPassedJetPUID(      fEventCounter.addSubCounter("jet selection", "Passed PU ID")          ),
    cSubPassedMatchWithTau( fEventCounter.addSubCounter("jet selection", "Passed tau match")      ),
    cSubPassedPt(           fEventCounter.addSubCounter("jet selection", "Passed pt cut")         ),
    cSubPassedEta(          fEventCounter.addSubCounter("jet selection", "Passed eta cut")        ),
    cSubPassedJetCount(     fEventCounter.addSubCounter("jet selection", "Passed jet number cut") )
{ 
  initialize(config);
  bookHistograms(new TDirectory());
}


JetSelection::~JetSelection() { }


void JetSelection::initialize(const ParameterSet& config) {

  return;
}


void JetSelection::bookHistograms(TDirectory* dir) {
  TDirectory* subdir = fHistoWrapper.mkdir(HistoLevel::kDebug, dir, "jetSelection_" + sPostfix);

  hJetPtAll     = fHistoWrapper.makeTH<TH1F>( HistoLevel::kDebug, subdir, "jetPtAll"    , "Jet pT, all"    , 40,  0.0, 400.0 );
  hJetEtaAll    = fHistoWrapper.makeTH<TH1F>( HistoLevel::kDebug, subdir, "jetEtaAll"   , "Jet #eta, all"  , 50, -2.5,   2.5 );
  hJetPtPassed  = fHistoWrapper.makeTH<TH1F>( HistoLevel::kDebug, subdir, "jetPtPassed" , "Jet pT, passed" , 40,  0.0, 400.0 );
  hJetEtaPassed = fHistoWrapper.makeTH<TH1F>( HistoLevel::kDebug, subdir, "jetEtaPassed", "Jet Eta, passed", 50, -2.5,   2.5 );

  hSelectedJetPt.push_back( fHistoWrapper.makeTH<TH1F>( HistoLevel::kDebug, subdir, "selectedJetsFirstJetPt" , "First jet pT" , 40, 0.0, 400.0) );
  hSelectedJetPt.push_back( fHistoWrapper.makeTH<TH1F>( HistoLevel::kDebug, subdir, "selectedJetsSecondJetPt", "Second jet pT", 40, 0.0, 400.0) );
  hSelectedJetPt.push_back( fHistoWrapper.makeTH<TH1F>( HistoLevel::kDebug, subdir, "selectedJetsThirdJetPt" , "Third jet pT" , 40, 0.0, 400.0) );
  hSelectedJetPt.push_back( fHistoWrapper.makeTH<TH1F>( HistoLevel::kDebug, subdir, "selectedJetsFourthJetPt", "Fourth jet pT", 40, 0.0, 400.0) );

  hSelectedJetEta.push_back( fHistoWrapper.makeTH<TH1F>( HistoLevel::kDebug, subdir, "selectedJetsFirstJetEta" , "First jet #eta" , 50, -2.5, 2.5) );
  hSelectedJetEta.push_back( fHistoWrapper.makeTH<TH1F>( HistoLevel::kDebug, subdir, "selectedJetsSecondJetEta", "Second jet #eta", 50, -2.5, 2.5) );
  hSelectedJetEta.push_back( fHistoWrapper.makeTH<TH1F>( HistoLevel::kDebug, subdir, "selectedJetsThirdJetEta" , "Third jet #eta" , 50, -2.5, 2.5) );
  hSelectedJetEta.push_back( fHistoWrapper.makeTH<TH1F>( HistoLevel::kDebug, subdir, "selectedJetsFourthJetEta", "Fourth jet #eta", 50, -2.5, 2.5) );

  hJetMatchingToTauDeltaR  = fHistoWrapper.makeTH<TH1F>( HistoLevel::kDebug, subdir, "JetMatchingToTauDeltaR" , "#DeltaR(jet, #tau)", 40, 0.0, 2.0 );
  hJetMatchingToTauPtRatio = fHistoWrapper.makeTH<TH1F>( HistoLevel::kDebug, subdir, "JetMatchingToTauPtRatio", "jet pT / #tau pT"  , 40, 0.0, 2.0 );
  
  return;
}


JetSelection::Data JetSelection::silentAnalyze(const Event& event, const Tau& tau) {
  ensureSilentAnalyzeAllowed(event.eventID()); 
  disableHistogramsAndCounters(); // Disable histogram filling and counter
  Data myData = privateAnalyze(event, tau.p4(), tau.pt());
  enableHistogramsAndCounters();

  return myData;
}


JetSelection::Data JetSelection::silentAnalyzeWithoutTau(const Event& event) {
  ensureSilentAnalyzeAllowed(event.eventID());  
  disableHistogramsAndCounters(); // Disable histogram filling and counter
  math::LorentzVectorT<double> tauP(0.,0.,9999.,0.);
  Data myData = privateAnalyze(event, tauP, -1.0);
  enableHistogramsAndCounters();

  return myData;
}


JetSelection::Data JetSelection::analyze(const Event& event, const Tau& tau) {
  ensureAnalyzeAllowed(event.eventID());
  JetSelection::Data data = privateAnalyze(event, tau.p4(), tau.pt());

  // Send data to CommonPlots
  if (fCommonPlots != nullptr) fCommonPlots->fillControlPlotsAtJetSelection(event, data);

  return data;
}


JetSelection::Data JetSelection::analyzeWithoutTau(const Event& event) {
  ensureAnalyzeAllowed(event.eventID());
  math::LorentzVectorT<double> tauP(0.,0.,9999.,0.);
  JetSelection::Data data = privateAnalyze(event, tauP, -1.);

  // Send data to CommonPlots
  if (fCommonPlots != nullptr) fCommonPlots->fillControlPlotsAtJetSelection(event, data);

  return data;
}


JetSelection::Data JetSelection::privateAnalyze(const Event& event, const math::LorentzVectorT<double>& tauP, const double tauPt) {
  Data output;

  cSubAll.increment();
  bool passedJetID        = false;
  bool passedJetPUID      = false;
  bool passedMatchWithTau = false;
  bool passedEta          = false;
  bool passedPt           = false;
  
  // For-loop: Alljets
  for(Jet jet: event.jets()) {

    //====== Apply Cut: jet ID
    if ( !jet.jetIDDiscriminator() ) continue;
    passedJetID = true;


    //====== Apply Cut: jet PU ID
    if ( !jet.jetPUIDDiscriminator() ) continue;
    passedJetPUID = true;
    output.fAllJets.push_back(jet);   
    // Fill histos
    hJetPtAll ->Fill( jet.pt()  );
    hJetEtaAll->Fill( jet.eta() );


    //====== Apply Cut: tau radius
      if (tauPt > 0.0) {
      double myDeltaR = ROOT::Math::VectorUtil::DeltaR(tauP, jet.p4());
      hJetMatchingToTauDeltaR->Fill(myDeltaR);
      if (myDeltaR < cfg_TauMatchDeltaR) continue;
      passedMatchWithTau = true;
    }


    //====== Apply Cut: pt
    if (jet.pt() < cfg_PtCut) continue;
    passedPt = true;


    //====== Apply Cut: eta
    if (std::fabs(jet.eta()) > cfg_EtaCut) continue;
    passedEta = true;


    //====== Jet passed all cuts     
    output.fSelectedJets.push_back(jet);
    hJetPtPassed ->Fill( jet.pt()  );
    hJetEtaPassed->Fill( jet.eta() );

  }

  // Fill counters (so far)
  if (passedJetID )       cSubPassedJetID.increment();
  if (passedJetPUID)      cSubPassedJetPUID.increment();
  if (passedMatchWithTau) cSubPassedMatchWithTau.increment();
  if (passedPt)           cSubPassedPt.increment();
  if (passedEta)          cSubPassedEta.increment();
  

  //====== Apply Cut: number of jets
  if ( !cfg_NJetsCut.passedCut(output.fSelectedJets.size()) ) return output;
  // Fill counter
  cSubPassedJetCount.increment();

  
  //====== Passed jet selection
  output.bPassedSelection = true;
  std::sort( output.fSelectedJets.begin(), output.fSelectedJets.end() );
  // Fill counter
  cPassedJetSelection.increment();


  //====== Find jet matched to tau
  if (tauPt > 0.0) {
    
    findJetMatchingToTau(output.fJetMatchedToTau, event, tauP);
    if (output.jetMatchedToTauFound()) 
      {
	hJetMatchingToTauPtRatio->Fill(tauPt / output.getJetMatchedToTau().pt());
      }
  }
  

  //====== Calculate HT
  output.fHT = 0.0;
  for(Jet jet: output.getSelectedJets()) { output.fHT += jet.pt(); }
  if (tauPt > 0.0) output.fHT += tauPt;

  // Fill pt and eta of jets
  size_t i = 0;
  for (Jet jet: output.fSelectedJets) {
    if (i < 4) {
      hSelectedJetPt[i] ->Fill( jet.pt()  );
      hSelectedJetEta[i]->Fill( jet.eta() );
    }
    ++i;
  }

  return output;
}


void JetSelection::findJetMatchingToTau(std::vector<Jet>& collection, const Event& event, const math::LorentzVectorT<double>& tauP) {
  double myMinDeltaR     = 9999;
  size_t mySelectedIndex = 9999;

  size_t i = 0;
  // For-loop: All jets
  for(Jet jet: event.jets()) {
    double myDeltaR = ROOT::Math::VectorUtil::DeltaR(tauP, jet.p4());

    if (myDeltaR < myMinDeltaR) 
      {
	myMinDeltaR = myDeltaR;
	mySelectedIndex = i;
      }
    i += 1;

  } // For-loop: All jets

  if (myMinDeltaR < 0.1) collection.push_back(event.jets()[mySelectedIndex]);

  return;
}
