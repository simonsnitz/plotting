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

#plt.rcParams['font.family'] = 'Gargi'

p = Path('../../data/dose_response')

#this part changes
#dataSheet = p / "GLAUdata_new.xlsx"
#dataSheet = p / "NOSdata_new2.xlsx"
#dataSheet = p / "PAPdata_new.xlsx"
#dataSheet = p / "ROTUdata_new.xlsx"
#dataSheet = p / "THPdata_new.xlsx"
#dataSheet = p / "THPa4_selectivity.xlsx"
#dataSheet = p / "WT-FEN1-FEN2-FEN3_doseResponse.xlsx"
dataSheet = sys.argv[1]

#create figure
fig, ax = plt.subplots()

#load data from xlsx file
fluorescence = pd.read_excel(dataSheet, sheet_name="fluorescence")
od600 = pd.read_excel(dataSheet, sheet_name="od600")
metadata = pd.read_excel(dataSheet, sheet_name="metadata")


#extract useful metadata
title = metadata.loc[0,"Title"]
Xtitle = metadata.loc[0,"Xtitle"]
Ytitle = metadata.loc[0,"Ytitle"]
colors = metadata.loc[:,"Colors"].values

#create new dataframe for fluorescence/od600
data = fluorescence.copy()
for i in list(data.keys()):
    try:
        data[i] = data[i]/od600[i]
    except:
        data[i] = data[i]

#set array for x-axis (ligand concentration)
xdata = fluorescence.loc[:,"Ligand concentration"].values

    #set xaxis limits
xaxis_max = float(fluorescence.iloc[-1,0])*2
xaxis_min = float(fluorescence.iloc[1,0])/8

max_val = 10**(len(str(int(data.max().max())))-1)

#calculate the background.
bkgrd = data.loc[:,"REFERENCE"].mean()

#update dataframe by subtracting background from each value           
    #Assumes DH10B column is last column.
for i in range(1,len(data.iloc[0]) -1):
    col = data.iloc[:,i]
    for n in range(0,len(col)):
        data.iloc[:,i][n] = (col[n]-bkgrd)
        #data.iloc[:,i][n] = (col[n]-bkgrd)/max_val

#remove zeros for rfu/od to simplify y-axis
if Ytitle == "Fluorescence (RFU/OD)" or "(RFU/OD)":
    max_val = 10**(len(str(int(data.iloc[:,1:-1].max().max())))-1)
    log10 = int(math.log10(max_val))
    Ytitle = r'$(RFU/OD) \times 10^' + str(log10) +'$'

elif Ytitle == "Fold change in fluorescence":
    max_val = 1
else:
    raise ValueError("y-axis title must be 'Fluorescence (RFU/OD)' or 'Fold change in fluorescence'")
for i in range(1,len(data.iloc[0]) -1):
    col = data.iloc[:,i]
    for n in range(0,len(col)):
        data.iloc[:,i][n] = col[n]/max_val


#create an array for the number of biosensors you're comparing
iterArray = [1+x*3 for x in range(0,int(len(data.columns[1:])/3))]

#Generate variant name labels from column labels. remove last two characters
labels = [data.columns.values[i][:-2] for i in iterArray]


#Summarizing statistics. Create 2 list of lists. One with averages data, the other with standard deviation data.
    #don't count any missing values (nan)
avgFluo = []
avgFluoErr = []
for i in iterArray:
    avg =  [mean([float(x) for x in data.iloc[y][i:i+3].values if str(x) != "nan"]) 
        for y in range(0,len(xdata))]
    avgFluo.append(avg)

    avgErr =  [stdev([float(x) for x in data.iloc[y][i:i+3].values if str(x) != "nan"]) 
        for y in range(0,len(xdata))]
    avgFluoErr.append(avgErr)

Bkgrd = [round(x[0]*max_val,1) for x in avgFluo]
BkgrdErr = [round(x[0]*max_val,1) for x in avgFluoErr]
Background = [str(Bkgrd[x])+" +/- "+str(BkgrdErr[x]) for x in range(0,len(Bkgrd))]

#Hill sigmoid function
def sigmoid(x, a, b, c):
        return a * np.power(x,b) / (np.power(c,b) + np.power(x,b))

#create x-axis ticks. large number in 3rd position of linspace "100,000" needed to avoid choppy line.
    #this needs to change based on the x-axis limits
x = np.linspace(0,(xaxis_max/2),100000)


#create list of colors for dots (individual data points)
    #still working on making this list with list comprehension
colorDots = []
for i in colors:
    colorDots.append(str(i))
    colorDots.append(str(i))
    colorDots.append(str(i))

#Loop through mutants and plot fitted sigmoid functions. May need to change these parameters.

#initParam = np.array([1.0,0.9,5.0])
median_x = np.median(x)
half_y = float(max(data.max().values[0:-1]))/2

initParam = (median_x, half_y, 5)

#plot curve_fit line based on averages data
EC50 = []
for i in range(0,len(labels)):
    popt, pcov = curve_fit(sigmoid, xdata, avgFluo[i],initParam,  maxfev=10000)
        
        #add EC50 value if it's not crazy high
    EC50_value = popt[2]
    if EC50_value <= 1000:
        EC50.append(round(popt[2],1))
    else:
        EC50.append("N/A")
    
    plt.plot(x, sigmoid(x, *popt), color = colors[i], label='fit')
    #plt.bar(xdata,avgFluo[i], yerr=avgFluoErr[i],visible=False, color='black', error_kw=dict(lw=1,capsize=3,capthick=1), label="error")

#plot individual data points as dots
numColumns = len(data.columns)
for i in range(1,numColumns-1):
    variant = data.columns.values[i]
    plt.plot(xdata, data.loc[:,variant],color = colorDots[i-1], marker='o', linestyle='None')

#Extend the xaxis max and min limits to give space on xaxis
plt.xlim(xaxis_min, xaxis_max)
#plt.ylim(0,7.5)

    #create table for displaying the calculated EC50s and Background signals for each variant
the_table = plt.table(cellText = [EC50,Background],
        rowLabels = ["EC50","Background"],
        colColours= colors,
        colLabels = labels,
        bbox=[0.05,-0.5,1,0.25])

the_table.set_fontsize(12)

    #position plot higher to avoid clashing with table
plt.subplots_adjust(bottom=0.3)

plt.ylabel(Ytitle, fontsize=20)
plt.xlabel(Xtitle, fontsize=20)
plt.title(title, fontsize=25)
#should be symlog, but tick spacing gets screwed up
ax.set_xscale('log')
ax.get_xaxis().set_major_formatter(ticker.ScalarFormatter())
#ax.get_xaxis().set_major_formatter(ticker.FormatStrFormatter('%.1f'))

ax.tick_params(axis='both', which='major', length=2, width=1, labelsize='18')
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)

#ax.xaxis.set_major_locator(ticker.MultipleLocator(10))
ax.legend(labels, prop={'size':15})

fig.set_size_inches(9,9)

plt.show()
