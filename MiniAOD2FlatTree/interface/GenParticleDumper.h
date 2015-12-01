#ifndef GenParticleDumper_h
#define GenParticleDumper_h

#include "FWCore/Framework/interface/EDFilter.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "DataFormats/Common/interface/View.h"
#include "DataFormats/Common/interface/Ptr.h"

#include <string>
#include <vector>

#include "TTree.h"

#include "DataFormats/Math/interface/LorentzVector.h"

#include "UCYHiggsAnalysis/MiniAOD2FlatTree/interface/BaseDumper.h"
#include "UCYHiggsAnalysis/MiniAOD2FlatTree/interface/FourVectorDumper.h"

class GenParticleDumper : public BaseDumper {
public:
  GenParticleDumper(edm::ConsumesCollector&& iConsumesCollector, std::vector<edm::ParameterSet>& psets);
  ~GenParticleDumper();

  void book(TTree*);
  bool fill(edm::Event&, const edm::EventSetup&);
  void reset();
   
private:
  bool filter();
  void saveLeptons(edm::Handle<reco::GenParticleCollection>& handle, FourVectorDumper& dumper, int pID);
  void saveHelicityInformation(math::XYZTLorentzVector& visibleTau, const std::vector<const reco::Candidate*>& offspring, const size_t index);
  void printDescendants(edm::Handle<reco::GenParticleCollection>& handle, const reco::Candidate* p);
  
private:  
  //edm::Handle<reco::GenParticleCollection> *handle;
  edm::EDGetTokenT<reco::GenParticleCollection> *token;
  
  // Input parameters/flags
  bool   cfg_debugMode;
  std::string cfg_branchName;

  // General particle list
  std::vector<double> *mass;
  std::vector<double> *vertexX;
  std::vector<double> *vertexY;
  std::vector<double> *vertexZ;
  std::vector<short>  *charge;
  std::vector<short>  *status;
  std::vector< std::vector<unsigned short> > *mothers;
  std::vector< std::vector<unsigned short> > *daughters;

  // MC electrons
  FourVectorDumper *electrons;
  
  // MC muons
  FourVectorDumper *muons;
  
  // MC taus
  FourVectorDumper *taus;
  FourVectorDumper *visibleTaus;
  std::vector<short> *tauNcharged;
  std::vector<short> *tauNPi0;
  std::vector<double> *tauRtau;
  short *tauAssociatedWithHiggs;
  std::vector<short> *tauMother;
  std::vector<bool> *tauDecaysToElectron;
  std::vector<bool> *tauDecaysToMuon;
  std::vector<double> *tauSpinEffects;
  FourVectorDumper *tauNeutrinos;
  
  // Neutrinos
  FourVectorDumper *neutrinos;

  // Other auxiliary variables
  int width;

};
#endif
