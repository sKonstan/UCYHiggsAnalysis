// -*- c++ -*-
#include "EventSelection/interface/ElectronSelection.h"

#include "Framework/interface/ParameterSet.h"
#include "EventSelection/interface/CommonPlots.h"
#include "DataFormat/interface/Event.h"
#include "Framework/interface/HistoWrapper.h"
//#include "Framework/interface/makeTH.h"

ElectronSelection::Data::Data() 
: fHighestSelectedElectronPt(0.0),
  fHighestSelectedElectronEta(0.0) { }


ElectronSelection::Data::~Data() { }


ElectronSelection::ElectronSelection(const ParameterSet& config, EventCounter& eventCounter, HistoWrapper& histoWrapper, CommonPlots* commonPlots, const std::string& postfix)
: BaseSelection(eventCounter, histoWrapper, commonPlots, postfix),
  // Input Parameters (passed through python configuration file)
  cfg_PtCut(config.getParameter<float>("PtCut")),
  cfg_EtaCut(config.getParameter<float>("EtaCut")),
  cfg_RelIsolString(config.getParameter<std::string>("RelIsolString")),
  cfg_RelIsoCut(-1.0),
  cfg_VetoMode(false),
  // Event counter for passing selection
  cPassedElectronSelection( fEventCounter.addCounter("passed e selection ("+postfix+")") ),
  // Event sub-counters for passing selection
  cSubAll(             fEventCounter.addSubCounter("e selection (" + postfix + ")", "All events")       ),
  cSubPassedPt(        fEventCounter.addSubCounter("e selection (" + postfix + ")", "Passed pt cut")    ),
  cSubPassedEta(       fEventCounter.addSubCounter("e selection (" + postfix + ")", "Passed eta cut")   ),
  cSubPassedID(        fEventCounter.addSubCounter("e selection (" + postfix + ")", "Passed ID")        ),
  cSubPassedIsolation( fEventCounter.addSubCounter("e selection (" + postfix + ")", "Passed isolation") )
{
  initialize(config, postfix);
}


ElectronSelection::ElectronSelection(const ParameterSet& config, const std::string& postfix)
: BaseSelection(),
  // Input Parameters (passed through python configuration file)
  cfg_PtCut(config.getParameter<float>("PtCut")),
  cfg_EtaCut(config.getParameter<float>("EtaCut")),
  cfg_RelIsolString(config.getParameter<std::string>("RelIsolString")),
  cfg_RelIsoCut(-1.0),
  cfg_VetoMode(false),
  // Event counter for passing selection
  cPassedElectronSelection(fEventCounter.addCounter("passed e selection ("+postfix+")")),
  // Event Sub-counters for passing selection
  cSubAll(            fEventCounter.addSubCounter("e selection (" + postfix + ")", "All events")       ),
  cSubPassedPt(       fEventCounter.addSubCounter("e selection (" + postfix + ")", "Passed pt cut")    ),
  cSubPassedEta(      fEventCounter.addSubCounter("e selection (" + postfix + ")", "Passed eta cut")   ),
  cSubPassedID(       fEventCounter.addSubCounter("e selection (" + postfix + ")", "Passed ID")        ),
  cSubPassedIsolation(fEventCounter.addSubCounter("e selection (" + postfix + ")", "Passed isolation") )
{
  initialize(config, postfix);
  bookHistograms(new TDirectory());
}


ElectronSelection::~ElectronSelection() { }


void ElectronSelection::initialize(const ParameterSet& config, const std::string& postfix) {
  if (postfix.find("veto") != std::string::npos || postfix.find("Veto") != std::string::npos) cfg_VetoMode = true;

  if (cfg_RelIsolString == "veto" || cfg_RelIsolString == "Veto") 
    {
      cfg_RelIsoCut = 0.15; // Based on 2012 cut based isolation
    } 
  else if (cfg_RelIsolString == "none" || cfg_RelIsolString == "None")
    {
      cfg_RelIsoCut = 99999.99;
    }
  else if (cfg_RelIsolString == "tight" || cfg_RelIsolString == "Tight")
    {
      cfg_RelIsoCut = 0.10; // Based on 2012 cut based isolation
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
      throw hplus::Exception("config") << "Invalid electronIsolation option '" << cfg_RelIsolString << "'! Options: 'veto', 'tight'";
    }

  return;
}


void ElectronSelection::bookHistograms(TDirectory* dir) {
  TDirectory* subdir = fHistoWrapper.mkdir(HistoLevel::kDebug, dir, "eSelection_" + sPostfix);

  hElectronPtAll     = fHistoWrapper.makeTH<TH1F>( HistoLevel::kDebug, subdir, "electronPtAll"    , "Electron pT, all"    , 40,  0.0, 400.0 );
  hElectronEtaAll    = fHistoWrapper.makeTH<TH1F>( HistoLevel::kDebug, subdir, "electronEtaAll"   , "Electron eta, all"   , 50, -2.5,   2.5 );
  hElectronPtPassed  = fHistoWrapper.makeTH<TH1F>( HistoLevel::kDebug, subdir, "electronPtPassed" , "Electron pT, passed" , 40,  0.0, 400.0 );
  hElectronEtaPassed = fHistoWrapper.makeTH<TH1F>( HistoLevel::kDebug, subdir, "electronEtaPassed", "Electron eta, passed", 50, -2.5,   2.5 );

  // Resolutions
  hPtResolution  = fHistoWrapper.makeTH<TH1F>( HistoLevel::kDebug, subdir, "ptResolution" , "(reco pT - gen pT) / reco pT"   , 200, -1.0, 1.0 );
  hEtaResolution = fHistoWrapper.makeTH<TH1F>( HistoLevel::kDebug, subdir, "etaResolution", "(reco eta - gen eta) / reco eta", 200, -1.0, 1.0 );
  hPhiResolution = fHistoWrapper.makeTH<TH1F>( HistoLevel::kDebug, subdir, "phiResolution", "(reco phi - gen phi) / reco phi", 200, -1.0, 1.0 );

  // Isolation efficiency
  hIsolPtBefore  = fHistoWrapper.makeTH<TH1F>( HistoLevel::kDebug, subdir, "IsolPtBefore" , "Electron pT before isolation is applied" , 40,  0.0, 400.0 );
  hIsolEtaBefore = fHistoWrapper.makeTH<TH1F>( HistoLevel::kDebug, subdir, "IsolEtaBefore", "Electron eta before isolation is applied", 50, -2.5,   2.5 );
  hIsolVtxBefore = fHistoWrapper.makeTH<TH1F>( HistoLevel::kDebug, subdir, "IsolVtxBefore", "Nvertices before isolation is applied"   , 60,  0.0,  60.0 );
  hIsolPtAfter   = fHistoWrapper.makeTH<TH1F>( HistoLevel::kDebug, subdir, "IsolPtAfter"  , "Electron pT before isolation is applied" , 40,  0.0, 400.0 );
  hIsolEtaAfter  = fHistoWrapper.makeTH<TH1F>( HistoLevel::kDebug, subdir, "IsolEtaAfter" , "Electron eta before isolation is applied", 50, -2.5,   2.5 );
  hIsolVtxAfter  = fHistoWrapper.makeTH<TH1F>( HistoLevel::kDebug, subdir, "IsolVtxAfter" , "Nvertices before isolation is applied"   , 60,  0.0,  60.0 );

  return;
}


ElectronSelection::Data ElectronSelection::silentAnalyze(const Event& event) {
  ensureSilentAnalyzeAllowed(event.eventID());
  disableHistogramsAndCounters(); // Disables histogram filling and counter
  Data myData = privateAnalyze(event);
  enableHistogramsAndCounters();

  return myData;
}


ElectronSelection::Data ElectronSelection::analyze(const Event& event) {
  ensureAnalyzeAllowed(event.eventID());
  ElectronSelection::Data data = privateAnalyze(event);

  // Send data to CommonPlots
  if (fCommonPlotsIsEnabled()) fCommonPlots->fillControlPlotsAtElectronSelection(event, data);

  return data;
}


ElectronSelection::Data ElectronSelection::privateAnalyze(const Event& event) {
  Data output;
  cSubAll.increment();
  bool passedPt   = false;
  bool passedEta  = false;
  bool passedID   = false;
  bool passedIsol = false;

  // For-loop: All electrons
  for(Electron electron: event.electrons()) {

    // Fill histos
    hElectronPtAll ->Fill( electron.pt()  );
    hElectronEtaAll->Fill( electron.eta() );


    //====== Apply Cut: pt
    if ( electron.pt() < cfg_PtCut ) continue;
    passedPt = true;


    //====== Apply Cut: eta
    if ( std::fabs(electron.eta()) > cfg_EtaCut ) continue;
    passedEta = true;


    //====== Apply Cut: electron ID (see DataFormat/interface/Electron.h)
    if ( !electron.electronIDDiscriminator() ) continue;
    passedID = true;
    // Fill histos
    hIsolPtBefore ->Fill( electron.pt()  );
    hIsolEtaBefore->Fill( electron.eta() );
    if ( fCommonPlotsIsEnabled() ) hIsolVtxBefore->Fill(fCommonPlots->nVertices());


    //====== Apply Cut: electron isolation
    if (electron.relIsoDeltaBeta() > cfg_RelIsoCut) continue;
    passedIsol = true;
    // Fill histos
    hIsolPtAfter ->Fill( electron.pt()  );
    hIsolEtaAfter->Fill( electron.eta() );
    if ( fCommonPlotsIsEnabled() ) hIsolVtxAfter->Fill(fCommonPlots->nVertices());


    //====== After All Cuts
    hElectronPtPassed ->Fill( electron.pt()  );
    hElectronEtaPassed->Fill( electron.eta() );


    // Determine pt and eta the of highest-pt electron
    if (electron.pt() > output.fHighestSelectedElectronPt) 
      {
	output.fHighestSelectedElectronPt  = electron.pt();
	output.fHighestSelectedElectronEta = electron.eta();
      }

    // Save electrons in vector of selected objects
    output.fSelectedElectrons.push_back(electron);


    // Fill resolution histograms
    if ( event.isMC() ) 
      {
	hPtResolution ->Fill( (electron.pt()  - electron.MCelectron()->pt()  ) / electron.pt()  );
	hEtaResolution->Fill( (electron.eta() - electron.MCelectron()->eta() ) / electron.eta() );
	hPhiResolution->Fill( (electron.phi() - electron.MCelectron()->phi() ) / electron.phi() );
      }

  } // For-loop: All electrons


  // Fill counters
  if ( passedPt   ) cSubPassedPt.increment();
  if ( passedEta  ) cSubPassedEta.increment();
  if ( passedID   ) cSubPassedID.increment();
  if ( passedIsol ) cSubPassedIsolation.increment();

  if (cfg_VetoMode) 
    {
      if (output.fSelectedElectrons.size() == 0) cPassedElectronSelection.increment();
    }
  else 
    {
      if (output.fSelectedElectrons.size() > 0 ) cPassedElectronSelection.increment();
    }


  return output;
}
