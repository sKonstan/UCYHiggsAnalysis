#include "UCYHiggsAnalysis/MiniAOD2FlatTree/interface/ElectronDumper.h"

#include <algorithm>

ElectronDumper::ElectronDumper(edm::ConsumesCollector&& iConsumesCollector, std::vector<edm::ParameterSet>& psets)
  : genParticleToken(iConsumesCollector.consumes<reco::GenParticleCollection>(edm::InputTag("prunedGenParticles"))) {
  inputCollections = psets;
    
  // Four-vector variables
  pt  = new std::vector<double>[inputCollections.size()];
  eta = new std::vector<double>[inputCollections.size()];    
  phi = new std::vector<double>[inputCollections.size()];    
  e   = new std::vector<double>[inputCollections.size()];    

  // Other essential variables
  relIsoDeltaBetaCorrected = new std::vector<float>[inputCollections.size()];
  isPF                     = new std::vector<bool>[inputCollections.size()];
  caloIso                  = new std::vector<float>[inputCollections.size()];
  trackIso                 = new std::vector<float>[inputCollections.size()];

  MCelectron               = new FourVectorDumper[inputCollections.size()];
  nDiscriminators          = inputCollections[0].getParameter<std::vector<std::string> >("discriminators").size();
  discriminators           = new std::vector<bool>[inputCollections.size()*nDiscriminators];

  // Tokens
  electronToken    = new edm::EDGetTokenT<edm::View<pat::Electron>>[inputCollections.size()];
  electronIDToken  = new edm::EDGetTokenT<edm::ValueMap<bool>>[inputCollections.size()*nDiscriminators];
  gsfElectronToken = new edm::EDGetTokenT<edm::View<reco::GsfElectron>>[inputCollections.size()];
  rhoToken         = new edm::EDGetTokenT<double>[inputCollections.size()];

  // Other auxiliary variables
  width = 12;
  cfg_debugMode    = false;
  cfg_branchName   = "";

  // For-loop: All input collections
  for(size_t i = 0; i < inputCollections.size(); ++i){
    edm::InputTag inputtag = inputCollections[i].getParameter<edm::InputTag>("src");
    electronToken[i] = iConsumesCollector.consumes<edm::View<pat::Electron>>(inputtag);
    gsfElectronToken[i] = iConsumesCollector.consumes<edm::View<reco::GsfElectron>>(inputtag);
    edm::InputTag rhoSource = inputCollections[i].getParameter<edm::InputTag>("rhoSource");
    rhoToken[i] = iConsumesCollector.consumes<double>(rhoSource);
    std::string IDprefix = inputCollections[i].getParameter<std::string>("IDprefix");
    std::vector<std::string> discriminatorNames = inputCollections[i].getParameter<std::vector<std::string> >("discriminators");
    for (size_t j = 0; j < discriminatorNames.size(); ++j) {
      edm::InputTag discrTag(IDprefix, discriminatorNames[j]);
      electronIDToken[i*discriminatorNames.size()+j] = iConsumesCollector.consumes<edm::ValueMap<bool>>(discrTag);
    }// for (size_t j = 0; j < discriminatorNames.size(); ++j) {
  }// for(size_t i = 0; i < inputCollections.size(); ++i){
    
  useFilter = false;
  // For-loop: All input collections
  for(size_t i = 0; i < inputCollections.size(); ++i){
    bool param = inputCollections[i].getUntrackedParameter<bool>("filter",false);
    if(param) useFilter = true;
  }// For-loop: All input collections

}


ElectronDumper::~ElectronDumper(){}


void ElectronDumper::book(TTree* tree){
  booked = true;

  // For-loop: All input collections
  for(size_t i = 0; i < inputCollections.size(); ++i){

    // Input parameters/flags
    cfg_debugMode  = inputCollections[i].getUntrackedParameter<bool>("debugMode");
    cfg_branchName = inputCollections[i].getUntrackedParameter<std::string>("branchName","");

    if(cfg_branchName.length() == 0) cfg_branchName = inputCollections[i].getParameter<edm::InputTag>("src").label();
      
    // Four-vector variables
    tree->Branch( (cfg_branchName + "_pt") .c_str(), &pt[i]  );
    tree->Branch( (cfg_branchName + "_eta").c_str(), &eta[i] );
    tree->Branch( (cfg_branchName + "_phi").c_str(), &phi[i] );
    tree->Branch( (cfg_branchName + "_e")  .c_str(), &e[i]   );

    // Other essential variables (with fixed initial size)
    tree->Branch( (cfg_branchName + "_relIsoDeltaBeta").c_str(), &relIsoDeltaBetaCorrected[i] );
    tree->Branch( (cfg_branchName + "_isPF")           .c_str(), &isPF[i]                     );
    tree->Branch( (cfg_branchName + "_caloIso")        .c_str(), &caloIso[i]                  );
    tree->Branch( (cfg_branchName + "_trackIso")       .c_str(), &trackIso[i]                 );

    MCelectron[i].book(tree, cfg_branchName, "MCelectron");
        
    std::vector<std::string> discriminatorNames = inputCollections[i].getParameter<std::vector<std::string> >("discriminators");
    // For-loop: All discriminators
    for(size_t iDiscr = 0; iDiscr < discriminatorNames.size(); ++iDiscr) {
      // Convert dashes into underscores
      std::replace(discriminatorNames[iDiscr].begin(), discriminatorNames[iDiscr].end(),'-','_');
      tree->Branch( (cfg_branchName + "_" + discriminatorNames[iDiscr]).c_str(), &discriminators[inputCollections.size()*iDiscr+i]);
    }// for(size_t iDiscr = 0; iDiscr < discriminatorNames.size(); ++iDiscr) {

  }// for(size_t i = 0; i < inputCollections.size(); ++i){

  return;
}


bool ElectronDumper::fill(edm::Event& iEvent, const edm::EventSetup& iSetup){
  if (!booked) return true;  
  
  // Create edm handle and get the GenParticleCollection (only if not real data)
  edm::Handle <reco::GenParticleCollection> genParticlesHandle;  
  if (!iEvent.isRealData()) iEvent.getByToken(genParticleToken, genParticlesHandle);

  // For-loop: All input collections    
  for(size_t ic = 0; ic < inputCollections.size(); ++ic){

    // Create edm handle and get the pat::Electron collection
    edm::Handle<edm::View<pat::Electron>> electronHandle;
    iEvent.getByToken(electronToken[ic], electronHandle);

    // Print debugging info?
    if (cfg_debugMode){
      std::cout << "\n" << std::setw(width*6) << cfg_branchName << std::endl;
      std::cout << std::string(width*14, '=') << std::endl;
      std::cout << std::setw(5)     << "Index"
                << std::setw(width) << "Pt"     << std::setw(width) << "Eta"   << std::setw(width) << "Phi"     << std::setw(width) << "E"
                << std::setw(width) << "RelIso" << std::setw(width) << "isPF"  << std::setw(width) << "caloIso" << std::setw(width) << "trackIso"
                << std::setw(width) << "deltaR" << std::setw(width) << "Pt"    << std::setw(width) << "Eta"     << std::setw(width) << "Phi"
                << std::setw(width) << "E"      
		<< std::endl;
	std::cout << std::string(width*14, '=') << std::endl;
    }

    // Sanity check
    if(electronHandle.isValid()){
      
      // Setup also handle for GsfElectrons (needed for ID)
      edm::Handle<edm::View<reco::GsfElectron>> gsfHandle;
      iEvent.getByToken(gsfElectronToken[ic], gsfHandle);

      // Setup handles for rho
      edm::Handle<double> rhoHandle;
      iEvent.getByToken(rhoToken[ic], rhoHandle);

      // Setup handles for ID
      std::vector<edm::Handle<edm::ValueMap<bool>>> IDhandles;
      std::vector<std::string> discriminatorNames = inputCollections[ic].getParameter<std::vector<std::string> >("discriminators");

      // For-loop: All discriminators
      for (size_t j = 0; j < discriminatorNames.size(); ++j) {
	edm::Handle<edm::ValueMap<bool>> IDhandle;
	iEvent.getByToken(electronIDToken[ic*inputCollections.size()+j], IDhandle);
	IDhandles.push_back(IDhandle);
      }

      // For-loop: All electrons
      for(size_t i=0; i<electronHandle->size(); ++i) {

	// Get the pat::Electron
	const pat::Electron& obj = electronHandle->at(i);

	// Four-vector variables
	pt[ic] .push_back( obj.p4().pt()     );
	eta[ic].push_back( obj.p4().eta()    );
	phi[ic].push_back( obj.p4().phi()    );
	e[ic]  .push_back( obj.p4().energy() );

	// Calculate relative isolation (delta beta)
	// See: https://cmssdt.cern.ch/SDT/doxygen/CMSSW_7_5_2/doc/html/d3/df3/structreco_1_1GsfElectron_1_1PflowIsolationVariables.html
	double isolation = obj.pfIsolationVariables().sumChargedHadronPt  
	  + std::max(obj.pfIsolationVariables().sumNeutralHadronEt + obj.pfIsolationVariables().sumPhotonEt - 0.5 * obj.pfIsolationVariables().sumPUPt, 0.0);
	double relIso = isolation / obj.pt();

	// Other essential variables
	relIsoDeltaBetaCorrected[ic].push_back(relIso);
	isPF[ic]    .push_back( obj.isPF()     );
	caloIso[ic] .push_back( obj.caloIso()  );
	trackIso[ic].push_back( obj.trackIso() );
                
	// For-loop: All discriminators
	// See: https://twiki.cern.ch/twiki/bin/view/CMS/MultivariateElectronIdentificationRun2
	for(size_t iDiscr = 0; iDiscr < discriminatorNames.size(); ++iDiscr) {
	  discriminators[inputCollections.size()*iDiscr+ic].push_back((*(IDhandles[iDiscr]))[gsfHandle->ptrAt(i)]);
	}


	// Print debugging info?
	if (cfg_debugMode){
	  std::cout << std::setw(5)     << i
		    << std::setw(width) << obj.p4().pt()     << std::setw(width) << obj.p4().eta() << std::setw(width) << obj.p4().phi()
		    << std::setw(width) << obj.p4().energy() << std::setw(width) << relIso         << std::setw(width) << obj.isPF()
		    << std::setw(width) << obj.caloIso()     << std::setw(width) << obj.trackIso();
	    // << std::endl;
	}

	// MC match info (best-match from genParticles, delta-R based)
	if (!iEvent.isRealData()) fillMCMatchInfo(ic, genParticlesHandle, obj);
		
      }// for(size_t i=0; i<electronHandle->size(); ++i) {
    }// if(electronHandle.isValid()){
  }// for(size_t ic = 0; ic < inputCollections.size(); ++ic){

  return filter();
}


void ElectronDumper::fillMCMatchInfo(size_t ic, edm::Handle<reco::GenParticleCollection>& genParticles, const pat::Electron& ele) {
  double deltaRBestMatch = 9999.0;

  reco::Candidate::LorentzVector p4BestMatch(0,0,0,0);

  // Sanity check
  if(genParticles.isValid()){

    // For-loop: All genParticles
    for (size_t iMC=0; iMC < genParticles->size(); ++iMC) {

      // Get the genParticle
      const reco::Candidate & gp = (*genParticles)[iMC];
      
      // Skip if not an electron
      if (abs(gp.pdgId()) != 11) continue;

      // Get the 4-momentum
      reco::Candidate::LorentzVector p4 = gp.p4();

      // Calculate delta-R of genParticle (e) from pat::Electron
      double DR = deltaR(p4,ele.p4());
      if (DR < 0.1 && DR < deltaRBestMatch) {
        deltaRBestMatch = DR;
        p4BestMatch = p4;
      }

    }// for (size_t iMC=0; iMC < genParticles->size(); ++iMC) {
  }// if(genParticles.isValid()){

  // Print debugging info?
  if (cfg_debugMode){
    std::cout << std::setw(width) << deltaRBestMatch
	      << std::setw(width) << p4BestMatch.pt()     << std::setw(width) << p4BestMatch.eta() << std::setw(width) << p4BestMatch.phi()
	      << std::setw(width) << p4BestMatch.energy() << std::endl;
  }

  // Add the best match 
  MCelectron[ic].add(p4BestMatch.pt(), p4BestMatch.eta(), p4BestMatch.phi(), p4BestMatch.energy());

  return;
}


void ElectronDumper::reset(){                                                                                                                                           
  if(booked){                                                                                                                                                     

    // For-loop: All input collections
    for(size_t ic = 0; ic < inputCollections.size(); ++ic){                                                                                                       
                                                                                                                                                                  
      // Four-vector variables
      pt[ic] .clear();                                                                                                                                             
      eta[ic].clear();                                                                                                                                            
      phi[ic].clear();                                                                                                                                            
      e[ic]  .clear();                                                                                                                                              
              
      // Other essential variables
      relIsoDeltaBetaCorrected[ic].clear();
      isPF[ic]      .clear();
      caloIso[ic]   .clear();
      trackIso[ic]  .clear();
      MCelectron[ic].reset();
    }                                                                                                                                                             

    // For-loop: All discriminators
    for(size_t ic = 0; ic < inputCollections.size()*nDiscriminators; ++ic){                                                                                       
      discriminators[ic].clear();                                                                                                                                 
    }                                                                                                                                                             
  }                                                                                                                                                               
  return;
}
