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

  // GenJet Constituents (Optional)
  genConstituentsPt      = new std::vector< std::vector<double> >;
  genConstituentsEta     = new std::vector< std::vector<double> >;
  genConstituentsPhi     = new std::vector< std::vector<double> >;
  genConstituentsE       = new std::vector< std::vector<double> >;
  genConstituentsPdgId   = new std::vector< std::vector<short> >;
  genConstituentsStatus  = new std::vector< std::vector<short> >;
  genConstituentsCharge  = new std::vector< std::vector<short> >;
  genConstituentsVertexX = new std::vector< std::vector<double> >;
  genConstituentsVertexY = new std::vector< std::vector<double> >;
  genConstituentsVertexZ = new std::vector< std::vector<double> >;

  // Other auxiliary variables 
  width = 14;
  cfg_debugMode = false;
  cfg_branchName = "";
  cfg_saveGenJetConstituents = false;

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
      
    // Input parameters/flags
    cfg_branchName             = inputCollections[i].getUntrackedParameter<std::string>("branchName","");
    cfg_saveGenJetConstituents = inputCollections[i].getUntrackedParameter<bool>("saveGenJetConstituents","");
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
    
    // GenJet Constituents (Optional)
    if(cfg_saveGenJetConstituents){
      tree->Branch( ( cfg_branchName + "_genConstituentsPt" )   .c_str(), &genConstituentsPt[i]      );
      tree->Branch( ( cfg_branchName + "_genConstituentsEta")   .c_str(), &genConstituentsEta[i]     );
      tree->Branch( ( cfg_branchName + "_genConstituentsPhi")   .c_str(), &genConstituentsPhi[i]     );
      tree->Branch( ( cfg_branchName + "_genConstituentsE")     .c_str(), &genConstituentsE[i]       );
      tree->Branch( ( cfg_branchName + "_genConstituentsPdgId") .c_str(), &genConstituentsPdgId[i]   );
      tree->Branch( ( cfg_branchName + "_genConstituentsStatus").c_str(), &genConstituentsStatus[i]  );
      tree->Branch( ( cfg_branchName + "_genConstituentsCharge").c_str(), &genConstituentsCharge[i]  );
      tree->Branch( ( cfg_branchName + "_genConstituentsVerteX").c_str(), &genConstituentsVertexX[i] );
      tree->Branch( ( cfg_branchName + "_genConstituentsVerteY").c_str(), &genConstituentsVertexY[i] );
      tree->Branch( ( cfg_branchName + "_genConstituentsVerteZ").c_str(), &genConstituentsVertexZ[i] );
    }

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

	// Other essential variables [https://twiki.cern.ch/twiki/bin/view/CMSPublic/WorkBookMiniAOD2015#GenJets]
	charge[ic]          .push_back( gj.charge()          );
	emEnergy[ic]        .push_back( gj.emEnergy()        );
	hadEnergy[ic]       .push_back( gj.hadEnergy()       );
	auxEnergy[ic]       .push_back( gj.auxiliaryEnergy() );
	invisEnergy[ic]     .push_back( gj.invisibleEnergy() );
	// Get the GenJet constituents (alternative)
	nGenConstituents[ic].push_back( gj.numberOfDaughters() );

	// Save the genJet constituents? Since the genParticles are filtered (pruned) then these might not be available otherwise!
	if(cfg_saveGenJetConstituents){

	  std::vector<double>  genConstituentsPt_tmp;
	  std::vector<double>  genConstituentsEta_tmp;
	  std::vector<double>  genConstituentsPhi_tmp;
	  std::vector<double>  genConstituentsE_tmp;
	  std::vector<short>   genConstituentsPdgId_tmp;
	  std::vector<short>   genConstituentsStatus_tmp;
	  std::vector<short>   genConstituentsCharge_tmp;
	  std::vector<double>  genConstituentsVertexX_tmp;
	  std::vector<double>  genConstituentsVertexY_tmp;
	  std::vector<double>  genConstituentsVertexZ_tmp;
	  
	  // For-loop: All daughters (constituents) of genJet
	  for(Size_t idau=0; idau<gj.numberOfDaughters(); idau++){
	    
	    // Get the reco::Candidate daughter
	    const reco::Candidate* Dau = gj.daughter(idau);

	    // Fill temporary containers
	    genConstituentsPt_tmp     .push_back( Dau->pt()     );
	    genConstituentsEta_tmp    .push_back( Dau->eta()    );
	    genConstituentsPhi_tmp    .push_back( Dau->phi()    );
	    genConstituentsE_tmp      .push_back( Dau->energy() );
	    genConstituentsPdgId_tmp  .push_back( Dau->pdgId()  );
	    genConstituentsStatus_tmp .push_back( Dau->status() );
	    genConstituentsCharge_tmp .push_back( Dau->charge() );
	    genConstituentsVertexX_tmp.push_back( Dau->vx()     );
	    genConstituentsVertexY_tmp.push_back( Dau->vy()     );
	    genConstituentsVertexZ_tmp.push_back( Dau->vz()     );
	  }
	  
	  genConstituentsPt[ic]     .push_back( genConstituentsPt_tmp      );
	  genConstituentsEta[ic]    .push_back( genConstituentsEta_tmp     );
	  genConstituentsPhi[ic]    .push_back( genConstituentsPhi_tmp     );
	  genConstituentsE[ic]      .push_back( genConstituentsE_tmp       );
	  genConstituentsPdgId[ic]  .push_back( genConstituentsPdgId_tmp   );
	  genConstituentsStatus[ic] .push_back( genConstituentsStatus_tmp  );
	  genConstituentsCharge[ic] .push_back( genConstituentsCharge_tmp  );
	  genConstituentsVertexX[ic].push_back( genConstituentsVertexX_tmp );
	  genConstituentsVertexY[ic].push_back( genConstituentsVertexY_tmp );
	  genConstituentsVertexZ[ic].push_back( genConstituentsVertexZ_tmp );

	}// if(cfg_saveGenJetConstituents){


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

      if(cfg_saveGenJetConstituents){
	genConstituentsPt[ic]     .clear();
	genConstituentsEta[ic]    .clear();
	genConstituentsPhi[ic]    .clear();
	genConstituentsE[ic]      .clear();
	genConstituentsPdgId[ic]  .clear();
	genConstituentsStatus[ic] .clear();
	genConstituentsCharge[ic] .clear();
	genConstituentsVertexX[ic].clear();
	genConstituentsVertexY[ic].clear();
	genConstituentsVertexZ[ic].clear();
      }

    }// for(size_t ic = 0; ic < inputCollections.size(); ++ic){
    
  }// if(booked){

  return;
}
