import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import matplotlib.ticker as ticker
import matplotlib.transforms as transforms
import numpy as np

plt.rcParams['font.family'] = 'Gargi'

#create figure
fig, ax = plt.subplots()

bar_width = 0.3

#palette = ['#999999', '#999999','#999999','#999999', '#999999', '#2E6AFF', '#999999', '#999999']
#palette = ['#DC2EFF', '#FFf92f','#FF2E2E','#00D100', '#FF620E', '#2E6AFF', '#696969', '#EEEEEE']
#y_pos = np.arange(len(labels))


    #Andy's fenchol production sensing stuff
#labels = ['Uninduced', 'Induced']
#avgFluo = [561.2829, 875.071]
#fluo = [554.0, 557.6, 572.1, 908.6, 872.5, 844.0]


labels = ['TAA', 'WT', 'Gen1', 'Gen2', 'Gen3', 'Gen4', 'Gen5']
#labels = ['TAA', '4OMT', '6OMT', 'EcOMT', 'PbOMT', 'Gf1OMT', 'Gf2OMT', 'Gf6OMT']
x = np.arange(len(labels))

avg0 = [847, 882, 1017, 1167, 1226, 1291, 1138]
avg10 = [880, 1177, 1976, 7202, 31048, 50866, 55083]
avg100 = [923, 11665, 20327, 23961, 46134, 63169, 69933]

avg0err = [8.92, 7.16, 12.27, 1.03, 12.36, 22.17, 27.82]
avg10err = [11.31, 32.03, 82.31, 263.1, 1772, 1572, 958.3]
avg100err = [34.72, 962.1, 1220, 1267, 431.8, 829.5, 432.7]


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
'''
for i in range(0,7):
    #plt.scatter(labels[i], fluo[counter], s=120, facecolor="None",edgecolors='#000000', zorder=1, linewidth=2.5, transform=trans+offset(-10))
    #plt.scatter(labels[i], fluo[counter+1], s=120, facecolor="None", edgecolors='#000000', zorder=2, linewidth=2.5)
    #plt.scatter(labels[i], fluo[counter+2], s=120, facecolor="None", edgecolors='#000000', zorder=3, linewidth=2.5, transform=trans+offset(10))
    counter+=3
    plt.bar(x-bar_width/3, avg0[i], bar_width, labels[i], color=palette[i], edgecolor='#000000', zorder=0, linewidth=4)
    plt.bar(x, avg10[i], bar_width, labels[i],color=palette[i], edgecolor='#000000', zorder=0, linewidth=4)
    plt.bar(x+bar_width/3, avg100[i], bar_width, labels[i],color=palette[i], edgecolor='#000000', zorder=0, linewidth=4)
'''
plt.bar(x- bar_width, avg0, bar_width, label="0uM", edgecolor='#000000', color="#0872fc", zorder=0, linewidth=2, yerr=avg0err, error_kw=dict(lw=2, capsize=5, capthick=2))
plt.bar(x, avg10, bar_width, label="10uM", edgecolor='#000000', color="#fcaf08", zorder=0, linewidth=2, yerr=avg10err, error_kw=dict(lw=2, capsize=5, capthick=2))
plt.bar(x+ bar_width, avg100, bar_width, label="100uM", edgecolor='#000000', color="#fc0808", zorder=0, linewidth=2, yerr=avg100err, error_kw=dict(lw=2, capsize=5, capthick=2))


ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.set_xlabel('O-Methyltransferase', fontsize=18)
ax.set_ylabel('Fluorescence (RFU/OD)', fontsize=18)
plt.title('Activity Screening of Evolved OMTs with a THP Biosensor', fontsize=18)

#ax.set_ylim(0,18)
ax.legend(prop={'size':15})

ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.tick_params(axis='both', which='major', labelsize=16)
fig.tight_layout()

plt.show()
