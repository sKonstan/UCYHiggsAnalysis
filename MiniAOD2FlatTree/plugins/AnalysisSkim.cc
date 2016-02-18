/** \class AnalysisSkim
 *
 *  
 *  Filter to select events for 
 *  a given trigger efficiency study
 *
 *  \original author Sami Lehti  -  HIP Helsinki
 *  \editor Alexandros Attikis   -  UCY
 *
 */

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDFilter.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Utilities/interface/InputTag.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "DataFormats/Common/interface/View.h"
#include "DataFormats/Common/interface/Ptr.h"

#include "FWCore/Framework/interface/ConsumesCollector.h"
#include "FWCore/Framework/interface/TriggerNamesService.h"
#include "DataFormats/Common/interface/TriggerResults.h"

#include "DataFormats/PatCandidates/interface/Jet.h"

#include "FWCore/Framework/interface/LuminosityBlock.h"

#include <iostream>
#include <regex>

class AnalysisSkim : public edm::EDFilter {

public:
  explicit AnalysisSkim(const edm::ParameterSet&);
  ~AnalysisSkim();

  virtual bool filter(edm::Event&, const edm::EventSetup& );

private:
  edm::EDGetTokenT<edm::TriggerResults> trgResultsToken;
  std::vector<std::string> cfg_triggerBits;

  edm::EDGetTokenT<edm::View<pat::Jet>> jetToken;
  std::vector<std::string> cfg_jetUserFloats;

  edm::InputTag cfg_jetCollection;
  bool cfg_debugMode;
  double cfg_jetEtCut;
  double cfg_jetEtaCut;
  int cfg_nJets;

  int nEvents, nSelectedEvents;
  int width;
};


AnalysisSkim::AnalysisSkim(const edm::ParameterSet& iConfig)
  : trgResultsToken(consumes<edm::TriggerResults>(iConfig.getParameter<edm::InputTag>("TriggerResults"))),
    jetToken(consumes<edm::View<pat::Jet>>(iConfig.getParameter<edm::InputTag>("JetCollection")))
{
  
  cfg_triggerBits    = iConfig.getParameter<std::vector<std::string> >("HLTPaths");
  cfg_jetUserFloats  = iConfig.getParameter<std::vector<std::string> >("JetUserFloats");
  cfg_jetCollection  = iConfig.getParameter<edm::InputTag>("JetCollection");
  cfg_jetEtCut       = iConfig.getParameter<double>("JetEtCut");
  cfg_jetEtaCut      = iConfig.getParameter<double>("JetEtaCut");                            
  cfg_nJets          = iConfig.getParameter<int>("NJets");
  cfg_debugMode      = iConfig.getParameter<bool>("debugMode");
  nEvents            = 0;
  nSelectedEvents    = 0;
  
  width = 12;
}


AnalysisSkim::~AnalysisSkim(){
  double eff = 0;
  if(nEvents > 0) eff = ((double)nSelectedEvents)/((double) nEvents);
  std::cout << "AnalysisSkim: " //  	edm::LogVerbatim("AnalysisSkim") 
	    << " Number_events_read " << nEvents
	    << " Number_events_kept " << nSelectedEvents
	    << " Efficiency         " << eff << std::endl;
}


bool AnalysisSkim::filter(edm::Event& iEvent, const edm::EventSetup& iSetup ){

  nEvents++;

  // Create a trigger handle & get the trigger results
  edm::Handle<edm::TriggerResults> trghandle;
  iEvent.getByToken(trgResultsToken, trghandle);

  // Sanity check
  if(trghandle.isValid()){
    edm::TriggerResults tr = *trghandle;
    bool fromPSetRegistry;

    // See: https://cmssdt.cern.ch/SDT/doxygen/CMSSW_7_5_2/doc/html/dd/d62/classedm_1_1service_1_1TriggerNamesService.html#ab131a2837bc895a40e401678d6c7844e
    edm::Service<edm::service::TriggerNamesService> tns;
    std::vector<std::string> hlNames; 

    tns->getTrigPaths(tr, hlNames, fromPSetRegistry);
    bool passed      = false;
    bool trgBitFound = false;
    
    // Print debugging info?
    if (cfg_debugMode){
      std::cout << "\n" << std::string(width*10, '=') << std::endl;
      std::cout << std::setw(5)     << "Index"    << std::setw(width*5) << "HLT (cfg)"   << std::setw(width) << "Bit Found"
		<< std::setw(width) << "Fired"    << std::setw(width)   << "# Triggers Searched"
		<< std::endl;
      std::cout << std::string(width*10, '=') << std::endl;
    }

    // For-loop: All trigger bits
    for(size_t i = 0; i < cfg_triggerBits.size(); ++i){
      std::regex hlt_re(cfg_triggerBits[i]);
      int n = 0;

      // For-loop: All trigger bits
      for(std::vector<std::string>::const_iterator j = hlNames.begin(); j!= hlNames.end(); ++j){
	// std::cout << "hlNames_it = " << *j << std::endl;

	// Look for the specific trigger name
	if (std::regex_search(*j, hlt_re)) {
	  trgBitFound = true;

	  // Get the trigger bit for the specific trigger, then break loop
	  if(trghandle->accept(n)) {
	    passed = true;
	    break;
	  }

	}// if (std::regex_search(*j, hlt_re)) {
	n++;
      }// for(std::vector<std::string>::const_iterator j = hlNames.begin(); j!= hlNames.end(); ++j){

      // Print debugging info?
      if (cfg_debugMode){
	std::cout << std::setw(5)     << i        << std::setw(width*5) << cfg_triggerBits[i] << std::setw(width) << trgBitFound
		  << std::setw(width) << passed   << std::setw(width)   << n                  
		  << std::endl;
      }

    }// for(size_t i = 0; i < cfg_triggerBits.size(); ++i){

    // If none of the trigger paths found inform user
    if(!trgBitFound) {
      std::cout << "Skimming with trigger bit, but none of the triggers was found!" << std::endl;
      std::cout << "Looked for triggers:" << std::endl;
      for (auto& p: cfg_triggerBits) {
	std::cout << "    " << p << std::endl;
      }

      // Inform user of available triggers
      std::cout << "Available triggers in dataset:" << std::endl;
      for(std::vector<std::string>::const_iterator j = hlNames.begin(); j!= hlNames.end(); ++j){
	std::cout << "    " << *j << std::endl;
      }
      exit(1);
    }
    
    if(!passed) return false; 
  }

  // Get the pat::Jets
  edm::Handle<edm::View<pat::Jet> > jethandle;
  iEvent.getByToken(jetToken, jethandle);
  int njets = 0;

  // Sanity Check
  if(jethandle.isValid()){

    // Print debugging info?
    if (cfg_debugMode){
      std::cout << "\n" << std::string(width*10, '=') << std::endl;
      std::cout << std::setw(5)       << "Index"         << std::setw(width*2) << "Jet Collection"
		<< std::setw(width)   << "Et"            << std::setw(width)   << "Eta"            << std::setw(width) << "Phi" << std::setw(width) << "Energy"
		<< std::setw(width+5) << "# Jets Passed"
		<< std::endl;
      std::cout << std::string(width*10, '=') << std::endl;
    }


    // For-loop: All Jets
    for(size_t i=0; i<jethandle->size(); ++i) {

      // Get the pat::Jet
      const pat::Jet& obj = jethandle->at(i);

      if (cfg_debugMode){
	std::cout << std::setw(5)       << i              << std::setw(width*2) << cfg_jetCollection.label()
		  << std::setw(width)   << obj.p4().pt()  << std::setw(width)   << obj.p4().eta()   << std::setw(width) << obj.p4().phi() << std::setw(width) << obj.p4().energy()
		  << std::setw(width+5) << njets
		  << std::endl;
      }
    
      // Apply kinematical cuts
      if( obj.p4().pt()        < cfg_jetEtCut ) continue;
      if( fabs(obj.p4().eta()) > cfg_jetEtaCut) continue;

      /*
	bool passed = true;
	for(size_t j = 0; j < cfg_jetUserFloats.size(); ++j){
	if(obj.userFloat(cfg_jetUserFloats[j]) < 0) {
	passed = false;
	break;
	}
	}
	if(!passed) continue;
      */

      njets++;
    }
  }

  // Apply Jet Multiplicity Cut
  if(njets < cfg_nJets) return false;

  nSelectedEvents++;
  return true;
}

DEFINE_FWK_MODULE(AnalysisSkim);   

