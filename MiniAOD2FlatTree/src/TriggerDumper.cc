#include "UCYHiggsAnalysis/MiniAOD2FlatTree/interface/TriggerDumper.h"

#include <regex>
#include "Math/VectorUtil.h"

TriggerDumper::TriggerDumper(edm::ConsumesCollector&& iConsumesCollector, const edm::ParameterSet& pset)
  : trgResultsToken(iConsumesCollector.consumes<edm::TriggerResults>(pset.getParameter<edm::InputTag>("TriggerResults"))),
    trgObjectsToken(iConsumesCollector.consumes<pat::TriggerObjectStandAloneCollection>(pset.getParameter<edm::InputTag>("TriggerObjects"))),
    trgL1ETMToken(iConsumesCollector.consumes<std::vector<l1extra::L1EtMissParticle>>(pset.getParameter<edm::InputTag>("L1Extra"))) {
  inputCollection = pset;
  booked          = false;
  cfg_triggerBits = inputCollection.getParameter<std::vector<std::string> >("TriggerBits");
  cfg_useFilter   = inputCollection.getUntrackedParameter<bool>("filter",false);
  cfg_trgMatchStr = inputCollection.getUntrackedParameter<std::vector<std::string> >("TriggerMatch",std::vector<std::string>());
  cfg_trgMatchDr  = inputCollection.getUntrackedParameter<double>("TriggerMatchDR",0.1);
  cfg_debugMode   = inputCollection.getUntrackedParameter<bool>("debugMode");
  width           = 10;
}


TriggerDumper::~TriggerDumper(){}


void TriggerDumper::book(TTree* tree){
  if (cfg_debugMode) std::cout << "void TriggerDumper::book()" << std::endl;

  theTree = tree;

  return;
}


void TriggerDumper::book(const edm::Run& iRun, HLTConfigProvider hltConfig){
  if (cfg_debugMode) std::cout << "void TriggerDumper::book()" << std::endl;

  if(booked) return;
  booked = true;

  theTree->Branch("L1MET_l1extra_x", &L1MET_l1extra_x);
  theTree->Branch("L1MET_l1extra_y", &L1MET_l1extra_y);
  theTree->Branch("L1MET_x"        , &L1MET_x        );
  theTree->Branch("L1MET_y"        , &L1MET_y        );
  theTree->Branch("HLTMET_x"       , &HLTMET_x       );
  theTree->Branch("HLTMET_y"       , &HLTMET_y       );

  theTree->Branch("HLTTau_pt"      , &HLTTau_pt      );  
  theTree->Branch("HLTTau_eta"     , &HLTTau_eta     );
  theTree->Branch("HLTTau_phi"     , &HLTTau_phi     );
  theTree->Branch("HLTTau_e"       , &HLTTau_e       );

//  theTree->Branch("HLTMu_pt"       , &HLTMu_pt      );  
//  theTree->Branch("HLTMu_eta"      , &HLTMu_eta     );
//  theTree->Branch("HLTMu_phi"      , &HLTMu_phi     );
//  theTree->Branch("HLTMu_e"        , &HLTMu_e       );
    

  // For-loop: All trigger bits (user-defined from python cfg file)
  for(size_t i = 0; i < cfg_triggerBits.size(); ++i){
    // std::cout << "cfg_triggerBits["<<i<<"] = " << cfg_triggerBits[i] << std::endl;
    selectedTriggers.push_back(cfg_triggerBits[i]);

    // NOTE: Do not find the exact names or versions of HLT path names
    // because they do change in the middle of the run causing buggy behavior
  }

  // Initialise variables
  iBit         = new bool[selectedTriggers.size()];
  iCountAll    = new int[selectedTriggers.size()];
  iCountPassed = new int[selectedTriggers.size()];

  // For-loop: All selected triggers. Create TTree TBranches
  for(size_t i = 0; i < selectedTriggers.size(); ++i){
    theTree->Branch(std::string(selectedTriggers[i] + "x" ).c_str(), &iBit[i]);
    iCountAll[i]    = 0;
    iCountPassed[i] = 0;
  }


  // Trigger matching
  std::regex obj_re("((Tau)|(Mu)|(Ele))");
  // For-loop: All triggers requested for matching
  for(size_t imatch = 0; imatch < cfg_trgMatchStr.size(); ++imatch){
    std::string name = "";
    std::smatch match;
    
    // Search for matching string to append in front of the trigger
    if (std::regex_search(cfg_trgMatchStr[imatch], match, obj_re) && match.size() > 0) name = match.str(0); 
    if(name=="Tau") name = "Taus";       // FIXME, these should come from the config
    if(name=="Mu")  name = "Muons";      // FIXME, these should come from the config    
    if(name=="Ele") name = "Electrons"; // FIXME, these should come from the config    
    name+= "_TrgMatch_";
    
    if (cfg_debugMode) std::cout << "cfg_trgMatchStr["<<imatch<<"] = " << cfg_trgMatchStr[imatch] << std::endl;
    
    std::regex match_re(cfg_trgMatchStr[imatch]);
    // For-loop: All selected triggers
    for(size_t i = 0; i < selectedTriggers.size(); ++i){		
      
      if (cfg_debugMode) std::cout << "selectedTriggers["<<i<<"] = " << selectedTriggers[i] << std::endl;
    
      if (std::regex_search(selectedTriggers[i], match_re)) {
	std::string branchName = name+cfg_trgMatchStr[imatch] + "x";
	bool exists = false;
	      
	// For-loop: All trigger match branches
	for(size_t j = 0; j < trgMatchBranches.size(); ++j){
	  
	  if (cfg_debugMode) std::cout << "trgMatchBranches["<<j<<"] = " << trgMatchBranches[j] << std::endl;	  
	  
	  if(trgMatchBranches[j] == branchName){
	    exists = true;
	    break;
	  }
	}

	if(!exists) trgMatchBranches.push_back(branchName);
      }
    }// for(size_t i = 0; i < selectedTriggers.size(); ++i){		
  }// for(size_t imatch = 0; imatch < cfg_trgMatchStr.size(); ++imatch){


  // The discriminators
  nTrgDiscriminators = trgMatchBranches.size();
  trgdiscriminators  = new std::vector<bool>[nTrgDiscriminators];

  // For-loop: All trigger match branches. Create TTree TBranches
  for(size_t i = 0; i < trgMatchBranches.size(); ++i){
    theTree->Branch(trgMatchBranches[i].c_str(), &trgdiscriminators[i]);
  }

  return;
}


bool TriggerDumper::fill(edm::Event& iEvent, const edm::EventSetup& iSetup){
  if (cfg_debugMode) std::cout << "void TriggerDumper::fill()" << std::endl;

  // Get a handle for L1 MET
  edm::Handle<std::vector<l1extra::L1EtMissParticle> > l1etmhandle;
  iEvent.getByToken(trgL1ETMToken, l1etmhandle);

  // Initialise variables
  L1MET_l1extra_x = 0.0;
  L1MET_l1extra_y = 0.0;

  // Sanity check
  if(l1etmhandle.isValid() && l1etmhandle->size() > 0){
    L1MET_l1extra_x = l1etmhandle.product()->begin()->px();
    L1MET_l1extra_y = l1etmhandle.product()->begin()->py();
  }

  // Get a handle for Trigger Results 
  edm::Handle<edm::TriggerResults> trgResultsHandle;
  iEvent.getByToken(trgResultsToken, trgResultsHandle);

  // Sanity check
  if(trgResultsHandle.isValid()){
    names = iEvent.triggerNames(*trgResultsHandle);

    // Print debugging info?
    if (cfg_debugMode){
      std::cout << "\n" << std::setw(width*8) << std::endl;
      std::cout << std::string(width*17, '=') << std::endl;
      std::cout << std::setw(5) << "Index"       << std::setw(width*6) << "Selected Trigger"  << std::setw(width*6)  
		<< "Matched edg::TriggerResults" << std::setw(width)   << "Accept" 
                << std::endl;
      std::cout << std::string(width*17, '=') << std::endl;
    }

    // For-loop: all selected triggers
    for(size_t i = 0; i < selectedTriggers.size(); ++i){
           
      // Initialise all bits to false (not fired)
      iBit[i] = false;

      // For-loop: all trigger results
      for(size_t j = 0; j < trgResultsHandle->size(); ++j){
	
	// Find the selected triggers from the pool of available trigger names
	size_t pos = names.triggerName(j).find(selectedTriggers[i]);
	// std::cout << "names.triggerName("<<j<<") = " << names.triggerName(j) << std::endl;

	// If a match is found between the selected trigger name and the currect trigger name
	if (pos == 0 && names.triggerName(j).size() > 0) {
	  if (cfg_debugMode) std::cout << std::setw(5) << i << std::setw(width*6) << selectedTriggers[i] << std::setw(width*6) << names.triggerName(j)
				       << std::setw(width)  << trgResultsHandle->accept(j) << std::endl;

	  //Set the bit result of the given trigger and increment the general counter
	  iBit[i] = trgResultsHandle->accept(j);
	  iCountAll[i] += 1;

	  // If the selected trigger bit fired increment the counter
	  if(trgResultsHandle->accept(j)) iCountPassed[i] += 1;
	  continue;
	}
      }
    }

    // Initialise variables
    L1MET_x  = 0;  
    L1MET_y  = 0;
    HLTMET_x = 0;
    HLTMET_y = 0;

    // edm::Handle<pat::TriggerObjectStandAloneCollection> patTriggerObjects;
    iEvent.getByToken(trgObjectsToken,patTriggerObjects);


    // Print debugging info?
    if (cfg_debugMode){
      std::cout << "\n" << std::setw(width*8) << std::endl;
      std::cout << std::string(width*17, '=') << std::endl;
      std::cout << std::setw(5)       << "Index"  << std::setw(width*7) << "Collection" << std::setw(width)   << "L1ETM "
		<< std::setw(width)   << "MET "   << std::setw(width)   << "Tau "       << std::setw(width)   << "Mu"
		<< std::setw(width)   << "Ele"    << std::setw(width+4) << "Pt "        << std::setw(width+4) << "Eta "
		<< std::setw(width+4) << "Phi"    << std::setw(width+4) << "Energy" 
                << std::endl;
      std::cout << std::string(width*17, '=') << std::endl;
    }

    // Sanity check
    if(patTriggerObjects.isValid()){
      int index   = -1;

      // For-loop: All PAT trigger objects
      for (pat::TriggerObjectStandAlone patTriggerObject : *patTriggerObjects) {
	// Initialise variables
	index++;
	bool bL1ETM = false;
	bool bMET   = false;
	bool bTau   = false;
	bool bMu    = false;
	bool bEle   = false;

	patTriggerObject.unpackPathNames(names);

	if(patTriggerObject.id(trigger::TriggerL1ETM)){
	  bL1ETM  = true;
	  L1MET_x = patTriggerObject.p4().x(); 
	  L1MET_y = patTriggerObject.p4().y();
	  // std::cout << "Trigger L1ETM " << patTriggerObject.p4().Pt() << std::endl;
	}

	if(patTriggerObject.id(trigger::TriggerMET)){
	  bMET     = true;
	  HLTMET_x = patTriggerObject.p4().x();
	  HLTMET_y = patTriggerObject.p4().y();
	  //std::cout << "Trigger MET " << patTriggerObject.p4().Pt() << std::endl;
	}
	
	if(patTriggerObject.id(trigger::TriggerTau)){
	  bTau = true;
	  std::vector<std::string> pathNamesAll  = patTriggerObject.pathNames(false);
	  bool fired = false;

	  // For-loop: All path names
	  for(size_t i = 0; i < pathNamesAll.size(); ++i){
	    // std::cout << "pathNamesAll["<<i<<"] = " << pathNamesAll[i] << std::endl;
	    if(patTriggerObject.hasPathName( pathNamesAll[i], false, true )) fired = true;
	  }

	  // Save the HLT tau p4 when fired
	  if(fired){
	    HLTTau_pt .push_back( patTriggerObject.p4().Pt()  );
	    HLTTau_eta.push_back( patTriggerObject.p4().Eta() );
	    HLTTau_phi.push_back( patTriggerObject.p4().Phi() );
	    HLTTau_e  .push_back( patTriggerObject.p4().E()   );	   	    
	  }
	  
	}// if(patTriggerObject.id(trigger::TriggerTau)){

	if(patTriggerObject.id(trigger::TriggerMuon)){
	  bMu = true;
	  std::vector<std::string> pathNamesAll  = patTriggerObject.pathNames(false);
	  bool fired = false;

	  // For-loop: All path names
	  for(size_t i = 0; i < pathNamesAll.size(); ++i){
	    // std::cout << "pathNamesAll["<<i<<"] = " << pathNamesAll[i] << std::endl;
	    if(patTriggerObject.hasPathName( pathNamesAll[i], false, true )) fired = true;
	  }

	  // Save the HLT tau p4 when fired
	  if(fired){
	    // HLTMu_pt .push_back( patTriggerObject.p4().Pt()  );
	    // HLTMu_eta.push_back( patTriggerObject.p4().Eta() );
	    // HLTMu_phi.push_back( patTriggerObject.p4().Phi() );
	    // HLTMu_e  .push_back( patTriggerObject.p4().E()   );	   	    
	  }
	  
	}// if(patTriggerObject.id(trigger::TriggerMuon)){


	if(patTriggerObject.id(trigger::TriggerElectron)){
	  bEle = true;
	  std::vector<std::string> pathNamesAll  = patTriggerObject.pathNames(false);
	  bool fired = false;

	  // For-loop: All path names
	  for(size_t i = 0; i < pathNamesAll.size(); ++i){
	    // std::cout << "pathNamesAll["<<i<<"] = " << pathNamesAll[i] << std::endl;
	    if(patTriggerObject.hasPathName( pathNamesAll[i], false, true )) fired = true;
	  }

	  // Save the HLT tau p4 when fired
	  if(fired){
	    // HLTMu_pt .push_back( patTriggerObject.p4().Pt()  );
	    // HLTMu_eta.push_back( patTriggerObject.p4().Eta() );
	    // HLTMu_phi.push_back( patTriggerObject.p4().Phi() );
	    // HLTMu_e  .push_back( patTriggerObject.p4().E()   );	   	    
	  }
	  
	}// if(patTriggerObject.id(trigger::TriggerElectron)){
	
	
	if (cfg_debugMode){
	  std::cout << index << std::setw(width*7) << patTriggerObject.collection() 
		    << std::setw(width) << bL1ETM  << std::setw(width) << bMET << std::setw(width) << bTau
		    << std::setw(width) << bMu     << std::setw(width) << bEle
		    << std::setw(width+4) << patTriggerObject.p4().Pt()  <<  std::setw(width+4) << patTriggerObject.p4().Eta() 
		    << std::setw(width+4) << patTriggerObject.p4().Phi() <<  std::setw(width+4) << patTriggerObject.p4().E() << std::endl;
	}

      }// for (pat::TriggerObjectStandAlone patTriggerObject : *patTriggerObjects) {
    }// if(patTriggerObjects.isValid()){
  }// if(trgResultsHandle.isValid()){

  return filter();
}


bool TriggerDumper::filter(){
  if (cfg_debugMode) std::cout << "void TriggerDumper::filter()" << std::endl;

  if(!cfg_useFilter) return true;

  bool passed = false;

  // For-loop: All trigger bits
  for(size_t i = 0; i < cfg_triggerBits.size(); ++i){
    if(iBit[i]) passed = true;
  }
  return passed;
}


void TriggerDumper::reset(){
  if (cfg_debugMode) std::cout << "void TriggerDumper::reset()" << std::endl;
  
  if(booked){

    // For-loop: All trigger bits
    for(size_t i = 0; i < cfg_triggerBits.size(); ++i) iBit[i] = 0;

    L1MET_x  = 0;
    L1MET_y  = 0;
    HLTMET_x = 0;
    HLTMET_y = 0;

    HLTTau_pt .clear();
    HLTTau_eta.clear();
    HLTTau_phi.clear();
    HLTTau_e  .clear();

//    HLTMu_pt .clear();
//    HLTMu_eta.clear();
//    HLTMu_phi.clear();
//    HLTMu_e  .clear();

    // For-loop: All trigger discriminators
    for(int i = 0; i < nTrgDiscriminators; ++i) trgdiscriminators[i].clear();
  }// if(booked){

  return;
}


std::pair<int,int> TriggerDumper::counters(std::string path){
  if (cfg_debugMode) std::cout << "void TriggerDumper::counters()" << std::endl;

  int index = -1;
  // Forl-loop: All selected triggers
  for(size_t i = 0; i < selectedTriggers.size(); ++i){
    if(path==selectedTriggers[i]){
      index = i;
      break;
    }
  }
  
  if(index == -1) return std::pair<int,int>(0,0);
  
  return std::pair<int,int>(iCountAll[index],iCountPassed[index]);
}


void TriggerDumper::triggerMatch(int id, std::vector<reco::Candidate::LorentzVector> objs){
  if (cfg_debugMode) std::cout << "void TriggerDumper::triggerMatch()" << std::endl;
  // Called inside MiniAOD2FlatTreeFilter.cc

  // For-loop: All objects
  for(size_t iobj = 0; iobj < objs.size(); ++iobj){

    // For-loop: All trigger discriminators
    for(int i = 0; i < nTrgDiscriminators; ++i){
      bool matchFound = false;

      std::string matchedTrgObject = trgMatchBranches[i];
      size_t len = matchedTrgObject.length();
      size_t pos = matchedTrgObject.find("_TrgMatch_") + 10;
      matchedTrgObject = matchedTrgObject.substr(pos, len-pos);

      if(!isCorrectObject(id, matchedTrgObject)) continue;

      // Sanity check
      if(patTriggerObjects.isValid()){

	// For-loop: All PAT trigger objects
	for (pat::TriggerObjectStandAlone patTriggerObject : *patTriggerObjects) {
	  patTriggerObject.unpackPathNames(names);
	  
	  if(patTriggerObject.id(id)){
	    bool fired = false;
	    std::vector<std::string> pathNamesAll  = patTriggerObject.pathNames(false);
	    std::regex match_re(matchedTrgObject);

	    // For-loop: All paths
	    for(size_t i = 0; i < pathNamesAll.size(); ++i){

	      if (std::regex_search(pathNamesAll[i], match_re)) {
		if(patTriggerObject.hasPathName( pathNamesAll[i], false, true )) fired = true;
	      }
	    }
	    if(!fired) continue;

	    double dr = ROOT::Math::VectorUtil::DeltaR(objs[iobj],patTriggerObject.p4());
	    if(dr < cfg_trgMatchDr) matchFound = true;
	    
	  }// if(patTriggerObject.id(id)){	  	  
	}// for (pat::TriggerObjectStandAlone patTriggerObject : *patTriggerObjects) {
      }// if(patTriggerObjects.isValid()){

      trgdiscriminators[i].push_back(matchFound);

    }// for(int i = 0; i < nTrgDiscriminators; ++i){          
  }// for(size_t iobj = 0; iobj < objs.size(); ++iobj){

  return;
}


bool TriggerDumper::isCorrectObject(int id, std::string trgObject){
  if (cfg_debugMode) std::cout << "void TriggerDumper::isCorrect()" << std::endl;

  //http://cmslxr.fnal.gov/source/DataFormats/HLTReco/interface/TriggerTypeDefs.h
  std::string sid = "";
  switch (id) {
  case trigger::TriggerTau:
    sid = "Tau";
    break;
  case trigger::TriggerMuon:
    sid = "Mu";
    break;
  case trigger::TriggerElectron:
    sid = "Ele";
    break;
  default:
    std::cout << "Unknown trigger id " << id << " exiting.." << std::endl;
    exit(1);
  }

  if(trgObject.find(sid) < trgObject.length()) return true;
  return false;  
}
