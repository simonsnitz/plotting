import matplotlib.pyplot as plt
import matplotlib
from matplotlib.colors import LinearSegmentedColormap
import numpy as np
import matplotlib.ticker as ticker
import pandas as pd
import seaborn as sns; sns.set()
from statistics import mean, stdev
import matplotlib.transforms as transforms
import matplotlib.font_manager as mfm
mfm.findSystemFonts(fontpaths=None, fontext='ttf')
from pathlib import Path
import sys



sys.path.append('../')
from plotting_functions import *


    #create figure
fig, ax = plt.subplots()
    #set font parameters
plt.rcParams['font.family'] = 'Gargi'
sns.set(font_scale=1.5)


    #point to file for data import (exact file changes)
dataSheet = sys.argv[1]


    #load data from pre-formated excel sheet
metadata, fluorescence, od600 = load_data(dataSheet)


    #divide fluorescence by od
data = divide_rfu_od(fluorescence, od600)


title, xtitle, ytitle, xlabels, x = set_titles_labels(metadata, data)

    #determine the number of replicates in the dataset
num_reps = get_num_replicates(data)


    #create a list for the number of unique conditions (replicates not counted)
iterArray = [1+x*num_reps for x in range(0,int(len(data.columns[1:-1])/num_reps))]


    #set legend labels
ylabels = [data.columns[x][:-2] for x in iterArray]


    #set colors to use for bars
colors = set_colors(metadata, ylabels)


ylabels, ytitle, fold = create_fold_df(iterArray, data, num_reps, xlabels, ylabels)



wildtype = fold.iloc[:,-1]

perc_wt = pd.DataFrame()


for i in range(0,fold.shape[1]):
    perc = fold.iloc[:,i] / wildtype
    perc_wt[i] = perc

print(perc_wt)

'''
    #create dataframe for averages
averages = pd.DataFrame()

counter = 0
for i in iterArray:
    avg =  [mean([float(x) for x in data.iloc[y][i:i+num_reps].values if str(x) != "nan"]) 
        for y in range(0,len(xlabels))]
            
    averages[ylabels[counter]] = avg
    counter += 1


    #create dataframe for fold change
fold = pd.DataFrame()
    #remove 'dmso' from ylabels
ylabels = ylabels[1:]
ytitle = "Fold change in fluorescence"
for i in ylabels:
    fold[i] = averages[i]/averages["DMSO"]
fold = fold.T

'''

    #get max value to set y-axis limit
max_nums = []
for i in perc_wt.columns:
    max_nums.append(perc_wt[i].max())
max_value = round(1.2*(max(max_nums)),0)

#print(max_value)

#custom colormap function
def NonLinCdict(steps, hexcol_array):
    cdict = {'red': (), 'green': (), 'blue': ()}
    for s, hexcol in zip(steps, hexcol_array):
        rgb = matplotlib.colors.hex2color(hexcol)
        cdict['red'] = cdict['red'] + ((s, rgb[0], rgb[0]),)
        cdict['green'] = cdict['green'] + ((s, rgb[1], rgb[1]),)
        cdict['blue'] = cdict['blue'] + ((s, rgb[2], rgb[2]),)
    return cdict

#hc = ['#ffffff','#009BFF', '#C100FF']
hc = ['#0400ff','#ffffff','#ffd000', '#ff001e', '#ff001e']
th = [0,0.1, 0.3,0.6,1]

cdict = NonLinCdict(th, hc)
cm = LinearSegmentedColormap('test', cdict)

#increase font size by a little
sns.set(font_scale=1.5)


#create seaborn heatmap
#ax = sns.heatmap(fold, vmin=0, vmax= max_value, annot=True,fmt='.0f',yticklabels= ylabels, xticklabels= xlabels, linewidths=1, linecolor="#7a7a7a", cmap=cm)
ax = sns.heatmap(perc_wt, vmin=0, vmax= max_value,yticklabels= ylabels, xticklabels= xlabels,linewidths=0.5, linecolor="#7a7a7a", cmap=cm)
plt.title(title)
plt.xlabel(xtitle)
plt.ylabel(ytitle)
plt.yticks(rotation=0)
plt.xticks(rotation=45)
#fig.set_size_inches(9,9)

plt.show()

'''
    #set axis/legend labels, axis tick marks, and title
ax.set_xticks(x)
ax.set_xticklabels(xlabels,fontsize=20)
ax.set_xlabel(xtitle, fontsize=26)
ax.set_ylabel(ytitle, fontsize=26)
plt.title(title, fontsize=22)

leg = ax.legend(prop={'size':20})
for legobj in leg.legendHandles:
    legobj.set_linewidth(1.0)


    #styling
ax.tick_params(axis='y', which='major', length=2, width=1, labelsize=22)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
#fig.tight_layout()
fig.set_size_inches(12,9)

    #show the figure and add prompt to decide whether or not to save it.
plt.show()
'''
