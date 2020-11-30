import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import matplotlib.ticker as ticker
import matplotlib.transforms as transforms
import numpy as np
from pathlib import Path
from statistics import mean, stdev
from fpdf import FPDF

#create figure and set font
fig, ax = plt.subplots()
plt.rcParams['font.family'] = 'Gargi'

#point to file for data import (exact file changes)
p = Path('../../data/grouped_bars')
dataSheet = p / "THP_biosynthesis_dopamine.xlsx"
#dataSheet = p / "OMT_evolution_data.xlsx"

#set bar width. Change this dynamically?
bar_width = 0.3


#load metadata from excel file
metadata = pd.read_excel(dataSheet, sheet_name=2)

#set graph and axis titles
title = metadata.loc[0,"Title"]
xtitle = metadata.loc[0,"Xtitle"]
ytitle = metadata.loc[0,"Ytitle"]
colors = metadata.loc[:,"Colors"].values


#load data from excel file
fluorescence = pd.read_excel(dataSheet, sheet_name=0)
od600 = pd.read_excel(dataSheet, sheet_name=1)

#create new dataframe for fluorescence/od600
data = fluorescence
for i in list(data.keys()):
    try:
        data[i] = data[i]/od600[i]
    except:
        data[i] = data[i]


#set X-axis condition labels
xlabels = data.loc[0:]['Construct'].values
x = np.arange(len(xlabels))

#remove zeros for rfu/od to simplify y-axis
if ytitle == "Fluorescence (RFU/OD)":
    max_val = 10**(len(str(int(data.iloc[:,1:-1].max().max())))-1)
elif ytitle == "Fold change in fluorescence":
    max_val = 1
else:
    raise ValueError("y-axis title must be 'Fluorescence (RFU/OD)' or 'Fold change in fluorescence'")

for i in range(1,len(data.iloc[0]) -1):
    col = data.iloc[:,i]
    for n in range(0,len(col)):
        data.iloc[:,i][n] = col[n]/max_val


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

#create a list of all individual data points
fluo = []
for i in iterArray:
    for j in data.iloc[0:].values:
        for k in list(j[i:i+3]):
            fluo.append(float(k))

#function for positioning individual data points such that they don't overlap
offset = lambda p: transforms.ScaledTranslation(p/72.0, 0, plt.gcf().dpi_scale_trans)
trans = plt.gca().transData

#create a list for positioning of each set of grouped bars next to each other
bar = [-bar_width,0,bar_width]


#plot bar chart averages with error bars
counter = 0
#dynamically adjust the size and spacing of dots according to number of bars
numBars = len(iterArray)*len(xlabels)
dotSize = (500/(numBars))**1.2
offsetSize = (1/(numBars))*200

for i in range(0,len(avgFluo)):
    plt.bar(x+ bar[i], avgFluo[i], bar_width, label=legendLabels[i], edgecolor='#000000', color=colors[i], zorder=0, linewidth=2, yerr=avgFluoErr[i], error_kw=dict(lw=1.3, capsize=5, capthick=1.3))
    
    #plot individual data points
    for j in range(0,len(xlabels)):
        plt.scatter(x[j]+bar[i], fluo[counter], s=dotSize, facecolor="None", edgecolors='#000000', zorder=1, linewidth=2, transform=trans+offset(-offsetSize))
        plt.scatter(x[j]+bar[i], fluo[counter+1],s=dotSize, facecolor="None", edgecolors='#000000', zorder=2, linewidth=2)
        plt.scatter(x[j]+bar[i], fluo[counter+2], s=dotSize, facecolor="None", edgecolors='#000000', zorder=3, linewidth=2, transform=trans+offset(offsetSize))
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
fig.set_size_inches(12,9)

#show the figure and add prompt to decide whether or not to save it.
plt.show()

'''
#save the figure as png and as a pdf report with metadata
new_figure = plt.savefig("THP_biosynthesis_dopamine.png",dpi=300)

#save as a pdf
pdf = FPDF()
#pdf.set_font("Garamond",16)
pdf.add_page()
pdf.image(new_figure)

pdf.output("THP_biosynthesis_dopamine.pdf","F")
'''
