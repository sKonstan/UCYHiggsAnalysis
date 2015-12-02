#include "UCYHiggsAnalysis/MiniAOD2FlatTree/interface/MuonDumper.h"

#include "DataFormats/VertexReco/interface/Vertex.h"

MuonDumper::MuonDumper(edm::ConsumesCollector&& iConsumesCollector, std::vector<edm::ParameterSet>& psets, const edm::InputTag& recoVertexTag)
  : genParticleToken(iConsumesCollector.consumes<reco::GenParticleCollection>(edm::InputTag("prunedGenParticles"))),
    vertexToken(iConsumesCollector.consumes<edm::View<reco::Vertex>>(recoVertexTag)) {
  inputCollections = psets;
  booked           = false;

  // Four-vector variables
  pt  = new std::vector<double>[inputCollections.size()];
  eta = new std::vector<double>[inputCollections.size()];    
  phi = new std::vector<double>[inputCollections.size()];    
  e   = new std::vector<double>[inputCollections.size()];    

  // Other essential variables 
  isGlobalMuon = new std::vector<bool>[inputCollections.size()];
  isLooseMuon  = new std::vector<bool>[inputCollections.size()];
  isMediumMuon = new std::vector<bool>[inputCollections.size()];
  isTightMuon  = new std::vector<bool>[inputCollections.size()];
  ecalIso      = new std::vector<float>[inputCollections.size()];
  hcalIso      = new std::vector<float>[inputCollections.size()];
  caloIso      = new std::vector<float>[inputCollections.size()];
  relIsoDeltaBetaCorrected = new std::vector<float>[inputCollections.size()];

  MCmuon          = new FourVectorDumper[inputCollections.size()];
  nDiscriminators = inputCollections[0].getParameter<std::vector<std::string> >("discriminators").size();
  discriminators  = new std::vector<bool>[inputCollections.size()*nDiscriminators];    

  // Tokens
  muonToken = new edm::EDGetTokenT<edm::View<pat::Muon>>[inputCollections.size()];

  // Other auxiliary variables
  width          = 10;
  cfg_debugMode  = false;
  cfg_branchName = "";

  // For-loop: All input collections
  for(size_t i = 0; i < inputCollections.size(); ++i){
    edm::InputTag inputtag = inputCollections[i].getParameter<edm::InputTag>("src");
    muonToken[i] = iConsumesCollector.consumes<edm::View<pat::Muon>>(inputtag);
  }
    
  useFilter = false;
  // For-loop: All input collections
  for(size_t i = 0; i < inputCollections.size(); ++i){
    bool param = inputCollections[i].getUntrackedParameter<bool>("filter",false);
    if(param) useFilter = true;
  }
}


MuonDumper::~MuonDumper(){}


void MuonDumper::book(TTree* tree){
  booked = true;

  // For-loop: All input collections
  for(size_t i = 0; i < inputCollections.size(); ++i){

    // Input parameters/flags
    cfg_debugMode  = inputCollections[i].getUntrackedParameter<bool>("debugMode");
    cfg_branchName = inputCollections[i].getUntrackedParameter<std::string>("branchName","");

    if(cfg_branchName.length() == 0) cfg_branchName = inputCollections[i].getParameter<edm::InputTag>("src").label();

    // Four-vector variables    
    tree->Branch( (cfg_branchName + "_pt")  .c_str(), &pt[i]  );
    tree->Branch( (cfg_branchName + "_eta") .c_str(), &eta[i] );
    tree->Branch( (cfg_branchName  + "_phi").c_str(), &phi[i] );
    tree->Branch( (cfg_branchName + "_e")   .c_str(), &e[i]   );

    // Other essential variables 
    tree->Branch( (cfg_branchName + "_isGlobalMuon")   .c_str(), &isGlobalMuon[i]  );
    tree->Branch( (cfg_branchName + "_muIDLoose")      .c_str(), &isLooseMuon[i]   );
    tree->Branch( (cfg_branchName + "_muIDMedium")     .c_str(), &isMediumMuon[i]  );
    tree->Branch( (cfg_branchName + "_muIDTight")      .c_str(), &isTightMuon[i]   );
    tree->Branch( (cfg_branchName + "_ecalIso")        .c_str(), &ecalIso[i]       );
    tree->Branch( (cfg_branchName + "_hcalIso")        .c_str(), &hcalIso[i]       );
    tree->Branch( (cfg_branchName + "_caloIso")        .c_str(), &caloIso[i]       );
    tree->Branch( (cfg_branchName + "_relIsoDeltaBeta").c_str(), &relIsoDeltaBetaCorrected[i] );

    MCmuon[i].book(tree, cfg_branchName, "MCmuon");
        
    std::vector<std::string> discriminatorNames = inputCollections[i].getParameter<std::vector<std::string> >("discriminators");
    // For-loop: All discriminators
    for(size_t iDiscr = 0; iDiscr < discriminatorNames.size(); ++iDiscr) {
      tree->Branch((cfg_branchName + "_" + discriminatorNames[iDiscr]).c_str(), &discriminators[inputCollections.size()*iDiscr+i]);
    }

  }// for(size_t i = 0; i < inputCollections.size(); ++i){

  return;
}


bool MuonDumper::fill(edm::Event& iEvent, const edm::EventSetup& iSetup){
  if (!booked) return true;
    
  // Create edm handle and get the GenParticleCollection (only if not real data)
  edm::Handle <reco::GenParticleCollection> genParticlesHandle;
  if (!iEvent.isRealData()) iEvent.getByToken(genParticleToken, genParticlesHandle);

  // Get vertex
  edm::Handle<edm::View<reco::Vertex> > vertexHandle;
  iEvent.getByToken(vertexToken, vertexHandle);
    
  // For-loop: All input collections
  for(size_t ic = 0; ic < inputCollections.size(); ++ic){
   
    edm::InputTag inputtag = inputCollections[ic].getParameter<edm::InputTag>("src");
    std::vector<std::string> discriminatorNames = inputCollections[ic].getParameter<std::vector<std::string> >("discriminators");

    // Create edm handle and get the pat::Muon collection
    edm::Handle<edm::View<pat::Muon>> muonHandle;
    iEvent.getByToken(muonToken[ic], muonHandle);

    // Print debugging info?
    if (cfg_debugMode){
      std::cout << "\n" << std::setw(width*8) << cfg_branchName << std::endl;
      std::cout << std::string(width*17, '=') << std::endl;
      std::cout << std::setw(5)       << "Index"
                << std::setw(width)   << "Pt"             << std::setw(width) << "Eta"      << std::setw(width) << "Phi"      << std::setw(width) << "E"
	// << std::setw(width) << "RelIso"         << std::setw(width) << "ecalIso"  << std::setw(width) << "hcalIso"  << std::setw(width) << "caloIso"
		<< std::setw(width)   << "RelIso"         << std::setw(width) << "caloIso"
                << std::setw(width)   << "isLoose"        << std::setw(width) << "isMedium" << std::setw(width) << "isTight"  << std::setw(width) << "isGlobal"
                << std::setw(width*2) << "deltaR"         << std::setw(width) << "Pt"       << std::setw(width) << "Eta"      << std::setw(width) << "Phi"
                << std::setw(width)   << "E"
                << std::endl;
      std::cout << std::string(width*17, '=') << std::endl;
    }
    
    // Sanity check
    if(muonHandle.isValid()){

      // For-loop: All muons
      for(size_t i=0; i<muonHandle->size(); ++i) {

	// Get the pat::Muon
	const pat::Muon& obj = muonHandle->at(i);

	// Four-vector variables
	pt[ic] .push_back( obj.p4().pt()     );
	eta[ic].push_back( obj.p4().eta()    );
	phi[ic].push_back( obj.p4().phi()    );
	e[ic]  .push_back( obj.p4().energy() );
                
	// Other essential variables [https://twiki.cern.ch/twiki/bin/view/CMS/SWGuideMuonIdRun2]
	isGlobalMuon[ic].push_back( obj.isGlobalMuon() );
	isLooseMuon[ic] .push_back( obj.isLooseMuon()  );
	isMediumMuon[ic].push_back( obj.isMediumMuon() );
	ecalIso[ic]     .push_back( obj.ecalIso()      );
	hcalIso[ic]     .push_back( obj.hcalIso()      );
	caloIso[ic]     .push_back( obj.caloIso()      );

	// Tight Discriminator
	bool bIsTightMuon = false;
	if (vertexHandle->size() == 0) bIsTightMuon = false;
	else bIsTightMuon = obj.isTightMuon(vertexHandle->at(0));
	isTightMuon[ic].push_back(bIsTightMuon);
	
	// Relative isolation in cone of DeltaR=0.3
	double isolation = (obj.pfIsolationR03().sumChargedHadronPt 
			    + std::max(obj.pfIsolationR03().sumNeutralHadronEt + obj.pfIsolationR03().sumPhotonEt - 0.5 * obj.pfIsolationR03().sumPUPt, 0.0));
	double relIso = isolation / obj.pt();
	relIsoDeltaBetaCorrected[ic].push_back(relIso);

	// For-loop: All discriminators
	for(size_t iDiscr = 0; iDiscr < discriminatorNames.size(); ++iDiscr) {
	  discriminators[inputCollections.size()*iDiscr+ic].push_back(obj.muonID(discriminatorNames[iDiscr]));
	}
		
	// Print debugging info? 
	if(cfg_debugMode){
	  std::cout << std::setw(5)     << i
		    << std::setw(width)<< obj.p4().pt()    << std::setw(width) << obj.p4().eta()     << std::setw(width) << obj.p4().phi() << std::setw(width) << obj.p4().energy()
	    // << std::setw(width)<< relIso           << std::setw(width) << obj.ecalIso()      << std::setw(width) << obj.hcalIso()  << std::setw(width) << obj.caloIso()
		    << std::setw(width)<< relIso           << std::setw(width) << obj.caloIso()
		    << std::setw(width)<< obj.isLooseMuon()<< std::setw(width) << obj.isMediumMuon() << std::setw(width) << bIsTightMuon
		    << std::setw(width)<< obj.isGlobalMuon();
	}

	// MC match info (best-match from genParticles, delta-R based)
	if (!iEvent.isRealData()) fillMCMatchInfo(ic, genParticlesHandle, obj);

      }// for(size_t i=0; i<muonHandle->size(); ++i) {
    }// if(muonHandle.isValid()){
  }// for(size_t ic = 0; ic < inputCollections.size(); ++ic){

  return filter();
}


void MuonDumper::fillMCMatchInfo(size_t ic, edm::Handle<reco::GenParticleCollection>& genParticles, const pat::Muon& ele) {
  double deltaRBestMatch = 9999.0;

  reco::Candidate::LorentzVector p4BestMatch(0,0,0,0);
  
  // Sanity check
  if(genParticles.isValid()){

    // For-loop: All genParticles
    for (size_t iMC=0; iMC < genParticles->size(); ++iMC) {
      
      // Get the genParticle
      const reco::Candidate & gp = (*genParticles)[iMC];

      // Skip if not a muon
      if (abs(gp.pdgId()) != 13) continue;

      // Get the 4-momentum
      reco::Candidate::LorentzVector p4 = gp.p4();

      // Calculate delta-R of genParticle (muon) from pat:Muon
      double DR = deltaR(p4,ele.p4());      
      if (DR < 0.1 && DR < deltaRBestMatch) {
        deltaRBestMatch = DR;
        p4BestMatch = p4;
      }

    }// for (size_t iMC=0; iMC < genParticles->size(); ++iMC) {
  }// if(genParticles.isValid()){
  
  // Print debugging info?
  if (cfg_debugMode){
    std::cout << std::setw(width*2) << deltaRBestMatch
              << std::setw(width)   << p4BestMatch.pt()     << std::setw(width) << p4BestMatch.eta() << std::setw(width) << p4BestMatch.phi()
              << std::setw(width)   << p4BestMatch.energy() << std::endl;
  }
  
  // Add the best match
  MCmuon[ic].add(p4BestMatch.pt(), p4BestMatch.eta(), p4BestMatch.phi(), p4BestMatch.energy());
  
  return;
}


void MuonDumper::reset(){                                                                                                                                           
  if(booked){          

    // For-loop: All input collections
    for(size_t ic = 0; ic < inputCollections.size(); ++ic){                                                                                                       
          
      // Four-vector variables
      pt[ic] .clear();
      eta[ic].clear();
      phi[ic].clear();
      e[ic]  .clear();

      // Other essential variables
      isGlobalMuon[ic].clear();
      isLooseMuon[ic] .clear();
      isMediumMuon[ic].clear();
      isTightMuon[ic] .clear();
      ecalIso[ic]     .clear();
      hcalIso[ic]     .clear();
      caloIso[ic]     .clear();        
      relIsoDeltaBetaCorrected[ic].clear();

      MCmuon[ic].reset();
    }        
    
    // For-loop: All input collections
    for(size_t ic = 0; ic < inputCollections.size()*nDiscriminators; ++ic){
      discriminators[ic].clear();
    }

  }// if(booked){
  
  return;
}
