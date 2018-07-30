
TTree *CreateTree(){

  fstream *in=new fstream("NoOpAmp_Cf_EJ276_5in_Teflon_CH1PMT_CH2SiPM_CH1_1.dat",ios::in);
  fstream *in2=new fstream("NoOpAmp_Cf_EJ276_5in_Teflon_CH1PMT_CH2SiPM_CH2_1.dat",ios::in);

  TTree *theTree=new TTree("T","a TTree with Traces recorded with a Textronix scope");
  vector<Double_t> Xvalues_1;
  vector<Double_t> Yvalues_1;
  vector<Double_t> Xvalues_2;
  vector<Double_t> Yvalues_2;
  //Ch2->Xvalues.push_back(0);
  theTree->Branch("Ch1.time",&Xvalues_1);
  theTree->Branch("Ch1.amplitude",&Yvalues_1);
  theTree->Branch("Ch2.time",&Xvalues_2);
  theTree->Branch("Ch2.amplitude",&Yvalues_2);
  Int_t npoints=0;

  Char_t header[256];
  Double_t xincrement;

  Double_t time;
  Char_t *volts=new Char_t[256];
  Char_t *volts2=new Char_t[256];
  Double_t voltage_1;
  Double_t voltage_2;

  Char_t header1[7];
  Char_t header2[14];


  Int_t nTraces=3;
  Int_t counter=0;
  in->get(header1,7);
  in2->get(header1,7);
  *in>>xincrement;
  *in2>>xincrement;
  cout<<header1<<" "<<xincrement<<endl;
  in->get(header2,14);
  in2->get(header2,14);
  *in>>npoints;
  *in2>>npoints;
  npoints = 9952;

  cout<<header2<<" "<<npoints<<endl;

  while(!in->eof()){
  //while(counter<=nTraces){

    Xvalues_1.clear();
    Yvalues_1.clear();
    Xvalues_2.clear();
    Yvalues_2.clear();
   //in->getline(header,256);
    //cout<<header<<endl;
    //sscanf(header," %s %lf %s   %d,",header1,&xincrement,header2,&npoints);
    //cout<<header2<<" "<< npoints<<"\t"<<header2<<" "<<xincrement;
    //for(Int_t k=0;k<=npoints;k++){
    for(Int_t k=0;k<npoints;k++){
      in->getline(volts,256,',');
      voltage_1=atof(volts);
      in2->getline(volts2,256,',');
      voltage_2=atof(volts2);
      time=xincrement*k;
      //if(k%10000==0)
      //cout<<k<<" "<<time<<" "<<voltage_2<<endl;
      Xvalues_1.push_back(time);
      Yvalues_1.push_back(voltage_1);
      Xvalues_2.push_back(time);
      Yvalues_2.push_back(voltage_2);      
    }
    //cout<<"# of points of the trace is: "<<Yvalues.size()<<endl;
    theTree->Fill();
    counter++;
    //break;
    
  }
cout<<counter<<" traces have been analyzed."<<endl;
  return theTree;
}


void Do(Char_t *filename){

  TFile *fil=new TFile(filename,"recreate");
  TTree *T=CreateTree();
  T->Write();
  fil->Close();
}
