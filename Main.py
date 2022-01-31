import pandas as pd
import numpy as np

Rf = 1.56
GME_data = pd.read_csv('GME.csv')
GME_data["Returns"] = ""
GME_data["From Mean"] = ""

SP_data = pd.read_csv('S&P.csv')
SP_data["Returns"] = ""
SP_data["From Mean"] = ""

class Details:
    def __init__(self, data, mean, varience, covarience, beta, yearly_mean, CAPM):
        self.data = data
        self.mean = mean
        self.varience = varience
        self.covarience = covarience
        self.beta = beta
        self.yearly_mean = yearly_mean
        self.CAPM = CAPM


def varience(mean, data):
    count = 0
    avg_sum2 = 0
    for point in range(1, len(data)):
        count += 1
        avg_sum2 += (mean - data[point]) ** 2
      
    varience = avg_sum2 / count
    return(varience)

def yearly_mean(mean):
    result = ((1 + (mean/100)) ** 330) - 1
 
    return(result)

def ind_return(data):
    stuff = []
    ranger = len(data["Adj Close"])
    mean_sum = 0
    count = 0

    for Adj in range(1, ranger):
        first = (data["Adj Close"][Adj - 1])
        sec = (data["Adj Close"][Adj])
        if isinstance(first, str):
            first = first.replace(",", "").replace(".", "")
            sec = sec.replace(".", "").replace(",", "")
        first = int(first)
        sec = int(sec)
        r = sec - first
        pr = r / first
        mean_sum += float(round(pr, 8) * 100)
        count += 1
  
        data["Returns"][Adj] = float(round(pr, 8) * 100)
    mean = mean_sum / count
    stuff.append(mean)
    thing = varience(mean, data["Returns"])
    stuff.append(thing)

    for Adj in range(1, ranger):
        num = (data["Returns"][Adj]) 
        data["From Mean"][Adj] = num - mean

    return(stuff)
        
def covarience(set1, set2):
    summy = 0
    count = -1 
    set1 = set1["From Mean"]
    set2 = set2["From Mean"]
    for i in range(1, len(set1)):
        product = float(set1[i]) * float(set2[i])
        summy += product
        count += 1
    covarience = summy / count
    return(covarience)
        


GME = Details(GME_data, ind_return(GME_data)[0], ind_return(GME_data)[1], "null", "null", "null", "null")

SP = Details(SP_data, ind_return(SP_data)[0], ind_return(SP_data)[1], "null", "null", "null", "null")

cov1 = covarience(GME_data, SP_data)

GME.covarience = cov1

GME.beta = cov1 / SP.varience

GME.yearly_mean = yearly_mean(GME.mean)

SP.yearly_mean = yearly_mean(SP.mean)


def CAPM(stock):
    result = Rf + (stock.beta * (stock.mean - Rf))
    return result
GME.CAPM = CAPM(GME)
print(GME.CAPM)