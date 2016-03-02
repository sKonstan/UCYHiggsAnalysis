// -*- c++ -*-
#ifndef EventSelection_METSelection_h
#define EventSelection_METSelection_h

#include "EventSelection/interface/BaseSelection.h"
#include "DataFormat/interface/MET.h"
#include "Framework/interface/EventCounter.h"
#include "Framework/interface/GenericScaleFactor.h"
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

class METSelection: public BaseSelection {
public:
  enum METType {
    kGenMET,
    kL1MET,
    kHLTMET,
    kCaloMET,
    kType1MET,
    kType1MET_noHF,
    kPuppiMET
  };
  
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

    const bool passedSelection() const { return bPassedSelection; }
    const math::XYVectorD& getMET() const;
    const float getMETSignificance() const { return fMETSignificance; }
    const float getMETTriggerSF() const { return fMETTriggerSF; }
    
    friend class METSelection;

  private:
    bool bPassedSelection;
    std::vector<math::XYVectorD> fSelectedMET; // MET collection for storing MET object (as p2 - easier tomanipulate)
    float fMETSignificance;
    float fMETTriggerSF; // Cache MET trigger SF
  };
  
  // Main class
  explicit METSelection(const ParameterSet& config, EventCounter& eventCounter, HistoWrapper& histoWrapper, CommonPlots* commonPlots, const std::string& postfix = "");
  explicit METSelection(const ParameterSet& config);
  virtual ~METSelection();

  virtual void bookHistograms(TDirectory* dir);
  
  /// Use silentAnalyze() if you do not want to fill histograms or increment counters. Otherwise use analyze() 
  Data silentAnalyze(const Event& event, int nVertices);
  Data analyze(const Event& event, int nVertices);

private:
  /// Initialisation called from constructor
  void initialize(const ParameterSet& config);
  /// The actual selection
  Data privateAnalyze(const Event& iEvent, int nVertices);

  // Input parameters
  const DirectionalCut<float> cfg_METCut;
  const DirectionalCut<float> cfg_METSignificanceCut;
  const std::string cfg_METTypeString;
  const bool cfg_PhiCorrections;
  METType cfg_METType;
  GenericScaleFactor cfg_METTriggerSFReader;
  
  // Event counter for passing selection
  Count cPassedMETSelection;

  // Histograms
  WrappedTH1 *hMET;
  WrappedTH1 *hMETSig;;

};

#endif
