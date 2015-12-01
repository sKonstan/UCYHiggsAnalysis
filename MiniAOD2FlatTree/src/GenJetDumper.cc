#include "UCYHiggsAnalysis/MiniAOD2FlatTree/interface/GenJetDumper.h"


GenJetDumper::GenJetDumper(edm::ConsumesCollector&& iConsumesCollector, std::vector<edm::ParameterSet>& psets){
  inputCollections = psets;
  booked           = false;

  // Four-vector variables (with fixes initial size)
  pt  = new std::vector<double>[inputCollections.size()];
  eta = new std::vector<double>[inputCollections.size()];    
  phi = new std::vector<double>[inputCollections.size()];    
  e   = new std::vector<double>[inputCollections.size()];    
  // Other essential variables (with fixes initial size)   
  charge           = new std::vector<short>[inputCollections.size()];
  emEnergy         = new std::vector<double>[inputCollections.size()];
  hadEnergy        = new std::vector<double>[inputCollections.size()];
  auxEnergy        = new std::vector<double>[inputCollections.size()];
  invisEnergy      = new std::vector<double>[inputCollections.size()];
  nGenConstituents = new std::vector<short>[inputCollections.size()];

  // Other auxiliary variables 
  width = 14;
  genJetToken = new edm::EDGetTokenT<reco::GenJetCollection>[inputCollections.size()];

  // For-loop: All input collections
  for(size_t i = 0; i < inputCollections.size(); ++i){
    edm::InputTag inputtag = inputCollections[i].getParameter<edm::InputTag>("src");
    genJetToken[i] = iConsumesCollector.consumes<reco::GenJetCollection>(inputtag);
  }
        
  useFilter = false;
  // For-loop: All input collections 
  for(size_t i = 0; i < inputCollections.size(); ++i){
    bool param = inputCollections[i].getUntrackedParameter<bool>("filter",false);
    if(param) useFilter = true;
  }

}


GenJetDumper::~GenJetDumper(){}


void GenJetDumper::book(TTree* tree){
  booked = true;

  // For-loop: All input collections
  for(size_t i = 0; i < inputCollections.size(); ++i){
      
    cfg_branchName = inputCollections[i].getUntrackedParameter<std::string>("branchName","");
    if(cfg_branchName.length() == 0) cfg_branchName = inputCollections[i].getParameter<edm::InputTag>("src").label();
      
    // Four-vector variables   
    tree->Branch( ( cfg_branchName + "_pt") .c_str(), &pt[i]  );
    tree->Branch( ( cfg_branchName + "_eta").c_str(), &eta[i] );
    tree->Branch( ( cfg_branchName + "_phi").c_str(), &phi[i] );
    tree->Branch( ( cfg_branchName + "_e")  .c_str(), &e[i]   );
    // Other essential variables    
    tree->Branch( ( cfg_branchName + "_charge")          .c_str(), &charge[i]           );
    tree->Branch( ( cfg_branchName + "_emEnergy")        .c_str(), &emEnergy[i]         );
    tree->Branch( ( cfg_branchName + "_hadEnergy")       .c_str(), &hadEnergy[i]        );
    tree->Branch( ( cfg_branchName + "_auxEnergy")       .c_str(), &auxEnergy[i]        );
    tree->Branch( ( cfg_branchName + "_invisEnergy")     .c_str(), &invisEnergy[i]      );
    tree->Branch( ( cfg_branchName + "_nGenConstituents").c_str(), &nGenConstituents[i] );
    
  }// for(size_t i = 0; i < inputCollections.size(); ++i){
    
  return;
}


bool GenJetDumper::fill(edm::Event& iEvent, const edm::EventSetup& iSetup){
  if (!booked) return true;

  // For-loop: All input collections
  for(size_t ic = 0; ic < inputCollections.size(); ++ic){

    // Input parameters/flags
    cfg_debugMode  = inputCollections[ic].getUntrackedParameter<bool>("debugMode");
    cfg_branchName = inputCollections[ic].getUntrackedParameter<std::string>("branchName","");
	
    // Print debugging info?
    if (cfg_debugMode){
      std::cout << std::setw(width*6) << cfg_branchName << std::endl;
      std::cout << std::string(width*10, '=') << std::endl;
      std::cout << std::setw(5)     << "Index"
		<< std::setw(width) << "Pt"        << std::setw(width) << "Eta"       << std::setw(width) << "Phi"       << std::setw(width) << "Energy"
		<< std::setw(width) << "emEnergy"  << std::setw(width) << "hadEnergy" << std::setw(width) << "auxEnergy" << std::setw(width) << "invisEnergy"  
		<< std::setw(width) << "nConstituents"
		<< std::endl;
      std::cout << std::string(width*10, '=') << std::endl;
    }

    // Create edm handle and get the GenJetCollection         
    edm::Handle<reco::GenJetCollection> handle;
    iEvent.getByToken(genJetToken[ic], handle);
      
    // Sanity check 
    if(handle.isValid()){

      // For-loop: GenJets (gj)
      for(size_t gj_index=0; gj_index < handle->size(); ++gj_index) {
	  
	// Get the GenJet
	// const reco::Candidate & gj = handle->at(gj_index);
	const reco::GenJet & gj = handle->at(gj_index);
	  
	// Four-vector variables
	pt[ic] .push_back( gj.pt()     );
	eta[ic].push_back( gj.eta()    );
	phi[ic].push_back( gj.phi()    );
	e[ic]  .push_back( gj.energy() );

	// Other essential variables  
	charge[ic]          .push_back( gj.charge()          );
	emEnergy[ic]        .push_back( gj.emEnergy()        );
	hadEnergy[ic]       .push_back( gj.hadEnergy()       );
	auxEnergy[ic]       .push_back( gj.auxiliaryEnergy() );
	invisEnergy[ic]     .push_back( gj.invisibleEnergy() );
	// Get the GenJet constituents (alternative)
	nGenConstituents[ic].push_back( gj.numberOfDaughters() );

	// NOTE: The method getGenConstituents() does not work on MiniAOD since the
	// constituents are of type pat::PackedGenParticle in MiniAOD (https://hypernews.cern.ch/HyperNews/CMS/get/physTools/3326/1.html)
	// Instead, the methods numberOfDaughters() and daughterPtr(index) work & return the packed PF Candidates.
	/*
	  std::vector <const reco::GenParticle*> mcparts = gj.getGenConstituents();
	  short int nConstituents = 0;
	  for (unsigned i = 0; i < mcparts.size (); i++) {
	  const reco::GenParticle* mcpart = mcparts[i];
	  if (mcpart) nConstituents++;	 
	  } for (unsigned i = 0; i < mcparts.size (); i++) {
	  nGenConstituents[ic].push_back( gj_mcparts.size() );
	*/
	
	// Print debugging info?
	if (cfg_debugMode){
	  std::cout << std::setw(5)     << gj_index
		    << std::setw(width) << gj.pt()              << std::setw(width) << gj.eta()             << std::setw(width) << gj.phi()       
		    << std::setw(width) << gj.energy()          << std::setw(width) << gj.emEnergy()        << std::setw(width) << gj.hadEnergy() 
		    << std::setw(width) << gj.auxiliaryEnergy() << std::setw(width) << gj.invisibleEnergy() << std::setw(width) << gj.numberOfDaughters()
		    << std::endl;
	}
	  
      }// for(size_t gj_index=0; gj_index < handle->size(); ++gj_index) {
    }// if(handle.isValid()){
  }// for(size_t ic = 0; ic < inputCollections.size(); ++ic){
    
  return filter();
}


bool GenJetDumper::filter(){
  if(!useFilter) return true;
  return true;
}


void GenJetDumper::reset(){
  if(booked){
   
    // For-loop: All input collections
    for(size_t ic = 0; ic < inputCollections.size(); ++ic){

      // Four-vector variables  
      pt[ic] .clear();
      eta[ic].clear();
      phi[ic].clear();
      e[ic]  .clear();
      // Other essential variables
      charge[ic]          .clear();
      emEnergy[ic]        .clear();
      hadEnergy[ic]       .clear();
      auxEnergy[ic]       .clear();
      invisEnergy[ic]     .clear();
      nGenConstituents[ic].clear();

    }// for(size_t ic = 0; ic < inputCollections.size(); ++ic){
    
  }// if(booked){

  return;
}
