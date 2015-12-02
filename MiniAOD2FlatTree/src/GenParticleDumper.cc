#include "UCYHiggsAnalysis/MiniAOD2FlatTree/interface/GenParticleDumper.h"
#include "UCYHiggsAnalysis/MiniAOD2FlatTree/interface/NtupleAnalysis_fwd.h"
#include "UCYHiggsAnalysis/MiniAOD2FlatTree/interface/GenParticleTools.h"

#include "TLorentzVector.h"


GenParticleDumper::GenParticleDumper(edm::ConsumesCollector&& iConsumesCollector, std::vector<edm::ParameterSet>& psets){
  inputCollections = psets;
  booked           = false;

  // Four-vector variables (with fixes initial size)
  pt        = new std::vector<double>[inputCollections.size()];
  eta       = new std::vector<double>[inputCollections.size()];    
  phi       = new std::vector<double>[inputCollections.size()];    
  e         = new std::vector<double>[inputCollections.size()];    
  // Other essential variables (with fixed initial size)
  pdgId     = new std::vector<short>[inputCollections.size()];
  mass      = new std::vector<double>[inputCollections.size()];
  vertexX   = new std::vector<double>[inputCollections.size()];
  vertexY   = new std::vector<double>[inputCollections.size()];
  vertexZ   = new std::vector<double>[inputCollections.size()];
  charge    = new std::vector<short>[inputCollections.size()];
  status    = new std::vector<short>[inputCollections.size()];
  mothers   = new std::vector< std::vector<unsigned short> >;
  daughters = new std::vector< std::vector<unsigned short> >;

  // Electrons
  electrons = new FourVectorDumper[inputCollections.size()];
  
  // Muons
  muons = new FourVectorDumper[inputCollections.size()];
  
  // Taus
  taus                   = new FourVectorDumper[inputCollections.size()];
  visibleTaus            = new FourVectorDumper[inputCollections.size()];
  tauNcharged            = new std::vector<short>[inputCollections.size()];
  tauNPi0                = new std::vector<short>[inputCollections.size()];
  tauRtau                = new std::vector<double>[inputCollections.size()];
  tauAssociatedWithHiggs = new short[inputCollections.size()];
  tauMother              = new std::vector<short>[inputCollections.size()];
  tauDecaysToElectron    = new std::vector<bool>[inputCollections.size()];
  tauDecaysToMuon        = new std::vector<bool>[inputCollections.size()];
  tauSpinEffects         = new std::vector<double>[inputCollections.size()];
  tauNeutrinos           = new FourVectorDumper[inputCollections.size()];  

  // Neutrinos
  neutrinos = new FourVectorDumper[inputCollections.size()];

  // Tokens
  token = new edm::EDGetTokenT<reco::GenParticleCollection>[inputCollections.size()];
  // handle = new edm::Handle<reco::GenParticleCollection>[inputCollections.size()];
  
  // Other auxiliary variables
  width = 14;
  cfg_branchName = "";
  cfg_debugMode  = false;
	
  // For-loop: All input collections
  for(size_t i = 0; i < inputCollections.size(); ++i){
    edm::InputTag inputtag = inputCollections[i].getParameter<edm::InputTag>("src");
    token[i] = iConsumesCollector.consumes<reco::GenParticleCollection>(inputtag);
  }
  
  useFilter = false;
  // For-loop: All input collections
  for(size_t i = 0; i < inputCollections.size(); ++i){
      bool param = inputCollections[i].getUntrackedParameter<bool>("filter",false);
      if(param) useFilter = true;
  }

}


GenParticleDumper::~GenParticleDumper(){}


void GenParticleDumper::book(TTree* tree){
  booked = true;

  // For-loop: Input collections
  for(size_t i = 0; i < inputCollections.size(); ++i){
   
    // Input parameters/flags
    cfg_branchName = inputCollections[i].getUntrackedParameter<std::string>("branchName","");
    
    if(cfg_branchName.length() == 0) cfg_branchName = inputCollections[i].getParameter<edm::InputTag>("src").label();

    // Save GenParticles?
    if (inputCollections[i].getUntrackedParameter<bool>("saveAllGenParticles", false)) {

      // Four-vector variables
      tree->Branch( ( cfg_branchName+"_pt") .c_str(), &pt[i]  );
      tree->Branch( ( cfg_branchName+"_eta").c_str(), &eta[i] );
      tree->Branch( ( cfg_branchName+"_phi").c_str(), &phi[i] );
      tree->Branch( ( cfg_branchName+"_e")  .c_str(), &e[i]   );
      // Other essential variables
      tree->Branch( ( cfg_branchName+"_pdgId")    .c_str(), &pdgId[i]     );
      tree->Branch( ( cfg_branchName+"_mass")     .c_str(), &mass[i]      ); 
      tree->Branch( ( cfg_branchName+"_vertexX")  .c_str(), &vertexX[i]   ); 
      tree->Branch( ( cfg_branchName+"_vertexY")  .c_str(), &vertexY[i]   ); 
      tree->Branch( ( cfg_branchName+"_vertexZ")  .c_str(), &vertexZ[i]   ); 
      tree->Branch( ( cfg_branchName+"_charge")   .c_str(), &charge[i]    );
      tree->Branch( ( cfg_branchName+"_status")   .c_str(), &status[i]    );
      tree->Branch( ( cfg_branchName+"_mothers")  .c_str(), &mothers[i]   );
      tree->Branch( ( cfg_branchName+"_daughters").c_str(), &daughters[i] );

    }// if (inputCollections[i].getUntrackedParameter<bool>("saveAllGenParticles", false)) {
    
    // Save electrons?
    if (inputCollections[i].getUntrackedParameter<bool>("saveGenElectrons", false)) electrons[i].book(tree, cfg_branchName, "Electrons");

    // Save muons?
    if (inputCollections[i].getUntrackedParameter<bool>("saveGenMuons", false)) muons[i].book(tree, cfg_branchName, "Muons");

    // Save taus?    
    if (inputCollections[i].getUntrackedParameter<bool>("saveGenTaus", false)) {
      taus[i].book(tree, cfg_branchName, "Taus");
      visibleTaus[i].book(tree, cfg_branchName, "VisibleTau");
      tree->Branch( ( cfg_branchName + "_TauProngs").c_str(),&tauNcharged[i]);
      tree->Branch( ( cfg_branchName + "_TauNpi0").c_str(),&tauNPi0[i]);
      tree->Branch( ( cfg_branchName + "_TauRtau").c_str(),&tauRtau[i]);
      tree->Branch( ( cfg_branchName + "_TauAssociatedWithHiggs").c_str(),&tauAssociatedWithHiggs[i]);
      tree->Branch( ( cfg_branchName + "_TauMother").c_str(),&tauMother[i]);
      tree->Branch( ( cfg_branchName + "_TauDecaysToElectron").c_str(),&tauDecaysToElectron[i]);
      tree->Branch( ( cfg_branchName + "_TauDecaysToMuon").c_str(),&tauDecaysToMuon[i]);
      tree->Branch( ( cfg_branchName + "_TauSpinEffects").c_str(),&tauSpinEffects[i]);
      tauNeutrinos[i].book(tree, cfg_branchName, "TauNeutrinos");
    }

    // Save neutrinos?
    if (inputCollections[i].getUntrackedParameter<bool>("saveGenNeutrinos", false)) neutrinos[i].book(tree, cfg_branchName, "Neutrinos");

  }// for(size_t i = 0; i < inputCollections.size(); ++i){
  
  return;
}


bool GenParticleDumper::fill(edm::Event& iEvent, const edm::EventSetup& iSetup){
  if (!booked) return true;

  // For-loop: All collections
  for(size_t ic = 0; ic < inputCollections.size(); ++ic){

    // Input parameters/flags
    cfg_debugMode  = inputCollections[ic].getUntrackedParameter<bool>("debugMode");
    cfg_branchName = inputCollections[ic].getUntrackedParameter<std::string>("branchName","");
    
    // Create edm handle and get the GenParticleCollection
    edm::Handle<reco::GenParticleCollection> handle;
    iEvent.getByToken(token[ic], handle);

    // Print debugging info?
    if (cfg_debugMode){
      std::cout << std::setw(width*6) << cfg_branchName << std::endl;
      std::cout << std::string(width*13, '=') << std::endl;
      std::cout << std::setw(5)     << "Index"
		<< std::setw(width) << "Pt"        << std::setw(width) << "Eta"   << std::setw(width) << "Phi" << std::setw(width) << "E"
		<< std::setw(width) << "Status"    << std::setw(width) << "PdgId" << std::setw(width) << "Moms"  
		<< std::setw(width) << "Daughters" << std::setw(width) << "Mass"  << std::setw(width) << "Charge" 
		<< std::setw(width) << "Vtx-X"     << std::setw(width) << "Vtx-Y" << std::setw(width) << "Vtx-Z" << std::endl;
      std::cout << std::string(width*13, '=') << std::endl;
    }
    
    // Sanity check
    if(handle.isValid()){

      // General particle list
      if (inputCollections[ic].getUntrackedParameter<bool>("saveAllGenParticles", false)) {

	// For-loop: GenParticles (gp)
        for(size_t gp_index = 0; gp_index < handle->size(); ++gp_index) {

	  // Get the GenParticle
          const reco::Candidate & gp = handle->at(gp_index);

	  // Four-vector variables
          pt[ic] .push_back( gp.pt()     );
          eta[ic].push_back( gp.eta()    );
          phi[ic].push_back( gp.phi()    );
          e[ic]  .push_back( gp.energy() );   
	  // Other essential variables
          pdgId[ic]  .push_back( gp.pdgId()  );
	  mass[ic]   .push_back( gp.mass()   );
	  vertexX[ic].push_back( gp.vx()     );
	  vertexY[ic].push_back( gp.vy()     );
	  vertexZ[ic].push_back( gp.vz()     );
	  charge[ic] .push_back( gp.charge() );	  
	  status[ic] .push_back( gp.status() );
	  
	  // Find index for all mothers
 	  std::vector<unsigned short> mothers_tmp;
	  short gpMom_index = -1;

	  // For-loop: mothers
	  for(size_t iMom = 0; iMom < gp.numberOfMothers(); iMom++) {	      

	    // Sanity check
	    if (gp.mother(iMom) == nullptr) continue;
	    
	    // For-loop: GenParticles
	    for(size_t j = 0; j < handle->size(); ++j) {
	      
	      // Find the index of the mother by comparing memory addresses
	      if ( gp.mother(iMom) == &(handle->at(j)) ) gpMom_index = j;
	      
	    }// for(size_t j = 0; j < handle->size(); ++j) {
	    mothers_tmp.push_back(gpMom_index);

	  }// for(unsigned int iMom = 0; iMom < gp.numberOfMothers(); iMom++){
 	  mothers[ic].push_back(mothers_tmp);


	  // Find index of all daughters
	  std::vector<unsigned short> daughters_tmp;
	  short gpDau_index = -1;
	  // For-loop: daughters
	  for(size_t iDau = 0; iDau < gp.numberOfDaughters(); iDau++){

	    // Sanity check
	    if (gp.daughter(iDau) == nullptr) continue;

	    // For-loop: GenParticles
	    for(size_t k = 0; k < handle->size(); ++k) {
	      
	      // Find the index of the mother by comparing memory addresses
	      if ( gp.daughter(iDau) == &(handle->at(k)) ) gpDau_index = k;
	      
	    }// for(size_t k = 0; k < handle->size(); ++k) {
	    daughters_tmp.push_back( gpDau_index );

	  }// for(size_t iDau = 0; iDau < gp.numberOfDaughters(); iDau++){
	  daughters[ic].push_back( daughters_tmp );
	  
	  // Print debugging info?
	  if (cfg_debugMode){
	    std::cout << std::setw(5) << gp_index
		      << std::setw(width) << gp.pt()                << std::setw(width) << gp.eta()   << std::setw(width) << gp.phi()  << std::setw(width) << gp.energy()
		      << std::setw(width) << gp.status()            << std::setw(width) << gp.pdgId() << std::setw(width) << gp.numberOfMothers()  
		      << std::setw(width) << gp.numberOfDaughters() << std::setw(width) << gp.mass()  << std::setw(width) << gp.charge()
		      << std::setw(width) << gp.vx()                << std::setw(width) << gp.vy()    << std::setw(width) << gp.vz() << std::endl;
	  }
  
        }//for(size_t i = 0; i < handle->size(); ++i) {
      }// if (inputCollections[ic].getUntrackedParameter<bool>("saveAllGenParticles", false)) {

      // MC electrons
      if (inputCollections[ic].getUntrackedParameter<bool>("saveGenElectrons", false)) saveLeptons(handle, electrons[ic], 11);

      // MC muons
      if (inputCollections[ic].getUntrackedParameter<bool>("saveGenMuons", false)) saveLeptons(handle, muons[ic], 13);

      // MC taus
      if (inputCollections[ic].getUntrackedParameter<bool>("saveGenTaus", false)) {
        tauAssociatedWithHiggs[ic] = -1;
        std::vector<const reco::Candidate*> tauLeptons = GenParticleTools::findParticles(handle, 15);
        size_t tauIndex = 0;
        for (auto& p: tauLeptons) {
          // 4-momentum of tau lepton
          taus[ic].add(p->pt(), p->eta(), p->phi(), p->energy());
          // tau offspring information
          std::vector<const reco::Candidate*> offspring = GenParticleTools::findOffspring(handle, p);
          short nCharged = 0;
          short nPi0 = 0;
          bool decaysToElectron = false;
          bool decaysToMuon = false;
          math::XYZTLorentzVector neutrinoMomentum;
          for (auto&po: offspring) {
            int absPid = std::abs(po->pdgId());
            if (absPid == 11) { // Electron
              ++nCharged;
              decaysToElectron = true;
            } else if (absPid == 13) { // Muon
              ++nCharged;
              decaysToMuon = true;
            } else if (absPid == 111) { // Pi0
              ++nPi0;
            } else if (absPid == 211 || absPid == 321) { // Pi+, K+
              ++nCharged;
            } else if (absPid == 12 || absPid == 14 || absPid == 16) { // neutrino
              neutrinoMomentum += po->p4();
            }
          }

          // Visible tau
          math::XYZTLorentzVector visibleTau = p->p4() - neutrinoMomentum;
          visibleTaus[ic].add(visibleTau.pt(), visibleTau.eta(), visibleTau.phi(), visibleTau.energy());

          // Other offspring information
          tauNcharged[ic].push_back(nCharged);
          tauNPi0[ic].push_back(nPi0);
          tauDecaysToElectron[ic].push_back(decaysToElectron);
          tauDecaysToMuon[ic].push_back(decaysToMuon);
          tauNeutrinos[ic].add(neutrinoMomentum.pt(), neutrinoMomentum.eta(), neutrinoMomentum.phi(), neutrinoMomentum.energy());

          // rtau and spineffects
          saveHelicityInformation(visibleTau, offspring, ic);

          // tau ancestry information
          std::vector<const reco::Candidate*> ancestry = GenParticleTools::findAncestry(handle, p);
          int tauOriginCode = kTauOriginUnknown;
          for (auto& p: ancestry) {
            int absPid = std::abs(p->pdgId());
            if (absPid == kFromZ || absPid == kFromW) {
              tauOriginCode = absPid;
            } else if (absPid == kFromHiggs) {
              tauOriginCode = absPid;
              tauAssociatedWithHiggs[ic] = tauIndex;
            }
          }
          if (tauOriginCode == kTauOriginUnknown && ancestry.size() > 0) {
            tauOriginCode = kFromOtherSource;
          }
          tauMother[ic].push_back(tauOriginCode);
          ++tauIndex;
        }
      }

      // Neutrinos
      if (inputCollections[ic].getUntrackedParameter<bool>("saveGenNeutrinos", false)) {
        saveLeptons(handle, neutrinos[ic], 12);
        saveLeptons(handle, neutrinos[ic], 14);
        saveLeptons(handle, neutrinos[ic], 16);
      }
      
    }// if(handle.isValid()){
  }// for(size_t i = 0; i < inputCollections.size(); ++-i){

  return filter();
}


bool GenParticleDumper::filter(){
  if(!useFilter) return true;
  return true;
}


void GenParticleDumper::reset(){
  if(booked){
    for(size_t ic = 0; ic < inputCollections.size(); ++ic){
      if (inputCollections[ic].getUntrackedParameter<bool>("saveAllGenParticles", false)) {

	// Four-vector variables
        pt[ic] .clear();
        eta[ic].clear();
        phi[ic].clear();
        e[ic]  .clear();
	// Other essential variables
        pdgId[ic]    .clear();
	mass[ic]     .clear();
	vertexX[ic]  .clear();
	vertexY[ic]  .clear();
	vertexZ[ic]  .clear();
	charge[ic]   .clear();
	status[ic]   .clear();
        mothers[ic]  .clear();
        daughters[ic].clear();
      }// if (inputCollections[ic].getUntrackedParameter<bool>("saveAllGenParticles", false)) {

      if (inputCollections[ic].getUntrackedParameter<bool>("saveGenNeutrinos", false)) neutrinos[ic].reset();
      if (inputCollections[ic].getUntrackedParameter<bool>("saveGenElectrons", false)) electrons[ic].reset();
      if (inputCollections[ic].getUntrackedParameter<bool>("saveGenMuons", false)) muons[ic].reset();
      if (inputCollections[ic].getUntrackedParameter<bool>("saveGenTaus", false)) {
        taus[ic].reset();
        visibleTaus[ic].reset();
        tauNcharged[ic].clear();
        tauNPi0[ic].clear();
        tauRtau[ic].clear();
        tauMother[ic].clear();
        tauDecaysToElectron[ic].clear();
        tauDecaysToMuon[ic].clear();
        tauSpinEffects[ic].clear();
        tauNeutrinos[ic].reset();
      }// if (inputCollections[ic].getUntrackedParameter<bool>("saveGenTaus", false)) {

    } // for(size_t ic = 0; ic < inputCollections.size(); ++ic){
  } // if(booked){
  
  return;
}


void GenParticleDumper::saveLeptons(edm::Handle<reco::GenParticleCollection>& handle, FourVectorDumper& dumper, int pID) {
  std::vector<const reco::Candidate*> matches = GenParticleTools::findParticles(handle, pID);
  for (auto& p: matches) {
    dumper.add(p->pt(), p->eta(), p->phi(), p->energy());
  }

  return;
}


void GenParticleDumper::saveHelicityInformation(math::XYZTLorentzVector& visibleTau, const std::vector<const reco::Candidate*>& offspring, const size_t index) {
  // Find leading ch. particle
  math::XYZTLorentzVector ldgPion;
  for (auto& p: offspring) {
    if (std::abs(p->pdgId()) == 211) {
      if (p->p4().P() > ldgPion.P()) {
        ldgPion = p->p4();
      }
    }
  }
  // Save rtau
  double rtau = -1;
  if (visibleTau.P() > 0.0) {
    rtau = ldgPion.P() / visibleTau.P();
  }
  tauRtau[index].push_back(rtau);
  // Save spin effects info
  TLorentzVector ldgPionBoosted(ldgPion.px(), ldgPion.py(), ldgPion.pz(), ldgPion.energy());
  TLorentzVector visibleTauForBoost(visibleTau.px(), visibleTau.py(), visibleTau.pz(), visibleTau.energy());
  ldgPionBoosted.Boost(-1.0 * visibleTauForBoost.BoostVector());
  tauSpinEffects[index].push_back(ldgPionBoosted.E() / 1.778 / 2.0);
  
  return;
}
 

void GenParticleDumper::printDescendants(edm::Handle<reco::GenParticleCollection>& handle, const reco::Candidate* p) {
  std::vector<const reco::Candidate*> offspring = GenParticleTools::findOffspring(handle, p);
  std::cout << "Offspring for pid=" << p->pdgId() << std::endl;
  for (auto& p: offspring) {
    std::cout << "  " << p->pdgId() << std::endl;
  }

  return;
}
