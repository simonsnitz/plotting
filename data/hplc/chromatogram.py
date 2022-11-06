import matplotlib.pyplot as plt
import sys

data = sys.argv[1]

with open(data) as d:
    d = d.read().split("\n")
    allData = d[43:]

    x = [float(allData[i].split('\t')[0]) for i in range(0,len(allData)-1)]
    y = [float(allData[i].split('\t')[2]) for i in range(len(allData)-1)]

        #filter by time
    totalPoints = len(allData)
    start = int(totalPoints*0.11)
    end = int(totalPoints*0.36)


    x = x[start:end]
    y = y[start:end]
    
    #print(len(allData))
    #print(y)

    fig, ax = plt.subplots()
    fig.set_size_inches(12,4)
    plt.xticks(fontsize=18)
    #ax.set_ylim([0,35])
    plt.xlabel("Time (minute)", fontsize=18)
    plt.yticks([])
    plt.plot(x, y, color='#26baff', linewidth=3)

    plt.show()