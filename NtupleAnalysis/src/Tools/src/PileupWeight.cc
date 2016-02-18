#include "Tools/interface/PileupWeight.h"
#include "Framework/interface/Exception.h"

#include "TFile.h"
#include "TH1.h"

PileupWeight::PileupWeight(const ParameterSet& pset)
: fEnabled(false),
  h_weight(nullptr) {
  boost::optional<bool> status = pset.getParameterOptional<bool>("usePileupWeights");
  if (status) {
    fEnabled = *status;
  }
}
PileupWeight::~PileupWeight() {}

double PileupWeight::getWeight(const Event& fEvent){
  if(!fEnabled || fEvent.isData()) return 1;

  if(h_weight == 0)
    throw hplus::Exception("runtime") << "PileupWeight enabled, but no PileupWeights in multicrab!";

  int NPU = fEvent.vertexInfo().simulatedValue();
  int bin = h_weight->GetXaxis()->FindBin( NPU );
  //std::cout << "***" << NPU << ":" << bin << ":" << h_weight->GetBinContent( bin ) << std::endl;
  return h_weight->GetBinContent( bin );
}

void PileupWeight::calculateWeights(TH1* h_data, TH1* h_mc){
  if(!h_data or !h_mc)
    throw hplus::Exception("runtime") << "Did not find pileup distributions";

  h_data->Scale(1.0/h_data->Integral());
  h_mc->Scale(1.0/h_mc->Integral());
  //std::cout << h_data->Integral() << ", " << h_mc->Integral() << std::endl;

  h_weight = (TH1*)h_data->Clone("lumiWeights");
  h_weight->Divide(h_mc);
//   for (int i = 1; i < h_weight->GetNbinsX()+1; ++i)
//     std::cout << i << ":" << h_weight->GetBinContent(i) << std::endl;
}
