import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.transforms as transforms
from pathlib import Path
import sys


#sys.path.append('../')
from plotting_functions import *


    #create figure
fig, ax = plt.subplots()
    #set font
plt.rcParams['font.family'] = 'Gargi'


    #point to file for data import (exact file changes)
dataSheet = sys.argv[1]


    #load data from pre-formated excel sheet
metadata, fluorescence, od600 = load_data(dataSheet)


    #divide fluorescence by od
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


    #create nested lists for the averages, standard deviations, and individual data points
avgFluo, avgFluoErr, fluo = create_avg_std_indiv_lists(iterArray, data, num_reps, xlabels)


    #function for positioning individual data points such that they don't overlap
offset = lambda p: transforms.ScaledTranslation(p/72.0, 0, plt.gcf().dpi_scale_trans)
trans = plt.gca().transData


    #dynamically adjust the size and spacing of dots according to number of bars
num_bars = len(iterArray)*len(xlabels)
dotSize, offsetSize, dotSpacing = set_dot_params(num_bars, num_reps)


    # Figure out a formula that sets good bar width for any number of bars
    #CHANGE THIS. Dynamically set bar width based on number of bars ???
num_var = len(iterArray)
num_cond = len(xlabels)

#bar_width = 1.2/(num_bars**0.5)
# bar_width = 1/((num_cond*0.5)*(num_var*0.6))
bar_width = 0.16

bar = [(-0.5 - ((len(legendLabels)-2)/2) + x)*bar_width 
            for x in range(0,len(legendLabels))]


    #plot bar chart averages with error bars
counter = 0

for i in range(0,len(avgFluo)):
    plt.bar(x+ bar[i], avgFluo[i], bar_width, label=legendLabels[i], edgecolor='#000000', color=colors[i], zorder=0, linewidth=3, yerr=avgFluoErr[i], error_kw=dict(lw=2, capsize=5, capthick=2))
   

        #plot individual data points if there are fewer than 12 bars.
    if num_bars < 100 and num_reps > 1:
        for j in range(0,len(xlabels)):
            for k in range(0, num_reps):
                plt.scatter(x[j]+bar[i], fluo[counter+k], s=50, facecolor="None", edgecolors='#000000', zorder=1, linewidth=2, transform=trans+offset((dotSpacing[k])*1.5))
            counter += num_reps
        
        ax.tick_params(axis='x', which='major', length=2, width=1, labelsize=14)
    else:
        ax.tick_params(axis='x', which='major', length=2, width=1, labelsize=18)


            

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

#save the figure as png and as a pdf report with metadata
new_figure = plt.savefig("THP_biosynthesis_dopamine.png",dpi=300)

#save as a pdf
pdf = FPDF()
#pdf.set_font("Garamond",16)
pdf.add_page()
pdf.image(new_figure)

pdf.output("THP_biosynthesis_dopamine.pdf","F")

'''
