#include "Framework/interface/HistoSplitter.h"
#include "Framework/interface/Exception.h"

#include <iomanip>
#include <sstream>

HistoSplitterItem::HistoSplitterItem(const ParameterSet& config)
: sLabel(config.getParameter<std::string>("label")),
  fBinLowEdges(config.getParameter<std::vector<float> >("binLowEdges")),
  bUseAbsoluteValues(config.getParameter<bool>("useAbsoluteValues", false)) {
  // Check awkward params
  if (sLabel.size() == 0)
    throw hplus::Exception("config") << "Label size is zero, please provide a label!";
  bool status = true;
  std::stringstream s;
  std::stringstream msg;
  float previousValue = 0;
  for (const auto p: fBinLowEdges) {
    if (s.str().size()) {
      s << ", " << p;
      if (p <= previousValue) {
        status = false;
        msg << previousValue << " vs. " << p;
      }
    } else {
      s << p;
    }
    previousValue = p;
  }
  if (!status)
    throw hplus::Exception("config") << "Bin low edges not sorted in ascending order! " << msg.str() << " in " << s.str();
}

const size_t HistoSplitterItem::getBinIndex(const float value) const {
  size_t n = fBinLowEdges.size();
  float testValue = value;
  if (bUseAbsoluteValues)
    testValue = std::abs(testValue);
  for (size_t i = 0; i < n; ++i) {
    if (testValue < fBinLowEdges[i])
      return i;
  }
  return n;
}

const std::string HistoSplitterItem::getBinDescription(const size_t i) const { 
  std::stringstream s;
  std::string label;
  if (bUseAbsoluteValues)
    label = "abs("+sLabel+")";
  else
    label = sLabel;
  if (this->getBinCount() == 1) 
    s << label << "=all";
  else if (i == 0)
    s << label << "<" << fBinLowEdges[i];
  else if (i == this->getBinCount()-1)
    s << label << ">" << fBinLowEdges[fBinLowEdges.size()-1];
  else if (i > 0 && i < this->getBinCount()-1)
    s << label << "=" << fBinLowEdges[i-1] << ".." << fBinLowEdges[i];
  else
    throw hplus::Exception("assert") << "Invalid index" << i << " for axis " << label << "! Valid range: 0.." << this->getBinCount()-1;
  return s.str();
}

HistoSplitter::HistoSplitter(const ParameterSet& config, HistoWrapper& histoWrapper)
: fHistoWrapper(histoWrapper) {
  // Create splitter items
  std::vector<ParameterSet> psets = config.getParameter<std::vector<ParameterSet>>("histogramSplitting", std::vector<ParameterSet>{});
  for (auto p: psets) {
    fHistoSplitterItems.push_back(HistoSplitterItem(p));
    fCurrentBinIndex.push_back(0);
  }
  // Count total number of histograms split histograms (not including the sum histo)
  fNUnfoldedBins = 1;
  for (auto p: fHistoSplitterItems) {
    fNUnfoldedBins *= p.getBinCount();
  }
  // Construct binning string
  std::stringstream s;
  for (auto p: fHistoSplitterItems) {
    if (s.str().size() > 0)
      s << ":";
      s << p.getLabel() << ":" << p.getBinCount();
  }
  s << ":";
  fBinningString = s.str();
  // Initialize other values
  initialize();
}
  
HistoSplitter::~HistoSplitter() { }

void HistoSplitter::bookHistograms(TDirectory* dir) {
  // Create histogram with binning information
  hBinInfo = fHistoWrapper.makeTH<TH1F>(HistoLevel::kSystematics, dir, "SplittedBinInfo", "SplittedBinInfo", fHistoSplitterItems.size()+1, 0, fHistoSplitterItems.size()+1);
  if (hBinInfo->isActive()) {
    hBinInfo->getHisto()->GetXaxis()->SetBinLabel(1, "Control"); // Needed when merging histograms (divide by this number the other bins)
    hBinInfo->SetBinContent(1, 1);
  }
  // Fill binning information histogram
  for (size_t i = 0; i < fHistoSplitterItems.size(); ++i) {
    // Fill histogram
    hBinInfo->getHisto()->GetXaxis()->SetBinLabel(i+2, fHistoSplitterItems[i].getLabel().c_str());
    hBinInfo->SetBinContent(i+2, fHistoSplitterItems[i].getBinCount());
  }
  // Add control count - Needed when merging histograms (divide by this number the other bins)
  hBinInfo->getHisto()->GetXaxis()->SetBinLabel(1, "Control");
  hBinInfo->SetBinContent(1, 1);
}

void HistoSplitter::initialize() {
  bIndicesAreValid = false;
}

void HistoSplitter::setFactorisationBinForEvent(const std::vector<float>& values) {
  bIndicesAreValid = true;
  size_t n = fHistoSplitterItems.size();
  if (!n) {
    fCurrentUnfoldedBinIndex = 0;
    return;
  }
  if (n != values.size())
    throw hplus::Exception("assert") << "setFactorisationBinForEvent() called with " << values.size() 
                                     << "entries when " << n << " were expected!";
  for (size_t i = 0; i < n; ++i) {
    fCurrentBinIndex[i] = fHistoSplitterItems[i].getBinIndex(values[i]);
  }
  fCurrentUnfoldedBinIndex = getShapeBinIndex();
}

void HistoSplitter::createShapeHistogram(HistoLevel level, TDirectory* dir, WrappedUnfoldedFactorisationHisto*& unfoldedHisto, const std::string& title, const std::string& label, int nbins, double min, double max) {
  // x-axis contains distribution, y-axis contains unfolded splitted bins (including under- and overflows)
  // Create histo
  std::string s = fBinningString+title+";"+label;
  unfoldedHisto = fHistoWrapper.makeTH<TH2F>(fNUnfoldedBins, level, dir, title.c_str(), s.c_str(), nbins, min, max);
  // Set labels to y-axis
  setAxisLabelsForUnfoldedHisto(unfoldedHisto);
}


void HistoSplitter::fillShapeHistogram(WrappedUnfoldedFactorisationHisto* h, double value) {
  checkIndexValidity();
  h->Fill(value, fCurrentUnfoldedBinIndex);
  //std::cout << "Filling shape " << h->getHisto()->GetTitle() << " current bin=" << fCurrentUnfoldedBinIndex << std::endl;
}

void HistoSplitter::fillShapeHistogram(WrappedUnfoldedFactorisationHisto* h, double value, double weight) {
  checkIndexValidity();
  h->Fill(value, fCurrentUnfoldedBinIndex, weight);
}


const size_t HistoSplitter::getShapeBinIndex() const {
  size_t index = 0;
  size_t multiplier = 1;
  for (size_t i = 0; i < fCurrentBinIndex.size(); ++i) {
    index += multiplier * fCurrentBinIndex[i];
    multiplier *= fHistoSplitterItems[i].getBinCount();
  }
  return index;
}

const std::vector<size_t> HistoSplitter::obtainIndicesFromUnfoldedIndex(size_t unfoldedIndex) const {
  std::vector<size_t> result;
  if (fHistoSplitterItems.size() == 0)
    return result;
  result.resize(fHistoSplitterItems.size());
  size_t base = fNUnfoldedBins;
  size_t remainder = unfoldedIndex;
  for (size_t i = 0; i < fHistoSplitterItems.size(); ++i) {
    size_t j = fHistoSplitterItems.size() - 1 - i;
    base /= fHistoSplitterItems[j].getBinCount();
    result[j] = remainder / base;
    remainder -= base*result[j];
  }
  if (remainder != 0)
    throw hplus::Exception("assert") << "Obtaining of bin indices from unfolded index failed!";
  return result;
}

void HistoSplitter::setAxisLabelsForUnfoldedHisto(WrappedUnfoldedFactorisationHisto* h) const {
  if (!h->isActive()) return;
  for (size_t i = 0; i < fNUnfoldedBins; ++i) {
    std::string myInfoString = getFullBinDescriptionStringByBinIndex(obtainIndicesFromUnfoldedIndex(i));
    h->getHisto()->GetYaxis()->SetBinLabel(i+1, myInfoString.c_str());
  }
}

void HistoSplitter::checkIndexValidity() const {
  if (!bIndicesAreValid)
    throw hplus::Exception("assert") << "You forgot to call HistoSplitter::setFactorisationBinForEvent() for the event! Check your code!";
}

const std::string HistoSplitter::getFullBinDescriptionStringByBinIndex(const std::vector<size_t >& indices) const {
  std::stringstream s;
  for (size_t i = 0; i < fHistoSplitterItems.size(); ++i) {
    if (s.str().size())
      s << ":";
    s << fHistoSplitterItems[i].getBinDescription(indices[i]);
  }
  // Fallback if no splitting is requested
  if (!s.str().size())
    s << "all bins";
  return s.str();
}
