/** \class PUInfo
 * 
 * 
 *  Analyzer for dumping the MC PU distribution
 *  in a separate root file before skimming
 * 
 *  \original author Sami Lehti  -  HIP Helsinki
 *  \editor Alexandros Attikis   -  UCY
 *
 */

// user include files  
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "FWCore/Framework/interface/ConsumesCollector.h"
#include "SimDataFormats/PileupSummaryInfo/interface/PileupSummaryInfo.h"
#include "SimDataFormats/GeneratorProducts/interface/GenEventInfoProduct.h"

#include "TFile.h"
#include "TH1F.h"

#include <iostream>
#include <vector>
 
class PUInfo : public edm::EDAnalyzer {
public:
  PUInfo(const edm::ParameterSet&);
  ~PUInfo();

  void beginJob();
  void analyze( const edm::Event&, const edm::EventSetup&);
  void endJob();

private:
  edm::EDGetTokenT<std::vector<PileupSummaryInfo> > puSummaryToken;
  edm::EDGetTokenT<GenEventInfoProduct> eventInfoToken;
  std::string cfg_outputFileName;
  bool cfg_debugMode;
  int width = 16;
  TH1F* hPU;
};

PUInfo::PUInfo(const edm::ParameterSet& iConfig) :
  puSummaryToken(consumes<std::vector<PileupSummaryInfo>>(iConfig.getParameter<edm::InputTag>("PileupSummaryInfoSrc"))),
  eventInfoToken(consumes<GenEventInfoProduct>(edm::InputTag("generator"))),
  cfg_outputFileName(iConfig.getParameter<std::string>("OutputFileName")),
  cfg_debugMode(iConfig.getUntrackedParameter<bool>("debugMode"))
{
  
  // Book histograms
  hPU = new TH1F("pileup", "pileup", 50, 0.0, 50.0);

}


PUInfo::~PUInfo() {}


void PUInfo::beginJob(){}


void PUInfo::analyze( const edm::Event& iEvent, const edm::EventSetup& iSetup){
  if (iEvent.isRealData()) return;
  
  // Create an event info handle
  edm::Handle<GenEventInfoProduct> genEventInfoHandle;
  iEvent.getByToken(eventInfoToken, genEventInfoHandle);

  double w = 1.0;
  // Sanity chck
  if (genEventInfoHandle.isValid()) {

    if (genEventInfoHandle->weight() < 0.0) w = -1.0;

  }

  // Create a PU summary info hadle 
  edm::Handle<std::vector<PileupSummaryInfo> > hpileup;
  iEvent.getByToken(puSummaryToken, hpileup);

  // Print debugging info?
  if (cfg_debugMode){
    std::cout << "\n" << std::string(width*6, '=')  << std::endl;
    std::cout << std::setw(5)     << "Index"         << std::setw(width) << "Bunch Crossing"    << std::setw(width) << "Bunch Spacing"
      // << std::setw(width) << "Inst Lumi"     << std::setw(width) << "NTrks (high pT)"   << std::setw(width) << "NTrks (low pT)"
      // << std::setw(width) << "# Interactions"<< std::setw(width) << "sum pT (high pT)"  << std::setw(width) << "sum pT (low pT)"
      // << std::setw(width) << "z Positions"   << std::setw(width) << "True # Interactions"
	      << std::setw(width) << "# Interactions"<< std::setw(width+6) << "# Interactions (True)"
              << std::endl;
    std::cout << std::string(width*6, '=') << std::endl;
  }
  
  // Sanity check
  if(hpileup.isValid()) {
    short nPU   = 0;
    short index = 0;
        
  
    // For-loop: All Vertices [https://cmssdt.cern.ch/SDT/doxygen/CMSSW_7_5_2/doc/html/d9/d53/classPileupSummaryInfo.html]
    for(std::vector<PileupSummaryInfo>::const_iterator iPV = hpileup->begin(); iPV != hpileup->end(); ++iPV, ++index) {

      if (cfg_debugMode){
	std::cout << std::setw(5)     << index                         << std::setw(width) << iPV->getBunchCrossing()    << std::setw(width) << iPV->getBunchSpacing()
	  // << std::setw(width) << iPV->getPU_instLumi().at(0)   << std::setw(width) << iPV->getPU_ntrks_highpT().at(0) << std::setw(width) << iPV->getPU_ntrks_lowpT().at(0)
	  // << std::setw(width) << iPV->getPU_NumInteractions()  << std::setw(width) << iPV->getPU_sumpT_highpT().at(0) << std::setw(width) << iPV->getPU_sumpT_lowpT().at(0)
	  // << std::setw(width) << iPV->getPU_zpositions().at(0) << std::setw(width) << iPV->getTrueNumInteractions()
		  << std::setw(width) << iPV->getPU_NumInteractions()  << std::setw(width) << iPV->getTrueNumInteractions()
		  << std::endl;
      }
      
      if(iPV->getBunchCrossing() == 0) {
	nPU = iPV->getTrueNumInteractions();
	break;
      }
      
    }

    // Fill histogram
    hPU->Fill(nPU, w);
  }

  return;
}


void PUInfo::endJob(){

  // Open, Write & Close output files
  if(hPU->GetEntries() > 0){

    TFile* fOUT = TFile::Open( cfg_outputFileName.c_str(), "RECREATE");
    fOUT->cd();
    hPU->Write();
    fOUT->Close();
  }

  return;
}

DEFINE_FWK_MODULE(PUInfo);
