// -*- c++ -*-
#ifndef EventSelection_BJetSelection_h
#define EventSelection_BJetSelection_h

#include "EventSelection/interface/BaseSelection.h"
#include "EventSelection/interface/JetSelection.h"
#include "Framework/interface/EventCounter.h"
#include "Tools/interface/DirectionalCut.h"

#include <string>
#include <vector>

class ParameterSet;
class CommonPlots;
class Event;
class EventCounter;
class HistoWrapper;
class WrappedTH1;
class WrappedTH2;

class BJetSelection: public BaseSelection {
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
    int getNumberOfSelectedBJets() const { return fSelectedBJets.size(); }
    const std::vector<Jet>& getSelectedBJets() const { return fSelectedBJets; }
    const double getBTaggingScaleFactorEventWeight() const { return fBTaggingScaleFactorEventWeight; }
    const double getBTaggingPassProbability() const { return fBTaggingPassProbability; } /// Obtain probability for passing - tagging (without applying the selection)
    
    friend class BJetSelection;

  private:
    bool bPassedSelection;
    double fBTaggingScaleFactorEventWeight;
    double fBTaggingPassProbability;
    std::vector<Jet> fSelectedBJets;

  };
  
  // Main class
  explicit BJetSelection(const ParameterSet& config, EventCounter& eventCounter, HistoWrapper& histoWrapper, CommonPlots* commonPlots, const std::string& postfix = "");
  explicit BJetSelection(const ParameterSet& config);
  virtual ~BJetSelection();

  virtual void bookHistograms(TDirectory* dir);
  
  /// Use silentAnalyze() if you do not want to fill histograms or increment counters. Otherwise use analyze()  
  Data silentAnalyze(const Event& event, const JetSelection::Data& jetData);
  Data analyze(const Event& event, const JetSelection::Data& jetData);

private:
  /// Initialisation called from constructor
  void initialize(const ParameterSet& config);
  /// The actual event selection
  Data privateAnalyze(const Event& iEvent, const JetSelection::Data& jetData);
  double calculateBTagPassingProbability(const Event& iEvent, const JetSelection::Data& jetData);

  // Input parameters
  const DirectionalCut<int> cfg_NJetsCut;
  float fDisriminatorValue; // not a const because constructor sets it based on input string
  
  // Event counter for passing selection
  Count cPassedBJetSelection;
  // Event sub-counters for passing selection  
  Count cSubAll;
  Count cSubPassedDiscriminator;
  Count cSubPassedNBjets;

  // Histograms
  std::vector<WrappedTH1*> hSelectedBJetPt;
  std::vector<WrappedTH1*> hSelectedBJetEta;
};

#endif
