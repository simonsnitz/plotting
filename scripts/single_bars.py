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



    #set colors to use for bars
bar_colors = set_colors(metadata, xlabels)
    #override color scheme
#bar_colors = ["#C28CFF" for i in range(0,len(xlabels))]


    #remove "zeros" from yaxis values, to simplify
#ytitle, data = simplify_yaxis(ytitle, data)


    #determine the number of replicates in the dataset
num_reps = get_num_replicates(data)

    #create a list for the number of unique conditions (replicates not counted)
#iterArray = [1+x*num_reps for x in range(0,int(len(data.columns[1:-1])/num_reps))]
    # only one bar per condition for the single bars program
iterArray = [0]

    #create nested lists for the averages, standard deviations, 
        #and individual data points
avgFluo, avgFluoErr, fluo = create_avg_std_indiv_lists(iterArray, data, num_reps, xlabels)


    #function for positioning individual data points such that they don't overlap
offset = lambda p: transforms.ScaledTranslation(p/72.0, 0, plt.gcf().dpi_scale_trans)
trans = plt.gca().transData


    #dynamically adjust the size and spacing of dots according to the number of bars
num_bars = len(iterArray)*len(xlabels)
dotSize, offsetSize, dotSpacing = set_dot_params(num_bars, num_reps)



    #dynamically set bar width based on number of bars
#bar_width = 2*(1/(num_bars**0.8))
bar_width = 1.2/(num_bars**0.5)
#bar_width = 0.15


counter = 0

for i in range(0,len(xlabels)):
    
        #plot bars
    plt.bar(xlabels[i], avgFluo[i], bar_width, color=bar_colors[i], edgecolor='#000000', zorder=0, linewidth=3.5, yerr=avgFluoErr[i], error_kw=dict(lw=2, capsize=10, capthick=2))

        #plot individual data points
    for j in range(0,num_reps):
        plt.scatter(xlabels[i], fluo[counter+j], s=100, facecolor="None",edgecolors='#000000', zorder=1, linewidth=2, 
            transform=trans+offset(dotSpacing[j]*0.8)
            )
    counter+=num_reps
    

if num_bars > 13:
    ax.tick_params(axis='x', which='major', length=2, width=1, labelsize=14)
else:
    ax.tick_params(axis='x', which='major', length=2, width=1, labelsize=18)

ax.set_ylim([0,None])
plt.xticks(xlabels, fontsize=22, rotation=90)
#plt.xticks(xlabels, fontsize=16)
plt.xlabel(xtitle, fontsize=26)
plt.ylabel(ytitle, fontsize=26)
# plt.title(title, fontsize=24)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# ax.set_yscale('log')
# plt.ylim(1,200)

ax.tick_params(axis='y', which='major', length=2, width=1, labelsize=22)
fig.set_size_inches(16,8)

plt.show()
