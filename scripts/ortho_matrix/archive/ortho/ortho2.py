import matplotlib.pyplot as plt
import matplotlib
from matplotlib.colors import LinearSegmentedColormap
import numpy as np
import pandas as pd
import sys
import seaborn as sns; sns.set()
import statistics as stat
import matplotlib.font_manager as mfm
mfm.findSystemFonts(fontpaths=None, fontext='ttf')

sns.set(font_scale=1.5)
plt.rcParams['font.family'] = 'Gargi'
#plt.rcParams['font.freefont'] = 'FreeMono.ttf'
fig,ax = plt.subplots()

generation = sys.argv[1]

#automatically create generation number
gen = str(generation[3])

#list protein names
regulators = ["GLAU"+gen, "NOS"+gen, "PAP"+gen, "ROTU"+gen, "THP"+gen]
if gen == "1":
    first= "First"
elif gen == "2":
    first = "Second"
elif gen == "3":
    first = "Third"
else:
    first = "Fourth"

#list compounds used
compounds = ["Glaucine", "Noscapine", "Papaverine", "Rotundine", "Tetrahydropapaverine"]

#import data
#data = pd.read_csv('gen1ortho.csv')
data = pd.read_csv(generation)


od600 = data.iloc[23:31,1:].astype('float64')
RFU = data.iloc[55:63,1:].astype('float64')

fluo = pd.DataFrame(RFU.values / od600.values)

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



#create new dataframe for standard deviation values
stdOrtho = pd.DataFrame()
#add standev for GLAU, NOS
for i in range(0,6):
    stdOrtho.loc[0,i] = fluo.iloc[0:3,i].std()
    i += 6
    stdOrtho.loc[1,i-6] = fluo.iloc[0:3,i].std()
#add standev for PAP, ROTU
for i in range(0,6):
    stdOrtho.loc[2,i] = fluo.iloc[3:6,i].std()
    i += 6
    stdOrtho.loc[3,i-6] = fluo.iloc[3:6,i].std()
#add standev for THP
for i in range(0,6):
    boo = []
    boo.append(fluo.at[6,i])
    boo.append(fluo.at[7,i]) 
    boo.append(fluo.at[7,i+6])
    stdOrtho.loc[4,i] = stat.stdev(boo)



#create new dataframe for fold change relative to DMSO control
foldOrtho = pd.DataFrame()
#fill in da data!
for n in range(0,5):
    for i in range(0,5): 
        foldOrtho.loc[n,i] = avgOrtho.iloc[n,i]/avgOrtho.iloc[n,5]

#foldOrtho = foldOrtho.T

#custom colormap function
def NonLinCdict(steps, hexcol_array):
    cdict = {'red': (), 'green': (), 'blue': ()}
    for s, hexcol in zip(steps, hexcol_array):
        rgb = matplotlib.colors.hex2color(hexcol)
        cdict['red'] = cdict['red'] + ((s, rgb[0], rgb[0]),)
        cdict['green'] = cdict['green'] + ((s, rgb[1], rgb[1]),)
        cdict['blue'] = cdict['blue'] + ((s, rgb[2], rgb[2]),)
    return cdict

hc = ['#ffffff','#009BFF', '#C100FF']
th = [0,0.1, 1]

cdict = NonLinCdict(th, hc)
cm = LinearSegmentedColormap('test', cdict)

#increase font size by a little
sns.set(font_scale=1.5)

#create seaborn heatmap
ax = sns.heatmap(foldOrtho, vmin=0, vmax= 1000, annot=True,fmt='.0f',yticklabels= regulators, xticklabels= compounds, linewidths=1, linecolor="#7a7a7a", cmap=cm)
#ax.set_title("Orthogonality of " +first+ " Generation Sensors")
plt.yticks(rotation=0)
plt.xticks(rotation=45)
fig.set_size_inches(9,9)

plt.show()



'''
fig, ax = plt.subplots()
index = np.arange(5)
bar_width = 0.18

palette = ['b','r','#000000','c','y']

for i in range(0,5):
    plt.bar(index + i*(bar_width), avgOrtho.iloc[:5,i], bar_width, yerr= stdOrtho.iloc[:5,i], color= palette[i], label= compounds[i])

plt.xlabel('Compound')
plt.ylabel('Fluorescence (RFU/OD600)')
plt.title('Orthogonality of '+first+' Generation Sensors')
plt.xticks(index + 2*(bar_width), regulators)
plt.legend()
plt.tight_layout()
plt.show()
'''
