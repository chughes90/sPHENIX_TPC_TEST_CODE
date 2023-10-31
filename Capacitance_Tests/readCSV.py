#!/usr/bin/python3

from ROOT import TGraph, TCanvas, TF1, TH1F, TLegend
from ROOT import gROOT, gBenchmark

#gBenchmark.Start( 'fit1' )

from array import array

import pandas as pd
import operator

NFiles = 7
c = [TCanvas() for i in range(NFiles)]
gr = [TGraph() for i in range(NFiles)]
e_fit = [TF1() for i in range(NFiles)]
slope = []
for w in range(NFiles):
 
    # reading the CSV file
    df = pd.read_csv('./Data/scopeData-{}.csv'.format(w+1))

    #print(df.head())

    # displaying the contents of the CSV file
    #print(df[' OUT1'])

    input = df[' IN1']
    print(input)
    max_index, max_value = max(enumerate(input), key=operator.itemgetter(1))
    print(max_index)
    amplitude = input[max_index:max_index+150]
    if w in [1,3,5,7]:
        amplitude/=5
    print(amplitude)
    time = df['TIME ms'][max_index:max_index+150]
    time = array('d', -time)
    #t = min(time)
    #time = [x - t for x in time]
    print(time)
    e_fit[w] = TF1( 'e1', '[Constant]*exp([Slope]*x)+[Bias]',  min(time),  max(time) )
    e_fit[w].SetParameters(-1.01345, 3.32519, -0.0203828)

    gr[w] = TGraph( len(time), array('d', time), array('d', amplitude ) )
    c[w] = TCanvas( 'c{}'.format(w), 'The Fit Canvas {}'.format(w), 200, 10, 700, 500 )

    gr[w].SetMarkerColor(2)
    gr[w].SetLineColor(2)

    gr[w].Draw( 'ACP' )
    gr[w].Fit(e_fit[w],"R+")

    par1 = e1.GetParameters()
    print("PRINT par1:")
    print(par1[0]) #Bias
    print(par1[1]) #Constant
    print(par1[2]) #Slope

    e_fit[w].SetParameters( par1 )
    gr[w].Fit(e_fit[w],"R+")
    par2 = e_fit[w].GetParameters()
    slope.append(par2[2])
    print('C = ',1.0/par2[2]*1e-3*1/(2.25*1e6)*1e9, ' nF')
    #c[w].Update()

print(slope)
#DAWING
h = TH1F("h","h;T [ms];V",1000,-100,100)
title = [
    'GEM 1',
    'Trans 1',
    'GEM 2',
    'Trans 2',
    'GEM 3',
    'Trans 3',
    'GEM 4',
         ]
col = [1,2,4,7,6,1,2]
mark = [20,20,20,20,20,24,24]

c = TCanvas( 'c', 'The Canvas ', 800, 600 )
c.GetPad(0).SetLogx()

h.Draw('AXIS')
h  .GetXaxis().SetRangeUser(1e-6,250)
h  .GetYaxis().SetRangeUser(-2,4)

leg  =TLegend(0.5,0.6,0.8,0.9,"","brNDC")
leg  .SetFillStyle(0)
leg  .SetTextSize(0.04)
leg  .SetTextAlign(12)
leg  .SetBorderSize(0)
leg  .SetTextFont(42)

for ig,g in enumerate(gr):
    g.SetMarkerStyle(mark[ig])
    g.SetMarkerColor(col[ig])
    g.SetLineColor(col[ig])
    g.Draw('Psame')

    R = 2.25
    #if ig>4:
    #    R=22.25
    leg  .AddEntry(g  ,title[ig]+' {:.4f} nF'.format(1.0/slope[ig]*1e-3*1/(R*1e6)*1e9),"p");	    

leg  .Draw()
#gBenchmark.Show( 'fit1' )
