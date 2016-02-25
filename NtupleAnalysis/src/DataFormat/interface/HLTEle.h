// -*- c++ -*-
#ifndef DataFormat_HLTEle_h
#define DataFormat_HLTEle_h

#include "DataFormat/interface/HLTEleGenerated.h"
#include "DataFormat/interface/ParticleIterator.h"

#include <vector>

class HLTEle;

class HLTEleCollection: public HLTEleGeneratedCollection, public ParticleIteratorAdaptor<HLTEleCollection> {
public:
  using value_type = HLTEle;

  HLTEleCollection() {}
  explicit HLTEleCollection(const std::string& prefix): HLTEleGeneratedCollection(prefix) {}
  ~HLTEleCollection() {}

  void setupBranches(BranchManager& mgr);

  HLTEle operator[](size_t i) const;
  std::vector<HLTEle> toVector() const;

  friend class HLTEle;
  friend class HLTEleGenerated<HLTEleCollection>;
  friend class Particle<HLTEleCollection>;

protected:

private:

};

class HLTEle: public HLTEleGenerated<HLTEleCollection> {
public:
  HLTEle() {}
  HLTEle(const HLTEleCollection* coll, size_t index): HLTEleGenerated(coll, index) {}
  ~HLTEle() {}
  
};

inline
HLTEle HLTEleCollection::operator[](size_t i) const {
  return HLTEle(this, i);
}

inline
std::vector<HLTEle> HLTEleCollection::toVector() const {
  return ParticleCollectionBase::toVector(*this);
}

#endif
