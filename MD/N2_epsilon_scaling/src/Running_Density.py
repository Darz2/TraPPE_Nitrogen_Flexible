#!/usr/bin/env python

import CoolProp.CoolProp as CP
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

plt.style.use('fivethirtyeight')
CP.set_config_string(CP.ALTERNATIVE_REFPROP_PATH, f'~/Software/REFPROP/REFPROP-cmake/build')

Temperature = T_VAL
Pressure = P_VAL
specie = ["MOLECULE_DEF"]

Density_RP = CP.PropsSI('D', 'T',Temperature, 'P', Pressure*1e5, specie[0])
Thermal_Conductivity_RP = CP.PropsSI('L', 'T',Temperature, 'P', Pressure*1e5, specie[0])

# print(Density_RP)
# print(Thermal_Conductivity_RP*1000) # in mW/m-K


data = pd.read_csv('density.dat',skiprows=1, delimiter=' ')
x = data['#']*1e-6
y = data['TimeStep']*1000
Mean_Density = np.mean(y)
plt.cla()
plt.xlabel('Time [ns]')
plt.ylabel('Density [kg/m$^3$]')
plt.title("DENSITY")
plt.axhline(y=Density_RP,linestyle='-', alpha = 0.5, color='r', label="REFPROP")
plt.axhline(y=Mean_Density,linestyle='-', color='g', label= 'MD (Running Mean)')
plt.plot(x,y,label='MD (instantaneous)')
plt.legend(loc="upper right")
plt.tight_layout()
plt.savefig("density.png")