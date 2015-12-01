#ifndef GenMETDumper_h
#define GenMETDumper_h

#include "FWCore/Framework/interface/EDFilter.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/Framework/interface/ConsumesCollector.h"
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "DataFormats/Common/interface/View.h"
#include "DataFormats/Common/interface/Ptr.h"

namespace reco {
  class GenMET;
}

#include <string>
#include <vector>

#include "TTree.h"
#include "DataFormats/Math/interface/LorentzVector.h"

class GenMETDumper {
    public:
	GenMETDumper(edm::ConsumesCollector&& iConsumesCollector, std::vector<edm::ParameterSet>& psets);
	~GenMETDumper();

	void book(TTree*);
	bool fill(edm::Event&, const edm::EventSetup&);
	void reset();

    private:
	bool filter();
        bool useFilter;
	bool booked;

	std::vector<edm::ParameterSet> inputCollections;
	edm::EDGetTokenT<edm::View<reco::GenMET>> *token;
	int width;
	bool cfg_debugMode;
	std::string cfg_branchName;

        double GenMET;
        double GenMET_phi;
	double GenMET_auxEnergy;
	double GenMET_ChargedEMEt;
	double GenMET_ChargedMEtFraction;
	double GenMET_ChargedHadEt;
	double GenMET_ChargedHadEtFraction;
	double GenMET_emEnergy;
	double GenMET_hadEnergy;
	double GenMET_invisEnergy;
	double GenMET_invisEt;
	double GenMET_MuonEt;
	double GenMET_MuonEtFraction;
	double GenMET_NeutralEMEt;
	double GenMET_NeutralEMEtFraction;
	double GenMET_NeutralHadEt;
	double GenMET_NeutralHadEtFraction;
};
#endif
