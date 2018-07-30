#define ScopePSD_cxx
#include "ScopePSD.h"
#include <TH2.h>
#include <TStyle.h>
#include <TCanvas.h>

void ScopePSD::Loop()
{
//   In a ROOT session, you can do:
//      Root > .L ScopePSD.C
//      Root > ScopePSD t
//      Root > t.GetEntry(12); // Fill t data members with entry number 12
//      Root > t.Show();       // Show values of entry 12
//      Root > t.Show(16);     // Read and show values of entry 16
//      Root > t.Loop();       // Loop on all entries
//

//     This is the loop skeleton where:
//    jentry is the global entry number in the chain
//    ientry is the entry number in the current Tree
//  Note that the argument to GetEntry must be:
//    jentry for TChain::GetEntry
//    ientry for TTree::GetEntry and TBranch::GetEntry
//
//       To read only selected branches, Insert statements like:
// METHOD1:
//    fChain->SetBranchStatus("*",0);  // disable all branches
//    fChain->SetBranchStatus("branchname",1);  // activate branchname
// METHOD2: replace line
//    fChain->GetEntry(jentry);       //read all branches
//by  b_branchname->GetEntry(ientry); //read only this branch
   if (fChain == 0) return;

   Long64_t nentries = fChain->GetEntriesFast();

   Long64_t nbytes = 0, nb = 0;
   for (Long64_t jentry=0; jentry<nentries;jentry++) {
      Long64_t ientry = LoadTree(jentry);
      if (ientry < 0) break;
      nb = fChain->GetEntry(jentry);   nbytes += nb;
      fDelay = 100;

      CalcPSD(Ch1_amplitude,Ch1_QDC,Ch1_PSD);
      CalcPSD(Ch2_amplitude,Ch2_QDC,Ch2_PSD);
      
      Ch1_PSDh->Fill(Ch1_QDC, Ch1_PSD);
      Ch2_PSDh->Fill(Ch2_QDC, Ch2_PSD);

      outTree->Fill();
      // if (Cut(ientry) < 0) continue;
   }
   outFile->Write();
   TCanvas *C1 = new TCanvas();
   C1->Divide(2,1);
   C1->cd(1);
   Ch1_PSDh->Draw("colz");
   C1->cd(2);
   Ch2_PSDh->Draw("colz");
   
}
