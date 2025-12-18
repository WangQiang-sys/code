void readH(TGraph* gh);
void Calculated_Irradiation_Time()
{
   
   TGraph* gh = new TGraph();
   readH(gh);
//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......

   double Ep;
   cout << "Please input Ep(MeV) " << endl;
   cin >> Ep;

   double cross_section = gh->Eval(Ep);

// cout << "-----------------------------------------------------------------" << endl;
   cout << "Ep = " << Ep << " MeV" << " 51V(p,n)51Cr reaction cross section is " << cross_section << " b "<< endl;
// cout << "-----------------------------------------------------------------" << endl;

   double Ie;
   cout << "Please input Ie(nA) " << endl;
   cin >> Ie;


   const double D = 100e-6;//Target thickness ug/cm2
   const double A = 51;//Mass number of 51V
   const double Na = 6.02214076e23;// 阿伏伽德罗常数
   const double e = 1.602176634e-19; // Electron charge
   const double Ne = 1;//the charge number of each particle
   const double C1= 1.0e-24;//b to cm2
   const double C2= 1.0e-9;//nA to A

   double N = (cross_section * C1 * Ie * C2 * D * Na)/(e * Ne * A);

// cout << "-------------------------------------------------------------------------" << endl;
   cout << "Number of neutrons produced per unit time in the reaction 51(p,n)51Cr " <<endl;
   cout << N << endl;
// cout << "-------------------------------------------------------------------------" << endl;

//The unit of time is hour 

   const double Lambda = 0.693/(27.7*24);
   const double B = 0.0991;                      //320 keV gamma ray branching ratio
   const double Efficient = 0.3;                 //320 keV gamma ray Efficient
   const double Nr = 10000;                      //The gamma ray number of detected
   const double P = N*3600;                      //The number of 51V generated per hours
   const double tw = 0;     //The waiting time between the end of irradiation and the beginning of measurement
   const double ti = 3;     //The irradiation time

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......

   double tc = -(1/Lambda) * log(1-(Nr * Lambda * exp(Lambda * tw))/(P * (1-exp(-Lambda * ti)) * B * Efficient));
   // double ti = -log(1-(Lambda * Nr * exp(Lambda * tw))/(P * B * Efficient *(1-exp(-Lambda * tc))))/Lambda;
   cout << "----------------------------------------------------------------------" << endl;
   cout << "When gamma number Nr = " << Nr << " is detected, the measuring time is required"<< endl;
   cout << "tc is " << tc << endl;
   cout << "----------------------------------------------------------------------" << endl;

}

void readH(TGraph* g)
{
   // TCanvas *c = new TCanvas();
    g->SetName("51V(p,n)51Cr");
    g->SetTitle("51V(p,n)51Cr reaction cross section;Energy (MeV);Cross section (b)");

    // Open data file
    ifstream inf("51Vpn51Cr.txt", ios::in);
    if (!inf.is_open()) {
        cout << "Data file does not exist!" << endl;
        return; 
    }

    double e, cs;  // e: energy, cs: cross section
    int i = 0;
    
    // Read data and fill into TGraph
    while (inf >> e >> cs) {
        g->SetPoint(i++, e, cs);
    }
    
    // Draw the graph
   //  c->cd();
   //  g->SetLineColor(2);   // Set line color to red
   //  g->SetMarkerColor(2);  // Set marker color to red
   //  g->Draw("AC*");
   //  g->GetXaxis()->SetRangeUser(0, 2.5); // Optional: set x-axis range
   //  c->Draw();

}





   



