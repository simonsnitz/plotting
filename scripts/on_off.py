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
dataSheet = sys.argv[1]

    #load data from pre-formated excel sheet
metadata, fluorescence, od600 = load_data(dataSheet)

    #divide fluorescence by od600
data = divide_rfu_od(fluorescence, od600)

    #set titles, xaxis labels, and number of xaxis conditions(x)
title, xtitle, ytitle, xlabels, x = set_titles_labels(metadata, data)

    #remove "zeros" from yaxis values, to simplify
#ytitle, data = simplify_yaxis(ytitle, data)

    #determine the number of replicates in the dataset
num_reps = get_num_replicates(data)

    #create a list for the number of unique conditions (replicates not counted)
iterArray = [1+x*num_reps for x in range(0,int(len(data.columns[1:-1])/num_reps))]

    #create nested lists for the averages, standard deviations, 
        #and individual data points
avgFluo, avgFluoErr, fluo = create_avg_std_indiv_lists(iterArray, data, num_reps, xlabels)



for i in range(0,len(xlabels)):

    plt.vlines(xlabels[i], ymin=avgFluo[0][i], ymax=avgFluo[1][i], colors="#000000")

    plt.scatter(xlabels[i], avgFluo[0][i], s=40, facecolor="#000000", edgecolors="#000000", zorder=5)
    plt.scatter(xlabels[i], avgFluo[1][i], s=40, facecolor="#FFFFFF", edgecolors="#000000", zorder=5)


min_y = 100
max_y = 100000

    #plot horizontal lines for reference
plt.axhline(y=1000, color="#0c69cc", linewidth=1, alpha=0.4)
plt.axhline(y=10000, color="#0c69cc", linewidth=1, alpha=0.4)


ax.set_ylim([min_y,max_y])
ax.set_yscale('log')
plt.xticks(xlabels, fontsize=12, rotation=45)

plt.xlabel(xtitle, fontsize=20)
plt.ylabel(ytitle, fontsize=20)

ax.tick_params(axis='y', which='major', length=2, width=1, labelsize=18)
fig.set_size_inches(16,6)

plt.show()