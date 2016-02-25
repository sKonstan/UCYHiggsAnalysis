// -*- c++ -*-
#ifndef DataFormat_HLTMu_h
#define DataFormat_HLTMu_h

#include "DataFormat/interface/HLTMuGenerated.h"
#include "DataFormat/interface/ParticleIterator.h"

#include <vector>

class HLTMu;

class HLTMuCollection: public HLTMuGeneratedCollection, public ParticleIteratorAdaptor<HLTMuCollection> {
public:
  using value_type = HLTMu;

  HLTMuCollection() {}
  explicit HLTMuCollection(const std::string& prefix): HLTMuGeneratedCollection(prefix) {}
  ~HLTMuCollection() {}

  void setupBranches(BranchManager& mgr);

  HLTMu operator[](size_t i) const;
  std::vector<HLTMu> toVector() const;

  friend class HLTMu;
  friend class HLTMuGenerated<HLTMuCollection>;
  friend class Particle<HLTMuCollection>;

protected:

private:

};

class HLTMu: public HLTMuGenerated<HLTMuCollection> {
public:
  HLTMu() {}
  HLTMu(const HLTMuCollection* coll, size_t index): HLTMuGenerated(coll, index) {}
  ~HLTMu() {}
  
};

inline
HLTMu HLTMuCollection::operator[](size_t i) const {
  return HLTMu(this, i);
}

inline
std::vector<HLTMu> HLTMuCollection::toVector() const {
  return ParticleCollectionBase::toVector(*this);
}

#endif
