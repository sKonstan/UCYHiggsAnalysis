#include <iostream>                                                        
#include <fstream>                                                         
#include <TCanvas.h>                                                       
#include <TH1.h>                                                           
#include <TFile.h>
#include <cmath>                                                         

// DYJetsToLL_M_10to50  0.08511908
// DYJetsToLL_M_50      0.03000326
// ttHJetToNonbb_M125   0.00000253
// TTJets               0.00857211
// WJetsToLNu           0.29992937
// WW                   0.00021082
// WZ                   0.00007608
// ZZ                   0.00003436

double w[8];

void test() { 
  TFile *f = new TFile ("SignalAnalysis_13Apr2016_23h01m05s/TTJets/res/histograms-TTJets.root");
  TFile *y= (TFile*) f->Get("SignalAnalysis_mH125_Run2015D");
  TFile *f1_ttH=new TFile ("SignalAnalysis_13Apr2016_23h01m05s/ttHJetToNonbb_M125/res/histograms-ttHJetToNonbb_M125.root");
  TFile *f1_ZZ=new TFile ("SignalAnalysis_13Apr2016_23h01m05s/ZZ/res/histograms-ZZ.root");
  TFile *f1_WZ=new TFile ("SignalAnalysis_13Apr2016_23h01m05s/WZ/res/histograms-WZ.root");
  TFile *f1_WW=new TFile ("SignalAnalysis_13Apr2016_23h01m05s/WW/res/histograms-WW.root");
  TFile *f1_WJetsToLNu=new TFile ("SignalAnalysis_13Apr2016_23h01m05s/WJetsToLNu/res/histograms-WJetsToLNu.root");
  TFile *f1_TTJets=new TFile ("SignalAnalysis_13Apr2016_23h01m05s/TTJets/res/histograms-TTJets.root");
  TFile *f1_DYJetsToLL_M_10to50=new TFile ("SignalAnalysis_13Apr2016_23h01m05s/DYJetsToLL_M_10to50/res/histograms-DYJetsToLL_M_10to50.root");
  TFile *f1_DYJetsToLL_M_50=new TFile ("SignalAnalysis_13Apr2016_23h01m05s/DYJetsToLL_M_50/res/histograms-DYJetsToLL_M_50.root");

  TFile *f_ttH= (TFile*) f1_ttH->Get("SignalAnalysis_mH125_Run2015D");
  TFile *f_ZZ= (TFile*) f1_ZZ->Get("SignalAnalysis_mH125_Run2015D");
  TFile *f_WZ= (TFile*) f1_WZ->Get("SignalAnalysis_mH125_Run2015D");
  TFile *f_WW= (TFile*) f1_WW->Get("SignalAnalysis_mH125_Run2015D");
  TFile *f_WJetsToLNu= (TFile*) f1_WJetsToLNu->Get("SignalAnalysis_mH125_Run2015D");
  TFile *f_TTJets= (TFile*) f1_TTJets->Get("SignalAnalysis_mH125_Run2015D");
  TFile *f_DYJetsToLL_M_10to50= (TFile*) f1_DYJetsToLL_M_10to50->Get("SignalAnalysis_mH125_Run2015D");
  TFile *f_DYJetsToLL_M_50= (TFile*) f1_DYJetsToLL_M_50->Get("SignalAnalysis_mH125_Run2015D");

  w[0]= 0.00000253*10000;
  w[1]= 0.00003436*10000;
  w[2]= 0.00007608*10000;
  w[3]= 0.00021082*10000;
  w[4]= 0.29992937*10000;
  w[5]= 0.00857211*10000;
  w[6]= 0.08511908*10000;
  w[7]= 0.03000326*10000;
  //................................................................................................................................................//

  TH1D *LepImpPar =(TH1D*) y->Get("LepImpPar");
  TH2I *LepMode =(TH2I* ) y->Get("LepMode");
 
  //===========================================================MET cut===========================================================//
  TH1D *h_METcut_ttH=(TH1D*) f_ttH->Get("METcut");
  TH1D *h_METcut_ZZ=(TH1D*) f_ZZ->Get("METcut");
  TH1D *h_METcut_WZ=(TH1D*) f_WZ->Get("METcut");
  TH1D *h_METcut_WW=(TH1D*) f_WW->Get("METcut");
  TH1D *h_METcut_WJetsToLNu  =(TH1D*) f_WJetsToLNu->Get("METcut");
  TH1D *h_METcut_TTJets=(TH1D*) f_TTJets->Get("METcut");
  TH1D *h_METcut_DYJetsToLL_M_10to50=(TH1D*) f_DYJetsToLL_M_10to50->Get("METcut");
  TH1D *h_METcut_DYJetsToLL_M_50=(TH1D*) f_DYJetsToLL_M_50->Get("METcut");

  int nbins=100;
  double BinCont[8][nbins];  //[dataset][bin]
  double signal[nbins],signBkg[nbins], Significance[nbins], x[nbins];

  for (int i=0;i<8;i++){
    for (int j=0;j<nbins;j++){
      BinCont[i][j]=0;
    }
  }
  for (int i=0; i<nbins; i++){
    signal[i]=0;
    signBkg[i]=0;
    Significance[i]=0;
    x[i]=i;
  }


   for (int i=1; i<nbins+1; i=i+5){
    BinCont[0][i-1]=h_METcut_ttH->GetBinContent(i);
    BinCont[1][i-1]=h_METcut_ZZ->GetBinContent(i);
    BinCont[2][i-1]=h_METcut_WZ->GetBinContent(i);
    BinCont[3][i-1]=h_METcut_WW->GetBinContent(i);
    BinCont[4][i-1]=h_METcut_WJetsToLNu->GetBinContent(i);
    BinCont[5][i-1]=h_METcut_TTJets->GetBinContent(i);
    BinCont[6][i-1]=h_METcut_DYJetsToLL_M_10to50->GetBinContent(i);
    BinCont[7][i-1]=h_METcut_DYJetsToLL_M_50->GetBinContent(i);
  }


  for (int i=0; i<nbins; i++){
    signal[i]=w[0]*BinCont[0][i];
    for (int j=0; j<8;j++){
      signBkg[i]+=w[j]*BinCont[j][i];
    }
    Significance[i]=signal[i]/sqrt(signBkg[i]);
  }


  std::cout<<"MET_cut"<<std::endl;
  
  TCanvas *c3 = new TCanvas("c3","MEt_cut vs Significance",200,10,700,500);
  gr = new TGraph(nbins,x,Significance);
  c3->cd();
  c3->SetGrid();
  //gr->SetMarkerSize(2);
  gr->SetMarkerStyle(5);
  gr->SetTitle("ME_{T} cut vs Significance");
  gr->GetXaxis()->SetTitle("ME_{T} cut (GeV)");
  gr->GetYaxis()->SetTitle("Significance");
  gr->Draw("AP");
  c3->SaveAs("METcut_Eff.png");

  //===================================NJets_cut===================================================//

  TH1D *h_NJets_cut_ttH=(TH1D*) f_ttH->Get("NJets_cut");
  TH1D *h_NJets_cut_ZZ=(TH1D*) f_ZZ->Get("NJets_cut");
  TH1D *h_NJets_cut_WZ=(TH1D*) f_WZ->Get("NJets_cut");
  TH1D *h_NJets_cut_WW=(TH1D*) f_WW->Get("NJets_cut");
  TH1D *h_NJets_cut_WJetsToLNu  =(TH1D*) f_WJetsToLNu->Get("NJets_cut");
  TH1D *h_NJets_cut_TTJets=(TH1D*) f_TTJets->Get("NJets_cut");
  TH1D *h_NJets_cut_DYJetsToLL_M_10to50=(TH1D*) f_DYJetsToLL_M_10to50->Get("NJets_cut");
  TH1D *h_NJets_cut_DYJetsToLL_M_50=(TH1D*) f_DYJetsToLL_M_50->Get("NJets_cut");

  nbins=11;
  for (int i=0;i<8;i++){
    for (int j=0;j<100;j++){
      BinCont[i][j]=0;
    }
  }
  for (int i=0; i<nbins; i++){
    signal[i]=0;
    signBkg[i]=0;
    Significance[i]=0;
    x[i]=i+2;
  }


  for (int i=1; i<nbins+1; i++){
    BinCont[0][i-1]=h_NJets_cut_ttH->GetBinContent(i);
    BinCont[1][i-1]=h_NJets_cut_ZZ->GetBinContent(i);
    BinCont[2][i-1]=h_NJets_cut_WZ->GetBinContent(i);
    BinCont[3][i-1]=h_NJets_cut_WW->GetBinContent(i);
    BinCont[4][i-1]=h_NJets_cut_WJetsToLNu->GetBinContent(i);
    BinCont[5][i-1]=h_NJets_cut_TTJets->GetBinContent(i);
    BinCont[6][i-1]=h_NJets_cut_DYJetsToLL_M_10to50->GetBinContent(i);
    BinCont[7][i-1]=h_NJets_cut_DYJetsToLL_M_50->GetBinContent(i);
  }


  for (int i=0; i<nbins; i++){
    signal[i]=w[0]*BinCont[0][i];
    for (int j=0; j<8;j++){
      signBkg[i]+=w[j]*BinCont[j][i];
    }
    Significance[i]=signal[i]/sqrt(signBkg[i]);
  }

  std::cout<<"NJets_cut"<<std::endl;
  
  TCanvas *c4 = new TCanvas("NJets_cut vs Significance","NJets_cut vs Significance",200,10,700,500);
  gr1 = new TGraph(nbins,x,Significance);
  c4->cd();
  c4->SetGrid();
  //gr->SetMarkerSize(2);
  gr1->SetMarkerStyle(5);
  gr1->SetTitle("NJets_cut vs Significance");
  gr1->GetXaxis()->SetTitle("NJets_cut");
  gr1->GetYaxis()->SetTitle("Significance");
  gr1->Draw("AP");
  c4->SaveAs("NJETScut_Eff.png");
  
  //=========================================Lep1Pt_cut=================================================//
  TH1D *h_Lep1Pt_cut_ttH=(TH1D*) f_ttH->Get("Lep1Pt_cut");
  TH1D *h_Lep1Pt_cut_ZZ=(TH1D*) f_ZZ->Get("Lep1Pt_cut");
  TH1D *h_Lep1Pt_cut_WZ=(TH1D*) f_WZ->Get("Lep1Pt_cut");
  TH1D *h_Lep1Pt_cut_WW=(TH1D*) f_WW->Get("Lep1Pt_cut");
  TH1D *h_Lep1Pt_cut_WJetsToLNu  =(TH1D*) f_WJetsToLNu->Get("Lep1Pt_cut");
  TH1D *h_Lep1Pt_cut_TTJets=(TH1D*) f_TTJets->Get("Lep1Pt_cut");
  TH1D *h_Lep1Pt_cut_DYJetsToLL_M_10to50=(TH1D*) f_DYJetsToLL_M_10to50->Get("Lep1Pt_cut");
  TH1D *h_Lep1Pt_cut_DYJetsToLL_M_50=(TH1D*) f_DYJetsToLL_M_50->Get("Lep1Pt_cut");

 nbins=20;

  for (int i=0;i<8;i++){
    for (int j=0;j<100;j++){
      BinCont[i][j]=0;
    }
  }
  for (int i=0; i<nbins; i++){
    signal[i]=0;
    signBkg[i]=0;
    Significance[i]=0;
    x[i]=i;
  }


  for (int i=1; i<nbins+1; i++){
    BinCont[0][i-1]=h_Lep1Pt_cut_ttH->GetBinContent(i);
    BinCont[1][i-1]=h_Lep1Pt_cut_ZZ->GetBinContent(i);
    BinCont[2][i-1]=h_Lep1Pt_cut_WZ->GetBinContent(i);
    BinCont[3][i-1]=h_Lep1Pt_cut_WW->GetBinContent(i);
    BinCont[4][i-1]=h_Lep1Pt_cut_WJetsToLNu->GetBinContent(i);
    BinCont[5][i-1]=h_Lep1Pt_cut_TTJets->GetBinContent(i);
    BinCont[6][i-1]=h_Lep1Pt_cut_DYJetsToLL_M_10to50->GetBinContent(i);
    BinCont[7][i-1]=h_Lep1Pt_cut_DYJetsToLL_M_50->GetBinContent(i);
  }


  for (int i=0; i<nbins; i++){
    signal[i]=w[0]*BinCont[0][i];
    for (int j=0; j<8;j++){
      signBkg[i]+=w[j]*BinCont[j][i];
    }
    Significance[i]=signal[i]/sqrt(signBkg[i]);
  }


  std::cout<<"Lep1Pt__cut"<<std::endl;
  
  TCanvas *c5 = new TCanvas("c5","Lep1Pt_cut vs Significance",200,10,700,500);
  gr = new TGraph(nbins,x,Significance);
  c5->cd();
  c5->SetGrid();
  //gr->SetMarkerSize(2);
  gr->SetMarkerStyle(5);
  gr->SetTitle("Lep1Pt cut vs Significance");
  gr->GetXaxis()->SetTitle("Lep1Pt cut (GeV)");
  gr->GetYaxis()->SetTitle("Significance");
  gr->Draw("AP");
  c5->SaveAs("Lep1Pt_cut_Eff.png");

  //=====================================Lep2Pt_cut========================================//
  TH1D *h_Lep2Pt_cut_ttH=(TH1D*) f_ttH->Get("Lep2Pt_cut");
  TH1D *h_Lep2Pt_cut_ZZ=(TH1D*) f_ZZ->Get("Lep2Pt_cut");
  TH1D *h_Lep2Pt_cut_WZ=(TH1D*) f_WZ->Get("Lep2Pt_cut");
  TH1D *h_Lep2Pt_cut_WW=(TH1D*) f_WW->Get("Lep2Pt_cut");
  TH1D *h_Lep2Pt_cut_WJetsToLNu  =(TH1D*) f_WJetsToLNu->Get("Lep2Pt_cut");
  TH1D *h_Lep2Pt_cut_TTJets=(TH1D*) f_TTJets->Get("Lep2Pt_cut");
  TH1D *h_Lep2Pt_cut_DYJetsToLL_M_10to50=(TH1D*) f_DYJetsToLL_M_10to50->Get("Lep2Pt_cut");
  TH1D *h_Lep2Pt_cut_DYJetsToLL_M_50=(TH1D*) f_DYJetsToLL_M_50->Get("Lep2Pt_cut");

 nbins=20;

  for (int i=0;i<8;i++){
    for (int j=0;j<100;j++){
      BinCont[i][j]=0;
    }
  }
  for (int i=0; i<nbins; i++){
    signal[i]=0;
    signBkg[i]=0;
    Significance[i]=0;
    x[i]=i;
  }


  for (int i=1; i<nbins+1; i++){
    BinCont[0][i-1]=h_Lep2Pt_cut_ttH->GetBinContent(i);
    BinCont[1][i-1]=h_Lep2Pt_cut_ZZ->GetBinContent(i);
    BinCont[2][i-1]=h_Lep2Pt_cut_WZ->GetBinContent(i);
    BinCont[3][i-1]=h_Lep2Pt_cut_WW->GetBinContent(i);
    BinCont[4][i-1]=h_Lep2Pt_cut_WJetsToLNu->GetBinContent(i);
    BinCont[5][i-1]=h_Lep2Pt_cut_TTJets->GetBinContent(i);
    BinCont[6][i-1]=h_Lep2Pt_cut_DYJetsToLL_M_10to50->GetBinContent(i);
    BinCont[7][i-1]=h_Lep2Pt_cut_DYJetsToLL_M_50->GetBinContent(i);
  }


  for (int i=0; i<nbins; i++){
    signal[i]=w[0]*BinCont[0][i];
    for (int j=0; j<8;j++){
      signBkg[i]+=w[j]*BinCont[j][i];
    }
    Significance[i]=signal[i]/sqrt(signBkg[i]);
  }


  std::cout<<"Lep2Pt__cut"<<std::endl;

  TCanvas *c6 = new TCanvas("c6","Lep2Pt_cut vs Significance",200,10,700,500);
  gr = new TGraph(nbins,x,Significance);
  c6->cd();
  c6->SetGrid();
  //gr->SetMarkerSize(2);
  gr->SetMarkerStyle(5);
  gr->SetTitle("Lep2Pt cut vs Significance");
  gr->GetXaxis()->SetTitle("Lep2Pt cut (GeV)");
  gr->GetYaxis()->SetTitle("Significance");
  gr->Draw("AP");
  c6->SaveAs("Lep2Pt_cut_Eff.png");


  //=================Leptons-Impact Parameter===================================================//
  
  TCanvas *c1 = new TCanvas ("c1","c1",0,0,600,600);
  
  
  c1->SetLogy();
  c1->cd();
  TF1 *g1 = new TF1("g1","[0]*exp(-[1]*x)",0.1,0.2);
  int n=2;
  double par[2];
  par[0]=100; 
  par[1]=20;
  int i = 0;
  while(i==0){
    for(int j=0;j<2;j++) {g1->SetParameter(j,par[j]);}
    TFitResultPtr r1 = LepImpPar->Fit("g1","SRB");
    LepImpPar->Draw();
    for(int l=0;l<n;l++) {par[l]=r1->Value(l);}
    c1->Update();                                           
    c1->Modified(); 
    i=1;
    //cin>>i;                                                                                                                                                                                                             
  }
  c1->SaveAs("d0_fit.png");
  
  //====================Leptons Mode==========================================//
  TCanvas *c2 = new TCanvas ("c2","c2",0,0,600,600); 
  c2->cd();
  c2->SetGrid();
  LepMode->SetCanExtend(TH1::kAllAxes);
  LepMode->SetStats(0);
  LepMode->SetTitle("Leptons");
  //LepMode->LabelsOption("v");
  LepMode->Draw("TEXT"); 
  c2->SaveAs("LepMode.png");
  
    

 //=====================PassedEvts============================================================//
 TH1D *hPassedEvents_ttH=(TH1D*) f_ttH->Get("PassedEvents");
 TH1D *hPassedEvents_ZZ=(TH1D*) f_ZZ->Get("PassedEvents");
 TH1D *hPassedEvents_WZ=(TH1D*) f_WZ->Get("PassedEvents");
 TH1D *hPassedEvents_WW=(TH1D*) f_WW->Get("PassedEvents");
 TH1D *hPassedEvents_WJetsToLNu  =(TH1D*) f_WJetsToLNu->Get("PassedEvents");
 TH1D *hPassedEvents_TTJets=(TH1D*) f_TTJets->Get("PassedEvents");
 TH1D *hPassedEvents_DYJetsToLL_M_10to50=(TH1D*) f_DYJetsToLL_M_10to50->Get("PassedEvents");
 TH1D *hPassedEvents_DYJetsToLL_M_50=(TH1D*) f_DYJetsToLL_M_50->Get("PassedEvents");
 
 for (int i=0;i<8;i++){
   for (int j=0;j<100;j++){
     BinCont[i][j]=0;
   }
 }
 
 BinCont[0][5]=hPassedEvents_ttH->GetBinContent(5);
 BinCont[1][5]=hPassedEvents_ZZ->GetBinContent(5);
 BinCont[2][5]=hPassedEvents_WZ->GetBinContent(5);
 BinCont[3][5]=hPassedEvents_WW->GetBinContent(5);
 BinCont[4][5]=hPassedEvents_WJetsToLNu->GetBinContent(5);
 BinCont[5][5]=hPassedEvents_TTJets->GetBinContent(5);
 BinCont[6][5]=hPassedEvents_DYJetsToLL_M_10to50->GetBinContent(5);
 BinCont[7][5]=hPassedEvents_DYJetsToLL_M_50->GetBinContent(5);
 
 double Bkg=0;
 std::cout<<w[0]*BinCont[0][5]<<std::endl;
 for (int i=1; i<8; i++){
   Bkg+=w[i]*BinCont[i][5];
   std::cout<<w[i]*BinCont[i][5]<<std::endl;
 }   

 cout<<"s/sqrt(b)= "<<w[0]*BinCont[0][5]/sqrt(Bkg)<<endl;
 return;
}
