##import matplotlib.pyplot as plt

## Work the best so far! Curve fits nicely and ymin/ymax don't have to be 0 and 1!

import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

fig,ax = plt.subplots()

def sigmoid(x, a, b, c, d):
    return ((a-b) / (1.0 + np.exp(x - (c)) ** d)) +b

xdata = np.array([0.0, 1.0, 10.0, 100.0, 1000.0])
ydata = np.array([1300, 1300.0, 1691.0, 10479.8, 59064.1])
ydataerr = [120.8, 120.8, 140.0, 160.5, 1181.0]

plt.errorbar(xdata, ydata, yerr=ydataerr, fmt='bo', capsize=5, label="data")

#both initial values work. Doesn't change anything
#popt, pcov = curve_fit(sigmoid, xdata, ydata, p0 = [1.0,1.0,1.0,0.5])
popt, pcov = curve_fit(sigmoid, xdata, ydata, p0 = [1000.0, 65000.0, 150.0, 0.03])

print(*popt)
x = np.linspace(0,2000,1000)

plt.plot(x, sigmoid(x, *popt), 'r-', label='fit')
plt.ylim(0,65000)
plt.ylabel('Fluorescence (RFU/OD600)', fontsize=20)
plt.xlabel('Tetrahydropapaverine (uM)', fontsize=20)
plt.title('RamR response to Tetrahydropapaverine', fontsize=25)

ax.set_xscale('log')
ax.tick_params(axis='both', which='major', labelsize='18')

plt.show()
