#!/bin/bash
# 
#
 
#dVs: G1T, G1B, G2T, G2B, G3T, G3B, G4T, G4B
 
dV_arr=(301 1179 371 1179 495 30 555 590) 
 
#Loop through all channels
card=100
#for (( i=1; i<9; i++ ))
for (( i=8; i<9; i++ ))
do
  read -p "Which module are you testing?" module_readback
  module="$module_readback"
  pos=$(( $i ))
  read -p "Move SHV cable to Position $pos. Have you done that: true/false ?" move
 
  while [ $move != "true" ]
  do
    echo "CAN NOT PROCEED UNTIL YOU HAVE MOVED SHV CABLE TO PROPER POSITION $pos." 
    read -p "HAVE YOU MOVED CABLE SHV CABLE TO POSITION $pos: true/false ?" move
  done
  
  #assume we are using channel 8 in Eric's crate

  index=$(( $card + 8 ))
  
  #get a 10% increment
  
  increment=$(( ${dV_arr[$i-1]} / 10 ))
  
  #empty arrays for filling with ALL STRINGS
  arr=()
  
  #Set voltage of channel in 10 % increments 
  for (( j=1; j<11; j++  ))
  do
 
    #determine the set voltage
    v_set=$(( $increment * $j ))
    echo "snmpset -Oqv -v 2c -m +WIENER-CRATE-MIB -c guru $AUX_IP outputVoltage.u$index F $v_set"
 
    #set the set voltage
    snmpset -Oqv -v 2c -m +WIENER-CRATE-MIB -c guru $AUX_IP outputVoltage.u$index F $v_set
    sleep 5

    #stability criterion
    # STABLE: Lo = "80 01 C0" Hi = "80 01 80" OF = "00 01 40"
    # UNSTABLE: ANYTHING ELSE
    #echo "snmpget -Oqv -v 2c -m +WIENER-CRATE-MIB -c guru $AUX_IP outputStatus.u$index"
    stable="false"
 
    while [ $stable != "true"  ]
    do
      status_code="$(snmpget -Oqv -v 2c -m +WIENER-CRATE-MIB -c guru $AUX_IP outputStatus.u$index)"
      #echo "$status_code"
      if [[ $status_code = *"80 01 C0"* ]] || [[ $status_code = *"80 01 80"* ]] || [[ $status_code = *"00 01 40"* ]]
      then
        stable="true"
        #echo $stable
      fi
    done
 
    sleep 5
 
    #readback the Voltage and Current
    #echo "snmpget -Oqv -v 2c -m +WIENER-CRATE-MIB -c guru $AUX_IP outputTerminalVoltage.u$index"
    #echo "snmpget -Op +020.12 -0qv 2c -m +WIENER-CRATE-MIB -c guru $AUX_IP outputMeasurementCurrent.u$index"
 
    v_meas_str=" $(snmpget -Oqv -v 2c -m +WIENER-CRATE-MIB -c guru $AUX_IP outputMeasurementTerminalVoltage.u$index)"
    i_meas_str=" $(snmpget -Op +020.12 -Oqv -v 2c -m +WIENER-CRATE-MIB -c guru $AUX_IP outputMeasurementCurrent.u$index)"

    #remove the +/- from the string
    v_meas_str=`echo $v_meas_str | cut -c 2-`
    i_meas_str=`echo $i_meas_str | cut -c 2-`

    #setting space as a delimiter, we know we just want everything before the space
    IFS=' ' read -ra ADDR_v<<<"$v_meas_str"
    read -ra ADDR_i<<<"$i_meas_str"
 
    #voltage/current values (no V or A)
    v_meas=${ADDR_v[0]}
    i_meas=${ADDR_i[0]}
  
    #volatge/current/resistance values as numbers
    r_meas=$( echo "$v_meas / $i_meas / 1000000" | bc -l )
    i_meas=$( echo "$i_meas * 1000000" | bc -l )

    printf "\n"
    echo "Voltage: $v_meas V,  Current: $i_meas uA,  Resistance: $r_meas MOhm" 
    printf "\n"
  
    #store the voltages, current, and resistance in an array to be passed to ROOT
    arr+=($v_meas)
    arr+=($i_meas)
    arr+=($r_meas)
  done

  #zero all the channels before moving on to next one
 
  for (( i=0; i<16; i++ ))
  do
    index=$(( $card + $i ))
    #Set voltage of channel at the index to zero (performs a rampdown without setting the channel to "off")
    echo "snmpset -Oqv -v 2c -m +WIENER-CRATE-MIB -c guru $AUX_IP outputVoltage.u$index F 0"
    snmpset -Oqv -v 2c -m +WIENER-CRATE-MIB -c guru $AUX_IP outputVoltage.u$index F 0
  done

  #pass arrays to ROOT function to plot and save
  #root -b -l "Plot_Resistances.C(${volt_arr[@]},${curr_arr[@]},${resi_arr[@]},$module)"
 
  ./Plot_Resistances "${arr[@]}"
 
done


