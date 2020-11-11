import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import matplotlib.ticker as ticker

plt.rcParams['font.family'] = 'Gargi'

#create figure
fig, ax = plt.subplots()

bar_width = 0.4

palette = ['#DC2EFF', '#FFf92f','#FF2E2E','#00D100', '#FF620E', '#2E6AFF', '#696969', '#EEEEEE']
#y_pos = np.arange(len(labels))


    #Andy's fenchol production sensing stuff
#labels = ['Uninduced', 'Induced']
#avgFluo = [561.2829, 875.071]
#fluo = [554.0, 557.6, 572.1, 908.6, 872.5, 844.0]


labels = ['GLAU', 'NOS', 'PAP', 'ROTU', 'THP']
avgFluo = [1.96607, 1.791983, 1.984816, 4.295868, 12.10484]
fluo = [1.993977, 1.967664, 1.936565, 1.854120, 1.784031, 1.737797, 2.135925, 1.920666, 1.897858, 4.322294, 4.239665, 4.325643, 11.07379, 12.72028, 12.520448]

'''
labels = ['Gf1','Gf2','Gf6','Ps1','Gf1+Gf6','Gf1+Ps1','Gf2+Gf6','Gf2+Ps1']
avgFluo = [8.4811, 4.76963, 1, 1, 13.4647, 17.5908, 5.0405, 5.195594]
fluo = [9.2652, 6.27, 9.91, 4.959, 4.819, 4.53, 1,1,1,1,1,1,14.07, 13.43, 12.89, 17.72, 17.36, 17.684, 4.813, 5.112, 5.1966, 5.174, 5.1767, 5.236]
'''
counter = 0
for i in range(0,5):
    plt.scatter(labels[i], fluo[counter], s=80, color=palette[i], edgecolors='#000000', zorder=1)
    plt.scatter(labels[i], fluo[counter+1], s=80, color=palette[i], edgecolors='#000000', zorder=2)
    plt.scatter(labels[i], fluo[counter+2], s=80, color=palette[i], edgecolors='#000000', zorder=3)
    counter+=3
    plt.bar(labels[i], avgFluo[i], bar_width, color=palette[i], edgecolor='#000000', zorder=0)


plt.xticks(labels, fontsize=16)
plt.xlabel('Benzylisoquinoline Alkaloid', fontsize=16)
plt.ylabel('Fold change in fluorescence', fontsize=16)
plt.title('RamR Response to Various Benzyisoquinoline Alkaloids', fontsize=18)
ax.set_ylim(1,14)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
#ax.tick_params(axis='both', which='major', labelsize=14)
plt.show()
