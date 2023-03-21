import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sys
import matplotlib.ticker as ticker
import matplotlib.transforms as transforms
from pathlib import Path
import math
from statistics import mean, stdev
import seaborn as sns

from plotting_functions import *

#create figure and set font
fig, ax = plt.subplots()
plt.rcParams['font.family'] = 'Gargi'

    #import data
d = pd.read_excel(sys.argv[1], )



# columns = [i for i in data.columns]

sns.violinplot( data=d, inner=None)
sns.swarmplot( data=d, color="#000000", alpha=0.8)

min_y = 0
max_y = 130
ax.set_ylim([min_y,max_y])

ax.tick_params(axis='y', which='major', length=2, width=1, labelsize=16)
ax.tick_params(axis='x', which='major', length=2, width=1, labelsize=16)

fig.set_size_inches(14,5)
plt.show()