import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sys
import matplotlib.ticker as ticker
import matplotlib.transforms as transforms
from pathlib import Path
from statistics import mean, stdev

plt.rcParams['font.family'] = 'Gargi'

fig,ax = plt.subplots()

x = [1,2,3,4,5]

#GLAU
#y = [100,100,25,5,1]
#NOS
#y = [100,100,50,25,2.5]
#PAP
#y = [200,200,100,25,2.5]
#ROTU
#y = [100,100,25,10,2.5]
#THP
y = [50,50,5,2,1]

plt.step(x,y, linewidth=3)

plt.xlim(1,5)
plt.ylim(0.5,250)
ax.set_yscale('log')

#plt.ylabel("Glaucine (uM)", fontsize=20)
plt.xlabel("Round of Evolution", fontsize=22)
ax.tick_params(axis='both', which='major', length=2, width=1, labelsize='20')
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.xaxis.set_major_locator(ticker.MaxNLocator(integer=True))

fig.set_size_inches(5,9)

plt.show()
