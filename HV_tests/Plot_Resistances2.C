 //plot the resistances and currents as a function of voltages and save the TH1F to a root file
 
#include <iostream>
#include <TFile.h>
#include <TH1.h>
#include <TH2.h>
#include <TH3.h>
#include <TVector3.h>
#include <TNtuple.h>
#include <TApplication.h>
#include <TGraph.h>
#include <numeric>
#include <iostream>
using namespace std;
 
int main(int argc, char *argv[])
{
 
  //initialize a TApplication for on-the-fly plotting
  TApplication app("Root app", &argc, argv);

  int n_points=(argc-1)/3; // we will always have 31 points
 
  //initialize arays of floats
  float voltages[n_points]={0};
  float currents[n_points]={0};
  float resistances[n_points]={0};
 
  char Plot_Title[256];
  sprintf(Plot_Title,"Resistance vs. Voltage, Module: %s","RESISTOR_TEST");
 
  //loop over the things and fill arrays
  int counter=0;
 
  //for determinging the maximum resistance
  float max_res=0;
 
  for (int i = 1; i <= (argc-3); i+=3)
  {
    voltages[counter] = -1*std::stof(argv[i]);
    currents[counter] = -1*std::stof(argv[i+1]);
    resistances[counter] = std::stof(argv[i+2]);
 
    if(resistances[counter] > max_res){max_res = resistances[counter];}
 
    counter++;
  }
 
 
  //plot the resistance vs voltage
  //auto currents_vs_volt = new TGraph(n_points,voltages,currents);
  auto resistances_vs_volt = new TGraph(n_points,voltages,resistances);
  resistances_vs_volt->SetTitle("Plot_Title;Voltage [V]; Effective Resistance [MOhm]");
  resistances_vs_volt->SetNameTitle("resistances_vs_volt",Plot_Title);
 
  //set y-axis minimum of TGraph to 0 and maximum to max_res + 2
  resistances_vs_volt->GetHistogram()->SetMinimum(0.0);
  resistances_vs_volt->GetHistogram()->SetMaximum(max_res+2);
 
  resistances_vs_volt->Draw("AC*");
 
  app.Run();
 
  return 0;
 
}
