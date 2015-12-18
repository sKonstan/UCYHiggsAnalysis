// root -l
// .x runPixelRefitting.cc("L1PixTks_CandPixHits_TPs_GenPs_NPixHitsMin3_rphi3mm_rz5mm_PrivateProduction_29July2015", "SingleMuon_NoPU", "", -1);
void runPixelRefitting(const std::string MulticrabDir = "", 
		      const std::string SampleName = "", 
		      const std::string text = "", 
		      const int maxEvents = -1)
{

  gSystem->CompileMacro("PixelRefitting.C");

  const std::string absolutePath = "/Users/attikis/hltaus/rootFiles/TTrees/CMSSW_6_2_0_SLHC12_patch1/TkTauFromCaloAnalyzer_v6";
  
  PixelRefitting macro(absolutePath + "/" + MulticrabDir, SampleName, text, maxEvents);
  macro.Loop();
}
