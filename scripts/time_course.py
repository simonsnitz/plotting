import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib.ticker import MaxNLocator
import matplotlib.transforms as transforms
import sys
import argparse

sys.path.append('../')
from plotting_functions import *


    #create figure
fig, ax = plt.subplots()
    #set font
# plt.rcParams['font.family'] = 'Gargi'


    #parse arguments
parser = argparse.ArgumentParser()
parser.add_argument("-t", "--type", help="Type of data to plot")
parser.add_argument("-d", "--data", help="Plotting data")
args = parser.parse_args()

dataSheet = args.data


    #load data from pre-formated excel sheet
metadata, fluorescence, od600 = load_data(dataSheet)


    #set titles, xaxis labels, and number of xaxis conditions(x)
title, xtitle, ytitle, xlabels, x = set_titles_labels(metadata, fluorescence)


    #TODO fix this, if you want to plot rfu/od vs time
    #divide fluorescence by od
rfu_od = divide_rfu_od(fluorescence, od600)


    #use cli argument to set which type of data to plot
if args.type == "f" or args.type == "fluo" or args.type == "fluorescence":
    print("fluorescence")
    data = fluorescence
    ytitle = r'$RFU$'
        #set X-axis condition labels
    xlabels = data.loc[0:]['Time'].values
elif args.type == "o" or args.type == "od" or args.type == "od600":
    print("od600")
    data = od600
    ytitle = r'$OD_{600}$'
        #set X-axis condition labels
    xlabels = data.loc[0:]['Time'].values
elif args.type == "of" or args.type == "o/f" or args.type == "od/fluo":
    print("rfu/od")
    data = rfu_od
    ytitle = r'$RFU/OD$'
else:
    raise ValueError("Must indicate whether to plot either od or fluorescence")
    exit()



    #convert seconds to hours
xlabels = [i/3600 for i in xlabels]
xtitle = xtitle + " (hours)"


    #create an array for the number of conditions you have
iterArray = [1+x*3 for x in range(0,int(len(data.columns[1:])/3))]


    #set legend labels
legendLabels = [data.columns[x][:-2] for x in iterArray]


    #set colors to use for bars
colors = set_colors(metadata, legendLabels)


    #determine the number of replicates in the dataset
num_reps = get_num_replicates(data)


    #create nested lists for the averages, standard deviations, and individual data points
avgFluo, avgFluoErr, fluo = create_avg_std_indiv_lists(iterArray, data, num_reps, xlabels)


    #create datasets +/- error for plotting error as a "fill_between" visual
avgFluoTop = [ [avgFluo[i][j] + avgFluoErr[i][j] for j in range(0,len(avgFluo[0]))]
        for i in range(0,len(avgFluo))]
avgFluoBottom = [ [avgFluo[i][j] - avgFluoErr[i][j] for j in range(0,len(avgFluo[0]))]
        for i in range(0,len(avgFluo))]


    #plot lines
for i in range(0,len(avgFluo)):
    
        #plots lines with vertical lines to represent error
    #plt.errorbar(xlabels, avgFluo[i], label=legendLabels[i], color=colors[i], zorder=0, linewidth=3, yerr=avgFluoErr[i], elinewidth=2)
    
        #plots lines with "fill between" to represent error
    plt.plot(xlabels, avgFluo[i], label=legendLabels[i], color=colors[i], zorder=0, linewidth=3)
    plt.fill_between(xlabels, avgFluoTop[i], avgFluoBottom[i], color=colors[i], alpha=0.3)


    #set axis/legend labels, axis tick marks, and title
ax.set_xlabel(xtitle, fontsize=24)
ax.set_ylabel(ytitle, fontsize=24)
ax.set_xlim(3,9)
ax.set_ylim(0,15000)
#plt.title(title, fontsize=18)
ax.legend(prop={'size':20})


    #styling
ax.xaxis.set_major_locator(MaxNLocator(integer=True))
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.tick_params(axis='both', which='major', labelsize=20)
fig.tight_layout()
fig.set_size_inches(18,8)

    #show the figure and add prompt to decide whether or not to save it.
plt.show()
