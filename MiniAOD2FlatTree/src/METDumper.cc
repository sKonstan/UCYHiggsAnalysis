#include "UCYHiggsAnalysis/MiniAOD2FlatTree/interface/METDumper.h"

#include "TMath.h"

METDumper::METDumper(edm::ConsumesCollector&& iConsumesCollector, std::vector<edm::ParameterSet>& psets, bool bIsMC = true){
  inputCollections = psets;
  booked           = false;
  isMC             = bIsMC;

  // For each collection
  MET               = new double[inputCollections.size()];
  MET_x             = new double[inputCollections.size()];
  MET_y             = new double[inputCollections.size()];
  MET_significance  = new double[inputCollections.size()];
  MET_isCaloMET     = new bool[inputCollections.size()];
  MET_isPFMET       = new bool[inputCollections.size()];
  MET_isRecoMET     = new bool[inputCollections.size()];

  // Other auxiliary variables
  width = 18;
  token = new edm::EDGetTokenT<edm::View<pat::MET>>[inputCollections.size()];

  // For-loop: All input collections 
  for(size_t i = 0; i < inputCollections.size(); ++i){
    edm::InputTag inputtag = inputCollections[i].getParameter<edm::InputTag>("src");
    token[i] = iConsumesCollector.consumes<edm::View<pat::MET>>(inputtag);
  }
    
  useFilter = false;
  // For-loop: All input collections 
  for(size_t i = 0; i < inputCollections.size(); ++i){
    if(inputCollections[i].getUntrackedParameter<bool>("filter",false)) useFilter = true;
  }
}


METDumper::~METDumper(){}


void METDumper::book(TTree* tree){
  booked = true;
    
  // For-loop: All input collections 
  for(size_t i = 0; i < inputCollections.size(); ++i){
      
    // Input parameters/flags
    cfg_branchName  = inputCollections[i].getUntrackedParameter<std::string>("branchName","");
      
    if(cfg_branchName.length() == 0) cfg_branchName = inputCollections[i].getParameter<edm::InputTag>("src").label();
    // For each collection
    tree->Branch( (cfg_branchName)                  .c_str(), &MET[i]              );
    tree->Branch( (cfg_branchName + "_x")           .c_str(), &MET_x[i]            );
    tree->Branch( (cfg_branchName + "_y")           .c_str(), &MET_y[i]            );
    tree->Branch( (cfg_branchName + "_significance").c_str(), &MET_significance[i] );
    tree->Branch( (cfg_branchName + "_isCaloMET")   .c_str(), &MET_isCaloMET[i]    );
    tree->Branch( (cfg_branchName + "_isPFMET")     .c_str(), &MET_isPFMET[i]      );
    tree->Branch( (cfg_branchName + "_isRecoMET")   .c_str(), &MET_isRecoMET[i]    );
  }

  // Raw calo MET
  tree->Branch("CaloMET"      , &caloMET      );
  tree->Branch("CaloMET_x"    , &caloMET_x    );
  tree->Branch("CaloMET_y"    , &caloMET_y    );
  // tree->Branch("CaloMET_phi"  , &caloMET_phi  );
  tree->Branch("CaloMET_sumEt", &caloMET_sumEt);

  // GenMET
  if(isMC){
    tree->Branch("GenMET"                     , &GenMET                      );
    tree->Branch("GenMET_x"                   , &GenMET_x                    );
    tree->Branch("GenMET_y"                   , &GenMET_y                    );
    tree->Branch("GenMET_phi"                 , &GenMET_phi                  );
    tree->Branch("GenMET_NeutralEMEtFraction" , &GenMET_NeutralEMEtFraction  );
    tree->Branch("GenMET_NeutralEMEt"         , &GenMET_NeutralEMEt          );
    tree->Branch("GenMET_ChargedMEtFraction"  , &GenMET_ChargedEMEtFraction  );
    tree->Branch("GenMET_ChargedEMEt"         , &GenMET_ChargedEMEt          );
    tree->Branch("GenMET_NeutralHadEtFraction", &GenMET_NeutralHadEtFraction );
    tree->Branch("GenMET_NeutralHadEt"        , &GenMET_NeutralHadEt         );
    tree->Branch("GenMET_ChargedHadEtFraction", &GenMET_ChargedHadEtFraction );
    tree->Branch("GenMET_ChargedHadEt"        , &GenMET_ChargedHadEt         );
    tree->Branch("GenMET_MuonEtFraction"      , &GenMET_MuonEtFraction       );
    tree->Branch("GenMET_MuonEt"              , &GenMET_MuonEt               );
    tree->Branch("GenMET_InvisibleEtFraction" , &GenMET_InvisibleEtFraction  );
    tree->Branch("GenMET_InvisibleEt"         , &GenMET_InvisibleEt          );
  }

  return;
}


bool METDumper::fill(edm::Event& iEvent, const edm::EventSetup& iSetup){
  if (!booked) return true;

  const int index   = 0;
  // For-loop: All input collections
  for(size_t i = 0; i < inputCollections.size(); ++i){
    if (inputCollections[0].getUntrackedParameter<bool>("debugMode")) 
      {
	cfg_debugMode = true;
	break;
      }
  }


  if (cfg_debugMode){
    // std::cout << "\n" << std::setw(width*6) << cfg_branchName << std::endl;
    std::cout << std::string(width*10, '=') << std::endl;
    std::cout << "\n" << std::setw(5)  << "Index"    << std::setw(width) << "Name"    << std::setw(width) << "MET"
	      << std::setw(width)      << "MET_x"    << std::setw(width) << "MET_y"   << std::setw(width) << "MET_sig" 
	      << std::setw(width)      << "isCaloMET"<< std::setw(width) << "isPFMET" << std::setw(width) << "isRecoMET"
	      << std::endl;
    std::cout << std::string(width*10, '=') << std::endl;
  }


  // For-loop: All input collections
  for(size_t i = 0; i < inputCollections.size(); ++i){

    // Input parameters/flags
    // cfg_debugMode   = inputCollections[i].getUntrackedParameter<bool>("debugMode");
    cfg_branchName  = inputCollections[i].getUntrackedParameter<std::string>("branchName","");

    // Create edm handle and get the GenMetCollection
    edm::Handle<edm::View<pat::MET>> handle;
    iEvent.getByToken(token[i], handle);

    // Sanity check
    if(handle.isValid()){
  
      // Get the pat::MET object
      const edm::Ptr<pat::MET> patMET = handle->ptrAt(index);
      
      // For each collection
      MET[i]              = patMET->p4().Et();
      MET_x[i]            = patMET->p4().px();
      MET_y[i]            = patMET->p4().py();
      MET_significance[i] = patMET->metSignificance();
      MET_isCaloMET[i]    = patMET->isCaloMET();
      MET_isPFMET[i]      = patMET->isPFMET();
      MET_isRecoMET[i]    = patMET->isRecoMET();
      
      if (cfg_debugMode){
	std::cout << std::setw(5)     << index               << std::setw(width) << cfg_branchName    << std::setw(width) << patMET->p4().Et()
		  << std::setw(width) << patMET->p4().px()   << std::setw(width) << patMET->p4().py() << std::setw(width) << patMET->metSignificance()
		  << std::setw(width) << patMET->isCaloMET() << std::setw(width) << patMET->isPFMET() << std::setw(width) << patMET->isRecoMET()
		  << std::endl;
      }


      // GenMET
      const reco::GenMET *genMET = handle->ptrAt(index)->genMET();
      if(genMET){
	GenMET                      = genMET->et();
	GenMET_x                    = genMET->px();
	GenMET_y                    = genMET->py();
	GenMET_phi                  = genMET->phi();
	GenMET_NeutralEMEtFraction  = genMET->NeutralEMEtFraction();
	GenMET_NeutralEMEt          = genMET->NeutralEMEt();
	GenMET_ChargedEMEtFraction  = genMET->ChargedEMEtFraction();
	GenMET_ChargedEMEt          = genMET->ChargedEMEt();
	GenMET_NeutralHadEtFraction = genMET->NeutralHadEtFraction();
	GenMET_NeutralHadEt         = genMET->NeutralHadEt();
	GenMET_ChargedHadEtFraction = genMET->ChargedHadEtFraction();
	GenMET_ChargedHadEt         = genMET->ChargedHadEt();
	GenMET_MuonEtFraction       = genMET->MuonEtFraction();
	GenMET_MuonEt               = genMET->MuonEt();
	GenMET_InvisibleEtFraction  = genMET->InvisibleEtFraction();
	GenMET_InvisibleEt          = genMET->InvisibleEt();
      }

      // NOTE: Member function caloMETPt() returns caloMET only for slimmedMETs, for MET_Type1_NoHF and Puppi it seems to return the PFMET.
      // Fixed by hard coding the caloMET to use slimmedMETs
      if(inputCollections[i].getParameter<edm::InputTag>("src").label() == "slimmedMETs" && handle->ptrAt(index)->caloMETPt()){
	caloMET       = handle->ptrAt(index)->caloMETPt();
	caloMET_x     = handle->ptrAt(index)->caloMETPt() * TMath::Cos(handle->ptrAt(index)->caloMETPhi());
	caloMET_y     = handle->ptrAt(index)->caloMETPt() * TMath::Sin(handle->ptrAt(index)->caloMETPhi());
	// caloMET_phi   = handle->ptrAt(index)->caloMETPhi();
	caloMET_sumEt = handle->ptrAt(index)->caloMETSumEt();
      }
    }else{
      throw cms::Exception("config") << "Cannot find MET collection! " << inputCollections[i].getParameter<edm::InputTag>("src").label();
    }
  }

  
// Print debugging info?
if (cfg_debugMode * isMC){
  std::cout << "\n" << std::setw(width*6) << "GenMET" << std::endl;
  std::cout << std::string(width*10, '=') << std::endl;
  std::cout << std::setw(5)     << "Index"               << std::setw(width) << "GenMET" 
  	    << std::setw(width) << "EM Et Frac (0)"  << std::setw(width) << "EM Et (0)"         
	    << std::setw(width) << "EM Et Frac (+)"  << std::setw(width) << "EM Et (+)"
	    << std::setw(width) << "Had Et Frac (0)" << std::setw(width) << "Had Et (0)"
	    << std::setw(width) << "Had Et Frac (+)" << std::setw(width) << "Had Et (+)"
  	    << std::endl;
  std::cout << std::string(width*10, '=') << std::endl;

  std::cout << std::setw(5)     << index                       << std::setw(width) << GenMET	   
	    << std::setw(width) << GenMET_NeutralEMEtFraction  << std::setw(width) << GenMET_NeutralEMEt         
	    << std::setw(width) << GenMET_ChargedEMEtFraction  << std::setw(width) << GenMET_ChargedEMEt         
	    << std::setw(width) << GenMET_NeutralHadEtFraction << std::setw(width) << GenMET_NeutralHadEt
	    << std::setw(width) << GenMET_ChargedHadEtFraction << std::setw(width) << GenMET_ChargedHadEt
	    << std::endl;
 }
 
  return filter();
}


bool METDumper::filter(){
  if(!useFilter) return true;

  return true;
}


void METDumper::reset(){
  if(booked){
    
    // For-loop: All input collections 
    for(size_t i = 0; i < inputCollections.size(); ++i){

      // For each collection
      MET[i]              = 0.0;
      MET_x[i]            = 0.0;
      MET_y[i]            = 0.0;
      MET_significance[i] = 0.0;
      MET_isCaloMET[i]    = false;
      MET_isPFMET[i]      = false;
      MET_isRecoMET[i]    = false;
    }
    
    // CaloMET
    caloMET       = 0.0;
    caloMET_x     = 0.0;
    caloMET_y     = 0.0;
    // caloMET_phi   = 0.0;
    caloMET_sumEt = 0.0;
    
    // GenMET
    GenMET                      = 0.0;
    GenMET_x                    = 0.0;
    GenMET_y                    = 0.0;
    GenMET_phi                  = 0.0;
    GenMET_NeutralEMEtFraction  = 0.0;
    GenMET_NeutralEMEt          = 0.0;
    GenMET_ChargedEMEtFraction  = 0.0;
    GenMET_ChargedEMEt          = 0.0;
    GenMET_NeutralHadEtFraction = 0.0;
    GenMET_NeutralHadEt         = 0.0;        
    GenMET_ChargedHadEtFraction = 0.0;
    GenMET_ChargedHadEt         = 0.0;        
    GenMET_MuonEtFraction       = 0.0;      
    GenMET_MuonEt               = 0.0;              
    GenMET_InvisibleEtFraction  = 0.0; 
    GenMET_InvisibleEt          = 0.0;         
  }

  return;
}
