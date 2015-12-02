#ifndef TauDumper_h
#define TauDumper_h

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
#include "DataFormats/PatCandidates/interface/Tau.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "UCYHiggsAnalysis/MiniAOD2FlatTree/interface/BaseDumper.h"
#include "UCYHiggsAnalysis/MiniAOD2FlatTree/interface/FourVectorDumper.h"

class TauDumper : public BaseDumper {
    public:
	TauDumper(edm::ConsumesCollector&& iConsumesCollector, std::vector<edm::ParameterSet>& psets);
	~TauDumper();

	void book(TTree*);
	bool fill(edm::Event&, const edm::EventSetup&);
	void reset();

    private:
        void fillMCMatchInfo(size_t ic, edm::Handle<reco::GenParticleCollection>& genParticles, const pat::Tau& tau);
        
	bool filter();
        
        edm::EDGetTokenT<edm::View<pat::Tau>> *tauToken;
        edm::EDGetTokenT<edm::View<pat::Jet>> *jetToken;
        edm::EDGetTokenT<reco::GenParticleCollection> genParticleToken;

        std::vector<double> *lChTrackPt;
        std::vector<double> *lChTrackEta;
        std::vector<double> *lNeutrTrackPt;
        std::vector<double> *lNeutrTrackEta;

        std::vector<short> *decayMode;
        std::vector<float> *ipxy;
        std::vector<float> *ipxySignif;
	std::vector<short> *nProngs;
        std::vector<short> *pdgTauOrigin;
        std::vector<short> *MCNProngs;
        std::vector<short> *MCNPiZeros;

        FourVectorDumper *MCtau;               // 4-vector for generator visible tau
        FourVectorDumper *matchingJet;         // 4-vector for matching jet       
        FourVectorDumper *systTESup;           // Systematics variations for tau 4-vector (up)
        FourVectorDumper *systTESdown;         // Systematics variations for tau 4-vector (down)
        FourVectorDumper *systExtremeTESup;    // Extreme Systematics variations for tau 4-vector (up)
        FourVectorDumper *systExtremeTESdown;  // Extreme Systematics variations for tau 4-vector (down)

	int width;
        bool cfg_debugMode;
	std::string cfg_branchName;        
};
#endif
