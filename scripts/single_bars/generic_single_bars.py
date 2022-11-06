import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sys
import matplotlib.ticker as ticker
import matplotlib.transforms as transforms
from pathlib import Path
import math
from statistics import mean, stdev

sys.path.append('../')
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
bar_colors = ["#52BFFF" for i in range(0,len(xlabels))]


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
            transform=trans+offset(dotSpacing[j]*0.3)
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
fig.set_size_inches(4,8)

plt.show()


if __name__ == "__main__":

    #load metadata from excel file
    metadata = pd.read_excel(dataSheet, sheet_name="metadata")
    fluorescence = pd.read_excel(dataSheet, sheet_name="fluorescence")
    od600 = pd.read_excel(dataSheet, sheet_name="od600")


    #create new dataframe for fluorescence/od600
    data = pd.DataFrame().reindex_like(fluorescence)

    for i in list(fluorescence.keys()):
        try:
            data[i] = fluorescence[i]/od600[i]
        except:
            data[i] = fluorescence[i]


        #set graph and axis titles
    title = metadata.loc[0,"Title"]
    xtitle = metadata.loc[0,"Xtitle"]
    ytitle = metadata.loc[0,"Ytitle"]
        #set X-axis condition labels
    xlabels = data.loc[0:]['Construct'].dropna().values
        #set number X-axis conditions
    x = np.arange(len(xlabels))


    #set bar colors from metadata. If only one color provided, set all bars to that same color.
    bar_colors = metadata.loc[:,"Colors"].dropna().values

    bar_colors = ["#ff932e"]

    if len(bar_colors) == 1:
        bar_colors = [bar_colors[0]]*(len(xlabels))
    elif len(bar_colors) != len(xlabels):
        raise ValueError("Invalid number of colors given. Need to provide one color or number equivalent to number of conditions")

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


        #create lists for averages and standard deviations of all conditions    
    if len(iterArray) > 1:
        avgFluo = []
        for i in iterArray:
            avg =  [mean([float(x) for x in data.iloc[y][i:i+num_reps].values]) 
                for y in range(0,len(xlabels))]
            avgFluo.append(avg)
    
        avgFluoErr = []
        if num_reps > 1:
            avgErr =  [stdev([float(x) for x in data.iloc[y][i:i+num_reps].values]) 
                for y in range(0,len(xlabels))]
            avgFluoErr.append(avgErr)
        else:
            num = len(avgFluo)
            avgFluoErr = [0]*num 

    else:
        avgFluo =  [mean([float(x) for x in data.iloc[y][1:1+num_reps].values]) 
            for y in range(0,len(xlabels))]
    
        avgFluoErr =  [stdev([float(x) for x in data.iloc[y][1:1+num_reps].values]) 
            for y in range(0,len(xlabels))]

    #create a list of all individual data points
    fluo = []
    for i in data.iloc[0:].values:
        for j in list(i[1:1+num_reps]):
            fluo.append(float(j))

    #dotSpacing = [(-0.5 - ((num_reps-2)/2) + 1*x)*offsetSize for x in range(0,num_reps)]

