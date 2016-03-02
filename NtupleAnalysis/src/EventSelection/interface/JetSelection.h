// -*- c++ -*-
#ifndef EventSelection_JetSelection_h
#define EventSelection_JetSelection_h

#include "EventSelection/interface/BaseSelection.h"
#include "DataFormat/interface/Jet.h"
#include "EventSelection//interface/TauSelection.h"
#include "Framework/interface/EventCounter.h"
#include "Tools/interface/DirectionalCut.h"
#include <boost/concept_check.hpp>

#include <string>
#include <vector>

class ParameterSet;
class CommonPlots;
class Event;
class EventCounter;
class HistoWrapper;
class WrappedTH1;
class WrappedTH2;

class JetSelection: public BaseSelection {
public:
  
  // Class to encapsulate the access to the data members of
  // TauSelection. If you want to add a new accessor, add it here
  // and keep all the data of TauSelection private.

  class Data {
  public:
    // The reason for pointer instead of reference is that const
    // reference allows temporaries, while const pointer does not.
    // Here the object pointed-to must live longer than this object.
    Data();
    ~Data();

    bool passedSelection() const { return bPassedSelection; }
    int getNumberOfSelectedJets() const { return fSelectedJets.size(); }
    const std::vector<Jet>& getSelectedJets() const { return fSelectedJets; }
    const std::vector<Jet>& getAllJets() const { return fAllJets; }
    bool jetMatchedToTauFound() const { return (fJetMatchedToTau.size() > 0); }
    const Jet& getJetMatchedToTau() const;
    const double HT() const { return fHT; }

    friend class JetSelection;

  private:
    bool bPassedSelection;
    std::vector<Jet> fAllJets; // All jets (needed for MET)
    std::vector<Jet> fSelectedJets;
    std::vector<Jet> fJetMatchedToTau;
    double fHT; // HT (scalar sum of jets)
  };
  
  /// Constructor with/without histogrammi
  explicit JetSelection(const ParameterSet& config, EventCounter& eventCounter, HistoWrapper& histoWrapper, CommonPlots* commonPlots, const std::string& postfix = "");
  explicit JetSelection(const ParameterSet& config);
  virtual ~JetSelection();

  virtual void bookHistograms(TDirectory* dir);
  
  /// Use silentAnalyze() if you do not want to fill histograms or increment counters. Otherwise use analyze()    
  Data silentAnalyze(const Event& event, const Tau& tau);
  Data silentAnalyzeWithoutTau(const Event& event);
  Data analyze(const Event& event, const Tau& tau);
  Data analyzeWithoutTau(const Event& event);

private:
  /// Initialisation called from constructor
  void initialize(const ParameterSet& config);
  /// The actual selection
  Data privateAnalyze(const Event& event, const math::LorentzVectorT<double>& tauP, const double tauPt);
  void findJetMatchingToTau(std::vector<Jet>& collection, const Event& event, const math::LorentzVectorT<double>& tauP);
  
  // Input parameters
  const float cfg_PtCut;
  const float cfg_EtaCut;
  const float cfg_TauMatchDeltaR;
  const DirectionalCut<int> cfg_NJetsCut;
  
  // Event counter for passing selection
  Count cPassedJetSelection;
  // Event sub-counters for passing selection
  Count cSubAll;
  Count cSubPassedJetID;
  Count cSubPassedJetPUID;
  Count cSubPassedMatchWithTau;
  Count cSubPassedPt;
  Count cSubPassedEta;
  Count cSubPassedJetCount;

  // Histograms
  WrappedTH1 *hJetPtAll;
  WrappedTH1 *hJetEtaAll;
  WrappedTH1 *hJetPtPassed;
  WrappedTH1 *hJetEtaPassed;
  std::vector<WrappedTH1*> hSelectedJetPt;
  std::vector<WrappedTH1*> hSelectedJetEta;
  WrappedTH1 *hJetMatchingToTauDeltaR;
  WrappedTH1 *hJetMatchingToTauPtRatio;
};

#endif
