import matplotlib.pyplot as plot
import sys
import redpitaya_scpi as scpi
import numpy as np
from time import sleep
import time









#Setup the connection to the Red Pitaya
#rp_s = scpi.scpi(sys.argv[1])
IP = sys.argv[1]
rp_s = scpi.scpi(IP)

#Set the parameters for the signal generator
wave_form = 'SQUARE'
# wave_form = 'SINUS'
freq = 3 #2000
ampl = 0.9
#Decimation factor
#Decimation (1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096, 8192, 16384, 32768, 65536)
dec = 2048 #32

#Generate the signal
def set_generator(waveform, frequency, amplitude, offset):
    rp_s.tx_txt('GEN:RST')
    rp_s.tx_txt('SOUR1:FUNC ' + str(waveform).upper())
    rp_s.tx_txt('SOUR1:FREQ:FIX ' + str(frequency))
    rp_s.tx_txt('SOUR1:VOLT ' + str(amplitude))
    rp_s.tx_txt('SOUR1:VOLT:OFFS ' + str(offset))
    rp_s.tx_txt('OUTPUT1:STATE ON')
    rp_s.tx_txt('SOUR1:TRIG:INT')

# Generate 
#set_generator(wave_form, freq, ampl, 0)
#sleep(1)


#Define a function to sample the oscilloscope
def sample_oscilloscope():
    #Set the parameters for the acquisition
    rp_s.tx_txt('ACQ:RST')
    rp_s.tx_txt('ACQ:DATA:FORMAT ASCII')
    rp_s.tx_txt('ACQ:DATA:UNITS VOLTS')
    rp_s.tx_txt(f'ACQ:DEC {dec}')
    #rp_s.tx_txt('ACQ:SOUR1:GAIN HV')
    rp_s.tx_txt(f'ACQ:TRIG:LEV {0.5*ampl}')
    rp_s.tx_txt('ACQ:TRIG CH1_PE')
    rp_s.tx_txt('ACQ:START')
    #sleep(1)

    #Wait for the acquisition to finish
    while 1:
        rp_s.tx_txt('ACQ:TRIG:STAT?')
        if rp_s.rx_txt() == 'TD':
            break
    #Read the data from the acquisition
    rp_s.tx_txt('ACQ:SOUR1:DATA?')
    #print('Reading data...')
    #rp_s.tx_txt('ACQ:SOUR1:DATA:STA:N? 0,1000')
    buff_string = rp_s.rx_txt()
    #print('Done reading data!') 

    #Convert the data to a list of floats
    buff_string = buff_string.strip('{}\n\r').replace("  ", "").split(',')
    buff = list(map(float, buff_string))

    return buff

# Get data
buff = sample_oscilloscope()
#print( len(buff) )
#buff_1 = sample_oscilloscope()
#buff_2 = sample_oscilloscope()
#Plot the data
plot.plot(buff)
plot.ylabel('Voltage')
plot.show()