import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sys
import seaborn as sns; sns.set()

data = pd.read_csv('gen1ortho.csv')

od600 = data.iloc[23:31,1:].astype('float64')
RFU = data.iloc[55:63,1:].astype('float64')

fluo = pd.DataFrame(RFU.values / od600.values)

compounds = ['GLAU','NOS','PAP','ROTU','THP','DMSO']

#calculate and subtract background from entire dataframe
bkgrd = fluo.iloc[6,6:].mean()
fluo = fluo.subtract(bkgrd)

#create new dataframe for average values
avgOrtho = pd.DataFrame()

#add averages for GLAU, NOS
for i in range(0,6):
    avgOrtho.loc[0,i] = fluo.iloc[0:3,i].mean()
    i += 6
    avgOrtho.loc[1,i-6] = fluo.iloc[0:3,i].mean()
#add averages for PAP, ROTU
for i in range(0,6):
    avgOrtho.loc[2,i] = fluo.iloc[3:6,i].mean()
    i += 6
    avgOrtho.loc[3,i-6] = fluo.iloc[3:6,i].mean()
#add averages for THP
for i in range(0,6):
    boo = []
    boo.append(fluo.at[6,i])
    boo.append(fluo.at[7,i]) 
    boo.append(fluo.at[7,i+6])
    avgOrtho.loc[4,i] = (sum(boo)/3)

#create new dataframe for fold change relative to DMSO control
foldOrtho = pd.DataFrame()

for n in range(0,5):
    for i in range(0,5): 
        foldOrtho.loc[n,i] = avgOrtho.iloc[n,i]/avgOrtho.iloc[n,5]

#print(foldOrtho)

ax = sns.heatmap(foldOrtho,annot=True, cmap="Blues")
        #"YlGnBu")
plt.show()
