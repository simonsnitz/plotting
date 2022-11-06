import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sys
import matplotlib.ticker as ticker
import matplotlib.transforms as transforms
from pathlib import Path 
from statistics import mean, stdev
import math
import sys
import argparse


sys.path.append('../')
from plotting_functions import *

#create figure
fig, ax = plt.subplots()
#set font
plt.rcParams['font.family'] = 'Gargi'

    #import data
dataSheet = sys.argv[1]

    #load data
data = pd.read_excel(dataSheet)


xlabel_name =  data.columns[0]
xlabels = data.loc[0:][xlabel_name].dropna().values
    #set number X-axis conditions
x = np.arange(len(xlabels))

x = HPLC_AVG = data.loc[0:][data.columns[1]].dropna().values[:-1]
xerr = HPLC_ERR = data.loc[0:][data.columns[2]].dropna().values[:-1]
y = SENSOR_AVG = data.loc[0:][data.columns[3]].dropna().values
yerr = SENSOR_ERR = data.loc[0:][data.columns[4]].dropna().values



plt.scatter(x, y, color='white', s=200, edgecolor="blue", linewidth=3)
plt.errorbar(x, y, yerr=yerr, xerr=xerr, ls="None", color='black', lw=2, capsize=4, capthick=2)

plt.title("Comparison of HPLC and biosensor measurements")
plt.ylabel("RFU/OD", fontsize=22)
plt.xlabel("4Ome-Norbelladine (uM)", fontsize=22)
ax.set_xscale('linear')
#ax.set_yscale('log')
plt.xticks(fontsize=20)
plt.yticks(fontsize=18)
#ax.set_ylim([0,80000])
#ax.set_xlim([0,1200])
fig.set_size_inches(12,8)
plt.show()