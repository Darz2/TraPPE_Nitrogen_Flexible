#!/usr/bin/env python

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

temperature = [300]
plt.style.use('fivethirtyeight')

def relative_deviation(array1, array2):
    array1, array2 = np.array(array1), np.array(array2)
    
    # Avoid division by zero
    with np.errstate(divide='ignore', invalid='ignore'):
        rel_dev = np.abs(array2 - array1) / np.abs(array1)
        rel_dev[np.abs(array1) == 0] = np.nan  # Set to NaN where division by zero occurs
    
    return rel_dev

for T in temperature:
    data = pd.read_csv(f'../TP/Density_{T}.dat', delimiter=' ')
    SD_data = pd.read_csv(f'../TP/SD_Density_{T}.dat', delimiter=' ')
    # print(data)
    x = data.iloc[:, 0]
    y_MD = data.iloc[:, 1]
    y_RF = data.iloc[:, 2]
    SD = SD_data.iloc[:,1]
    print(SD)

    plt.cla()
    plt.errorbar(x, y_MD, yerr=SD, label='MD', fmt='o', capsize=5)

    plt.plot(x,y_RF,label='REFPROP')
    plt.legend(loc="upper left")
    plt.xlabel('Pressure [bar]')
    plt.ylabel('Density [kg/m$^3$]')
    plt.tight_layout()
    plt.savefig(f"density_{T}_36.png")
    
    difference_1 = relative_deviation(y_RF, y_MD)
    print(difference_1*100)