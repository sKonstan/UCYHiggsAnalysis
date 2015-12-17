#include "UCYHiggsAnalysis/MiniAOD2FlatTree/interface/TauDumper.h"
#include "UCYHiggsAnalysis/MiniAOD2FlatTree/interface/NtupleAnalysis_fwd.h"
#include "UCYHiggsAnalysis/MiniAOD2FlatTree/interface/GenParticleTools.h"

#include "DataFormats/JetReco/interface/Jet.h"

TauDumper::TauDumper(edm::ConsumesCollector&& iConsumesCollector, std::vector<edm::ParameterSet>& psets)
  : genParticleToken(iConsumesCollector.consumes<reco::GenParticleCollection>(edm::InputTag("prunedGenParticles"))) {
  inputCollections = psets;
  booked           = false;

  // Four-vector variables
  pt    = new std::vector<double>[inputCollections.size()];
  eta   = new std::vector<double>[inputCollections.size()];    
  phi   = new std::vector<double>[inputCollections.size()];    
  e     = new std::vector<double>[inputCollections.size()];    

  // Other essential variables
  pdgId           = new std::vector<int>[inputCollections.size()];
  nDiscriminators = inputCollections[0].getParameter<std::vector<std::string> >("discriminators").size();
  discriminators  = new std::vector<bool>[inputCollections.size()*nDiscriminators];
  lChTrackPt      = new std::vector<double>[inputCollections.size()];
  lChTrackEta     = new std::vector<double>[inputCollections.size()];
  lNeutrTrackPt   = new std::vector<double>[inputCollections.size()];
  lNeutrTrackEta  = new std::vector<double>[inputCollections.size()];
  decayMode       = new std::vector<short>[inputCollections.size()];
  ipxy            = new std::vector<float>[inputCollections.size()];
  ipxySignif      = new std::vector<float>[inputCollections.size()];
  nProngs         = new std::vector<short>[inputCollections.size()];
  pdgTauOrigin    = new std::vector<short>[inputCollections.size()];
  MCNProngs       = new std::vector<short>[inputCollections.size()];
  MCNPiZeros      = new std::vector<short>[inputCollections.size()];
  MCtau           = new FourVectorDumper[inputCollections.size()];
  matchingJet     = new FourVectorDumper[inputCollections.size()];
    
  // Systematics variations for tau 4-vector
  systTESup          = new FourVectorDumper[inputCollections.size()];
  systTESdown        = new FourVectorDumper[inputCollections.size()];
  systExtremeTESup   = new FourVectorDumper[inputCollections.size()];
  systExtremeTESdown = new FourVectorDumper[inputCollections.size()];
    
  // Tokens
  tauToken = new edm::EDGetTokenT<edm::View<pat::Tau> >[inputCollections.size()];
  jetToken = new edm::EDGetTokenT<edm::View<pat::Jet> >[inputCollections.size()];

  // Other auxiliary variables
  width          = 10;
  cfg_debugMode  = false;
  cfg_branchName = "";
    
  // For-loop: All input collecitons
  for(size_t i = 0; i < inputCollections.size(); ++i){
    edm::InputTag inputtag = inputCollections[i].getParameter<edm::InputTag>("src");
    tauToken[i]            = iConsumesCollector.consumes<edm::View<pat::Tau>>(inputtag);
    edm::InputTag jettag   = inputCollections[i].getParameter<edm::InputTag>("jetSrc");
    jetToken[i]            = iConsumesCollector.consumes<edm::View<pat::Jet>>(jettag);
  }

  useFilter = false;
  // For-loop: All input collections
  for(size_t i = 0; i < inputCollections.size(); ++i){
    bool param = inputCollections[i].getUntrackedParameter<bool>("filter",false);
    if(param) useFilter = true;
  }
}


TauDumper::~TauDumper(){}

void TauDumper::book(TTree* tree){
  booked = true;

  // For-loop: All input collections
  for(size_t i = 0; i < inputCollections.size(); ++i){

    // Input parameters/flags
    cfg_debugMode  = inputCollections[i].getUntrackedParameter<bool>("debugMode");
    cfg_branchName = inputCollections[i].getUntrackedParameter<std::string>("branchName","");
    if( cfg_branchName.length() == 0) cfg_branchName = inputCollections[i].getParameter<edm::InputTag>("src").label();

    // Four-vector variables
    tree->Branch( (cfg_branchName + "_pt") .c_str(), &pt[i]  );
    tree->Branch( (cfg_branchName + "_eta").c_str(), &eta[i] );
    tree->Branch( (cfg_branchName + "_phi").c_str(), &phi[i] );
    tree->Branch( (cfg_branchName + "_e")  .c_str(), &e[i]   );

    // Other essential variables 
    tree->Branch( ( cfg_branchName + "_pdgId")       .c_str(), &pdgId[i]          );
    tree->Branch( ( cfg_branchName + "_pdgOrigin")   .c_str(), &pdgTauOrigin[i]   );
    tree->Branch( ( cfg_branchName + "_mcNProngs")   .c_str(), &MCNProngs[i]      );
    tree->Branch( ( cfg_branchName + "_mcNPizero")   .c_str(), &MCNPiZeros[i]     );
    tree->Branch( ( cfg_branchName + "_lChTrkPt")    .c_str(), &lChTrackPt[i]     );
    tree->Branch( ( cfg_branchName + "_lChTrkEta")   .c_str(), &lChTrackEta[i]    );
    tree->Branch( ( cfg_branchName + "_lNeutrTrkPt") .c_str(), &lNeutrTrackPt[i]  );
    tree->Branch( ( cfg_branchName + "_lNeutrTrkEta").c_str(), &lNeutrTrackEta[i] );
    tree->Branch( ( cfg_branchName + "_decay")       .c_str(), &decayMode[i]      );
    tree->Branch( ( cfg_branchName + "_IPxy")        .c_str(), &ipxy[i]           );
    tree->Branch( ( cfg_branchName + "_IPxySignif")  .c_str(), &ipxySignif[i]     );
    tree->Branch( ( cfg_branchName + "_nProngs")     .c_str(), &nProngs[i]        );

    MCtau[i]      .book(tree, cfg_branchName, "MCVisibleTau");
    matchingJet[i].book(tree, cfg_branchName, "matchingJet");

    // For-loop: All discriminators [https://twiki.cern.ch/twiki/bin/view/CMSPublic/SWGuidePFTauID]
    std::vector<std::string> discriminatorNames = inputCollections[i].getParameter<std::vector<std::string> >("discriminators");
    for(size_t iDiscr = 0; iDiscr < discriminatorNames.size(); ++iDiscr) {
      tree->Branch( ( cfg_branchName + "_"+discriminatorNames[iDiscr]).c_str(),&discriminators[inputCollections.size()*iDiscr+i]);
    }

    // Systematics variations for tau 4-vector 	
    systTESup[i]         .book(tree, cfg_branchName, "TESup");
    systTESdown[i]       .book(tree, cfg_branchName, "TESdown");
    systExtremeTESup[i]  .book(tree, cfg_branchName, "TESextremeUp");
    systExtremeTESdown[i].book(tree, cfg_branchName, "TESextremeDown");
  }
 
  return;
}


bool TauDumper::fill(edm::Event& iEvent, const edm::EventSetup& iSetup){
  if (!booked) return true;

  // Create edm handle and get the GenParticleCollection (only if not real data)  
  edm::Handle <reco::GenParticleCollection> genParticlesHandle;
  if (!iEvent.isRealData()) iEvent.getByToken(genParticleToken, genParticlesHandle);

  // For-loop: All input collections
  for(size_t ic = 0; ic < inputCollections.size(); ++ic){

    // Create edm handle and get the pat::Tau collection 
    edm::Handle<edm::View<pat::Tau>> tauHandle;
    iEvent.getByToken(tauToken[ic], tauHandle);

    // Create edm handle and get the pat::Jet collection 
    edm::Handle<edm::View<pat::Jet>> jetHandle;
    iEvent.getByToken(jetToken[ic], jetHandle);

    // Print debugging info?
    if (cfg_debugMode){
      std::cout << "\n" << std::setw(width*8) << cfg_branchName << std::endl;
      std::cout << std::string(width*17, '=') << std::endl;
      std::cout << std::setw(5)       << "Index"
                << std::setw(width)   << "Pt"             << std::setw(width)   << "Eta"  << std::setw(width)   << "Phi"      << std::setw(width) << "E"
		<< std::setw(width)   << "decayMode"      << std::setw(width*2) << "dxy"  << std::setw(width*2) << "dxy_sig"  << std::setw(width) << "nProngs"
                << std::setw(width*2) << "deltaR"         << std::setw(width)   << "Pt"   << std::setw(width)   << "Eta"      << std::setw(width) << "Phi"
                << std::setw(width)   << "E"
                << std::endl;
      std::cout << std::string(width*17, '=') << std::endl;
    }

    // Sanity check
    if(tauHandle.isValid()){

      std::vector<std::string> discriminatorNames = inputCollections[ic].getParameter<std::vector<std::string> >("discriminators");
      double TESvariation        = inputCollections[ic].getUntrackedParameter<double>("TESvariation");
      double TESvariationExtreme = inputCollections[ic].getUntrackedParameter<double>("TESvariationExtreme");
    
      // For-loop: All taus
      for(size_t i=0; i<tauHandle->size(); ++i) {
	
	// Get the pat::Tau
        const pat::Tau& tau = tauHandle->at(i);

	// Four-vector variables
        pt[ic] .push_back( tau.p4().pt()     );
        eta[ic].push_back( tau.p4().eta()    );
        phi[ic].push_back( tau.p4().phi()    );
        e[ic]  .push_back( tau.p4().energy() );
        
        // Leading charged particle
        if(tau.leadChargedHadrCand().isNonnull()){
          lChTrackPt[ic] .push_back( tau.leadChargedHadrCand()->p4().Pt()  );
          lChTrackEta[ic].push_back( tau.leadChargedHadrCand()->p4().Eta() );
        } else {
          lChTrackPt[ic].push_back(-1.0);
          lChTrackEta[ic].push_back(-10.0);
        }

        // Leading neutral particle
        if (tau.leadNeutralCand().isNonnull()) {
          lNeutrTrackPt[ic] .push_back( tau.leadNeutralCand()->p4().Pt()  );
          lNeutrTrackEta[ic].push_back( tau.leadNeutralCand()->p4().Eta() );
        } else {
          lNeutrTrackPt[ic] .push_back(-1.0);
          lNeutrTrackEta[ic].push_back(-10.0);
        }
      
	// Other essential variables1 [https://cmssdt.cern.ch/SDT/doxygen/CMSSW_7_5_2/doc/html/d1/de9/classpat_1_1Tau.html]
        decayMode[ic] .push_back( tau.decayMode() ); //See "hadronicDecayMode" [https://cmssdt.cern.ch/SDT/doxygen/CMSSW_5_3_14/doc/html/dd/d63/classreco_1_1PFTau.html]
        ipxy[ic]      .push_back( tau.dxy()       );
        ipxySignif[ic].push_back( tau.dxy_Sig()   );
        nProngs[ic]   .push_back( tau.signalChargedHadrCands().size() );

	// For-loop: All discriminators
        for(size_t iDiscr = 0; iDiscr < discriminatorNames.size(); ++iDiscr) {
          discriminators[inputCollections.size()*iDiscr+ic].push_back(tau.tauID(discriminatorNames[iDiscr]));
        }

        // Systematics variations
        if (!iEvent.isRealData()) {
          systTESup[ic]         .add( tau.p4().pt()*(1.0+TESvariation)       , tau.p4().eta(), tau.p4().phi(), tau.p4().energy()*(1.0+TESvariation)        );
          systTESdown[ic]       .add( tau.p4().pt()*(1.0-TESvariation)       , tau.p4().eta(), tau.p4().phi(), tau.p4().energy()*(1.0-TESvariation)        );
          systExtremeTESup[ic]  .add( tau.p4().pt()*(1.0+TESvariationExtreme), tau.p4().eta(), tau.p4().phi(), tau.p4().energy()*(1.0+TESvariationExtreme) );
          systExtremeTESdown[ic].add( tau.p4().pt()*(1.0-TESvariationExtreme), tau.p4().eta(), tau.p4().phi(), tau.p4().energy()*(1.0-TESvariationExtreme) );
        }

	// Print debugging info?
        if(cfg_debugMode){
	  std::cout << std::setw(5)     << i
                    << std::setw(width) << tau.p4().pt()    << std::setw(width)   << tau.p4().eta() << std::setw(width)   << tau.p4().phi() << std::setw(width) << tau.p4().energy()
		    << std::setw(width) << tau.decayMode()  << std::setw(width*2) << tau.dxy()      << std::setw(width*2) << tau.dxy_Sig()  
		    << std::setw(width) << tau.signalChargedHadrCands().size();
	}

        
	// Find MC particle matching to the tau. Logic is done in the following order:
	// - e   is true if DeltaR(reco_tau, MC_e)  < 0.1
	// - mu  is true if DeltaR(reco_tau, MC_mu) < 0.1
	// - tau is true if DeltaR(reco_tau, MC_mu) < 0.1
	// - jet flavour should be taken from the flavour of the jet matching to the tau
	// The assignment is done in the following order:
	// - If e is true and tau is true   -> pdgId = +-1511
	// - If e is true and tau is false  -> pdgId = +-11
	// - If mu is true and tau is true  -> pdgId = +-1513
	// - If mu is true and tau is false -> pdgId = +-13
	// - If tau is true                 -> pdgId = +-15
	// - else                           -> pdgId = 0

	// MC match info
	if (!iEvent.isRealData()) fillMCMatchInfo(ic, genParticlesHandle, tau);

	// Find matching jet
	reco::Candidate::LorentzVector p4BestJet(0,0,0,0);
	double myMinDeltaR = 999.0;
	int jetPdgId = 0;

	// For-loop: All Jets
	for(size_t iJet = 0; iJet < jetHandle->size(); ++iJet) {
	  
	  // Get the pat::Jet
	  const pat::Jet& jet = jetHandle->at(iJet);
	  
	  // Calculate delta-R of pat::Jet from pat:Tau
	  double DR = deltaR(tau.p4(), jet.p4());
	  if (DR < 0.2 && DR < myMinDeltaR) {
	    p4BestJet = jet.p4();
	    myMinDeltaR = DR;
	    jetPdgId = abs(jet.partonFlavour());
	  }
	}// for(size_t iJet = 0; iJet < jetHandle->size(); ++iJet) {

	// Add the best match
	matchingJet[ic].add(p4BestJet.pt(), p4BestJet.eta(), p4BestJet.phi(), p4BestJet.energy());

	// If tau does not match to e/mu/tau; then store as tau pdgId the partonFlavour of the matching jet 
	if (!iEvent.isRealData()) 
	  {
	    if (pdgId[ic][pdgId[ic].size()-1] == -1) pdgId[ic][pdgId[ic].size()-1] = jetPdgId;
	  }
	
      }// if(tauHandle.isValid()){
    }// for(size_t i=0; i<tauHandle->size(); ++i) {
  }// for(size_t ic = 0; ic < inputCollections.size(); ++ic){
  
  return filter();
}


void TauDumper::fillMCMatchInfo(size_t ic, edm::Handle<reco::GenParticleCollection>& genParticles, const pat::Tau& tau) {
  int tauPid              = 0;
  int tauOrigin           = 0;
  bool matchesToTau       = false;
  bool matchesToE         = false;
  bool matchesToMu        = false;
  double deltaRBestTau    = 9999.0;
  short simulatedNProngs  = 0;
  short simulatedNPizeros = 0;
  reco::Candidate::LorentzVector p4BestTau(0,0,0,0);

  // Sanity check
  if(genParticles.isValid()){

    // For-loop: All genParticles
    for (size_t iMC=0; iMC < genParticles->size(); ++iMC) {

      // Get the genPArticle
      const reco::Candidate & gp = (*genParticles)[iMC];

      // Skip if not an electron, muon or tau
      if( abs(gp.pdgId()) != 11 && abs(gp.pdgId()) != 13 && abs(gp.pdgId()) != 15) continue;

      // Get the 4-momentum
      reco::Candidate::LorentzVector p4 = gp.p4();

      // electron
      if (abs(gp.pdgId()) == 11) {
        if (deltaR(p4,tau.p4()) < 0.1) {
          matchesToE = true;
          p4BestTau = p4;
          ++simulatedNProngs;
        }
      } //muon
      else if (abs(gp.pdgId()) == 13) {
        if (deltaR(p4,tau.p4()) < 0.1) {
          matchesToMu = true;
          p4BestTau = p4;
          ++simulatedNProngs;
        }
      }//tau 
      else if (abs(gp.pdgId()) == 15) {
	
	// Get the offspring (see local "GenParticleTools.cc")
        std::vector<const reco::Candidate*> offspring = GenParticleTools::findOffspring(genParticles, &(genParticles->at(iMC)));
        
	// Calculate visible tau pt
        reco::Candidate::LorentzVector neutrinoMomentum(0., 0., 0., 0.);
        for (auto& po: offspring) {
          int absPid = std::abs(po->pdgId());
	  // Neutrinos
          if (absPid == 12 || absPid == 14 || absPid == 16) neutrinoMomentum += po->p4();
        }

	// Subtract the neutrino 4-momentum
        p4 -= neutrinoMomentum;

        // Do deltaR matching
        double DR = deltaR(p4,tau.p4());
        if (DR < 0.1 && DR < deltaRBestTau) {

          // Matches to visible tau
          deltaRBestTau = DR;
          p4BestTau     = p4;
          matchesToTau  = true;

          // Calculate prongs and pizeros
          for (auto& po: offspring) {
            int absPid = std::abs(po->pdgId());
            if (absPid == 111) ++simulatedNPizeros;
            if (absPid == 211 || absPid == 321) ++simulatedNProngs;
          }

          // Find out which particle produces the tau
          std::vector<const reco::Candidate*> ancestry = GenParticleTools::findAncestry(genParticles, &(genParticles->at(iMC)));
          for (auto& pa: ancestry) {
            int absPid = std::abs(pa->pdgId());
            if (absPid == kFromZ || absPid == kFromW || absPid == kFromHiggs) tauOrigin = absPid;
          }
	  
          if (tauOrigin == 0 && ancestry.size() > 0) tauOrigin = kFromOtherSource;
        }// if (DR < 0.1 && DR < deltaRBestTau) {
      }// else if (abs(gp.pdgId()) == 15) {
    }// for (size_t iMC=0; iMC < genParticles->size(); ++iMC) {
  }// if(genParticles.isValid()){

  if (matchesToE) {
    if (matchesToTau)
      tauPid = kTauDecaysToElectron;
    else
      tauPid = kElectronToTau;
  } else if (matchesToMu) {
    if (matchesToTau)
      tauPid = kTauDecaysToMuon;
    else
      tauPid = kMuonToTau;
  } else if (matchesToTau) {
    tauPid = kTauDecaysToHadrons;
  } else {
    // Reference jet is a reco::PFJet and therefore not included into miniAOD
    // Need to do actual matching in ntuple reader
    tauPid = -1;
  }

  // Print debugging info?
  if (cfg_debugMode){
    std::cout << std::setw(width*2) << deltaRBestTau
              << std::setw(width)   << p4BestTau.pt()     << std::setw(width) << p4BestTau.eta() << std::setw(width) << p4BestTau.phi()
              << std::setw(width)   << p4BestTau.energy() << std::endl;
  }

  // Save variables
  pdgId[ic]       .push_back(tauPid);
  pdgTauOrigin[ic].push_back(tauOrigin);
  MCNProngs[ic]   .push_back(simulatedNProngs);
  MCNPiZeros[ic]  .push_back(simulatedNPizeros);


  // Add the best match
  MCtau[ic].add(p4BestTau.pt(), p4BestTau.eta(), p4BestTau.phi(), p4BestTau.energy());
  
  return;
}


bool TauDumper::filter(){
  if(!useFilter) return true;

  int n = 0;
  // For-loop: All input collections
  for(size_t ic = 0; ic < inputCollections.size(); ++ic){
    for(std::vector<double>::const_iterator i = pt[ic].begin(); i!= pt[ic].end(); ++i){
      if(*i > 20) n++;
    }

  }// for(size_t ic = 0; ic < inputCollections.size(); ++ic){

  return n > 0;
}


void TauDumper::reset(){
  if(booked){

    // For-loop: All input collections
    for(size_t ic = 0; ic < inputCollections.size(); ++ic){

      // Four-vector variables
      pt[ic] .clear();
      eta[ic].clear();
      phi[ic].clear();
      e[ic]  .clear();

      // Other essential variables
      lChTrackPt[ic]    .clear();
      lChTrackEta[ic]   .clear();  
      lNeutrTrackPt[ic] .clear();
      lNeutrTrackEta[ic].clear();  
      decayMode[ic]     .clear();
      ipxy[ic]          .clear();
      ipxySignif[ic]    .clear();
      nProngs[ic]       .clear();
      pdgId[ic]         .clear();
      pdgTauOrigin[ic]  .clear();
      MCNProngs[ic]     .clear();
      MCNPiZeros[ic]    .clear();

      MCtau[ic]      .reset();
      matchingJet[ic].reset();

      // Other essential variables 
      systTESup[ic]         .reset();
      systTESdown[ic]       .reset();
      systExtremeTESup[ic]  .reset();
      systExtremeTESdown[ic].reset();
    }

    // For-loop: All input collections 
    for(size_t ic = 0; ic < inputCollections.size()*nDiscriminators; ++ic){
      discriminators[ic].clear();
    }
  }

  return;
}
