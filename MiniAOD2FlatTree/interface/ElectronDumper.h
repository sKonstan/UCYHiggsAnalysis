#ifndef ElectronDumper_h
#define ElectronDumper_h

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

#include "DataFormats/PatCandidates/interface/Electron.h"
#include "UCYHiggsAnalysis/MiniAOD2FlatTree/interface/FourVectorDumper.h"

class ElectronDumper : public BaseDumper {
    public:
	ElectronDumper(edm::ConsumesCollector&& iConsumesCollector, std::vector<edm::ParameterSet>& psets);
	~ElectronDumper();

        void book(TTree*);
	bool fill(edm::Event&, const edm::EventSetup&);
        void reset();

    private:
	void fillMCMatchInfo(size_t ic, edm::Handle<reco::GenParticleCollection>& genParticles, const pat::Electron& ele);
        
	// EDGetToken is used to quickly retrieve data from the edm::Event, edm::LuminosityBlock or edm::Run.
        edm::EDGetTokenT<edm::View<pat::Electron>> *electronToken;
        edm::EDGetTokenT<edm::View<reco::GsfElectron>> *gsfElectronToken;
        edm::EDGetTokenT<double> *rhoToken;
        edm::EDGetTokenT<reco::GenParticleCollection> genParticleToken;
        edm::EDGetTokenT<edm::ValueMap<bool>> *electronIDToken;

	int width;
        bool cfg_debugMode;
	std::string cfg_branchName;
        
        std::vector<float> *relIsoDeltaBetaCorrected;
	std::vector<bool> *isPF;
	std::vector<float> *caloIso;    // sum of ecalIso() and hcalIso()
	std::vector<float> *trackIso;   // summed track pt in a cone of deltaR<0.4
        
        // 4-vector for generator electrons  (MC-matched to pat::Electrons)
        FourVectorDumper *MCelectron;
};
#endif
