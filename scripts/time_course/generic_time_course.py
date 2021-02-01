import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import matplotlib.ticker as ticker
from matplotlib.ticker import MaxNLocator
import matplotlib.transforms as transforms
import numpy as np
from pathlib import Path
from statistics import mean, stdev
from fpdf import FPDF
import math

#create figure and set font
fig, ax = plt.subplots()
plt.rcParams['font.family'] = 'Gargi'

#point to file for data import (exact file changes)
p = Path('../../data/time_course')
dataSheet = p / "RamZ_selection_data.xlsx"


#load metadata from excel file
metadata = pd.read_excel(dataSheet, sheet_name="metadata")

#set graph and axis titles
title = metadata.loc[0,"Title"]
xtitle = metadata.loc[0,"Xtitle"]
ytitle = metadata.loc[0,"Ytitle"]
colors = metadata.loc[:,"Colors"].values


#load data from excel file
fluorescence = pd.read_excel(dataSheet, sheet_name="fluorescence")
od600 = pd.read_excel(dataSheet, sheet_name="od600")


#create new dataframe for fluorescence/od600
rfu_od = pd.DataFrame().reindex_like(fluorescence)

for i in list(fluorescence.keys()):
    try:
        rfu_od[i] = fluorescence[i]/od600[i]
    except:
        rfu_od[i] = fluorescence[i]


    #set which dataset to use for plotting
#data = fluorescence
#ytitle = r'$RFU/OD$'

data = od600
ytitle = r'$OD_{600}$'


#set X-axis condition labels
xlabels = data.loc[0:]['Time'].values
    #convert seconds to hours
xlabels = [i/3600 for i in xlabels]
xtitle = xtitle + " (hours)"

x = np.arange(len(xlabels))

''' This screws things up when plotting time_course data

#remove zeros for rfu/od to simplify y-axis
if ytitle == "Fluorescence (RFU/OD)" or "RFU/OD600":
    max_val = 10**(len(str(int(data.iloc[:,1:-1].max().max())))-1)
    log10 = int(math.log10(max_val))
    ytitle = r'$(RFU/OD) \times 10^' + str(log10) +'$'

elif ytitle == "Fold change in fluorescence":
    max_val = 1
else:
    raise ValueError("y-axis title must be 'Fluorescence (RFU/OD)', 'RFU/OD600'  or 'Fold change in fluorescence'")
for i in range(1,len(data.iloc[0]) -1):
    col = data.iloc[:,i]
    for n in range(0,len(col)):
        data.iloc[:,i][n] = col[n]/max_val
'''

#create an array for the number of conditions you have
iterArray = [1+x*3 for x in range(0,int(len(data.columns[1:])/3))]

if len(iterArray) != len(colors):
    raise ValueError("You must indicate "+len(iterArray)+" colors. Only "+len(colors)+" colors supplied")

#set legend labels
legendLabels = [data.columns[x][:-2] for x in iterArray]

#create lists for averages and standard deviations of all conditions
avgFluo = []
avgFluoErr = []

for i in iterArray:
    avg =  [mean([float(x) for x in data.iloc[y][i:i+3].values]) 
        for y in range(0,len(xlabels))]
    avgFluo.append(avg)

    avgErr =  [stdev([float(x) for x in data.iloc[y][i:i+3].values]) 
        for y in range(0,len(xlabels))]
    avgFluoErr.append(avgErr)

'''
#create a list of all individual data points
#fluo = []
#for i in iterArray:
#    for j in data.iloc[0:].values:
#        for k in list(j[i:i+3]):
#            fluo.append(float(k))
'''

#create datasets +/- error for plotting error as a "fill_between" visual
avgFluoTop = [ [avgFluo[i][j] + avgFluoErr[i][j] for j in range(0,len(avgFluo[0]))]
        for i in range(0,len(avgFluo))]
avgFluoBottom = [ [avgFluo[i][j] - avgFluoErr[i][j] for j in range(0,len(avgFluo[0]))]
        for i in range(0,len(avgFluo))]
        
for i in range(0,len(avgFluo)):
    
    #plt.plot(xlabels, avgFluo[i], label=legendLabels[i], color=colors[i], zorder=0, linewidth=3)
    #plt.fill_between(xlabels, avgFluoTop[i], avgFluoBottom[i], color=colors[i], alpha=0.5)
    
    plt.errorbar(xlabels, avgFluo[i], label=legendLabels[i], color=colors[i], zorder=0, linewidth=3, yerr=avgFluoErr[i], elinewidth=2)

'''
    if numBars < 13:
        #plot individual data points if there are fewer than 10 bars.
        for j in range(0,len(xlabels)):
            plt.scatter(x[j]+bar[i], fluo[counter], s=dotSize, facecolor="None", edgecolors='#000000', zorder=1, linewidth=2, transform=trans+offset(-offsetSize))
            plt.scatter(x[j]+bar[i], fluo[counter+1],s=dotSize, facecolor="None", edgecolors='#000000', zorder=2, linewidth=2)
            plt.scatter(x[j]+bar[i], fluo[counter+2], s=dotSize, facecolor="None", edgecolors='#000000', zorder=3, linewidth=2, transform=trans+offset(offsetSize))
            counter+=3
'''

#set axis/legend labels, axis tick marks, and title
ax.set_xlabel(xtitle, fontsize=18)
ax.set_ylabel(ytitle, fontsize=18)
plt.title(title, fontsize=18)
ax.legend(prop={'size':15})

#styling
ax.xaxis.set_major_locator(MaxNLocator(integer=True))
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.tick_params(axis='both', which='major', labelsize=16)
fig.tight_layout()
fig.set_size_inches(12,9)

#show the figure and add prompt to decide whether or not to save it.
plt.show()


