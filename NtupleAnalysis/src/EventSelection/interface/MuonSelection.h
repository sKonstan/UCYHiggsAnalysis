// -*- c++ -*-
#ifndef EventSelection_MuonSelection_h
#define EventSelection_MuonSelection_h

#include "EventSelection/interface/BaseSelection.h"
#include "DataFormat/interface/Muon.h"
#include "Framework/interface/EventCounter.h"

#include <string>
#include <vector>

class ParameterSet;
class CommonPlots;
class Event;
class EventCounter;
class HistoWrapper;
class WrappedTH1;
class WrappedTH2;

class MuonSelection: public BaseSelection {
public:
    /**
    * Class to encapsulate the access to the data members of
    * TauSelection. If you want to add a new accessor, add it here
    * and keep all the data of TauSelection private.
    */
  class Data {
  public:
    // The reason for pointer instead of reference is that const
    // reference allows temporaries, while const pointer does not.
    // Here the object pointed-to must live longer than this object.
    Data();
    ~Data();

    const bool hasIdentifiedMuons() const { return (fSelectedMuons.size() > 0); }
    const std::vector<Muon>& getSelectedMuons() const { return fSelectedMuons; }
    const float getHighestSelectedMuonPt() const { return fHighestSelectedMuonPt; }
    const float getHighestSelectedMuonEta() const { return fHighestSelectedMuonEta; }
    const float getHighestSelectedMuonPtBeforePtCut() const { return fHighestSelectedMuonPtBeforePtCut; }

    friend class MuonSelection;

  private:
    /// pt and eta of highest pt muon passing the selection
    float fHighestSelectedMuonPt;
    float fHighestSelectedMuonEta;
    float fHighestSelectedMuonPtBeforePtCut;

    std::vector<Muon> fSelectedMuons;
  };
  
  // Main class
  explicit MuonSelection(const ParameterSet& config, EventCounter& eventCounter, HistoWrapper& histoWrapper, CommonPlots* commonPlots, const std::string& postfix);
  explicit MuonSelection(const ParameterSet& config, const std::string& postfix);
  virtual ~MuonSelection();

  virtual void bookHistograms(TDirectory* dir);
  
  /// Use silentAnalyze() if you do not want to fill histograms or increment counters. Otherwise use analyze()
  Data silentAnalyze(const Event& event);
  Data analyze(const Event& event);

private:
  /// Initialisation called from constructor
  void initialize(const ParameterSet& config, const std::string& postfix);
  /// The actual selection
  Data privateAnalyze(const Event& iEvent);

  // Input parameters
  const double cfg_PtCut;
  const double cfg_EtaCut;
  std::string cfg_RelIsolString;
  float cfg_RelIsoCut;
  bool cfg_VetoMode;
  
  // Event counter for passing selection
  Count cPassedMuonSelection;
  // Event sub-counters for passing selection       
  Count cSubAll;
  Count cSubPassedPt;
  Count cSubPassedEta;
  Count cSubPassedID;
  Count cSubPassedIsolation;
  
  // Histograms
  WrappedTH1 *hMuonPtAll;
  WrappedTH1 *hMuonEtaAll;
  WrappedTH1 *hMuonPtPassed;
  WrappedTH1 *hMuonEtaPassed;
  WrappedTH1 *hPtResolution;
  WrappedTH1 *hEtaResolution;
  WrappedTH1 *hPhiResolution;
  WrappedTH1 *hIsolPtBefore;
  WrappedTH1 *hIsolEtaBefore;
  WrappedTH1 *hIsolVtxBefore;
  WrappedTH1 *hIsolPtAfter;
  WrappedTH1 *hIsolEtaAfter;
  WrappedTH1 *hIsolVtxAfter;
};

#endif
