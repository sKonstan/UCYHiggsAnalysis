#include "UCYHiggsAnalysis/MiniAOD2FlatTree/interface/GenMETDumper.h"

#include "DataFormats/METReco/interface/GenMET.h"

GenMETDumper::GenMETDumper(edm::ConsumesCollector&& iConsumesCollector, std::vector<edm::ParameterSet>& psets){
  inputCollections = psets;
  booked           = false;

  // Other auxiliary variables
  width = 14;
  token = new edm::EDGetTokenT<edm::View<reco::GenMET>>[inputCollections.size()];

  // For-loop: All input collections
  for(size_t i = 0; i < inputCollections.size(); ++i){
    edm::InputTag inputtag = inputCollections[i].getParameter<edm::InputTag>("src");
    token[i] = iConsumesCollector.consumes<edm::View<reco::GenMET>>(inputtag);
  }
    
  useFilter = false;
  // For-loop: All input collections 
  for(size_t i = 0; i < inputCollections.size(); ++i){
    if(inputCollections[i].getUntrackedParameter<bool>("filter",false)) useFilter = true;
  }
}


GenMETDumper::~GenMETDumper(){}


void GenMETDumper::book(TTree* tree){
  booked = true;

  cfg_branchName = inputCollections[0].getUntrackedParameter<std::string>("branchName","");
  tree->Branch( (cfg_branchName + "_et") .c_str(), &GenMET    );
  tree->Branch( (cfg_branchName + "_phi").c_str(), &GenMET_phi);

  return;
}


bool GenMETDumper::fill(edm::Event& iEvent, const edm::EventSetup& iSetup){
  if (!booked) return true;
    
  // For-loop: All input collections
  for(size_t i = 0; i < inputCollections.size(); ++i){

    // Input parameters/flags
    cfg_debugMode   = inputCollections[i].getUntrackedParameter<bool>("debugMode");
    cfg_branchName  = inputCollections[i].getUntrackedParameter<std::string>("branchName","");
    const int index = 0;

    // Print debugging info?
    if (cfg_debugMode){
      std::cout << std::setw(width*6) << cfg_branchName << std::endl;
      std::cout << std::string(width*10, '=') << std::endl;
      std::cout << std::setw(5)     << "Index"
		<< std::setw(width) << "GenMET"               << std::setw(width) << "Phi"                << std::setw(width) << "AuxEnergy"
		<< std::setw(width) << "ChargedEMEt"          << std::setw(width) << "ChargedMEtFraction" << std::setw(width) << "ChargedHadEt"
		<< std::setw(width) << "ChargedHadEtFraction" << std::setw(width) << "emEnergy"           << std::setw(width) << "HadEnergy"
		<< std::setw(width) << "invisEnergy"          << std::setw(width) << "invisEt"            << std::setw(width) << "InvisEt"
		<< std::setw(width) << "MuonEt"               << std::setw(width) << "MuonEtFraction"     << std::setw(width) << "NeutralEMEt"
		<< std::setw(width) << "NeutralEMEtFraction"  << std::setw(width) << "NeutralHadEt"       << std::setw(width) << "NeutralHadEtFraction"
		<< std::endl;
      std::cout << std::string(width*10, '=') << std::endl;
    }


    // Create edm handle and get the GenMetCollection
    edm::Handle<edm::View<reco::GenMET>> handle;
    iEvent.getByToken(token[i], handle);

    // Sanity check
    if(handle.isValid()){
      GenMET                      = handle->ptrAt(index)->et();
      GenMET_phi                  = handle->ptrAt(index)->phi();
      GenMET_auxEnergy            = handle->ptrAt(index)->auxiliaryEnergy();
      GenMET_ChargedEMEt          = handle->ptrAt(index)->ChargedEMEt();
      GenMET_ChargedMEtFraction   = handle->ptrAt(index)->ChargedEMEtFraction();
      GenMET_ChargedHadEt         = handle->ptrAt(index)->ChargedHadEt();
      GenMET_ChargedHadEtFraction = handle->ptrAt(index)->ChargedHadEtFraction();
      GenMET_emEnergy             = handle->ptrAt(index)->emEnergy();
      GenMET_hadEnergy            = handle->ptrAt(index)->hadEnergy();
      GenMET_invisEnergy          = handle->ptrAt(index)->invisibleEnergy();
      GenMET_invisEt              = handle->ptrAt(index)->InvisibleEt();
      GenMET_MuonEt               = handle->ptrAt(index)->MuonEt();
      GenMET_MuonEtFraction       = handle->ptrAt(index)->MuonEtFraction();
      GenMET_NeutralEMEt          = handle->ptrAt(index)->NeutralEMEt();
      GenMET_NeutralEMEtFraction  = handle->ptrAt(index)->NeutralEMEtFraction();
      GenMET_NeutralHadEt         = handle->ptrAt(index)->NeutralHadEt();
      GenMET_NeutralHadEtFraction = handle->ptrAt(index)->NeutralHadEtFraction();

      // Print debugging info?
      if (cfg_debugMode){
	std::cout << std::setw(5)     << index
		  << std::setw(width) << GenMET                      << std::setw(width) << GenMET_phi                << std::setw(width) << GenMET_auxEnergy
		  << std::setw(width) << GenMET_ChargedEMEt          << std::setw(width) << GenMET_ChargedMEtFraction << std::setw(width) << GenMET_ChargedHadEt
		  << std::setw(width) << GenMET_ChargedHadEtFraction << std::setw(width) << GenMET_emEnergy           << std::setw(width) << GenMET_hadEnergy
		  << std::setw(width) << GenMET_invisEnergy          << std::setw(width) << GenMET_invisEt            << std::setw(width) << GenMET_invisEt
		  << std::setw(width) << GenMET_MuonEt               << std::setw(width) << GenMET_MuonEtFraction     << std::setw(width) << GenMET_NeutralEMEt
		  << std::setw(width) << GenMET_NeutralEMEtFraction  << std::setw(width) << GenMET_NeutralHadEt       << std::setw(width) << GenMET_NeutralHadEtFraction
		  << std::endl;
	std::cout << std::string(width*10, '=') << std::endl;
      }

    }// if(handle.isValid()){
    else{
      throw cms::Exception("config") << "Cannot find MET collection! " << inputCollections[i].getParameter<edm::InputTag>("src").label();
    }
  }
  // for(size_t i = 0; i < inputCollections.size(); ++i){

  return filter();
}


bool GenMETDumper::filter(){
  if(!useFilter) return true;

  return true;
}


void GenMETDumper::reset(){
  if(booked){
    GenMET = 0;
    GenMET_phi = 0;
  }
  return;
}
