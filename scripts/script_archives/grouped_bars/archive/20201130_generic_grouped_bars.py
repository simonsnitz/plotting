import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import matplotlib.ticker as ticker
import matplotlib.transforms as transforms
import numpy as np
from pathlib import Path
from statistics import mean, stdev

plt.rcParams['font.family'] = 'Gargi'


p = Path('../../data/grouped_bars')
#dataSheet = p / "OMT_evolution_data.csv"

#data to import (this part changes)
dataSheet = p / "THP_biosynthesis_dopamine.csv"

#change this?
bar_width = 0.3

#create figure
fig, ax = plt.subplots()

#load data from csv
data = pd.read_csv(str(dataSheet))

#set graph and axis titles
title = data.iloc[0][1]
xtitle = data.iloc[1][1]
ytitle = data.iloc[2][1]
colors = [x for x in data.iloc[3][1:].values if str(x) != 'nan']

#set X-axis condition labels
xlabels = data.loc[4:]['Label'].values
x = np.arange(len(xlabels))

#create an array for the number of conditions you have
iterArray = [1+x*3 for x in range(0,int(len(data.columns[1:])/3))]

#set legend labels
legendLabels = [data.columns[x] for x in iterArray]

#populate lists for averages and standard deviations of all conditions
avgFluo = []
avgFluoErr = []
for i in iterArray:
    avg =  [mean([float(x) for x in data.iloc[y][i:i+3].values]) 
        for y in range(4,len(xlabels)+4)]
    avgFluo.append(avg)

    avgErr =  [stdev([float(x) for x in data.iloc[y][i:i+3].values]) 
        for y in range(4,len(xlabels)+4)]
    avgFluoErr.append(avgErr)

#create array of all individual data points
fluo = []
for i in iterArray:
    for j in data.iloc[4:].values:
        for k in list(j[i:i+3]):
            fluo.append(float(k))


#function for positioning individual data points such that they don't overlap
offset = lambda p: transforms.ScaledTranslation(p/72.0, 0, plt.gcf().dpi_scale_trans)
trans = plt.gca().transData

#create a list for positioning of each set of grouped bars next to each other
bar = [-bar_width,0,bar_width]

counter = 0
    #plot bar chart averages with error bars
for i in range(0,len(avgFluo)):
    plt.bar(x+ bar[i], avgFluo[i], bar_width, label=legendLabels[i], edgecolor='#000000', color=colors[i], zorder=0, linewidth=2, yerr=avgFluoErr[i], error_kw=dict(lw=2, capsize=5, capthick=2))
        #plot individual data points
    for j in range(0,len(xlabels)):
        plt.scatter(x[j]+bar[i], fluo[counter], s=40, facecolor="None", edgecolors='#000000', zorder=1, linewidth=2, transform=trans+offset(-10))
        plt.scatter(x[j]+bar[i], fluo[counter+1],s=40, facecolor="None", edgecolors='#000000', zorder=2, linewidth=2)
        plt.scatter(x[j]+bar[i], fluo[counter+2], s=40, facecolor="None", edgecolors='#000000', zorder=3, linewidth=2, transform=trans+offset(10))
        counter+=3

#set axis/legend labels, axis tick marks, and title
ax.set_xticks(x)
ax.set_xticklabels(xlabels)
ax.set_xlabel(xtitle, fontsize=18)
ax.set_ylabel(ytitle, fontsize=18)
plt.title(title, fontsize=18)
ax.legend(prop={'size':15})

#styling
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.tick_params(axis='both', which='major', labelsize=16)
fig.tight_layout()

plt.show()
