#ifndef METDumper_h
#define METDumper_h

#include "FWCore/Framework/interface/EDFilter.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/Framework/interface/ConsumesCollector.h"
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "DataFormats/Common/interface/View.h"
#include "DataFormats/Common/interface/Ptr.h"
#include "DataFormats/PatCandidates/interface/MET.h"

#include <string>
#include <vector>

#include "TTree.h"
#include "DataFormats/Math/interface/LorentzVector.h"

class METDumper {
    public:
	METDumper(edm::ConsumesCollector&& iConsumesCollector, std::vector<edm::ParameterSet>& psets, bool bIsMC);
	~METDumper();

	void book(TTree*);
	bool fill(edm::Event&, const edm::EventSetup&);
	void reset();

    private:
	bool filter();
        bool useFilter;
	bool booked;

	std::vector<edm::ParameterSet> inputCollections;
	edm::EDGetTokenT<edm::View<pat::MET>> *token;


	int width;
        bool cfg_debugMode;
	std::string cfg_branchName;
	bool isMC;

        // For each collection (https://cmssdt.cern.ch/SDT/doxygen/CMSSW_5_3_14/doc/html/d6/df9/DataFormats_2PatCandidates_2interface_2MET_8h_source.html)
	double *MET;
	double *MET_x;
	double *MET_y;
        double *MET_significance;
	bool   *MET_isCaloMET;
	bool   *MET_isPFMET;
	bool   *MET_isRecoMET;

	// For single collection (raw calo MET)
        double caloMET;
        double caloMET_x;
        double caloMET_y;
        // double caloMET_phi;
        double caloMET_sumEt;

        // GenMET (https://cmssdt.cern.ch/SDT/doxygen/CMSSW_5_3_14/doc/html/df/dd8/GenMET_8h_source.html
	double GenMET;
	double GenMET_x;
        double GenMET_y;
        double GenMET_phi;
	double GenMET_NeutralEMEtFraction;  // Neutral EM Et Fraction
	double GenMET_NeutralEMEt;          // Neutral EM Et 
	double GenMET_ChargedEMEtFraction;  // Charged EM Et Fraction 	
	double GenMET_ChargedEMEt;          // Charged EM Et  	
	double GenMET_NeutralHadEtFraction; // Neutral Had Et Fraction	
	double GenMET_NeutralHadEt;         // Neutral Had Et
	double GenMET_ChargedHadEtFraction; // Charged Had Et Fraction 
	double GenMET_ChargedHadEt;         // Charged Had Et 
	double GenMET_MuonEtFraction;       // Muon Et Fraction 
	double GenMET_MuonEt;               // Muon Et 	
	double GenMET_InvisibleEtFraction;  // Invisible Et Fraction 
	double GenMET_InvisibleEt;          // Invisible Et  

};
#endif
