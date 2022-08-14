## Works the best so far! Curve fits nicely and ymin/ymax don't have to be 0 and 1!
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.optimize import curve_fit
import sys
import matplotlib.ticker as ticker
import matplotlib.transforms as transforms
from pathlib import Path 
from statistics import mean, stdev
import math
import sys
import argparse

sys.path.append('../')
from plotting_functions import *


#create figure
fig, ax = plt.subplots()
#set font
plt.rcParams['font.family'] = 'Gargi'


    #parse arguments
parser = argparse.ArgumentParser()
parser.add_argument("-t", "--table", help="Include table")
parser.add_argument("-d", "--data", help="Plotting data")
parser.add_argument("-r", "--reference", help="What do I do with the reference values?")
args = parser.parse_args()

dataSheet = args.data


    #load data from pre-formated excel sheet
metadata, fluorescence, od600 = load_data(dataSheet)
 
    
    #divide fluorescence by od
data = divide_rfu_od(fluorescence, od600)


    #set titles, xaxis labels, and number of xaxis conditions(x)
title, xtitle, ytitle, xdata = set_titles_labels(metadata, fluorescence)

                #if args.table == "yes":

    #remove "zeros" from yaxis values, to simplify
ytitle, data = simplify_yaxis(ytitle, data)


    #determine the number of replicates in the dataset
num_reps = get_num_replicates(data)


    #create a list for the number of unique conditions (replicates not counted)
iterArray = [1+x*num_reps for x in range(0,int(len(data.columns[1:-1])/num_reps))]


    #set legend labels
labels = [data.columns[x][:-2] for x in iterArray]

    
    #set colors to use for bars
colors = set_colors(metadata, labels)

colors = ["#0008ff","#f59700","#088000"]

    #create nested lists for the averages, standard deviations, 
        #and individual data points
avgFluo, avgFluoErr, fluo = create_avg_std_indiv_lists(iterArray, data, num_reps, xdata)


    #set xaxis limits
xaxis_max = float(fluorescence.iloc[-1,0])*2
xaxis_min = float(fluorescence.iloc[1,0])/8


    #Hill sigmoid function
def sigmoid(x, a, b, c, d):
        return d + (a-d) * np.power(x,b) / (np.power(c,b) + np.power(x,b))
#def sigmoid(x, a, b, c):
#        return a * np.power(x,b) / (np.power(c,b) + np.power(x,b))


    #create x-axis ticks. large number in 3rd position of linspace "100,000" needed to avoid choppy line.
x = np.linspace(1e-8,(xaxis_max/2),100000)


    #create list of colors for dots (individual data points)
        #still working on making this list with list comprehension
colorDots = []
for i in colors:
    colorDots.append(str(i))
    colorDots.append(str(i))
    colorDots.append(str(i))


    #loop through mutants and plot fitted sigmoid functions. May need to change these parameters.
median_x = np.median(x)
half_y = float(max(data.max().values[0:-1]))/2
initParam = (median_x, half_y, 5, 1)
#initParam = np.array([1.0,0.9,5.0])


    #plot curve_fit line based on averages data
EC50 = []



for i in range(0,len(labels)):
    popt, pcov = curve_fit(sigmoid, xdata, avgFluo[i], initParam, maxfev=10000)
        
        #add EC50 value if it's not crazy high
    EC50_value = popt[2]
    print(EC50_value)
    if EC50_value <= 1000:
        EC50.append(round(popt[2],1))
    else:
        EC50.append("N/A")
    
    plt.plot(x, sigmoid(x, *popt), color = colors[i], label='fit', lw=3.5)
        #add error bar
    #plt.bar(xdata,avgFluo[i], yerr=avgFluoErr[i],visible=False, color='black', error_kw=dict(lw=1,capsize=3,capthick=1), label="error")


    #plot individual data points as dots
numColumns = len(data.columns)
for i in range(1,numColumns-1):
    variant = data.columns.values[i]
    plt.plot(xdata, data.loc[:,variant],color = colorDots[i-1], markersize=8, marker='o', linestyle='None')


    #create a table with information on background signal and estimated EC50 values
if args.table == "yes":
    
    max_val = 10**(len(str(int(data.max().max())))-1)
    BkgrdAvg = [round(x[0]*max_val,2) for x in avgFluo]
    BkgrdErr = [round(x[0]*max_val,2) for x in avgFluoErr]
    Background = [str(BkgrdAvg[x])+" +/- "+str(BkgrdErr[x]) for x in range(0,len(BkgrdAvg))]

    the_table = plt.table(cellText = [EC50,Background],
            rowLabels = ["EC50 (uM)","Background"],
            colColours= colors,
            colLabels = labels,
            bbox=[0.05,-0.5,1,0.25])

    the_table.set_fontsize(12)
        #position plot higher to avoid clashing with table
    plt.subplots_adjust(bottom=0.3)


    #Extend the xaxis max and min limits to give space on xaxis
plt.xlim(xaxis_min, xaxis_max)

#plt.title(title, fontsize=22)
plt.ylabel(ytitle, fontsize=24)
plt.xlabel(xtitle, fontsize=24)

    #should be symlog, but tick spacing gets screwed up
ax.set_xscale('log')
ax.get_xaxis().set_major_formatter(ticker.ScalarFormatter())
ax.get_xaxis().set_major_formatter(ticker.FormatStrFormatter('%.1f'))

ax.tick_params(axis='both', which='major', length=2, width=1, labelsize='18')
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)

#ax.xaxis.set_major_locator(ticker.MultipleLocator(10))
plt.legend(labels, prop={'size':20}, loc="best")

fig.set_size_inches(14,8)

plt.show()

