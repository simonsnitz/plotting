import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import matplotlib.ticker as ticker
import matplotlib.transforms as transforms

plt.rcParams['font.family'] = 'Gargi'

#create figure
fig, ax = plt.subplots()

bar_width = 0.4

palette = ['#999999', '#999999','#999999','#999999', '#999999', '#2E6AFF', '#999999', '#999999']
#palette = ['#DC2EFF', '#FFf92f','#FF2E2E','#00D100', '#FF620E', '#2E6AFF', '#696969', '#EEEEEE']
#y_pos = np.arange(len(labels))


    #Andy's fenchol production sensing stuff
#labels = ['Uninduced', 'Induced']
#avgFluo = [561.2829, 875.071]
#fluo = [554.0, 557.6, 572.1, 908.6, 872.5, 844.0]


labels = ['TAA', 'OMT1', 'OMT2', 'OMT3', 'OMT4', 'OMT5', 'OMT6', 'OMT7']
#labels = ['TAA', '4OMT', '6OMT', 'EcOMT', 'PbOMT', 'Gf1OMT', 'Gf2OMT', 'Gf6OMT']
avgFluo = [1.0, 10.22, 1.19, 3.11, 2.0, 15.43, 1.92, 1.00]
#fluo = [1.993977, 1.967664, 1.936565, 1.854120, 1.784031, 1.737797, 2.135925, 1.920666, 1.897858, 4.322294, 4.239665, 4.325643, 11.07379, 12.72028, 12.520448]
fluo = [1,1,1,9.78, 10.35, 10.53, 1.15, 1.18, 1.24, 3.09, 3.02, 3.21, 2.10, 2.09, 1.83, 15.43, 15.40, 15.55, 1.88, 1.93, 1.96, 1, 1, 1.02]

'''
labels = ['Gf1','Gf2','Gf6','Ps1','Gf1+Gf6','Gf1+Ps1','Gf2+Gf6','Gf2+Ps1']
avgFluo = [8.4811, 4.76963, 1, 1, 13.4647, 17.5908, 5.0405, 5.195594]
fluo = [9.2652, 6.27, 9.91, 4.959, 4.819, 4.53, 1,1,1,1,1,1,14.07, 13.43, 12.89, 17.72, 17.36, 17.684, 4.813, 5.112, 5.1966, 5.174, 5.1767, 5.236]
'''
counter = 0

offset = lambda p: transforms.ScaledTranslation(p/72.0, 0, plt.gcf().dpi_scale_trans)
trans = plt.gca().transData

for i in range(0,8):
    plt.scatter(labels[i], fluo[counter], s=120, facecolor="None",edgecolors='#000000', zorder=1, linewidth=2.5, transform=trans+offset(-10))
    plt.scatter(labels[i], fluo[counter+1], s=120, facecolor="None", edgecolors='#000000', zorder=2, linewidth=2.5)
    plt.scatter(labels[i], fluo[counter+2], s=120, facecolor="None", edgecolors='#000000', zorder=3, linewidth=2.5, transform=trans+offset(10))
    counter+=3
    plt.bar(labels[i], avgFluo[i], bar_width, color=palette[i], edgecolor='#000000', zorder=0, linewidth=4)

plt.xticks(labels, fontsize=16)
plt.xlabel('O-Methyltransferase', fontsize=18)
plt.ylabel('Fold change in fluorescence', fontsize=18)
plt.title('Activity Screening of OMTs with a THP Biosensor', fontsize=24)
ax.set_ylim(0,18)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.tick_params(axis='both', which='major', labelsize=16)
plt.show()
