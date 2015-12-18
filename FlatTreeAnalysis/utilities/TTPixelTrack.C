#ifndef TTPixelTrack_cxx
#define TTPixelTrack_cxx

#include "TTPixelTrack.h"

//****************************************************************************
TTPixelTrack::TTPixelTrack()
//****************************************************************************
{

  _InitVars();

}


//****************************************************************************
TTPixelTrack::~TTPixelTrack()
//****************************************************************************
{

}


//****************************************************************************
void TTPixelTrack::_InitVars(void)
//****************************************************************************
{

  theMomentum.SetXYZ(0.0, 0.0, 0.0);
  theRInv      = 0.0;
  thePOCA.SetXYZ(0.0, 0.0, 0.0);
  theZ0        = 0.0;
  theD0        = 0.0;
  theChi2      = 0.0;
  theChi2Red   = 0.0;
  theSigmaRInv = 0.0;
  theSigmaPhi0 = 0.0;
  theSigmaD0   = 0.0;
  theSigmaT    = 0.0;
  theSigmaZ0   = 0.0;
  thenhit      = 0;
  thencandidatehit = 0;
  thePixelHits.clear();
  theCandidatePixelHits.clear();
  pixHits_R.clear();
  pixHits_Z.clear();
  pixHits_Phi.clear();
  pixHits_Type.clear();
  candPixHits_R.clear();
  candPixHits_Z.clear();
  candPixHits_Phi.clear();
  candPixHits_Type.clear();

  return;
}


//****************************************************************************
void TTPixelTrack::init(TVector3 aMomentum,
			TVector3 aPOCA,
                        double aRInv,
                        double aChi2,
                        int    anhit,
                        double sigmarinv,
                        double sigmad0,
                        double sigmaphi0,
                        double sigmat,
                        double sigmaz0,
                        std::vector<TVector3> pixHits,
                        std::vector<TVector3> candidatePixHits)
//****************************************************************************
{

  // theL1Track=aL1Track;
  _InitVars();
  theMomentum           = aMomentum;
  thePOCA               = aPOCA;
  theZ0                 = getZ0();
  theD0                 = getD0();
  theRInv               = aRInv;
  theCharge             = getCharge();
  theChi2               = aChi2;
  thenhit               = anhit;
  thencandidatehit      = (int) candidatePixHits.size();
  theSigmaRInv          = sigmarinv;
  theSigmaPhi0          = sigmad0;
  theSigmaD0            = sigmaphi0;
  theSigmaT             = sigmat;
  theSigmaZ0            = sigmaz0;
  thePixelHits          = pixHits;
  theCandidatePixelHits = candidatePixHits;
  _FillAuxPixelHitVariables();
  
  return;
}


//****************************************************************************
double TTPixelTrack::getD0(void)
//****************************************************************************
{
  theD0 = -thePOCA.X() * sin( theMomentum.Phi() ) + thePOCA.Y() * cos(theMomentum.Phi() );
  return theD0;
}


//****************************************************************************
int TTPixelTrack::getCharge(void)
//****************************************************************************
{
  if (theRInv < 0.0) theCharge = -1;
  else if (theRInv > 0.0) theCharge = +1;
  else{
    std::cout << "E R R O R ! TTPixelTrack::getCharge(...) - Invalid value for theRInv \"" << theRInv << "\". EXIT" << std::endl;
    exit(1);
  }

  return theCharge;
}



//****************************************************************************
int TTPixelTrack::getPixelHitType(TVector3 pixHit)
//****************************************************************************
{
  
  int type = 4;
  if ( pixHit.Perp() < 12.0 ) type=3;
  if ( pixHit.Perp() <  8.0 ) type=2;
  if ( pixHit.Perp() <  5.0 ) type=1;
  
  if ( fabs( pixHit.Z() ) > 28.0) type=-1;
  if ( fabs( pixHit.Z() ) > 35.0) type=-2;
  if ( fabs( pixHit.Z() ) > 45.0) type=-3;
  
 return type;
 
}


//****************************************************************************
int TTPixelTrack::getPixelHitsPattern(void)
//****************************************************************************
{
  
  int nHits = (int) thePixelHits.size();  
  thePixelHitsPattern=0;
  
  for(int i =0; i< nHits; i++){

    int hitType = getPixelHitType(thePixelHits.at(i));
    if (hitType > 0) thePixelHitsPattern += pow(2, abs(hitType)-1);
    else thePixelHitsPattern += pow(2, abs(hitType)-1+4);
  }

  return thePixelHitsPattern;

}


//****************************************************************************
void TTPixelTrack::_FillAuxPixelHitVariables(void)
//****************************************************************************
{

  for(int i = 0; i < (int) thePixelHits.size(); i++){
    pixHits_R.push_back( thePixelHits.at(i).Perp() );
    pixHits_Z.push_back( thePixelHits.at(i).Z() );
    pixHits_Phi.push_back( thePixelHits.at(i).Phi() );
    pixHits_Type.push_back( getPixelHitType(thePixelHits.at(i) ) );
  }
  
  for(int i = 0; i < (int) theCandidatePixelHits.size(); i++){    
    candPixHits_R.push_back(    theCandidatePixelHits.at(i).Perp() );
    candPixHits_Z.push_back(    theCandidatePixelHits.at(i).Z()    );
    candPixHits_Phi.push_back(  theCandidatePixelHits.at(i).Phi()  );
    candPixHits_Type.push_back( getPixelHitType( theCandidatePixelHits.at(i) ) );
}    
  
  return;
}


//****************************************************************************
void TTPixelTrack::PrintProperties(void)
//****************************************************************************
{
  
  Table info("Pt | Eta | Phi | z0 | d0 | Q | ChiSq | RedChiSq | Hits | Hits Pattern | Hit-Type | Hit-R | Hit-Z | Hit-Phi", "Text");
  info.AddRowColumn(0, auxTools.ToString( theMomentum.Perp(), 4) );
  info.AddRowColumn(0, auxTools.ToString( theMomentum.Eta() , 4) );
  info.AddRowColumn(0, auxTools.ToString( theMomentum.Phi() , 4) );
  info.AddRowColumn(0, auxTools.ToString( theZ0, 4) );
  info.AddRowColumn(0, auxTools.ToString( theD0, 4) );
  string theQ = "-";
  if(theCharge > 0) theQ = "+";
  info.AddRowColumn(0, theQ);
  info.AddRowColumn(0, auxTools.ToString( theChi2 ) );
  info.AddRowColumn(0, auxTools.ToString( theChi2Red ) );
  info.AddRowColumn(0, auxTools.ToString( thenhit) + " (" + auxTools.ToString(candPixHits_Type.size()) + ")" );
  int pixHits_Pattern = getPixelHitsPattern();
  info.AddRowColumn(0, auxTools.ToString( pixHits_Pattern) );
  info.AddRowColumn(0, auxTools.ConvertIntVectorToString(pixHits_Type) );
  info.AddRowColumn(0, auxTools.ConvertIntVectorToString(pixHits_R)    );
  info.AddRowColumn(0, auxTools.ConvertIntVectorToString(pixHits_Z)    );
  info.AddRowColumn(0, auxTools.ConvertIntVectorToString(pixHits_Phi)  );
  // info.AddRowColumn(0, auxTools.ToString(candPixHits_Type.size()) );
  // info.AddRowColumn(0, auxTools.ConvertIntVectorToString(candPixHits_Type) );
  // info.AddRowColumn(0, auxTools.ConvertIntVectorToString(candPixHits_R)    );
  // info.AddRowColumn(0, auxTools.ConvertIntVectorToString(candPixHits_Z)    );
  // info.AddRowColumn(0, auxTools.ConvertIntVectorToString(candPixHits_Phi)  );
  info.Print();

  return;
}


//****************************************************************************
void TTPixelTrack::PrintAllProperties(void)
//****************************************************************************
{
  
  std::vector<double> pixHits_R;
  std::vector<double> pixHits_Z;
  std::vector<double> pixHits_Phi;
  for(int i = 0; i < (int) thePixelHits.size(); i++){
    pixHits_R.push_back( thePixelHits.at(i).Perp() );
    pixHits_Z.push_back( thePixelHits.at(i).Z() );
    pixHits_Phi.push_back( thePixelHits.at(i).Phi() );
  }    

  Table info("Pt | Eta | Phi | RInv | x0 | y0 | z0 | chi2 | redChi2 | err(RInv) | err(Phi0) | err(D0) | err(T) | err(Z0) | NHits | Hit R | Hit Z | Hit Phi", "Text");
  info.AddRowColumn(0, auxTools.ToString( theMomentum.Perp() ) );
  info.AddRowColumn(0, auxTools.ToString( theMomentum.Eta() ) );
  info.AddRowColumn(0, auxTools.ToString( theMomentum.Phi() ) );
  info.AddRowColumn(0, auxTools.ToString( theRInv ) );
  info.AddRowColumn(0, auxTools.ToString( thePOCA.X() ) );
  info.AddRowColumn(0, auxTools.ToString( thePOCA.Y() ) );
  info.AddRowColumn(0, auxTools.ToString( thePOCA.Z() ) );
  info.AddRowColumn(0, auxTools.ToString( theChi2 ) );
  info.AddRowColumn(0, auxTools.ToString( theChi2Red ) );
  info.AddRowColumn(0, auxTools.ToString( theSigmaRInv ) );
  info.AddRowColumn(0, auxTools.ToString( theSigmaPhi0 ) );
  info.AddRowColumn(0, auxTools.ToString( theSigmaD0 ) );
  info.AddRowColumn(0, auxTools.ToString( theSigmaT) );
  info.AddRowColumn(0, auxTools.ToString( theSigmaZ0) );
  info.AddRowColumn(0, auxTools.ToString( thenhit) );
  info.AddRowColumn(0, auxTools.ConvertIntVectorToString(pixHits_R)    );
  info.AddRowColumn(0, auxTools.ConvertIntVectorToString(pixHits_Z)    );
  info.AddRowColumn(0, auxTools.ConvertIntVectorToString(pixHits_Phi)  );
  info.Print();

  return;
}

#endif
