// -*- c++ -*-
#include "EventSelection/interface/METSelection.h"

#include "Framework/interface/ParameterSet.h"
#include "EventSelection/interface/CommonPlots.h"
#include "DataFormat/interface/Event.h"
#include "Framework/interface/HistoWrapper.h"
#include "Framework/interface/Exception.h"
//#include "Framework/interface/makeTH.h"

METSelection::Data::Data() 
: bPassedSelection(false),
  fMETSignificance(-1.0),
  fMETTriggerSF(0.0)
{ }


METSelection::Data::~Data() { }


const math::XYVectorD& METSelection::Data::getMET() const {
  if (fSelectedMET.size() == 0) {
    throw hplus::Exception("assert") << "No MET stored into result container!";
  }

  return fSelectedMET[0];
}


METSelection::METSelection(const ParameterSet& config, EventCounter& eventCounter, HistoWrapper& histoWrapper, CommonPlots* commonPlots, const std::string& postfix)
: BaseSelection(eventCounter, histoWrapper, commonPlots, postfix),
  cfg_METCut(config, "METCut"),
  cfg_METSignificanceCut(config, "METSignificanceCut"),
  cfg_METTypeString(      config.getParameter<std::string>("METType")               ),
  cfg_PhiCorrections(     config.getParameter<bool>("PhiCorrections")               ),
  cfg_METTriggerSFReader( config.getParameterOptional<ParameterSet>("metTriggerSF") ),
  // Event counter for passing selection
  cPassedMETSelection( fEventCounter.addCounter("passed MET selection (" + postfix + ")") )
{
  initialize(config);
}


METSelection::METSelection(const ParameterSet& config)
: BaseSelection(),
  cfg_METCut(config, "METCut"),
  cfg_METSignificanceCut(config, "METSignificanceCut"),
  cfg_METTypeString(      config.getParameter<std::string>("METType")               ),
  cfg_PhiCorrections(     config.getParameter<bool>("PhiCorrections")               ),
  cfg_METTriggerSFReader( config.getParameterOptional<ParameterSet>("metTriggerSF") ),
  // Event counter for passing selection
  cPassedMETSelection(fEventCounter.addCounter("passed MET selection"))
{
  initialize(config);
  bookHistograms(new TDirectory());
}


METSelection::~METSelection() { }


void METSelection::initialize(const ParameterSet& config) {

  if (cfg_METTypeString == "GenMET")              cfg_METType = kGenMET;
  else if (cfg_METTypeString == "L1MET")          cfg_METType = kL1MET;
  else if (cfg_METTypeString == "HLTMET")         cfg_METType = kHLTMET;
  else if (cfg_METTypeString == "CaloMET")        cfg_METType = kCaloMET;
  else if (cfg_METTypeString == "MET_Type1")      cfg_METType = kType1MET;
  else if (cfg_METTypeString == "MET_Type1_NoHF") cfg_METType = kType1MET_noHF;
  else if (cfg_METTypeString == "MET_Puppi")      cfg_METType = kPuppiMET;
  else 
    {
      throw hplus::Exception("config") << "Invalid MET 'type' chosen in config! Options are: MET_Type1, MET_Type1_NoHF, MET_Puppi, GenMET, L1MET, HLTMET, CaloMET";
    }

  return;
}


void METSelection::bookHistograms(TDirectory* dir) {
  TDirectory* subdir = fHistoWrapper.mkdir(HistoLevel::kDebug, dir, "metSelection_" + sPostfix);

  hMET    = fHistoWrapper.makeTH<TH1F>( HistoLevel::kDebug, subdir, "hMET"   , "MET"             ,  80,  0.0, 800.0 );
  hMETSig = fHistoWrapper.makeTH<TH1F>( HistoLevel::kDebug, subdir, "hMETSig", "MET Significance", 100,  0.0, 100.0 );

  return;
}


METSelection::Data METSelection::silentAnalyze(const Event& event, int nVertices) {
  ensureSilentAnalyzeAllowed(event.eventID());
  disableHistogramsAndCounters(); // Disable histogram filling and counter
  Data myData = privateAnalyze(event, nVertices);
  enableHistogramsAndCounters();

  return myData;
}


METSelection::Data METSelection::analyze(const Event& event, int nVertices) {
  ensureAnalyzeAllowed(event.eventID());
  METSelection::Data data = privateAnalyze(event, nVertices);

  // Send data to CommonPlots
  if (fCommonPlots != nullptr) fCommonPlots->fillControlPlotsAtMETSelection(event, data);

  return data;
}


METSelection::Data METSelection::privateAnalyze(const Event& iEvent, int nVertices) {
  Data output;

  
  output.fSelectedMET.push_back( iEvent.met().p2() ); 
  output.fMETSignificance = iEvent.met().significance();
  // Fill histos
  hMET   ->Fill( iEvent.met().et()     );
  hMETSig->Fill( iEvent.met().significance() );


  //====== Apply Cut:  phi corrections (FIXME: not implemented)
  

  // Set tau trigger SF value to data object
  double metValue = output.getMET().R();
  if (iEvent.isMC()) 
    {
      output.fMETTriggerSF = cfg_METTriggerSFReader.getScaleFactorValue(metValue);
    } 
  

  //====== Apply Cut: MET
  if ( !cfg_METCut.passedCut(metValue) ) return output;
  
 
  //====== Apply Cut: MET significance
  if ( !cfg_METSignificanceCut.passedCut(iEvent.met().significance()) ) return output;
  

  //====== Passed MET selection
  output.bPassedSelection = true;
  cPassedMETSelection.increment();  
  
  return output;
}
