#include "UCYHiggsAnalysis/MiniAOD2FlatTree/interface/TrackDumper.h"
#include "DataFormats/VertexReco/interface/Vertex.h"

TrackDumper::TrackDumper(edm::ConsumesCollector&& iConsumesCollector, std::vector<edm::ParameterSet>& psets) {
  inputCollections = psets;
  booked           = false;

  pt    = new std::vector<double>[inputCollections.size()];
  eta   = new std::vector<double>[inputCollections.size()];    
  phi   = new std::vector<double>[inputCollections.size()];    
  e     = new std::vector<double>[inputCollections.size()];    
  pdgId = new std::vector<int>[inputCollections.size()];    

  fIPTwrtPV  = new std::vector<float>[inputCollections.size()];
  fIPzwrtPV  = new std::vector<float>[inputCollections.size()];
  fIPTSignif = new std::vector<float>[inputCollections.size()];
  fIPzSignif = new std::vector<float>[inputCollections.size()];
    
  // Tokens
  token       = new edm::EDGetTokenT<edm::View<pat::PackedCandidate>>[inputCollections.size()];
  vertexToken = new edm::EDGetTokenT<edm::View<reco::Vertex>>[inputCollections.size()];

  // Other auxiliary variables
  width                        = 12;
  cfg_debugMode                = false;
  cfg_branchName               = "";
  cfg_ptCut                    = -999.9;
  cfg_etaCut                   = -999.9;
  cfg_saveOnlyChargedParticles = false;
  cfg_IPvsPVzCut               = -999.9;

  // For-loop: All input collections
  for(size_t i = 0; i < inputCollections.size(); ++i){
    edm::InputTag inputtag = inputCollections[i].getParameter<edm::InputTag>("src");
    token[i] = iConsumesCollector.consumes<edm::View<pat::PackedCandidate>>(inputtag);
  }

  // For-loop: All input collections
  for(size_t i = 0; i < inputCollections.size(); ++i){
    edm::InputTag inputtag = inputCollections[i].getParameter<edm::InputTag>("OfflinePrimaryVertexSrc");
    vertexToken[i] = iConsumesCollector.consumes<edm::View<reco::Vertex>>(inputtag);
  }
    
  useFilter = false;
  // For-loop: All input collections
  for(size_t i = 0; i < inputCollections.size(); ++i){
    bool param = inputCollections[i].getUntrackedParameter<bool>("filter",false);
    if(param) useFilter = true;
  }
}


TrackDumper::~TrackDumper(){}


void TrackDumper::book(TTree* tree){
  booked = true;

  // For-loop: All input collections
  for(size_t i = 0; i < inputCollections.size(); ++i){
      
    // Input parameters/flags
    cfg_debugMode  = inputCollections[i].getUntrackedParameter<bool>("debugMode");
    cfg_branchName = inputCollections[i].getUntrackedParameter<std::string>("branchName","");
    if( cfg_branchName.length() == 0) cfg_branchName = inputCollections[i].getParameter<edm::InputTag>("src").label();
      
    tree->Branch( (cfg_branchName + "_pt")   .c_str(), &pt[i]    );
    tree->Branch( (cfg_branchName + "_eta")  .c_str(), &eta[i]   );
    tree->Branch( (cfg_branchName + "_phi")  .c_str(), &phi[i]   );
    tree->Branch( (cfg_branchName + "_e")    .c_str(), &e[i]     );
    tree->Branch( (cfg_branchName + "_pdgId").c_str(), &pdgId[i] );
      
    tree->Branch( (cfg_branchName + "_IPTwrtPV")       .c_str(), &fIPTwrtPV[i]  );
    tree->Branch( (cfg_branchName + "_IPzwrtPV")       .c_str(), &fIPzwrtPV[i]  );
    tree->Branch( (cfg_branchName + "_IPTSignificance").c_str(), &fIPTSignif[i] );
    tree->Branch( (cfg_branchName + "_IPzSignificance").c_str(), &fIPzSignif[i] );

  }// for(size_t i = 0; i < inputCollections.size(); ++i){

  return;
}


bool TrackDumper::fill(edm::Event& iEvent, const edm::EventSetup& iSetup){
  if (!booked) return true;

  // For-loop: All input collections
  for(size_t ic = 0; ic < inputCollections.size(); ++ic){

    // Input parameters/flags 
    cfg_debugMode                = inputCollections[ic].getUntrackedParameter<bool>("debugMode");
    cfg_branchName               = inputCollections[ic].getUntrackedParameter<std::string>("branchName","");
    cfg_ptCut                    = inputCollections[ic].getUntrackedParameter<double>("ptCut");
    cfg_etaCut                   = inputCollections[ic].getUntrackedParameter<double>("etaCut");
    cfg_saveOnlyChargedParticles = inputCollections[ic].getUntrackedParameter<bool>("saveOnlyChargedParticles");
    cfg_IPvsPVzCut               = inputCollections[ic].getUntrackedParameter<double>("IPvsPVz");

    // Create edm handle and get the PackedCandidate
    edm::Handle<edm::View<pat::PackedCandidate> > handle;
    iEvent.getByToken(token[ic], handle);

    // Create edm handle and get the OfflineVertex Collection
    edm::Handle<edm::View<reco::Vertex> > hoffvertex;
    iEvent.getByToken(vertexToken[ic], hoffvertex);
    

    // Print debugging info?
    if (cfg_debugMode){
      std::cout << "\n" << std::setw(width*8) << cfg_branchName << std::endl;
      std::cout << std::string(width*14, '=') << std::endl;
      std::cout << std::setw(5)       << "Index"
                << std::setw(width)   << "Pt"         << std::setw(width)   << "Eta"          << std::setw(width)   << "Phi"        << std::setw(width) << "E"
                << std::setw(width)   << "pdgId"      << std::setw(width)   << "IPTwrtPV"     << std::setw(width+4) << "IPTwrtPV_Sig" 
                << std::setw(width)   << "IPZwrtPV"   << std::setw(width+4) << "IPZwrtPV_Sig"
                << std::endl;
      std::cout << std::string(width*14, '=') << std::endl;
    }

    // Sanity Check
    if(handle.isValid()){

      // For-loop: All Packed PF Candidates
      for(size_t i=0; i<handle->size(); ++i) {  

	// Get the pat::PackedCandidate
	// https://cmssdt.cern.ch/SDT/doxygen/CMSSW_7_5_2/doc/html/d8/d79/classpat_1_1PackedCandidate.html
	const pat::PackedCandidate& cand = handle->at(i);

	// Apply the cuts
	if (cand.p4().pt() < cfg_ptCut) continue;
	if (std::fabs(cand.p4().eta()) > cfg_etaCut) continue;

	// Select only charged particles to save disc space
	int absPid = abs(cand.pdgId());
	if (cfg_saveOnlyChargedParticles) {
	  if (!(absPid == 11 || absPid == 13 || absPid == 211)) continue;
	}

	// Sanity check
	if (!hoffvertex->size()) continue; 

	// Convert vertex dimensions into mm
	math::XYZPoint pv(hoffvertex->at(0).x()*10.0, hoffvertex->at(0).y()*10.0, hoffvertex->at(0).z()*10.0);
	float dxy = cand.dxy(pv);
	float dz  = cand.dz(pv);

	// Save only those particles, which are within 5 mm from PV
	if (std::fabs(dz) > cfg_IPvsPVzCut) continue;

	// Calculate IP significances
	float IPTSignif = 0.0;
	if (dxy > 0.0) IPTSignif = dxy / cand.dxyError();

	float IPzSignif = 0.0;
	if (dz > 0.0) IPzSignif = dz / cand.dzError();

	// Print debugging info?
	if (cfg_debugMode){
	  std::cout << std::setw(5)     << i
		    << std::setw(width) << cand.p4().pt()  << std::setw(width) << cand.p4().eta() << std::setw(width) << cand.p4().phi() << std::setw(width) << cand.p4().energy()
		    << std::setw(width) << cand.pdgId()    << std::setw(width) << dxy             << std::setw(width+4) << IPTSignif
		    << std::setw(width) << dz              << std::setw(width+4) << IPzSignif
		    << std::endl;
	}
	
	// Save candidates which have passed the cuts
	pt[ic]   .push_back(cand.p4().pt());
	eta[ic]  .push_back(cand.p4().eta());
	phi[ic]  .push_back(cand.p4().phi());
	e[ic]    .push_back(cand.p4().energy());
	pdgId[ic].push_back(cand.pdgId());
                
	fIPTwrtPV[ic] .push_back(dxy);
	fIPzwrtPV[ic] .push_back(dz);
	fIPTSignif[ic].push_back(IPTSignif);
	fIPzSignif[ic].push_back(IPzSignif);

      }// for(size_t i=0; i<handle->size(); ++i) {
    }// if(handle.isValid()){
  }// for(size_t ic = 0; ic < inputCollections.size(); ++ic){

  return filter();
}


bool TrackDumper::filter(){
  if(!useFilter) return true;
  return true;
}


void TrackDumper::reset(){
  if(booked){

    // For-loop: All input collections
    for(size_t ic = 0; ic < inputCollections.size(); ++ic){

      pt[ic]   .clear();
      eta[ic]  .clear();
      phi[ic]  .clear();
      e[ic]    .clear();
      pdgId[ic].clear();
        
      fIPTwrtPV[ic] .clear();
      fIPzwrtPV[ic] .clear();
      fIPTSignif[ic].clear();
      fIPzSignif[ic].clear();

    }// for(size_t ic = 0; ic < inputCollections.size(); ++ic){

  }// if(booked){

  return;
}
