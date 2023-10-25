# sPHENIX_TPC_TEST_CODE
Code for testing the capacitance, connectivity, HV holding, and resistance of HV modules in the sPHENIX TPC


**Capacitance_Tests**
- Contains code for to test the capacitance of the sPHENIX GEM/TGs 1x1
- Requires Red Pitaya + Test Cables
- Sends square wave pulse through GEM, measures RC constant from fit to response
- code lives on OPC0 machine at <insert path here>

**HV_Tests**
- Contains code for applying High Votlage in steps to sPHENIX GEM/TGs 1x1
- Requires Test Cables + ISEG Power Supply
- Ramps each GEM or TG up to its designed voltage in 10 steps, measures current and calculates resistance
- save the I vs V and R vs V curves to ROOT files
- code lives on OPC0 machine at /home/phnxrc/TPC/bin/TPC-mpod-utilities
- requires you to compile .C code: ```g++ -Wall -Wextra -o Plot_Resistances Plot_Resistances2.C `root-config --cflags --libs` ```
