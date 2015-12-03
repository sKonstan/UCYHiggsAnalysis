#include "UCYHiggsAnalysis/MiniAOD2FlatTree/interface/JetDumper.h"
#include "CondFormats/JetMETObjects/interface/JetCorrectorParameters.h"
#include "JetMETCorrections/Objects/interface/JetCorrectionsRecord.h"
#include "FWCore/Framework/interface/ESHandle.h"
#include "FWCore/Framework/interface/EventSetup.h"

#include "DataFormats/JetReco/interface/PileupJetIdentifier.h"
#include "UCYHiggsAnalysis/MiniAOD2FlatTree/interface/NtupleAnalysis_fwd.h"

JetDumper::JetDumper(edm::ConsumesCollector&& iConsumesCollector, std::vector<edm::ParameterSet>& psets){
  inputCollections = psets;
  booked           = false;

  // Four-vector variables
  pt  = new std::vector<double>[inputCollections.size()];
  eta = new std::vector<double>[inputCollections.size()];    
  phi = new std::vector<double>[inputCollections.size()];    
  e   = new std::vector<double>[inputCollections.size()];    

  // Other essential variables
  pdgId         = new std::vector<short>[inputCollections.size()];
  hadronFlavour = new std::vector<int>[inputCollections.size()];
  partonFlavour = new std::vector<int>[inputCollections.size()];

  nDiscriminators = inputCollections[0].getParameter<std::vector<std::string> >("discriminators").size();
  discriminators  = new std::vector<float>[inputCollections.size()*nDiscriminators];
  nUserfloats     = inputCollections[0].getParameter<std::vector<std::string> >("userFloats").size();
  userfloats      = new std::vector<double>[inputCollections.size()*nUserfloats];
  jetToken        = new edm::EDGetTokenT<edm::View<pat::Jet> >[inputCollections.size()];

  // Other auxiliary variables
  width          = 12;
  cfg_debugMode  = false;
  cfg_branchName = "";

  // For-loop: All input collections
  for(size_t i = 0; i < inputCollections.size(); ++i){
    edm::InputTag inputtag = inputCollections[i].getParameter<edm::InputTag>("src");
    jetToken[i] = iConsumesCollector.consumes<edm::View<pat::Jet>>(inputtag);
  }
    
  useFilter = false;
  // For-loop: All input collections
  for(size_t i = 0; i < inputCollections.size(); ++i){
    bool param = inputCollections[i].getUntrackedParameter<bool>("filter",false);
    if(param) useFilter = true;
  }

  jetIDloose           = new std::vector<bool>[inputCollections.size()];
  jetIDtight           = new std::vector<bool>[inputCollections.size()];
  jetIDtightLeptonVeto = new std::vector<bool>[inputCollections.size()];
  jetPUIDloose         = new std::vector<bool>[inputCollections.size()];
  jetPUIDmedium        = new std::vector<bool>[inputCollections.size()];
  jetPUIDtight         = new std::vector<bool>[inputCollections.size()];

  isBasicJet = new std::vector<bool>[inputCollections.size()];
  isCaloJet  = new std::vector<bool>[inputCollections.size()];
  isJPTJet   = new std::vector<bool>[inputCollections.size()];
  isPFJet    = new std::vector<bool>[inputCollections.size()];

  neutralHadronEnergyFraction = new std::vector<double>[inputCollections.size()];
  neutralEmEnergyFraction     = new std::vector<double>[inputCollections.size()];
  nConstituents               = new std::vector<short>[inputCollections.size()];
  chargedHadronMultiplicity   = new std::vector<short>[inputCollections.size()];

  MCjet = new FourVectorDumper[inputCollections.size()];

  // Systematics variations for tau 4-vector
  systJESup   = new FourVectorDumper[inputCollections.size()];
  systJESdown = new FourVectorDumper[inputCollections.size()];
  systJERup   = new FourVectorDumper[inputCollections.size()];
  systJERdown = new FourVectorDumper[inputCollections.size()];

}


JetDumper::~JetDumper(){}


void JetDumper::book(TTree* tree){
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
    tree->Branch( (cfg_branchName + "_pdgId")        .c_str(), &pdgId[i]         );
    tree->Branch( (cfg_branchName + "_hadronFlavour").c_str(), &hadronFlavour[i] );
    tree->Branch( (cfg_branchName + "_partonFlavour").c_str(), &partonFlavour[i] );

    std::vector<std::string> discriminatorNames = inputCollections[i].getParameter<std::vector<std::string> >("discriminators");
    // For-loop: All discriminators
    for(size_t iDiscr = 0; iDiscr < discriminatorNames.size(); ++iDiscr) {
      tree->Branch( (cfg_branchName+"_"+discriminatorNames[iDiscr]).c_str(), &discriminators[inputCollections.size()*iDiscr+i]);
    }

    std::vector<std::string> userfloatNames = inputCollections[i].getParameter<std::vector<std::string> >("userFloats");
    // For-loop: All user foloat names (e.g. "pileupJetId:fullDiscriminant")
    for(size_t iDiscr = 0; iDiscr < userfloatNames.size(); ++iDiscr) {
      std::string branch_name = userfloatNames[iDiscr];
      size_t pos_semicolon    = branch_name.find(":");
      branch_name             = branch_name.erase(pos_semicolon,1);
      tree->Branch( (cfg_branchName+"_" + branch_name).c_str(), &userfloats[inputCollections.size()*iDiscr+i]);
    }

    tree->Branch( ( cfg_branchName + "_IDloose")          .c_str(), &jetIDloose[i]           );
    tree->Branch( ( cfg_branchName + "_IDtight")          .c_str(), &jetIDtight[i]           );
    tree->Branch( ( cfg_branchName + "_IDtightLeptonVeto").c_str(), &jetIDtightLeptonVeto[i] );
    tree->Branch( ( cfg_branchName + "_PUIDloose")        .c_str(), &jetPUIDloose[i]         );
    tree->Branch( ( cfg_branchName + "_PUIDmedium")       .c_str(), &jetPUIDmedium[i]        );
    tree->Branch( ( cfg_branchName + "_PUIDtight")        .c_str(), &jetPUIDtight[i]         );

    tree->Branch( ( cfg_branchName + "_isBasicJet").c_str(), &isBasicJet[i] );
    tree->Branch( ( cfg_branchName + "_isCaloJet") .c_str(), &isCaloJet[i]  );
    tree->Branch( ( cfg_branchName + "_isJPTJet")  .c_str(), &isJPTJet[i]   );
    tree->Branch( ( cfg_branchName + "_isPFJet")   .c_str(), &isPFJet[i]    );

    tree->Branch( ( cfg_branchName + "_neutralHadronEnergyFraction").c_str(), &neutralHadronEnergyFraction[i] );
    tree->Branch( ( cfg_branchName + "_neutralEmEnergyFraction")    .c_str(), &neutralEmEnergyFraction[i]     );
    tree->Branch( ( cfg_branchName + "_nConstituents ")             .c_str(), &nConstituents[i]               );
    tree->Branch( ( cfg_branchName + "_chargedHadronMultiplicity")  .c_str(), &chargedHadronMultiplicity[i]   );
    
    MCjet[i].book(tree, cfg_branchName, "MCjet");

    // Systematics variations for tau 4-vector    
    systJESup[i]  .book(tree, cfg_branchName, "JESup"  );
    systJESdown[i].book(tree, cfg_branchName, "JESdown");
    systJERup[i]  .book(tree, cfg_branchName, "JERup"  );
    systJERdown[i].book(tree, cfg_branchName, "JERdown");

  }// for(size_t i = 0; i < inputCollections.size(); ++i){

  return;
}


bool JetDumper::fill(edm::Event& iEvent, const edm::EventSetup& iSetup){
  if (!booked) return true;

  // Jet Energy Corrections?
  if (!fJECUncertainty.size()) {

    // For-loop: All input collections
    for(size_t i = 0; i < inputCollections.size(); ++i) {
      edm::ESHandle<JetCorrectorParametersCollection> JetCorParColl;
      iSetup.get<JetCorrectionsRecord>().get(inputCollections[i].getParameter<std::string>("jecPayload"),JetCorParColl);
      bool found = true;
      try {
	JetCorrectorParameters const & JetCorPar = (*JetCorParColl)["Uncertainty"];
      } catch(cms::Exception e) {
	std::cout << "Warning: cannot find cell 'Uncertainty' in JEC uncertainty table; JEC uncertainty forced to 0" << std::endl;
	found = false;
      }
      if (found) {
	JetCorrectorParameters const & JetCorPar = (*JetCorParColl)["Uncertainty"];
	fJECUncertainty.push_back(new JetCorrectionUncertainty(JetCorPar));
      } else {
	fJECUncertainty.push_back(nullptr);
      }
    
    }// for(size_t i = 0; i < inputCollections.size(); ++i) {
  }// if (!fJECUncertainty.size()) {

  // For-loop: All input collections
  for(size_t ic = 0; ic < inputCollections.size(); ++ic){

    std::vector<std::string> discriminatorNames = inputCollections[ic].getParameter<std::vector<std::string> >("discriminators");
    std::vector<std::string> userfloatNames     = inputCollections[ic].getParameter<std::vector<std::string> >("userFloats");
	
    edm::Handle<edm::View<pat::Jet>> jetHandle;
    iEvent.getByToken(jetToken[ic], jetHandle);

    // Input parameters/flags
    cfg_debugMode  = inputCollections[ic].getUntrackedParameter<bool>("debugMode");
    cfg_branchName = inputCollections[ic].getUntrackedParameter<std::string>("branchName","");

    // Print debugging info?
    if (cfg_debugMode){
      std::cout << std::setw(width*6) << cfg_branchName << std::endl;
      std::cout << std::string(width*14, '=') << std::endl;
      std::cout << std::setw(5)     << "Index"
		<< std::setw(width) << "Pt"          << std::setw(width)   << "Eta"           << std::setw(width)   << "Phi"           << std::setw(width) << "Energy"
		<< std::setw(width) << "genParton "  << std::setw(width+4) << "hadronFlavour" << std::setw(width+4) << "partonFlavour" 
		<< std::setw(width) << "IDLoose"     << std::setw(width)   << "IDTight"       << std::setw(width+4) << "IDTightLepVeto" << std::setw(width+4) << "nConstituents"
		<< std::setw(width) << "nProngs"
		<< std::endl;
      std::cout << std::string(width*14, '=') << std::endl;
    }

    // Sanity Check
    if(jetHandle.isValid()){

      // For-loop: All jets
      for(size_t i=0; i<jetHandle->size(); ++i) {

	// Get the pat::Jet
	const pat::Jet& obj = jetHandle->at(i);

	// Four-vector variables 
	pt[ic] .push_back( obj.p4().pt()     );
	eta[ic].push_back( obj.p4().eta()    );
	phi[ic].push_back( obj.p4().phi()    );
	e[ic]  .push_back( obj.p4().energy() );
	
	// For-loop: All discriminators
	for(size_t iDiscr = 0; iDiscr < discriminatorNames.size(); ++iDiscr) {
	  // std::cout << inputCollections[ic].getUntrackedParameter<std::string>("branchname","") << " / " << discriminatorNames[iDiscr] << std::endl;
	  discriminators[inputCollections.size()*iDiscr+ic].push_back(obj.bDiscriminator(discriminatorNames[iDiscr]));
	}

	// For-looP All user floats
	for(size_t iDiscr = 0; iDiscr < userfloatNames.size(); ++iDiscr) {
	  //std::cout << inputCollections[ic].getUntrackedParameter<std::string>("branchname","") << " / " << userfloatNames[iDiscr] << std::endl;
	  userfloats[inputCollections.size()*iDiscr+ic].push_back(obj.userFloat(userfloatNames[iDiscr]));
	}

	// For MC matching
     	int genParton = 0;
	if(obj.genParton()) genParton = obj.genParton()->pdgId();

	pdgId[ic]        .push_back( genParton );
	hadronFlavour[ic].push_back( obj.hadronFlavour() );
	partonFlavour[ic].push_back( obj.partonFlavour() );

	// Jet ID
	jetIDloose[ic]          .push_back( passJetID(kJetIDLoose, obj)        );
	jetIDtight[ic]          .push_back( passJetID(kJetIDTight, obj)        );
	jetIDtightLeptonVeto[ic].push_back( passJetID(kJetIDTightLepVeto, obj) );
	isBasicJet[ic]          .push_back( obj.isBasicJet() );
	isCaloJet[ic]           .push_back( obj.isCaloJet()  );
	isJPTJet[ic]            .push_back( obj.isJPTJet()   );
	isPFJet[ic]             .push_back( obj.isPFJet()    );

	neutralHadronEnergyFraction[ic].push_back( obj.neutralHadronEnergyFraction() );
	neutralEmEnergyFraction[ic]    .push_back( obj.neutralEmEnergyFraction()     );
	nConstituents[ic]              .push_back( obj.nConstituents()               );
	chargedHadronMultiplicity[ic]  .push_back( obj.chargedHadronMultiplicity()   );

	// Print debugging info?
         if (cfg_debugMode){
	   std::cout << std::setw(5)       << i
                     << std::setw(width)   << obj.pt()              << std::setw(width) << obj.eta()                   << std::setw(width)   << obj.phi()
                     << std::setw(width)   << obj.energy()          << std::setw(width) << genParton                   << std::setw(width+4) << obj.hadronFlavour()
                     << std::setw(width+4) << obj.partonFlavour()   << std::setw(width) << passJetID(kJetIDLoose, obj) << std::setw(width)   << passJetID(kJetIDTight, obj)
		     << std::setw(width+4) << passJetID(kJetIDTightLepVeto, obj) 
		     << std::setw(width+4) << obj.nConstituents()  
		     << std::setw(width)   << obj.chargedHadronMultiplicity() 
                     << std::endl;
         }


	// Jet PU ID [https://twiki.cern.ch/twiki/bin/view/CMS/PileupJetID]
	double PUID = 0;
	if(obj.hasUserData("pileupJetId:fullDiscriminant")) PUID = obj.userFloat("pileupJetId:fullDiscriminant");
	int puIDflag = static_cast<int>(PUID);
	jetPUIDloose[ic] .push_back(PileupJetIdentifier::passJetId(puIDflag, PileupJetIdentifier::kLoose)  );
	jetPUIDmedium[ic].push_back(PileupJetIdentifier::passJetId(puIDflag, PileupJetIdentifier::kMedium) );
	jetPUIDtight[ic] .push_back(PileupJetIdentifier::passJetId(puIDflag, PileupJetIdentifier::kTight)  );
                
	// GenJet
	if (obj.genJet() != nullptr) MCjet[ic].add(obj.genJet()->pt(), obj.genJet()->eta(), obj.genJet()->phi(), obj.genJet()->energy());
	else MCjet[ic].add(0.0, 0.0, 0.0, 0.0);
                
	// Systematics
	if (!iEvent.isRealData()) {
	  // JES
	  double uncUp = 0.0;
	  double uncDown = 0.0;
	  if (fJECUncertainty[ic] != nullptr) {
	    fJECUncertainty[ic]->setJetEta(obj.eta());
	    fJECUncertainty[ic]->setJetPt(obj.pt()); // here you must use the CORRECTED jet pt
	    uncUp = fJECUncertainty[ic]->getUncertainty(true);
	  }
	  systJESup[ic].add(obj.p4().pt()*(1.0+uncUp),
			    obj.p4().eta(),
			    obj.p4().phi(),
			    obj.p4().energy()*(1.0+uncUp));
	  if (fJECUncertainty[ic] != nullptr) {
	    // Yes, one needs to set pt and eta again
	    fJECUncertainty[ic]->setJetEta(obj.eta());
	    fJECUncertainty[ic]->setJetPt(obj.pt()); // here you must use the CORRECTED jet pt
	    uncDown = fJECUncertainty[ic]->getUncertainty(false);
	  }
	  systJESdown[ic].add(obj.p4().pt()*(1.0-uncDown),
			      obj.p4().eta(),
			      obj.p4().phi(),
			      obj.p4().energy()*(1.0-uncDown));
	  // JER
                  
	}// if (!iEvent.isRealData()) {

      }// for(size_t i=0; i<jetHandle->size(); ++i) {
    }// if(jetHandle.isValid()){
  }// for(size_t ic = 0; ic < inputCollections.size(); ++ic){

  return filter();
}


void JetDumper::reset(){

  //For-loop: All input collections
  for(size_t ic = 0; ic < inputCollections.size(); ++ic){

    // Four-vector variables
    pt[ic] .clear();
    eta[ic].clear();
    phi[ic].clear();
    e[ic]  .clear();

    // Other essential variables
    pdgId[ic]        .clear();
    hadronFlavour[ic].clear();
    partonFlavour[ic].clear();
    jetIDloose[ic]   .clear();
    jetIDtight[ic]   .clear();
    jetIDtightLeptonVeto[ic].clear();
    jetPUIDloose[ic] .clear();
    jetPUIDmedium[ic].clear();
    jetPUIDtight[ic] .clear();
    isBasicJet[ic]   .clear();
    isCaloJet[ic]    .clear();
    isJPTJet[ic]     .clear();
    isPFJet[ic]      .clear();
    neutralHadronEnergyFraction[ic].clear();
    neutralEmEnergyFraction[ic]    .clear();
    nConstituents[ic]              .clear();
    chargedHadronMultiplicity[ic]  .clear();


    MCjet[ic].reset();

    // Systematics
    systJESup[ic]  .reset();
    systJESdown[ic].reset();
    systJERup[ic]  .reset();
    systJERdown[ic].reset();
  }

  //For-loop: All discriminators
  for(size_t ic = 0; ic < inputCollections.size()*nDiscriminators; ++ic){
    discriminators[ic].clear();
  }

  //For-loop: All discriminators*userFloats
  for(size_t ic = 0; ic < inputCollections.size()*nUserfloats; ++ic){
    userfloats[ic].clear();
  }
}


bool JetDumper::passJetID(int id, const pat::Jet& jet) {
  
  // Recipy taken from https://twiki.cern.ch/twiki/bin/view/CMS/JetID (read on 14.08.2015)
  double eta = fabs(jet.eta());

  if (eta < 3.0) {
    // PF Jet ID       Loose   Tight   TightLepVeto
    // Neutral Hadron Fraction < 0.99  < 0.90  < 0.90
    // Neutral EM Fraction     < 0.99  < 0.90  < 0.90
    // Number of Constituents  > 1     > 1     > 1
    // Muon Fraction           -       -       < 0.8
    int nConstituents = jet.chargedMultiplicity() + jet.electronMultiplicity() + jet.muonMultiplicity() + jet.neutralMultiplicity();

    if (id == kJetIDLoose) {
      if (!(jet.neutralHadronEnergyFraction() < 0.99)) return false;
      if (!(jet.neutralEmEnergyFraction()     < 0.99)) return false;
      if (!(nConstituents                     > 1   )) return false;
    } else if (id == kJetIDTight) {
      if (!(jet.neutralHadronEnergyFraction() < 0.90)) return false;
      if (!(jet.neutralEmEnergyFraction()     < 0.90)) return false;
      if (!(nConstituents                     > 1   )) return false;      
    } else if (id == kJetIDTightLepVeto) {
      if (!(jet.neutralHadronEnergyFraction() < 0.90)) return false;
      if (!(jet.neutralEmEnergyFraction()     < 0.90)) return false;
      if (!(nConstituents                     > 1   )) return false;      
      if (!(jet.muonEnergyFraction()          < 0.80)) return false;
    }// if (eta < 3.0) {

    if (eta < 2.4) {
      // And for -2.4 <= eta <= 2.4 in addition apply
      // Charged Hadron Fraction > 0     > 0     > 0
      // Charged Multiplicity    > 0     > 0     > 0
      // Charged EM Fraction     < 0.99  < 0.99  < 0.90
      if (id == kJetIDLoose) {
        if (!(jet.chargedHadronEnergyFraction() > 0.0 )) return false;
        if (!(jet.chargedHadronMultiplicity()   > 0   )) return false;
        if (!(jet.chargedEmEnergyFraction()     < 0.99)) return false;
      } else if (id == kJetIDTight) {
        if (!(jet.chargedHadronEnergyFraction() > 0.0 )) return false;
        if (!(jet.chargedHadronMultiplicity()   > 0   )) return false;
        if (!(jet.chargedEmEnergyFraction()     < 0.99)) return false;        
      } else if (id == kJetIDTightLepVeto) {
        if (!(jet.chargedHadronEnergyFraction() > 0.0 )) return false;
        if (!(jet.chargedHadronMultiplicity()   > 0   )) return false;
        if (!(jet.chargedEmEnergyFraction()     < 0.90)) return false;
      }
    }// if (eta < 2.4) {
  } else {
    //     PF Jet ID                   Loose   Tight
    //     Neutral EM Fraction         < 0.90  < 0.90
    //     Number of Neutral Particles > 10    >10 
    if (id == kJetIDLoose) {
      if (!(jet.neutralEmEnergyFraction() < 0.90)) return false;
      if (!(jet.neutralMultiplicity()     > 10  )) return false;    
    } else if (id == kJetIDTight) {
      if (!(jet.neutralEmEnergyFraction() < 0.90)) return false;
      if (!(jet.neutralMultiplicity()     > 10  )) return false;    
    }
  }

  return true;
}
