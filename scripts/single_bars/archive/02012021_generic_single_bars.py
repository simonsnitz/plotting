import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sys
import matplotlib.ticker as ticker
import matplotlib.transforms as transforms
from pathlib import Path

#set font
plt.rcParams['font.family'] = 'Gargi'

#create figure
fig, ax = plt.subplots()

#import data
dataSheet = sys.argv[1]

#p = Path('../../data/single_bars')
#dataSheet = p / "OMT_screen_data.csv"

#change this?
bar_width = 0.4

#create a dataframe
dfe = pd.DataFrame()
#load metadata from excel file
metadata = pd.read_excel(dataSheet, sheet_name="metadata")

#data = pd.read_csv(dataSheet)

#set graph and axis titles
title = metadata.loc[0,"Title"]
xtitle = metadata.loc[0,"Xtitle"]
ytitle = metadata.loc[0,"Ytitle"]
#colors = metadata.loc[:,"Colors"].values

#title = data.iloc[0][1]
#xtitle = data.iloc[1][1]
#ytitle = data.iloc[2][1]

labels = data.loc[3:]['Label'].values

avgFluo = data.mean(axis=1)[3:].values
avgFluoErr = data.std(axis=1)[3:].values


maxFluo = max(avgFluo)

fluo = []

for i in range(3,(len(labels)+3)):
    for x in data.iloc[i][1:]:
        fluo.append(float(x))

counter = 0

offset = lambda p: transforms.ScaledTranslation(p/72.0, 0, plt.gcf().dpi_scale_trans)
trans = plt.gca().transData

for i in range(0,len(labels)):
    
    plt.scatter(labels[i], fluo[counter], s=120, facecolor="None",edgecolors='#000000', zorder=1, linewidth=2.5, transform=trans+offset(-10))
    
    plt.scatter(labels[i], fluo[counter+1], s=120, facecolor="None", edgecolors='#000000', zorder=2, linewidth=2.5)
    
    plt.scatter(labels[i], fluo[counter+2], s=120, facecolor="None", edgecolors='#000000', zorder=3, linewidth=2.5, transform=trans+offset(10))
    counter+=3

    plt.bar(labels[i], avgFluo[i], bar_width, color=(0,0,1,(avgFluo[i]/maxFluo)**2), edgecolor='#000000', zorder=0, linewidth=4, yerr=avgFluoErr[i], error_kw=dict(lw=2, capsize=5, capthick=2))


plt.xticks(labels, fontsize=16)
plt.xlabel(xtitle, fontsize=18)
plt.ylabel(ytitle, fontsize=18)
plt.title(title, fontsize=24)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.tick_params(axis='both', which='major', labelsize=16)

plt.show()

