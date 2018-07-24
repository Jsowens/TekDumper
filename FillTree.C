TTree *CreateTree(){

  fstream *in=new fstream("SINGLE_TEST_1.dat",ios::in);

  TTree *theTree=new TTree("T","a TTree with Traces recorded with a Textronix scope");
  vector<Double_t> Xvalues;
  vector<Double_t> Yvalues;
  theTree->Branch("time",&Xvalues);
  theTree->Branch("amplitude",&Yvalues);
  Int_t npoints=0;

  Char_t header[256];
  Double_t xincrement;
  Double_t time;
  Char_t *volts=new Char_t[23];
  Double_t voltage;

  Char_t header1[7];
  Char_t header2[14];


  Int_t nTraces=3;
  Int_t counter=0;
  in->get(header1,7);
  *in>>xincrement;
  //cout<<header1<<" "<<xincrement<<endl;
  in->get(header2,14);
  *in>>npoints;
  npoints = 9952;
  //cout<<header2<<" "<<npoints<<endl;

  while(!in->eof()){
  //while(counter<=nTraces){

    Xvalues.clear();
    Yvalues.clear();
   //in->getline(header,256);
    //cout<<header<<endl;
    //sscanf(header," %s %lf %s   %d,",header1,&xincrement,header2,&npoints);
    //cout<<header2<<" "<< npoints<<"\t"<<header2<<" "<<xincrement;
    //for(Int_t k=0;k<=npoints;k++){
    for(Int_t k=0;k<npoints;k++){
      in->getline(volts,23,',');
      voltage=atof(volts);
      time=xincrement*k;
      //if(k%10000==0)
      //cout<<k<<" "<<time<<" "<<voltage<<endl;
      Xvalues.push_back(time);
      Yvalues.push_back(voltage);
    }
    cout<<"# of points of the trace is: "<<Yvalues.size()<<endl;
    theTree->Fill();
    counter++;
    //break;
    
  }
cout<<counter<<" traces have been analyzed."<<endl;
  return theTree;
}


void Do(){

  TFile *fil=new TFile("test.root","recreate");
  TTree *T=CreateTree();
  T->Write();
  fil->Close();
}
