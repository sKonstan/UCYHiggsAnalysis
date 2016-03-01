// -*- c++ -*-
#include "EventSelection/interface/MuonSelection.h"

#include "Framework/interface/ParameterSet.h"
#include "EventSelection/interface/CommonPlots.h"
#include "DataFormat/interface/Event.h"
#include "Framework/interface/HistoWrapper.h"
//#include "Framework/interface/makeTH.h"

MuonSelection::Data::Data() 
: fHighestSelectedMuonPt(0.0),
  fHighestSelectedMuonEta(0.0) { }


MuonSelection::Data::~Data() { }


MuonSelection::MuonSelection(const ParameterSet& config, EventCounter& eventCounter, HistoWrapper& histoWrapper, CommonPlots* commonPlots, const std::string& postfix)
: BaseSelection(eventCounter, histoWrapper, commonPlots, postfix),
  // Input Parameters (passed through python configuration file) 
  cfg_PtCut(config.getParameter<float>("PtCut")),
  cfg_EtaCut(config.getParameter<float>("EtaCut")),
  cfg_RelIsolString(config.getParameter<std::string>("RelIsolString")),
  cfg_RelIsoCut(-1.0),
  cfg_VetoMode(false),
  // Event counter for passing selection
  cPassedMuonSelection( fEventCounter.addCounter("passed mu selection ("+postfix+")") ),
  // Event sub-counters for passing selection 
  cSubAll(             fEventCounter.addSubCounter("mu selection (" + postfix + ")", "All events")       ),
  cSubPassedPt(        fEventCounter.addSubCounter("mu selection (" + postfix + ")", "Passed pt cut")    ),
  cSubPassedEta(       fEventCounter.addSubCounter("mu selection (" + postfix + ")", "Passed eta cut")   ),
  cSubPassedID(        fEventCounter.addSubCounter("mu selection (" + postfix + ")", "Passed ID")        ),
  cSubPassedIsolation( fEventCounter.addSubCounter("mu selection (" + postfix + ")", "Passed isolation") )
{
  initialize(config, postfix);
}


MuonSelection::MuonSelection(const ParameterSet& config, const std::string& postfix)
: BaseSelection(),
  cfg_PtCut(config.getParameter<float>("muonPtCut")),
  cfg_EtaCut(config.getParameter<float>("muonEtaCut")),
  cfg_RelIsolString(config.getParameter<std::string>("RelIsolString")),
  cfg_RelIsoCut(-1.0),
  cfg_VetoMode(false),
  // Event counter for passing selection
  cPassedMuonSelection( fEventCounter.addCounter("passed mu selection (" + postfix + ")") ),
  // Event sub-counter for passing selection
  cSubAll(             fEventCounter.addSubCounter("mu selection (" + postfix + ")", "All events")       ),
  cSubPassedPt(        fEventCounter.addSubCounter("mu selection (" + postfix + ")", "Passed pt cut")    ),
  cSubPassedEta(       fEventCounter.addSubCounter("mu selection (" + postfix + ")", "Passed eta cut")   ),
  cSubPassedID(        fEventCounter.addSubCounter("mu selection (" + postfix + ")", "Passed ID")        ),
  cSubPassedIsolation( fEventCounter.addSubCounter("mu selection (" + postfix + ")", "Passed isolation") )
{
  initialize(config, postfix);
  bookHistograms(new TDirectory());
}


MuonSelection::~MuonSelection() { }


void MuonSelection::initialize(const ParameterSet& config, const std::string& postfix) {
  if (postfix.find("veto") != std::string::npos || postfix.find("Veto") != std::string::npos) cfg_VetoMode = true;

  if (cfg_RelIsolString == "veto" || cfg_RelIsolString == "Veto") 
    {
      cfg_RelIsoCut = 0.20; // Based on 2012 isolation
    } 
  else if (cfg_RelIsolString == "none" || cfg_RelIsolString == "None") 
    {
      cfg_RelIsoCut = 99999.99;
    } 
  else if (cfg_RelIsolString == "tight" || cfg_RelIsolString == "Tight") 
    {
      cfg_RelIsoCut = 0.12; // Based on 2012 isolation
    } 
  else if (cfg_RelIsolString == "medium" || cfg_RelIsolString == "Medium") 
    {
      cfg_RelIsoCut = 0.20; // Based on nothing
    } 
  else if (cfg_RelIsolString == "loose" || cfg_RelIsolString == "Loose") 
    {
      cfg_RelIsoCut = 0.35; // Based on nothing
    } 
  else
    {
      throw hplus::Exception("config") << "Invalid muonIsolation option '" << cfg_RelIsolString << "'! Options: 'veto', 'tight'";
    }

  return;
}


void MuonSelection::bookHistograms(TDirectory* dir) {
  TDirectory* subdir = fHistoWrapper.mkdir(HistoLevel::kDebug, dir, "muSelection_"+sPostfix);

  hMuonPtAll     = fHistoWrapper.makeTH<TH1F>( HistoLevel::kDebug, subdir, "muonPtAll"   , "Muon pT, all"   , 40,  0.0, 400.0 );
  hMuonEtaAll    = fHistoWrapper.makeTH<TH1F>( HistoLevel::kDebug, subdir, "muonEtaAll"  , "Muon eta, all"  , 50, -2.5,   2.5 );
  hMuonPtPassed  = fHistoWrapper.makeTH<TH1F>( HistoLevel::kDebug, subdir, "muonPtPassed", "Muon pT, passed", 40,  0.0, 400.0 );
  hMuonEtaPassed = fHistoWrapper.makeTH<TH1F>( HistoLevel::kDebug, subdir, "muonPtPassed", "Muon pT, passed", 40,  0.0, 400.0 );
 
 // Resolution
  hPtResolution  = fHistoWrapper.makeTH<TH1F>( HistoLevel::kDebug, subdir, "ptResolution" , "(reco pT - gen pT) / reco pT"   , 200, -1.0, 1.0 );
  hEtaResolution = fHistoWrapper.makeTH<TH1F>( HistoLevel::kDebug, subdir, "etaResolution", "(reco eta - gen eta) / reco eta", 200, -1.0, 1.0 );
  hPhiResolution = fHistoWrapper.makeTH<TH1F>( HistoLevel::kDebug, subdir, "phiResolution", "(reco phi - gen phi) / reco phi", 200, -1.0, 1.0 );

  // Isolation efficiency
  hIsolPtBefore  = fHistoWrapper.makeTH<TH1F>( HistoLevel::kDebug, subdir, "IsolPtBefore" , "Muon pT before isolation is applied"  , 40,  0.0, 400.0 );
  hIsolEtaBefore = fHistoWrapper.makeTH<TH1F>( HistoLevel::kDebug, subdir, "IsolEtaBefore", "Muon eta before isolation is applied" , 50, -2.5,   2.5 );
  hIsolVtxBefore = fHistoWrapper.makeTH<TH1F>( HistoLevel::kDebug, subdir, "IsolVtxBefore", "Nvertices before isolation is applied", 60,  0.0,  60.0 );
  hIsolPtAfter   = fHistoWrapper.makeTH<TH1F>( HistoLevel::kDebug, subdir, "IsolPtAfter"  , "Muon pT before isolation is applied"  , 40,  0.0, 400.0 );
  hIsolEtaAfter  = fHistoWrapper.makeTH<TH1F>( HistoLevel::kDebug, subdir, "IsolEtaAfter" , "Muon eta before isolation is applied" , 50, -2.5,   2.5 );
  hIsolVtxAfter  = fHistoWrapper.makeTH<TH1F>( HistoLevel::kDebug, subdir, "IsolVtxAfter" , "Nvertices before isolation is applied", 60,  0.0,  60.0 );

  return;
}


MuonSelection::Data MuonSelection::silentAnalyze(const Event& event) {
  ensureSilentAnalyzeAllowed(event.eventID());
  disableHistogramsAndCounters(); // Disable histogram filling and counter
  Data myData = privateAnalyze(event);
  enableHistogramsAndCounters();

  return myData;
}


MuonSelection::Data MuonSelection::analyze(const Event& event) {
  ensureAnalyzeAllowed(event.eventID());
  MuonSelection::Data data = privateAnalyze(event);

  // Send data to CommonPlots
  if (fCommonPlotsIsEnabled()) fCommonPlots->fillControlPlotsAtMuonSelection(event, data);

  return data;
}


MuonSelection::Data MuonSelection::privateAnalyze(const Event& event) {
  Data output;
  cSubAll.increment();
  bool passedPt   = false;
  bool passedEta  = false;
  bool passedID   = false;
  bool passedIsol = false;

  // For-loop: All muons
  for(Muon muon: event.muons()) {

    // Fill histos
    hMuonPtAll ->Fill( muon.pt()  );
    hMuonEtaAll->Fill( muon.eta() );


    //====== Apply Cut: pt
    if (muon.pt() < cfg_PtCut) continue;
    passedPt = true;


    //====== Apply Cut: eta
    if (std::fabs(muon.eta()) > cfg_EtaCut) continue;
    passedEta = true;


    //====== Apply Cut: muon ID (see DataFormat/interface/Muon.h)  
    if (!muon.muonIDDiscriminator()) continue;
    passedID = true;
    // Fill histos
    hIsolPtBefore ->Fill( muon.pt()  );
    hIsolEtaBefore->Fill( muon.eta() );
    if (fCommonPlotsIsEnabled()) hIsolVtxBefore->Fill(fCommonPlots->nVertices());


    //====== Apply Cut: muon isolation
    if (muon.relIsoDeltaBeta() > cfg_RelIsoCut) continue;
    passedIsol = true;
    // Fill histos
    hIsolPtAfter ->Fill( muon.pt()  );
    hIsolEtaAfter->Fill( muon.eta() );
    if (fCommonPlotsIsEnabled()) hIsolVtxAfter->Fill(fCommonPlots->nVertices());


    //====== After All Cuts
    hMuonPtPassed ->Fill( muon.pt());
    hMuonEtaPassed->Fill( muon.eta());


    // Determine pt and eta the of highest-pt muon
    if (muon.pt() > output.fHighestSelectedMuonPt) 
      {
	output.fHighestSelectedMuonPt = muon.pt();
	output.fHighestSelectedMuonEta = muon.eta();
      }

    // Save muon in vector of selected objects
    output.fSelectedMuons.push_back(muon);


    // Fill resolution histograms
    if (event.isMC()) 
      {
	hPtResolution ->Fill( (muon.pt()  - muon.MCmuon()->pt()  ) / muon.pt()  );
	hEtaResolution->Fill( (muon.eta() - muon.MCmuon()->eta() ) / muon.eta() );
	hPhiResolution->Fill( (muon.phi() - muon.MCmuon()->phi() ) / muon.phi() );
      }

  } // For-loop: All muons


  // Fill counters
  if ( passedPt   ) cSubPassedPt.increment();
  if ( passedEta  ) cSubPassedEta.increment();
  if ( passedID   ) cSubPassedID.increment();
  if ( passedIsol ) cSubPassedIsolation.increment();

  if (cfg_VetoMode) 
    {
      if (output.fSelectedMuons.size() == 0) cPassedMuonSelection.increment();
    } 
  else
    {
      if (output.fSelectedMuons.size() > 0 ) cPassedMuonSelection.increment();
    }

  return output;
}
