#include "UCYHiggsAnalysis/MiniAOD2FlatTree/interface/EventInfoDumper.h"

#include "SimDataFormats/PileupSummaryInfo/interface/PileupSummaryInfo.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "FWCore/Framework/interface/ConsumesCollector.h"


EventInfoDumper::EventInfoDumper(edm::ConsumesCollector&& iConsumesCollector, const edm::ParameterSet& pset)
  : puSummaryToken(iConsumesCollector.consumes<std::vector<PileupSummaryInfo>>(pset.getParameter<edm::InputTag>("PileupSummaryInfoSrc"))),
    lheToken(iConsumesCollector.consumes<LHEEventProduct>(pset.getUntrackedParameter<edm::InputTag>("LHESrc", edm::InputTag("")))),
    vertexToken(iConsumesCollector.consumes<edm::View<reco::Vertex>>(pset.getParameter<edm::InputTag>("OfflinePrimaryVertexSrc"))),
    topPtToken(iConsumesCollector.consumes<double>(pset.getParameter<edm::InputTag>("TopPtProducer")))
{

  // Other auxiliary variables
  width = 11;

  // Input parameters/flags
  cfg_debugMode  = pset.getUntrackedParameter<bool>("debugMode");
  cfg_branchName = pset.getUntrackedParameter<std::string>("branchName","");
}


EventInfoDumper::~EventInfoDumper(){}


void EventInfoDumper::book(TTree* tree){

  // Setup the TTree
  tree->Branch( (cfg_branchName + "_event"                    ).c_str(), &event               );
  tree->Branch( (cfg_branchName + "_run"                      ).c_str(), &run                 );     
  tree->Branch( (cfg_branchName + "_lumi"                     ).c_str(), &lumi                );
  tree->Branch( (cfg_branchName + "_prescale"                 ).c_str(), &prescale            );
  tree->Branch( (cfg_branchName + "_nPUvertices"              ).c_str(), &nPU                 );
  tree->Branch( (cfg_branchName + "_NUP"                      ).c_str(), &NUP                 );
  tree->Branch( (cfg_branchName + "_nGoodOfflineVertices"     ).c_str(), &nGoodOfflinePV      );
  tree->Branch( (cfg_branchName + "_pvX"                      ).c_str(), &pvX                 );
  tree->Branch( (cfg_branchName + "_pvY"                      ).c_str(), &pvY                 );
  tree->Branch( (cfg_branchName + "_pvZ"                      ).c_str(), &pvZ                 );
  tree->Branch( (cfg_branchName + "_pvDistanceToNextVertex"   ).c_str(), &distanceToNextPV    );
  tree->Branch( (cfg_branchName + "_pvDistanceToClosestVertex").c_str(), &distanceToClosestPV );
  tree->Branch( (cfg_branchName + "_topPtWeight"              ).c_str(), &topPtWeight         );
  // tree->Branch( (cfg_branchName + "_pvPtSumRatioToNext"       ).c_str(), &ptSumRatio          );
  
  return;
}


bool EventInfoDumper::fill(edm::Event& iEvent, const edm::EventSetup& iSetup){

  event    = iEvent.id().event();
  run      = iEvent.run();
  lumi     = iEvent.luminosityBlock();
  prescale = 1.0;
  nPU      = -1;
  NUP      = -1;
  
  // Get the PU collection
  edm::Handle<std::vector<PileupSummaryInfo> > hpileup;
  iEvent.getByToken(puSummaryToken, hpileup);

  // Print debugging info?                                                                                                                                                         
  if (cfg_debugMode){
    std::cout << "\n" << std::setw(width*8) << cfg_branchName << std::endl;
    std::cout << std::string(width*16, '=') << std::endl;
    std::cout << std::setw(5)       << "Event"
	      << std::setw(width)   << "Run"             << std::setw(width)   << "Lumi"                 << std::setw(width) << "nPU"  << std::setw(width) << "nPartons"
	      << std::setw(width)   << "nGoodPV"         << std::setw(width)   << "pvX"                  << std::setw(width) << "pvY"  << std::setw(width) << "pvZ"
	      << std::setw(width*2) << "distaneToNextPV" << std::setw(width*2) << "distanceToClosestPV"  << std::setw(width) << "ptSum0" 
	      << std::setw(width)   << "ptSum1"  	 << std::setw(width)   << "ptSumRatio"
	      << std::endl;
    std::cout << std::string(width*16, '=') << std::endl;
  }

  // Sanity check (protection for data)
  if(hpileup.isValid()) {

    // For-loop: All Primary vertices [https://cmssdt.cern.ch/SDT/doxygen/CMSSW_7_5_2/doc/html/d9/d53/classPileupSummaryInfo.html]
    for(std::vector<PileupSummaryInfo>::const_iterator iPV = hpileup->begin(); iPV != hpileup->end(); ++iPV) {
      if(iPV->getBunchCrossing() == 0) {
	nPU = iPV->getTrueNumInteractions();
	break;
      }
    }
  }

  // Number of jets for combining W+Jets/Z+jets inclusive with exclusive
  edm::Handle<LHEEventProduct> lheHandle;
  iEvent.getByToken(lheToken, lheHandle);
  if (lheHandle.isValid()) {
    // Store NUP = number of partons
    NUP = lheHandle->hepeup().NUP;
  }

  // PV
  nGoodOfflinePV      = -1;
  pvX                 = 0.0;
  pvY                 = 0.0;
  pvZ                 = 0.0;
  ptSumRatio          = -1.0;
  distanceToNextPV    = -1.0;
  distanceToClosestPV = -1.0;

  double ptSum0 = 0.0;
  double ptSum1 = 0.0;
      
  // Get a handle to the Vertex collection [https://cmssdt.cern.ch/SDT/doxygen/CMSSW_7_5_2/doc/html/da/d95/classreco_1_1Vertex.html]
  edm::Handle<edm::View<reco::Vertex> > hoffvertex;
  if(iEvent.getByToken(vertexToken, hoffvertex)){

    // Get the number of offline Primary Vertices (PV)
    nGoodOfflinePV = hoffvertex->size();

    // Multiply by 10 to get mm
    pvX = hoffvertex->at(0).x()*10.0;
    pvY = hoffvertex->at(0).y()*10.0;
    pvZ = hoffvertex->at(0).z()*10.0;

    // If more than 1 good offline PV: Look how often one misses the hard PV because of PU
    if (nGoodOfflinePV > 1) {
      distanceToNextPV = std::fabs(hoffvertex->at(0).z() - hoffvertex->at(1).z());

      // For-loop: All offline PVs
      for (size_t i = 1; i < hoffvertex->size(); ++i) {
	
	// Calculate distance of PV to closest nearby vertex
	float delta = std::fabs(hoffvertex->at(0).z() - hoffvertex->at(i).z());
	if (delta < distanceToClosestPV || distanceToClosestPV < 0.0) distanceToClosestPV = delta;
	
      }// for (size_t i = 1; i < hoffvertex->size(); ++i) {


      // For-loop: All tracks associated to PV (sumPt sorted). 
      // NOTE: Tracks are NOT saved in miniAOD [https://twiki.cern.ch/twiki/bin/view/CMSPublic/WorkBookMiniAOD2015#Primary_vertices_and_BeamSpot]
      std::vector<reco::TrackBaseRef>::const_iterator tracks_pv0;
      for (tracks_pv0 = hoffvertex->at(0).tracks_begin(); tracks_pv0 != hoffvertex->at(0).tracks_end(); tracks_pv0++) {
	
	// Calculate sum of track pT^2 over all tracks associated with this vertex
	ptSum0 += hoffvertex->at(0).trackWeight(*tracks_pv0) * (*tracks_pv0)->pt() * (*tracks_pv0)->pt();
	// std::cout << "sumPt0 =  " << hoffvertex->at(0).trackWeight(*tracks_pv0) << " * " <<  (*tracks_pv0)->pt()*(*tracks_pv0)->pt() << " = " << ptSum1 << std::endl;
      }


      // For-loop: All tracks associated to second-in-rank PV (sumPt sorted)
      std::vector<reco::TrackBaseRef>::const_iterator tracks_pv1;
      for (tracks_pv1 = hoffvertex->at(1).tracks_begin(); tracks_pv1 != hoffvertex->at(1).tracks_end(); tracks_pv1++) {

	// Calculate sum of track pT^2 over all tracks associated with this vertex
	ptSum1 += hoffvertex->at(1).trackWeight(*tracks_pv1) * (*tracks_pv1)->pt() * (*tracks_pv1)->pt();
	//std::cout << "sumPt1 =  " << hoffvertex->at(1).trackWeight(*tracks_pv1) << " * " <<  (*tracks_pv1)->pt() * (*tracks_pv1)->pt() << " = " << ptSum1 << std::endl;
      }

      // Calculate the ratio of the ptSum of the PV to that of the second-in-rank PV
      if (ptSum0 > 0.0) ptSumRatio = ptSum1 / ptSum0;
      
    }// if (nGoodOfflinePV > 1) {

    // Multiply by 10 to get mm
    distanceToNextPV    *= 10.0;
    distanceToClosestPV *= 10.0;


  // Print debugging info?                                                                                                                                                         
  if (cfg_debugMode){
    std::cout << std::setw(5)       << event
	      << std::setw(width)   << run               << std::setw(width)   << lumi                 << std::setw(width) << nPU  << std::setw(width) << NUP
	      << std::setw(width)   << nGoodOfflinePV    << std::setw(width)   << pvX                  << std::setw(width) << pvY  << std::setw(width) << pvZ
	      << std::setw(width*2) << distanceToNextPV  << std::setw(width*2) << distanceToClosestPV  << std::setw(width) << ptSum0
	      << std::setw(width)   << ptSum1            << std::setw(width)   << ptSumRatio
	      << std::endl;
  }


  }// if(iEvent.getByToken(vertexToken, hoffvertex)){


  // Top pt                                                                                                                                                                        
  topPtWeight = 1.0;
  edm::Handle<double> topPtHandle;
  if (iEvent.getByToken(topPtToken, topPtHandle)) {
    topPtWeight = *(topPtHandle.product());
  }

  return filter();
}


bool EventInfoDumper::filter(){
  return true;
}


void EventInfoDumper::reset(){
  return;
}
