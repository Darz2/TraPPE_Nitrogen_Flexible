#!/usr/bin/env python

#### import the packages ######################################################

import os
import numpy as np
import scienceplots
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.ticker import ScalarFormatter, MultipleLocator

marker_1 = 'o'       # List of markers
marker_2 = 'd'
plot_size = (4, 3)
graphic_font = 'Arial'
math_font = 'dejavuserif'  #['dejavusans', 'dejavuserif', 'cm', 'stix', 'stixsans', 'custom']
spine_width = 1
markersize=4
capsize=3
markeredgewidth=0.75
legend_linewidth = 1 #legend
linewidth =1 #color_line for plot
tick_width=0.75
tick_length=4
minor_tick_width= 0.5
minor_tick_length=2
tick_labelsize=10
legend_fontsize=8
legend_boxwidth=0.75
label_fontsize=12
borderaxespad=0.6
alpha = 1
CO2_color = '#e41a1c'
MIX_color = '#00ff01'
rgba_CO2_color = mcolors.to_rgba(CO2_color)
rgba_MIX_color = mcolors.to_rgba(MIX_color)
CO2_face_color = (rgba_CO2_color[0], rgba_CO2_color[1], rgba_CO2_color[2], 0.6)
MIX_face_color = (rgba_MIX_color[0], rgba_MIX_color[1], rgba_MIX_color[2], 0.6)
resolution_value = 1200
break_threshold = 10 # for NIST data
plt.rcParams['font.serif'] = graphic_font
plt.rcParams['mathtext.fontset'] = math_font


with plt.style.context([ 'ieee']):
    plt.rcParams['font.family'] = graphic_font
    plt.rcParams['mathtext.fontset'] = math_font
    # plt.rcParams['text.usetex'] = True
    fig, ax = plt.subplots(figsize=plot_size)

    ax.spines['top'].set_linewidth(spine_width)    # Top border
    ax.spines['bottom'].set_linewidth(spine_width) # Bottom border
    ax.spines['left'].set_linewidth(spine_width)   # Left border
    ax.spines['right'].set_linewidth(spine_width)  # Right border
    
    
    VLE_CO2_NIST = np.loadtxt('VLE_NIST.dat', delimiter='\t', skiprows=5)
    VLE_CO2_SIM = np.loadtxt('TP/VLE.dat', delimiter=' ', skiprows=1)
    VLE_CO2_SIM_SD = np.loadtxt('TP/SD_VLE.dat', delimiter=' ', skiprows=1)
    # print(VLE_CO2[0:,0])

    
    SIM_mix = plt.errorbar(VLE_CO2_SIM[:,1], VLE_CO2_SIM[:,0], xerr=VLE_CO2_SIM_SD[:,1],
        fmt=marker_1,
        markersize=markersize,
        markerfacecolor=MIX_face_color,
        markeredgecolor='g',
        markeredgewidth=markeredgewidth,
        linewidth= linewidth,
        capsize=capsize,
        capthick=capsize,
        color=MIX_color, 
        label=f"CFCMC Simulations \n(TraPPE-Flex)")
    
    SIM_mix = plt.errorbar(VLE_CO2_SIM[:,2], VLE_CO2_SIM[:,0], xerr=VLE_CO2_SIM_SD[:,2],
        fmt=marker_1,
        markersize=markersize,
        markerfacecolor=MIX_face_color,
        markeredgecolor="g",
        markeredgewidth=markeredgewidth,
        linewidth= linewidth,
        capsize=capsize,
        capthick=capsize,
        color=MIX_color)

    NIST_mix = plt.plot(VLE_CO2_NIST[0:,3], VLE_CO2_NIST[0:,0],                
        linestyle='solid',
        linewidth=linewidth,
        color='k',
        label=f"REFPROP")
    
    NIST_mix = plt.plot(VLE_CO2_NIST[0:,2], VLE_CO2_NIST[0:,0],                
        linestyle='solid',
        linewidth=linewidth,
        color='k')

    # plt.xlabel(r'$\rho$ / [10$^{3}$ kg m$^{-3}$]', fontsize=label_fontsize)
    plt.xlabel("Density / [Kg/m3]")
    plt.ylabel("Temperature /  [K]")
    # plt.title("VLE - CO$_2$")
    
    # ax.xaxis.set_major_locator(MultipleLocator(40))
    # ax.xaxis.set_minor_locator(MultipleLocator(10))
    # ax.yaxis.set_major_locator(MultipleLocator(0.1))
    # ax.yaxis.set_minor_locator(MultipleLocator(0.05))
    
    ax.tick_params(axis='both', which='major', direction='in', width=tick_width, length=tick_length, labelsize=tick_labelsize,
                bottom=True, top=True, left=True, right=True)
    ax.tick_params(axis='both', which='minor', direction='in', width=minor_tick_width, length=minor_tick_length,
                bottom=True, top=True, left=True, right=True)
        
    combined_legend = plt.legend(fontsize=legend_fontsize, loc=(0.2,0.075), ncol=1,borderaxespad=1)
    #outline1 = combined_legend.get_frame().set_alpha(0)
    outline = combined_legend.get_frame()
    outline.set_linewidth(legend_boxwidth)
    outline.set_edgecolor('black')

    output_dir = os.path.join(os.getcwd())
    file_name = f"VLE.jpg"
    file_path = os.path.join(output_dir, file_name)
    fig.savefig(file_path, dpi=resolution_value, bbox_inches='tight')
    fig.savefig(fr"{file_name}", dpi=resolution_value, bbox_inches='tight')
    
    output_dir = os.path.join(os.getcwd())
    file_name = f"VLE.pdf"
    file_path = os.path.join(output_dir, file_name)
    fig.savefig(file_path, dpi=resolution_value, bbox_inches='tight')
    fig.savefig(fr"{file_name}", dpi=resolution_value, bbox_inches='tight')