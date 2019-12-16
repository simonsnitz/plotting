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

#trash code for generating labels. Labels array is hard coded :/
labels = ['WT','NOS1','NOS2','NOS3','NOS4']
avgLabels = list(range(0,len(labels)))
for i in range(0,len(labels)):
    avgLabels[i] = labels[i]+'avg'

#Add new columns for variants fluorescence averages. Numbers 5 and 12 are hard coded here :/
numCon = list(range(0,12))
for i in range(0,5):
    data[avgLabels[i]] = numCon

#print(data.loc[0:,'WT1'])
#print(data.iloc[0:,0])

#Fill in data for average values. 1st identifiers can be abstracted. 2nd will be a bit harder.
for i in numCon:
    data.loc[i,'WTavg'] = data.loc[i, 'WT1':'WT3'].mean()
    data.loc[i,'NOS1avg'] = data.loc[i, 'NOS1-1':'NOS1-3'].mean()
    data.loc[i,'NOS2avg'] = data.loc[i, 'NOS2-1':'NOS2-3'].mean()
    data.loc[i,'NOS3avg'] = data.loc[i, 'NOS3-1':'NOS3-3'].mean()
    data.loc[i,'NOS4avg'] = data.loc[i, 'NOS4-1':'NOS4-3'].mean()


xdata = data.iloc[:,0]
#loop through this part
#for i in ___:
ydata = data['NOS3avg']

'''
#example data
xdata = np.array([0.0, 1.0, 10.0, 100.0, 1000.0])
ydata = np.array([1300, 1300.0, 1691.0, 10479.8, 59064.1])
ydataerr = [120.8, 120.8, 140.0, 160.5, 1181.0]
#set error bars
plt.errorbar(xdata, ydata, yerr=ydataerr, fmt='bo', capsize=5, label="data")
'''

#define sigmoid function
def sigmoid(x, a, b, c, d):
    return ((a-b) / (1.0 + np.exp(x - (c)) ** d)) +b


#Run curve_fit function
#both initial values work. Doesn't change anything
#popt, pcov = curve_fit(sigmoid, xdata, ydata, p0 = [1.0,1.0,1.0,0.5])
popt, pcov = curve_fit(sigmoid, xdata, ydata, p0 = [1.0, 70000.0, 1.0, 1.0])
x = np.linspace(0,20000,100000)
print(pcov)

#Plot fitted sigmoid function
plt.plot(x, sigmoid(x, *popt), 'r-', label='fit')

'''
popt, pcov = curve_fit(sigmoid, xdata, ydata, p0 = [1.0, 65000.0, 1.0, 0.03])
plt.plot(x, sigmoid(x, *popt), 'g-', label='fit')
ydata = data['NOS2avg']
popt, pcov = curve_fit(sigmoid, xdata, ydata, p0 = [1.0, 65000.0, 1.0, 0.03])
plt.plot(x, sigmoid(x, *popt), 'b-', label='fit')
ydata = data['NOS3avg']
popt, pcov = curve_fit(sigmoid, xdata, ydata, p0 = [1.0, 65000.0, 1.0, 0.03])
plt.plot(x, sigmoid(x, *popt), 'y-', label='fit')
ydata = data['NOS4avg']
popt, pcov = curve_fit(sigmoid, xdata, ydata, p0 = [1.0, 65000.0, 1.0, 0.03])
plt.plot(x, sigmoid(x, *popt), 'c-', label='fit')
'''

#plot individual data points
    #set x axis
lig = data.iloc[:,0]
    #loop through this part. need array of names and array of colors for dots.
plt.plot(lig, data.loc[:,'NOS3-1'], 'bo')
plt.plot(lig, data.loc[:,'NOS3-2'], 'bo')
plt.plot(lig, data.loc[:,'NOS3-3'], 'bo')

plt.xlim(0.05,200)
plt.ylim(-1000,80000)
plt.ylabel('Fluorescence (RFU/OD600)', fontsize=20)
#pull compound name from data frame
plt.xlabel('Noscapine (uM)', fontsize=20)
plt.title('RamR response to Noscapine', fontsize=25)
ax.set_xscale('log')
ax.tick_params(axis='both', which='major', labelsize='18')

plt.show()
