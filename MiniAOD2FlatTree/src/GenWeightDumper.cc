#include "UCYHiggsAnalysis/MiniAOD2FlatTree/interface/GenWeightDumper.h"


GenWeightDumper::GenWeightDumper(edm::ConsumesCollector&& iConsumesCollector, std::vector<edm::ParameterSet> psets){
  inputCollections = psets;
  booked           = false;

  token = new edm::EDGetTokenT<GenEventInfoProduct>[inputCollections.size()];

  // For-loop: All input collections
  for(size_t i = 0; i < inputCollections.size(); ++i){
    edm::InputTag inputtag = inputCollections[i].getParameter<edm::InputTag>("src");
    token[i] = iConsumesCollector.consumes<GenEventInfoProduct>(inputtag);
  }
    
  useFilter = false;
  // For-loop: All input collections
  for(size_t i = 0; i < inputCollections.size(); ++i){
    if(inputCollections[i].getUntrackedParameter<bool>("filter",false)) useFilter = true;
  }

  // Other auxiliary variables
  width          = 15;
  cfg_debugMode  = false;
  cfg_branchName = "";

}


GenWeightDumper::~GenWeightDumper(){}


void GenWeightDumper::book(TTree* tree){
  booked = true;

  // Input parameters/flags                                                                                                                                                        
  // cfg_debugMode  = inputCollections[i].getUntrackedParameter<bool>("debugMode");
  cfg_branchName = inputCollections[0].getUntrackedParameter<std::string>("branchName","");
  
  tree->Branch( (cfg_branchName + "_Weight") .c_str(), &GenWeight );

  return;
}


bool GenWeightDumper::fill(edm::Event& iEvent, const edm::EventSetup& iSetup){
  if (!booked) return true;

  // For-loop: All input collections
  for(size_t i = 0; i < inputCollections.size(); ++i){
	
    // Input parameters/flags
    cfg_debugMode  = inputCollections[i].getUntrackedParameter<bool>("debugMode");
    cfg_branchName = inputCollections[i].getUntrackedParameter<std::string>("branchName","");

    // Print debugging info?
    if (cfg_debugMode){
      std::cout << "\n" << std::setw(width*5) << cfg_branchName << std::endl;
      std::cout << std::string(width*10, '=') << std::endl;
      std::cout << std::setw(5)       << "Index"
                << std::setw(width)   << "alphaQCD"           << std::setw(width)   << "alphaQED" << std::setw(width)   << "nMEPartons"      
		<< std::setw(width*2) << "nMEPartonsFiltered" << std::setw(width)   << "qScale"   << std::setw(width)   << "weight"
                << std::setw(width*2) << "weightProduct"      
                << std::endl;
      std::cout << std::string(width*10, '=') << std::endl;
    }
    
    // Get a handle [https://cmssdt.cern.ch/SDT/doxygen/CMSSW_7_5_2/doc/html/d3/d77/classGenEventInfoProduct.html]
    edm::Handle<GenEventInfoProduct> handle;
    iEvent.getByToken(token[i], handle);

    // Sanity check
    if(handle.isValid()){
      GenWeight = handle->weight();

      // Print debugging info?
      if (cfg_debugMode){
	std::cout << std::setw(5)       << i
		  << std::setw(width)   << handle->alphaQCD()           << std::setw(width)   << handle->alphaQED() << std::setw(width)   << handle->nMEPartons()
		  << std::setw(width*2) << handle->nMEPartonsFiltered() << std::setw(width)   << handle->qScale()   << std::setw(width)   << handle->weight()
		  << std::setw(width*2) << handle->weightProduct()
		  << std::endl;
      }

    }

  }// for(size_t i = 0; i < inputCollections.size(); ++i){
    
  return filter();
}


bool GenWeightDumper::filter(){
  if(!useFilter) return true;

  return true;
}


void GenWeightDumper::reset(){
  if(booked){
    GenWeight = 0;
  }

  return;
}
