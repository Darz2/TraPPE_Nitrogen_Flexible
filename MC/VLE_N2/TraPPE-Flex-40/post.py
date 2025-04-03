#!/usr/bin/env python

import os
import re
import sys
import math
import subprocess
import numpy as np
import pandas as pd

# Create the direcotries to store the thermophysical properties if already exist remove and create a new one 

bash_code = '''
if [ -d "TP" ]; then
    rm -r "TP"
fi
mkdir "TP"
'''

subprocess.call(bash_code, shell=True)
specie="N2"

# define the statistics parameter

block=5
sim=2

###################################################### MODIFICATION SPACE ##########################################

temperature = np.arange(80, 101, 10)
# temperature = np.arange(100, 111, 10)

# Function to calculate the average of the elements in the array

def avg(array):

  sum_of_array = sum(array)
  number_of_elements = len(array)
  average = sum_of_array / number_of_elements
  return average

# Function ot calculate the variance of the elements in the array

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

# start the looping for the temperatures

for T in temperature:

    density_box1_b =[]
    density_box2_b = []
    
    for i in range(1, block + 1):
        
        density_box1_s =[]
        density_box2_s = []
        
        for j in range(1, sim + 1):
            
            fold= f"{specie}/T_{T}/block_{i}/sim_{j}"
            
            print("Current Working Directory:", os.getcwd())
            print("Current Temperature:", T)
            print("Current Block:", i)
            print("Current sim:", j)
                    
            if os.path.exists(f"{fold}/sim.log"):
                
                # try:
                #     os.chdir(f'{fold}')
                #     result = subprocess.run(['grep', '-A', '2', 'Density', 'sim.log'], capture_output=True, text=True)
                #     lines = result.stdout.splitlines()

                # except subprocess.CalledProcessError as e:
                #     print("output not found in sim.log at", fold)
                #     exit(1)
            
                # else:
                    # print(lines)
                    
                    try:
                        
                        os.chdir(f'{fold}')
                        density_df = pd.read_csv("OUTPUT/av_density.dat",delim_whitespace=True, header=None, skiprows=1)
                        box1 = density_df.iloc[:, 1]
                        box2 = density_df.iloc[:, 2]
                        density_box1 = np.mean(box1)
                        density_box2 = np.mean(box2)
                        
                        # density_line = lines[1]
                        # density_box1 = float(density_line.split()[1])
                        # density_box2 = float(density_line.split()[2])
                        # print(density_box1)
                        # print(density_box2)
                        
                        density_box1_s.append(density_box1)
                        density_box2_s.append(density_box2)
                        os.chdir("../../../..")
                        
                    except IndexError:
                        print("ERROR", fold)
                        print("Current Working Directory:", os.getcwd())
                        os.chdir("../../../..")
                        continue
                    
                    # os.chdir("../../../..")
                    print("Current Working Directory:", os.getcwd())
            
            else:
                print("File does not exist at", fold)
                sys.exit() 
                
        avgs_density_box1 = avg(density_box1_s)
        avgs_density_box2 = avg(density_box2_s)
        
        density_box1_b.append(avgs_density_box1)        
        density_box2_b.append(avgs_density_box2)
        
    avgb_density_box1 = avg(density_box1_b)
    avgb_density_box2 = avg(density_box2_b)
    
    sd_density_box1 = sd(density_box1_b)
    sd_density_box2 = sd(density_box2_b)
    
    file_properties = f"TP/VLE.dat"
    file_sd         = f"TP/SD_VLE.dat"
    
    if not os.path.isfile(file_properties):  
        with open(file_properties, "w") as file: 
            file.write("Temperature Density_box1 Density_box2\n") 
            file.write(f"{T} {avgb_density_box1} {avgb_density_box2}\n") 
    else:
        with open(file_properties, "a") as file:  
            file.write(f"{T} {avgb_density_box1} {avgb_density_box2}\n") 
            
    if not os.path.isfile(file_sd): 
        with open(file_sd, "w") as file:  
            file.write("Pressure SD-Density_box1 SD_Density_box2\n") 
            file.write(f"{T} {sd_density_box1} {sd_density_box2}\n") 
    else:
        with open(file_sd, "a") as file: 
            file.write(f"{T} {sd_density_box1} {sd_density_box2}\n")    
    
    