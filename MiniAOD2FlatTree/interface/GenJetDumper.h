#ifndef GenJetDumper_h
#define GenJetDumper_h

#include "FWCore/Framework/interface/EDFilter.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "DataFormats/Common/interface/View.h"
#include "DataFormats/Common/interface/Ptr.h"

#include <string>
#include <vector>

#include "TTree.h"
#include "DataFormats/Math/interface/LorentzVector.h"

#include "UCYHiggsAnalysis/MiniAOD2FlatTree/interface/BaseDumper.h"
#include "DataFormats/JetReco/interface/GenJet.h"

class GenJetDumper : public BaseDumper {
    public:
	GenJetDumper(edm::ConsumesCollector&& iConsumesCollector, std::vector<edm::ParameterSet>& psets);
	~GenJetDumper();

	void book(TTree*);
	bool fill(edm::Event&, const edm::EventSetup&);
	void reset();

    private:
	bool filter();
        edm::EDGetTokenT<reco::GenJetCollection> *genJetToken;

	// Input parameters/flags
	bool   cfg_debugMode;
	std::string cfg_branchName;
	int width;
	std::vector<short>  *charge;
	std::vector<double> *emEnergy;
	std::vector<double> *hadEnergy;
	std::vector<double> *auxEnergy;
	std::vector<double> *invisEnergy;
	std::vector<short>  *nGenConstituents;
	// std::vector< std::vector<unsigned short> > *genConstituents;

};
#endif
