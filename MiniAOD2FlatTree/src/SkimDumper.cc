#include "UCYHiggsAnalysis/MiniAOD2FlatTree/interface/SkimDumper.h"

SkimDumper::SkimDumper(edm::ConsumesCollector&& iConsumesCollector, const edm::ParameterSet& pset){
    inputCollection = pset;
    booked = false;
    std::vector<edm::InputTag> tags = inputCollection.getParameter<std::vector<edm::InputTag> >("Counters");
    
    token = new edm::EDGetTokenT<edm::MergeableCounter>[tags.size()];
    for(size_t i = 0; i < tags.size(); ++i) {
      // Use edm::InLumi in consumes template to signal that the counters are read from lumiblock instead of event
      token[i] = iConsumesCollector.consumes<edm::MergeableCounter, edm::InLumi>(tags[i]);
    }
}


SkimDumper::~SkimDumper(){}


void SkimDumper::book(){
    booked = true;
    std::vector<edm::InputTag> tags = inputCollection.getParameter<std::vector<edm::InputTag> >("Counters");
    hCounter = new TH1F("SkimCounter","",tags.size(),0,tags.size());

    // For-loop: All skim counters
    for(size_t i = 0; i < tags.size(); ++i){
	hCounter->GetXaxis()->SetBinLabel(i+1,tags[i].label().c_str());
    }

    return;
}


#include "DataFormats/Common/interface/MergeableCounter.h"
bool SkimDumper::fill(const edm::LuminosityBlock& iLumi, const edm::EventSetup& iSetup){
    if (!booked) return true;

    std::vector<edm::InputTag> tags = inputCollection.getParameter<std::vector<edm::InputTag> >("Counters");
    
    // For-loop: All skim counters
    for(size_t i = 0; i < tags.size(); ++i){
      
      // std::cout << "check tags["<<i<<"] = " << tags[i].label() << std::endl;
      edm::Handle<edm::MergeableCounter> count;
      
      // One Luminosity block is a time interval whose length is equal to 2^18 orbits (~23,3 seconds)
      // The Luminosity block counter is reset at the beginning of each run. The average amount of pileup interactions (num of PVs) 
      // decreases exponentially with time (or lumi block number) due to the loss of protons in the beam. 
      iLumi.getByToken(token[i], count);
      
      // Sanity check
      if( count.isValid() ){
	hCounter->Fill(i,count->value);
	// std::cout << "check count-value = " << count->value << std::endl;
      }

    }// for(size_t i = 0; i < tags.size(); ++i){
    return true;
}


void SkimDumper::reset(){
    if(booked){
    }

    return;
}


TH1F* SkimDumper::getCounter(){
    return hCounter;
}
