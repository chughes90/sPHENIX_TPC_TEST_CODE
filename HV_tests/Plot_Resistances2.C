 //plot the resistances and currents as a function of voltages and save the TH1F to a root file
 
#include <iostream>
#include <chrono>
#include <ctime> 
#include <string>
#include <sstream>
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

  //initialize a file to save in a directory 1 under the current one called ROOT_FILES

  //first get a timestamp and cast as string
  auto ts = std::chrono::system_clock::now();
  std::time_t start_time = std::chrono::system_clock::to_time_t(ts);
  std::stringstream ss;
  ss << start_time;
  std::string time_stamp = ss.str();

  //then add timpestamp to file name
  char file_name[256];
  sprintf(file_name,"ROOT_FILES/%s_RESISTOR_TEST.root",time_stamp.c_str());
  std::unique_ptr<TFile> outputfile( TFile::Open( file_name, "RECREATE" ) );	

  // we will always have 31 points
  int n_points=(argc-1)/3; 
 
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
    voltages[counter] = TMath::Abs(std::stof(argv[i]));
    currents[counter] = TMath::Abs(std::stof(argv[i+1]));
    resistances[counter] = TMath::Abs(std::stof(argv[i+2]));

    // If you have a resistance > 1000 MOhm (1 GOhm), set it to 1000 MOhm
    if(resistances[counter] > 1000){resistances[counter] = 1000;}

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
  resistances_vs_volt->GetHistogram()->SetMaximum(1.2*max_res);
 
  resistances_vs_volt->Draw("AC*");

  resistances_vs_volt->Write();

  app.Run();
 
  return 0;
 
}
