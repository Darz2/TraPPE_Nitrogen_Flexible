#!/usr/bin/env python

import sys
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
CP.set_config_bool(CP.REFPROP_USE_GERG, True)

#-----------------------------------------INPUT_SPACE ---------------------------------------------#

bash_code = '''
if [ -d "TP" ]; then
    rm -r "TP"
fi
mkdir "TP"
'''
subprocess.call(bash_code, shell=True)

specie      = "N2"
directories = [5, 6, 7, 8]
temperature = [300]
pressure    = [120, 140, 160, 180 , 200]

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

for D in directories:
    for T in temperature:
        for P in pressure:
            
            Dens1_b   = []
            density_RP  = round(CP.PropsSI('D', 'T',T, 'P', P*1e5, specie),4)                
            fold = f"N2_TRAPPE_FLEX-{D}/T_{T}_P_{P}"
            os.chdir(fold)
            
            if os.path.exists(r'density.dat'):
                
                try:
                    
                    dens_files = np.loadtxt(r'density.dat', skiprows=2)
                    dens_array= np.array(dens_files)
                    density_coloumn = dens_array[0:,1]
                    density1 = np.mean(density_coloumn)
                    density1 = round(density1*1000,4)
                    
                    print('#########################################################')
                    print('Temperature :', T)
                    print('Pressure :', P)
                    print('Density [MD-1]          = ' + str(density1) + ' Kg/m3')
                    print('Density [REFPROP]     = ' + str(density_RP) + ' Kg/m3')
                    print('#########################################################')
                    print('\n')
                    
                    os.chdir("../../")
                    print(os.getcwd())

                except FileNotFoundError:
                        
                    print("density.dat file does not exists")
                        
            else:
                print("File does not exist at", fold)
                os.chdir("../../")
                
            file_properties = f"TP/Density_{D}.dat"
            
            if not os.path.isfile(file_properties):
                with open(file_properties, "w") as file:
                    file.write("Pressure Density1 [Kg/m3] Density_REFPROP [Kg/m3]\n")
                    file.write(f"{P} {density1} {density_RP}\n")
            else:
                with open(file_properties, "a") as file:
                    file.write(f"{P} {density1} {density_RP}\n")

# end of program  