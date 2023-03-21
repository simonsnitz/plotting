import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sys
import matplotlib.ticker as ticker
import matplotlib.transforms as transforms
from pathlib import Path
import math
from statistics import mean, stdev

from plotting_functions import *

#create figure and set font
fig, ax = plt.subplots()
plt.rcParams['font.family'] = 'Gargi'

    #import data
data = pd.read_excel(sys.argv[1])

columns = [i for i in data.columns]

independent = [i for i in data[columns[1]]]

dependent = [i for i in data[columns[0]]]

for i in range(0, len(independent)):
    plt.scatter(independent[i], dependent[i], s=30, facecolor="#0088ff", edgecolors="#000000")
# for i in range(0,len(xlabels)):

#     plt.vlines(xlabels[i], ymin=avgFluo[0][i], ymax=avgFluo[1][i], colors="#000000")

#     plt.scatter(xlabels[i], avgFluo[0][i], s=40, facecolor="#000000", edgecolors="#000000", zorder=5)
#     plt.scatter(xlabels[i], avgFluo[1][i], s=40, facecolor="#FFFFFF", edgecolors="#000000", zorder=5)

min_y = 0
max_y = 110
ax.set_ylim([min_y,max_y])

min_x = 0
max_x = 110
ax.set_xlim([min_x,max_x])

plt.xlabel(columns[1], fontsize=22)
plt.ylabel(columns[0], fontsize=22)
ax.tick_params(axis='y', which='major', length=2, width=1, labelsize=16)
ax.tick_params(axis='x', which='major', length=2, width=1, labelsize=16)

fig.set_size_inches(7,6)
plt.show()


# ax.set_ylim([min_y,max_y])
# ax.set_yscale('log')
# plt.xticks(xlabels, fontsize=12, rotation=45)

# plt.xlabel(xtitle, fontsize=20)
# plt.ylabel(ytitle, fontsize=20)

# ax.tick_params(axis='y', which='major', length=2, width=1, labelsize=18)

# plt.show()