## Work the best so far! Curve fits nicely and ymin/ymax don't have to be 0 and 1!

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.optimize import curve_fit
import sys
import matplotlib.ticker as ticker
import matplotlib.transforms as transforms

plt.rcParams['font.family'] = 'Gargi'

dataSheet = sys.argv[1]

#create figure
fig,ax = plt.subplots()

#create a dataframe
dfe = pd.DataFrame()
#data = pd.read_csv("testData.csv")
data = pd.read_csv(str(dataSheet))

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


#create new dataframe for standard deviation values
stdBkgrd = pd.DataFrame()

# ?or not?



#'''

#define sigmoid function
#def sigmoid(x, a, b, c, d):
#    return ((a-b) / (1.0 + np.exp(x - (c)) ** d)) +b

#Hill sigmoid function
def sigmoid(x, a, b, c):
        return a * np.power(x,b) / (np.power(c,b) + np.power(x,b))

x = np.linspace(0,100,100000)
xdata = data.iloc[:,0]
colors = ['#0099ff','#3372cc','#674c9a','#9a2667','#ce0035']
colorLines = []
for i in colors:
    colorLines.append(str(i)+'-')
colorDots = []
for i in colors:
    dot = str(i)
    colorDots.append(dot)
    colorDots.append(dot)
    colorDots.append(dot)
print(colorDots)

#Loop through mutants and plot fitted sigmoid functions
#initParam = np.array([1.0,0.93,1.0])
initParam = np.array([1.0,1.0,5.0])
counter = 0
for i in avgLabels:
    popt, pcov = curve_fit(sigmoid, xdata, data[i],initParam,  maxfev=5000)
            #p0 = [1.0, 20000.0, 0.01, 1.0])
    plt.plot(x, sigmoid(x, *popt), color = colors[counter], label='fit')
    counter += 1
    #print(popt)


#print(data.columns.values)
lig = data.iloc[:,0]
#colorDots = ['bo','bo','bo','go','go','go','ro','ro','ro','co','co','co','yo','yo','yo']



for i in range(1,16):
    variant = data.columns.values[i]
    plt.plot(lig, data.loc[:,variant],color = colorDots[i-1], marker='o', linestyle='None')

#extract compound name from data frame
compound = str(data.columns.values[0])

plt.xlim(0.05,300)
plt.ylim(0,75000)
plt.ylabel('Fluorescence (RFU/OD600)', fontsize=20)
plt.xlabel(compound+' (uM)', fontsize=20)
plt.title('RamR variant response to '+compound, fontsize=25)
#should be symlog, but tick spacing gets screwed up
ax.set_xscale('log')
ax.tick_params(axis='both', which='major', length=2, width=1, labelsize='18')
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)

#ax.xaxis.set_major_locator(ticker.MultipleLocator(10))
ax.legend(labels, prop={'size':15})

plt.show()
'''


#script for plotting background bar charts

#fig, ax = plt.subplots()
#index = np.arange(5)
bar_width = 0.5

if labels[1] == "NOS1":
    palette = ['#fbbe00', '#fbbe00', '#FBBE00', '#fbbe00', '#fbbe00']
elif labels[1] == "PAP1":
    palette = ['#ff2e2e', '#ff2e2e', '#ff2e2e', '#FF2E2E', '#ff2e2e']
elif labels[1] == "THP1":
    palette = ['#ff620e', '#ff620e', '#ff620e', '#ff620e', '#ff620e']
elif labels[1] == "GLAU1":
    palette = ['#dc2eff', '#dc2eff', '#dc2eff', '#dc2eff', '#DC2EFF']
elif labels[1] == "ROTU1":
    palette = ['#00d100', '#00D100', '#00d100', '#00d100', '#00d100']
 

avgBkgrd = data.iloc[0][17:]
dots = data.iloc[0][1:16]

offset = lambda p: transforms.ScaledTranslation(p/72.0, 0, plt.gcf().dpi_scale_trans)
trans = plt.gca().transData

counter = 0
for i in range(0,5):
    plt.scatter(labels[i],dots[counter], s=120, facecolor="None", edgecolors='#000000', zorder=1, linewidth=2.5, transform=trans+offset(-10))
    plt.scatter(labels[i],dots[counter+1], s=120, facecolor="None", edgecolors='#000000', zorder=2, linewidth=2.5)
    plt.scatter(labels[i],dots[counter+2], s=120, facecolor="None", edgecolors='#000000', zorder=3, linewidth=2.5, transform=trans+offset(10))
    counter+= 3                
    plt.bar(labels[i], avgBkgrd[i], bar_width, color= palette[i], label= labels[i], edgecolor="#000000", linewidth=4, zorder=0)

plt.xlabel('RamR variant', fontsize=16)
plt.ylabel('Fluorescence (RFU/OD600)', fontsize=16)
plt.title('Transcriptional leak of evolved RamR variants', fontsize=18)

#leg = plt.legend()


ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.tick_params(axis='both', which='major', labelsize=14)
plt.show()
'''



#print(data.iloc[0][17:])
