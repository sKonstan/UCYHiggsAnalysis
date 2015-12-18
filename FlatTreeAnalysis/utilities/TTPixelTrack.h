#ifndef TTPixelTrack_h
#define TTPixelTrack_h

// System
#include <iostream>

// User
#include "AuxTools.C"
#include "Table.C"

using namespace std;

class TTPixelTrack{     
 public:
  // Constructors/Destructors
  TTPixelTrack();
  
  ~TTPixelTrack();
  
  // Function declaration
  void init(TVector3 aMomentum,
	    TVector3 aPOCA,
	    double aRInv,
	    double aChi2,
	    int nhit,
	    double sigmarinv, 
	    double sigmaphi0,
	    double sigmad0,
	    double sigmat,
	    double sigmaz0,
	    vector<TVector3> pixHits,
	    vector<TVector3> candidatePixHits);

  int getL1Track() const {return 0; }

  TVector3 getMomentum() const {return theMomentum;}
  
  double getRInv() const {return theRInv;}

  TVector3 getPOCA() const {return thePOCA;}

  double getZ0() const {return thePOCA.Z();}

  double getD0();

  int getCharge();

  double getChi2() const {return theChi2;}

  double getChi2Red() const {return theChi2Red;}
  
  double getSigmaRInv() const {return theSigmaRInv;}

  double getSigmaPhi0() const {return theSigmaPhi0;}

  double getSigmaD0() const {return theSigmaD0;}

  double getSigmaT() const {return theSigmaT;}

  double getSigmaZ0() const {return theSigmaZ0;}

  int getNhit() const {return thenhit;}

  int getPixelHitsPattern(void);

  int getCandidatePixelHitsPattern(void);

  int getNcandidatehit() const {return thencandidatehit;}

  int getPixelHitType(TVector3 pixHit);
    
  std::vector<TVector3> getPixelHits() const {return thePixelHits;}

  std::vector<TVector3> getCandidatePixelHits() const {return theCandidatePixelHits;}

  void PrintProperties(void);

  void PrintAllProperties(void);

  // Variable declaration
  TVector3 theMomentum;
  double theRInv;
  TVector3 thePOCA;
  double theZ0;
  double theD0;
  int theCharge;
  double theChi2;
  double theChi2Red;
  double theSigmaRInv;
  double theSigmaPhi0;
  double theSigmaD0;
  double theSigmaT;
  double theSigmaZ0;
  int thenhit;
  int thePixelHitsPattern;
  int thencandidatehit;
  std::vector<TVector3> thePixelHits;
  std::vector<TVector3> theCandidatePixelHits;
  std::vector<double> pixHits_R;
  std::vector<double> pixHits_Z;
  std::vector<double> pixHits_Phi;
  std::vector<double> pixHits_Type;
  std::vector<double> candPixHits_R;
  std::vector<double> candPixHits_Z;
  std::vector<double> candPixHits_Phi;
  std::vector<double> candPixHits_Type;
  
 private:
  void _FillAuxPixelHitVariables(void);

  void _InitVars(void);
  
  AuxTools auxTools; 
  
};

#endif
