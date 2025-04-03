#!/usr/bin/env python

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

energy = [5, 6, 7, 8]
plt.style.use('fivethirtyeight')

for E in energy:
    data = pd.read_csv(f'../TP/Density_{E}.dat', delimiter=' ')
    # print(data)
    x = data.iloc[:, 0]
    y_MD = data.iloc[:, 1]
    y_RF = data.iloc[:, 2]

    plt.cla()
    plt.plot(x,y_MD,label='MD')
    plt.plot(x,y_RF,label='REFPROP')
    plt.legend(loc="upper left")
    plt.xlabel('Pressure [bar]')
    plt.ylabel('Density [kg/m$^3$]')
    plt.tight_layout()
    plt.savefig(f"density_{E}.png")
