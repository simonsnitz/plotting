import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import matplotlib.ticker as ticker
import matplotlib.transforms as transforms

plt.rcParams['font.family'] = 'Gargi'

#create figure
fig, ax = plt.subplots()

bar_width = 0.4

#palette = ['#999999', '#999999','#999999','#999999', '#999999', '#2E6AFF', '#999999', '#999999']
palette = ['#DC2EFF', '#fbbe00','#FF2E2E','#00D100', '#FF620E', '#2E6AFF', '#696969', '#EEEEEE']
#y_pos = np.arange(len(labels))


labels = ['GLAU', 'NOS', 'PAP', 'ROTU', 'THP']
avgFluo = [1.96607, 1.791983, 1.984816, 4.295868, 12.10484]
fluo = [1.993977, 1.967664, 1.936565, 1.854120, 1.784031, 1.737797, 2.135925, 1.920666, 1.897858, 4.322294, 4.239665, 4.325643, 11.07379, 12.72028, 12.520448]

counter = 0

offset = lambda p: transforms.ScaledTranslation(p/72.0, 0, plt.gcf().dpi_scale_trans)
trans = plt.gca().transData

for i in range(0,5):
    plt.scatter(labels[i], fluo[counter], s=120, facecolor="None",edgecolors='#000000', zorder=1, linewidth=2.5, transform=trans+offset(-10))
    plt.scatter(labels[i], fluo[counter+1], s=120, facecolor="None", edgecolors='#000000', zorder=2, linewidth=2.5)
    plt.scatter(labels[i], fluo[counter+2], s=120, facecolor="None", edgecolors='#000000', zorder=3, linewidth=2.5, transform=trans+offset(10))
    counter+=3
    plt.bar(labels[i], avgFluo[i], bar_width, color=palette[i], edgecolor='#000000', zorder=0, linewidth=4)

plt.xticks(labels, fontsize=16)
plt.xlabel('Benzylisoquinoline Alkaloid', fontsize=18)
plt.ylabel('Fold change in fluorescence', fontsize=18)
plt.title('RamR Response to Variuos Benzylisoquinoline Alkaloids', fontsize=24)
ax.set_ylim(0,14)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.tick_params(axis='both', which='major', labelsize=16)
plt.show()
