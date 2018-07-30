//////////////////////////////////////////////////////////
// This class has been automatically generated on
// Fri Jul 27 11:47:31 2018 by ROOT version 5.34/30
// from TTree T/a TTree with Traces recorded with a Textronix scope
// found on file: NoOpAmp_Cf_EJ276_5in_Teflon_CH1PMT_CH2SiPM.root
//////////////////////////////////////////////////////////

#ifndef ScopePSD_h
#define ScopePSD_h

#include <TROOT.h>
#include <TChain.h>
#include <TFile.h>
#include <iostream>
//#include <stdlib>
#include <vector>
#include <TH2F.h>
#include <TTree.h>
#include <TFile.h>
//#include <../ROOTSCOPE-master/myROOTSCOPE_lite.C>

// Header file for the classes stored in the TTree if any.
#include <vector>

using namespace std;

// Fixed size dimensions of array or collections stored in the TTree if any.

class ScopePSD {
public :
TTree          *fChain;   //!pointer to the analyzed TTree or TChain
Int_t           fCurrent; //!current Tree number in a TChain

// Declare private variables
Int_t fDelay;
TH2F *Ch1_PSDh;
TH2F *Ch2_PSDh;

 TTree *outTree;
 TFile *outFile;

   // Declaration of leaf types
   vector<double>  *Ch1_time;
   vector<double>  *Ch1_amplitude;
   vector<double>  *Ch2_time;
   vector<double>  *Ch2_amplitude;

   Double_t Ch1_QDC;
   Double_t Ch1_PSD;
   Double_t Ch2_QDC;
   Double_t Ch2_PSD;

   //ROOTSCOPE *app;

   // List of branches
   TBranch        *b_Ch1_time;   //!
   TBranch        *b_Ch1_amplitude;   //!
   TBranch        *b_Ch2_time;   //!
   TBranch        *b_Ch2_amplitude;   //!

   ScopePSD(TTree *tree=0);
   virtual ~ScopePSD();
   virtual Int_t    Cut(Long64_t entry);
   virtual Int_t    GetEntry(Long64_t entry);
   virtual Long64_t LoadTree(Long64_t entry);
   virtual void     Init(TTree *tree);
   virtual void     Loop();
   virtual Bool_t   Notify();
   virtual void     Show(Long64_t entry = -1);

   // Delcare Functions
int CalcPSD(vector<double> *trace, Double_t &fullArea, Double_t &PSD);
};
#endif

#ifdef ScopePSD_cxx
ScopePSD::ScopePSD(TTree *tree) : fChain(0) 
{
// if parameter tree is not specified (or zero), connect the file
// used to generate this class and read the Tree.
   if (tree == 0) {
      TFile *f = (TFile*)gROOT->GetListOfFiles()->FindObject("NoOpAmp_Cf_EJ276_5in_Teflon_CH1PMT_CH2SiPM.root");
      if (!f || !f->IsOpen()) {
         f = new TFile("NoOpAmp_Cf_EJ276_5in_Teflon_CH1PMT_CH2SiPM.root");
      }
      f->GetObject("T",tree);

   }
   Init(tree);
fDelay = 0.0;
//app = new ROOTSCOPE(gClient->GetRoot());
 outFile = new TFile("Test.root","recreate");
 outTree = new TTree("PSD_TREE","Contains the PSD of Channel 1 and 2");
Ch1_PSDh = new TH2F("Ch1", "Ch1 PSD Histogram",2000,0,100,2000,0,100);
Ch2_PSDh = new TH2F("Ch2", "Ch2 PSD Histogram",2000,0,100,2000,0,100);
 Ch1_QDC = 0;
 Ch1_PSD = 0;
 Ch2_QDC = 0;
 Ch2_PSD = 0;

 //app->AddHisto(Ch1_PSD);
 //app->AddHisto(Ch1_QDC);
 //app->AddHisto(Ch2_PSD);
 //app->AddHisto(Ch2_QDC);
 
 outTree->Branch("Ch1_QDC",&Ch1_QDC,"QDC1/D");
 outTree->Branch("Ch1_PSD",&Ch1_PSD,"PSD1/D");
 outTree->Branch("Ch2_QDC",&Ch2_QDC,"QDC2/D");
 outTree->Branch("Ch2_PSD",&Ch2_PSD,"PSD2/D");
}

ScopePSD::~ScopePSD()
{
   if (!fChain) return;
   delete fChain->GetCurrentFile();
}

Int_t ScopePSD::GetEntry(Long64_t entry)
{
// Read contents of entry.
   if (!fChain) return 0;
   return fChain->GetEntry(entry);
}
Long64_t ScopePSD::LoadTree(Long64_t entry)
{
// Set the environment to read one entry
   if (!fChain) return -5;
   Long64_t centry = fChain->LoadTree(entry);
   if (centry < 0) return centry;
   if (fChain->GetTreeNumber() != fCurrent) {
      fCurrent = fChain->GetTreeNumber();
      Notify();
   }
   return centry;
}

void ScopePSD::Init(TTree *tree)
{
   // The Init() function is called when the selector needs to initialize
   // a new tree or chain. Typically here the branch addresses and branch
   // pointers of the tree will be set.
   // It is normally not necessary to make changes to the generated
   // code, but the routine can be extended by the user if needed.
   // Init() will be called many times when running on PROOF
   // (once per file to be processed).

   // Set object pointer
   Ch1_time = 0;
   Ch1_amplitude = 0;
   Ch2_time = 0;
   Ch2_amplitude = 0;
   // Set branch addresses and branch pointers
   if (!tree) return;
   fChain = tree;
   fCurrent = -1;
   fChain->SetMakeClass(1);

   fChain->SetBranchAddress("Ch1.time", &Ch1_time, &b_Ch1_time);
   fChain->SetBranchAddress("Ch1.amplitude", &Ch1_amplitude, &b_Ch1_amplitude);
   fChain->SetBranchAddress("Ch2.time", &Ch2_time, &b_Ch2_time);
   fChain->SetBranchAddress("Ch2.amplitude", &Ch2_amplitude, &b_Ch2_amplitude);
   Notify();
}

Bool_t ScopePSD::Notify()
{
   // The Notify() function is called when a new file is opened. This
   // can be either for a new TTree in a TChain or when when a new TTree
   // is started when using PROOF. It is normally not necessary to make changes
   // to the generated code, but the routine can be extended by the
   // user if needed. The return value is currently not used.

   return kTRUE;
}

void ScopePSD::Show(Long64_t entry)
{
// Print contents of entry.
// If entry is not specified, print current entry
   if (!fChain) return;
   fChain->Show(entry);
}
Int_t ScopePSD::Cut(Long64_t entry)
{
// This function may be called from Loop.
// returns  1 if entry is accepted.
// returns -1 otherwise.
   return 1;
}

    int ScopePSD::CalcPSD(vector<double> *trace, Double_t &fullArea, Double_t &PSD){
  //Calculates the PSD ratio of the trace

  //Declare Variables
  int sze = trace->size();
  fullArea = 0.0;
  Double_t tailArea = 0.0;
  PSD = 0.0;
  int maxPoint = 0;

  //Find full area & max point
  for (int i = 0; i < sze; i++){
    fullArea -= trace->at(i);
    if (trace->at(i) >= maxPoint){
      maxPoint = -trace->at(i);
    }
  }  
  
  if (fDelay + maxPoint >= sze){
    cout << "fDelay is larger than the size of the trace";
    return -1;
  }

  for (int i = fDelay + maxPoint; i < sze; i++){
    tailArea -= trace->at(i);
  }

  PSD = tailArea / fullArea;
  
  //cout << "Tail Area = " << tailArea << "\nFull Area = " << fullArea << "\nPSD = " << PSD << endl;
  return 0;
  
}
 
#endif // #ifdef ScopePSD_cxx
