#include "UCYHiggsAnalysis/MiniAOD2FlatTree/interface/FourVectorDumper.h"

FourVectorDumper::FourVectorDumper()
: booked(false) { }

FourVectorDumper::~FourVectorDumper() { }

void FourVectorDumper::book(TTree* tree, const std::string& branchName, const std::string& postfix) {
  booked = true;
  std::string modPostfix = "";
  if (!postfix.empty()) modPostfix = postfix;

  // Four-vector variables
  tree->Branch( (branchName + "_pt_"  + modPostfix).c_str(), &pt  );
  tree->Branch( (branchName + "_eta_" + modPostfix).c_str(), &eta );
  tree->Branch( (branchName + "_phi_" + modPostfix).c_str(), &phi );
  tree->Branch( (branchName + "_e_"   + modPostfix).c_str(), &e   );

  return;
}


bool FourVectorDumper::fill(edm::Event& iEvent, const edm::EventSetup& iSetup){
  if(booked) return filter();
  return true;
}


bool FourVectorDumper::filter(){
  return true;
}


void FourVectorDumper::add(const double _pt, const double _eta, const double _phi, const double _e) {
  
  // Four-vector variables 
  pt .push_back( _pt  );
  eta.push_back( _eta );
  phi.push_back( _phi );
  e  .push_back( _e   );

  return;
}

void FourVectorDumper::reset(){
  if(booked){
    
    // Four-vector variables
    pt .clear();
    eta.clear();
    phi.clear();
    e  .clear();
  }

  return;
}
