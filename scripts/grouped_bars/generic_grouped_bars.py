import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import matplotlib.ticker as ticker
import matplotlib.transforms as transforms
import numpy as np
from pathlib import Path
from statistics import mean, stdev
from fpdf import FPDF
import math
import sys


sys.path.append('../')
from plotting_functions import *


#create figure and set font
fig, ax = plt.subplots()
plt.rcParams['font.family'] = 'Gargi'

#point to file for data import (exact file changes)
dataSheet = sys.argv[1]
#p = Path('../../data/grouped_bars')






    #load data from pre-formated excel sheet
metadata, fluorescence, od600 = load_data(dataSheet)


    #divide fluorescence by od600
data = divide_rfu_od(fluorescence, od600)


    #set titles, xaxis labels, and number of xaxis conditions(x)
title, xtitle, ytitle, xlabels, x = set_titles_labels(metadata, data)




    #remove "zeros" from yaxis values, to simplify
ytitle, data = simplify_yaxis(ytitle, data)


    #determine the number of replicates in the dataset
num_reps = get_num_replicates(data)


    #create a list for the number of unique conditions (replicates not counted)
iterArray = [1+x*num_reps for x in range(0,int(len(data.columns[1:-1])/num_reps))]


#set legend labels
legendLabels = [data.columns[x][:-2] for x in iterArray]
    
    #set colors to use for bars
colors = set_colors(metadata, legendLabels)

    #create nested lists for the averages, standard deviations, 
        #and individual data points
avgFluo, avgFluoErr, fluo = create_avg_std_indiv_lists(iterArray, data, num_reps, xlabels)


#function for positioning individual data points such that they don't overlap
offset = lambda p: transforms.ScaledTranslation(p/72.0, 0, plt.gcf().dpi_scale_trans)
trans = plt.gca().transData


#dynamically adjust the size and spacing of dots according to number of bars
num_bars = len(iterArray)*len(xlabels)
dotSize, offsetSize, dotSpacing = set_dot_params(num_bars, num_reps)


#dynamically set bar width based on number of bars ???
num_var = len(iterArray)
num_cond = len(xlabels)

#bar_width = 1.2/(num_bars**0.5)
#bar_width = 1/((num_cond*0.5)*(num_var*0.6))

bar_width = 0.3

print("number of bars: "+str(num_bars))
print("bar width: "+str(bar_width))

bar = [(-0.5 - ((len(legendLabels)-2)/2) + x)*bar_width 
            for x in range(0,len(legendLabels))]




#plot bar chart averages with error bars
counter = 0

for i in range(0,len(avgFluo)):
    plt.bar(x+ bar[i], avgFluo[i], bar_width, label=legendLabels[i], edgecolor='#000000', color=colors[i], zorder=0, linewidth=3, yerr=avgFluoErr[i], error_kw=dict(lw=1.5, capsize=5, capthick=1.5))
   

        #plot individual data points if there are fewer than 13 bars.
    if num_bars < 13 and num_reps > 1:
        for j in range(0,len(xlabels)):
            for k in range(0, num_reps):
                plt.scatter(x[j]+bar[i], fluo[counter+k], s=dotSize, facecolor="None", edgecolors='#000000', zorder=1, linewidth=2, transform=trans+offset(dotSpacing[k]))
            counter += num_reps
            
            '''
            plt.scatter(x[j]+bar[i], fluo[counter], s=dotSize, facecolor="None", edgecolors='#000000', zorder=1, linewidth=2, transform=trans+offset(-offsetSize))
            plt.scatter(x[j]+bar[i], fluo[counter+1],s=dotSize, facecolor="None", edgecolors='#000000', zorder=2, linewidth=2)
            plt.scatter(x[j]+bar[i], fluo[counter+2], s=dotSize, facecolor="None", edgecolors='#000000', zorder=3, linewidth=2, transform=trans+offset(offsetSize))
            counter+=3
            '''


#set axis/legend labels, axis tick marks, and title
ax.set_xticks(x)
ax.set_xticklabels(xlabels)

if num_bars > 13:
    ax.tick_params(axis='x', which='major', length=2, width=1, labelsize=14)
else:
    ax.tick_params(axis='x', which='major', length=2, width=1, labelsize=18)


ax.set_xlabel(xtitle, fontsize=20)
ax.set_ylabel(ytitle, fontsize=20)
plt.title(title, fontsize=22)
leg = ax.legend(prop={'size':15})
for legobj in leg.legendHandles:
    legobj.set_linewidth(1.0)

#styling
ax.tick_params(axis='y', which='major', length=2, width=1, labelsize=18)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
fig.tight_layout()
fig.set_size_inches(9,9)

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


'''
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
data = pd.DataFrame().reindex_like(fluorescence)

for i in list(fluorescence.keys()):
    try:
        data[i] = fluorescence[i]/od600[i]
    except:
        data[i] = fluorescence[i]


#set X-axis condition labels
xlabels = data.loc[0:]['Construct'].dropna().values
x = np.arange(len(xlabels))


#remove zeros for rfu/od to simplify y-axis
if ytitle == "Fluorescence (RFU/OD)" or "(RFU/OD)":
    max_val = 10**(len(str(int(data.iloc[:,1:-1].max().max())))-1)
    log10 = int(math.log10(max_val))
    ytitle = r'$(RFU/OD) \times 10^' + str(log10) +'$'

elif ytitle == "Fold change in fluorescence":
    max_val = 1
else:
    raise ValueError("y-axis title must be 'Fluorescence (RFU/OD)' or 'Fold change in fluorescence'")
for i in range(1,len(data.iloc[0]) -1):
    col = data.iloc[:,i]
    for n in range(0,len(col)):
        data.iloc[:,i][n] = col[n]/max_val

    #get the number of replicates from the column labels
last_char = [ x[-1] for x in data.columns.values]
num_reps = []
for i in last_char:
    try:
        num_reps.append(int(i))
    except:
        pass
num_reps = max(num_reps)

#create an array for the number of conditions you have
iterArray = [1+x*num_reps for x in range(0,int(len(data.columns[1:])/num_reps))]


if len(iterArray) < len(colors):
    raise ValueError("You must indicate at least "+len(iterArray)+" colors. Only "+len(colors)+" colors supplied")
'''



'''
#create lists for averages and standard deviations of all conditions
avgFluo = []
avgFluoErr = []
for i in iterArray:
    avg =  [mean([float(x) for x in data.iloc[y][i:i+num_reps].values]) 
        for y in range(0,len(xlabels))]
    avgFluo.append(avg)
    
    if num_reps > 1:
        avgErr =  [stdev([float(x) for x in data.iloc[y][i:i+num_reps].values]) 
            for y in range(0,len(xlabels))]
        avgFluoErr.append(avgErr)
    else:
        num = len(avgFluo)
        avgFluoErr = [0]*num 


#create a list of all individual data points
fluo = []
for i in iterArray:
    for j in data.iloc[0:].values:
        for k in list(j[i:i+3]):
            fluo.append(float(k))
'''

