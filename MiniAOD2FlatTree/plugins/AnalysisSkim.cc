/** \class AnalysisSkim
 *
 *  
 *  Filter to select events for 
 *  tau+MET trigger MET-leg efficiency study
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
	std::vector<std::string> triggerBits;

        edm::EDGetTokenT<edm::View<pat::Jet>> jetToken;
        std::vector<std::string> jetUserFloats;

	double jetEtCut,jetEtaCut;
	int nJets;

        int nEvents, nSelectedEvents;
};

AnalysisSkim::AnalysisSkim(const edm::ParameterSet& iConfig)
: trgResultsToken(consumes<edm::TriggerResults>(iConfig.getParameter<edm::InputTag>("TriggerResults"))),
  jetToken(consumes<edm::View<pat::Jet>>(iConfig.getParameter<edm::InputTag>("JetCollection")))
{
    triggerBits        = iConfig.getParameter<std::vector<std::string> >("HLTPaths");

    jetUserFloats      = iConfig.getParameter<std::vector<std::string> >("JetUserFloats");

    jetEtCut           = iConfig.getParameter<double>("JetEtCut");
    jetEtaCut          = iConfig.getParameter<double>("JetEtaCut");                            
    nJets              = iConfig.getParameter<int>("NJets");

    nEvents         = 0;
    nSelectedEvents = 0;
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

    // Trigger bits
    edm::Handle<edm::TriggerResults> trghandle;
    iEvent.getByToken(trgResultsToken,trghandle);
    if(trghandle.isValid()){
        edm::TriggerResults tr = *trghandle;
        bool fromPSetRegistry;
        edm::Service<edm::service::TriggerNamesService> tns;
        std::vector<std::string> hlNames; 
        tns->getTrigPaths(tr, hlNames, fromPSetRegistry);
	bool passed = false;
        bool trgBitFound = false;
        for(size_t i = 0; i < triggerBits.size(); ++i){
	    std::regex hlt_re(triggerBits[i]);
	    int n = 0;
            for(std::vector<std::string>::const_iterator j = hlNames.begin(); j!= hlNames.end(); ++j){
		if (std::regex_search(*j, hlt_re)) {
		    trgBitFound = true;
		    if(trghandle->accept(n)) {
			passed = true;
                        break;
		    }
                }
		n++;
            }
        }
        if(!trgBitFound) {
            std::cout << "Skimming with trigger bit, but none of the triggers was found!" << std::endl;
            std::cout << "Looked for triggers:" << std::endl;
            for (auto& p: triggerBits) {
                std::cout << "    " << p << std::endl;
            }
            
            std::cout << "Available triggers in dataset:" << std::endl;
            for(std::vector<std::string>::const_iterator j = hlNames.begin(); j!= hlNames.end(); ++j){
                std::cout << "    " << *j << std::endl;
            }
            exit(1);
        }

	if(!passed) return false; 
    }

    edm::Handle<edm::View<pat::Jet> > jethandle;
    iEvent.getByToken(jetToken, jethandle);
    int njets = 0;
    if(jethandle.isValid()){
        for(size_t i=0; i<jethandle->size(); ++i) {
            const pat::Jet& obj = jethandle->at(i);

	    if(obj.p4().pt() < jetEtCut) continue;
	    if(fabs(obj.p4().eta()) > jetEtaCut) continue;
/*
	    bool passed = true;
	    for(size_t j = 0; j < jetUserFloats.size(); ++j){
		if(obj.userFloat(jetUserFloats[j]) < 0) {
		    passed = false;
		    break;
		}
	    }
	    if(!passed) continue;
*/
	    njets++;
	}
    }
    if(njets < nJets) return false;

    nSelectedEvents++;
    return true;
}

DEFINE_FWK_MODULE(AnalysisSkim);   

