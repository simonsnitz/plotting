import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import matplotlib.ticker as ticker
import matplotlib.transforms as transforms
import numpy as np
from pathlib import Path
from statistics import mean, stdev

plt.rcParams['font.family'] = 'Gargi'


p = Path('../../data')
dataSheet = p / "OMT_evolution_data.csv"

#change this?
bar_width = 0.3

#create figure
fig, ax = plt.subplots()

#load data from csv
data = pd.read_csv(str(dataSheet))

#set graph and axis titles
title = data.iloc[0][1]
xtitle = data.iloc[1][1]
ytitle = data.iloc[2][1]

#set X-axis condition labels
xlabels = data.loc[3:]['Label'].values
x = np.arange(len(xlabels))


#set legend labels
iterArray = [1+x*3 for x in range(0,int(len(data.columns[1:])/3))]
legendLabels = [data.columns[x] for x in iterArray]

avgFluo = []
avgFluoErr = []

for i in iterArray:
    avg =  [mean([float(x) for x in data.iloc[y][i:i+3].values]) 
        for y in range(3,len(xlabels)+3)]
    avgFluo.append(avg)

    avgErr =  [stdev([float(x) for x in data.iloc[y][i:i+3].values]) 
        for y in range(3,len(xlabels)+3)]
    avgFluoErr.append(avgErr)


offset = lambda p: transforms.ScaledTranslation(p/72.0, 0, plt.gcf().dpi_scale_trans)
trans = plt.gca().transData


bar = [-bar_width,0,bar_width]
colors = ["#0872fc","#fcaf08","#fc0808"]

for i in range(0,len(avgFluo)):
    plt.bar(x+ bar[i], avgFluo[i], bar_width, label=legendLabels[i], edgecolor='#000000', color=colors[i], zorder=0, linewidth=2, yerr=avgFluoErr[i], error_kw=dict(lw=2, capsize=5, capthick=2))


ax.set_xticks(x)
ax.set_xticklabels(xlabels)
ax.set_xlabel(xtitle, fontsize=18)
ax.set_ylabel(ytitle, fontsize=18)
plt.title(title, fontsize=18)

ax.legend(prop={'size':15})

ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.tick_params(axis='both', which='major', labelsize=16)
fig.tight_layout()

plt.show()

