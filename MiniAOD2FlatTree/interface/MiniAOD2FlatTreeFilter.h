#ifndef MiniAOD2FlatTreeFilter_h
#define MiniAOD2FlatTreeFilter_h

#include "FWCore/Framework/interface/EDFilter.h"
#include "FWCore/Framework/interface/MakerMacros.h"
        
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"  
#include "DataFormats/Common/interface/View.h"
        
#include <string>

#include "TFile.h"
#include "TTree.h"
#include "DataFormats/Math/interface/LorentzVector.h"
#include "HLTrigger/HLTcore/interface/HLTConfigProvider.h"
#include "CommonTools/TriggerUtils/interface/PrescaleWeightProvider.h"

#include "UCYHiggsAnalysis/MiniAOD2FlatTree/interface/EventInfoDumper.h"
#include "UCYHiggsAnalysis/MiniAOD2FlatTree/interface/SkimDumper.h"
#include "UCYHiggsAnalysis/MiniAOD2FlatTree/interface/TriggerDumper.h"
#include "UCYHiggsAnalysis/MiniAOD2FlatTree/interface/METNoiseFilterDumper.h"
#include "UCYHiggsAnalysis/MiniAOD2FlatTree/interface/TauDumper.h"
#include "UCYHiggsAnalysis/MiniAOD2FlatTree/interface/ElectronDumper.h"
#include "UCYHiggsAnalysis/MiniAOD2FlatTree/interface/MuonDumper.h"
#include "UCYHiggsAnalysis/MiniAOD2FlatTree/interface/JetDumper.h"
#include "UCYHiggsAnalysis/MiniAOD2FlatTree/interface/METDumper.h"
#include "UCYHiggsAnalysis/MiniAOD2FlatTree/interface/GenMETDumper.h"
#include "UCYHiggsAnalysis/MiniAOD2FlatTree/interface/TrackDumper.h"
#include "UCYHiggsAnalysis/MiniAOD2FlatTree/interface/GenParticleDumper.h"
#include "UCYHiggsAnalysis/MiniAOD2FlatTree/interface/GenJetDumper.h"
#include "UCYHiggsAnalysis/MiniAOD2FlatTree/interface/GenWeightDumper.h"

/**
	Class for making a tree from MiniAOD
	Original Author: S.Lehti
*/

class MiniAOD2FlatTreeFilter : public edm::EDFilter {
    public:
        MiniAOD2FlatTreeFilter(const edm::ParameterSet&);
        ~MiniAOD2FlatTreeFilter();

        void beginRun(edm::Run const&, edm::EventSetup const&);
        void beginJob();
        bool filter(edm::Event&, const edm::EventSetup&);
        void endJob();

    private:
	void fill(edm::Event&, const edm::EventSetup&);
	void reset();
        void endLuminosityBlock(const edm::LuminosityBlock&, const edm::EventSetup&);                                   

	bool isMC();

	std::string hltProcessName;
        HLTConfigProvider hltConfig;
        //PrescaleWeightProvider prescaleWeight;

	std::string outputFileName;
        std::string PUInfoInputFileName;
	std::string TopPtInputFileName;
	std::string codeVersion;
        std::string dataVersion;
	int cmEnergy;
	edm::ParameterSet eventInfoCollections;
	edm::ParameterSet skim;
	edm::ParameterSet trigger;
        edm::ParameterSet metNoiseFilter;
        std::vector<edm::ParameterSet> tauCollections;
	std::vector<edm::ParameterSet> electronCollections;
	std::vector<edm::ParameterSet> muonCollections;
	std::vector<edm::ParameterSet> jetCollections;
	std::vector<edm::ParameterSet> metCollections;
	std::vector<edm::ParameterSet> genMetCollections;
	std::vector<edm::ParameterSet> genWeightCollections;
        std::vector<edm::ParameterSet> trackCollections;
        std::vector<edm::ParameterSet> genParticleCollections;
        std::vector<edm::ParameterSet> genJetCollections;


	TFile* fOUT;
	TTree* Events;

	EventInfoDumper *eventInfo;
	SkimDumper* skimDumper;
	TriggerDumper* trgDumper;
        METNoiseFilterDumper* metNoiseFilterDumper;
	TauDumper* tauDumper;
	ElectronDumper* electronDumper;
	MuonDumper* muonDumper;
	JetDumper* jetDumper;
	METDumper* metDumper;
	GenMETDumper* genMetDumper;
        GenWeightDumper* genWeightDumper;
	TrackDumper* trackDumper;
	GenParticleDumper* genParticleDumper;
        GenJetDumper* genJetDumper;
};

#endif
