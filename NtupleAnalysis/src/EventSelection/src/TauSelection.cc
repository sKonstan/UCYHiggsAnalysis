// -*- c++ -*-
#include "EventSelection/interface/TauSelection.h"

#include "Framework/interface/Exception.h"
#include "Framework/interface/ParameterSet.h"
#include "EventSelection/interface/CommonPlots.h"
#include "DataFormat/interface/Event.h"
#include "Framework/interface/HistoWrapper.h"
#include "DataFormat/interface/HLTTau.h"
//#include "Framework/interface/makeTH.h"

#include "Math/VectorUtil.h"

#include <cmath>

TauSelection::Data::Data() 
: fRtau(-1.0),
  fIsGenuineTau(false),
  fTauMisIDSF(1.0),
  fTauTriggerSF(1.0),
  fRtauAntiIsolatedTau(-1.0),
  fIsGenuineTauAntiIsolatedTau(false),
  fAntiIsolatedTauMisIDSF(1.0),
  fAntiIsolatedTauTriggerSF(1.0)
{ }


TauSelection::Data::~Data() { }


const Tau& TauSelection::Data::getSelectedTau() const { 
  if (!hasIdentifiedTaus())
    {
      throw hplus::Exception("Assert") << "You forgot to check if taus exist (hasIdentifiedTaus()), this message occurs when none exist!";
    }

  return fSelectedTaus[0];
}


const Tau& TauSelection::Data::getAntiIsolatedTau() const {
  if (!hasAntiIsolatedTaus()) 
    {
      throw hplus::Exception("Assert") << "You forgot to check if taus exist (hasAntiIsolatedTaus()), this message occurs when none exist!";
    }

  return fAntiIsolatedTaus[0];
}


TauSelection::TauSelection(const ParameterSet& config, EventCounter& eventCounter, HistoWrapper& histoWrapper, CommonPlots* commonPlots, const std::string& postfix)
: BaseSelection(eventCounter, histoWrapper, commonPlots, postfix),
  // Input Parameters (passed through python configuration file)
  cfg_TrgMatch(    config.getParameter<bool> ("TrgMatch")    ),
  cfg_TrgDeltaR(   config.getParameter<float>("TrgDeltaR")   ),
  cfg_PtCut(       config.getParameter<float>("PtCut")       ),
  cfg_EtaCut(      config.getParameter<float>("EtaCut")      ),
  cfg_LdgTrkPtCut( config.getParameter<float>("LdgTrkPtCut") ),
  cfg_Nprongs(     config.getParameter<int>  ("Nprongs")     ),
  cfg_RtauCut(     config.getParameter<float>("Rtau")        ),
  // Misidentification SF
  fEToTauMisIDSFRegion(   assignTauMisIDSFRegion( config, "E")   ),
  fEToTauMisIDSFValue(    assignTauMisIDSFValue(  config, "E")   ),
  fMuToTauMisIDSFRegion(  assignTauMisIDSFRegion( config, "Mu")  ),
  fMuToTauMisIDSFValue(   assignTauMisIDSFValue(  config, "Mu")  ),
  fJetToTauMisIDSFRegion( assignTauMisIDSFRegion( config, "Jet") ),
  fJetToTauMisIDSFValue(  assignTauMisIDSFValue(  config, "Jet") ),
  // Trigger SF
  fTauTriggerSFReader( config.getParameterOptional<ParameterSet>("tauTriggerSF") ),
  // Event counter for passing selection
  cPassedTauSelection(fEventCounter.addCounter("passed tau selection ("+postfix+")")),
  // Event sub-counters for passing selection 
  cSubAll(                        fEventCounter.addSubCounter("tau selection (" + postfix + ")", "All events")                    ),
  cSubPassedTriggerMatching(      fEventCounter.addSubCounter("tau selection (" + postfix + ")", "Passed trigger matching")       ),
  cSubPassedDecayMode(            fEventCounter.addSubCounter("tau selection (" + postfix + ")", "Passed decay mode")             ),
  cSubPassedGenericDiscriminators(fEventCounter.addSubCounter("tau selection (" + postfix + ")", "Passed generic discriminators") ),
  cSubPassedElectronDiscr(        fEventCounter.addSubCounter("tau selection (" + postfix + ")", "Passed e discr")                ),
  cSubPassedMuonDiscr(            fEventCounter.addSubCounter("tau selection (" + postfix + ")", "Passed mu discr")               ),
  cSubPassedPt(                   fEventCounter.addSubCounter("tau selection (" + postfix + ")", "Passed pt cut")                 ),
  cSubPassedEta(                  fEventCounter.addSubCounter("tau selection (" + postfix + ")", "Passed eta cut")                ),
  cSubPassedLdgTrk(               fEventCounter.addSubCounter("tau selection (" + postfix + ")", "Passed ldg.trk pt cut")         ),
  cSubPassedNprongs(              fEventCounter.addSubCounter("tau selection (" + postfix + ")", "Passed nprongs")                ),
  cSubPassedIsolation(            fEventCounter.addSubCounter("tau selection (" + postfix + ")", "Passed isolation")              ),
  cSubPassedRtau(                 fEventCounter.addSubCounter("tau selection (" + postfix + ")", "Passed Rtau")                   )
{ 
  initialize(config);
}


TauSelection::TauSelection(const ParameterSet& config)
: BaseSelection(),
  // Input Parameters (passed through python configuration file)
  cfg_TrgMatch(    config.getParameter<bool> ("TrgMatch")    ),
  cfg_TrgDeltaR(   config.getParameter<float>("TrgDeltaR")   ),
  cfg_PtCut(       config.getParameter<float>("PtCut")       ),
  cfg_EtaCut(      config.getParameter<float>("EtaCut")      ),
  cfg_LdgTrkPtCut( config.getParameter<float>("LdgTrkPtCut") ),
  cfg_Nprongs(     config.getParameter<int>  ("Nprongs")     ),
  cfg_RtauCut(     config.getParameter<float>("Rtau")        ), 
  // Misidentification SF
  fEToTauMisIDSFRegion(   assignTauMisIDSFRegion( config, "E")   ),
  fEToTauMisIDSFValue(    assignTauMisIDSFValue(  config, "E")   ),
  fMuToTauMisIDSFRegion(  assignTauMisIDSFRegion( config, "Mu")  ),
  fMuToTauMisIDSFValue(   assignTauMisIDSFValue(  config, "Mu")  ),
  fJetToTauMisIDSFRegion( assignTauMisIDSFRegion( config, "Jet") ),
  fJetToTauMisIDSFValue(  assignTauMisIDSFValue(  config, "Jet") ),
  // Trigger SF
  fTauTriggerSFReader(config.getParameterOptional<ParameterSet>("tauTriggerSF")),
  // Event counter for passing selection
  cPassedTauSelection(fEventCounter.addCounter("passed tau selection")),
  // Event sub-counters for passing selection 
  cSubAll(                        fEventCounter.addSubCounter("tau selection", "All events")                    ),
  cSubPassedTriggerMatching(      fEventCounter.addSubCounter("tau selection", "Passed trigger matching")       ),
  cSubPassedDecayMode(            fEventCounter.addSubCounter("tau selection", "Passed decay mode")             ),
  cSubPassedGenericDiscriminators(fEventCounter.addSubCounter("tau selection", "Passed generic discriminators") ),
  cSubPassedElectronDiscr(        fEventCounter.addSubCounter("tau selection", "Passed e discr")                ),
  cSubPassedMuonDiscr(            fEventCounter.addSubCounter("tau selection", "Passed mu discr")               ),
  cSubPassedPt(                   fEventCounter.addSubCounter("tau selection", "Passed pt cut")                 ),
  cSubPassedEta(                  fEventCounter.addSubCounter("tau selection", "Passed eta cut")                ),
  cSubPassedLdgTrk(               fEventCounter.addSubCounter("tau selection", "Passed ldg.trk pt cut")         ),
  cSubPassedNprongs(              fEventCounter.addSubCounter("tau selection", "Passed nprongs")                ),
  cSubPassedIsolation(            fEventCounter.addSubCounter("tau selection", "Passed isolation")              ),
  cSubPassedRtau(                 fEventCounter.addSubCounter("tau selection", "Passed Rtau")                   )
{ 
  initialize(config);
  bookHistograms(new TDirectory());
}


TauSelection::~TauSelection() { }


void TauSelection::initialize(const ParameterSet& config) {

  return;
}


void TauSelection::bookHistograms(TDirectory* dir) {
  TDirectory* subdir = fHistoWrapper.mkdir(HistoLevel::kDebug, dir, "tauSelection_"+sPostfix);

  hTriggerMatchDeltaR   = fHistoWrapper.makeTH<TH1F>( HistoLevel::kDebug, subdir, "triggerMatchDeltaR"  , "Trigger match #DeltaR"   , 60,  0.0,   3.0 );
  hTauPtTriggerMatched  = fHistoWrapper.makeTH<TH1F>( HistoLevel::kDebug, subdir, "tauPtTriggerMatched" , "Tau pT, trigger matched" , 40,  0.0, 400.0 );
  hTauEtaTriggerMatched = fHistoWrapper.makeTH<TH1F>( HistoLevel::kDebug, subdir, "tauEtaTriggerMatched", "Tau eta, trigger matched", 50, -2.5,   2.5 );
  hNPassed              = fHistoWrapper.makeTH<TH1F>( HistoLevel::kDebug, subdir, "tauNpassed"          , "Number of passed taus"   , 20,  0.0,  20.0 );

  // Resolutions
  hPtResolution  = fHistoWrapper.makeTH<TH1F>( HistoLevel::kDebug, subdir, "ptResolution" , "(reco pT - gen pT) / reco pT"   , 200, -1.0, 1.0 );
  hEtaResolution = fHistoWrapper.makeTH<TH1F>( HistoLevel::kDebug, subdir, "etaResolution", "(reco eta - gen eta) / reco eta", 200, -1.0, 1.0 );
  hPhiResolution = fHistoWrapper.makeTH<TH1F>( HistoLevel::kDebug, subdir, "phiResolution", "(reco phi - gen phi) / reco phi", 200, -1.0, 1.0 );

  // Isolation efficiency
  hIsolPtBefore  = fHistoWrapper.makeTH<TH1F>( HistoLevel::kDebug, subdir, "IsolPtBefore" , "Tau pT before isolation is applied"   , 40,  0.0, 400.0 );
  hIsolEtaBefore = fHistoWrapper.makeTH<TH1F>( HistoLevel::kDebug, subdir, "IsolEtaBefore", "Tau eta before isolation is applied"  , 50, -2.5,   2.5 );
  hIsolVtxBefore = fHistoWrapper.makeTH<TH1F>( HistoLevel::kDebug, subdir, "IsolVtxBefore", "Nvertices before isolation is applied", 60,  0.0,  60.0 );
  hIsolPtAfter   = fHistoWrapper.makeTH<TH1F>( HistoLevel::kDebug, subdir, "IsolPtAfter"  , "Tau pT before isolation is applied"   , 40,  0.0, 400.0 );
  hIsolEtaAfter  = fHistoWrapper.makeTH<TH1F>( HistoLevel::kDebug, subdir, "IsolEtaAfter" , "Tau eta before isolation is applied"  , 50, -2.5,   2.5 );
  hIsolVtxAfter  = fHistoWrapper.makeTH<TH1F>( HistoLevel::kDebug, subdir, "IsolVtxAfter" , "Nvertices before isolation is applied", 60,  0.0,  60.0 );

  return;
}


TauSelection::Data TauSelection::silentAnalyze(const Event& event) {
  ensureSilentAnalyzeAllowed(event.eventID());
  disableHistogramsAndCounters(); // Disable histogram filling and counter   
  Data myData = privateAnalyze(event);
  enableHistogramsAndCounters();

  return myData;
}


TauSelection::Data TauSelection::analyze(const Event& event) {
  ensureAnalyzeAllowed(event.eventID());
  TauSelection::Data data = privateAnalyze(event);

  // Send data to CommonPlots
  // if (fCommonPlots != nullptr) fCommonPlots->fillControlPlotsAfterTauSelection(event, data); // HIP
  if (fCommonPlots != nullptr) fCommonPlots->fillControlPlotsAtTauSelection(event, data); // new

  return data;
}


TauSelection::Data TauSelection::privateAnalyze(const Event& event) {
  Data output;
 
  cSubAll.increment();
  bool passedTrgMatch     = false;
  bool passedDecayMode    = false;
  bool passedGenericDiscr = false;
  bool passedEdiscr       = false;
  bool passedMuDiscr      = false;
  bool passedPt           = false;
  bool passedEta          = false;
  bool passedLdgTrkPt     = false;
  bool passedNprongs      = false;
  bool passedIsol         = false;
  bool passedRtau         = false;
  
  // Cache vector of trigger tau 4-momenta
  std::vector<math::LorentzVectorT<double>> myTriggerTauMomenta;
  for (HLTTau p: event.triggerTaus()) {
    myTriggerTauMomenta.push_back(p.p4());
  }


  // For-loop: All taus
  for (Tau tau: event.taus()) {


    //====== Apply Cut: trigger matching
    if ( !this->passTrgMatching(tau, myTriggerTauMomenta) ) continue;
    passedTrgMatch = true;


    //====== Apply Cut: decay mode
    if ( !this->passDecayModeFinding(tau) ) continue;   
    passedDecayMode = true;
    // Fill histos
    hTauPtTriggerMatched ->Fill( tau.pt()  );
    hTauEtaTriggerMatched->Fill( tau.eta() );


    //====== Apply Cut: generic discriminators
    if ( !this->passGenericDiscriminators(tau) ) continue;
    passedGenericDiscr = true;


    //====== Apply Cut: electron discrimator
    if ( !this->passElectronDiscriminator(tau) ) continue;
    passedEdiscr = true;


    //====== Apply Cut: muon discrimator
    if ( !this->passMuonDiscriminator(tau) ) continue;
    passedMuDiscr = true;


    //====== Apply Cut: pt
    if ( !this->passPtCut(tau) ) continue;
    passedPt = true;


    //====== Apply Cut: eta
    if ( !this->passEtaCut(tau) ) continue;
    passedEta = true;


    //====== Apply Cut: ldg. track pt cut
    if ( !this->passLdgTrkPtCut(tau) ) continue;
    passedLdgTrkPt = true;


    //====== Apply Cut: number of prongs
    if ( !this->passNprongsCut(tau) ) continue;
    passedNprongs = true;
    // Fill histos
    hIsolPtBefore ->Fill( tau.pt()  );
    hIsolEtaBefore->Fill( tau.eta() );
    if (fCommonPlotsIsEnabled()) hIsolVtxBefore->Fill(fCommonPlots->nVertices());


    //====== Apply Cut: tau isolation
    if ( !this->passIsolationDiscriminator(tau) )
      {
	output.fAntiIsolatedTaus.push_back(tau);
	continue;
      }
    passedIsol = true;
    // Fill histos
    hIsolPtAfter ->Fill( tau.pt()  );
    hIsolEtaAfter->Fill( tau.eta() );
    if (fCommonPlotsIsEnabled()) hIsolVtxAfter->Fill(fCommonPlots->nVertices());

    
    //====== Apply Cut: Rtau
    if (!this->passRtauCut(tau)) continue;
    passedRtau = true;

    
    //====== After All Cuts  
    output.fSelectedTaus.push_back(tau);
    
    // Fill resolution histograms 
    if (event.isMC()) 
      {
	hPtResolution ->Fill( (tau.pt()  - tau.MCVisibleTau()->pt()  ) / tau.pt()  );
	hEtaResolution->Fill( (tau.eta() - tau.MCVisibleTau()->eta() ) / tau.eta() );
	hPhiResolution->Fill( (tau.phi() - tau.MCVisibleTau()->phi() ) / tau.phi() );
      }

  } // For-loop: All taus
  
  // Fill histos
  hNPassed ->Fill( output.fSelectedTaus.size() );

  // If there are multiple taus, choose the one with highest pT
  std::sort(output.fSelectedTaus.begin()    , output.fSelectedTaus.end()     );
  std::sort(output.fAntiIsolatedTaus.begin(), output.fAntiIsolatedTaus.end() );

  
  // Fill data object
  if (output.fSelectedTaus.size())
    {
      output.fRtau = output.getSelectedTau().rtau();
      if ( event.isMC() ) output.fIsGenuineTau = output.getSelectedTau().isGenuineTau();
    }
  
  if (output.fAntiIsolatedTaus.size()) 
    {
      output.fRtauAntiIsolatedTau = output.getAntiIsolatedTau().rtau();
    if (event.isMC()) output.fIsGenuineTauAntiIsolatedTau = output.getAntiIsolatedTau().isGenuineTau();
    }

  if (fCommonPlots != nullptr) 
    {
    if (output.fSelectedTaus.size()) fCommonPlots->fillControlPlotsAfterTauSelection(event, output);
    }

  // Set tau misidentification SF value to data object
  if ( event.isMC() ) setTauMisIDSFValue(output);

  // Set tau trigger SF value to data object
  if ( event.isMC() ) 
    {
    if ( output.hasIdentifiedTaus() ) output.fTauTriggerSF = fTauTriggerSFReader.getScaleFactorValue(output.getSelectedTau().pt());
    
    if ( output.hasAntiIsolatedTaus() ) output.fAntiIsolatedTauTriggerSF = fTauTriggerSFReader.getScaleFactorValue(output.getAntiIsolatedTau().pt());
    }

  // Fill counters
  if (passedTrgMatch)     cSubPassedTriggerMatching.increment();
  if (passedDecayMode)    cSubPassedDecayMode.increment();
  if (passedGenericDiscr) cSubPassedGenericDiscriminators.increment();
  if (passedEdiscr)       cSubPassedElectronDiscr.increment();
  if (passedMuDiscr)      cSubPassedMuonDiscr.increment();
  if (passedPt)           cSubPassedPt.increment();
  if (passedEta)          cSubPassedEta.increment();
  if (passedLdgTrkPt)     cSubPassedLdgTrk.increment();
  if (passedNprongs)      cSubPassedNprongs.increment();
  if (passedIsol)         cSubPassedIsolation.increment();
  if (passedRtau)         cSubPassedRtau.increment();
  if (output.fSelectedTaus.size() > 0)  cPassedTauSelection.increment();

  return output;
}


bool TauSelection::passTrgMatching(const Tau& tau, std::vector<math::LorentzVectorT<double>>& trgTaus) const {
  if (!cfg_TrgMatch) return true;
  double myMinDeltaR = 9999.0;

  // For-loop: All trg-taus
  for (auto& p: trgTaus) {
    double myDeltaR = ROOT::Math::VectorUtil::DeltaR(p, tau.p4());
    myMinDeltaR = std::min(myMinDeltaR, myDeltaR);
  }
  
  hTriggerMatchDeltaR->Fill(myMinDeltaR);

  return (myMinDeltaR < cfg_TrgDeltaR);
}


bool TauSelection::passNprongsCut(const Tau& tau) const {

  if (cfg_Nprongs > 0) {
    
    if (cfg_Nprongs == 12) 
      {
	return (tau.decayMode() >= 0 && tau.decayMode() <= 4);
      } 
    else if (cfg_Nprongs == 13)
      {
	return ((tau.decayMode() >= 0 && tau.decayMode() <= 4) || (tau.decayMode() >= 10 && tau.decayMode() <= 14));
      }
    else if (cfg_Nprongs == 23) 
      {
	return (tau.decayMode() >= 5 && tau.decayMode() <= 14);
      } 
    else if (cfg_Nprongs == 123) 
      {
	return (tau.decayMode() >= 0 && tau.decayMode() <= 14);
      } 
    else 
      {
	return (tau.decayMode() >= (cfg_Nprongs-1)*5 && tau.decayMode() <= cfg_Nprongs*5-1);
      }
  }

  return true;
}


std::vector<TauSelection::TauMisIDRegionType> TauSelection::assignTauMisIDSFRegion(const ParameterSet& config, const std::string& label) const{
  std::vector<TauMisIDRegionType> result;
  if (config.getParameterOptional<float>("tauMisidetification"+label+"ToTauBarrelSF")) result.push_back(kBarrel);
  if (config.getParameterOptional<float>("tauMisidetification"+label+"ToTauEndcapSF")) result.push_back(kEndcap);
  if (config.getParameterOptional<float>("tauMisidetification"+label+"ToTauSF")) result.push_back(kFullCoverage);

  return result;
}


std::vector<float> TauSelection::assignTauMisIDSFValue(const ParameterSet& config, const std::string& label) const {
  std::vector<float> result;

  if (config.getParameterOptional<float>("tauMisidetification"+label+"ToTauBarrelSF"))
    {
    result.push_back(config.getParameter<float>("tauMisidetification"+label+"ToTauBarrelSF"));
    }

  if (config.getParameterOptional<float>("tauMisidetification"+label+"ToTauEndcapSF"))
    {
    result.push_back(config.getParameter<float>("tauMisidetification"+label+"ToTauEndcapSF"));
    }

  if (config.getParameterOptional<float>("tauMisidetification"+label+"ToTauSF"))
    {
      result.push_back(config.getParameter<float>("tauMisidetification"+label+"ToTauSF"));
    }

  return result;
}


void TauSelection::setTauMisIDSFValue(Data& data) {

  if (data.hasIdentifiedTaus()) 
    {
      if (!data.isGenuineTau())  data.fTauMisIDSF = setTauMisIDSFValueHelper(data.getSelectedTau());
    }

  if (data.hasAntiIsolatedTaus()) 
    {
      if (!data.getAntiIsolatedTauIsGenuineTau()) data.fAntiIsolatedTauMisIDSF = setTauMisIDSFValueHelper(data.getAntiIsolatedTau());
    }

  return;
}


float TauSelection::setTauMisIDSFValueHelper(const Tau& tau) {
  double eta = tau.eta();

  if (tau.isElectronToTau()) {
    for (size_t i = 0; i < fEToTauMisIDSFRegion.size(); ++i) 
      {
	if (tauMisIDSFBelongsToRegion(fEToTauMisIDSFRegion[i], eta)) return fEToTauMisIDSFValue[i];
      }
  } 
  else if (tau.isMuonToTau()) 
    {
      for (size_t i = 0; i < fMuToTauMisIDSFRegion.size(); ++i) 
	{
	  if (tauMisIDSFBelongsToRegion(fMuToTauMisIDSFRegion[i], eta))
	    return fMuToTauMisIDSFValue[i];
	}
    } 
  else if (tau.isJetToTau()) 
    {
      for (size_t i = 0; i < fJetToTauMisIDSFRegion.size(); ++i) 
	{
	  if (tauMisIDSFBelongsToRegion(fJetToTauMisIDSFRegion[i], eta))
	    return fJetToTauMisIDSFValue[i];
	}
    }

  return 1.0;
}


bool TauSelection::tauMisIDSFBelongsToRegion(TauMisIDRegionType region, double eta) {

  if (region == kFullCoverage) return true;
  else if (region == kBarrel)  return std::abs(eta) < 1.5;
  else if (region == kEndcap)  return std::abs(eta) > 1.5;

  // never reached
  return false;
}
