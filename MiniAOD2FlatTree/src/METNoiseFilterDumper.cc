#include "UCYHiggsAnalysis/MiniAOD2FlatTree/interface/METNoiseFilterDumper.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Common/interface/TriggerNames.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
//#include "DataFormats/METReco/interface/BeamHaloSummary.h"
#include "DataFormats/Common/interface/TriggerResults.h"

#include <iostream>

METNoiseFilterDumper::METNoiseFilterDumper(edm::ConsumesCollector&& iConsumesCollector, const edm::ParameterSet& pset)
  : useFilter(false),
    booked(false),
    trgResultsToken(iConsumesCollector.consumes<edm::TriggerResults>(pset.getParameter<edm::InputTag>("triggerResults"))),
    hbheNoiseTokenRun2LooseToken(iConsumesCollector.consumes<bool>(pset.getParameter<edm::InputTag>("hbheNoiseTokenRun2LooseSource"))),
    hbheNoiseTokenRun2TightToken(iConsumesCollector.consumes<bool>(pset.getParameter<edm::InputTag>("hbheNoiseTokenRun2TightSource"))),
    hbheIsoNoiseToken(iConsumesCollector.consumes<bool>(pset.getParameter<edm::InputTag>("hbheIsoNoiseTokenSource"))),
    bPrintTriggerResultsList(pset.getUntrackedParameter<bool>("printTriggerResultsList")),
    bTriggerResultsListPrintedStatus(false),
    fFilters(pset.getParameter<std::vector<std::string>>("filtersFromTriggerResults"))
{ 

  // Other auxiliary variables
  width          = 10;
  cfg_debugMode  = pset.getUntrackedParameter<bool>("debugMode");
  cfg_branchName = pset.getUntrackedParameter<std::string>("branchName","");

}


METNoiseFilterDumper::~METNoiseFilterDumper() { }


void METNoiseFilterDumper::book(TTree* tree){
  theTree = tree;
  booked = true;
  
  bFilters = new bool[fFilters.size()+3];

  // For-loop: All filters
  for (size_t i = 0; i < fFilters.size(); ++i) {
    theTree->Branch( (cfg_branchName + "_" + fFilters[i]).c_str(), &bFilters[i]);
  }

  // Create the TTree branches
  theTree->Branch( (cfg_branchName + "_hbheNoiseTokenRun2Loose").c_str(), &bFilters[fFilters.size()]   );
  theTree->Branch( (cfg_branchName + "_hbheNoiseTokenRun2Tight").c_str(), &bFilters[fFilters.size()+1] );
  theTree->Branch( (cfg_branchName + "_hbheIsoNoiseToken")      .c_str(), &bFilters[fFilters.size()+2] );
  
  return;
}


bool METNoiseFilterDumper::fill(edm::Event& iEvent, const edm::EventSetup& iSetup){

  // Obtain trigger results object (some filters have been stored as paths there)
  edm::Handle<edm::TriggerResults> trgResults;
  iEvent.getByToken(trgResultsToken, trgResults);
  const edm::TriggerNames& triggerNames = iEvent.triggerNames(*trgResults);

  // Sanity check
  if (!trgResults.isValid()) throw cms::Exception("Assert") << "METFilters: edm::TriggerResults object is not valid!";

  // Print info if requested
  if (!bTriggerResultsListPrintedStatus && bPrintTriggerResultsList) printAvailableFilters(iEvent, trgResults);
  
  // Print debugging info?                                                                                                                                                         
  if (cfg_debugMode){
    std::cout << "\n" << std::setw(width*8) << cfg_branchName << std::endl;
    std::cout << std::string(width*17, '=') << std::endl;
    std::cout << std::setw(5)       << "Index"
	      << std::setw(width*5) << "Trigger Name"   << std::setw(width*4)  << "Filter"  << std::setw(width)   << "Accept" 
	      << std::endl;
    std::cout << std::string(width*17, '=') << std::endl;
  }


  // For-loop: All filters
  for (size_t i = 0; i < fFilters.size(); ++i) {
    bool found = false;

    // For-loop: all trigger results
    for (size_t j = 0; j < trgResults->size(); ++j) {

      // Found the filter that corresponds to the given trigger
      if ( fFilters[i].compare(triggerNames.triggerName(j) ) == 0) {
        found = true;

	// Store results
        bFilters[i] = trgResults->accept(j);

	if (cfg_debugMode){ 
	  std::cout << std::setw(5) << i << std::setw(width*5) << triggerNames.triggerName(j) << std::setw(width*4)  << fFilters[i]  
		    << std::setw(width)  << trgResults->accept(j) << std::endl;	
	}
      }

    }// for (size_t j = 0; j < trgResults->size(); ++j) {
    
    if (!found) {
      printAvailableFilters(iEvent, trgResults);
      throw cms::Exception("Assert") << "METFilters: key '" << fFilters[i] << "' not found in TriggerResults (see above list for available filters)!";
    }

  }

  // Get handle for HB/HE Noise (Loose)
  edm::Handle<bool> hbheNoiseLooseHandle;
  iEvent.getByToken(hbheNoiseTokenRun2LooseToken, hbheNoiseLooseHandle);
  bFilters[fFilters.size()] = *hbheNoiseLooseHandle;

  // Get handle for HB/HE Noise (Tight)
  edm::Handle<bool> hbheNoiseTightHandle;
  iEvent.getByToken(hbheNoiseTokenRun2TightToken, hbheNoiseTightHandle);
  bFilters[fFilters.size()+1] = *hbheNoiseTightHandle;

  // Get handle for HB/HE Iso Noise
  edm::Handle<bool> hbheIsoNoiseHandle;
  iEvent.getByToken(hbheIsoNoiseToken, hbheIsoNoiseHandle);
  bFilters[fFilters.size()+2] = *hbheIsoNoiseHandle;
  
  return filter();
}


void METNoiseFilterDumper::printAvailableFilters(edm::Event& iEvent, edm::Handle<edm::TriggerResults>& trgResults) {
  const edm::TriggerNames& triggerNames = iEvent.triggerNames(*trgResults);
  std::cout << "=== TriggerResults list including METFilters (for information):" << std::endl;

  // Print debugging info?
  std::cout << "\n" << std::setw(width*8) << cfg_branchName << std::endl;
  std::cout << std::string(width*12, '=') << std::endl;
  std::cout << std::setw(5)       << "Index"
	    << std::setw(width*5) << "Trigger Name"   << std::setw(width)   << "Accept" 
	    << std::endl;
  std::cout << std::string(width*12, '=') << std::endl;

  // For-loop: All trigger results
  for (size_t i = 0; i < trgResults->size(); ++i) {
    std::cout << std::setw(5)       << i
	      << std::setw(width*5) << triggerNames.triggerName(i) << std::setw(width)  << trgResults->accept(i)
	      << std::endl;
    // std::cout << "  " <<  triggerNames.triggerName(i) << " status=" << trgResults->accept(i) << std::endl;
  }
  std::cout << "\n" << std::endl;
  
  bTriggerResultsListPrintedStatus = true;

  return;
}

bool METNoiseFilterDumper::filter(){
  return true;
}

void METNoiseFilterDumper::reset(){
  if(!booked) return;

  return;
}
