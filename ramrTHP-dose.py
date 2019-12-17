##import matplotlib.pyplot as plt

## Work the best so far! Curve fits nicely and ymin/ymax don't have to be 0 and 1!

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.optimize import curve_fit

#create figure
fig,ax = plt.subplots()

#create a dataframe
dfe = pd.DataFrame()
data = pd.read_csv("testData.csv")


#calculate the background
bkgrd = data.loc[:,"DH10B"].mean()


#Dannys more readable, more robust, faster (uses C++) code
#def rm_background(col, background, skip=['Noscapine', 'DH10B']):
#    if col in skip:
#        return col
#    return col - background
#
#new_df = data.apply(lambda x: rm_background(x,bkgrd))


#update dataframe by subtracting background from each value           Assumes DH10B column is last column.
for i in range(1,len(data.iloc[0]) -1):
    col = data.iloc[:,i]
    for n in range(0,len(col)):
        data.iloc[:,i][n] = col[n]-bkgrd

#Generate variant name labels from column labels. Loop array values are hard-coded, assume we have WT and 4 mutants to compare. Can change later...
labels = []
for i in [1,4,7,10,13]:
    labels.append(data.columns.values[i][:-2])

#Generate 'average' variant labels.
avgLabels = list(range(0,len(labels)))
for i in range(0,len(labels)):
    avgLabels[i] = labels[i]+'avg'

#Add new columns for variant's fluorescence averages. Numbers 5 and 12 are hard coded here, assumes you have WT and 4 mutants, 12 concentrations.
numCon = list(range(0,12))
for i in range(0,5):
    data[avgLabels[i]] = numCon

#create an array of labels used to generate mean. For example ['WT-1','WT-3', ...]
meanLabels = []
for i in [1,3,4,6,7,9,10,12,13,15]:
    meanLabels.append(data.columns.values[i])
#Fill in data for average values. Abstracted! Assumes you have 3 data points you're averaging.
for i in numCon:
    counter = 0
    for n in range(0,len(avgLabels)):
        data.loc[i,avgLabels[n]] = data.loc[i,meanLabels[counter]:meanLabels[(counter+1)]].mean()
        counter += 2

#define sigmoid function
def sigmoid(x, a, b, c, d):
    return ((a-b) / (1.0 + np.exp(x - (c)) ** d)) +b

x = np.linspace(0,20000,100000)
xdata = data.iloc[:,0]
colorLines = ['b-','g-','r-','c-','y-']
#Loop through mutants and plot fitted sigmoid functions
counter = 0
for i in avgLabels:
    popt, pcov = curve_fit(sigmoid, xdata, data[i], p0 = [1.0, 65000.0, 1.0, 0.03])
    plt.plot(x, sigmoid(x, *popt), colorLines[counter], label='fit')
    counter += 1


#print(data.columns.values)
lig = data.iloc[:,0]
colorDots = ['bo','bo','bo','go','go','go','ro','ro','ro','co','co','co','yo','yo','yo']
for i in range(1,16):
    variant = data.columns.values[i]
    plt.plot(lig, data.loc[:,variant],colorDots[i-1])

'''
#plot individual data points
    #set x axis
lig = data.iloc[:,0]
    #loop through this part. need array of names and array of colors for dots.
plt.plot(lig, data.loc[:,'NOS3-1'], 'bo')
plt.plot(lig, data.loc[:,'NOS3-2'], 'bo')
plt.plot(lig, data.loc[:,'NOS3-3'], 'bo')
'''
#extract compound name from data frame
compound = str(data.columns.values[0])

plt.xlim(0.05,200)
plt.ylim(-1000,80000)
plt.ylabel('Fluorescence (RFU/OD600)', fontsize=20)
plt.xlabel(compound+' (uM)', fontsize=20)
plt.title('RamR response to '+compound, fontsize=25)
ax.set_xscale('log')
ax.tick_params(axis='both', which='major', labelsize='18')

plt.show()
