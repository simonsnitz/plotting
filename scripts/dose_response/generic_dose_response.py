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

plt.rcParams['font.family'] = 'Gargi'

p = Path('../../data/dose_response')

#this part changes
dataSheet = p / "NOSdata_new.xlsx"

#create figure
fig, ax = plt.subplots()

#load data from xlsx file
data = pd.read_excel(dataSheet, sheet_name=0)
metadata = pd.read_excel(dataSheet, sheet_name=1)

#extract useful metadata
title = metadata.loc[0,"Title"]
Xtitle = metadata.loc[0,"Xtitle"]
Ytitle = metadata.loc[0,"Ytitle"]
colors = metadata.loc[:,"Colors"].values

max_val = 10**(len(str(int(data.max().max())))-1)

#calculate the background.
bkgrd = data.loc[:,"DH10B"].mean()

#update dataframe by subtracting background from each value           
    #Assumes DH10B column is last column.
for i in range(1,len(data.iloc[0]) -1):
    col = data.iloc[:,i]
    for n in range(0,len(col)):
        data.iloc[:,i][n] = (col[n]-bkgrd)/max_val


#create an array for the number of biosensors you're comparing
iterArray = [1+x*3 for x in range(0,int(len(data.columns[1:])/3))]

#Generate variant name labels from column labels. remove last two characters
labels = [data.columns.values[i][:-2] for i in iterArray]

#Summarizing statistics. Create 2 list of lists. One with averages data, the other with standard deviation data.
avgFluo = []
avgFluoErr = []
for i in iterArray:
    avg =  [mean([float(x) for x in data.iloc[y][i:i+3].values]) 
        for y in range(0,8+4)]
    avgFluo.append(avg)

    avgErr =  [stdev([float(x) for x in data.iloc[y][i:i+3].values]) 
        for y in range(0,8+4)]
    avgFluoErr.append(avgErr)


#Hill sigmoid function
def sigmoid(x, a, b, c):
        return a * np.power(x,b) / (np.power(c,b) + np.power(x,b))

#create x-axis ticks. large number in 3rd position of linspace "100,000" needed to avoid choppy line.
x = np.linspace(0,100,100000)

#set array for x-axis (ligand concentration)
xdata = data.iloc[:,0]

#create list of colors for dots (individual data points)
    #still working on making this list with list comprehension
colorDots = []
for i in colors:
    colorDots.append(str(i))
    colorDots.append(str(i))
    colorDots.append(str(i))

#Loop through mutants and plot fitted sigmoid functions. May need to change these parameters.
#initParam = np.array([1.0,0.93,1.0])
initParam = np.array([1.0,0.9,5.0])

#plot curve_fit line based on averages data
for i in range(0,len(labels)):
    popt, pcov = curve_fit(sigmoid, xdata, avgFluo[i],initParam,  maxfev=10000)
    plt.plot(x, sigmoid(x, *popt), color = colors[i], label='fit')
    #plt.bar(xdata,avgFluo[i], yerr=avgFluoErr[i],visible=False, color='black', error_kw=dict(lw=1,capsize=3,capthick=1), label="error")

#plot individual data points as dots
numColumns = len(data.columns)
for i in range(1,numColumns-1):
    variant = data.columns.values[i]
    plt.plot(xdata, data.loc[:,variant],color = colorDots[i-1], marker='o', linestyle='None')

#Extend the xaxis max and min limits to give space on xaxis
xaxis_max = float(data.iloc[-1,0])*2
xaxis_min = float(data.iloc[1,0])/2

plt.xlim(xaxis_min, xaxis_max)
plt.ylabel(Ytitle, fontsize=20)
plt.xlabel(Xtitle, fontsize=20)
plt.title(title, fontsize=25)
#should be symlog, but tick spacing gets screwed up
ax.set_xscale('log')
ax.tick_params(axis='both', which='major', length=2, width=1, labelsize='18')
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)

#ax.xaxis.set_major_locator(ticker.MultipleLocator(10))
ax.legend(labels, prop={'size':15})

fig.set_size_inches(12,9)

plt.show()
