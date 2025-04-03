#!/usr/bin/env python

import os
import math
import subprocess
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import CoolProp.CoolProp as CP

#----------------------------------------- REFPROP ---------------------------------------------#

CP.set_config_string(CP.ALTERNATIVE_REFPROP_PATH, '~/Software/REFPROP/REFPROP-cmake/build')
# To activates the GERG 2008
# CP.set_config_bool(CP.REFPROP_USE_GERG, True)

#-----------------------------------------INPUT_SPACE ---------------------------------------------#

bash_code = '''
if [ -d "TP_1" ]; then
    rm -r "TP_1"
fi
mkdir "TP_1"
'''
subprocess.call(bash_code, shell=True)

specie      = "N2"
temperature = [300]
pressure    = [100, 120, 140, 160, 180, 200]
block       = 5
sim         = 2

#----------------------------------------  Functions -------------------------------------------# 

def avg(array):
    sum_of_array = sum(array)
    number_of_elements = len(array)

    try:
        average = sum_of_array / number_of_elements
    except ZeroDivisionError:
        average = float('nan')

    return average

def sd(array):
    mean = sum(array) / len(array)
    squared_mean = mean ** 2
    squared_elements = []
    for element in array:
        squared_element = element ** 2
        squared_elements.append(squared_element)
    variance = sum(squared_elements) / len(array)
    standard_deviation = math.sqrt(variance - squared_mean)
    return standard_deviation

#----------------------------------------  MAIN LOOP -------------------------------------------# 

for T in temperature:
    
    for P in pressure:
        
        Dens1_b   = []
        density_RP  = round(CP.PropsSI('D', 'T',T, 'P', P*1e5, specie),6)
        
        for i in range(1, block + 1):
            
            Dens1_s   = []
            
            for j in range(1, sim + 1):
                
                fold = f"T_{T}_1/T_{T}_P_{P}/block_{i}/sim_{j}"
                os.chdir(fold)
                
                if os.path.exists(r'density.dat'):
                    
                    try:
                        
                        dens_files = np.loadtxt(r'density.dat', skiprows=2)
                        dens_array= np.array(dens_files)
                        density_coloumn = dens_array[0:,1]
                        density1 = np.mean(density_coloumn)
                        Dens1_s.append(density1)
                        
                        print('#########################################################')
                        print('Temperature :', T)
                        print('Pressure :', P)
                        print('Density [MD-1]          = ' + str(density1*1000) + ' Kg/m3')
                        print('Density [REFPROP]     = ' + str(density_RP) + ' Kg/m3')
                        print('#########################################################')
                        print('\n')
                        
                        os.chdir("../../../../")
                        print(os.getcwd())

                    except FileNotFoundError:
                            
                        print("density.dat file does not exists")
                            
                else:
                    print("File does not exist at", fold)
                    os.chdir("../../../../")
            
            if len(Dens1_s) > 0:
                
                avgs_Den1 = avg(Dens1_s)
                Dens1_b.append(avgs_Den1)
                
            else:
                print("The SIM array is empty.")
                
        if len(Dens1_b) > 0:
            
            avgb_Den1 = round(avg(Dens1_b)*1000,4)
            sd_Den1 = round(sd(Dens1_b)*1000,6)

            
            file_properties = f"TP_1/Density_{T}.dat"
            file_sd = f"TP_1/SD_Density_{T}.dat"            
            
            if not os.path.isfile(file_properties):
                with open(file_properties, "w") as file:
                    file.write("Pressure Density1 [Kg/m3] Density_REFPROP [Kg/m3]\n")
                    file.write(f"{P} {avgb_Den1} {density_RP}\n")
            else:
                with open(file_properties, "a") as file:
                    file.write(f"{P} {avgb_Den1} {density_RP}\n")

            if not os.path.isfile(file_sd):
                with open(file_sd, "w") as file:
                    file.write("Pressure SD_Density1\n")
                    file.write(f"{P} {sd_Den1}\n")
            else:
                with open(file_sd, "a") as file:
                    file.write(f"{P} {sd_Den1}\n")
        else:
            print("The BLOCK array is empty.")

# end of program  