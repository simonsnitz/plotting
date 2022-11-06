import pandas as pd
import numpy as np
import math
from statistics import mean, stdev
import warnings 

pd.options.mode.chained_assignment = None

def load_data(dataSheet):
    metadata = pd.read_excel(dataSheet, sheet_name="metadata")
    fluorescence = pd.read_excel(dataSheet, sheet_name="fluorescence")
    od600 = pd.read_excel(dataSheet, sheet_name="od600")
    #raise value error if sheet wrong
    return metadata, fluorescence, od600


def divide_rfu_od(fluorescence, od600):
    data = pd.DataFrame().reindex_like(fluorescence)

    for i in list(fluorescence.keys()):
        try:
            data[i] = fluorescence[i]/od600[i]
        except:
            data[i] = fluorescence[i]
    
    return data


def set_titles_labels(metadata, data):
    title = metadata.loc[0,"Title"]
    xtitle = metadata.loc[0,"Xtitle"]
    ytitle = metadata.loc[0,"Ytitle"]
        #set X-axis condition labels
    xlabel_name =  data.columns[0]
    xlabels = data.loc[0:][xlabel_name].dropna().values
        #set number X-axis conditions
    x = np.arange(len(xlabels))

    if xlabel_name == "Construct" or xlabel_name == "Time":
        return title, xtitle, ytitle, xlabels, x
    else:
        return title, xtitle, ytitle, xlabels


def set_colors(metadata, labels):
    colors = metadata.loc[:,"Colors"].dropna().values
    
    if len(colors) == 1:
        colors = [colors[0]]*(len(labels))
    elif len(colors) != len(labels):
        warnings.warn("Invalid number of colors given. Need to provide one color or number equivalent to number of conditions. Default color set to boring blue", stacklevel=2)
        colors = ["#12b0ff"]*len(labels)
    return colors



def simplify_yaxis(ytitle, data):
    if ytitle == "Fluorescence (RFU/OD)" or "(RFU/OD)":
        max_val = 10**(len(str(int(data.iloc[:,1:-1].max().max())))-1)
        log10 = int(math.log10(max_val))
        ytitle = r'$(RFU/OD) \times 10^' + str(log10) +'$'

    elif ytitle == "Fold change in fluorescence":
        max_val = 1
    else:
        raise ValueError("y-axis title must be 'Fluorescence (RFU/OD)', '(RFU/OD)', or 'Fold change in fluorescence'")
    for i in range(1,len(data.iloc[0]) -1):
        col = data.iloc[:,i]
        for n in range(0,len(col)):
            data.iloc[:,i][n] = col[n]/max_val

    return ytitle, data


def get_num_replicates(data):
    last_char = [ x[-1] for x in data.columns.values]
    num_reps = []
    for i in last_char:
        try:
            num_reps.append(int(i))
        except:
            pass
    num_reps = max(num_reps)

    return num_reps
    

def create_avg_std_indiv_lists(iterArray, data, num_reps, xlabels):
    fluo = []
    if len(iterArray) > 1:
        avgFluo = []
        avgFluoErr = []
        for i in iterArray:
            avg =  [mean([float(x) for x in data.iloc[y][i:i+num_reps].values if str(x) != "nan"]) 
                for y in range(0,len(xlabels))]
            avgFluo.append(avg)
    
            if num_reps > 1:
                avgErr =  [stdev([float(x) for x in data.iloc[y][i:i+num_reps].values if str(x) != "nan"])               for y in range(0,len(xlabels))]
                avgFluoErr.append(avgErr)

                for j in data.iloc[0:].values:
                    for k in list(j[i:i+3]):
                        fluo.append(float(k))
            else:
                num = len(avgFluo)
                avgFluoErr = [0]*num 
                fluo = [0]*num

    else:
        avgFluo =  [mean([float(x) for x in data.iloc[y][1:1+num_reps].values if str(x) != "nan"]) 
            for y in range(0,len(xlabels))]
    
        avgFluoErr =  [stdev([float(x) for x in data.iloc[y][1:1+num_reps].values if str(x) != "nan"])             for y in range(0,len(xlabels))]
        
        for i in data.iloc[0:].values:
            for j in list(i[1:1+num_reps]):
                fluo.append(float(j))

    return avgFluo, avgFluoErr, fluo

    #must have "DMSO" control. add flexibility to include non-dmso controls
def create_fold_df(iterArray, data, num_reps, xlabels, ylabels):
    
    averages = pd.DataFrame()

    counter = 0
    for i in iterArray:
        avg =  [mean([float(x) for x in data.iloc[y][i:i+num_reps].values if str(x) != "nan"]) 
            for y in range(0,len(xlabels))]
            
        averages[ylabels[counter]] = avg
        counter += 1

        #create dataframe for fold change
    fold = pd.DataFrame()
        #remove 'dmso' from ylabels
    ylabels = ylabels[1:]
    ytitle = "Fold change in fluorescence"
    for i in ylabels:
        fold[i] = averages[i]/averages["DMSO"]
    fold = fold.T

    return ylabels, ytitle, fold




def set_dot_params(num_bars, num_reps):
    dotSize = (300/(num_bars))**1.3
    offsetSize = (1/(num_bars))*80
    dotSpacing = [(-0.5 - ((num_reps-2)/2) + 1*x)*offsetSize*1.5
            for x in range(0,num_reps)]

    return dotSize, offsetSize, dotSpacing



